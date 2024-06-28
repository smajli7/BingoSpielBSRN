import math
import os
import sys
import random
import time
from random import choice
from rich.console import Console
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.box import SQUARE
from rich.box import HEAVY
from rich.box import HEAVY_EDGE
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import yes_no_dialog, button_dialog
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.formatted_text import HTML
from datetime import datetime

buzzwords_list = []  # erstellt eine leere Liste, wo die Buzzwörter gespeichert werden
console = Console() # erstellt eine Konsole
session = PromptSession() # erstellt eine Session

log_files = {}  # Dictionary zum Speichern der Log-Dateien

def initialize_file(filename): # Funktion, die die Datei einliest
    global buzzwords_list
    try:
        with open(filename) as file:  # öffnet die Datei
            reader = file.readlines()  # liest die Datei ein
            buzzwords_list = [i.strip() for i in reader]  # entfernt die Zeilenumbrüche und speichert die Wörter in der Liste
        random.shuffle(buzzwords_list)  # mischt die Liste, um zufällige Auswahl zu gewährleisten
    except FileNotFoundError:
        console.print(f"Fehler: Datei '{filename}' nicht gefunden.", style="bold red")
        return False
    return True

def get_filename():
    print("\033c", end="", flush=True)  # Löscht die Konsole
    while True:
        filename = session.prompt(HTML("Geben Sie den <ansigreen>Dateinamen</ansigreen> ein, aus dem die Wörter gezogen werden sollen: "))
        if initialize_file(filename):
            return filename
            break
    



def get_player_count():  # Funktion, die die Spieleranzahl abfragt
    while True:
        try:
            console.clear()
            playercount = int(session.prompt(HTML("Geben Sie die <ansicyan>Spieleranzahl</ansicyan> ein: ")))
            return playercount
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")


def get_player_names(playercount):  # Funktion, die die Spielernamen abfragt
    playernamelist = []

    for j in range(playercount): # Schleife, die die Spielernamen abfragt
        playername = prompt(HTML(f"Geben Sie den Namen des <ansimagenta>Spielers {j + 1}</ansimagenta> ein: "))
        playernamelist.append(playername)


        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Spieler Nummer", justify="center") # Tabelle für die Spielernamen
        table.add_column("Spieler Name", justify="center")
        for i, name in enumerate(playernamelist, start=1): # Schleife, die die Spielernamen in die Tabelle einfügt
            table.add_row(str(i), name) # fügt die Spielernamen in die Tabelle ein




    playernames_str = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(playernamelist)])

    if not yes_no_dialog(title="Bestätigung", text=f"Sind diese Spielernamen korrekt?\n\n{playernames_str}").run(): # Bestätigung der Spielernamen
        return get_player_names(playercount) # ruft die Funktion get_player_names erneut auf
    console.print(table) # Ausgabe der Tabelle
    return playernamelist # gibt die Liste der Spielernamen zurück





def get_dimensionx():  # Funktion, die die Spaltenanzahl abfragt
    while True: # Schleife, die die Spaltenanzahl abfragt
        try:
            xsize = int(session.prompt(HTML("Wie viele <ansicyan>Spalten</ansicyan> sollen die Bingokarten haben? (mindestens 2): "))) # Eingabe der Spaltenanzahl
            if xsize > 1:
                return xsize
            else:
                console.print("Fehler: Die Anzahl der Spalten muss größer als 1 sein.", style="bold red") # Fehlermeldung, wenn die Spaltenanzahl kleiner als 2 ist
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red") # Fehlermeldung, wenn die Eingabe keine ganze Zahl ist


def get_dimensiony():  # Funktion, die die Zeilenanzahl abfragt
    while True:
        try:
            ysize = int(session.prompt(HTML("Wie viele <ansicyan>Zeilen</ansicyan> sollen die Bingokarten haben? (mindestens 2): "))) # Eingabe der Zeilenanzahl
            if ysize > 1: # Überprüfung, ob die Zeilenanzahl größer als 1 ist
                return ysize # gibt die Zeilenanzahl zurück
            else: # Fehlermeldung, wenn die Zeilenanzahl kleiner als 2 ist
                console.print("Fehler: Die Anzahl der Zeilen muss größer als 1 sein.", style="bold red")
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")
            
            
def create_log_file(pid):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{timestamp}-bingo-Spieler{pid}.txt"
    log_files[0] = open(filename, 'w')
    log_files[0].write(f"{timestamp} Start des Spiels\n")
    return log_files[0]


def log_event( event):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_files[0].write(f"{timestamp} {event}\n")


def generate_bingo_cards(playernamelist, xsize, ysize):  # Funktion, die die Bingokarten generiert
    matrixlist = []  # Liste der Bingokarten
    middle_x = xsize // 2    # Mitte der x-Achse zur Bestimmung des Jokers
    middle_y = ysize // 2    # Mitte der y-Achse zur Bestimmung des Jokers

    for k in playernamelist:  # for Schleife, die die Bingokarten für jeden Spieler generiert
        if len(buzzwords_list) < xsize * ysize: # Überprüfung, ob genug Buzzwörter vorhanden sind
            raise ValueError("Nicht genug Buzzwords, um die Bingokarten zu füllen") # Fehlermeldung, wenn nicht genug Buzzwörter vorhanden sind
        matrix = [] # Liste für die Bingokarte
        for l in range(ysize):  # zeilen
            b = [] # Liste für die Zeile
            for j in range(xsize):  # spalten
                if xsize % 2 != 0 and ysize % 2 != 0 and l == middle_y and j == middle_x: # Joker in der Mitte, nur wenn xsize und(!) ysize ungerade sind
                    b.append("Joker") # fügt den Joker in die Mitte der Bingokarte ein
                else:
                    random_word = buzzwords_list.pop(0)  # nimmt das erste Element aus der Liste und entfernt es, damit kein Wort doppelt vorkommt
                    b.append(random_word) # fügt das zufällige Wort in die Bingokarte ein
            matrix.append(b) # fügt die Zeile der Bingokarte in die Bingokarte ein
        matrixlist.append(matrix)  # fügt die Bingokartenmatrix einer person in die Bingokartenliste ein
    return matrixlist # gibt die Liste der Bingokarten zurück


def display_bingo_cards(playernamelist, matrixlist, marked_words): # Funktion, die die Bingokarten anzeigt
    print("\033c", end="", flush=True)  # Löscht die Konsole

    console.print("Die Bingokarten wurden generiert. Viel Spaß beim Spielen!", style="bold green")
    for i, matrix in enumerate(matrixlist):  # i ist der Index, matrix ist die Bingokarte

        table = Table(show_header=False, box=HEAVY_EDGE, border_style="bold blue", title=f"[bold blue]Spieler:[/bold blue] [magenta]{playernamelist[i]}[/magenta]")

        for _ in range(len(matrix[0])): # Spaltenanzahl
            table.add_column()

        for row in matrix:  # row ist eine Zeile der Bingokarte
            table.add_row(*[f"[red]{cell}[/red]" if cell in marked_words or cell == "Joker" else str(cell) for cell in row])   # Ausgabe der Bingokarte

        console.print(table)

def check_winner(matrix, marked_words): # Funktion, die überprüft, ob ein Spieler gewonnen hat
    size = len(matrix) # Größe der Bingokarte


    for row in matrix: # Überprüfung der Zeilen
        if all(cell in marked_words or cell == "Joker" for cell in row): # Überprüfung, ob alle Wörter in der Zeile markiert sind
            return True # gibt True zurück, wenn alle Wörter in der Zeile markiert sind


    for col in range(size): # Überprüfung der Spalten
        if all(matrix[row][col] in marked_words or matrix[row][col] == "Joker" for row in range(size)): # Überprüfung, ob alle Wörter in der Spalte markiert sind
            return True # gibt True zurück, wenn alle Wörter in der Spalte markiert sind


    if all(matrix[i][i] in marked_words or matrix[i][i] == "Joker" for i in range(size)): # Überprüfung der Diagonalen
        return True # gibt True zurück, wenn alle Wörter in der Diagonalen markiert sind
    if all(matrix[i][size - 1 - i] in marked_words or matrix[i][size - 1 - i] == "Joker" for i in range(size)): # Überprüfung der Diagonalen
        return True # gibt True zurück, wenn alle Wörter in der Diagonalen markiert sind

    return False # gibt False zurück, wenn kein Spieler gewonnen hat

def mark_word(playernamelist, matrixlist,pid,idlist): # Funktion, die die Wörter markiert
    marked_words = set() # Set für die markierten Wörter
    while True: # Schleife, die die Wörter markiert
        display_bingo_cards(playernamelist, matrixlist, marked_words)# Anzeige der Bingokarten
        word_to_mark = session.prompt("Geben Sie das Wort ein, das Sie markieren oder unmarkieren möchten (oder 'exit' zum Beenden): ") # Eingabe des zu markierenden Worts
        if word_to_mark.lower() == 'exit': # wenn exit dann Spielende
            break # beendet die Schleife
        found = False # Variable, die angibt, ob das Wort gefunden wurde
        for matrix in matrixlist: # Schleife, die die Bingokarten durchgeht
            for row in matrix: # Schleife, die die Zeilen der Bingokarte durchgeht
                if word_to_mark in row: # Überprüfung, ob das Wort in der Zeile enthalten ist
                    if word_to_mark in marked_words: # Überprüfung, ob das Wort bereits markiert ist
                        marked_words.remove(word_to_mark) # entfernt das Wort aus den markierten Wörtern
                    else: # wenn das Wort nicht markiert ist
                        marked_words.add(word_to_mark) # fügt das Wort zu den markierten Wörtern hinzu
                    found = True # setzt die Variable auf True
                    break # beendet die Schleife
            if found: # wenn das Wort gefunden wurde
                break
        lessen(pid)#lesen ob jemand Gewonnen hat

        for i, matrix in enumerate(matrixlist): # Schleife, die die Bingokarten durchgeht
            if check_winner(matrix, marked_words):# Überprüfung, ob ein Spieler gewonnen hat
                display_bingo_cards(playernamelist, matrixlist, marked_words)  # Anzeige
                console.clear()
                log_event("Sieg")  # Loggen des Siegs
                log_event("Ende des Spiels")  # Loggen des Spielendes
                log_files[0].close()
                create_victory_screen(playernamelist[0])#Sieges-Screen anzeigen  
                schrieben(playernamelist[0],pid,idlist)#Gegenern Mitteilen das man Gewonen hat



def create_victory_screen(text):#Funktion zum Erstellen des Sieges-Screens
    
    background_colors = ['green', 'blue', 'magenta', 'yellow', 'cyan']#Hintergrundfarben
   
    victory_text = f"Spieler {text} hat gewonnen!"#Sieger text

    
    
       

    for color in background_colors:#schleife zur Farben wechslung
        console.clear()#console leeren um den siege anzu zeigen
        styled_panel = Panel.fit(f"[bold {color} on black]{victory_text}[/]")#Sieges text mit der Schleifen Farbe
        console.print(styled_panel)#Ausgabe
        time.sleep(1)


    console.clear()#console leeren
    styled_panel = Panel.fit(f"[bold white on blue]{victory_text}[/]")#Sieges text mit wießer box um den satzt
    console.print(styled_panel)#Ausgabe


def send(pipe,pipm):
    fifo=os.open(str(pipe),os.O_WRONLY)#Pipe öffnen zum schreiben
    s=f"{pipm}\n".encode()
    os.write(fifo,s)#Pipe nachricht schreiben
    os.close(fifo)#close pipe
    
def sendfile(pipe,pipm,xs,ys):
   for pa in pipe:
        with open(pa, 'w') as fifo:#öffnet die pipes der gegener um Spieldaten zu schreiben
            fifo.write(pipm + "\n")#Pipe nachricht schreiben
            fifo.flush()  # Sicherstellen, dass die Daten sofort geschrieben werden
            time.sleep(1)
            fifo.write(f"{xs}\n")#Pipe nachricht schreiben
            fifo.flush()  # Sicherstellen, dass die Daten sofort geschrieben werden
            time.sleep(1)
            fifo.write(f"{ys}\n")#Pipe nachricht schreiben
            fifo.flush()  # Sicherstellen, dass die Daten sofort geschrieben werden
            time.sleep(1)
            fifo.close#close pipe
        
def empfang(zahl,pi):
    pipelist=[]#emfangene Pipe von den gegnern und speichert in der liste
    for i in range(1,zahl):#schleife für die anzahl der spieler
        try:
            print(f"es fehlen: {zahl-i} spiler code:{pi}")#Sagt wie viel spieler fehlen
            fifo=os.open(str(pi),os.O_RDONLY)#öffnet eigene pipe um die pipe von den gegenern zu erhalten
            try:
                time.sleep(2)
                daten=os.read(fifo,128)#list die nachricht wieder im bereich 128 byt aus
                pipelist.append(daten.decode().strip())#verwandelt byt UTF-8 in String ohne lerzeichen und  erweiter dies in der liste
            finally:
                os.close(fifo)#close pipe
        except IOError as e:
            print(e)
    return pipelist# Gibt die liste der spiler pipes ohne seine eigen pipe zurück

def empfangfile(pi):
    liste=[]#Spieldaten in liste ab speichern
    with open(pi, 'r') as fifo:#öffnet eigene pipe um die Spieldaten zu erhalten
        while True:
            line = fifo.readline().strip()#verwandelt byt UTF-8 in String ohne lerzeichen 
            if line:
                liste.append(line)
            else:
                fifo.close()#close pipe
                return liste


def lessenid(co):
    liste=[]#spieler pipes
    with open(co, 'r') as fifo:#öffnet eigene pipe um die Pipes von den mitspielern zu erhalten
        while True:
            line = fifo.readline().strip()#verwandelt byt UTF-8 in String ohne lerzeichen 
            if line:
                liste.append(line)
            else:
                fifo.close()#close pipe
                return liste
        
        
     
                 
def schriebid(ji,pi):
    for pa in ji:
        if(pa==pi):#Skipt seine eigene pipe
            continue
        with open(pa, 'w') as fifo:#öffnet die pipes an die die gegner pipes gesendet wreden
            for value in ji:
                fifo.write(value + "\n")#Schreibt die pipes von den gegnern mit zeilenumbruch
                fifo.flush()#Sicherstellen, dass die Daten sofort geschrieben werden
                time.sleep(1)
            fifo.close()#close pipe            
                
                
def lessen(pi4):
    try:
        fifo=os.open(pi4,os.O_RDONLY | os.O_NONBLOCK)#öffnet seine eigene pipe als nur lessen und nicht blockirend
     
        time.sleep(1)
        daten=os.read(fifo,128)#liset aus der pipe mit eine geben breich 128 byt kann auch mehr sein des do größer die nachricht ist
        if daten:#wen daten vorhanden sind
            ergebnis=daten.decode().strip()#verwandelt byt UTF-8 in String ohne lerzeichen
            log_event("Ende des Spiels")
            log_files[0].close()
            create_victory_screen(ergebnis)#Sieger-Screen anzeigen 
            time.sleep(4)
            os.unlink(pi4)#löschung der Pipes
            os.close(fifo)#close pipe
            sys.exit()#System Beneden
    except IOError as e:
        print(e)     
                    
        
    
         
                 
def schrieben(name,pi6,paths):
    for i in paths:#geht durch jede gegenerische pipe
        if(i==pi6):#Skipt seine eigene pipe
            continue
        fifo=os.open(i,os.O_WRONLY)#Pipe öffnen zum schreiben des Siegers
        s=f"{name}".encode()#verwandelt String in byt UTF-8
        os.write(fifo,s)#Pipe Gewinner nachricht schreiben
        os.close(fifo)#close pipe
    os.unlink(pi6)#löschung der Pipes
    sys.exit() #System Beneden
               
def namedpipe(piname):#Methode zu generirung der fifo Pipes
    if not os.path.exists(piname):#checkt ob solch eine pipe schon gibt
        os.mkfifo(piname)#Generirt die Pipe
        
def start_game():  # Funktion, die das Spiel startet
    pid=os.getpid()#prozess id hersufinden
    pids=str(pid)#prozess id in String umändern
    namedpipe(pids)#generirt Benante FIFO pipe
    try:
        while True:#While schleife für die erfassung des Befehls
            #überprüft welche eingabe gemacht worden ist
            JN=str(input("joinround or newround"))# Fragen ob er joinen will oder eine runde erstellen will
            if(JN=="newround"):
                file=get_filename() # Filename wird initialisiert und als String zurück gegeben
                playercount = get_player_count() # Spieleranzahl wird übernommen
                playernamelist = get_player_names(1) # Spierliste
                xsize = get_dimensionx() #x
                ysize = get_dimensiony() #y
                create_log_file(pids) 
                matrixlist = generate_bingo_cards(playernamelist, xsize, ysize) # Spielfeld wird generiert
                
                if(playercount>1):
                    spieler_ids=empfang(playercount,pid)#Methode welche die liste der gegnerische pips spiel ermittelt und zurück gibt
                    sendfile(spieler_ids,file,xsize,ysize)#Methode zur sendung von spiel informationen
                    spieler_ids.append(f"{pids}\n")#ergnzung der eigene pipe
                    time.sleep(2)#seit für verabeitung von den gegenerischen spiler
                    schriebid(spieler_ids,pids)#snedet die Spielder pips liste an die Gegnerischen spieler
                mark_word(playernamelist, matrixlist,pids,spieler_ids)
            elif(JN=="joinround"):
                vr=str(input("code"))#input von der newround pipe zur komunikation
                send(vr,pids)#Senden der eigen pipe and die newround prozesses
                filename=empfangfile(pids)#Empfangen von Spiel informationen vom newround prozesses
                initialize_file(filename[0])#Benutz die empfange daten zur generirung des Spieles
                playernamelist = get_player_names(1)#Spieler namen erfassen
                spie=lessenid(pids)#lesen der Gegnerische pipes
                matrixlist = generate_bingo_cards(playernamelist, int(filename[1]), int(filename[2]))# Spielfeld wird generiert
                create_log_file(pids)
                mark_word(playernamelist, matrixlist,pids,spie) # Funktion zur Markierung von Wörtern
            else:print("Falsche eingabe, bitte noch mal versuchen")#Print für falsch eingaben
    except KeyboardInterrupt:#exceptions zur löschung der Pipes
        os.unlink(pids)    
    except FileNotFoundError:
        os.unlink(pids)  
    except BrokenPipeError:
        os.unlink(pids)  
    except IOError:
        os.unlink(pids)            

if __name__ == "__main__":  # wird ausgeführt, wenn das Skript direkt ausgeführt wird
    start_game()  # ruft die Funktion start_game auf

import os
import sys
import random
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import HEAVY_EDGE
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import yes_no_dialog, button_dialog, prompt
from prompt_toolkit.formatted_text import HTML
from datetime import datetime

buzzwords_list = []  # Erstellt eine leere Liste, wo die Buzzwörter gespeichert werden
console = Console()  # Erstellt eine Konsole
session = PromptSession()  # Erstellt eine Session

log_files = {}  # Dictionary zum Speichern der Log-Dateien

def initialize_file(filename):  # Funktion, die die Datei einliest
    global buzzwords_list
    try:
        with open(filename) as file:  # Öffnet die Datei
            reader = file.readlines()  # Liest die Datei ein
            buzzwords_list = [i.strip() for i in reader]  # Entfernt die Zeilenumbrüche und speichert die Wörter in der Liste
        random.shuffle(buzzwords_list)  # Mischt die Liste, um zufällige Auswahl zu gewährleisten
    except FileNotFoundError:
        console.print(f"Fehler: Datei '{filename}' nicht gefunden.", style="bold red")
        return False
    return True

def get_filename():
    print("\033c", end="", flush=True)  # Löscht die Konsole
    while True:
        filename = session.prompt(
            HTML("Geben Sie den <ansigreen>Dateinamen</ansigreen> ein, aus dem die Wörter gezogen werden sollen: "))
        if initialize_file(filename):
            return filename

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

    for j in range(playercount):  # Schleife, die die Spielernamen abfragt
        playername = prompt(HTML(f"Geben Sie den Namen des <ansimagenta>Spielers {j + 1}</ansimagenta> ein: "))
        playernamelist.append(playername)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Spieler Nummer", justify="center")  # Tabelle für die Spielernamen
        table.add_column("Spieler Name", justify="center")
        for i, name in enumerate(playernamelist, start=1):  # Schleife, die die Spielernamen in die Tabelle einfügt
            table.add_row(str(i), name)  # Fügt die Spielernamen in die Tabelle ein

    playernames_str = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(playernamelist)])

    if not yes_no_dialog(title="Bestätigung",
                         text=f"Sind diese Spielernamen korrekt?\n\n{playernames_str}").run():  # Bestätigung der Spielernamen
        return get_player_names(playercount)  # Ruft die Funktion get_player_names erneut auf
    console.print(table)  # Ausgabe der Tabelle
    return playernamelist  # Gibt die Liste der Spielernamen zurück

def get_dimensionx():  # Funktion, die die Spaltenanzahl abfragt
    while True:  # Schleife, die die Spaltenanzahl abfragt
        try:
            xsize = int(session.prompt(HTML(
                "Wie viele <ansicyan>Spalten</ansicyan> sollen die Bingokarten haben? (mindestens 2): ")))  # Eingabe der Spaltenanzahl
            if xsize > 1:
                return xsize
            else:
                console.print("Fehler: Die Anzahl der Spalten muss größer als 1 sein.",
                              style="bold red")  # Fehlermeldung, wenn die Spaltenanzahl kleiner als 2 ist
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.",
                          style="bold red")  # Fehlermeldung, wenn die Eingabe keine ganze Zahl ist

def get_dimensiony():  # Funktion, die die Zeilenanzahl abfragt
    while True:
        try:
            ysize = int(session.prompt(HTML(
                "Wie viele <ansicyan>Zeilen</ansicyan> sollen die Bingokarten haben? (mindestens 2): ")))  # Eingabe der Zeilenanzahl
            if ysize > 1:  # Überprüfung, ob die Zeilenanzahl größer als 1 ist
                return ysize  # Gibt die Zeilenanzahl zurück
            else:  # Fehlermeldung, wenn die Zeilenanzahl kleiner als 2 ist
                console.print("Fehler: Die Anzahl der Zeilen muss größer als 1 sein.", style="bold red")
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")

def create_log_file(pid):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{timestamp}-bingo-Spieler{pid}.txt"
    log_files[0] = open(filename, 'w')
    log_files[0].write(f"{timestamp} Start des Spiels\n")
    return log_files[0]

def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_files[0].write(f"{timestamp} {event}\n")

def generate_bingo_cards(playernamelist, xsize, ysize):  # Funktion, die die Bingokarten generiert
    matrixlist = []  # Liste der Bingokarten
    middle_x = xsize // 2  # Mitte der x-Achse zur Bestimmung des Jokers
    middle_y = ysize // 2  # Mitte der y-Achse zur Bestimmung des Jokers

    for k in playernamelist:  # Schleife, die die Bingokarten für jeden Spieler generiert
        if len(buzzwords_list) < xsize * ysize:  # Überprüfung, ob genug Buzzwörter vorhanden sind
            raise ValueError(
                "Nicht genug Buzzwords, um die Bingokarten zu füllen")  # Fehlermeldung, wenn nicht genug Buzzwörter vorhanden sind
        used_words = set()  # Set für verwendete Wörter
        matrix = []  # Liste für die Bingokarte
        for l in range(ysize):  # Zeilen
            b = []  # Liste für die Zeile
            for j in range(xsize):  # Spalten
                if xsize % 2 != 0 and ysize % 2 != 0 and l == middle_y and j == middle_x:  # Joker in der Mitte, nur wenn xsize und ysize ungerade sind
                    b.append("Joker")  # Fügt den Joker in die Mitte der Bingokarte ein
                else:
                    while True:
                        random_word = buzzwords_list.pop(0)  # Nimmt das erste Element aus der Liste und entfernt es, damit kein Wort doppelt vorkommt
                        if random_word not in used_words:  # Überprüfung, ob das Wort bereits verwendet wurde
                            used_words.add(random_word)  # Fügt das Wort zu den verwendeten Wörtern hinzu
                            b.append(random_word)  # Fügt das zufällige Wort in die Bingokarte ein
                            break  # Beendet die Schleife, wenn ein neues Wort gefunden wurde
                    buzzwords_list.append(random_word)  # Füge das Wort zurück zur Liste, damit es nicht verloren geht
            matrix.append(b)  # Fügt die Zeile der Bingokarte in die Bingokarte ein
        matrixlist.append(matrix)  # Fügt die Bingokartenmatrix einer Person in die Bingokartenliste ein
    return matrixlist  # Gibt die Liste der Bingokarten zurück


def display_bingo_cards(playernamelist, matrixlist, marked_words):  # Funktion, die die Bingokarten anzeigt
    print("\033c", end="", flush=True)  # Löscht die Konsole

    console.print("Die Bingokarten wurden generiert. Viel Spaß beim Spielen!", style="bold green")
    for i, matrix in enumerate(matrixlist):  # i ist der Index, matrix ist die Bingokarte

        table = Table(show_header=False, box=HEAVY_EDGE, border_style="bold blue",
                      title=f"[bold blue]Spieler:[/bold blue] [magenta]{playernamelist[i]}[/magenta]")

        for _ in range(len(matrix[0])):  # Spaltenanzahl
            table.add_column()

        for row in matrix:  # row ist eine Zeile der Bingokarte
            table.add_row(*[f"[red]{cell}[/red]" if cell in marked_words or cell == "Joker" else str(cell) for cell in row])  # Ausgabe der Bingokarte

        console.print(table)

def check_winner(matrix, marked_words):  # Funktion, die überprüft, ob ein Spieler gewonnen hat
    size = len(matrix)  # Größe der Bingokarte

    for row in matrix:  # Überprüfung der Zeilen
        if all(cell in marked_words or cell == "Joker" for cell in row):  # Überprüfung, ob alle Wörter in der Zeile markiert sind
            return True  # Gibt True zurück, wenn alle Wörter in der Zeile markiert sind

    for col in range(size):  # Überprüfung der Spalten
        if all(matrix[row][col] in marked_words or matrix[row][col] == "Joker" for row in range(size)):  # Überprüfung, ob alle Wörter in der Spalte markiert sind
            return True  # Gibt True zurück, wenn alle Wörter in der Spalte markiert sind

    if all(matrix[i][i] in marked_words or matrix[i][i] == "Joker" for i in range(size)):  # Überprüfung der Diagonalen
        return True  # Gibt True zurück, wenn alle Wörter in der Diagonalen markiert sind
    if all(matrix[i][size - 1 - i] in marked_words or matrix[i][size - 1 - i] == "Joker" for i in range(size)):  # Überprüfung der Diagonalen
        return True  # Gibt True zurück, wenn alle Wörter in der Diagonalen markiert sind

    return False  # Gibt False zurück, wenn kein Spieler gewonnen hat

def mark_word(playernamelist, matrixlist, pid, idlist):  # Funktion, die die Wörter markiert
    marked_words = set()  # Set für die markierten Wörter
    if len(idlist) > 0:  # Prüft nur, wenn mehrere Spieler drin sind
        lesen(pid)  # Lesen, ob jemand gewonnen hat
    while True:  # Schleife, die die Wörter markiert
        display_bingo_cards(playernamelist, matrixlist, marked_words)  # Anzeige der Bingokarten
        word_to_mark = session.prompt(
            "Geben Sie das Wort ein, das Sie markieren oder unmarkieren möchten (oder 'exit' zum Beenden): ")  # Eingabe des zu markierenden Worts
        if word_to_mark.lower() == 'exit':  # wenn exit dann Spielende
            break  # Beendet die Schleife
        found = False  # Variable, die angibt, ob das Wort gefunden wurde
        for matrix in matrixlist:  # Schleife, die die Bingokarten durchgeht
            for row in matrix:  # Schleife, die die Zeilen der Bingokarte durchgeht
                if word_to_mark in row:  # Überprüfung, ob das Wort in der Zeile enthalten ist
                    if word_to_mark in marked_words:  # Überprüfung, ob das Wort bereits markiert ist
                        marked_words.remove(word_to_mark)  # Entfernt das Wort aus den markierten Wörtern
                    else:  # Wenn das Wort nicht markiert ist
                        marked_words.add(word_to_mark)  # Fügt das Wort zu den markierten Wörtern hinzu
                    found = True  # Setzt die Variable auf True
                    break  # Beendet die Schleife
            if found:  # Wenn das Wort gefunden wurde
                break
        if len(idlist) > 0:  # Prüft nur, wenn mehrere Spieler drin sind
            lesen(pid)  # Lesen, ob jemand gewonnen hat

        for i, matrix in enumerate(matrixlist):  # Schleife, die die Bingokarten durchgeht
            if check_winner(matrix, marked_words):  # Überprüfung, ob ein Spieler gewonnen hat
                display_bingo_cards(playernamelist, matrixlist, marked_words)  # Anzeige
                console.clear()
                log_event("Sieg")  # Loggen des Siegs
                log_event("Ende des Spiels")  # Loggen des Spielendes
                log_files[0].close()
                create_victory_screen(playernamelist[0])  # Sieges-Screen anzeigen
                if len(idlist) == 0:  # Unlinken, wenn man selbst spielte
                    os.unlink(pid)
                    sys.exit()
                if len(idlist) > 0:  # Schaut, ob mehrere Spieler drin sind
                    schreiben(playernamelist[0], pid, idlist)  # Gegnern mitteilen, dass man gewonnen hat

def create_victory_screen(text):  # Funktion zum Erstellen des Sieges-Screens
    background_colors = ['green', 'blue', 'magenta', 'yellow', 'cyan']  # Hintergrundfarben
    victory_text = f"Spieler {text} hat gewonnen!"  # Siegertext

    for color in background_colors:  # Schleife zur Farbwechselung
        console.clear()  # Konsole leeren, um den Sieg anzuzeigen
        styled_panel = Panel.fit(f"[bold {color} on black]{victory_text}[/]")  # Siegestext mit der Schleifenfarbe
        console.print(styled_panel)  # Ausgabe
        time.sleep(1)

    console.clear()  # Konsole leeren
    styled_panel = Panel.fit(f"[bold yellow]{victory_text}[/]")  # Siegestext mit weißer Box um den Satz
    console.print(styled_panel)  # Ausgabe

def send(pipe, pipm):
    fifo = os.open(str(pipe), os.O_WRONLY)  # Pipe öffnen zum Schreiben
    s = f"{pipm}\n".encode()
    os.write(fifo, s)  # Pipe-Nachricht schreiben
    os.close(fifo)  # Pipe schließen

def empfang(zahl, pi):
    pipelist = []  # Empfangene Pipe von den Gegnern und speichert in der Liste
    for i in range(1, zahl):  # Schleife für die Anzahl der Spieler
        try:
            console.print(f"[bold red]Es fehlen:[/bold red] [bold yellow]{zahl - i}[/bold yellow] Spieler")
            console.print(f"[bold green]Spielcode:[/bold green] [bold cyan]{pi}[/bold cyan]")  # Sagt, wie viele Spieler fehlen
            fifo = os.open(str(pi), os.O_RDONLY)  # Öffnet eigene Pipe, um die Pipe von den Gegnern zu erhalten
            try:
                daten = os.read(fifo, 128)  # Liest die Nachricht wieder im Bereich 128 Byte aus
                pipelist.append(daten.decode().strip())  # Verwandelt Byte UTF-8 in String ohne Leerzeichen und erweitert dies in der Liste
            finally:
                os.close(fifo)  # Pipe schließen
        except IOError as e:
            print(e)
    return pipelist  # Gibt die Liste der Spieler-Pipes ohne eigene Pipe zurück

def sendfile(pipe, pids2, pipm1, xs, ys):
    for pa in pipe:

        with open(pa, 'w') as fifo:  # Öffnet die Pipes der Gegner, um Spieldaten zu schreiben
            fifo.write(f"{pipm1}\n")  # Pipe-Nachricht schreiben
            fifo.write(f"{xs}\n")  # Pipe-Nachricht schreiben
            fifo.write(f"{ys}\n")  # Pipe-Nachricht schreiben
            for value in pids2:
                fifo.write(value + "\n")  # Schreibt die Pipes der Gegner mit Zeilenumbruch
            fifo.flush()  # Sicherstellen, dass die Daten sofort geschrieben werden

def empfangfile(pi):
    liste = []  # Spieldaten in Liste abspeichern
    with open(pi, 'r') as fifo:  # Öffnet eigene Pipe, um die Spieldaten zu erhalten
        while True:
            line = fifo.readline().strip()  # Verwandelt Byte UTF-8 in String ohne Leerzeichen
            if line:
                liste.append(line)
            else:
                return liste  # Gibt die Liste zurück

def lesen(pi4):
    try:
        fifo = os.open(pi4, os.O_RDONLY | os.O_NONBLOCK)  # Öffnet eigene Pipe nur zum Lesen und nicht blockierend
        daten = os.read(fifo, 128)  # Liest aus der Pipe im Bereich 128 Byte, kann auch mehr sein, desto größer die Nachricht ist
        if daten:  # Wenn Daten vorhanden sind
            ergebnis = daten.decode().strip()  # Verwandelt Byte UTF-8 in String ohne Leerzeichen
            log_event("Ende des Spiels")
            log_files[0].close()
            create_victory_screen(ergebnis)  # Sieger-Screen anzeigen
            os.unlink(pi4)  # Löschen der Pipes
            os.close(fifo)  # Pipe schließen
            sys.exit()  # System beenden
    except IOError as e:
        print(e)

def schreiben(name, pi6, paths):
    for i in paths:  # Geht durch jede gegnerische Pipe
        if i == pi6:  # Skipt eigene Pipe
            continue
        fifo = os.open(i, os.O_WRONLY)  # Pipe öffnen zum Schreiben des Siegers
        s = f"{name}".encode()  # Verwandelt String in Byte UTF-8
        os.write(fifo, s)  # Pipe-Gewinner-Nachricht schreiben
        os.close(fifo)  # Pipe schließen
    os.unlink(pi6)  # Löschen der Pipes
    sys.exit()  # System beenden

def namedpipe(piname):  # Methode zur Generierung der FIFO-Pipes
    if not os.path.exists(piname):  # Prüft, ob eine solche Pipe schon existiert
        os.mkfifo(piname)  # Generiert die Pipe

def start_game():  # Funktion, die das Spiel startet
    pid = os.getpid()  # Prozess-ID herausfinden
    pids = str(pid)  # Prozess-ID in String umwandeln
    namedpipe(pids)  # Generiert benannte FIFO-Pipe
    try:
        while True:  # While-Schleife zur Erfassung des Befehls
            # Überprüft, welche Eingabe gemacht worden ist
            JN = prompt(HTML('<ansigreen>joinround</ansigreen> / <ansicyan>newround</ansicyan>? ')) # Fragt, ob der Nutzer beitreten oder eine neue Runde erstellen möchte
            if JN == "newround":
                file = get_filename()  # Dateiname wird initialisiert und als String zurückgegeben
                playercount = get_player_count()  # Spieleranzahl wird übernommen
                playernamelist = get_player_names(1)  # Spielerliste
                xsize = get_dimensionx()  # x
                ysize = get_dimensiony()  # y
                create_log_file(pids)
                matrixlist = generate_bingo_cards(playernamelist, xsize, ysize)  # Spielfeld wird generiert
                spieler_ids = []
                if playercount > 1:
                    spieler_ids1 = empfang(playercount, pid)  # Methode, welche die Liste der gegnerischen Pipes ermittelt und zurückgibt
                    spieler_ids.append(f"{pids}\n")  # Ergänzung der eigenen Pipe
                    sendfile(spieler_ids1, spieler_ids, file, xsize, ysize)  # Methode zur Sendung von Spielinformationen
                    time.sleep(2)  # Zeit für Verarbeitung von den gegnerischen Spielern
                mark_word(playernamelist, matrixlist, pids, spieler_ids)
                break
            if JN == "joinround":
                vr = str(input("\nSpielcode: "))  # Input von der newround-Pipe zur Kommunikation
                send(vr, pids)  # Senden der eigenen Pipe an die newround-Prozesse
                filename = empfangfile(pids)  # Empfangen von Spielinformationen vom newround-Prozess
                initialize_file(filename[0])  # Benutzt die empfangenen Daten zur Generierung des Spiels
                playernamelist = get_player_names(1)  # Spielernamen erfassen
                matrixlist = generate_bingo_cards(playernamelist, int(filename[1]), int(filename[2]))  # Spielfeld wird generiert
                create_log_file(pids)
                del filename[:3]  # Löscht die ersten 3 Positionen
                mark_word(playernamelist, matrixlist, pids, filename)  # Funktion zur Markierung von Wörtern
                break
            else:
                console.print("[bold red]Falsche Eingabe, bitte noch mal versuchen[/bold red]")
    except KeyboardInterrupt:  # Exceptions zur Löschung der Pipes
        os.unlink(pids)
    except FileNotFoundError:
        os.unlink(pids)
    except BrokenPipeError:
        os.unlink(pids)
    except IOError:
        os.unlink(pids)

if __name__ == "__main__":  # Wird ausgeführt, wenn das Skript direkt ausgeführt wird
    start_game()  # Ruft die Funktion start_game auf

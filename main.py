import math
import random
from random import choice
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from rich.box import HEAVY
from rich.box import HEAVY_EDGE
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import yes_no_dialog, button_dialog
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.formatted_text import HTML

buzzwords_list = []  # erstellt eine leere Liste, wo die Buzzwörter gespeichert werden
console = Console() # erstellt eine Konsole
session = PromptSession() # erstellt eine Session


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

def mark_word(playernamelist, matrixlist): # Funktion, die die Wörter markiert
    marked_words = set() # Set für die markierten Wörter
    while True: # Schleife, die die Wörter markiert
        display_bingo_cards(playernamelist, matrixlist, marked_words) # Anzeige der Bingokarten
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


        for i, matrix in enumerate(matrixlist): # Schleife, die die Bingokarten durchgeht
            if check_winner(matrix, marked_words): # Überprüfung, ob ein Spieler gewonnen hat
                display_bingo_cards(playernamelist, matrixlist, marked_words)  # Anzeige
                console.print(f"Spieler {playernamelist[i]} hat gewonnen!", style="bold green") # Ausgabe des Gewinners
                return # beendet die Funktion
    console.print("Das Spiel ist beendet. Danke fürs Spielen!", style="bold green") # Ausgabe, wenn das Spiel beendet ist

def start_game():  # Funktion, die das Spiel startet
    get_filename() # Filename wird initialisiert
    playercount = get_player_count() # Spieleranzahl wird übernommen
    playernamelist = get_player_names(playercount) # Spierliste
    xsize = get_dimensionx() #x
    ysize = get_dimensiony() #y
    matrixlist = generate_bingo_cards(playernamelist, xsize, ysize) # Spielfeld wird generiert
    mark_word(playernamelist, matrixlist) # Funktion zur Markierung von Wörtern


if __name__ == "__main__":  # wird ausgeführt, wenn das Skript direkt ausgeführt wird
    start_game()  # ruft die Funktion start_game auf

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

buzzwords_list = []  # erstellt eine leere Liste, wo die Buzzwörter gespeichert werden.
console = Console()
session = PromptSession()


def initialize_file(filename):  # diese Funktion füllt die Liste mit dem Inhalt aus der angegebenen Datei.
    global buzzwords_list
    try:
        with open(filename) as file:  # öffnet die Datei.
            reader = file.readlines()  # liest die Datei ein.
            buzzwords_list = [i.strip() for i in reader]  # entfernt die Zeilenumbrüche und speichert die Wörter in der Liste.
        random.shuffle(buzzwords_list)  # mischt die Liste, um zufällige Auswahl zu gewährleisten.
    except FileNotFoundError:
        console.print(f"Fehler: Datei '{filename}' nicht gefunden.", style="bold red")
        return False
    return True

def get_filename():
    print("\033c", end="", flush=True)  # clears the console
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


def get_player_names(playercount):  # Funktion, die die Spielernamen abfragt.
    playernamelist = []

    for j in range(playercount):
        playername = prompt(HTML(f"Geben Sie den Namen des <ansimagenta>Spielers {j + 1}</ansimagenta> ein: "))
        playernamelist.append(playername)

        # Displaying the table after each input
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Spieler Nummer", justify="center")
        table.add_column("Spieler Name", justify="center")
        for i, name in enumerate(playernamelist, start=1):
            table.add_row(str(i), name)




    playernames_str = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(playernamelist)])

    if not yes_no_dialog(title="Bestätigung", text=f"Sind diese Spielernamen korrekt?\n\n{playernames_str}").run():
        return get_player_names(playercount)
    console.print(table)
    return playernamelist





def get_dimensionx():  # Funktion, die die Spaltenanzahl abfragt.
    while True:
        try:
            xsize = int(session.prompt(HTML("Wie viele <ansicyan>Spalten</ansicyan> sollen die Bingokarten haben? (mindestens 2): ")))
            if xsize > 1:
                return xsize
            else:
                console.print("Fehler: Die Anzahl der Spalten muss größer als 1 sein.", style="bold red")
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")


def get_dimensiony():  # Funktion, die die Zeilenanzahl abfragt.
    while True:
        try:
            ysize = int(session.prompt(HTML("Wie viele <ansicyan>Zeilen</ansicyan> sollen die Bingokarten haben? (mindestens 2): ")))
            if ysize > 1:   
                return ysize
            else:
                console.print("Fehler: Die Anzahl der Zeilen muss größer als 1 sein.", style="bold red")
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")


def generate_bingo_cards(playernamelist, xsize, ysize):  # Funktion, die die Bingokarten generiert.
    global buzzwords_list
    matrixlist = []  # Liste der Bingokarten.
    middle_x = xsize // 2
    middle_y = ysize // 2

    for k in playernamelist:  # for Schleife, die die Bingokarten für jeden Spieler generiert.
        if len(buzzwords_list) < xsize * ysize:
            raise ValueError("Nicht genug Buzzwords, um die Bingokarten zu füllen")
        matrix = []
        for l in range(ysize):  # zeilen
            b = []
            for j in range(xsize):  # spalten
                if xsize % 2 != 0 and ysize % 2 != 0 and l == middle_y and j == middle_x:
                    b.append(0)  # Joker in der Mitte, nur wenn xsize und ysize ungerade sind
                else:
                    random_word = buzzwords_list.pop(0)  # nimmt das erste Element aus der Liste und entfernt es, damit kein Wort doppelt vorkommt
                    b.append(random_word)
            matrix.append(b)
        matrixlist.append(matrix)  # fügt die bingokartenmatrix einer person in die bingokartenliste ein
    return matrixlist


def display_bingo_cards(playernamelist, matrixlist, marked_words):
    print("\033c", end="", flush=True)  # clears the console

    console.print("Die Bingokarten wurden generiert. Viel Spaß beim Spielen!", style="bold green")
    for i, matrix in enumerate(matrixlist):  # i ist der Index, matrix ist die Bingokarte

        table = Table(show_header=False, box=HEAVY_EDGE, border_style="bold blue", title=f"[bold blue]Spieler:[/bold blue] [magenta]{playernamelist[i]}[/magenta]")
        # Adding columns for each column in the bingo card
        for _ in range(len(matrix[0])):
            table.add_column()

        for row in matrix:  # row ist eine Zeile der Bingokarte
            table.add_row(*[f"[red]{cell}[/red]" if cell in marked_words or cell == 0 else str(cell) for cell in row])   # Ausgabe der Bingokarte

        console.print(table)

def check_winner(matrix, marked_words):
    size = len(matrix)

    # rows
    for row in matrix:
        if all(cell in marked_words or cell == 0 for cell in row): 
            return True

    # columns
    for col in range(size):
        if all(matrix[row][col] in marked_words or matrix[row][col] == 0 for row in range(size)):
            return True

       # diagonals
    if all(matrix[i][i] in marked_words or matrix[i][i] == 0 for i in range(size)):
        return True
    if all(matrix[i][size - 1 - i] in marked_words or matrix[i][size - 1 - i] == 0 for i in range(size)):
        return True

    return False 

def mark_word(playernamelist, matrixlist):
    marked_words = set()
    while True:
        display_bingo_cards(playernamelist, matrixlist, marked_words)
        word_to_mark = session.prompt("Geben Sie das Wort ein, das Sie markieren oder unmarkieren möchten (oder 'exit' zum Beenden): ")
        if word_to_mark.lower() == 'exit': # wenn exit dann Spielende
            break
        found = False
        for matrix in matrixlist:
            for row in matrix:
                if word_to_mark in row:
                    if word_to_mark in marked_words:
                        marked_words.remove(word_to_mark)
                    else:
                        marked_words.add(word_to_mark)
                    found = True
                    break
            if found:
                break

        # Mark the word and then check for winners
        for i, matrix in enumerate(matrixlist):
            if check_winner(matrix, marked_words):
                display_bingo_cards(playernamelist, matrixlist, marked_words)  # Anzeige
                console.print(f"Spieler {playernamelist[i]} hat gewonnen!", style="bold green")
                return
    console.print("Das Spiel ist beendet. Danke fürs Spielen!", style="bold green")

def start_game():  # Funktion, die das Spiel startet.
    get_filename() # Filename wird initialisiert
    playercount = get_player_count() #Spieleranzahl wird übernommen
    playernamelist = get_player_names(playercount) #Spierliste
    xsize = get_dimensionx() #x
    ysize = get_dimensiony() #y
    matrixlist = generate_bingo_cards(playernamelist, xsize, ysize) #Spielfeld wird generiert
    mark_word(playernamelist, matrixlist) #Funktion zur Markierung von Wörtern


if __name__ == "__main__":  # wird ausgeführt, wenn das Skript direkt ausgeführt wird.
    start_game()  # ruft die Funktion start_game auf.

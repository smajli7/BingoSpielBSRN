import math
import random
from random import choice
from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from rich.box import HEAVY
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import yes_no_dialog

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
    while True:
        filename = session.prompt("Geben Sie den Dateinamen ein, aus dem die Wörter gezogen werden sollen: ")
        if initialize_file(filename):
            break



def get_player_count():  # Funktion, die die Spieleranzahl abfragt.
    while True:
        try:
            console.clear()
            playercount = int(session.prompt("Geben Sie die Spieleranzahl ein: "))
            return playercount
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")


def get_player_names(playercount):  # Funktion, die die Spielernamen abfragt.
    playernamelist = []

    for j in range(playercount):
        playername = session.prompt(f"Geben Sie den Namen des Spielers {j + 1} ein: ")
        playernamelist.append(playername)

        # Displaying the table after each input
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Spieler Nummer", justify="center")
        table.add_column("Spieler Name", justify="center")
        console.clear()
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
            xsize = int(session.prompt("Wie viele Spalten sollen die Bingokarten haben? "))
            return xsize
        except ValueError:
            console.print("Fehler: Die Eingabe muss eine ganze Zahl sein.", style="bold red")


def get_dimensiony():  # Funktion, die die Zeilenanzahl abfragt.
    while True:
        try:
            ysize = int(session.prompt("Wie viele Zeilen sollen die Bingokarten haben? "))
            return ysize
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



def display_bingo_cards(playernamelist, matrixlist):
    for i, matrix in enumerate(matrixlist):  # i ist der Index, matrix ist die Bingokarte
        console.print(f"\nBingokarte für [bold]{playernamelist[i]}[/bold]:")  # Ausgabe des Spielernamens

        table = Table(show_header=False, box=HEAVY, header_style="bold blue")

        # Adding columns for each column in the bingo card
        for _ in range(len(matrix[0])):
            table.add_column()

        for row in matrix:  # row ist eine Zeile der Bingokarte
            table.add_row(*[str(cell) for cell in row])

        console.print(table)


def start_game():  # Funktion, die das Spiel startet.
    get_filename()
    playercount = get_player_count()
    playernamelist = get_player_names(playercount)
    xsize = get_dimensionx()
    ysize = get_dimensiony()
    matrixlist = generate_bingo_cards(playernamelist, xsize, ysize)
    display_bingo_cards(playernamelist, matrixlist)


if __name__ == "__main__":  # wird ausgeführt, wenn das Skript direkt ausgeführt wird.
    start_game()  # ruft die Funktion start_game auf.

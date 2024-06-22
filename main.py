import TermTk as ttk
import math
from random import choice  # importiert nur das choice aus dem Modul random.

buzzwords_list = []  # erstellt eine leere Liste, wo die Buzzwörter gespeichert werden.

def initialize_file():  # diese Funktion füllt die Liste mit dem Inhalt aus buzzwords.txt.
    with open("buzzwords.txt") as file:  # öffnet die Datei.
        reader = file.readlines()  # liest die Datei ein.
        for i in reader:  # for Schleife, die jedes Element der Liste durchläuft.
            i = i.strip()  # entfernt die Zeilenumbrüche.
            buzzwords_list.append(i)  # fügt die Buzzwörter aus der Liste hinzu.

initialize_file()  # ruft die Funktion auf.

matrixlist = []  # Liste der Bingokarten.

def get_player_count(): # Funktion, die die Spieleranzahl abfragt.
    while True:
        playercount = input("Geben Sie die Spieleranzahl ein: ")
        try:
            playercount = int(playercount)
            return playercount;
        except ValueError:
            try:
                float(playercount)
                print("Fehler: Die eingegebene Zahl darf keine Kommazahl sein.")
            except ValueError:
                print("Fehler: Die Eingabe muss eine Zahl sein.")

def get_player_names(playercount):  # Funktion, die die Spielernamen abfragt.
    playernamelist = []
    for j in range(playercount):
        playername = input("Geben Sie den Namen des Spielers ein: ")
        playernamelist.append(playername)
    return playernamelist

def get_dimensionx():    # Funktion, die die Spaltenanzahl abfragt.
    while True:
        xsize = input("Wie viele Spalten sollen die Bingokarten haben? ")
        try:
            xsize = int(xsize)  # bestimmt die Spaltenanzahl
            return xsize
        except ValueError:
            try:
                float(xsize)
                print("Fehler: Die eingegebene Zahl darf keine Kommazahl sein.")
            except ValueError:
                print("Fehler: Die Eingabe muss eine Zahl sein.")

def get_dimensiony(): # Funktion, die die Zeilenanzahl abfragt.
    while True:
        ysize = input("Wie viele Zeilen sollen die Bingokarten haben? ")
        try:
            ysize = int(ysize)  # bestimmt die Zeilenanzahl.
            return ysize
        except ValueError:
            try:
                float(ysize)
                print("Fehler: Die eingegebene Zahl darf keine Kommazahl sein.")
            except ValueError:
                print("Fehler: Die Eingabe muss eine Zahl sein.")

def generate_bingo_cards(playernamelist, xsize, ysize): # Funktion, die die Bingokarten generiert.
    matrixlist = []  # Liste der Bingokarten.
    middle_x = xsize // 2
    middle_y = ysize // 2

    for k in playernamelist:    # for Schleife, die die Bingokarten für jeden Spieler generiert.
        matrix = []
        for l in range(ysize):  # zeilen
            b = []
            for j in range(xsize):  # spalten
                if xsize % 2 != 0 and ysize % 2 != 0 and l == middle_y and j == middle_x:
                    b.append(0)  # Joker in der Mitte, nur wenn xsize und ysize ungerade sind
                else:
                    random_word = choice(buzzwords_list)
                    b.append(random_word)
                    buzzwords_list.remove(random_word)
            matrix.append(b)
        matrixlist.append(matrix)  # fügt die bingokartenmatrix einer person in die bingokartenliste ein
        initialize_file()  # man setzt buzzwords_list wieder auf den ursprünglichen Inhalt zurück.
    return matrixlist

def display_bingo_cards(playernamelist, matrixlist):
    # Ausgabe der Bingokarten zur Überprüfung
    for i, matrix in enumerate(matrixlist):  # i ist der Index, matrix ist die Bingokarte
        print(f"\nBingokarte für {playernamelist[i]}:")  # Ausgabe des Spielernamens
        for row in matrix:  # row ist eine Zeile der Bingokarte
            print("\t".join(str(cell) for cell in row))  # Ausgabe der Bingokarte

def start_game():  # Funktion, die das Spiel startet.
    initialize_file()
    playercount = get_player_count()
    playernamelist = get_player_names(playercount)
    xsize = get_dimensionx()
    ysize = get_dimensiony()
    matrixlist = generate_bingo_cards(playernamelist, xsize, ysize)
    display_bingo_cards(playernamelist, matrixlist)

if __name__ == "__main__":  # wird ausgeführt, wenn das Skript direkt ausgeführt wird.
    start_game()  # ruft die Funktion start_game auf.

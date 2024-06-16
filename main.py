from random import choice  #importiert nur das choice aus dem Modul random.

buzzwords_list = [] #erstellt eine leere Liste, wo die Buzzwörter gespeichert werden.

def initialize_file(): #diese Funktion füllt die Liste mit dem Inhalt aus buzzwords.txt.
    with open("buzzwords.txt") as file: #öffnet die Datei.
        reader = file.readlines() #liest die Datei.
        for i in reader: #for Schleife, die jedes Element der Liste durchläuft.
            i = i.strip() #entfernt die Zeilenumbrüche.
            buzzwords_list.append(i) #fügt die Buzzwörter aus der Liste hinzu.

initialize_file() #ruft die Funktion auf.




















playernamelist = [] 
matrixlist = [] #Liste der Bingokarten
while True:
    playercount = input("Geben Sie die Spieleranzahl ein: ")
    try:
        playercount = int(playercount)
        break
    except ValueError:
        try:
            float(playercount)
            print("Fehler: Die eingegebene Zahl darf keine Kommazahl sein.")
        except ValueError:
            print("Fehler: Die Eingabe muss eine Zahl sein.")


playername = input("geben Sie den Namen des Spielers ein: ")
playernamelist.append(playername)

while True:
    xsize = input("wie viele spalten sollen die bingokarten haben?")
    try:
        xsize = int(xsize)
        break
    except ValueError:
        try:
            float(xsize)
            print("Fehler: Die eingegebene Zahl darf keine Kommazahl sein.")
        except ValueError:
            print("Fehler: Die Eingabe muss eine Zahl sein.")

while True:            
    ysize = input("wie viele Zeilen sollen die Bingokarten haben?")
    try:
        ysize = int(ysize)
        break
    except ValueError:
        try:
            float(ysize)
            print("Fehler: Die eingegebene Zahl darf keine Kommazahl sein.")
        except ValueError:
            print("Fehler: Die Eingabe muss eine Zahl sein.")

matrix = []
a = xsize * ysize #a ist die anzahl der felder

for j in range(0, a):
    random_word = choice(buzzwords_list)
    matrix.append(random_word)
    buzzwords_list.remove(random_word)
matrixlist.append(matrix)   


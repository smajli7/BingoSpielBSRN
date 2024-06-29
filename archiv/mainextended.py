from random import choice  #importing only 'choice' function from 'random' module

list = [] #creates an empty list where all the buzzwords will be stored

def initialize_file(): #this function will fill the list with buzzwords from the file
    with open("Buzzwords.txt") as file: #opens the file
       reader = file.readlines() #reads the file
       for i in reader: #for loop that goes through each line in the file
          i = i.strip() #removes the \n
          list.append(i) #adds the line to the list

initialize_file() #starts the function

random_word = choice(list) #picks a random word from the list above



















playernamelist = [] 
matrixlist = [] #Liste der Bingokarten
playercount = int(input("Geben Sie die Spieleranzahl ein: "))
playername = input("geben Sie den Namen des Spielers ein: ")
playernamelist.append(playername)
xsize = int(input("wie viele spalten sollen die bingokarten haben?"))
ysize = int(input("wie viele zeilen sollen die bingokarten haben?"))
matrix = []
a = xsize * ysize #a ist die anzahl der felder
for j in range(0, a):
   random_word = choice(list)
   matrix.append(random_word)
   list.remove(random_word)
matrixlist.append(matrix)   




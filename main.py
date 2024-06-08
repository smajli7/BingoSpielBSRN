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

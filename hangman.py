# Talanda Williams
# CST 438 Week 1
# Python Hangman

import random #used for picking the word from the list

class Hangman():
    def __init__(self, guessword):  #constructor of Hangman class
        self.guessword = guessword
        self.numberGuesses = 0
        self.displayword = len(guessword) * '_' #used to show guess progress
        self.wrong_guesses = 0 
        self.guessed = [] #used for containing prior guesses

    def __str__(self): #used for printing user progress/display world with a space for readability
        word =''
        for char in self.displayword:
            word += f" {char}"
        return word

    def guess(self, char):
        char = char.casefold() # casefold makes guesses case insensitive
        self.guessed.append(char)
        if char not in self.guessword: #increase
            self.wrong_guesses += 1
            return False
        new_displayword = '' #use to check against current displayed word + guessed word progress
        for i, character in enumerate(self.guessword): #find the position in guess word and 'save' into temp display word
            if character.casefold() == char:
                new_displayword += character # either show the new letter properly guessed in the display word...
            else:
                new_displayword += self.displayword[i] #... or copy existing position in display word
        self.displayword = new_displayword  
        return True
    
    def over(self): #checks for status of game ending parameters
        if self.wrong_guesses != 7 and self.displayword != self.guessword:
            return False
        return True
    
    def win(self): #states winning/losing 
        if self.wrong_guesses == 7:
            return False
        elif self.displayword == self.guessword:
            return True

def pickrandomword(): #function that pulls words from list and picks one randomly
    with open("hangmanwords.txt") as fileh:
        all_words = [x.strip() for x in fileh]
        linerange = len(all_words)
        return all_words[random.randrange(0, linerange)]

def main():
    word = pickrandomword() #step 1, pick word behind scenes
    game = Hangman(word) #step 2, apply it to game
    while(not game.over()):
        print(game)
        valid_guess = False
        while not valid_guess:
            letter = input("Make a guess\n") #step 3, make a valid guess
            if len(letter) != 1:
                print("enter only one letter")
            elif not letter.isalpha():
                print("guess must be a letter of the alphabet")
            elif letter in game.guessed:
                print("you've already guessed that letter")
            else:
                valid_guess = True #step 4, proceeds with correct letter input
        if not game.guess(letter):
            print(f"wrong guess, you have {7-game.wrong_guesses} left") #step 5, display number of guesses remaining if wrong guess
    print(game) #step 5, calls str and checks word, etc
    if not game.win():
        print("The word was", game.guessword) #step 6, lose game
    else:
        print("you win") #or better step 6, win game.

if __name__ == "__main__": #runs actual game code above
    main()

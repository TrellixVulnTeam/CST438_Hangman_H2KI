# Talanda Williams
# CST 438 Week 1
# Python Hangman

import random #used for picking the word from the list
import json
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

class Hangman():
    def __init__(self, guessword):  #constructor of Hangman class
        self.guessword = guessword
        self.displayword = len(guessword) * '_' #used to show guess progress
        self.wrong_guesses = 0 
        self.guessed = [] #used for containing prior guesses

    def __str__(self): #used for printing user progress/display world with a space for readability
        word = ''
        for char in self.displayword:
            word += f" {char}"
        return word
        #return self.displayword

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

@app.route('/')
def initialize():
    #if request.form.get("displayword") is None:
    word = pickrandomword()  # step 1, pick word behind scenes
    game = Hangman(word)  # step 2, apply it to 'game'
    print("initialized")
    return render_template("index.html", guessword=game.guessword, displayword=str(game),
                           wrong_guesses=game.wrong_guesses,
                           guessed=json.dumps(game.guessed), message="Welcome to the game")
    #word = pickrandomword()  # step 1, pick word behind scenes
    #game = Hangman(word)  # step 2, apply it to game
    #print(word)
    #return jsonify(guessword=game.guessword, displayword=game.displayword,
                    #  numberGuesses=game.numberGuesses, wrong_guesses=game.wrong_guesses,
                    #  guessed=game.guessed, incorrect=False, win=False, lost=False)

@app.route("/", methods=["POST"])
def main():
    render_template("index.html")
    word = pickrandomword()  # step 1, pick word behind scenes
    game = Hangman(word)  # step 2, apply it to game
    # print(word)
    game = Hangman(request.form.get("guessword"))
    print(request.form.get("displayword"))
    game.displayword = request.form.get("displayword").replace(' ', '')
    game.wrong_guesses = int(request.form.get("wrong_guesses"))
    game.guessed = json.loads(request.form.get("guessed"))
    letter = request.form.get('guess')
    # print (letter)
    if not game.over():
        # print(game)
        if len(letter) != 1:
            return render_template("index.html", guessword=game.guessword, displayword=str(game),
                                    wrong_guesses=game.wrong_guesses,
                                    guessed=json.dumps(game.guessed), incorrect=True, win=False, lost=False, message="Must be only one letter")
        elif not letter.isalpha():
            return render_template("index.html", guessword=game.guessword, displayword=str(game),
                                    wrong_guesses=game.wrong_guesses,
                                    guessed=json.dumps(game.guessed), incorrect=True, win=False, lost=False, message="Must be a letter")
        elif letter in game.guessed:
            return render_template("index.html", guessword=game.guessword, displayword=str(game),
                                    wrong_guesses=game.wrong_guesses,
                                    guessed=json.dumps(game.guessed), incorrect=True, win=False, lost=False, message="Already guessed")
        if not game.guess(letter) and not game.over():
            return render_template("index.html", guessword=game.guessword, displayword=str(game),
                                   wrong_guesses = game.wrong_guesses,
                                   guessed = json.dumps(game.guessed), incorrect=False, win=False, lost=False, message="incorrect guess")
        elif not game.over():
            return render_template("index.html", guessword=game.guessword, displayword=str(game),
                                   wrong_guesses=game.wrong_guesses,
                                   guessed=json.dumps(game.guessed), incorrect=False, win=False, lost=False, message="correct guess")
    # print(game) #step 5, calls str and checks word, etc
    if not game.win():
        return render_template("index.html", guessword=game.guessword, displayword=str(game),
                               wrong_guesses=game.wrong_guesses,
                               guessed=json.dumps(game.guessed), incorrect=True, win=False, lost=True, message="You Lose")
    else:
        return render_template("index.html", guessword=game.guessword, displayword=str(game),
                               wrong_guesses=game.wrong_guesses,
                               guessed=json.dumps(game.guessed), incorrect=True, win=True, lost=False, message="you win")

if __name__ == "__main__": #runs actual game code above
    main()

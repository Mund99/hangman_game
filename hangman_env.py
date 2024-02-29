import random

class HangmanGame:
    def __init__(self, datasets):
        self.datasets = datasets
        self.secret_word = self.choose_word()
        self.guessed_letters = []
        self.attempts_left = 6

    def choose_word(self):
        return random.choice(self.datasets)

    def display_word(self):
        display = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        return display

    def display_hangman(self):
        hangman_images = [
            """
            -----
            |   |
                |
                |
                |
                |
            --------
            """,
            """
            -----
            |   |
            O   |
                |
                |
                |
            --------
            """,
            """
            -----
            |   |
            O   |
            |   |
                |
                |
            --------
            """,
            """
            -----
            |   |
            O   |
           /|   |
                |
                |
            --------
            """,
            """
            -----
            |   |
            O   |
           /|\\  |
                |
                |
            --------
            """,
            """
            -----
            |   |
            O   |
           /|\\  |
           /    |
                |
            --------
            """,
            """
            -----
            |   |
            O   |
           /|\\  |
           / \\  |
                |
            --------
            """
        ]

        return hangman_images[6 - self.attempts_left]

    def play(self, guess):
        guess = guess.lower()
        if guess.isalpha() and len(guess) == 1:
            if guess in self.guessed_letters:
                return "You already guessed that letter. Try again.", self.attempts_left
            elif guess in self.secret_word:
                self.guessed_letters.append(guess)
                return "Good guess!", self.attempts_left
            else:
                self.attempts_left -= 1
                self.guessed_letters.append(guess)
                return "Incorrect guess.", self.attempts_left
        else:
            return "Invalid input. Please enter a single letter.", self.attempts_left

    def game_over(self):
        if "_" not in self.display_word():
            return True, f"Congratulations! You guessed the word: {self.secret_word}"
        elif self.attempts_left == 0:
            return True, f"Sorry, you ran out of attempts. The word was: {self.secret_word}"
        else:
            return False, ""


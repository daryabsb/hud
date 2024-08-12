import random

wordlist = [
    'apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 
    'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'papaya', 'quince', 'raspberry',
    'strawberry', 'tangerine', 'ugli', 'violet', 'watermelon', 'xigua', 'yam', 'zucchini',
    'avocado', 'blueberry', 'coconut', 'dragonfruit', 'eggplant', 'fennel', 'guava', 'huckleberry',
    'iceberg', 'jackfruit', 'kumquat', 'lime', 'melon', 'nutmeg', 'olive', 'pomegranate', 
    'radish', 'spinach', 'tomato', 'ube', 'vanilla', 'walnut', 'ximenia', 'yambean',
    'zebra', 'alpaca', 'butterfly', 'dolphin', 'elephant', 'flamingo', 'giraffe', 'hippopotamus',
    'iguana', 'jellyfish'
]

word = None
guessed_chars = set()
wrong_guesses = []
max_wrong_guesses = 3

def get_random_word():
    global word
    if word is None:
        word = random.choice(wordlist)
        print(word)
    return word

def split_word(word):
    return list(word)

def get_guess():
    return input("Guess a letter: ")

def display_word(word, guessed_chars):
    return ''.join([char if char in guessed_chars else '_' for char in word])

def guessing_game():
    global word
    global wrong_guesses
    global max_wrong_guesses
    global guessed_chars

    random_word = get_random_word()
    characters = set(split_word(random_word))
    
    print(f"Word: {display_word(random_word, guessed_chars)}")
    print(f"Guessed characters: {sorted(guessed_chars)}")
    print(f"Wrong guesses: {sorted(wrong_guesses)}")

    guess = get_guess()

    if guess in guessed_chars:
        print("You already guessed that letter!")
    elif guess in characters:
        print("Your choice was correct!")
        guessed_chars.add(guess)
        if guessed_chars >= characters:
            print(f"Congratulations, you guessed the word: {random_word}!")
            reset_game()
            return
    else:
        print("Your guess is wrong, try another letter!")
        wrong_guesses.append(guess)
        guessed_chars.add(guess)
        if len(wrong_guesses) >= max_wrong_guesses:
            print(f"Unfortunately, you lost the game! The word was: {random_word}")
            reset_game()
            return

    guessing_game()

def reset_game():
    global word
    global wrong_guesses
    global guessed_chars

    word = None
    wrong_guesses = []
    guessed_chars = set()

def run():
    guessing_game()

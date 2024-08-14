import random
from django.shortcuts import render
from django.http import JsonResponse

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

def get_random_word():
    return random.choice(wordlist)

def display_word(word, guessed_chars):
    return ''.join([char if char in guessed_chars else '_' for char in word])

def game_page(request):
    guessed_chars = set()
    if 'word' not in request.session:
        request.session['word'] = get_random_word()
        request.session['guessed_chars'] = list(guessed_chars)
        request.session['wrong_guesses'] = []

    word = request.session['word']
    guessed_chars = request.session['guessed_chars']
    wrong_guesses = request.session['wrong_guesses']

    context = {
        'word_display': display_word(word, guessed_chars),
        'guessed_chars': sorted(guessed_chars),
        'wrong_guesses': sorted(wrong_guesses),
        'max_wrong_guesses': 3 - len(wrong_guesses),
    }
    return render(request, 'games/main.html', context)

def guess_letter(request):
    if request.method == 'POST':
        guess = request.POST.get('guess')
        word = request.session.get('word')
        guessed_chars = set(request.session.get('guessed_chars', []))
        wrong_guesses = request.session.get('wrong_guesses', [])

        if guess in guessed_chars:
            message = "You already guessed that letter!"
        elif guess in word:
            guessed_chars.add(guess)
            message = "Your choice was correct!"
            if set(word) <= guessed_chars:
                message = f"Congratulations, you guessed the word: {word}!"
                request.session.flush()  # Reset the game
        else:
            wrong_guesses.append(guess)
            guessed_chars.add(guess)
            message = "Your guess is wrong, try another letter!"
            if len(wrong_guesses) >= 3:
                message = f"Unfortunately, you lost the game! The word was: {word}"
                request.session.flush()  # Reset the game

        # Convert the set to a list before saving to session
        request.session['guessed_chars'] = list(guessed_chars)
        request.session['wrong_guesses'] = wrong_guesses

        context = {
            'word_display': display_word(word, guessed_chars),
            'guessed_chars': sorted(list(guessed_chars)),
            'wrong_guesses': sorted(wrong_guesses),
            'message': message,
            'max_wrong_guesses': 3 - len(wrong_guesses),
        }
        return JsonResponse(context)

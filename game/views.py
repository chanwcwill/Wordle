import random
from django.shortcuts import render, redirect
from django.http import HttpRequest

# Simple built-in word list (can be expanded)
WORD_LIST = [
    'apple', 'grape', 'peach', 'mango', 'lemon', 'berry', 'melon', 'charm', 'crane', 'flame',
    'pride', 'sword', 'blaze', 'glove', 'brave', 'shine', 'sugar', 'tiger', 'zebra', 'eagle',
]

MAX_GUESSES = 6
WORD_LENGTH = 5


def get_feedback(guess, target):
    feedback = []
    target_chars = list(target)
    guess_chars = list(guess)
    # First pass: correct position
    for i in range(WORD_LENGTH):
        if guess_chars[i] == target_chars[i]:
            feedback.append('green')
            target_chars[i] = None  # Mark as used
        else:
            feedback.append(None)
    # Second pass: correct letter, wrong position
    for i in range(WORD_LENGTH):
        if feedback[i] is None:
            if guess_chars[i] in target_chars:
                feedback[i] = 'yellow'
                target_chars[target_chars.index(guess_chars[i])] = None
            else:
                feedback[i] = 'gray'
    return feedback


def wordle_game(request: HttpRequest):
    if 'target_word' not in request.session:
        request.session['target_word'] = random.choice(WORD_LIST)
        request.session['guesses'] = []
        request.session['feedback'] = []
        request.session['game_over'] = False
        request.session['win'] = False

    guesses = request.session.get('guesses', [])
    feedback = request.session.get('feedback', [])
    game_over = request.session.get('game_over', False)
    win = request.session.get('win', False)
    message = ''

    if request.method == 'POST' and not game_over:
        guess = request.POST.get('guess', '').lower()
        if len(guess) != WORD_LENGTH or not guess.isalpha():
            message = f"Please enter a valid {WORD_LENGTH}-letter word."
        elif guess not in WORD_LIST:
            message = "Word not in list."
        else:
            guesses.append(guess)
            fb = get_feedback(guess, request.session['target_word'])
            feedback.append(fb)
            if guess == request.session['target_word']:
                game_over = True
                win = True
                message = "Congratulations! You guessed the word!"
            elif len(guesses) >= MAX_GUESSES:
                game_over = True
                message = f"Game over! The word was {request.session['target_word'].upper()}."
            request.session['guesses'] = guesses
            request.session['feedback'] = feedback
            request.session['game_over'] = game_over
            request.session['win'] = win

    if request.method == 'POST' and (game_over or win) and 'play_again' in request.POST:
        for key in ['target_word', 'guesses', 'feedback', 'game_over', 'win']:
            if key in request.session:
                del request.session[key]
        return redirect('wordle_game')

    # Prepare rows for template: list of zipped (letter, color) for each guess
    rows = [zip(guess, fb) for guess, fb in zip(guesses, feedback)]
    empty_rows = MAX_GUESSES - len(rows)
    empty_rows_list = range(empty_rows)

    return render(request, 'game/wordle.html', {
        'guesses': guesses,
        'feedback': feedback,
        'max_guesses': MAX_GUESSES,
        'word_length': WORD_LENGTH,
        'game_over': game_over,
        'win': win,
        'message': message,
        'rows': rows,
        'empty_rows': empty_rows,
        'empty_rows_list': empty_rows_list,
        'word_length_list': range(WORD_LENGTH),
    })

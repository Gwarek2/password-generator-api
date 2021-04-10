"""
Simple password generator API built with Flask framework.
Uses "secrets" library for generating cryptographically strong passwords or tokens.
"""
from string import ascii_lowercase, ascii_uppercase, digits
from flask import Flask, request, render_template, jsonify, make_response
from src.helpers import *

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 

@app.route('/', methods=['GET'])
def index():
    """
    Returns project main page
    """
    return render_template('index.html')


@app.route('/generate', methods=['GET'])
def generate():
    """
    Generates password with given parameters, then returns password as JSON-response
    """
    # Loading password parameters
    parameters = request.args
    if not parameters:
        return make_response(jsonify({'error': 'No parameters for the password were given'}), 400)

    # Defining password length
    try:
        password_length = int(parameters.get('count'))
    except (ValueError, TypeError):
        return make_response(jsonify({'error': 'The count value must be an integer number'}), 400)

    if password_length < 4 or password_length > 50:
        return make_response(jsonify({'error': 'The count value must be bigger than 4 and lower than 50'}), 400)

    # Building character pool for password by parameters
    letters_pool = ''
    digits_pool = ''
    special_characters_pool = ''

    include_letters = parameters.get('letters')
    include_special_symbols = parameters.get('special_symbols')
    include_digits = str(parameters.get('digits'))

    if include_letters == 'on':
        letters_pool += ascii_lowercase + ascii_uppercase
    elif include_letters and include_letters.isalpha():
        letters_pool += include_letters
    else:
        if parameters.get('upper'):
            letters_pool += ascii_uppercase
        if parameters.get('lower'):
            letters_pool += ascii_lowercase

    if include_digits == 'on':
        digits_pool += digits
    elif include_digits.isdigit():
        digits_pool += include_digits

    if include_special_symbols == 'on':
        special_characters_pool += punctuation
    elif is_special_symbols(include_special_symbols):
        special_characters_pool += include_special_symbols

    # Creating list with pools, chance for each type: letters - 0.4, digits - 0.4, special_symbols - 0.2
    permitted_chars = diversify_pool(letters_pool, digits_pool, special_characters_pool)

    if not permitted_chars:
        return make_response(jsonify({'error': 'Permitted characters were not given'}), 400)

    # Generating password
    generated_password = generate_password(permitted_chars, password_length)

    return make_response(jsonify({'string': generated_password}), 200)


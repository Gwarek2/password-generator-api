"""
Simple password generator API built with Flask framework.
"""
from flask import Flask, request, render_template, jsonify, make_response
from src.password_generator import Password


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
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

    # Exceptions handler
    try:
        # Creating password
        password = Password(parameters)
        password.pool = (2, 2, 1)
        password_value = password.value
    except ValueError:
        return make_response(jsonify({'error': 'The count value must be an integer'}), 400)
    except AttributeError:
        return make_response(jsonify({'error': 'The count value were not given in request'}), 400)
    except ArithmeticError:
        return make_response(jsonify({'error': 'The count value must be bigger than 4 and less than 50'}), 400)
    except IndexError:
        return make_response(jsonify({'error': 'The permitted characters were not given in request'}), 400)

    return make_response(jsonify({'string': password_value}), 200)

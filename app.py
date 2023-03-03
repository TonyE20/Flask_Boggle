from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'its a secret'
debug = DebugToolbarExtension(app)

game = Boggle()

@app.route('/')
def create_board():
    """ Creates Game Board"""
    board = game.make_board()
    session['board'] = board
    # import pdb
    # pdb.set_trace()
    return render_template('index.html', board = board)

@app.route('/valid-word')
def check_word():
    """ Verifies word in dictionary"""
    # import pdb
    # pdb.set_trace()
    word = request.args['guess']
    board = session['board']
    verify_word = game.check_valid_word(board, word)
    return jsonify({'result': verify_word})

@app.route('/score', methods=["POST"])
def show_highest_score():
    """ Udates highscore and played times"""
    # import pdb
    # pdb.set_trace()
    score = request.json['score']
    high_score = session.get('high_score', 0)
    n_played = session.get('game_played', 0)
    session['game_played'] = n_played + 1
    if high_score < score:
        session['high_score'] = score 
    else: session['high_score'] = high_score
    
    return jsonify(top_score = score > high_score, n_played = n_played)
    
    

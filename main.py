from akinator import Akinator
from flask import render_template, Flask, request, abort

app = Flask(__name__)

aki = Akinator()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/game')
def game():
    aki.start_game()
    question = aki.question
    return render_template('game.html', question=question)

@app.route('/response', methods=['POST'])
def response():
    try:
        # Get the user's answer
        answer = request.form['answer']
        aki.answer(answer)
        # If the game is not over, ask the next question
        if aki.progression < 80:
            question = aki.question
            return render_template('game.html', question=question)
        else:
            # The game is over, make a guess
            aki.win()
            guess = aki.first_guess
            return render_template('guess.html', name=guess['name'], url=guess['absolute_picture_path'], description=guess['description'])
    except KeyError:
        # If the user's answer is not found in the form data, return a 400 Bad Request error
        abort(400)

@app.route('/guesses')
def guesses():
    li=[]
    for k in aki.guesses:
        if k["name"] not in li and k["name"]!=aki.first_guess["name"]:
            li.append(k["name"])
    return render_template("guesses.html",guesses=li)

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)

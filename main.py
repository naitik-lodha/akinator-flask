from akinator import Akinator
from flask import render_template,Flask, request

app=Flask(__name__)

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
    # Get the user's answer
    answer = request.form['answer']
    if answer == 'yes':
        aki.answer(0)
    elif answer == 'no':
        aki.answer( 1)
    elif answer == 'idk':
        aki.answer( 2)
    elif answer == 'probably':
        aki.answer( 3)
    elif answer == 'probably not':
        aki.answer( 4)

    # If the game is not over, ask the next question
    if aki.progression <= 80:
        question = aki.question
        return render_template('game.html', question=question)
    else:
        # The game is over, make a guess
        aki.win()
        guess = aki.first_guess
        print(guess["name"])
        return render_template('guess.html', name=guess['name'],url=guess['absolute_picture_path'],description=guess['description'])
@app.route('/guesses')
def guesses():
    li=[]
    for k in aki.guesses:
        if k["name"] not in li and k["name"]!=aki.first_guess["name"]:
            li.append(k["name"])
    return render_template("guesses.html",guesses=li)
if __name__ =="__main__":
    app.run(debug=True)
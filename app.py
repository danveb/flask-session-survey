from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'oh-so-secretive'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app) 

# responses = [] 

#root route 
@app.route('/')
def survey_home_page():
    """Shows survey start page"""
    return render_template('home.html', survey=satisfaction_survey)

#start route 
@app.route('/start', methods=['GET','POST']) 
def start_survey():
    """Redirect to Question #0"""
    # fire a POST request to 'start' route
    # set session of responses to empty list
    session['responses'] = [] 
    return redirect('/questions/0') 

#question route
@app.route('/questions/<int:num>')
def get_question(num):
    """Get Question"""
    responses = session.get('responses')

    # # error handling num may go above 4 (buggy?) 
    # if (len(responses) == len(satisfaction_survey.questions)):
    #     # redirect to thank you page
    #     return redirect('/thanks')

    # protect question so that question is not skipped; user may want to go to a different question than in order 7
    if (len(responses) != num):
        # flash message (base.html)
        flash("Sorry you are trying to access an invalid question")
        # redirect to current question 
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[num]
    return render_template('questions.html', question_num=num, question=question)

#answer route 
@app.route('/answer', methods=["GET", "POST"]) 
def get_answer():
    """Get Answer, append answer to responses and continue to next question"""
    answer_choice = request.form['answer']

    # need to add answer to session; rebind name in the session 
    responses = session['responses']
    responses.append(answer_choice)
    session['responses'] = responses 

    # if length responses == length of questions
    if (len(responses) == len(satisfaction_survey.questions)):
        # redirect to thank you page
        return redirect('/thanks')
    else:
        # return redirect('/questions/1')
        # redirect (len(responses)) 
        return redirect(f'/questions/{len(responses)}')

#thanks route
@app.route('/thanks')
def thank_you():
    """Thank the user for completing the survey"""
    return render_template('thank-you.html')
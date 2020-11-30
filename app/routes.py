from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User,Question, Result, feedback, MCQ, answers
from werkzeug.urls import url_parse
from sqlalchemy import func

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    users = User.query.all()
    
    return render_template('intro.html', title = 'Home', 
                            Question=Question, 
                            feedback=feedback, 
                            Result=Result )


@app.route('/login',methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:

        return redirect(url_for('login'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()

        if user is None or not user.check_password(form.password.data):

            flash("Incorrect password")

            return redirect(url_for('login'))

        login_user(user, remember = form.remember_me.data)

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            
            return redirect(url_for('index'))

        return redirect(next_page)

    return render_template('login.html', title = "Sign in", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:

        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("You've registered! Please Sign In")

        return redirect(url_for('login'))

    return render_template('register.html', title = "Register", form = form)

@app.route('/about')
def about():
    return render_template('about.html', title = "about")

@app.route('/dilip')
def dilip():
    return render_template('dilip.html', title ="dilip")

@app.route('/add_question')
def add_question():
    print("USER NAME: " + current_user.username)
    if current_user.is_authenticated and current_user.username == 'admin':
        return render_template('add_question.html')
    return render_template("restricted.html")

@app.route('/sonali')
def sonali():
    return render_template('sonali.html',title ="dilip")


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    Questions = Question.query.filter_by(text_question=0)

    feedbackflag = 0
    Feedback=""
    if not bool(current_user.Feedback.filter_by(user_id = current_user.id).first() == None):
        feedbackflag = 1
        Feedback = current_user.Feedback.filter_by(user_id = current_user.id).first().Feedback 
   
    score = ""
    question_sum = ""
    question_num = 0

    # to count number of questions
    for question in Questions:
        question_num+=1

   #MCQ quiz result calculation
    if bool(Result.query.filter_by(user_id = current_user.id).first()):
        question_sum = db.session.query(func.sum(Question.question_marks)).scalar()
        score = current_user.outcome[0].result


    questions = Question.query.filter_by(text_question=True)
    # variables for the total mark for the long question gotten, total mark weighting 
    # for the long questions, percentage for the mark and the response from admin
    quizcompleteflag = True
    markflag = False
    mark = 0
    question_mark = 0
    responses = ""
     # calculate the above variables below for each long answer question
    for question in questions:
        # if no long answer entry can be found for the current user then skip the loop
        if not bool(current_user.ques.filter_by(question_id = question.id).first()):
            quizcompleteflag = False
            break
        # if no long answer entry can be found for the current user then skip the loop
        if not bool(current_user.ques.filter_by(question_id = question.id).first().user_marks == None):
            markflag = True
            mark += current_user.ques.filter_by(question_id = question.id).first().user_marks
            question_mark += question.question_marks
    # if there are entries in the long answer for the current user
    if quizcompleteflag:
        responses = current_user.ques  
   
    return render_template('feedback.html',
                         title='feedback',Feedback=Feedback, 
                         feedbackflag=feedbackflag,
                         score = score,question_num=question_num, 
                         sum = question_sum,
                         question_mark = question_mark,
                         responses=responses,
                         mark = mark, markflag = markflag, 
                         quizcompleteflag = quizcompleteflag)


@app.route('/test')
def test():
    users = User.query.all()

    avg = 0
    numUser = 0
    avglong = 0
    numUseranswer = 0
    # calculate the user's avg marks for short answer question
    for user in users:
        if not bool(user.outcome.first()):
            continue
        else:
            numUser +=1
            avg += user.outcome[0].result

    return render_template('test.html', title = 'exam', avg = avg, numUser = numUser,
                           
                            Question=Question, 
                            feedback=feedback, 
                            Result=Result,
                            MCQ=MCQ )

@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam():
    
    questions = Question.query.filter_by(text_question=False)
    mcq=MCQ.query.all()
    score = 0 

    # if the quiz form on quiz.html has been submitted
    if request.method == "POST":

        # check if the answer submitted are correct for the short answer questions and generate the result accordingly
        for question in questions:
            ques_id = str(question.id)
            request_name = request.form[ques_id]
            if MCQ.query.filter_by(options_content = request_name).first().correct:
                score += 1

        #check if quiz has been done by a user previously if not add a quiz table for the result of the user
        if not bool(Result.query.filter_by(user_id = current_user.id).first()):
            outcome = Result(user_result= current_user)
            db.session.add(outcome)
            db.session.commit()
        current_user.outcome[0].result = score
        db.session.commit()    
        return redirect(url_for('feedback'))

    return render_template('exam.html', title='Quiz',questions=questions,mcq=mcq)


# quiz route for quiz.html the page where users get to play the quiz
@app.route('/exam2', methods=['GET', 'POST'])
@login_required
def exam2():
    
    questions = Question.query.filter_by(text_question=True)

    if request.method == "POST":


        for question in questions:
            ques_id = str(question.id)
            Answer = request.form[ques_id]
            if not bool(answers.query.filter_by(user_id = current_user.id, question_id = question.id).first()):
                answer = answers(answer_user = current_user, answers = question)
                db.session.add(answer)
                db.session.commit()
            result = current_user.ques.filter_by(question_id = question.id).first()
            result.answer = Answer
            result.response = None
            result.user_marks = None
            db.session.commit()

        return redirect(url_for('feedback'))

    return render_template('exam2.html', title='Exam2',questions=questions)

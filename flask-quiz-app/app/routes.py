from app import app
from flask import render_template, request, redirect, url_for, session, g, flash
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, QuestionForm, RequestResetForm
from app.models import User, Questions
from app import db

 

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        g.user = user

@app.route('/')
def home():
    session["marks"]= 0
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        session['user_id'] = user.id
        session['marks'] = 0
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
        #return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['marks'] = 0
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    form = QuestionForm()
    q = Questions.query.filter_by(q_id=id).first()
    if not q:
        return redirect(url_for('score'))
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        option = request.form['options']
        if option == q.ans:
            session['marks'] += 10
        return redirect(url_for('question', id=(id+1)))
    form.options.choices = [(q.a, q.a), (q.b, q.b), (q.c, q.c), (q.d, q.d)]
    return render_template('question.html', form=form, q=q, title='Question {}'.format(id))


@app.route('/score')
def score():
    if not g.user:
        return redirect(url_for('login'))
    g.user.marks = session['marks']
    db.session.commit()
    return render_template('score.html', title='Final Score')

@app.route('/logout')
def logout():
    if not g.user:
        return redirect(url_for('login'))
    session.pop('user_id', None)
    session.pop('marks', None)
    return redirect(url_for('home'))


# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
#     msg.body= f''' To reset your password, visit the following link:
# {url_for('reset_token',token=token, _external=True)}

# If you did not make this request then simply ignore this email and no change
# '''
#     mail.send(msg)


@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user= User.query.filter_by(username=form.username.data).first()
        #send_reset_email(user)
        if user:
            user.set_password(form.password.data)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password',form=form)


# @app.route('/reset_your_password', methods=['GET','POST'])
# def reset_it():
#     # user = User.verify_reset_token(token)
#     # if user is None:
#     #     flash('That is an invalid or expired token','warning')
#     #     return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html',title='Reset password',form=form)
from flask import Flask, render_template, request, url_for, redirect, session

from appconfig import app, db, User
from utilities import is_valid_data

@app.route('/')
def index():
    if session.get('curr_user'):
        return render_template('index.html',curr_user=session['curr_user'])
    else:
        return render_template('index.html')

@app.route('/signuphandler',methods=['POST'])
def signuphandler():

    fullname = request.form['fullname']
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    validate_status = is_valid_data(fullname,username,email,phone,password)

    if ( validate_status == 1):
        new_user = User(fullname=fullname,username=username,email=email,phone=phone)
        # Setting the unique user_id
        new_user.set_user_id()
        # Setting the hashed password in DB
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(f'Added New User ({fullname}) ({email})')
        user = User.query.filter_by(username=username).first()
        # Setting the session for user
        session['curr_user'] = user.get_user_dict()
        return redirect(url_for('user'))
    else:
        return redirect(url_for('signup',error_msg = validate_status))


@app.route('/signup')
@app.route('/signup/<error_msg>') # this route is invoked by singuphandler if some error occurs
def signup(error_msg=None):
    if not session.get('curr_user'):
        return render_template('signup.html',error_msg=error_msg)
    else:
        # return redirect(url_for('user',user_id='blahblah'+session['curr_user']))
        return render_template('signup.html',note_msg='Please Log-out Before A New SignUp!',curr_user=session['curr_user'])

@app.route('/users')
def users():
    if session.get('curr_user'):
        users = User.query.all()
        return render_template('users.html',users=users,curr_user=session['curr_user'])
    else:
        return render_template('users.html',error_msg="Accessed Only By Logged In Users!")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        # If User session is set prompt to logout
        if session.get('curr_user') :
            return render_template('login.html',note_msg='You are already logged-In',curr_user=session['curr_user'])
        # If no session is set , present the login page
        else :
            return render_template('login.html')
    # If request type is post check if user is trying to login or logout
    else :
        if 'logout' in request.form :
            session['curr_user'] = None
            return render_template('login.html')
        elif 'login' in request.form:

            username = request.form['username']
            password = request.form['password']
            is_user = User.query.filter_by(username=username).first()
            if is_user:
                # If given password matches up set the new session and redirect
                if is_user.check_password(password):
                    session['curr_user'] = is_user.get_user_dict()
                    return redirect(url_for('user'))
                else:
                    return render_template('login.html',error_msg='Incorrect password')
            # If No Such user is there in DB
            else:
                return render_template('login.html',error_msg='No user with this username is registered ?!')
        # if hidden field tried to messd up present the login page again
        else:
            return render_template('login.html')


@app.route('/user')
def user():
    if session.get('curr_user'):
        return render_template('user.html',curr_user=session['curr_user'])
    else:
        return render_template('user.html',note_msg='Please Log-In/Signup First !')
if __name__ == '__main__':
    app.run()

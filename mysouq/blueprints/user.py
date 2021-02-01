from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from ..models import user
from ..forms import user_forms

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/', methods=['POST', 'GET'])
@user_bp.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('item/home.html')


@user_bp.route("/signup", methods = ['POST', 'GET'])
def signup():

    signup_form = SignUpForm()

    if signup_form.validate_on_submit():

        user = User()
        
        user.username = signup_form.username.data
        user.password = user.encrypt_password(signup_form.password.data)
        user.email = signup_form.email.data
        user.brithday = signup_form.birthday.data

        user.save()

        return redirect(url_for("login.login"))

    return render_template("sign-up/sign-up.html", form = signup_form)    


@user_bp.route('/login', methods=['POST', 'GET'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data

        user = User.objects(username=username).first()

        if (user) and (user.authenticate(username, password)):

            session['user'] = user.serialize()

            return redirect(url_for('home.home'))

        else:

            flash("Invalid Login. Please check your username and password.")

            return redirect(url_for('login.login'))


        return redirect("/profile")

    
    return render_template('login/login.html', form=login_form)


@user_bp.route('/logout')
def logout():

    session.clear()

    return redirect("/")


@user_bp.route('/session')
def show_session():
    return dict(session)


@user_bp.route('/edit_profile', methods=['POST', 'GET'])
def edit_profile_user():

    user = User.objects(id = session["user"]['id']).first()

    edit_profile_form = EditProfileForm()
    
    if request.method == "GET":
 
        edit_profile_form.new_first_name.data = session['user']['first_name']
        edit_profile_form.new_last_name.data = session['user']['last_name']

    if  edit_profile_form.validate_on_submit():

        new_first_name = edit_profile_form.new_first_name.data
        new_last_name = edit_profile_form.new_last_name.data
    
        user.first_name = new_first_name
        user.last_name = new_last_name
        

        user.save()

        session['user'] = user.serialize()

        return redirect(url_for('home.home')) 

    return render_template("user/edit_profile_user.html", form = edit_profile_form)


@user_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():

    user = User.objects(id=session['user']['id']).first()

    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():

        current_password = change_password_form.current_password.data
        new_password = change_password_form.new_password.data

        if (user):
            user.change_password(current_password, new_password)

            user.save()

            flash("Your password has been successfully changed.")

            return redirect(url_for('user.change_password'))

    return render_template("user/change_password.html", form=change_password_form)
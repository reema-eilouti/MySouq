from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from mysouq.models.user import User
from mysouq.models.item import Item, Category
from mysouq.forms.user_forms import LoginForm, SignUpForm, ChangePasswordForm, EditProfileForm
from mysouq.forms.item_forms import AddCategoryForm, AddItemForm, EditItemForm
from mysouq.models.requests import UpgradeRequest
from functools import wraps


user_bp = Blueprint('user', __name__)


def login_required(function):
    @wraps(function)
    def check_required(*args, **kwargs):

        try:
            session['user']['id']
            return function(*args, **kwargs)

        except:
            return redirect(url_for('user.login'))

    return check_required


def disable_user(function):
    @wraps(function)
    def check(*args, **kwargs):

        try:
            if session['user']['disable'] == False:
                return function(*args, **kwargs)

            else :
                return render_template('user/disable.html')
        except:
            return render_template('user/disable.html')
    
    return check


def maintenance(function):
    @wraps(function)
    def check(*args, **kwargs):

        try:
            if session['user']['maintenance'] == False:
                return function(*args, **kwargs)

            else :
                return render_template('user/maintenance.html')

        except:
            return render_template('user/maintenance.html')
    
    return check



@user_bp.route('/', methods=['POST', 'GET'])
@user_bp.route('/home', methods=['POST', 'GET'])
def home():

    items = Item.objects()

    return render_template('base.html', items = items)


@user_bp.route("/signup", methods = ['POST', 'GET'])
def signup():

    signup_form = SignUpForm()

    if signup_form.validate_on_submit():

        user = User()
        
        user.username = signup_form.username.data
        user.password = user.encrypt_password(signup_form.password.data)
        user.email = signup_form.email.data
        user.birthday = signup_form.birthday.data

        user.save()

        return redirect(url_for("login.login"))

    return render_template("user/signup.html", form = signup_form)    


@user_bp.route('/login', methods=['POST', 'GET'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data

        user = User.objects(username=username).first()

        if user and user.authenticate(username, password):

            session['user'] = user.serialize()

            return redirect(url_for('user.home'))

        else:

            flash("Invalid Login. Please check your username and password.")

            return redirect(url_for('user.login'))

    
    return render_template('user/login.html', form = login_form)


@user_bp.route('/logout')
def logout():

    session.clear()

    return redirect("/")


@user_bp.route('/session')
def show_session():
    return dict(session)



@user_bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():

    user = User.objects(id = session["user"]['id']).first()

    return render_template("user/profile.html", user = user)


@user_bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():

    user = User.objects(id = session['user']['id']).first()

    edit_profile_form = EditProfileForm()
    
    if request.method == "GET":
 
        edit_profile_form.username.data = session['user']['username']
        edit_profile_form.email.data = session['user']['email']
        edit_profile_form.birthday.data = session['user']['birthday']


    if  edit_profile_form.validate_on_submit():

        new_username = edit_profile_form.username.data
        new_email = edit_profile_form.email.data
        new_birthday = edit_profile_form.birthday.data
    
        user.username = new_username
        user.email = new_email
        user.birthday = new_birthday
        
        user.save()

        session['user'] = user.serialize()

        return redirect(url_for('user.home')) 

    return render_template("user/edit_profile.html", form = edit_profile_form)


@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
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


@user_bp.route('/request_upgrade', methods=['GET', 'POST'])
@login_required
def request_upgrade():

    request = UpgradeRequest.objects(user = session['user']['id']).first()

    if not request:

        upgrade_request = UpgradeRequest(user = session['user']['id'], status = "Pending")

        upgrade_request.save()

    else:

        flash("You have already requested an upgrade.")

    return redirect(url_for('user.profile'))



@user_bp.route('/favorites_list', methods=['GET', 'POST'])
@login_required
def view_favorites():

    favorite_items = User.objects(id = session['user']['id']).get().favorites_list
    
    items = []

    for i in range(0, len(favorite_items)):

        item = Item.objects(id = favorite_items[i]).first()
        items.append(item)
           
    return render_template("user/favorites_list.html", items = items)


@user_bp.route('/add_category', methods=['GET', 'POST'])
# @login_required
def add_category():

    add_category_form = AddCategoryForm()

    if add_category_form.validate_on_submit():


        category_value = add_category_form.value.data
        category_label = add_category_form.label.data

        new_category = Category( value = category_value, label = category_label)

        new_category.save()
        
        return redirect(url_for("user.profile"))

    return render_template("user/add_category.html", form = add_category_form)
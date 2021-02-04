from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from mysouq.models.user import User
from mysouq.models.item import Item, Category
from mysouq.forms.user_forms import LoginForm, SignUpForm, ChangePasswordForm, EditProfileForm
from mysouq.forms.item_forms import AddCategoryForm, AddItemForm, EditItemForm
from mysouq.models.requests import UpgradeRequest, BuyRequest
from functools import wraps


user_bp = Blueprint('user', __name__)

# Decorators:

def login_required(function):
    """Login Decorator: 
    This function checks whether the user is logged in before accessing a functionality.
    If not; the user is taken to the Login Page."""

    @wraps(function)
    def check(*args, **kwargs):

        try:
            session['user']['id']
            return function(*args, **kwargs)
        except:
            return redirect(url_for('user.login'))

    return check

def check_disable(function):
    """Disable Decorator: 
    This function checks whether the user "disable" attribute is set to "False" before accessing a functionality.
    If not; then the admin account has set this user's "disable" to "True" and is taken to the Disable Page."""

    @wraps(function)
    def check(*args, **kwargs):

        if session['user']['disable'] == False:
            return function(*args, **kwargs)
        else:
            return render_template('user/disable.html')       
    
    return check

def check_maintenance(function):
    """Maintenance Decorator: 
    This function checks whether the user "maintenance" attribute is set to "False" before accessing a functionality.
    If not; then the admin account has set all users' "maintenance" to "True" and are taken to the Maintenance Page."""

    @wraps(function)
    def check(*args, **kwargs):

        if session['user']['maintenance'] == False:
            return function(*args, **kwargs)
        else:
            return render_template('user/maintenance.html')
    
    return check



@user_bp.route('/', methods=['POST', 'GET'])
@user_bp.route('/home', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance
def home():
    """This function previews the main home page of the site, it displays all the items to be sold for all users."""

    items = Item.objects(sold = False)

    return render_template('base.html', items = items)


@user_bp.route("/signup", methods = ['POST', 'GET'])
def signup():
    """This function creates an account for a new user."""

    signup_form = SignUpForm()

    if signup_form.validate_on_submit():

        user = User()
        
        user.username = signup_form.username.data
        user.password = user.encrypt_password(signup_form.password.data)
        user.email = signup_form.email.data
        user.birthday = signup_form.birthday.data

        user.save()

        return redirect(url_for("user.login"))

    return render_template("user/signup.html", form = signup_form)    


@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    """This function validates the user's login credentials then takes them to the Home page."""

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
    """This function removes the logged in user's information from the Session dictionary."""

    session.clear()

    return redirect("/")


@user_bp.route('/session')
def show_session():
    """This function prints out the Session dictionary.
    This is only accessable through the URL and is used by the site developers for testing."""

    return dict(session)



@user_bp.route('/profile', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance
def profile():
    """This function displays the logged in user's information."""

    user = User.objects(id = session['user']['id']).first()

    return render_template("user/profile.html", user = user)


@user_bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance
def edit_profile():
    """This function provides the user with a form to edit their information."""

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
@check_disable
@check_maintenance
def change_password():
    """This function allows the user to change/update their password
    It is a seperate functionality from "Edit Profile" for extra validation and seperation of concerns."""

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



@user_bp.route('/favorites_list', methods=['GET', 'POST'])
@login_required
@check_disable
@check_maintenance
def view_favorites():
    """This function lets the Buyer user see their favorited items."""

    favorite_items = User.objects(id = session['user']['id']).get().favorites_list
    
    items = []

    for i in range(0, len(favorite_items)):

        item = Item.objects(id = favorite_items[i]).first()
        items.append(item)
           
    return render_template("user/favorites_list.html", items = items)


@user_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
@check_disable
@check_maintenance
def add_category():
    """This function is accessed by the Admin only, it lets them add a new category for items.
    The changes made here can be viewed when a Seller user chooses a category when adding a new item."""

    add_category_form = AddCategoryForm()

    if add_category_form.validate_on_submit():


        category_value = add_category_form.value.data
        category_label = add_category_form.label.data

        new_category = Category( value = category_value, label = category_label)

        new_category.save()
        
        return redirect(url_for("user.profile"))

    return render_template("user/add_category.html", form = add_category_form)




@user_bp.route('/display_users', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance
def display_users():
    """This function is for the Admin only (if statement in the template)
    It lets them preview all the users and their status.
    Also, it allows the admin to Delete or Disable any user(s)."""

    users = User.objects()

    buyer_users = User.objects(role = 0)

    seller_users = User.objects(role = 1)

    return render_template('user/display_users.html', users = users, buyer_users = buyer_users, seller_users = seller_users)


@user_bp.route('/delete_user/<user_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance
def delete_user(user_id):
    """This function removes the user specified from the database."""

    user = User.objects(id = user_id).first()

    user.delete()

    flash(f"'{user.username}' account has been deleted.")

    return redirect(url_for('user.display_users'))


@user_bp.route('/disable_user/<user_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance    
def disable_user(user_id) :
    """This function sets the "disable" attribute of the user to "True".
    Such user can't access anything on the site (because of the decorator)."""
    
    user = User.objects(id = user_id).first()
    
    user.disable = True

    user.save()

    flash(f"'{user.username}' account has been disabled.")

    return redirect(url_for('user.display_users'))


@user_bp.route('/unlock_user/<user_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance    
def unlock_user(user_id) :
    """This function sets the "disable" attribute of the user to "False".
    Such user can now use the site as usual with no restrictions."""
    
    user = User.objects(id = user_id).first()
    
    user.disable = False

    user.save()

    flash(f"'{user.username}' account has been unlocked.")

    return redirect(url_for('user.display_users'))


@user_bp.route('/maintenance_mode', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance    
def maintenance_mode():
    """This function sets the "maintenance" attribute of all users to "True".
    All users will see the Maintenance Page when trying to access any page on the site."""

    User.objects(role = 0).update(maintenance = True) 

    User.objects(role = 1).update(maintenance = True) 

    flash('The website is currently under maintenance.')

    return redirect(url_for('user.profile'))


@user_bp.route('/maintenance_mode_off', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance    
def maintenance_mode_off():
    """This function sets the "maintenance" attribute of all users to "False".
    All users will be able to access any page on the site normally."""
    
    User.objects(role = 0).update(maintenance = False) 

    User.objects(role = 1).update(maintenance = False)

    flash('The website is back online!')
    
    return redirect(url_for('user.profile'))


@user_bp.route('/disable_list', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance  
def disable_list():
    """This function can be accessed by the Admin user to view which users they have locked(disable)."""

    users = User.objects(disable = True)

    return render_template('user/disable_list.html', users = users)
    

@user_bp.route('/buy_requests', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def buy_requests():
    """This function is accessed by the Buyer user to view their Buy Requests and their status."""

    requests_list = BuyRequest.objects(user = session['user']['id'])

    return render_template('user/buy_requests.html', requests_list = requests_list)


@user_bp.route('/review_buy_requests', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def review_buy_requests():
    """This function is accessed by the Seller user to display the Buy Requests on their items.
    There they can choose to Approve or Decline a request."""

    current_user = User.objects(id = session['user']['id']).first()

    my_items = Item.objects(user = current_user)
    
    my_buy_requests = []

    for item in my_items:
            
        my_buy_requests.append(BuyRequest.objects(item = item))

    return render_template("user/review_buy_requests.html", my_buy_requests = my_buy_requests)



@user_bp.route('/approve_buy_request/<item_id>/<request_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def approve_buy_request(item_id, request_id):
    """This function sets the "status" of a Buy Request to 'Approved'.
    Also, sets the "sold" attribute of the item to 'True'."""

    item = Item.objects(id = item_id).first()
    item.sold = True
    Item.objects(id = item_id).update_one(unset__buy_requests_list = request_id)
    item.save()

    request = BuyRequest.objects(id = request_id).first()
    request.status = "Approved"
    request.save()

    flash("Item has been sold!")
    
    return redirect(url_for('user.review_buy_requests'))


@user_bp.route('/decline_buy_request/<item_id>/<request_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def decline_buy_request(item_id, request_id):
    """This function sets the "status" of a Buy Request to 'Declined'."""

    Item.objects(id = item_id).update_one(unset__buy_requests_list = request_id)
    
    request = BuyRequest.objects(id = request_id).first()
    request.status = "Declined"
    request.save()

    flash("Buy Request has been declined!")
    
    return redirect(url_for('user.review_buy_requests'))



@user_bp.route('/upgrade_request', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def upgrade_request():
    """This function is accessed when a Buyer user wants to become a Seller user.
    The function creates a request of type upgrade with a "Pending" status for them."""

    request = UpgradeRequest.objects(user = session['user']['id']).first()

    if not request:

        upgrade_request = UpgradeRequest(user = session['user']['id'], status = "Pending")

        upgrade_request.save()

        flash("Upgrade Request has been sent.")

    else:

        flash("You have already sent an Upgrade Request.")


    return redirect(url_for("user.profile"))



@user_bp.route('/review_upgrade_requests', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def review_upgrade_requests():
    """This function is available for the Admin user to preview Upgrade Requests to choose to Approve or Decline."""

    users = User.objects()

    upgrade_requests = []

    for user in users:
        upgrade_requests.append(UpgradeRequest.objects(user = user).all())

    return render_template("user/review_upgrade_requests.html", upgrade_requests = upgrade_requests)


@user_bp.route('/approve_upgrade_request/<request_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def approve_upgrade_request(request_id):
    """This function sets the "status" of an Upgrade Request to 'Approved'.
    Also, sets the "role" of the user to '1' (Seller)."""

    request = UpgradeRequest.objects(id = request_id).first()
    request.status = "Approved"
    request.save()

    request.user.role = 1
    request.user.save()
    
    flash("Upgrade Request has been approved.")

    return redirect(url_for("user.review_upgrade_requests"))


@user_bp.route('/decline_upgrade_request/<request_id>', methods=['POST', 'GET'])
@login_required
@check_disable
@check_maintenance 
def decline_upgrade_request(request_id):
    """This function sets the "status" of an Upgrade Request to 'Declined'.
    Also, sets the "role" of the user to '0' (Buyer). Just in case the Admin changed their mind :P"""

    request = UpgradeRequest.objects(id = request_id).first()
    request.status = "Declined"
    request.save()

    request.user.role = 0
    request.user.save()

    flash("Upgrade Request has been declined.")
    

    return redirect(url_for("user.review_upgrade_requests"))
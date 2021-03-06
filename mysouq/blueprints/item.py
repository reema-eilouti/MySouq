from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from mysouq.models.user import User
from mysouq.models.item import Item, Category
from mysouq.models.requests import BuyRequest
from mysouq.forms.item_forms import AddItemForm, EditItemForm

item_bp = Blueprint('item', __name__)


@item_bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    """This function is available for the Seller User, it provides them with a form to add an item for sale."""

    add_item_form = AddItemForm()

    categories = Category.objects()

    add_item_form.category.choices = [(category.value, category.label) for category in categories]

    if add_item_form.validate_on_submit():

        title = add_item_form.title.data
        description = add_item_form.description.data
        price = add_item_form.price.data
        category = add_item_form.category.data

        item = Item(user = session['user']['id'], title = title, description = description, price = price, category = category)
        
        item.save()

        flash("Your item has been successfully added.")

        return redirect(url_for('user.home'))

    return render_template("item/add_item.html", form = add_item_form)


@item_bp.route('/edit_item/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """This function is available for the Seller User, it provides them with a form to edit an item of theirs.
    Another Seller user can try to edit an item that is not theirs but will be flashed by a message preventing them to do so."""

    edit_item_form = EditItemForm()

    categories = Category.objects()

    edit_item_form.category.choices = [(category.value, category.label) for category in categories]

    item = Item.objects(id = item_id).first()

    if request.method == "GET":

        edit_item_form.title.data = item.title
        edit_item_form.description.data = item.description
        edit_item_form.price.data = item.price
        edit_item_form.category.data = item.category


    if edit_item_form.validate_on_submit():

        item_user = item.user

        user = User.objects(id = session['user']['id']).first()

        if user == item_user :

            item.title = edit_item_form.title.data
            item.description = edit_item_form.description.data
            item.price = edit_item_form.price.data
            item.category = edit_item_form.category.data
            
            item.save()

            flash("Your item has been edited successfully.")

        else:

            flash("Action Not Allowed: Editing an item you don't own.")

        return redirect(url_for('user.home'))


    return render_template("item/edit_item.html", form = edit_item_form)    

 
@item_bp.route('/delete_item/<item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    """This function is available for the Seller User, it allows them to delete an item of theirs.
    Another Seller user can try to delete an item that is not theirs but will be flashed by a message preventing them to do so."""

    item = Item.objects(id = item_id).first() 

    item_user = item.user

    user = User.objects(id = session['user']['id']).first()

    if user == item_user :

        Item.objects(id = item_id, user = session['user']['id']).first().delete()

        flash('Item has been deleted')

    else: 

        flash("Action Not Allowed: Deleting an item you don't own.")

    return redirect(url_for("user.home"))  


@item_bp.route('/sort_by_date', methods=['GET', 'POST'])
def sort_by_date():
    """This function brings items from the database ordered descendingly by the date of their addition for the user to view."""

    items = Item.objects.order_by('-date')

    return render_template("base.html", items = items)        


@item_bp.route('/sort_by_price', methods=['GET', 'POST'])
def sort_by_price():
    """This function brings items from the database ordered descendingly by their price for the user to view."""

    items = Item.objects.order_by('-price')

    return render_template("base.html", items = items)    


@item_bp.route("/search", methods=['POST'])
def search_items():
    """This function is used when a user searches for a word; it can either be in the title or description.
    If the word was in the title of an item and the description of another, the priority is for the title."""
    
    if request.method == 'POST':
        
        search_keyword = str(request.form['search_keyword'])  

        results = Item.objects.search_text(search_keyword).order_by('$text_score')
        
        return render_template("item/searched_items.html", items = results, search_keyword = search_keyword)  


@item_bp.route('/item/<item_id>/add_favorite')
def add_favorite(item_id):
    """This function lets a Buyer user add items to the Favorites List."""

    User.objects(id = session['user']['id']).update_one(add_to_set__favorites_list = item_id)

    flash("Added To Favorites")

    return redirect(url_for('user.home'))          


@item_bp.route('/item/<item_id>/buy')
def buy_item(item_id):
    """This function allows a Buyer user to send a Buy Request to the seller of an item to be reviewed."""

    request = BuyRequest.objects(user = session['user']['id'], item = item_id).first()

    if not request:

        buy_request = BuyRequest(user = session['user']['id'], item = item_id, status = 'Pending')

        buy_request.save()
        
        Item.objects(id = item_id).update_one(add_to_set__buy_requests_list = buy_request.id)

        flash("A Buy Request has been sent to the item seller.")

    else:
        flash("Item already in your Buy Requests.")

    return redirect(url_for('user.home'))
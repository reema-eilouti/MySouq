from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from mysouq.models.user import User
from mysouq.models.item import Item
from mysouq.models.requests import BuyRequest, UpgradeRequest
from mysouq.forms.item_forms import AddItemForm, EditItemForm

item_bp = Blueprint('item', __name__)


@item_bp.route('/add_item', methods=['GET', 'POST'])
def add_item():

    add_item_form = AddItemForm()

    if add_item_form.validate_on_submit():

        title = add_item_form.title.data
        description = add_item_form.description.data
        price = add_item_form.price.data
        category = add_item_form.category.data

        item = Item(title = title, description = description, price = price, category = category)
        
        item.save()

        flash("Your item has been successfully added.")

        return redirect(url_for('user.home'))

    return render_template("item/add_item.html", form = add_item_form)


@item_bp.route('/edit_item/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

    edit_item_form = EditItemForm()

    item = Item.objects(id = item_id).first()

    if request.method == "GET":

        edit_item_form.title.data = item.title
        edit_item_form.description.data = item.description
        edit_item_form.price.data = item.price
        edit_item_form.category.data = item.category


    if edit_item_form.validate_on_submit():

        item.title = edit_item_form.title.data
        item.description = edit_item_form.description.data
        item.price = edit_item_form.price.data
        item.category = edit_item_form.category.data
        
        item.save()

        flash("Your item has been edited successfully.")

        return redirect(url_for('user.home'))

    return render_template("item/edit_item.html", form = edit_item_form)    

    
@item_bp.route('/delete_item/<item_id>', methods=['GET', 'POST'])
def delete_item(item_id):

    Item.objects(id = item_id).first().delete()

    return redirect(url_for("user.home"))  


@item_bp.route('/sort_by_date', methods=['GET', 'POST'])
def sort_date_items():

    items = Item.objects.order_by('-date')

    return render_template("base.html", items = items)        


@item_bp.route('/sort_by_price', methods=['GET', 'POST'])
def sort_price_items():

    items = Item.objects.order_by('-price')

    return render_template("base.html", items = items)    


@item_bp.route("/search", methods=['POST'])
def search_items():
    
    if request.method == 'POST':
        
        search_keyword = str(request.form['search_keyword'])  
        results = Item.objects.search_text(search_keyword).order_by('$text_score')
        
        return render_template("item/search-result.html", items = results, search_keyword = search_keyword)  


@item_bp.route('/item/<item_id>/add_favorite')
def add_favorite(item_id):

    User.objects(id = session['user']['id']).update_one(add_to_set__favorite = item_id)

    flash("Added To Favorites")

    return redirect(url_for('user.home'))          


@item_bp.route('/item/<item_id>/buy')
def buy_item(item_id):

    buy_request = BuyRequest(user = session['user']['id'], item = item_id, status = 'Pending')

    buy_request.save()
    
    buy_requests = BuyRequest.objects(item = item_id)

    print(buy_requests)
    
    Item.objects(id = item_id).update_one(add_to_set__buy_request_list = buy_request.id)

    return redirect(url_for('user.home', buy_requests = buy_requests))
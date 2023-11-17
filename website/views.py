from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Users, Items, Categories, Fronts, Roles, Preset, Order
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", current_user=current_user)

@views.route('/item', methods=['GET', 'POST'])
@login_required
def	item():
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	items = Items.query.all()
	if request.method == 'POST':
		try:
			name = request.form.get('name')
			cat_id = request.form.get('category_id')
			print(cat_id)
			item = Items(name=name, category_id=cat_id)
			db.session.add(item)
			db.session.commit()
			flash('Item added!', category='success')
			return redirect(url_for('views.item'))
		except:
			flash('Error adding item.', category='error')
			return redirect(url_for('views.item'))
	category_DB = Categories.query.all()
	for item in Items.query.all():
		print(item.name, item.category_id, category_DB[item.category_id-1].name)
	return render_template("item.html", user=current_user, items=items, categories=category_DB, category_list=category_DB)


@views.route('/preset', methods=['GET', 'POST'])
@login_required
def preset():
	items = Items.query.all()
	category_list = Categories.query.all()
	categories = []
	for cate in category_list :
		categories.append(cate.name)
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		json_obj_dict = {"item_list": []}
		try:
			print("in progress")
			name = request.form.get("name")
			if not name:
				raise Exception("Please fill out all fields.")
			elem = request.form.get("item0")
			i = 0
			while (elem != None):
				elem = request.form.get(f"item{i}")
				quant = request.form.get(f"quantity{i}")
				if elem != None:
					print(elem, quant)
					json_obj_dict["item_list"].append({"item_id": int(elem), "quantity": int(quant)})
				i += 1
			print(json_obj_dict)
			#put item_list in db
		except Exception as e:
			flash(f'Error adding item: {str(e)}', category='error')
			return redirect(url_for('views.preset'))
		else:
			preset = Preset(name=name, item_list=json_obj_dict)
			db.session.add(preset)
			db.session.commit()
			flash('Preset added!', category='success')
			return redirect(url_for('views.preset'))
	return render_template("preset.html", user=current_user, items=items, categories=category_list) #my_cat=categories) #todo check if my_cat is needed





@views.route('/order', methods=['GET', 'POST'])
@login_required
def	order():
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	presets = Preset.query.all()
	items = Items.query.all()
	print(presets)
			# print(Items.query.filter_by(id=item["item_id"]).first().name, item["quantity"])
	# create_order(current_user)
	return render_template("order.html", current_user=current_user, presets=presets, items=items)




def	create_order(current_user):
	preset = Preset.query.all()
	for p in preset:
		if p.id == 1:
			preset_id = p.id
	front = Fronts.query.all()
	for f in front:
		if f.id == 1:
			front_id = f.id
	status = "In progress"
	created_by = current_user.id
	create_order = Order(preset_id=preset_id, front=front_id, status=status, created_by=created_by)
	db.session.add(create_order)
	db.session.commit()


@views.route('/logi', methods=['GET', 'POST'])
@login_required
def	logi():
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	orders = Order.query.all()
	fronts = Fronts.query.all()
	presets = Preset.query.all()
	items = Items.query.all()
	users = Users.query.all()
	for user in users:
		print(user.username, user.id)
	for order in orders:
		print(order.created_at)
	return render_template("logi.html", current_user=current_user, orders=orders, fronts=fronts, presets=presets, items=items, users=users)


@views.route('/fronts', methods=['GET', 'POST'])
@login_required
def fronts():
	fronts = Fronts.query.all()
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		try:
			name = request.form.get('name')
			region = request.form.get('region')
			create_by = current_user.id
			if not name or not region:
				flash('Please fill out all fields.', category='error')
				return redirect(url_for('views.fronts'))
			front = Fronts(name=name, region=region, create_by=Users.query.filter_by(id=create_by).first().id)
			db.session.add(front)
			db.session.commit()
			flash('Front added!', category='success')
			return redirect(url_for('views.fronts'))
		except Exception as e:
			flash(f'Error Create front: {str(e)}', category='error')
			return redirect(url_for('views.fronts'))
	return render_template("fronts.html", current_user=current_user, fronts=fronts)


@views.route('/fronts/<int:id>/', methods=['GET', 'POST'])
@login_required
def order_front(id):
	front = Fronts.query.get_or_404(id)
	users = Users.query.all()
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		try:
			return redirect(url_for('views.order_front'))
		except Exception as e:
			flash(f'Error  front: {str(e)}', category='error')
			return redirect(url_for('views.order_front'))
	return render_template("front.html", current_user=current_user, users=users, front=front)






















@views.route('/admin')
@login_required
def admin():
	users = Users.query.all()
	roles = Roles.query.all()
	if current_user.username == 'Neoblacks' or current_user.role_id == 1:
		return render_template("admin.html", users=users, current_user=current_user, roles=roles)
	else:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))

@views.route('/admin/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	user = Users.query.get_or_404(id)
	roles = Roles.query.all()
	if request.method == 'POST':
		try:
			user.role_id = request.form.get('role')
			db.session.commit()
			flash('User role updated!', category='success')
			return redirect(url_for('views.admin'))
		except:
			flash('Error updating user role.', category='error')
			return redirect(url_for('views.admin'))
	else:
		return render_template("edit.html", user=user, current_user=current_user, roles=roles)

@views.route('/admin/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
	if current_user.username != 'Neoblacks' and current_user.role_id != 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	user = Users.query.get_or_404(id)
	if request.method == 'POST':
		try:
			db.session.delete(user)
			db.session.commit()
			flash('User deleted!', category='success')
			return redirect(url_for('views.admin'))
		except:
			flash('Error deleting user.', category='error')
			return redirect(url_for('views.admin'))
	else:
		return render_template("delete.html", user=user, current_user=current_user)

def	delete_role():
	role = Roles.query.all()
	for r in role:
		db.session.delete(r)
		db.session.commit()
		print(f"Role {r.name} deleted")

def	create_role():
	list_role = ['Admin', 'Leader', 'Coordinator', 'Head Logi', 'Head Front', 'Officier Logi', 'Officier Front', 'Trusted Logi', 'Trusted Soldier', 'Soldier', 'Inconnu']
	list_height = [100, 90, 80, 70, 70, 60, 60, 50, 40, 30, 0]
	for i in range(len(list_role)):
		role = Roles(name=list_role[i], height=list_height[i])
		db.session.add(role)
		db.session.commit()
		print(f"Role {list_role[i]} added")
	user = Users.query.all()
	for u in user:
		db.session.delete(u)
		db.session.commit()

@views.route('/admin/reset')
@login_required
def reset_admin():
	if current_user.username != 'Neoblacks' and current_user.role_id == 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	delete_role()
	create_role()
	return redirect(url_for('views.admin'))


path_file = "./List_item.json"

def parseFile(path_file):
	with open(path_file) as f:
		ob = json.loads(f.read())
		return (ob)

o = parseFile(path_file)
def delete_item():
	item = Items.query.all()
	for i in item:
		db.session.delete(i)
		db.session.commit()

def delete_category():
	category = Categories.query.all()
	for c in category:
		db.session.delete(c)
		db.session.commit()
		print(f"Category {c.name} deleted")

def add_category():
	for categ in o:
		cat = Categories(name=categ)
		db.session.add(cat)
		db.session.commit()
		for item in o[categ]:
			item = Items(name=item, category_id=Categories.query.filter_by(name=categ).first().id)
			db.session.add(item)
			db.session.commit()






@views.route('/item/reset')
@login_required
def reset():
	if current_user.username != 'Neoblacks' and current_user.role_id == 1:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	delete_item()
	delete_category()
	add_category()
	return redirect(url_for('views.item'))

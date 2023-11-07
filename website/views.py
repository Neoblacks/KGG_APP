from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Item, Preset, Category
from . import db
import os
import csv

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", user=current_user)

def handle_category():
	category = Category.query.all()
	for categorie in category:
		db.session.delete(categorie)
		db.session.commit()
	categories = ['Weapon', 'Heavy Weapon', 'Ammu heavy', 'Equipment', 'Medical', 'Materials', 'Jacket', 'Vehicles', 'Structures']
	for category in categories:
		cat = Category(name=category)
		db.session.add(cat)
		db.session.commit()

def handle_items():
	path_txt = "./List of all item foxhole - Feuille 1 (1).csv"
	ifile =csv.DictReader(open(path_txt))
	for row in ifile:
		print(row)
	# with open(path_txt, mode="r") as py_file:
	# 	print(py_file.read())
	pass#Faudra changer la structure du CSV là c'est la merde à lire, je vais ranger les courses je re

def handle_database():
	#handle_category()
	handle_items()
handle_database()


@views.route('/item', methods=['GET', 'POST'])
@login_required
def	item():
	if current_user.username != 'Neoblacks' and current_user.role != 'Admin':
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	items = Item.query.all()
	# category_DB = Category.query.all()
	if request.method == 'POST':
		try:
			name = request.form.get('name')
			cat_id = request.form.get('category_id')
			print(cat_id)
			item = Item(name=name, category_id=cat_id)
			db.session.add(item)
			db.session.commit()
			flash('Item added!', category='success')
			return redirect(url_for('views.item'))
		except:
			flash('Error adding item.', category='error')
			return redirect(url_for('views.item'))
	category_DB = Category.query.all()
	# print name of all items with category id and name
	for item in Item.query.all():
		print(item.name, item.category_id, category_DB[item.category_id-1].name)
	return render_template("item.html", user=current_user, items=items, categories=category_DB, category_list=category_DB)


@views.route('/preset', methods=['GET', 'POST'])
@login_required
def preset():
	items = Item.query.all()
	print(items)
	category_list = Category.query.all()
	categories = []
	for cate in category_list :
		categories.append(cate.name)
	print(categories)
	if current_user.username != 'Neoblacks' and current_user.role != 'Admin':
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		try:
			print("in progress")
		except Exception as e:
			flash(f'Error adding item: {str(e)}', category='error')
			return redirect(url_for('views.preset'))
	return render_template("preset.html", user=current_user, items=items, categories=category_list, my_cat=categories)

# @views.route('/testview')
# def testview():
# 	category_id = request.args.get('category_id')
# 	items = Item.query.filter_by(category_id=category_id).all()
# 	options = '\n'.join([f'<option value="{item.id}">{item.name}</option>' for item in items])
# 	print(options)
# 	return (options)

@views.route('/admin')
@login_required
def admin():
	create_category()
	users = User.query.all()
	if current_user.username == 'Neoblacks':
		return render_template("admin.html", users=users, user=current_user)
	else:
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))

@views.route('/admin/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
	if current_user.username != 'Neoblacks' and current_user.role != 'Admin':
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	user = User.query.get_or_404(id)
	if request.method == 'POST':
		user.role = request.form['role']
		try:
			db.session.commit()
			flash('User role updated!', category='success')
			print(User.query.get_or_404(id).role)
			return redirect(url_for('views.admin'))
		except:
			flash('Error updating user role.', category='error')
			return redirect(url_for('views.admin'))
	else:
		return render_template("edit.html", user=user, current_user=current_user)

@views.route('/admin/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
	if current_user.username != 'Neoblacks' and current_user.role != 'Admin':
		flash('You are not authorized to view this page.', category='error')
		return redirect(url_for('views.home'))
	user = User.query.get_or_404(id)
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


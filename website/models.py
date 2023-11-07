from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), unique=True)
	height = db.Column(db.Integer)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	role = db.Column(db.String(10), default='inconnu')
	player_role = db.Column(db.String(10))
	region = db.Column(db.String(150))
	sub_region = db.Column(db.String(150))


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), unique=True) # Weapon, Heavy Weapon, Ammu heavy, Equipment, Medical, Materials, Jacket, Vehicles, Structures

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), unique=True)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Preset(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	item_list_id = db.Column(db.Integer, db.ForeignKey('presetItem.id'))

class PresetItem(db.Model):
	id	= db.Column(db.Integer, primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
	quantity = db.Column(db.Integer)


class Fronts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_of_front = db.Column(db.String(150))
	region = db.Column(db.String(150))

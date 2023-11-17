from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Roles(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), unique=True)
	height = db.Column(db.Integer)

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=11)
	front = db.Column(db.Integer, db.ForeignKey('fronts.id'))


class Categories(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), unique=True) # Weapon, Heavy Weapon, Ammu heavy, Equipment, Medical, Materials, Jacket, Vehicles, Structures

class Items(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), unique=True)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class Preset(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	item_list = db.Column(db.JSON)

class	Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	front = db.Column(db.Integer, db.ForeignKey('fronts.id'))
	preset_id = db.Column(db.Integer, db.ForeignKey('preset.id'))
	status = db.Column(db.String(150))
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
	created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Fronts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	region = db.Column(db.String(150))
	create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
	# created_at = db.Column(db.DateTime(timezone=True), default=func.now())

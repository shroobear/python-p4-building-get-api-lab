#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []

    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
            "baked_goods": []
        }
        
        for bg in bakery.baked_goods:
            baked_good_dict = {
                "id": bg.id,
                "name": bg.name,
                "price": bg.price,
                "bakery_id": bg.bakery_id,
                "created_at": bg.created_at,
                "updated_at": bg.updated_at
            }
            bakery_dict['baked_goods'].append(baked_good_dict)
        
        bakeries.append(bakery_dict)
    
    response = make_response(
        jsonify(bakeries),
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    bakery_dict = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at,
        "baked_goods": []
    }
    for bg in bakery.baked_goods:
        baked_good_dict = {
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "bakery_id": bg.bakery_id,
            "created_at": bg.created_at,
            "updated_at": bg.updated_at
        }
        bakery_dict['baked_goods'].append(baked_good_dict)
    
    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    bg_list = []
    for bg in baked_goods:
        baked_good_dict = {
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "bakery_id": bg.bakery_id,
            "created_at": bg.created_at,
            "updated_at": bg.updated_at
        }
        bg_list.append(baked_good_dict)
    response = make_response(
        jsonify(bg_list),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    bakery = Bakery.query.filter(Bakery.id == expensive_bg.bakery_id)[0]
    expensive_bg_dict = {
        "bakery_id": expensive_bg.bakery_id,
        "created_at": expensive_bg.created_at,
        "id": expensive_bg.id,
        "name": expensive_bg.name,
        "price": expensive_bg.price,
        "updated_at": expensive_bg.updated_at
    }
    expensive_bg_dict['bakery'] = {
        "created_at": bakery.created_at,
        "id": bakery.id,
        "name": bakery.name,
        "updated_at": bakery.updated_at
    }

    response = make_response(
        jsonify(expensive_bg_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

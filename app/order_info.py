# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, jsonify
import hashlib
from . import db
from .models import Order, Dishes, Store, User

order_info = Blueprint('order', __name__)

@order_info.route('/user/<userID>/orders/<orderID>', methods=['GET', 'POST'])
def order_info_detail(userID, orderID):
    '''
    SXT
    订单详情api
    用户身份和订单信息确认后输出订单详细信息,失败返回（401）
    '''
    token = request.headers['accesstoken']
    user = User.verify_auth_token(token)
    if not user:
        return jsonify({'status_code': '401', 'error_message': 'Unauthorized'})
    listFood = []
    if request.method == 'GET':
        if vaild_order(userID, orderID):
            for per_user_order in Order.query.order_by(Order.id):
                if (per_user_order.id == orderID):
                    dishes = Dishes.query.filter_by(id = per_user_order.dishesId).first()
                    store_name = Store.query.filter_by(id = dishes.storeId).first().store_name
                    Food_detail = {
                        "dishName": dishes.dishName,
                        "price": dishes.dishPrice,
                        "number": 'undefined'
                    }
                    listFood.append(Food_detail)
                else:
                    return jsonify({'status_code': '401', 'error_message': 'No Orders'})
            status_code = '201'
            order_hash = hashlib.md5(orderID)
            order_detail = {
                'status_code': status_code,
                'storeName': store_name,
                'foodList': listFood,
                'mealFee': 'undefined',
                'ServiceFee': 'undefined',
                'totalFee': per_user_order.totalPrice,
                'Offer': 'undefined',
                'paymentMethod': 'undefined',
                'Date': per_user_order.createTime,
                'orderNumber': order_hash.hexdigest()
            }
            json_order_data = jsonify(order_detail)
            return json_order_data
        else:
            return jsonify({'status_code': '401', 'error_message': 'No User'})

def vaild_order(userID, OrderID):
    if userID is None or OrderID is None:
        return False
    if Order.query.filter_by(username= userID).first() is None:
        return False
    return True

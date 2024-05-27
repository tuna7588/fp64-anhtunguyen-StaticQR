import os
from flask import Flask, request, jsonify, url_for, session, redirect, render_template, flash
# from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import MenuStructure


app = Flask(__name__)
app.secret_key = 'mysecretkey'
# app.url_map.strict_slashes = False
# CORS(app)
users = {
    'admin': {'username': 'admin', 'password': 'admin'}
}

example_menu = MenuStructure("Example")
salad = {
    "name": "Salad", 
    "description": ["lettuce", "tomato", "cilantro", "chicken"], 
    "price": 5.99, 
    "category": "starters"
    }

pho = {
    "name": "Pho", 
    "description": ["noodles", "ginger", "beef", "lime"], 
    "price": 7.99, 
    "category": "main course"
}

tiramisu = {
    "name": "tiramisu", 
    "description": ["mascarpone", "matcha"], 
    "price": 3.99, 
    "category": "desserts"
}

example_menu.add_dish(salad)
example_menu.add_dish(pho)
example_menu.add_dish(tiramisu)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
# @app.route('/')
# def sitemap():
#     return generate_sitemap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    return render_template('admin.html')

@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    dishes = example_menu.get_all_dishes()
    return jsonify(dishes), 200

@app.route('/dishes/<int:id>', methods=['GET'])
def get_single_dish(id):
    dish = example_menu.get_dish(id)
    return jsonify(dish), 200

@app.route('/dishes', methods=['POST'])
def create_dish():
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    dish = request.json
    print("added", dish)
    example_menu.add_dish(dish)
    if dish is not None:
        return "dish created", 200

@app.route('/dishes/<int:id>', methods=['PUT'])
def update_dish(id):
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    updated_dish = {}
    if 'name' in request.json:
        updated_dish['name'] = request.json['name']
    if 'ingredients' in request.json:
        updated_dish['ingredients'] = request.json['ingredients']
    if 'price' in request.json:
        updated_dish['price'] = request.json['price']
    if 'category' in request.json:
        updated_dish['category'] = request.json['category']

    dish = example_menu.update_dish(id, updated_dish)
    return jsonify(dish)

@app.route('/dishes/<int:id>', methods=['DELETE'])
def delete_single_dish(id):
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    dish = example_menu.get_dish(id)
 
    if dish:
        example_menu.delete_dish(id)
        return jsonify({"message": f"Dish deleted successfully: {dish}"}), 200
    else:
        return jsonify({"error": "Dish not found"}), 404
   

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

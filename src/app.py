import os
from flask import Flask, request, jsonify, url_for
# from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import MenuStructure
#from models import Person

app = Flask(__name__)
# app.url_map.strict_slashes = False
# CORS(app)

# create the jackson family object
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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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
    dish = request.json
    print("added", dish)
    example_menu.add_dish(dish)
    if dish is not None:
        return "dish created", 200
@app.route('/dishes/<int:id>', methods=['DELETE'])
def delete_single_dish(id):
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

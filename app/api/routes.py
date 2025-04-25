from flask import Blueprint, jsonify, request
import json
import os

api = Blueprint('api', __name__)

def load_recipes():
    file_path = os.path.join(os.path.dirname(__file__), 'recipes.txt')
    with open(file_path, 'r') as file:
        return json.load(file)

def save_recipes(recipes):
    file_path = os.path.join(os.path.dirname(__file__), 'recipes.txt')
    with open(file_path, 'w') as file:
        json.dump(recipes, file, indent=4)

def convert_temperature(temp, from_unit, to_unit):
    if from_unit == to_unit:
        return temp
    if from_unit == 'F' and to_unit == 'C':
        return round((temp - 32) * 5/9, 1)
    if from_unit == 'C' and to_unit == 'F':
        return round((temp * 9/5) + 32, 1)
    return temp

def scale_recipe(recipe, new_servings):
    scale_factor = new_servings / recipe['servings']
    scaled_recipe = recipe.copy()
    scaled_recipe['servings'] = new_servings
    scaled_recipe['ingredients'] = [
        {
            'name': ing['name'],
            'amount': round(ing['amount'] * scale_factor, 2),
            'unit': ing['unit']
        }
        for ing in recipe['ingredients']
    ]
    return scaled_recipe

@api.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify(load_recipes())

@api.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes['recipes'] if r['id'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'error': 'Recipe not found'}), 404

@api.route('/recipes/<int:recipe_id>/scale', methods=['GET'])
def scale_recipe_endpoint(recipe_id):
    try:
        new_servings = int(request.args.get('servings', 1))
    except ValueError:
        return jsonify({'error': 'Invalid servings value'}), 400
    
    recipes = load_recipes()
    recipe = next((r for r in recipes['recipes'] if r['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    
    scaled_recipe = scale_recipe(recipe, new_servings)
    return jsonify(scaled_recipe)

@api.route('/recipes/<int:recipe_id>/convert-temp', methods=['GET'])
def convert_temperature_endpoint(recipe_id):
    to_unit = request.args.get('to', '').upper()
    if to_unit not in ['F', 'C']:
        return jsonify({'error': 'Invalid temperature unit. Use F or C'}), 400
    
    recipes = load_recipes()
    recipe = next((r for r in recipes['recipes'] if r['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    
    if 'baking_temperature' not in recipe or 'temperature_unit' not in recipe:
        return jsonify({'error': 'Recipe does not have temperature information'}), 400
    
    converted_temp = convert_temperature(
        recipe['baking_temperature'],
        recipe['temperature_unit'],
        to_unit
    )
    
    return jsonify({
        'original_temperature': recipe['baking_temperature'],
        'original_unit': recipe['temperature_unit'],
        'converted_temperature': converted_temp,
        'converted_unit': to_unit
    }) 
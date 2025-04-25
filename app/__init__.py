from flask import Flask, render_template
from app.api.routes import api
import os

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/')
    def home():
        try:
            from app.api.routes import load_recipes
            recipes_data = load_recipes()
            return render_template('index.html', recipes=recipes_data['recipes'])
        except Exception as e:
            return f"Error loading recipes: {str(e)}", 500
    
    @app.route('/recipes')
    def recipes():
        try:
            from app.api.routes import load_recipes
            recipes_data = load_recipes()
            return render_template('recipes.html', recipes=recipes_data['recipes'])
        except Exception as e:
            return f"Error loading recipes: {str(e)}", 500
    
    @app.route('/recipe/<int:recipe_id>')
    def recipe_detail(recipe_id):
        try:
            from app.api.routes import load_recipes
            recipes_data = load_recipes()
            recipe = next((r for r in recipes_data['recipes'] if r['id'] == recipe_id), None)
            if not recipe:
                return "Recipe not found", 404
            return render_template('recipe_detail.html', recipe=recipe)
        except Exception as e:
            return f"Error loading recipe: {str(e)}", 500
    
    @app.route('/recipe/<int:recipe_id>/scale')
    def scale_recipe(recipe_id):
        try:
            from app.api.routes import load_recipes, scale_recipe
            recipes_data = load_recipes()
            recipe = next((r for r in recipes_data['recipes'] if r['id'] == recipe_id), None)
            if not recipe:
                return "Recipe not found", 404
            
            from flask import request
            new_servings = int(request.args.get('servings', recipe['servings']))
            scaled_recipe = scale_recipe(recipe, new_servings)
            return render_template('recipe_detail.html', recipe=scaled_recipe)
        except Exception as e:
            return f"Error scaling recipe: {str(e)}", 500
    
    @app.route('/recipe/<int:recipe_id>/convert-temp')
    def convert_temp(recipe_id):
        try:
            from app.api.routes import load_recipes, convert_temperature
            recipes_data = load_recipes()
            recipe = next((r for r in recipes_data['recipes'] if r['id'] == recipe_id), None)
            if not recipe:
                return "Recipe not found", 404
            
            from flask import request
            to_unit = request.args.get('to', '').upper()
            if to_unit not in ['F', 'C']:
                return "Invalid temperature unit", 400
            
            if 'baking_temperature' not in recipe or 'temperature_unit' not in recipe:
                return "Recipe does not have temperature information", 400
            
            converted_temp = convert_temperature(
                recipe['baking_temperature'],
                recipe['temperature_unit'],
                to_unit
            )
            
            recipe['baking_temperature'] = converted_temp
            recipe['temperature_unit'] = to_unit
            return render_template('recipe_detail.html', recipe=recipe)
        except Exception as e:
            return f"Error converting temperature: {str(e)}", 500
    
    return app 
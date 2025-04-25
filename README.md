# TableChef
Your Cooking Assistant!

# Recipe API

A Flask-based REST API for managing recipes with features for scaling ingredients and temperature conversion.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Get All Recipes
- **GET** `/recipes`
- Returns all available recipes

### Get Specific Recipe
- **GET** `/recipes/<recipe_id>`
- Returns details of a specific recipe

### Scale Recipe
- **GET** `/recipes/<recipe_id>/scale?servings=<number>`
- Scales the recipe ingredients for the specified number of servings
- Example: `/recipes/1/scale?servings=12`

### Convert Temperature
- **GET** `/recipes/<recipe_id>/convert-temp?to=<F|C>`
- Converts the recipe's baking temperature between Fahrenheit and Celsius
- Example: `/recipes/1/convert-temp?to=C`

## Example Usage

1. Get all recipes:
```bash
curl http://localhost:5000/recipes
```

2. Get a specific recipe:
```bash
curl http://localhost:5000/recipes/1
```

3. Scale a recipe for 12 servings:
```bash
curl http://localhost:5000/recipes/1/scale?servings=12
```

4. Convert temperature to Celsius:
```bash
curl http://localhost:5000/recipes/1/convert-temp?to=C
```

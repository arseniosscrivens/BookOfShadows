from flask import Flask, request, jsonify
from BoS_db import get_session, Category, Item, Alias, ChemicalComponent, Reference, Effect, Recipe, RecipeStep, Vocab, ReferenceInfo, Author

app = Flask(__name__)
session = get_session()

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = session.query(Category).all()
    return jsonify([{'id': category.id, 'name': category.name} for category in categories])

@app.route('/items/<int:category_id>', methods=['GET'])
def get_items(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'aliases': [{'alias': alias.alias} for alias in item.aliases],
        'chemical_components': [{'name': component.name, 'rank': component.rank} for component in item.chemical_components],
        'references': [{'refID': reference.refID, 'location': reference.location} for reference in item.references],
        'effects': [{'effect': effect.effect} for effect in item.effects],
        'consumable': item.consumable,
        'edible': item.edible,
        'open_practice': item.open_practice,
        'reason': item.reason,
        'appearance': item.appearance,
        'information': item.information
    } for item in items])

@app.route('/vocabulary/<int:category_id>', methods=['GET'])
def get_vocabulary(category_id):
    vocab_terms = session.query(Vocab).filter_by(category_id=category_id).all()
    return jsonify([{
        'id': term.id,
        'term': term.term,
        'definition': term.definition,
        'ref_id': term.ref_id
    } for term in vocab_terms])

@app.route('/recipes/<int:category_id>', methods=['GET'])
def get_recipes(category_id):
    recipes = session.query(Recipe).filter_by(category_id=category_id).all()
    return jsonify([{
        'id': recipe.id,
        'name': recipe.name,
        'information': recipe.information,
        'steps': [{'step_number': step.step_number, 'step_text': step.step_text} for step in recipe.steps]
    } for recipe in recipes])

@app.route('/references', methods=['GET'])
def get_references():
    references = session.query(ReferenceInfo).all()
    return jsonify([{
        'id': reference.id,
        'category': reference.category,
        'title': reference.title,
        'subtitle': reference.subtitle,
        'year': reference.year,
        'authors': [{'name': author.name} for author in reference.authors]
    } for reference in references])

if __name__ == '__main__':
    app.run(debug=True)

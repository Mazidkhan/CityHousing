from flask import Blueprint, request, render_template
import sqlite3

register_public_bp = Blueprint('register_public_bp', __name__)

def connect_db():
    return sqlite3.connect('house.db')

@register_public_bp.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flats")
    flats = cursor.fetchall()
 
    return render_template('/public/base.html', flats_filter=flats)

@register_public_bp.route('/find-space', methods=['GET'])
def find_space():
    city = request.args.get('city', '')
    location = request.args.get('location', '')
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch the unfiltered data for cities and locations
    cursor.execute("SELECT * FROM flats")
    flats_filter = cursor.fetchall()
    
    # Now filter the flats based on the selected city and location
    query = "SELECT * FROM flats WHERE 1=1"
    parameters = []
    
    if city:
        query += " AND city = ?"
        parameters.append(city)
    
    if location:
        query += " AND location = ?"
        parameters.append(location)
    
    cursor.execute(query, parameters)
    flats = cursor.fetchall()
    
    conn.close()

    # Return the filtered flats and unfiltered flats_filter for the dropdowns
    return render_template('/public/find_space.html', flats=flats, flats_filter=flats_filter)

@register_public_bp.route('/add-space')
def add_space():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flats")
    flats = cursor.fetchall()

    return render_template('/public/add_space.html',flats_filter=flats)
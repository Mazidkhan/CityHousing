from flask import Blueprint, request, render_template
import sqlite3

register_public_bp = Blueprint('register_public_bp', __name__)

def connect_db():
    return sqlite3.connect('house.db')

@register_public_bp.route('/find-space', methods=['GET'])
def find_space():
    city = request.args.get('city', '')
    location = request.args.get('location', '')    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT city, location FROM flats
        UNION
        SELECT DISTINCT city, location FROM bungalows
    """)
    flats_and_bungalows = cursor.fetchall()
    cursor.execute("SELECT * FROM bungalows")
    bungalows = cursor.fetchall()
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
    
    return render_template('/public/find_space.html', flats=flats, flats_filter=flats_and_bungalows, bungalows=bungalows)

@register_public_bp.route('/flat-details/<int:flat_id>', methods=['GET'])
def flats_details(flat_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch details for the selected flat
    cursor.execute("SELECT * FROM flats WHERE id = ?", (flat_id,))
    flat = cursor.fetchone()
    
    if flat is None:
        return "Flat not found", 404
    
    # Extract image filenames from the flat record
    images = [flat[6], flat[7], flat[8]]  # Adjust indices based on column positions
    cursor.execute("""
            SELECT DISTINCT city, location FROM flats
            UNION
            SELECT DISTINCT city, location FROM bungalows
        """)
    flats_and_bungalows = cursor.fetchall()
    return render_template('/public/flats_details.html', flat=flat, images=images, flats_filter=flats_and_bungalows)

@register_public_bp.route('/bungalow-details/<int:bungalow_id>', methods=['GET'])
def bungalows_details(bungalow_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch details for the selected flat
    cursor.execute("SELECT * FROM bungalows WHERE id = ?", (bungalow_id,))
    flat = cursor.fetchone()
    
    if flat is None:
        return "Flat not found", 404
    
    # Extract image filenames from the flat record
    images = [flat[6], flat[7], flat[8]]  # Adjust indices based on column positions
    cursor.execute("""
                SELECT DISTINCT city, location FROM flats
                UNION
                SELECT DISTINCT city, location FROM bungalows
            """)
    flats_and_bungalows = cursor.fetchall()
    return render_template('/public/bungalows_details.html', flat=flat, images=images, flats_filter=flats_and_bungalows)

@register_public_bp.route('/add-space')
def add_space():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT city, location FROM flats
        UNION
        SELECT DISTINCT city, location FROM bungalows
    """)
    flats_and_bungalows = cursor.fetchall()

    return render_template('/public/add_space.html',flats_filter=flats_and_bungalows)

@register_public_bp.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT city, location FROM flats
        UNION
        SELECT DISTINCT city, location FROM bungalows
    """)
    flats_and_bungalows = cursor.fetchall()
    return render_template('/public/base.html', flats_filter=flats_and_bungalows)

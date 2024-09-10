from flask import Blueprint, request, redirect, url_for, render_template, session, flash, jsonify
import sqlite3
from functools import wraps

register_bp = Blueprint('register_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'name' not in session:
            return redirect(url_for('register_bp.add_space'))  # Redirect to login if not authenticated
        return f(*args, **kwargs)
    return decorated_function

def connect_db():
    return sqlite3.connect('house.db')

@register_bp.route('/add-space')
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

@register_bp.route('/owner/register', methods=['POST'])
def register():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['phone'] = request.form['phone']
        city = request.form['city']
        location = request.form['location']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO owner (name, city, location, full_address, phone, email, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (session['name'], city, location, address, phone, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('register_public_bp.add_space'))

@register_bp.route('/owner/login', methods=['POST'])
def login():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        name = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM owner WHERE name = ? AND password = ?", (name, password))
        existing_user = cursor.fetchone()

        conn.commit()
        conn.close()

        if existing_user:
            session['name'] = name
            session['password'] = password
            session['phone'] = existing_user[4]
            return render_template('/owner/base.html')  # Assuming you have a route named 'base'
        else:
            return render_template('/public/add_space.html', error="Incorrect details. Please try again.")

@register_bp.route('/owner/profile')
@login_required
def profile():
    conn = connect_db()
    cursor = conn.cursor()
    existing_user = cursor.execute("SELECT * FROM owner WHERE name = ? AND password = ?", (session['name'], session['password'])).fetchall()
    conn.close()
    return render_template('/owner/profile.html',existing_user=existing_user)

@register_bp.route('/owner/flats', methods=['GET', 'POST'])
@login_required
def flats():
    if request.method == 'POST':
        # Handling form submission (POST request)
        city = request.form['city']
        location = request.form['location']
        address = request.form['address']
        status = request.form['status']
        price = request.form['price']
        description = request.form['description']
        image1 = request.files['image1']
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')

        # Save images
        image1_filename = image1.filename
        image1.save(f'static/images/{image1_filename}')
        image2_filename = image2.filename if image2 else None
        image3_filename = image3.filename if image3 else None
        if image2:
            image2.save(f'static/images/{image2_filename}')
        if image3:
            image3.save(f'static/images/{image3_filename}')

        # Insert data into the flats table
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO flats (city, location, full_address, status, price, image1, image2, image3, description, owner, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (city, location, address, status, price, image1_filename, image2_filename, image3_filename, description, session['name'], session['phone'])
        )
        conn.commit()
        conn.close()

        flash('Flat added successfully!')
        return redirect(url_for('register_bp.flats'))

    # Handling GET request: retrieve flats data from the database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flats where owner = ? and phone = ?",(session['name'], session['phone']))
    flats_data = cursor.fetchall()
    conn.close()

    # Pass flats data to the template, or a message if no data exists
    if flats_data:
        return render_template('/owner/flats.html', flats=flats_data)
    else:
        flash('No flats added.')
        return render_template('/owner/flats.html', flats=None)

@register_bp.route('/owner/bungalows', methods=['GET', 'POST'])
@login_required
def bungalows():
    if request.method == 'POST':
        # Handling form submission (POST request)
        city = request.form['city']
        location = request.form['location']
        address = request.form['address']
        status = request.form['status']
        price = request.form['price']
        description = request.form['description']
        image1 = request.files['image1']
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')

        # Save images
        image1_filename = image1.filename
        image1.save(f'static/images/{image1_filename}')
        image2_filename = image2.filename if image2 else None
        image3_filename = image3.filename if image3 else None
        if image2:
            image2.save(f'static/images/{image2_filename}')
        if image3:
            image3.save(f'static/images/{image3_filename}')

        # Insert data into the flats table
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bungalows (city, location, full_address, status, price, image1, image2, image3, description, owner, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (city, location, address, status, price, image1_filename, image2_filename, image3_filename, description, session['name'], session['phone'])
        )
        conn.commit()
        conn.close()

        flash('Bungalow added successfully!')
        return redirect(url_for('register_bp.bungalows'))

    # Handling GET request: retrieve flats data from the database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bungalows where owner = ? and phone = ?",(session['name'], session['phone']))
    bungalows_data = cursor.fetchall()
    conn.close()

    # Pass flats data to the template, or a message if no data exists
    if bungalows_data:
        return render_template('/owner/bungalows.html', bungalows=bungalows_data)
    else:
        flash('No flats added.')
        return render_template('/owner/bungalows.html', flats=None)

@register_bp.route('/owner/flats/<int:flat_id>', methods=['PUT'])
@login_required
def update_flat(flat_id):
    # Get data from request
    city = request.form.get('city')
    location = request.form.get('location')
    address = request.form.get('address')
    status = request.form.get('status')
    price = request.form.get('price')
    description = request.form.get('description')

    # Optionally handle image files if they are being updated
    image1 = request.files.get('image1')
    image2 = request.files.get('image2')
    image3 = request.files.get('image3')

    # Save images if provided
    if image1:
        image1_filename = image1.filename
        image1.save(f'static/images/{image1_filename}')
    if image2:
        image2_filename = image2.filename
        image2.save(f'static/images/{image2_filename}')
    if image3:
        image3_filename = image3.filename
        image3.save(f'static/images/{image3_filename}')

    # Update data in the flats table
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE flats 
        SET city = ?, location = ?, full_address = ?, status = ?, price = ?, image1 = ?, image2 = ?, image3 = ?, description = ? 
        WHERE id = ?
    """, (city, location, address, status, price, 
          image1_filename if image1 else None, 
          image2_filename if image2 else None, 
          image3_filename if image3 else None, 
          description, flat_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Flat updated successfully!'})

@register_bp.route('/owner/bungalows/<int:bungalow_id>', methods=['PUT'])
@login_required
def update_bungalow(bungalow_id):
    # Get data from request
    city = request.form.get('city')
    location = request.form.get('location')
    address = request.form.get('address')
    status = request.form.get('status')
    price = request.form.get('price')
    description = request.form.get('description')

    # Optionally handle image files if they are being updated
    image1 = request.files.get('image1')
    image2 = request.files.get('image2')
    image3 = request.files.get('image3')

    # Save images if provided
    if image1:
        image1_filename = image1.filename
        image1.save(f'static/images/{image1_filename}')
    if image2:
        image2_filename = image2.filename
        image2.save(f'static/images/{image2_filename}')
    if image3:
        image3_filename = image3.filename
        image3.save(f'static/images/{image3_filename}')

    # Update data in the flats table
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE bungalows 
        SET city = ?, location = ?, full_address = ?, status = ?, price = ?, image1 = ?, image2 = ?, image3 = ?, description = ? 
        WHERE id = ?
    """, (city, location, address, status, price, 
          image1_filename if image1 else None, 
          image2_filename if image2 else None, 
          image3_filename if image3 else None, 
          description, bungalow_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Bungalow updated successfully!'})


@register_bp.route('/owner/flats/<int:flat_id>', methods=['DELETE'])
@login_required
def delete_flat(flat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flats WHERE id = ?", (flat_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Flat deleted successfully!'})

@register_bp.route('/owner/bungalows/<int:bungalow_id>', methods=['DELETE'])
@login_required
def delete_bungalow(bungalow_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bungalows WHERE id = ?", (bungalow_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Bungalow deleted successfully!'})


@register_bp.route('/logout')
def logout():
    session.pop('name', None)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT city, location FROM flats
        UNION
        SELECT DISTINCT city, location FROM bungalows
    """)
    flats_and_bungalows = cursor.fetchall()

    return render_template('/public/add_space.html', flats_filter=flats_and_bungalows)

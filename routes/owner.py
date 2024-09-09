from flask import Blueprint, request, redirect, url_for, render_template, session, flash, jsonify
import sqlite3

register_bp = Blueprint('register_bp', __name__)

def connect_db():
    return sqlite3.connect('house.db')

@register_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        session['name'] = request.form['name']
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

@register_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form['username']
        session['password'] = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM owner WHERE name = ? AND password = ?", (session['name'], session['password']))
        existing_user = cursor.fetchone()

        conn.commit()
        conn.close()

        if existing_user:
            return render_template('/owner/base.html')

@register_bp.route('/profile')
def profile():
    conn = connect_db()
    cursor = conn.cursor()
    existing_user = cursor.execute("SELECT * FROM owner WHERE name = ? AND password = ?", (session['name'], session['password'])).fetchall()
    print(existing_user)
    conn.close()
    return render_template('/owner/profile.html',existing_user=existing_user)

@register_bp.route('/flats', methods=['GET', 'POST'])
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
            "INSERT INTO flats (city, location, full_address, status, price, image1, image2, image3, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (city, location, address, status, price, image1_filename, image2_filename, image3_filename, description)
        )
        conn.commit()
        conn.close()

        flash('Flat added successfully!')
        return redirect(url_for('register_bp.flats'))

    # Handling GET request: retrieve flats data from the database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flats")
    flats_data = cursor.fetchall()
    conn.close()

    # Pass flats data to the template, or a message if no data exists
    if flats_data:
        return render_template('/owner/flats.html', flats=flats_data)
    else:
        flash('No flats added.')
        return render_template('/owner/flats.html', flats=None)

@register_bp.route('/flats/<int:flat_id>', methods=['PUT'])
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

@register_bp.route('/flats/<int:flat_id>', methods=['DELETE'])
def delete_flat(flat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flats WHERE id = ?", (flat_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Flat deleted successfully!'})

@register_bp.route('/bungalows')
def bungalows():
    return render_template('/owner/bungalows.html')

@register_bp.route('/logout')
def logout():
    session.pop('name', None)
    return render_template('/public/add_space.html')

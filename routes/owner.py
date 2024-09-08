from flask import Blueprint, request, redirect, url_for, render_template, session
import sqlite3,os,base64

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

@register_bp.route('/flats')
def flats():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flats')
    flat_rows = cursor.fetchall()
    conn.close()
    print(f'Flats:{flat_rows}')
    return render_template('/owner/flats.html', flats=flat_rows)


def save_file(file, folder):
    if file:
        filename = file.filename
        file_path = os.path.join(folder, filename)
        file.save(file_path)
        return filename
    return None

@register_bp.route('/flats/add', methods=['POST'])
def add_flat():
    conn = connect_db()
    cursor = conn.cursor()

    city = request.form['city']
    location = request.form['location']
    fulladdress = request.form['fulladdress']
    status = request.form['status']
    price = request.form['price']
    video_file = request.files.get('video')
    image1_file = request.files.get('image1')
    image2_file = request.files.get('image2')
    image3_file = request.files.get('image3')
    description = request.form['description']

    # Define upload folders
    video_folder = 'static/videos/'
    image_folder = 'static/images/'

    # Save files
    video_filename = save_file(video_file, video_folder)
    image1_filename = save_file(image1_file, image_folder)
    image2_filename = save_file(image2_file, image_folder)
    image3_filename = save_file(image3_file, image_folder)

    # Insert into database
    cursor.execute('''
        INSERT INTO flats (city, location, full_address, status, price, video, image1, image2, image3, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, location, fulladdress, status, price, video_filename, image1_filename, image2_filename, image3_filename, description))

    conn.commit()
    conn.close()

    return redirect(url_for('register_bp.flats'))

@register_bp.route('/flats/edit', methods=['POST'])
def edit_flat():
    conn = connect_db()
    cursor = conn.cursor()

    city = request.form['city']
    location = request.form['location']
    fulladdress = request.form['fulladdress']
    status = request.form['status']
    price = request.form['price']
    video_file = request.files.get('video')
    image1_file = request.files.get('image1')
    image2_file = request.files.get('image2')
    image3_file = request.files.get('image3')
    description = request.form['description']

    # Define upload folders
    video_folder = 'static/videos/'
    image_folder = 'static/images/'

    # Save files
    video_filename = save_file(video_file, video_folder)
    image1_filename = save_file(image1_file, image_folder)
    image2_filename = save_file(image2_file, image_folder)
    image3_filename = save_file(image3_file, image_folder)

    # Insert into database
    cursor.execute('''
        INSERT INTO flats (city, location, full_address, status, price, video, image1, image2, image3, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, location, fulladdress, status, price, video_filename, image1_filename, image2_filename, image3_filename, description))

    conn.commit()
    conn.close()

    return redirect(url_for('register_bp.flats'))


@register_bp.route('/bungalows')
def bungalows():
    return render_template('/owner/bungalows.html')

@register_bp.route('/logout')
def logout():
    session.pop('name', None)
    return render_template('/public/add_space.html')

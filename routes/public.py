from flask import Blueprint, request, render_template

register_public_bp = Blueprint('register_public_bp', __name__)

@register_public_bp.route('/')
def home():
    return render_template('/public/base.html')

@register_public_bp.route('/find-space')
def find_space():
    return render_template('/public/find_space.html')

@register_public_bp.route('/add-space')
def add_space():
    return render_template('/public/add_space.html')

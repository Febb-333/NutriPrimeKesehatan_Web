from flask import Blueprint, render_template
from database import execute_query

# Blueprint untuk landing page (tanpa url_prefix, jadi endpoint di '/')
home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """
    Menampilkan landing page berisi:
    hero, about, CTA hitung BMI, dan preview 4 makanan terbaru.
    """
    query = """
        SELECT id, name, calories, protein, category, image
        FROM foods
        ORDER BY created_at DESC
        LIMIT 4
    """
    foods = execute_query(query, fetch=True)

    return render_template('home/index.html', foods=foods)

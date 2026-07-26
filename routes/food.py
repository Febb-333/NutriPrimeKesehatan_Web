from flask import Blueprint, render_template, request, abort
from database import execute_query

# url_prefix='/makanan' + route('') -> endpoint akhir jadi '/makanan'
food_bp = Blueprint('food', __name__, url_prefix='/makanan')


@food_bp.route('')
def index():
    """
    Menampilkan daftar semua makanan.
    Mendukung pencarian nama (?q=...) dan filter kategori (?kategori=...)
    lewat query string, sehingga hasil bisa langsung dibagikan via URL.
    """
    keyword = request.args.get('q', '').strip()
    category = request.args.get('kategori', '').strip()

    # Query dibangun bertahap, tapi seluruh nilai dinamis tetap lewat
    # placeholder %s (prepared statement) -> aman dari SQL Injection.
    query = "SELECT id, name, calories, protein, fat, carbs, category FROM foods WHERE 1=1"
    params = []

    if keyword:
        query += " AND name LIKE %s"
        params.append(f"%{keyword}%")

    if category:
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY name ASC"

    foods = execute_query(query, tuple(params), fetch=True)

    # Ambil daftar kategori unik untuk mengisi dropdown filter
    categories = execute_query(
        "SELECT DISTINCT category FROM foods ORDER BY category ASC",
        fetch=True
    )

    return render_template(
        'food/list.html',
        foods=foods,
        categories=categories,
        keyword=keyword,
        selected_category=category
    )


@food_bp.route('/<int:food_id>')
def detail(food_id):
    """Menampilkan detail nutrisi lengkap satu makanan berdasarkan id."""
    query = "SELECT * FROM foods WHERE id = %s"
    food = execute_query(query, (food_id,), fetch_one=True)

    if not food:
        abort(404)

    return render_template('food/detail.html', food=food)

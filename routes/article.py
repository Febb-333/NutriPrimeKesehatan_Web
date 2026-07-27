from flask import Blueprint, render_template, abort
from database import execute_query

article_bp = Blueprint('article', __name__, url_prefix='/artikel')


@article_bp.route('')
def index():
    """Menampilkan daftar seluruh artikel kesehatan, terbaru di atas."""
    query = """
        SELECT id, title, slug, thumbnail, created_at
        FROM articles
        ORDER BY created_at DESC
    """
    articles = execute_query(query, fetch=True)
    return render_template('article/list.html', articles=articles)


@article_bp.route('/<slug>')
def detail(slug):
    """Menampilkan detail satu artikel berdasarkan slug."""
    query = "SELECT * FROM articles WHERE slug = %s"
    article = execute_query(query, (slug,), fetch_one=True)

    if not article:
        abort(404)

    return render_template('article/detail.html', article=article)
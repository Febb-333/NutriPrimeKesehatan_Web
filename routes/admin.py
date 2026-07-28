import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from database import execute_query

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view_func):
    """Decorator: tolak akses ke route admin kalau belum login."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Silakan login terlebih dahulu.', 'error')
            return redirect(url_for('admin.login'))
        return view_func(*args, **kwargs)
    return wrapped


def slugify(title):
    """Ubah judul artikel jadi slug URL-friendly, contoh: 'Tips Sehat!' -> 'tips-sehat'."""
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
    return slug


def generate_unique_slug(title, exclude_id=None):
    """Buat slug dari judul, tambahkan angka di belakang kalau sudah ada yang sama."""
    base_slug = slugify(title)
    slug = base_slug
    counter = 2

    while True:
        query = "SELECT id FROM articles WHERE slug = %s"
        params = [slug]
        if exclude_id:
            query += " AND id != %s"
            params.append(exclude_id)

        existing = execute_query(query, tuple(params), fetch_one=True)
        if not existing:
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1


def parse_food_form(form):
    """Ambil & validasi data form makanan (dipakai bareng oleh tambah & edit)."""
    errors = []
    data = {
        'name': form.get('name', '').strip(),
        'category': form.get('category', '').strip(),
        'description': form.get('description', '').strip(),
    }

    for field, label in [('calories', 'Kalori'), ('protein', 'Protein'),
                          ('fat', 'Lemak'), ('carbs', 'Karbohidrat')]:
        raw = form.get(field, '')
        try:
            value = float(raw)
            if value < 0:
                errors.append(f'{label} tidak boleh negatif.')
        except (TypeError, ValueError):
            errors.append(f'{label} harus berupa angka.')
            value = 0
        data[field] = value

    if not data['name']:
        errors.append('Nama makanan wajib diisi.')
    if not data['category']:
        errors.append('Kategori wajib diisi.')

    return data, errors


# ================= AUTH =================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        query = "SELECT id, username, password FROM users WHERE username = %s"
        user = execute_query(query, (username,), fetch_one=True)

        if user and check_password_hash(user['password'], password):
            session['admin_id'] = user['id']
            session['admin_username'] = user['username']
            flash(f"Selamat datang kembali, {user['username']}!", 'success')
            return redirect(url_for('admin.dashboard'))

        flash('Username atau password salah.', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout.', 'success')
    return redirect(url_for('admin.login'))


# ================= DASHBOARD =================

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'foods': execute_query("SELECT COUNT(*) AS total FROM foods", fetch_one=True)['total'],
        'articles': execute_query("SELECT COUNT(*) AS total FROM articles", fetch_one=True)['total'],
        'bmi_history': execute_query("SELECT COUNT(*) AS total FROM bmi_history", fetch_one=True)['total'],
        'contacts': execute_query("SELECT COUNT(*) AS total FROM contacts", fetch_one=True)['total'],
    }
    return render_template('admin/dashboard.html', stats=stats)


# ================= CRUD MAKANAN =================

@admin_bp.route('/makanan')
@login_required
def food_list():
    foods = execute_query("SELECT * FROM foods ORDER BY name ASC", fetch=True)
    return render_template('admin/food_list.html', foods=foods)


@admin_bp.route('/makanan/tambah', methods=['GET', 'POST'])
@login_required
def food_add():
    if request.method == 'POST':
        data, errors = parse_food_form(request.form)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/food_form.html', food=data, mode='tambah')

        query = """
            INSERT INTO foods (name, calories, protein, fat, carbs, category, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (
            data['name'], data['calories'], data['protein'],
            data['fat'], data['carbs'], data['category'], data['description']
        ), commit=True)

        flash('Makanan berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.food_list'))

    return render_template('admin/food_form.html', food=None, mode='tambah')


@admin_bp.route('/makanan/edit/<int:food_id>', methods=['GET', 'POST'])
@login_required
def food_edit(food_id):
    food = execute_query("SELECT * FROM foods WHERE id = %s", (food_id,), fetch_one=True)
    if not food:
        flash('Data makanan tidak ditemukan.', 'error')
        return redirect(url_for('admin.food_list'))

    if request.method == 'POST':
        data, errors = parse_food_form(request.form)
        if errors:
            for error in errors:
                flash(error, 'error')
            data['id'] = food_id
            return render_template('admin/food_form.html', food=data, mode='edit')

        query = """
            UPDATE foods SET name=%s, calories=%s, protein=%s, fat=%s,
                              carbs=%s, category=%s, description=%s
            WHERE id=%s
        """
        execute_query(query, (
            data['name'], data['calories'], data['protein'],
            data['fat'], data['carbs'], data['category'], data['description'], food_id
        ), commit=True)

        flash('Makanan berhasil diperbarui.', 'success')
        return redirect(url_for('admin.food_list'))

    return render_template('admin/food_form.html', food=food, mode='edit')


@admin_bp.route('/makanan/hapus/<int:food_id>', methods=['POST'])
@login_required
def food_delete(food_id):
    execute_query("DELETE FROM foods WHERE id = %s", (food_id,), commit=True)
    flash('Makanan berhasil dihapus.', 'success')
    return redirect(url_for('admin.food_list'))


# ================= CRUD ARTIKEL =================

@admin_bp.route('/artikel')
@login_required
def article_list():
    articles = execute_query("SELECT * FROM articles ORDER BY created_at DESC", fetch=True)
    return render_template('admin/article_list.html', articles=articles)


@admin_bp.route('/artikel/tambah', methods=['GET', 'POST'])
@login_required
def article_add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        errors = []
        if not title:
            errors.append('Judul wajib diisi.')
        if not content:
            errors.append('Konten wajib diisi.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/article_form.html',
                                    article={'title': title, 'content': content}, mode='tambah')

        slug = generate_unique_slug(title)
        query = "INSERT INTO articles (title, slug, content) VALUES (%s, %s, %s)"
        execute_query(query, (title, slug, content), commit=True)

        flash('Artikel berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.article_list'))

    return render_template('admin/article_form.html', article=None, mode='tambah')


@admin_bp.route('/artikel/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def article_edit(article_id):
    article = execute_query("SELECT * FROM articles WHERE id = %s", (article_id,), fetch_one=True)
    if not article:
        flash('Artikel tidak ditemukan.', 'error')
        return redirect(url_for('admin.article_list'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        errors = []
        if not title:
            errors.append('Judul wajib diisi.')
        if not content:
            errors.append('Konten wajib diisi.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/article_form.html',
                                    article={'id': article_id, 'title': title, 'content': content},
                                    mode='edit')

        # Slug hanya dibuat ulang kalau judul berubah, supaya link lama tidak rusak sia-sia
        slug = article['slug']
        if title != article['title']:
            slug = generate_unique_slug(title, exclude_id=article_id)

        query = "UPDATE articles SET title=%s, slug=%s, content=%s WHERE id=%s"
        execute_query(query, (title, slug, content, article_id), commit=True)

        flash('Artikel berhasil diperbarui.', 'success')
        return redirect(url_for('admin.article_list'))

    return render_template('admin/article_form.html', article=article, mode='edit')


@admin_bp.route('/artikel/hapus/<int:article_id>', methods=['POST'])
@login_required
def article_delete(article_id):
    execute_query("DELETE FROM articles WHERE id = %s", (article_id,), commit=True)
    flash('Artikel berhasil dihapus.', 'success')
    return redirect(url_for('admin.article_list'))
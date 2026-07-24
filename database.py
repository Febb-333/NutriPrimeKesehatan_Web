import mysql.connector
from mysql.connector import Error
from flask import current_app, g

# ==================================================================
# database.py
# Seluruh koneksi & query database (SQL Native) terpusat di file ini
# sesuai ketentuan project: tidak menggunakan SQLAlchemy / ORM lain.
# ==================================================================


def get_db():
    """
    Membuka koneksi database baru hanya jika belum ada koneksi
    pada request saat ini (disimpan di Flask 'g').
    Tujuannya agar 1 request hanya membuka 1 koneksi (efisien).
    """
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_NAME'],
                port=current_app.config['DB_PORT']
            )
        except Error as e:
            print(f"[DATABASE ERROR] Gagal konek ke database: {e}")
            raise
    return g.db


def close_db(e=None):
    """Menutup koneksi database otomatis setiap request selesai."""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


def execute_query(query, params=None, fetch=False, fetch_one=False, commit=False):
    """
    Helper generik untuk semua query SQL Native dengan prepared statement (%s).

    Parameter:
        query     : string SQL, gunakan %s sebagai placeholder
        params    : tuple/list nilai untuk placeholder (mencegah SQL Injection)
        fetch     : True -> kembalikan semua baris (list of dict)
        fetch_one : True -> kembalikan satu baris (dict) atau None
        commit    : True -> untuk INSERT/UPDATE/DELETE, commit + return lastrowid

    Cursor selalu dibuka dengan dictionary=True agar hasil query
    berupa dict (mis. row['name']) bukan tuple, sesuai ketentuan project.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())

        if commit:
            db.commit()
            result = cursor.lastrowid
        elif fetch_one:
            result = cursor.fetchone()
        elif fetch:
            result = cursor.fetchall()
        else:
            result = None

        return result
    except Error as e:
        db.rollback()
        print(f"[QUERY ERROR] {e}")
        raise
    finally:
        cursor.close()


def init_app(app):
    """Didaftarkan di app.py agar close_db() otomatis jalan tiap request selesai."""
    app.teardown_appcontext(close_db)

from flask import Flask, render_template
from config import Config
import database
from routes.home import home_bp
from routes.bmi import bmi_bp
from routes.bmr import bmr_bp
from routes.food import food_bp
from routes.article import article_bp
from routes.contact import contact_bp
from routes.admin import admin_bp

INDO_MONTHS = [
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]


def format_tanggal_indo(value):
    """Jinja filter: format datetime jadi '27 Juli 2026' (bukan 'July' berbahasa Inggris)."""
    if not value:
        return ''
    return f"{value.day} {INDO_MONTHS[value.month - 1]} {value.year}"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    database.init_app(app)

    app.jinja_env.filters['tanggal_indo'] = format_tanggal_indo

    app.register_blueprint(home_bp)
    app.register_blueprint(bmi_bp)
    app.register_blueprint(bmr_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
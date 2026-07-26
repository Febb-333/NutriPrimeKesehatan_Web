from flask import Flask, render_template
from config import Config
import database
from routes.home import home_bp
from routes.bmi import bmi_bp
from routes.bmr import bmr_bp
from routes.food import food_bp

# Blueprint fitur lain (article, admin, contact)
# akan di-import & di-register di sini secara bertahap pada tahap berikutnya.


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Daftarkan teardown supaya koneksi DB otomatis ditutup tiap request selesai
    database.init_app(app)

    # Registrasi blueprint
    app.register_blueprint(home_bp)
    app.register_blueprint(bmi_bp)
    app.register_blueprint(bmr_bp)
    app.register_blueprint(food_bp)

    # Halaman 404 kustom, dipakai saat detail makanan/artikel tidak ditemukan
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

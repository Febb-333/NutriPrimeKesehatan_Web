from flask import Flask
from config import Config
import database
from routes.home import home_bp

# Blueprint fitur lain (bmi, bmr, food, article, admin, contact)
# akan di-import & di-register di sini secara bertahap pada tahap berikutnya.


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Daftarkan teardown supaya koneksi DB otomatis ditutup tiap request selesai
    database.init_app(app)

    # Registrasi blueprint
    app.register_blueprint(home_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

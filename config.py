import os
from dotenv import load_dotenv

# Load variabel dari file .env (jika ada) ke environment
load_dotenv()


class Config:
    """
    Konfigurasi aplikasi NutriPrimeKesehatan.
    Semua nilai sensitif diambil dari environment variable (.env),
    dengan nilai default untuk kebutuhan development lokal.
    """

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-ubah-saat-production')

    # Kredensial database MariaDB/MySQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'nutriprimekesehatan')
    DB_PORT = int(os.getenv('DB_PORT', 3306))

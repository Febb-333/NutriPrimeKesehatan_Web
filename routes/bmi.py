from flask import Blueprint, render_template, request, flash
from database import execute_query

# url_prefix='/bmi' + route('') -> endpoint akhir jadi '/bmi' (tanpa trailing slash)
bmi_bp = Blueprint('bmi', __name__, url_prefix='/bmi')


# Daftar kategori BMI standar WHO, diurutkan dari batas atas terkecil.
# Setiap kategori punya penjelasan & rekomendasi kesehatan sendiri.
BMI_CATEGORIES = [
    {
        'max': 18.5,
        'label': 'Kurus',
        'explanation': 'Berat badan Anda berada di bawah rentang normal berdasarkan tinggi badan Anda.',
        'recommendation': 'Konsultasikan pola makan dengan ahli gizi, perbanyak asupan kalori sehat dari sumber protein, karbohidrat kompleks, dan lemak baik secara bertahap.'
    },
    {
        'max': 25.0,
        'label': 'Normal',
        'explanation': 'Selamat, berat badan Anda berada dalam rentang ideal berdasarkan tinggi badan Anda.',
        'recommendation': 'Pertahankan pola makan seimbang dan aktivitas fisik rutin minimal 150 menit per minggu untuk menjaga kondisi ini.'
    },
    {
        'max': 30.0,
        'label': 'Kelebihan Berat Badan',
        'explanation': 'Berat badan Anda sedikit di atas rentang normal berdasarkan tinggi badan Anda.',
        'recommendation': 'Kurangi konsumsi makanan tinggi kalori dan gula, perbanyak sayur dan buah, serta tingkatkan aktivitas fisik secara bertahap.'
    },
    {
        'max': float('inf'),
        'label': 'Obesitas',
        'explanation': 'Berat badan Anda jauh di atas rentang normal, berisiko terhadap berbagai penyakit tidak menular.',
        'recommendation': 'Disarankan berkonsultasi dengan dokter atau ahli gizi untuk menyusun program penurunan berat badan yang aman dan terarah.'
    },
]


def get_bmi_category(bmi_value):
    """Menentukan kategori BMI berdasarkan nilai BMI yang sudah dihitung."""
    for category in BMI_CATEGORIES:
        if bmi_value < category['max']:
            return category
    return BMI_CATEGORIES[-1]


def validate_input(name, height_raw, weight_raw):
    """
    Validasi input sederhana sesuai ketentuan project.
    Return: (list_error, height_float_or_None, weight_float_or_None)
    """
    errors = []

    if not name or not name.strip():
        errors.append('Nama wajib diisi.')

    try:
        height = float(height_raw)
        if height < 50 or height > 300:
            errors.append('Tinggi badan harus di antara 50 - 300 cm.')
    except (TypeError, ValueError):
        errors.append('Tinggi badan harus berupa angka.')
        height = None

    try:
        weight = float(weight_raw)
        if weight < 10 or weight > 300:
            errors.append('Berat badan harus di antara 10 - 300 kg.')
    except (TypeError, ValueError):
        errors.append('Berat badan harus berupa angka.')
        weight = None

    return errors, height, weight


@bmi_bp.route('', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {}

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        height_raw = request.form.get('height', '')
        weight_raw = request.form.get('weight', '')
        form_data = {'name': name, 'height': height_raw, 'weight': weight_raw}

        errors, height, weight = validate_input(name, height_raw, weight_raw)

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # Rumus BMI = berat(kg) / tinggi(m)^2
            height_m = height / 100
            bmi_value = round(weight / (height_m ** 2), 1)
            category = get_bmi_category(bmi_value)

            # Simpan riwayat perhitungan ke database (SQL Native, prepared statement)
            query = """
                INSERT INTO bmi_history (name, height, weight, bmi_value, category)
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(
                query,
                (name, height, weight, bmi_value, category['label']),
                commit=True
            )

            flash('Hasil perhitungan BMI berhasil disimpan.', 'success')

            result = {
                'name': name,
                'height': height,
                'weight': weight,
                'bmi_value': bmi_value,
                'category': category['label'],
                'explanation': category['explanation'],
                'recommendation': category['recommendation'],
            }

    return render_template('bmi/index.html', result=result, form_data=form_data)

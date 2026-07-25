from flask import Blueprint, render_template, request, flash

# url_prefix='/bmr' + route('') -> endpoint akhir jadi '/bmr' (tanpa trailing slash)
bmr_bp = Blueprint('bmr', __name__, url_prefix='/bmr')


# Faktor aktivitas fisik standar, dipakai untuk TDEE = BMR x faktor.
# Key disimpan sebagai value <select> di form, label untuk ditampilkan ke user.
ACTIVITY_LEVELS = {
    'sedentary': {
        'label': 'Sangat Jarang Olahraga',
        'factor': 1.2,
    },
    'light': {
        'label': 'Ringan (1-3 hari/minggu)',
        'factor': 1.375,
    },
    'moderate': {
        'label': 'Sedang (3-5 hari/minggu)',
        'factor': 1.55,
    },
    'active': {
        'label': 'Berat (6-7 hari/minggu)',
        'factor': 1.725,
    },
    'very_active': {
        'label': 'Sangat Berat (2x sehari / kerja fisik)',
        'factor': 1.9,
    },
}

# Defisit/surplus kalori standar untuk target cutting & bulking
CALORIE_ADJUSTMENT = 500


def calculate_bmr(gender, weight, height, age):
    """
    Hitung BMR (Basal Metabolic Rate) pakai rumus Mifflin-St Jeor,
    lebih akurat dibanding rumus Harris-Benedict lama.
    """
    base = (10 * weight) + (6.25 * height) - (5 * age)
    if gender == 'male':
        return base + 5
    return base - 161


def validate_input(age_raw, gender, height_raw, weight_raw, activity):
    """Validasi input sederhana untuk form BMR/TDEE."""
    errors = []

    try:
        age = int(age_raw)
        if age < 10 or age > 100:
            errors.append('Umur harus di antara 10 - 100 tahun.')
    except (TypeError, ValueError):
        errors.append('Umur harus berupa angka.')
        age = None

    if gender not in ('male', 'female'):
        errors.append('Gender wajib dipilih.')

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

    if activity not in ACTIVITY_LEVELS:
        errors.append('Tingkat aktivitas wajib dipilih.')

    return errors, age, height, weight


@bmr_bp.route('', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {}

    if request.method == 'POST':
        age_raw = request.form.get('age', '')
        gender = request.form.get('gender', '')
        height_raw = request.form.get('height', '')
        weight_raw = request.form.get('weight', '')
        activity = request.form.get('activity', '')

        form_data = {
            'age': age_raw,
            'gender': gender,
            'height': height_raw,
            'weight': weight_raw,
            'activity': activity,
        }

        errors, age, height, weight = validate_input(
            age_raw, gender, height_raw, weight_raw, activity
        )

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            bmr_value = round(calculate_bmr(gender, weight, height, age))
            activity_info = ACTIVITY_LEVELS[activity]
            tdee_value = round(bmr_value * activity_info['factor'])

            calorie_maintain = tdee_value
            # Cutting tidak boleh di bawah BMR (batas aman metabolisme)
            calorie_cutting = max(tdee_value - CALORIE_ADJUSTMENT, bmr_value)
            calorie_bulking = tdee_value + CALORIE_ADJUSTMENT

            result = {
                'bmr': bmr_value,
                'tdee': tdee_value,
                'maintain': calorie_maintain,
                'cutting': calorie_cutting,
                'bulking': calorie_bulking,
                'activity_label': activity_info['label'],
            }

    return render_template(
        'bmr/index.html',
        result=result,
        form_data=form_data,
        activity_levels=ACTIVITY_LEVELS
    )

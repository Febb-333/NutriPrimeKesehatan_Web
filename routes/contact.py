from flask import Blueprint, render_template, request, flash
from database import execute_query

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')


def validate_input(name, email, subject, message):
    """Validasi input sederhana untuk form kontak."""
    errors = []
    if not name or not name.strip():
        errors.append('Nama wajib diisi.')
    if not email or '@' not in email:
        errors.append('Email tidak valid.')
    if not subject or not subject.strip():
        errors.append('Subjek wajib diisi.')
    if not message or not message.strip():
        errors.append('Pesan wajib diisi.')
    return errors


@contact_bp.route('', methods=['GET', 'POST'])
def index():
    form_data = {}

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        form_data = {'name': name, 'email': email, 'subject': subject, 'message': message}

        errors = validate_input(name, email, subject, message)

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            query = """
                INSERT INTO contacts (name, email, subject, message)
                VALUES (%s, %s, %s, %s)
            """
            execute_query(query, (name, email, subject, message), commit=True)
            flash('Pesan Anda berhasil terkirim. Terima kasih telah menghubungi kami!', 'success')
            form_data = {}  # reset form setelah sukses

    return render_template('contact/index.html', form_data=form_data)
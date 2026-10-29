import logging
import os

from flask import request, render_template, flash, redirect, url_for
from . import app
from .forms import ContactForm, SUBJECT_CHOICES

LOG_DIR = os.path.join(os.path.dirname(app.root_path), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

contact_logger = logging.getLogger("contact")
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    _handler = logging.FileHandler(os.path.join(LOG_DIR, "contact.log"), encoding="utf-8")
    _handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    contact_logger.addHandler(_handler)
    contact_logger.propagate = False


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        subject_label = dict(SUBJECT_CHOICES).get(form.subject.data, form.subject.data)
        message_text = form.message.data.replace("\r", "").replace("\n", " \\n ")
        try:
            contact_logger.info(
                "name=%r | email=%r | phone=%r | subject=%r | message=%r | ip=%s",
                form.name.data,
                form.email.data,
                form.phone.data or "",
                subject_label,
                message_text,
                request.remote_addr,
            )
        except OSError:
            app.logger.exception("Не вдалося записати контактну форму в лог")
            flash("Не вдалося зберегти повідомлення. Спробуйте пізніше.", "danger")
            return redirect(url_for('contact'))

        flash(f"Дякуємо, {form.name.data}! Ваше повідомлення надіслано й збережено.", "success")
        return redirect(url_for('contact'))

    if request.method == 'POST':
        flash("Форму не відправлено: виправте помилки у полях.", "danger")

    return render_template('contact.html', form=form, title="Contacts")


@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', agent=agent, title="Homepage")
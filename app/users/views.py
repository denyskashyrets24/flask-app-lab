from flask import render_template, request, redirect, url_for, flash, session
from . import users_bp

FAKE_USERS = {
    "admin": "admin123",
    "student": "qwerty",
}

COOKIE_PATH = "/"
SESSION_COOKIE_NAME = "session"
THEME_COOKIE_NAME = "theme"
RESERVED_COOKIES = {SESSION_COOKIE_NAME, THEME_COOKIE_NAME}

THEMES = {
    "light": "Світла",
    "dark": "Темна",
    "green": "Зелена",
}
DEFAULT_THEME = "light"
THEME_MAX_AGE = 60 * 60 * 24 * 365

DEFAULT_COOKIE_MAX_AGE = 3600


def _require_login():
    if not session.get("username"):
        flash("Сесія недоступна. Будь ласка, увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))
    return None


def _current_theme():
    theme = request.cookies.get(THEME_COOKIE_NAME, DEFAULT_THEME)
    return theme if theme in THEMES else DEFAULT_THEME


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in FAKE_USERS and FAKE_USERS[username] == password:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Невірний логін або пароль.", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@users_bp.route("/profile")
def profile():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    cookies = {k: v for k, v in request.cookies.items() if k not in RESERVED_COOKIES}
    theme = _current_theme()
    return render_template(
        "users/profile.html",
        username=session["username"],
        cookies=cookies,
        theme=theme,
        themes=THEMES,
    )


@users_bp.route("/profile/theme", methods=["POST"])
def set_theme():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    theme = request.form.get("theme", "")
    if theme not in THEMES:
        flash("Невідома колірна схема.", "danger")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.set_cookie(THEME_COOKIE_NAME, theme, max_age=THEME_MAX_AGE, path=COOKIE_PATH)
    flash(f"Колірну схему змінено на «{THEMES[theme]}».", "success")
    return response


@users_bp.route("/profile/cookies/add", methods=["POST"])
def cookie_add():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    max_age_raw = request.form.get("max_age", "").strip()

    if not key or not value or key in RESERVED_COOKIES:
        flash("Ключ і значення є обов'язковими. Ключі «session» і «theme» зарезервовано.", "danger")
        return redirect(url_for("users.profile"))

    try:
        max_age = int(max_age_raw) if max_age_raw else DEFAULT_COOKIE_MAX_AGE
        if max_age <= 0:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути додатним цілим числом (у секундах).", "danger")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.set_cookie(key, value, max_age=max_age, path=COOKIE_PATH)
    flash(f"Кукі «{key}» додано (термін дії: {max_age} с).", "success")
    return response


@users_bp.route("/profile/cookies/delete", methods=["POST"])
def cookie_delete():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    key = request.form.get("key", "").strip()

    if not key or key in RESERVED_COOKIES:
        flash("Вкажіть ключ кукі для видалення (не «session» і не «theme»).", "danger")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    if key in request.cookies:
        response.delete_cookie(key, path=COOKIE_PATH)
        flash(f"Кукі «{key}» видалено.", "success")
    else:
        flash(f"Кукі «{key}» не знайдено.", "warning")
    return response


@users_bp.route("/profile/cookies/delete-all", methods=["POST"])
def cookies_delete_all():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    response = redirect(url_for("users.profile"))
    deleted = 0
    for key in request.cookies:
        if key in RESERVED_COOKIES:
            continue
        response.delete_cookie(key, path=COOKIE_PATH)
        deleted += 1

    if deleted:
        flash(f"Видалено кукі: {deleted}.", "success")
    else:
        flash("Немає кукі для видалення.", "info")
    return response


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))
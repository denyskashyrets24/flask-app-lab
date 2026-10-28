from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import users_bp

FAKE_USERS = {
    "admin": "admin123",
    "student": "qwerty",
}

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
    username = session.get("username")
    if not username:
        flash("Сесія недоступна. Будь ласка, увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    return render_template("users/profile.html", username=username)


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))
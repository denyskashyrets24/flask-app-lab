import os
import uuid
from datetime import datetime

from flask import render_template, redirect, url_for, flash
from . import products_bp, db
from .forms import ProductForm


def save_image(file):
    ext = file.filename.rsplit(".", 1)[-1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    folder = os.path.join(products_bp.static_folder, "uploads")
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, name))
    return f"uploads/{name}"


def remove_image(path):
    if path:
        full = os.path.join(products_bp.static_folder, path)
        if os.path.exists(full):
            os.remove(full)


def not_found():
    flash("Товар не знайдено.", "warning")
    return redirect(url_for("products.list_products"))


@products_bp.route("/")
def list_products():
    return render_template("products/products.html", products=db.all_products(), title="Товари")


@products_bp.route("/<int:id>")
def detail_product(id):
    product = db.get_product(id)
    if not product:
        return not_found()
    return render_template("products/detail_product.html", p=product, title=product["name"])


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        pid = db.add_product({
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": save_image(form.image.data) if form.image.data else None,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        flash("Товар додано.", "success")
        return redirect(url_for("products.detail_product", id=pid))
    return render_template("products/form.html", form=form, product=None, title="Додати товар")


@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = db.get_product(id)
    if not product:
        return not_found()

    form = ProductForm(data=dict(product, image=None))
    if form.validate_on_submit():
        changes = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
        }
        if form.image.data:
            remove_image(product["image"])
            changes["image"] = save_image(form.image.data)
        db.update_product(id, changes)
        flash("Товар оновлено.", "success")
        return redirect(url_for("products.detail_product", id=id))
    return render_template("products/form.html", form=form, product=product, title="Редагувати товар")


@products_bp.route("/<int:id>/delete", methods=["POST"])
def delete_product(id):
    product = db.get_product(id)
    if not product:
        return not_found()
    remove_image(product["image"])
    db.delete_product(id)
    flash("Товар видалено.", "success")
    return redirect(url_for("products.list_products"))
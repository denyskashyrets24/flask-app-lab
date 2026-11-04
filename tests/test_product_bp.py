import pytest
from app import app as flask_app

DATA = {
    "name": "Laptop",
    "content": "Good laptop for work",
    "price": "199.99",
    "category": "electronics",
    "quantity": "5",
}


@pytest.fixture
def client(tmp_path):
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        PRODUCTS_DB=str(tmp_path / "products.json"),
    )
    return flask_app.test_client()


def page(client, url):
    return client.get(url).get_data(as_text=True)


def test_create(client):
    r = client.post("/product/add", data=DATA)
    assert r.status_code == 302
    assert "Laptop" in page(client, "/product/1")


def test_create_invalid(client):
    r = client.post("/product/add", data={**DATA, "name": "ab", "price": "-5"})
    assert r.status_code == 200
    assert "Laptop" not in page(client, "/product/")


def test_list(client):
    client.post("/product/add", data=DATA)
    assert "Laptop" in page(client, "/product/")


def test_detail_not_found(client):
    r = client.get("/product/99", follow_redirects=True)
    assert "не знайдено" in r.get_data(as_text=True)


def test_edit(client):
    client.post("/product/add", data=DATA)
    r = client.post("/product/1/edit", data={**DATA, "name": "Phone"})
    assert r.status_code == 302
    body = page(client, "/product/1")
    assert "Phone" in body and "Laptop" not in body


def test_delete(client):
    client.post("/product/add", data=DATA)
    assert client.post("/product/1/delete").status_code == 302
    assert "Laptop" not in page(client, "/product/")
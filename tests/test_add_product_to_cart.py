import requests
from selene import browser, have, by, be
import allure
from utils.attach import response_attaching


def test_empty_cart_without_added_product():
    with allure.step("Открыть корзину"):
        browser.open('/cart')

    with allure.step("Проверить что корзина пуста по умолчанию"):
        browser.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))


def test_product_added_to_cart_from_catalog():
    with allure.step("Добавить товар в корзину методом POST /addproducttocart/catalog"):
        response = requests.post(f"{browser.config.base_url}/addproducttocart/catalog/51/1/1")
        response_attaching(response)

        assert response.status_code == 200
        assert response.json().get("success") is True
        cookie = response.cookies.get("Nop.customer")

    with allure.step("Открыть корзину"):
        browser.open("/cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.driver.refresh()

    with allure.step("Проверить что товар был добавлен в корзину"):
        browser.element(by.class_name("cart-qty")).should(have.text("(1)"))
        browser.element(".product-name").should(have.text("Music 2"))
        browser.element("input[value='1']").should(be.visible)


def test_product_not_added_to_cart_from_catalog_without_attributes():
    with allure.step("Добавить товар в корзину методом POST /addproducttocart/details"):
        response = requests.post(f"{browser.config.base_url}/addproducttocart/details/72/1")
        response_attaching(response)

        assert response.status_code == 200
        assert response.json().get("success") is False
        cookie = response.cookies.get("Nop.customer")

    with allure.step("Открыть корзину"):
        browser.open("/cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.driver.refresh()

    with allure.step("Проверить что в корзину не добавился товар без выбранных аттрибутов"):
        browser.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))


def test_multiple_products_added_to_cart_from_catalog():
    with allure.step("Добавить несколько товаров в корзину методом POST /addproducttocart/catalog"):
        session = requests.Session()

        response = session.post(f"{browser.config.base_url}/addproducttocart/catalog/51/1/4")
        response_attaching(response)

        assert response.status_code == 200
        assert response.json().get("success") is True

        response = session.post(f"{browser.config.base_url}/addproducttocart/catalog/13/1/3")
        response_attaching(response)

        assert response.status_code == 200
        assert response.json().get("success") is True

        cookie = session.cookies.get("Nop.customer")

    with allure.step("Открыть корзину"):
        browser.open("/cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.driver.refresh()

    with allure.step("Проверить что товары были добавлены в корзину"):
        browser.element(by.class_name("cart-qty")).should(have.text("(7)"))
        browser.all(".product-name").first.should(have.text("Music 2"))
        browser.element("input[value='4']").should(be.visible)

        browser.all(".product-name").second.should(have.text("Computing and Internet"))
        browser.element("input[value='3']").should(be.visible)


def test_product_added_to_cart_from_product_page():
    with allure.step("Добавить товар в корзину методом POST /addproducttocart/details"):
        response = requests.post(f"{browser.config.base_url}/addproducttocart/details/43/1")
        response_attaching(response)

        assert response.status_code == 200
        assert response.json().get("success") is True
        cookie = response.cookies.get("Nop.customer")

    with allure.step("Открыть корзину"):
        browser.open("/cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.driver.refresh()

    with allure.step("Проверить что в корзину добавился товар"):
        browser.element(by.class_name("cart-qty")).should(have.text("(1)"))
        browser.element('.product-name').should(have.text("Smartphone"))
        browser.element("input[value='1']").should(be.visible)

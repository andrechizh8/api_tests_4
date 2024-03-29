import logging
import os
from selene.support.shared import browser
from selene import have
import allure
from allure import step
from dotenv import load_dotenv
from framework.demoqa_with_env import DemoQaWithEnv

load_dotenv()


def test_login(browser_auth):
    browser.open("")

    with allure.step("Check successful login"):
        browser_auth.element(".account").should(have.exact_text("andrechizh.ru@yandex.ru"))


def test_add_product_to_cart(browser_auth,demoshop):
    browser.open("")

    with allure.step("Check successful add to cart"):
        demoshop.add_to_cart()
        browser.element(".ico-cart").click()
        browser.element("[class='product-name']").should(have.text("Laptop"))


def test_delete_product_from_cart(browser_auth, demoshop):
    browser.open("")

    with allure.step("Check successful delete from cart"):
        demoshop.add_to_cart()
        browser.element("[class='ico-cart']").click()
        browser.element("[name='removefromcart']").click()
        browser.element("[name='updatecart']").click()
        browser.element("[class='order-summary-content']").should(have.exact_text("Your Shopping Cart is empty!"))


def test_add_product_to_wishlist(browser_auth, demoshop):
    browser.open("")

    with allure.step("Check successful add to wishlist"):
        demoshop.add_to_wishlist()
        browser.open("wishlist")
        browser.element("[class='product']").should(have.exact_text("3rd Album"))


def test_delete_product_from_wishlist(browser_auth, demoshop):
    browser.open("")

    with allure.step("Check successful delete from wishlist"):
        demoshop.add_to_wishlist()
        browser.element("[class='ico-wishlist']").click()
        browser.element("[name='removefromcart']").click()
        browser.element("[name='updatecart']").click()
        browser.element("[class='wishlist-content']").should(have.exact_text("The wishlist is empty!"))


def test_successful_logout(browser_auth):
    browser.open("")

    with allure.step("Check sucessful logout"):
        browser.element("[class='ico-logout'").click()
        browser.element("[class='ico-register'").should(have.exact_text("Register"))


def test_with_framework(env):
    with step("Authorization"):
        demoqa = DemoQaWithEnv(env)
        demoqa.authorization_cookie = demoqa.login(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))
        logging.info(demoqa.authorization_cookie)

    with step("Add to cart"):
        result = demoqa.add_to_cart(cookie=demoqa.authorization_cookie)

    with step("Check add to cart"):
        assert result.status_code == 200
        assert "The product has been added to your" in result.json()["message"]


def test_delete_product_from_cart_2(browser_auth, demoshop):
    browser.open("")

    with allure.step("Check successful delete from cart"):
        browser.element("[class='ico-cart']").click()
        browser.element("[name='removefromcart']").click()
        browser.element("[name='updatecart']").click()
        browser.element("[class='order-summary-content']").should(have.exact_text("Your Shopping Cart is empty!"))

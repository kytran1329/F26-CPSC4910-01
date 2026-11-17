import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()


@pytest.fixture(scope="module")
def app_url():
    return os.getenv("APP_URL", "http://127.0.0.1:5000").rstrip("/")


@pytest.fixture(scope="module")
def logged_in_driver(app_url):
    username = os.getenv("DRIVER_USER")
    password = os.getenv("DRIVER_PASSWORD")
    if not username or not password:
        pytest.skip(
            "Set DRIVER_USER and DRIVER_PASSWORD to run driver dashboard tests."
        )

    browser = webdriver.Chrome(options=webdriver.ChromeOptions())
    wait = WebDriverWait(browser, 15)

    try:
        browser.get(app_url)
        wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)
        browser.find_element(By.NAME, "password").send_keys(password)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Login']")
            )
        ).click()
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "dashboard-name"), "'s Dashboard"
            )
        )
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def driver_dashboard(logged_in_driver, app_url):
    logged_in_driver.get(f"{app_url}/driverDash")
    WebDriverWait(logged_in_driver, 15).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "dashboard-name"), "'s Dashboard"
        )
    )
    return logged_in_driver


def test_driver_dashboard_view(driver_dashboard):
    dashboard = driver_dashboard

    assert dashboard.find_element(By.CLASS_NAME, "dashboard-name").text.endswith(
        "'s Dashboard"
    )
    assert dashboard.find_element(By.CSS_SELECTOR, ".points-value").is_displayed()
    assert "Driver Information" in dashboard.page_source
    assert "Total Balance" in dashboard.page_source
    assert "Point History" in dashboard.page_source
    assert "Order History" in dashboard.page_source


def test_order_history_tabs_switch_views(driver_dashboard):
    dashboard = driver_dashboard
    orders_view = dashboard.find_element(By.ID, "orders-view")
    items_view = dashboard.find_element(By.ID, "items-view")

    assert orders_view.is_displayed()
    assert not items_view.is_displayed()

    dashboard.find_element(By.ID, "items-tab").click()
    WebDriverWait(dashboard, 10).until(
        EC.visibility_of_element_located((By.ID, "items-view"))
    )
    assert not dashboard.find_element(By.ID, "orders-view").is_displayed()

    dashboard.find_element(By.ID, "orders-tab").click()
    WebDriverWait(dashboard, 10).until(
        EC.visibility_of_element_located((By.ID, "orders-view"))
    )
    assert not dashboard.find_element(By.ID, "items-view").is_displayed()


def test_change_selected_balance(driver_dashboard):
    dashboard = driver_dashboard
    select_element = dashboard.find_element(By.ID, "company_id")
    company_select = Select(select_element)
    company_options = [
        option for option in company_select.options if option.get_attribute("value")
    ]
    if len(company_options) < 2:
        pytest.skip("A second sponsor-company balance is needed to test selection.")

    current_company_id = company_select.first_selected_option.get_attribute("value")
    target_option = next(
        option
        for option in company_options
        if option.get_attribute("value") != current_company_id
    )
    target_company_id = target_option.get_attribute("value")
    target_company_name = target_option.text.strip()

    select_element = dashboard.find_element(By.ID, "company_id")
    Select(select_element).select_by_value(target_company_id)

    wait = WebDriverWait(dashboard, 15)
    wait.until(EC.staleness_of(select_element))
    wait.until(EC.url_contains(f"company_id={target_company_id}"))

    selected = Select(
        wait.until(EC.presence_of_element_located((By.ID, "company_id")))
    )
    assert selected.first_selected_option.get_attribute("value") == target_company_id

    label = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".points-label"))
    )
    assert target_company_name.casefold() in label.text.casefold()
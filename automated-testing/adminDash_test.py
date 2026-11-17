import os
from decimal import Decimal
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()

POINT_TEST_DRIVER = "Annie Smith"


@pytest.fixture(scope="module")
def app_url():
    return os.getenv("APP_URL", "http://127.0.0.1:5000").rstrip("/")


@pytest.fixture(scope="module")
def logged_in_admin(app_url):
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        pytest.skip(
            "Set ADMIN_USER and ADMIN_PASSWORD to run admin dashboard tests."
        )

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=options)
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
                (By.CLASS_NAME, "dashboard-name"), "Admin Dashboard"
            )
        )

        yield browser
    finally:
        browser.quit()


@pytest.fixture
def admin_dashboard(logged_in_admin, app_url):
    logged_in_admin.get(f"{app_url}/adminDash")
    WebDriverWait(logged_in_admin, 15).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "dashboard-name"), "Admin Dashboard"
        )
    )
    return logged_in_admin


def _point_test_driver_rows(browser):
    rows = browser.find_elements(
        By.CSS_SELECTOR, ".drivers-table tbody tr"
    )
    return [
        row
        for row in rows
        if row.find_element(By.CSS_SELECTOR, "button.driver-name").text.strip()
        == POINT_TEST_DRIVER
    ]


def _point_test_driver_total(browser):
    rows = _point_test_driver_rows(browser)
    if not rows:
        pytest.fail(
            f"{POINT_TEST_DRIVER} has no active sponsor-company balance to test."
        )
    return sum(
        (
            Decimal(row.find_element(By.CSS_SELECTOR, "td.balance").text.strip())
            for row in rows
        ),
        Decimal("0"),
    )


def _point_test_driver_balance_row(browser, driver_id, sponsor_company_id):
    for row in _point_test_driver_rows(browser):
        form = row.find_element(By.CSS_SELECTOR, "form.change-form")
        row_driver_id = form.find_element(
            By.NAME, "driver_id"
        ).get_attribute("value")
        row_company_id = form.find_element(
            By.NAME, "sponsorcomp_id"
        ).get_attribute("value")
        if row_driver_id == driver_id and row_company_id == sponsor_company_id:
            return row
    pytest.fail(
        f"{POINT_TEST_DRIVER}'s selected sponsor-company balance was not found."
    )


def _submit_point_test_driver_point_change(
    browser, driver_id, sponsor_company_id, action, reason
):
    row = _point_test_driver_balance_row(
        browser, driver_id, sponsor_company_id
    )
    form = row.find_element(By.CSS_SELECTOR, "form.change-form")
    form.find_element(By.NAME, "amount").send_keys("5")
    form.find_element(By.NAME, "reason").send_keys(reason)
    form.find_element(
        By.CSS_SELECTOR, f'button[name="action"][value="{action}"]'
    ).click()
    WebDriverWait(browser, 5).until(EC.alert_is_present()).accept()

    action_text = "added" if action == "add" else "subtracted"
    WebDriverWait(browser, 15).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".notice.success"),
            f"Successfully {action_text} 5 points.",
        )
    )


def test_dashboard_display(admin_dashboard):
    dashboard = admin_dashboard
    for heading in ("Sponsor Companies", "Sponsors", "Drivers", "Bulk Upload"):
        assert heading in dashboard.page_source

    assert dashboard.find_element(By.ID, "sponsor-filter").is_displayed()
    assert dashboard.find_element(By.ID, "driver-filter").is_displayed()
    assert dashboard.find_element(By.ID, "bulk-upload-file").get_attribute(
        "accept"
    ) == ".txt"


def test_admin_add_and_subtract(
    admin_dashboard, app_url
):
    browser = admin_dashboard
    wait = WebDriverWait(browser, 15)

    browser.find_element(By.LINK_TEXT, "Drivers").click()
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "dashboard-name"), "Manage Drivers"
        )
    )
    browser.find_element(By.LINK_TEXT, "Assign Points").click()
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "dashboard-name"), "Assign Points"
        )
    )

    initial_total = _point_test_driver_total(browser)
    target_row = _point_test_driver_rows(browser)[0]
    target_form = target_row.find_element(By.CSS_SELECTOR, "form.change-form")
    driver_id = target_form.find_element(
        By.NAME, "driver_id"
    ).get_attribute("value")
    sponsor_company_id = target_form.find_element(
        By.NAME, "sponsorcomp_id"
    ).get_attribute("value")
    initial_balance = Decimal(
        target_row.find_element(By.CSS_SELECTOR, "td.balance").text.strip()
    )

    run_id = uuid4().hex
    add_reason = f"test"
    subtract_reason = f"test"
    addition_may_have_applied = False

    try:
        addition_may_have_applied = True
        _submit_point_test_driver_point_change(
            browser, driver_id, sponsor_company_id, "add", add_reason
        )
        browser.get(f"{app_url}/assignPoints")
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "dashboard-name"), "Assign Points"
            )
        )
        assert _point_test_driver_total(browser) == initial_total + Decimal("5")

        _submit_point_test_driver_point_change(
            browser, driver_id, sponsor_company_id, "subtract", subtract_reason
        )
        browser.get(f"{app_url}/assignPoints")
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "dashboard-name"), "Assign Points"
            )
        )
        assert _point_test_driver_total(browser) == initial_total
        addition_may_have_applied = False
    finally:
        if addition_may_have_applied:
            try:
                WebDriverWait(browser, 2).until(EC.alert_is_present()).accept()
            except TimeoutException:
                pass

            browser.get(f"{app_url}/assignPoints")
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "dashboard-name"), "Assign Points"
                )
            )
            current_row = _point_test_driver_balance_row(
                browser, driver_id, sponsor_company_id
            )
            current_balance = Decimal(
                current_row.find_element(By.CSS_SELECTOR, "td.balance").text.strip()
            )

            if (
                current_balance == initial_balance + Decimal("5")
                and add_reason in current_row.find_elements(By.TAG_NAME, "td")[4].text
            ):
                _submit_point_test_driver_point_change(
                    browser,
                    driver_id,
                    sponsor_company_id,
                    "subtract",
                    subtract_reason,
                )
                restored_row = _point_test_driver_balance_row(
                    browser, driver_id, sponsor_company_id
                )
                assert Decimal(
                    restored_row.find_element(
                        By.CSS_SELECTOR, "td.balance"
                    ).text.strip()
                ) == initial_balance
            elif current_balance != initial_balance:
                pytest.fail(
                    f"{POINT_TEST_DRIVER}'s balance changed unexpectedly; automatic "
                    "restoration was not safe."
                )


@pytest.mark.parametrize(
    ("link_text", "page_heading"),
    (
        ("Sponsors", "Manage Sponsors"),
        ("Drivers", "Manage Drivers"),
        ("Reports", "Manage Reports"),
        ("Audit Logs", "Manage Audit Logs"),
    ),
)
def test_admin_navigation(
    admin_dashboard, link_text, page_heading
):
    admin_dashboard.find_element(By.LINK_TEXT, link_text).click()
    WebDriverWait(admin_dashboard, 15).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "dashboard-name"), page_heading
        )
    )
    assert page_heading in admin_dashboard.page_source


@pytest.mark.parametrize(
    ("filter_id", "row_selector", "data_attribute"),
    (
        ("sponsor-filter", ".sponsor-row", "data-sponsor"),
        ("driver-filter", ".driver-row", "data-sponsor-ids"),
    ),
)
def test_company_filters(
    admin_dashboard, filter_id, row_selector, data_attribute
):
    filter_select = Select(admin_dashboard.find_element(By.ID, filter_id))
    company_options = [
        option
        for option in filter_select.options
        if option.get_attribute("value") != "all"
    ]
    if not company_options:
        pytest.skip("No sponsor companies are available for filtering.")

    rows = admin_dashboard.find_elements(By.CSS_SELECTOR, row_selector)
    if not rows:
        pytest.skip("No matching dashboard rows are available for filtering.")

    company_id = company_options[0].get_attribute("value")
    filter_select.select_by_value(company_id)

    for row in rows:
        row_companies = row.get_attribute(data_attribute)
        if filter_id == "driver-filter":
            expected_visible = company_id in row_companies.split(",")
        else:
            expected_visible = row_companies == company_id
        assert row.is_displayed() is expected_visible


@pytest.mark.parametrize(
    ("row_selector", "modal_title"),
    (
        (".company-row", "Sponsor Company"),
        (".sponsor-row", "Sponsor Information"),
        (".driver-row", "Driver Information"),
    ),
)
def test_dashboard_rows(
    admin_dashboard, row_selector, modal_title
):
    rows = admin_dashboard.find_elements(By.CSS_SELECTOR, row_selector)
    if not rows:
        pytest.skip(f"No rows are available for {modal_title.lower()} details.")

    admin_dashboard.execute_script("arguments[0].click();", rows[0])
    modal = admin_dashboard.find_element(By.ID, "user-modal")
    WebDriverWait(admin_dashboard, 10).until(EC.visibility_of(modal))
    assert admin_dashboard.find_element(By.ID, "modal-title").text == modal_title

    modal.find_element(
        By.XPATH, ".//button[normalize-space()='Close']"
    ).click()
    WebDriverWait(admin_dashboard, 10).until(EC.invisibility_of_element(modal))


def test_bulk_upload_displays_selected_file_name(admin_dashboard, tmp_path):
    upload_file = tmp_path / "admin-dashboard-test.txt"
    upload_file.write_text("test|upload", encoding="utf-8")

    admin_dashboard.find_element(By.ID, "bulk-upload-file").send_keys(
        str(upload_file)
    )

    assert (
        admin_dashboard.find_element(By.ID, "selected-file-name").text
        == upload_file.name
    )

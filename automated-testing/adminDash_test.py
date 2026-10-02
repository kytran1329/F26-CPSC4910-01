import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_user_profile_link():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/home")

    link = driver.find_element(By.LINK_TEXT, "Admin Dashboard")
    link.click()

    assert "My Profile" in driver.page_source

    driver.quit()

def test_admin_dashboard_loads():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/adminDash")

    assert "Admin Dashboard" in driver.page_source

    driver.quit()

def test_admin_dashboard_drivers():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/adminDash")

    assert "Drivers" in driver.page_source

    driver.quit()

def test_admin_dashboard_sponsor_companies():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/adminDash")

    assert "Sponsor Companies" in driver.page_source

    driver.quit()

def test_admin_modal_opens():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/adminDash")

    button = driver.find_element(By.CLASS_NAME, "button")
    button.click()

    modal = driver.find_element(By.ID, "myModal")

    assert modal.is_displayed()

    driver.quit()
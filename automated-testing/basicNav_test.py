import os
import pytest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

# If anyone has to add any more tests, make sure that ALL test files end in "_test.py" 
# and ALL tests start with "test_"

# Checks if the web app loads properly
def test_app_loads():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")
    assert "Road Reward Login" in driver.page_source
    driver.quit

# Checks the about page link
def test_about_link():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")
    driver.implicitly_wait(1)

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(os.getenv("DRIVER_USER"))
    password_field.send_keys(os.getenv("DRIVER_PASSWORD"))

    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()

    link = driver.find_element(By.LINK_TEXT, "Back to Home")
    link.click()

    button = driver.find_element(By.LINK_TEXT, "About")
    button.click()
    
    assert "Road Reward" in driver.page_source
    driver.quit

# Checks the catalog page link
def test_catalog_link():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")
    driver.implicitly_wait(1)
    
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys(os.getenv("DRIVER_USER"))
    password_field.send_keys(os.getenv("DRIVER_PASSWORD"))
    
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()
    
    link = driver.find_element(By.LINK_TEXT, "Back to Home")
    link.click()
    
    button = driver.find_element(By.LINK_TEXT, "Catalog")
    button.click()
        
    assert "Product Search" in driver.page_source
    driver.quit


def test_placeholder():
    test = 'a'
    assert test == 'a', f"The test didn't work"
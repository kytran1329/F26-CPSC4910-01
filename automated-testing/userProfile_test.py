import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_user_profile_link():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/home")

    link = driver.find_element(By.LINK_TEXT, "User Profile")
    link.click()

    assert "My Profile" in driver.page_source

    driver.quit()

def test_user_profile_loads():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/userProfile")

    assert "My Profile" in driver.page_source

    driver.quit()    

def test_user_profile_information():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242/userProfile")

    assert "John" in driver.page_source
    assert "Smith" in driver.page_source

    driver.quit()
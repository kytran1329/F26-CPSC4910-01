import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_user_profile_link():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")

    driver.implicitly_wait(1)
    
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys("lukeskywalker@gmail.com")
    password_field.send_keys("T-16Skyhopper")
    
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()

    link = driver.find_element(By.LINK_TEXT, "Back to Home")
    link.click()

    button = driver.find_element(By.LINK_TEXT, "User Profile")
    button.click()

    assert "Luke Skywalker's Profile" in driver.page_source

    driver.quit()

def test_user_profile_loads():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")

    driver.implicitly_wait(1)
        
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
        
    username_field.send_keys("lukeskywalker@gmail.com")
    password_field.send_keys("T-16Skyhopper")
        
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()
    
    link = driver.find_element(By.LINK_TEXT, "Back to Home")
    link.click()
    
    button = driver.find_element(By.LINK_TEXT, "User Profile")
    button.click()

    assert "Luke Skywalker's Profile" in driver.page_source

    driver.quit()    

def test_user_profile_information():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")

    driver.implicitly_wait(1)
        
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
        
    username_field.send_keys("lukeskywalker@gmail.com")
    password_field.send_keys("T-16Skyhopper")
        
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()
    
    link = driver.find_element(By.LINK_TEXT, "Back to Home")
    link.click()
    
    button = driver.find_element(By.LINK_TEXT, "User Profile")
    button.click()

    assert "Luke" in driver.page_source
    assert "Skywalker" in driver.page_source

    driver.quit()
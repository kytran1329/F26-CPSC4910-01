import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_admin_login():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")

    driver.implicitly_wait(2)
        
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
        
    username_field.send_keys("chosenone@gmail.com")
    password_field.send_keys("Padme")
        
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()

    assert "Admin Dashboard" in driver.page_source

    driver.quit()

def test_admin_dashboard_loads():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")
    
    driver.implicitly_wait(2)
            
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
            
    username_field.send_keys("chosenone@gmail.com")
    password_field.send_keys("Padme")
            
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()
    
    assert "Admin Dashboard" in driver.page_source
    
    driver.quit()

def test_admin_dashboard_drivers():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")
        
    driver.implicitly_wait(2)
                
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
                
    username_field.send_keys("chosenone@gmail.com")
    password_field.send_keys("Padme")
                
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()

    assert "Drivers" in driver.page_source

    driver.quit()

def test_admin_dashboard_sponsor_companies():
    driver = webdriver.Chrome()
    driver.get("http://54.226.176.242")
        
    driver.implicitly_wait(2)
                
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
                
    username_field.send_keys("chosenone@gmail.com")
    password_field.send_keys("Padme")
            
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()

    assert "Sponsor Companies" in driver.page_source

    driver.quit()

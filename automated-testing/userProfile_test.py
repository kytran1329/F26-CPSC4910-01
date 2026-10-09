import os
import pytest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

def test_user_profile_link():
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
        
    username_field.send_keys(os.getenv("DRIVER_USER"))
    password_field.send_keys(os.getenv("DRIVER_PASSWORD"))
        
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
        
    username_field.send_keys(os.getenv("DRIVER_USER"))
    password_field.send_keys(os.getenv("DRIVER_PASSWORD"))
        
    button = driver.find_element(By.XPATH, "//button[text()='Login']")
    button.click()
    
    link = driver.find_element(By.LINK_TEXT, "Back to Home")
    link.click()
    
    button = driver.find_element(By.LINK_TEXT, "User Profile")
    button.click()

    assert "Luke" in driver.page_source
    assert "Skywalker" in driver.page_source

    driver.quit()

def test_admin_user_profile_link():
    admin = webdriver.Chrome()
    admin.get("http://54.226.176.242")

    admin.implicitly_wait(1)
    
    username_field = admin.find_element(By.NAME, "username")
    password_field = admin.find_element(By.NAME, "password")
    
    username_field.send_keys(os.getenv("ADMIN_USER"))
    password_field.send_keys(os.getenv("ADMIN_PASSWORD"))
    
    button = admin.find_element(By.XPATH, "//button[text()='Login']")
    button.click()

    link = admin.find_element(By.LINK_TEXT, "Back to Home")
    link.click()

    button = admin.find_element(By.LINK_TEXT, "User Profile")
    button.click()

    assert "Anakin Skywalker's Profile" in admin.page_source

    admin.quit()
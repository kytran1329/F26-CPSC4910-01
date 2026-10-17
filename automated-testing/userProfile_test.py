import os
import pytest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#Feature that lets you wait until something specific happens on the webpage before continuing
from selenium.webdriver.support import expected_conditions as EC #EC stands for Expected Change

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

def test_admin_can_change_first_name():
    admin = webdriver.Chrome()
    wait = WebDriverWait(admin, 10)

    try:
        admin.get("http://54.226.176.242")

        username_field = admin.find_element(By.NAME, "username")
        password_field = admin.find_element(By.NAME, "password")

        username_field.send_keys(os.getenv("ADMIN_USER"))
        password_field.send_keys(os.getenv("ADMIN_PASSWORD"))

        admin.find_element(By.XPATH, "//button[text()='Login']").click()

        # Navigate to User Profile
        wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Back to Home"))
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "User Profile"))
        ).click()

        # Save the original first name
        first_name_display = wait.until(
            EC.visibility_of_element_located((By.ID, "first-name-display"))
        )
        original_first_name = first_name_display.text.strip()

        # Change the first name to Annie
        admin.find_element(By.ID, "edit-first-name-button").click()

        first_name_input = wait.until(
            EC.visibility_of_element_located((By.ID, "first-name-input"))
        )
        first_name_input.clear()
        first_name_input.send_keys("Annie")

        admin.find_element(
            By.XPATH, "//form[@id='first-name-form']//button[@type='submit']"
        ).click()

        # Verify the change was saved
        wait.until(
            EC.text_to_be_present_in_element(
                (By.ID, "first-name-display"), "Annie"
            )
        )
        assert admin.find_element(By.ID, "first-name-display").text.strip() == "Annie"

        # Change the first name back to its original value
        admin.find_element(By.ID, "edit-first-name-button").click()

        first_name_input = wait.until(
            EC.visibility_of_element_located((By.ID, "first-name-input"))
        )
        first_name_input.clear()
        first_name_input.send_keys(original_first_name)

        admin.find_element(
            By.XPATH, "//form[@id='first-name-form']//button[@type='submit']"
        ).click()

        # Verify the original name was restored
        wait.until(
            EC.text_to_be_present_in_element(
                (By.ID, "first-name-display"), original_first_name
            )
        )
        assert (
            admin.find_element(By.ID, "first-name-display").text.strip()
            == original_first_name
        )

    finally:
        admin.quit()
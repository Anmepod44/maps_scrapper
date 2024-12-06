import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests

# Set up undetected ChromeDriver
options = Options()
# Uncomment below for headless mode if needed
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")  # Reduces detection
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

# Start undetected ChromeDriver
driver = uc.Chrome(options=options)

try:
    # Base URL for the first page
    base_url = "https://glovoapp.com/ke/en/nairobi/food_1/"
    page = 1
    total_count = 0  # To keep track of total elements across all pages

    while True:
        # Use base URL for the first page, then add `?page=n` for subsequent pages
        url = base_url if page == 1 else f"{base_url}?page={page}"
        
        # Check for HTTP 400 error
        response = requests.get(url)
        if response.status_code == 400:
            print(f"Encountered 400 error on page {page}. Stopping.")
            break
        driver.get(url)
        time.sleep(5)  # Allow the page to load
        
        # Find elements with the specified attribute
        elements = driver.find_elements(By.XPATH, '//*[@data-test-id="category-store-card"]')
        count = len(elements)

        for element in elements:
            try:
                store_name = element.find_element(By.XPATH, './/*[@data-test-id="store-card-title"]')
                print(store_name.text)
            except Exception as e:
                print(f"Error accessing store name: {e}")
                print(f"Page {page}: Found {count} elements")
        
        # Add to total count
        total_count += count
        
        # Move to the next page
        page += 1

    print(f"Total elements across all pages: {total_count}")

finally:
    driver.quit()
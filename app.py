import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
                name=store_name.text

                #Click on that area.
                # Wait for the nested element to be clickable
                nested_element = WebDriverWait(element, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "store-card__content"))
                )
                nested_element.click()
                time.sleep(5)
                
                #Get the master container
                master_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="default-wrapper"]/div/div/div/section[1]/div[2]/div[2]/div[3]/div[3]/div/div[1]'))
                )

                # #Get the store elements content : nested in the master container
                # nested_elements = master_container.find_elements(By.XPATH, './/div[@data-test-id="store-content"]')

                # for element in nested_elements:
                #     list_containers = master_container.find_elements(By.XPATH, './/div[contains(@class, "list__container")]')
                #     print(len(list_containers))

                
                # #Navigate through the store container elements.


                # # Wait for the new page to load (you can adjust this as needed)
                # time.sleep(5)

                print(master_container)

                # Go back to the previous page
                driver.back()

                # Wait for the page to reload before continuing
                time.sleep(5)
                print(f"Clicked on: {store_name.text}")
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
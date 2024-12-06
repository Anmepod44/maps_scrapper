import undetected_chromedriver as uc
import time

# Launch an undetectable Chrome browser
driver = uc.Chrome()

# Open a website
driver.get("https://www.google.com/maps")

# Print the title of the page
print(driver.title)

#wait for 10 seconds
time.wait(10)

# Close the browser
driver.quit()

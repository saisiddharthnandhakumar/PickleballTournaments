from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Ensure chromedriver path is correctly loaded
chromedriver_path = 'c:/Program Files/chromedriver-win64/chromedriver.exe'

# Check if chromedriver_path is valid
if not os.path.isfile(chromedriver_path):
    raise ValueError(f"The path is not a valid file: {chromedriver_path}")

# Set up Selenium WebDriver with SSL certificate error handling
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
service = Service(executable_path=chromedriver_path)  # Replace with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the pickleball brackets points and ratings page
url = 'https://pickleballbrackets.com/pts.aspx'
driver.get(url)

try:
    # Adjust the timeout as needed
    wait = WebDriverWait(driver, 120)

    # Function to safely extract text from elements
    def extract_text(elements):
        return [element.text.strip() if element.text.strip() else None for element in elements]

    # Example XPath (replace this with your copied XPath)
    see_more_xpath = '//*[@id="btnMoreResults"]'
    no_more_results_xpath = '//*[@id="dvNoMoreResults"]'  # XPath for "No More Results" div

    # Function to click "See More" until "No More Results" appears
    def click_see_more():
        while True:
            try:
                # Wait for the "See More" button to be clickable
                see_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, see_more_xpath)))
                print("Found 'See More' button, clicking it.")

                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView();", see_more_button)
                
                # Add a small delay to ensure button is clickable
                time.sleep(2)
                
                # Click the button
                see_more_button.click()
                print("Clicked 'See More' button.")

                # Wait for the new content to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'browse-row')))
                print("New content loaded, looking for 'See More' button again.")
                
                # Add a delay to ensure the page has loaded more results
                time.sleep(5)

            except Exception as e:
                print(f"No more 'See More' button or error: {e}")
                break

            # Check if "No More Results" message is present
            try:
                no_more_results = driver.find_element(By.XPATH, no_more_results_xpath)
                if no_more_results.is_displayed():
                    print("Found 'No More Results' message.")
                    break
            except Exception as e:
                print(f"No 'No More Results' message yet: {e}")

    # Click "See More" to load all data
    click_see_more()

    # Wait for the elements to be present and visible
    browse_row_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'browse-row')))
    
    # Extract text from elements with handling for missing data
    browse_row_data = extract_text(browse_row_elements)

    # Create a DataFrame
    df = pd.DataFrame({
        'Browse Row Data': browse_row_data
    })

    # Print the dataframe (optional: you can save it to a file if needed)
    print(df)
    df.to_csv('extract_data.csv', index=False)

except Exception as e:
    print(f'An error occurred: {e}')

finally:
    # Close the browser
    driver.quit()

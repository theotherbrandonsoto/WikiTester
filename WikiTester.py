# WikiTester.py
#Takes a Reddit Wiki URL, and then reviews each link in the Wiki then reports out on the failures. 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Prompt user for the URL to check
print('What is the URL you would like to check?')
wiki_url = input()

# Initialize WebDriver (ensure the appropriate WebDriver for your browser is installed)
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

try:
    # Open the provided URL
    driver.get(wiki_url)
    
    # Wait for the page to load by ensuring the presence of the body element
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Locate the specific <div> with class 'md wiki'
    container = driver.find_element(By.CSS_SELECTOR, 'div.md.wiki')
    
    # Find all anchor (<a>) elements within this container
    link_elems = container.find_elements(By.TAG_NAME, 'a')
    
    # Extract href attributes from anchor elements
    links = [elem.get_attribute('href') for elem in link_elems if elem.get_attribute('href')]

    # Initialize a dictionary to store the outcome
    link_status = {}

    # Loop through each link and check its status
    for link in links:
        try:
            # Make a HEAD request to check the URL status
            response = requests.head(link, allow_redirects=False, timeout=5)
            status_code = response.status_code
            
            if status_code in [200, 301, 302]:
                if status_code == 200:
                    # Load the page to check for "Page not found"
                    driver.get(link)
                    try:
                        # Check if the <span slot="title">Page not found</span> exists
                        wait.until(EC.presence_of_element_located((By.XPATH, '//span[@slot="title" and text()="Page not found"]')))
                        # If found, mark as failed
                        link_status[link] = 'Page not found'
                    except Exception:
                        # If not found, the page is considered working
                        link_status[link] = 'Working'
                else:
                    # For 301 and 302, consider as working
                    link_status[link] = 'Working'
            else:
                # Record the status code if not 200, 301, or 302
                link_status[link] = f'Status code: {status_code}'
        except requests.RequestException as e:
            # Record as failed if any error occurs
            link_status[link] = f'Failed ({e})'

    # Filter out non-working links
    non_working_links = {link: status for link, status in link_status.items() if status != 'Working'}

    # Print only non-working links
    print("\nNon-Working Links:")
    for link, status in non_working_links.items():
        print(f"{link}: Not Working (Reason: {status})")

    print(f"\nTotal Links Checked: {len(links)}")
    print(f"Successful Links: {len(links) - len(non_working_links)}")
    print(f"Failed Links: {len(non_working_links)}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

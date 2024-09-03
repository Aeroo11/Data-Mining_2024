from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

def scraper(url):
    print('Mau scrapping', url)
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        # options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        # Get the URL given
        driver.get(url)
 
        # Selenium will wait for a maximum of 5 seconds for an element matching the given criteria to be found. 
        # If no element is found in that time, Selenium will raise an error.
        try:
            wait = WebDriverWait(driver, timeout=5)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-container')))
            print('Elemen ditemukan')
        except:
            raise LookupError("Tidak ada elemen yang ditentukan")
        
        # BeautifulSoup will parse the URL
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
 
        # Prepare the variable for JSON data
        books = []

        # BeautifulSoup will find the CSS class that contain product container
        for book in soup.find_all('div', class_='entities-list'):
            
            # Safely get the text from the specified element
            book_name = book.find('div', class_='list-title')
            book_price = book.find('p', class_='formats-price')
            book_author = book.find('span', class_='list-author')
            book_price_bf = book.find('p', class_='formats-base-price')

            # Check if elements are found before accessing their text attribute
            book_name_text = book_name.text.strip() if book_name else 'No title'
            book_price_text = book_price.text.strip() if book_price else 'No price after discount'
            book_author_text = book_author.text.strip() if book_author else 'No author'
            book_price_bf_text = book_price_bf.text.strip() if book_price_bf else 'No price before discount'
            
            # Append the scraped data into books variable for JSON data
            books.append(
                {
                    'Book Title': book_name_text,
                    'Price Before Discount': book_price_bf_text,
                    'Price After Discount': book_price_text,
                    'Author': book_author_text
                }
            )
        
        # Close the WebDriver
        driver.quit()
 
        return books
    
    except Exception as e:
        print('Error:', e)
        driver.quit()

if __name__ == '__main__':
    url = 'https://www.gramedia.com/boutique'
    data = scraper(url)

    if data:
        with open('Gramedia_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json


def scapper(url):
    print("Mau Scraping: ", url)
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        driver.get(url)

    
        # BeautifulSoup will parse the URL
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
 
        # Prepare the variable for JSON data
        movies = []

        for course in soup.find_all('li', class_='ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent'):

            movie_name = course.find('h3', class_='ipc-title__text').text
            movie_year = course.find_all('span', {'class':'sc-b189961a-8 hCbzGp cli-title-metadata-item'})[0].text 
            movie_duration = course.find_all('span', {'class':'sc-b189961a-8 hCbzGp cli-title-metadata-item'})[1].text
            movie_age = course.find_all('span', {'class':'sc-b189961a-8 hCbzGp cli-title-metadata-item'})[2].text 
            
            # Get the text from the specified element and assign them to the variables
            # course_name = course.find('h5', class_='course-card__name').text
            # course_hour = course.find_all('span', {'class':'mr-2'})[0].text
            # course_summary = course.select('div.course-card__summary p')[0].text
            # course_total_module = course.find_all('div', class_= 'course-card__info-item')[0].find_all('span')[0].contents[0]
            # course_level = course.find('span', attrs={'class': None}).text
            
            # Not all courses in the list has rating, so we should manage it. 
            # If it has rating, get the text. If none, set it to empty string.
            # try:
            #     course_rating = course.find_all('span', {'class':'mr-2'})[1].text
            # except IndexError:
            #     # Handle the case when no span elements with the specified class are found
            #     course_rating = ''
 
            # Not all courses in the list has total students, so we should manage it. 
            # If it has total students, get the text. If none, set it to empty string.
            # try:
            #     course_total_students = course.find_all('span', {'class':'mr-3'})[1].get_text()
            # except:
            #     course_total_students = ''

        # Append the data to the courses list
            movies.append({
                'movie_name': movie_name,
                # 'movie_rate': 
                'movie_year': movie_year,
                'movie_duration': movie_duration,
                'movie_age': movie_age  
                # 'total_review': 
            })

    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return movies
    
        
if __name__ == "__main__":
    print('Mulai')
    url = "https://www.imdb.com/chart/top"

    data = scapper(url)

    with open('Imdb_data1.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print('Selesai')






from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json


def scapper(url):
    print("Mau Scraping: ", url)
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)

        driver.get(url)

        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # BeautifulSoup will parse the URL
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")

        # Prepare the variable for JSON data
        movies = []

        for movie in soup.find_all(
            "li", class_="ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent"
        ):

            movie_name = movie.find("h3", class_="ipc-title__text").text
            movie_data = movie.find_all(
                "span",
                {"class": "sc-b189961a-8 hCbzGp cli-title-metadata-item"},
            )
            movie_year = movie.find_all(
                "span", {"class": "sc-b189961a-8 hCbzGp cli-title-metadata-item"}
            )[0].text
            movie_duration = movie.find_all(
                "span", {"class": "sc-b189961a-8 hCbzGp cli-title-metadata-item"}
            )[1].text
            if len(movie_data) > 2:
                movie_age = movie.find_all(
                    "span", {"class": "sc-b189961a-8 hCbzGp cli-title-metadata-item"}
                )[2].text
            else:
                movie_age = "Unknown"

            movie_rate = movie.find("span", {"class": 'ipc-rating-star--rating'}).text

            total_review = movie.find("span", {"class": "ipc-rating-star--voteCount"}).text

            # if movie_rate:
            #     movie_rating = movie_rate.text.strip()
            # else:
            #     movie_rating = ""

            # total_review = movie.find("span", {"class": "ipc-rating-star--voteCont"})[0].text

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
            movies.append(
                {
                    "movie_name": movie_name,
                    "movie_rate": movie_rate,
                    "movie_year": movie_year,
                    "movie_duration": movie_duration,
                    "movie_age": movie_age,
                    "total_review": total_review
                }
            )

    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return movies


if __name__ == "__main__":
    print("Mulai")
    url = "https://www.imdb.com/chart/top"

    data = scapper(url)

    with open("Imdb_data2.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Selesai")
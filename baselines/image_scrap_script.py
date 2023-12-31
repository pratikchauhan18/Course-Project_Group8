
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import os
import time


# ref: https://github.com/chuanenlin/shutterscrape
# method to get the scraped images and stored in a directory
def imagescrape(searchTerm, searchPage, image_type, directory_path):
    titles = list()
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()

        permission_mode = 0o777
        main_path = os.path.join(directory_path, searchTerm)
        os.mkdir(main_path, permission_mode)

        count = 1
        for i in range(1, searchPage + 1):
            url = "https://www.shutterstock.com/search?searchterm=" + searchTerm + "&sort=popular&image_type=" + image_type + "&search_source=base_landing_page&language=en&page=" + str(i)
            driver.get(url)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(6)

            data = driver.execute_script("return document.documentElement.outerHTML")
            print("Page " + str(i))

            scraper = BeautifulSoup(data, "lxml")
            img_container = scraper.find_all("img", {
                "class": "mui-1l7n00y-thumbnail"
            })

            for j in range(0, len(img_container)-1):
                img_src = img_container[j].get("src")
                img_title = img_container[j].get("alt")

                try:
                    urllib.request.urlretrieve(img_src, main_path + '/{}_{}.{}'.format(searchTerm, str(count), img_src[-3:]))
                    titles.append([count, img_title])

                except Exception as e:
                    print(e)

                count += 1

        driver.close()

    except Exception as e:
        print(e)

    dataset = pd.DataFrame(titles, columns=["id", "title"])
    dataset.to_csv(r'{}'.format(directory_path) + '/joy_titles.csv', index=False)
    return


# method to create a directory with a given name
def create_directory(dirname):
    parent_path = 'E:\M_TECH ASSIGNMENTS\Information Retrieval\Project'
    permission_mode = 0o777
    image_path = os.path.join(parent_path, dirname)
    os.mkdir(image_path, permission_mode)

    return image_path


if __name__ == '__main__':
    dirname = 'image_data'
    image_path = create_directory(dirname)

    tag = 'depression anxiety'
    no_of_pages = 15
    type_of_posts = 'photo'

    imagescrape(tag, no_of_pages, type_of_posts, image_path)

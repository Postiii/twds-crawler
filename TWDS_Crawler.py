# Import Packages
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from google.auth import compute_engine
from google.cloud import datastore

# Local chrome options and path
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_path = r'/usr/local/bin/chromedriver'


class Crawler:
    def __init__(self):
        pass

    # Initialize Google Datastore Connection
    def initializeGDS(self):
        global credentials
        global client
        print("Setup Database Connection")
        credentials = compute_engine.Credentials()
        # service account
        client = datastore.Client.from_service_account_json('sa.json')

    # Insert Dictionary into Google Data Store
    def writeToDB(self, resultArticleDetails):
        # Extract single elements
        for value in resultArticleDetails.values():
            str_articlenumber = value["Article_ID"]
            str_URL = value['URL']
            str_title = value['Title']
            str_author = value['Author']
            str_pubdate = value['PublishingDate']
            str_text = value['Text']
            try:
                int_claps = value['Claps']
            except:
                int_claps = 0
            Tag_list = value['Tags']
            int_responses = value['No_Responses']
            int_reading_time = value['Reading_time']
            # Create new Article Entity
            Article = datastore.Entity(client.key('Article_ID', str_articlenumber), exclude_from_indexes=['Text'])
            Article.update({
                "URL": str_URL,
                "Title": str_title,
                "Author": str_author,
                "PublishingDate": str_pubdate,
                "Text": str_text,
                "Claps": int_claps,
                "Tags": Tag_list,
                "No_Responses": int_responses,
                "Reading_time": int_reading_time
            })
            client.put(Article)
        return (True)

    def getAuthors(self):
        print("Get Authors...")
        url = "https:/towardsdatascience.com/archive"
        # Define Webdriver
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.get(url)

        # Scroll page to load whole content --> in eigene Methode auslagern!
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get source code from page
        htmltext = driver.page_source
        soup = BeautifulSoup(htmltext, "lxml")
        driver.quit()
        # Extract links to profiles from TWDS Authors
        authors = []
        for link in soup.find_all("a",
                                  class_="link link--darker link--darken u-accentColor--textDarken u-baseColor--link u-fontSize14 u-flex1"):
            authors.append(link.get('href'))
        # Clear list from duplicates by using a dictionary
        authors = list(dict.fromkeys(authors))
        print("Received list of authors")
        return authors

    def getArticles(self, author):
        if author == "https://towardsdatascience.com/@TDSteam":
            pass
        else:
            print("Get Articles...")
            twdsarticles = {}
            # Define Webdriver
            driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)           
            url = author
            driver.get(url)

            # Scroll page to load whole content
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to the bottom.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load the page.
                time.sleep(2)
                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Get source code from page
            htmltext = driver.page_source
            soup = BeautifulSoup(htmltext, "lxml")
            driver.quit()
            # Get TWDS-Articles of each author
            for link in soup.find_all("a", class_=""):
                if "towards" not in link.get('href'):
                    pass
                else:
                    if link.get('href') not in twdsarticles.keys():
                        twdsarticles[link.get('href')] = url
                    else:
                        pass
            print("Received list of articles")
            return twdsarticles

    def getArticleDetails(self, articles):
        print("Get Article Details...")
        artdic = {}
        # Define Webdriver
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        url = articles
        driver.get(url)

        # Get source code from page
        htmltext = driver.page_source
        soup = BeautifulSoup(htmltext, "lxml")
        driver.quit()
        # Extract field values and parse them to json / dictionary
        tempdic = {}
        try:
            tempdic['Article_ID'] = soup.find("meta", attrs={"name": "parsely-post-id"})["content"]
        except:
            tempdic['Article_ID'] = "0"
        tempdic['URL'] = url
        tempdic['Title'] = soup.title.string
        tempdic['Author'] = soup.find("meta", attrs={"name": "author"})["content"]

        # Loop to extract clean date
        tempdic['PublishingDate'] = \
            re.findall(r".+?(?=T)", soup.find("meta", property="article:published_time")["content"])[0]

        # Loop to extract no of responses and reading_time
        tempdic['Reading_time'] = re.findall(r"[0-9]", soup.find("meta", attrs={"name": "twitter:data1"})["value"])[
                0]
        try:
            tempdic['No_Responses'] = re.findall(r"[0-9]", soup.find("span", "az").string)[0]
        except:
            tempdic['No_Responses'] = 0

        # Loop to extract tags
        li = soup.select("ul > li > a")
        tags = []
        for link in li:
            tags.append(link.string)
        tempdic['Tags'] = tags

        # Loop to extract claps
        btns = soup.find_all("button")
        for button in btns:
            if button.string is None:
                pass
            else:
                try:
                    tempdic['Claps'] = (int(button.string))
                except:
                    break

        # Loop to get clean text
        pagetext = ""
        text = soup.findAll("p")
        for t in text:
            pagetext += t.getText()
        # Clean special characters
        pagetext = (" ".join(re.findall(r"[A-Za-z0-9]*", pagetext))).replace("  ", " ")
        tempdic['Text'] = pagetext
        artdic[url] = tempdic
        return (artdic)


def main():
    print("Start Crawler")
    twdsCrawler = Crawler()
    twdsCrawler.initializeGDS()
    resultAuthors = twdsCrawler.getAuthors()
    for a in resultAuthors:
        resultArticles = twdsCrawler.getArticles(a)
        if not resultArticles:
            pass
        else:
            for articles in resultArticles:
                resultArticleDetails = twdsCrawler.getArticleDetails(articles)
                dbresult = twdsCrawler.writeToDB(resultArticleDetails)
                if dbresult is True:
                    print("Insert completed")
                else:
                    print("Crawler did not finish work properly.")
    print("Crawler finished work...")


if __name__ == '__main__':
    main()

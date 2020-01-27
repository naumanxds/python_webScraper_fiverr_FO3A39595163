import dictionary
import csv
import error_logger

from google import google
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

NOT_FOUND = 'None'

def startScraping():
    # create browser instance
    manager = GeckoDriverManager()
    browserOptions = Options()
    browserOptions.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=manager.install(), options=browserOptions)
    try: 
        dictionaryDetail = dictionary.readDict()
        searchKey = dictionaryDetail['search_key']
        filters = dictionaryDetail['filters']
        startPage = dictionaryDetail['next_page']
        timeNow = datetime.now()

        if searchKey is "":
            print(' There is no Search Key to Scrape Please Select option No 2. and Enter a SearchKey')
            return

        if not startPage:
            startPage = 1

        if dictionaryDetail['last_executed'] != '' and (timeNow - datetime.strptime(dictionaryDetail['last_executed'], '%Y-%m-%d %H:%M:%S.%f')) < timedelta(1):
            print(' =>> 24 Hrs Have not passed after the last execution yet. Script cannot Run now. <<=\n\n')
            driver.quit()
            exit()


        for loop in range(50):
            print(' >> Starting Google Search for Links << \n')
            scrapeLinks = []
            result = google.search(searchKey, startPage)
            for link in result:
                flag = False
                for filterKey in filters:
                    if filterKey in link.link:
                        flag = True
                        break

                if flag:
                    continue

                scrapeLinks.append(link.link)
            startPage += 1
            dictionaryDetail['next_page'] = startPage
            dictionaryDetail['last_executed'] = timeNow.strftime('%Y-%m-%d %H:%M:%S.%f')
            dictionary.writeDict(dictionaryDetail)
            visitWebsites(scrapeLinks)
    except Exception as e:
        error_logger.logError(format(e))
        
    driver.quit()

# visit each website extracted from google search
def visitWebsites(links):
    for link in links:
        try:
            baseUrl = link.split('://')
            baseUrl = baseUrl[0] + '://' + baseUrl[1].split('/')[0]
            html = getHtml(baseUrl)
            if checkResponsive(html):
                print(' => website is responsive => ' + baseUrl)
                continue
            print(' => website is not responsive => ' + baseUrl)

            extractEmails(html, baseUrl)
            allLinks = html.find_all('a')
            for href in allLinks:
                if 'impressum' in str(href.get('href')) or 'kontakt' in str(href.get('href')) or 'uber' in str(href.get('href')):
                    extractEmails(getHtml(baseUrl + '/' + str(href.get('href'))), baseUrl)
        except Exception as e:
            error_logger.logError(format(e), link)

# check if the website is responsive or not 
def checkResponsive(html):
    try:
        meta = html.find('meta', {'name' : 'viewport'})
        responsive = html.find('div', {'class' : 'responsive'})
        svg = html.find('svg')
        if str(meta) == NOT_FOUND and str(responsive) == NOT_FOUND and str(svg) == NOT_FOUND and ('responsive' not in str(html)):
            return False

        return True
    except Exception as e:
        error_logger.logError(format(e))
        return True

# extract emails from given html page
def extractEmails(html, baseUrl):
    try:
        mails = []
        hrefs = html.find_all('a')
        flag = False
        for href in hrefs:
            if 'mailto' in str(href.get('href')):
                mails.append(str(href.get('href')))
                flag = True

            if '@' in str(href.get_text()):
                mails.append(str(href.get_text()))
                flag = True

        if flag:
            mails.insert(0, baseUrl)
            writeFile(mails, baseUrl)
            print(' => Conatct Extracted Successfully for => ' + baseUrl)
    except Exception as e:
        error_logger.logError(format(e))

# write in file
def writeFile(data, url = ''):
    try:
        with open('Contact-Lists-' + datetime.now().strftime('%d-%b-%y') + '.csv', 'a', encoding="utf-8") as fh:
            csvWriter = csv.writer(fh)
            csvWriter.writerow(data)
    except Exception as e:
        error_logger.logError('Error in Writing Data into the file == ' + format(e), url)

# get html of the provided page url
def getHtml(url):
    try:
        driver.get(url)
        driver.execute_script('return document.documentElement.outerHTML')
        return BeautifulSoup(driver.page_source, 'lxml')

    except Exception as e:
        error_logger.logError('Error in Fetching HTML == ' + format(e), url)

    return False

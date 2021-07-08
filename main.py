import time
import urllib.request
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
CSV_LOCATION = "C:\\Users\\Marshiie\\Pictures\\Senior Project\\scrapeList.csv"
AMAZON_URL = "https://www.amazon.com/"
WALMART_URL = "https://www.walmart.com/"
NOVATCG_URL = "https://www.novatcg.com/shop/"
SEARCH_CSV_LOCATION = "C:\\Users\\Marshiie\\Pictures\\Senior Project\\searchList.csv"

def scrapeFromCSV(csvFileLocation):
    print("\n")
    count = 1
    with open(csvFileLocation, newline = "") as csvFile:
        reader = csv.reader(csvFile, delimiter = ",")
        for rows in reader:
            url = rows[0]
            marketPrice = rows[1]
            if 'amazon' in url:
                name = amazonNameScrape(url)
                price = amazonPriceScrape(url)
            elif 'walmart' in url:
                name = walmartNameScrape(url)
                price = "$" + walmartPriceScrape(url)
            elif 'novatcg' in url:
                name = novatcgNameScrape(url)
                price = novatcgPriceScrape(url)
            print(count, ". "
                  + name
                  + ": "
                  + price
                  + "\n"
                  + url
                  +"\n"
                  +marketPrice)
            count += 1

def amazonPriceScrape(url):
    request = urllib.request.Request(url, headers = {"User-Agent": USER_AGENT})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    if soup.find('span', attrs= {'id': 'priceblock_ourprice'}):
        price = soup.find('span', attrs= {'id': 'priceblock_ourprice'}).text
    elif soup.find('span', attrs= {'class': 'qa-price-block-our-price'}):
        price = soup.find('span', attrs= {'class': 'qa-price-block-our-price'}).text
    elif soup.find('span', attrs= {'price'}):
        price = soup.find('span', attrs= {'price'}).text
    elif soup.find('div', attrs= {'price'}):
        price = soup.find('div', attrs= {'price'}).text
    else:
        price = "N/A"
    return price

def amazonNameScrape(url):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    if soup.find('span', attrs={'id': 'productTitle'}):
        name = soup.find('span', attrs={'id': 'productTitle'}).text.strip()
    elif soup.find('h1', attrs={'id': 'title'}):
        name = soup.find('h1', attrs={'id': 'title'}).text.strip()
    elif soup.find('span', attrs={'class': 'a-size-large'}):
        name = soup.find('span', attrs={'class': 'a-size-large'}).text.strip()
    elif soup.find('span', attrs={'class': 'product'}):
        name = soup.find('span', attrs={'class': 'product'}).text.strip()
    else:
        name = "N/A"
    return name

def walmartPriceScrape(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    if soup.find('span', attrs={'class': 'price-characteristic'}):
        price = soup.find('span', attrs={'class': 'price-characteristic'}).text
    else:
        price = "N/A"
    return price

def walmartNameScrape(url):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    if soup.find('h1', attrs={'class': 'prod-ProductTitle'}):
        name = soup.find('h1', attrs={'class': 'prod-ProductTitle'}).text.strip()
    else:
        name = "N/A"
    return name

def novatcgPriceScrape(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    if soup.find('span', attrs={'class': 'woocommerce-Price-amount'}):
        price = soup.find('span', attrs={'class': 'woocommerce-Price-amount'}).text
    else:
        price = "N/A"
    return price

def novatcgNameScrape(url):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    if soup.find('h1', attrs={'class': 'product_title'}):
        name = soup.find('h1', attrs={'class': 'product_title'}).text.strip()
    else:
        name = "N/A"
    return name

def addProduct(url, price, csvFileLocation):
    with open(csvFileLocation, 'a', newline = "\n", encoding = "utf-8") as writer:
        addCSV = csv.writer(writer)
        addCSV.writerow([url, price])

def searchAmazon(item, searchCSVList):
    driver = webdriver.Chrome("C:\\Users\\Marshiie\\Pictures\\Senior Project\\Chromedriver.exe")
    driver.maximize_window()
    driver.get(AMAZON_URL)
    input = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    input.send_keys(item)
    time.sleep(2)
    button = driver.find_element_by_xpath('//*[@id="nav-search-submit-button"]')
    button.click()
    time.sleep(2)
    count = 1
    countMax = 5
    searchListReset = open(searchCSVList, 'w+')
    searchListReset.close()
    while count <= countMax:
        result = driver.find_element_by_css_selector('div[data-cel-widget="search_result_'
                                                     + str(count)
                                                     + '"]')
        while result.get_attribute("data-asin") == "":
            count += 1
            countMax += 1
            result = driver.find_element_by_css_selector('div[data-cel-widget="search_result_'
                                                         + str(count)
                                                         + '"]')
        asin = result.get_attribute("data-asin")
        url = "https://www.amazon.com/dp/" + asin
        print(url)
        price = amazonPriceScrape(url)
        price = price.replace("$", "")
        price = price.replace(",", "")
        with open(searchCSVList, 'a', newline = "") as searchList:
            addSearch = csv.writer(searchList)
            addSearch.writerow([url, price])
        count += 1
        searchList.close()
    driver.close()

def searchWalmart(item, searchCSVList):
    driver = webdriver.Chrome("C:\\Users\\Marshiie\\Pictures\\Senior Project\\Chromedriver.exe")
    driver.maximize_window()
    driver.get(WALMART_URL)
    input = driver.find_element_by_xpath('//*[@id="global-search-input"]')
    input.send_keys(item)
    time.sleep(2)
    button = driver.find_element_by_xpath('//*[@id="global-search-submit"]')
    button.click()
    time.sleep(2)
    count = 1
    countMax = 5
    searchListReset = open(searchCSVList, 'w+')
    searchListReset.close()
    securityURL = driver.current_url
    if 'blocked' in securityURL:
        pressAndHold = driver.find_element_by_xpath('//*[@id="px-captcha"]/div/iframe[9]')
        action = ActionChains(driver)
        action.click_and_hold(on_element = pressAndHold)
    while count <= countMax:
        try:
            driver.find_element_by_xpath('//*[@id="searchProductResult"]/ul/li['
                                              + str(count)
                                              + ']/div/div[2]/div[2]/a/div/img')
            result = driver.find_element_by_xpath('//*[@id="searchProductResult"]/ul/li['
                                              + str(count)
                                              + ']/div/div[2]/div[2]/a/div/img')
            result.click()
            time.sleep(5)
            url = driver.current_url
            print(url)
            driver.back()
            with open(searchCSVList, 'a', newline = "") as searchList:
                addSearch = csv.writer(searchList)
                addSearch.writerow([url, walmartPriceScrape(url)])
            count += 1
            searchList.close()
            time.sleep(5)
        except:
            try:
                driver.find_element_by_xpath('//*[@id="searchProductResult"]/div/div['
                                             + str(count)
                                             +']/div/div/div[2]/div[1]/a/div/img')
                result = driver.find_element_by_xpath('//*[@id="searchProductResult"]/div/div['
                                             + str(count)
                                             +']/div/div/div[2]/div[1]/a/div/img')
                result.click()
                time.sleep(5)
                url = driver.current_url
                print(url)
                driver.back()
                with open(searchCSVList, 'a', newline="") as searchList:
                    addSearch = csv.writer(searchList)
                    addSearch.writerow([url, walmartPriceScrape(url)])
                count += 1
                searchList.close()
                time.sleep(5)
            except:
                count -= 1
                print("Only found " + str(count) + " of the item: " + item)
                break
    driver.close()

def searchNovaTCG(item, searchCSVList):
    driver = webdriver.Chrome("C:\\Users\\Marshiie\\Pictures\\Senior Project\\Chromedriver.exe")
    driver.maximize_window()
    driver.get(NOVATCG_URL)
    initialSearchButton = driver.find_element_by_xpath('/html/body/header/nav/div/div/div[3]/div[1]')
    initialSearchButton.click()
    time.sleep(2)
    input = driver.find_element_by_xpath('/html/body/header/nav/div/div/div[3]/div[1]/div[2]/form/input[1]')
    input.send_keys(item)
    time.sleep(2)
    button = driver.find_element_by_xpath('/html/body/header/nav/div/div/div[3]/div[1]/div[2]/form/input[2]')
    button.click()
    time.sleep(2)
    count = 1
    countMax = 5
    searchListReset = open(searchCSVList, 'w+')
    searchListReset.close()
    while count <= countMax:
        try:
            driver.find_element_by_xpath('//*[@id="shop-isle-blog-container"]/ul/li['
                                              + str(count)
                                              +']/a')
            result = driver.find_element_by_xpath('//*[@id="shop-isle-blog-container"]/ul/li['
                                              + str(count)
                                              +']/a')
            result.click()
            time.sleep(5)
            url = driver.current_url
            print(url)
            price = novatcgPriceScrape(url)
            price = price.replace("$", "")
            price = price.replace(",", "")
            with open(searchCSVList, 'a', newline = "") as searchList:
                addSearch = csv.writer(searchList)
                addSearch.writerow([url, price])
            count += 1
            searchList.close()
            driver.back()
            time.sleep(5)
        except:
            count -= 1
            print("Could only find " + str(count) + " of the item: " + str(item))
            break
    driver.close()

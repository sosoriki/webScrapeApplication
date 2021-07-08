import csv
import schedule
import time
import smtplib
from email.message import EmailMessage

from main import amazonPriceScrape
from main import walmartPriceScrape
from main import novatcgPriceScrape
from main import amazonNameScrape
from main import walmartNameScrape
from main import novatcgNameScrape

CSV_LOCATION = "C:\\Users\\Marshiie\\Pictures\\Senior Project\\scrapeList.csv"
USERNAME = 'webscrapingalerts@gmail.com'
PASSWORD = 'vfezpfmvclyvsqxu'
RECEIVER = 'webscrapingdemo@gmail.com'

def scrape(csvFileLocation):
    tempList = []
    alertMessage = "***Alert Price Drops***\n\n"
    with open(csvFileLocation, newline = "") as csvFile:
        reader = csv.reader(csvFile, delimiter = ",")
        for rows in reader:
            url = rows[0]
            targetPrice = rows[1]
            targetPrice = targetPrice.replace('$', "")
            targetPrice = targetPrice.replace(',', "")
            if 'amazon' in url:
                priceRaw = amazonPriceScrape(url)
                if 'N/A' not in priceRaw:
                    price = priceRaw.replace('$', "")
                    price = price.replace(',', "")
                    price.strip()
                    targetPrice.strip()
                    if float(price) < float(targetPrice):
                        alertMessage = alertMessage + amazonNameScrape(url) + " is now $" + price + " from $" + targetPrice + "\n" + url + "\n\n"
                        tempList.append([url, price])
                    elif float(price) > float(targetPrice):
                        tempList.append([url, price])
                    else:
                        tempList.append([url, targetPrice])
                else:
                    tempList.append(([url, targetPrice]))
            elif 'walmart' in url:
                #don't need to remove $ because returns without $
                price = walmartPriceScrape(url)
                if 'N/A' not in price:
                    price = price.replace(',', "")
                    price.strip()
                    targetPrice.strip()
                    if float(price) < float(targetPrice):
                        alertMessage = alertMessage + walmartNameScrape(url) + "is now $" + price + " from $" + targetPrice + "\n" + url + "\n\n"
                    elif float(price) > float(targetPrice):
                        tempList.append([url, price])
                    else:
                        tempList.append([url, targetPrice])
                else:
                    tempList.append(([url, targetPrice]))
            elif 'novatcg' in url:
                priceRaw = novatcgPriceScrape(url)
                if 'N/A' not in priceRaw:
                    price = priceRaw.replace('$', "")
                    price = price.replace(',', "")
                    price.strip()
                    targetPrice.strip()
                    if float(price) < float(targetPrice):
                        alertMessage = alertMessage + novatcgNameScrape(url) + "is now $" + price + " from $" + targetPrice + "\n" + url + "\n\n"
                    elif float(price) > float(targetPrice):
                        tempList.append([url, price])
                    else:
                        tempList.append([url, targetPrice])
                else:
                    tempList.append(([url, targetPrice]))
    with open(csvFileLocation, 'w', newline = "\n", encoding = "utf-8") as writeCSV:
        write = csv.writer(writeCSV)
        write.writerows(tempList)
    return alertMessage

def alert(alertMessage, messageReceiver):
    message = EmailMessage()
    message.set_content(alertMessage)
    message['subject'] = "Price Alerts"
    message['to'] = messageReceiver
    message['from'] = USERNAME
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.send_message(message)
    server.quit()

def scrapeScript():
    message = scrape(CSV_LOCATION)
    if '$' in message:
        alert(message, RECEIVER)
        print("Email Sent")

schedule.every().hour.do(scrapeScript)

while True:
    schedule.run_pending()
    time.sleep(1)

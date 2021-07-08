import csv
from functools import partial
import smtplib
from email.message import EmailMessage

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SwapTransition

from main import searchAmazon
from main import searchWalmart
from main import searchNovaTCG
from main import amazonPriceScrape
from main import walmartPriceScrape
from main import novatcgPriceScrape
from main import amazonNameScrape
from main import walmartNameScrape
from main import novatcgNameScrape
from main import addProduct

SEARCH_CSV_LOCATION = "C:\\Users\\Marshiie\\Pictures\\Senior Project\\searchList.csv"
CSV_LOCATION = "C:\\Users\\Marshiie\\Pictures\\Senior Project\\scrapeList.csv"
USERNAME = 'webscrapingalerts@gmail.com'
PASSWORD = 'vfezpfmvclyvsqxu'
RECEIVER = 'webscrapingdemo@gmail.com'

class windowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(windowManager, self).__init__(**kwargs)

class homeScreen(Screen):
    def __init__(self, **kwargs):
        super(homeScreen, self).__init__(**kwargs)
        self.add_widget(Label(text = "Choose a Website to Scrape", pos_hint = {'center_x': .5, 'y': .2}))
        self.amazonButton = Button(text = "Amazon", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'y': .5})
        self.add_widget(self.amazonButton)
        self.amazonButton.bind(on_press = self.transitionAmazon)
        self.walmartButton = Button(text = "Walmart", size_hint=(.45, .1), pos_hint = {'center_x': .5, 'y': .4})
        self.add_widget(self.walmartButton)
        self.walmartButton.bind(on_press = self.transitionWalmart)
        self.novatcgButton = Button(text = "Nova TCG", size_hint=(.45, .1), pos_hint = {'center_x': .5, 'y': .3})
        self.add_widget(self.novatcgButton)
        self.novatcgButton.bind(on_press = self.transitionNovaTCG)
        self.previousDataButton = Button(text = "Show last searched", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'y': .2})
        self.add_widget(self.previousDataButton)
        self.previousDataButton.bind(on_press = self.transitionData)
        self.emailWatchListButton = Button(text = "Email watch list", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'y': .1})
        self.add_widget(self.emailWatchListButton)
        self.emailWatchListButton.bind(on_press = self.transitionEmail)
    
    def transitionAmazon(self, *args):
        self.manager.current = 'amazon'

    def transitionWalmart(self, *args):
        self.manager.current = 'walmart'

    def transitionNovaTCG(self, *args):
        self.manager.current = 'novatcg'

    def transitionData(self, *args):
        self.manager.current = 'data'

    def transitionEmail(self,*args):
        self.manager.current = 'email'
        
class amazonScreen(Screen):
    def __init__(self, **kwargs):
        super(amazonScreen, self).__init__(**kwargs)
        self.add_widget(Label(text = "Amazon Search", pos_hint = {'center_x': .5, 'y': .2}))
        self.homeButton = Button(text = "Home", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'center_y': .1})
        self.searchButton = Button(text="Search", size_hint = (.45, .1), pos_hint={'center_x': .25, 'center_y': .4})
        self.clearButton = Button(text = "Clear", size_hint = (.45, .1), pos_hint = {'center_x': .75, 'center_y': .4})
        self.dataButton = Button(text = "Show Data", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'center_y': .25})
        self.item = TextInput(text = "", size_hint = (.8, .05), pos_hint = {'center_x': .5, 'center_y': .55})
        self.add_widget(self.homeButton)
        self.add_widget(self.searchButton)
        self.add_widget(self.clearButton)
        self.add_widget(self.dataButton)
        self.add_widget(self.item)
        self.homeButton.bind(on_press = self.transitionHome)
        self.searchButton.bind(on_press = self.amazonSearch)
        self.clearButton.bind(on_press = self.clear)
        self.dataButton.bind(on_press = self.transitionData)

    def transitionHome(self, *args):
        self.manager.current = 'home'

    def amazonSearch(self, obj):
        searchAmazon(self.item.text, SEARCH_CSV_LOCATION)

    def clear(self, *args):
        self.item.text = ""

    def transitionData(self, *args):
        self.manager.current = 'data'

class walmartScreen(Screen):
    def __init__(self, **kwargs):
        super(walmartScreen, self).__init__(**kwargs)
        self.add_widget(Label(text = "Walmart Search", pos_hint = {'center_x': .5, 'y': .2}))
        self.homeButton = Button(text="Home", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'center_y': .1})
        self.searchButton = Button(text="Search", size_hint=(.45, .1), pos_hint = {'center_x': .25, 'center_y': .4})
        self.clearButton = Button(text="Clear", size_hint = (.45, .1), pos_hint = {'center_x': .75, 'center_y': .4})
        self.dataButton = Button(text="Show Data", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'center_y': .25})
        self.item = TextInput(text="", size_hint = (.8, .05), pos_hint = {'center_x': .5, 'center_y': .55})
        self.add_widget(self.homeButton)
        self.add_widget(self.searchButton)
        self.add_widget(self.clearButton)
        self.add_widget(self.dataButton)
        self.add_widget(self.item)
        self.homeButton.bind(on_press = self.transitionHome)
        self.searchButton.bind(on_press = self.walmartSearch)
        self.clearButton.bind(on_press = self.clear)
        self.dataButton.bind(on_press = self.transitionData)

    def transitionHome(self, *args):
        self.manager.current = 'home'

    def walmartSearch(self, obj):
        searchWalmart(self.item.text, SEARCH_CSV_LOCATION)

    def clear(self, *args):
        self.item.text = ""

    def transitionData(self, *args):
        self.manager.current = 'data'

class novatcgScreen(Screen):
    def __init__(self, **kwargs):
        super(novatcgScreen, self).__init__(**kwargs)
        self.add_widget(Label(text = "NovaTCG Search", pos_hint = {'center_x': .5, 'y': .2}))
        self.homeButton = Button(text="Home", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'center_y': .1})
        self.searchButton = Button(text="Search", size_hint=(.45, .1), pos_hint={'center_x': .25, 'center_y': .4})
        self.clearButton = Button(text="Clear", size_hint=(.45, .1), pos_hint={'center_x': .75, 'center_y': .4})
        self.dataButton = Button(text="Show Data", size_hint=(.45, .1), pos_hint={'center_x': .5, 'center_y': .25})
        self.item = TextInput(text="", size_hint=(.8, .05), pos_hint={'center_x': .5, 'center_y': .55})
        self.add_widget(self.homeButton)
        self.add_widget(self.searchButton)
        self.add_widget(self.clearButton)
        self.add_widget(self.dataButton)
        self.add_widget(self.item)
        self.homeButton.bind(on_press = self.transitionHome)
        self.searchButton.bind(on_press = self.novatcgSearch)
        self.clearButton.bind(on_press = self.clear)
        self.dataButton.bind(on_press = self.transitionData)

    def transitionHome(self, *args):
        self.manager.current = 'home'

    def novatcgSearch(self, obj):
        searchNovaTCG(self.item.text, SEARCH_CSV_LOCATION)

    def clear(self, *args):
        self.item.text = ""

    def transitionData(self, *args):
        self.manager.current = 'data'

class dataScreen(Screen):
    def on_enter (self, *args):
        dataScreen.clear_widgets(self)
        self.add_widget(Label(text = "Data Screen", pos_hint = {'center_x': .5, 'center_y': .95}))
        self.homeButton = Button(text = "Home", size_hint = (.45, .1), pos_hint = {'center_x': .5, 'center_y': .05})
        self.add_widget(self.homeButton)
        self.homeButton.bind(on_press = self.transitionHome)
        self.dataScreenWork()

    def transitionHome(self, *args):
        self.manager.current = 'home'

    def dataScreenWork(self):
        y = .85
        z = .8
        self.urlList = []
        with open(SEARCH_CSV_LOCATION, newline="") as csvFile:
            reader = csv.reader(csvFile, delimiter=",")
            for rows in reader:
                url = rows[0]
                self.urlList.append(url)
                if 'amazon' in url:
                    name = amazonNameScrape(url)
                    price = amazonPriceScrape(url)
                elif 'walmart' in url:
                    name = walmartNameScrape(url)
                    price = "$" + walmartPriceScrape(url)
                elif 'novatcg' in url:
                    name = novatcgNameScrape(url)
                    price = novatcgPriceScrape(url)
                self.add_widget(Label(text = str(name) + ": " + str(price), pos_hint = {'center_x': .5, 'center_y': y}))
                y -= .15
        self.addButton1 = Button(text = "Add to Watchlist", size_hint = (.18, .05),
                            pos_hint = {'center_x': .5, 'center_y': .8})
        self.add_widget(self.addButton1)
        self.addButton1.bind(on_press = partial(self.productAdd, count = 0))
        self.addButton2 = Button(text = "Add to Watchlist", size_hint = (.18, .05),
                                 pos_hint = {'center_x': .5, 'center_y': .65})
        self.add_widget(self.addButton2)
        self.addButton2.bind(on_press = partial(self.productAdd, count = 1))
        self.addButton3 = Button(text = "Add to Watchlist", size_hint = (.18, .05),
                                 pos_hint = {'center_x': .5, 'center_y': .5})
        self.add_widget(self.addButton3)
        self.addButton3.bind(on_press = partial(self.productAdd, count = 2))
        self.addButton4 = Button(text = "Add to Watchlist", size_hint = (.18, .05),
                                 pos_hint = {'center_x': .5, 'center_y': .35})
        self.add_widget(self.addButton4)
        self.addButton4.bind(on_press = partial(self.productAdd, count = 3))
        self.addButton5 = Button(text = "Add to Watchlist", size_hint = (.18, .05),
                                 pos_hint = {'center_x': .5, 'center_y': .2})
        self.add_widget(self.addButton5)
        self.addButton5.bind(on_press = partial(self.productAdd, count = 4))

    def productAdd(self, *args, count):
        url = self.urlList[count]
        if 'amazon' in url:
            price = amazonPriceScrape(url)
            addProduct(url, price, CSV_LOCATION)
        elif 'walmart' in url:
            price = "$" + walmartPriceScrape(url)
            addProduct(url, price, CSV_LOCATION)
        elif 'novatcg' in url:
            price = novatcgPriceScrape(url)
            addProduct(url, price, CSV_LOCATION)

class emailScreen(Screen):
    def on_enter(self, *args):
        self.add_widget(Label(text = "Email Sent", pos_hint = {'center_x': .5, 'y': .2}))
        self.homeButton = Button(text="Home", size_hint=(.45, .1), pos_hint={'center_x': .5, 'center_y': .1})
        self.add_widget(self.homeButton)
        self.homeButton.bind(on_press = self.transitionHome)
        self.sendEmail()

    def transitionHome(self, *args):
        self.manager.current = 'home'

    def sendEmail(self, *args):
        watchListMessage = "Your current watch list\n\n"
        with open(CSV_LOCATION, newline="") as csvFile:
            reader = csv.reader(csvFile, delimiter=",")
            for rows in reader:
                url = rows[0]
                watchListMessage = watchListMessage + url + "\n"
        message = EmailMessage()
        message.set_content(watchListMessage)
        message['subject'] = "Price Alerts"
        message['to'] = RECEIVER
        message['from'] = USERNAME
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.send_message(message)
        server.quit()

class webScrapeApp(App):
    def build(self):
        screenManager = windowManager(transition = SwapTransition())
        screenManager.add_widget(homeScreen(name = 'home'))
        screenManager.add_widget(amazonScreen(name = 'amazon'))
        screenManager.add_widget(walmartScreen(name = 'walmart'))
        screenManager.add_widget(novatcgScreen(name = 'novatcg'))
        screenManager.add_widget(dataScreen(name = 'data'))
        screenManager.add_widget(emailScreen(name = 'email'))
        return screenManager

webScrapeApp().run()

__author__ = 'Andriy.Malaman'



from bs4 import BeautifulSoup
#import urllib.request
#import psycopg2
from selenium import webdriver
from datetime import date


class AutoRiaDict(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["category_id"] = "1"  #cars = 1; trucks 2
        self["chooseTypeSearchAuto"] = "oldAutos"
        self["countpage"] = "100" #number of sear results per page
        self["bodystyle"] = "0" #0 - any, 3 - sedan, 5 - crossover, 8 - minivan, 4 - hatchback, 2 - wagon, 7 - cabriolet, 9 - pickup, 6 - kupe
        self['raceFrom'] = "" #thousands of kilometers
        self["raceTo"] = ""   #thousands of kilometers
        self["engineVolumeFrom"] = ""   #should be integer values
        self["engineVolumeTo"] = ""     #should be integer values
        self["fuelRatesType"] = "0" #0 - any, 1 - Benzin, 2 - Diesel, 3 - Gas
        self["marka"] = "0"
        self["model"] = "0"
        self["s_yers"] = "0"
        self["po_yers"] = "0"
        self["gearbox"] = "0" #0 - any; -1 - all automatic; 1 - mechanic; 2 - automatic; 3 - tiptronic; 4 - adaptive; 5- variator;
        self["auto_repairs"] = "2" #0 - any; 1 - car for repairs; 2 - car can go

def get_url_for_ria(params):
    """
    Builds URL for auto.ria.com based on parameters in dictionary params
    return string with correct URL
    """
    return "http://auto.ria.com/?target=search&event=big&"+"&".join(["%s=%s" % (k,v) for (k,v)in params.items()])


def get_all_prices_per_page_usd(pr_results):
    """
     gets all prices per page in USD
     return lst with numeric values
    """
    lst = []
    for soup in pr_results:
        try:
            if soup.find(class_="price").find(class_="green"):
                lst.append(int(soup.find(class_="price").find(class_="green").get_text().replace(" ","")))
        except:
            print ("Error in get_all_prices_per_page_usd. Parse text:"+ soup.find(class_="price").find(class_="green").get_text().replace(" ","") )
    return lst

def get_car_age(to_year):
    """ return car age based on current year and produce year"""
    car_age = 0
    if  date.today().year > to_year:
        car_age = date.today().year - to_year
    return car_age

def findAveragePrice(lst):
    """
    @parsm lst : list; contains all values
    function return average value for values in list
    """
    price = 0
    try:
        price = int(sum(lst)/len(lst))
    except:
        print ("Error in findAveragePrice")
    return price

def cut_search_results_from_page(soup):
    """
    function receives whole page source and cut from page source section, which correlate
    to search allResults
    returns beautiful soup object which contain search results section
    """
    n_results= soup.find(id="search_auto_results")
    if n_results:
        return n_results.find_all(class_="definition-data")

def get_all_prices_for_all_rates_usd(p_car):
    """
    pcar - is instance of AutoRiaDict class
    returns all prices for particular pCar params within allowedRace (allowed Race = car_age*30)
    """

    car_age = get_car_age(int(p_car["po_yers"]))
    dct = {}
    for i in range(1,car_age*3):
        #define start milleage and finish milleage
        p_car["raceFrom"] = str(i*10)
        p_car["raceTo"] = str((i+1)*10)

        #execute search and get page source
        driver = webdriver.PhantomJS('/usr/bin/phantomjs/bin/phantomjs')
        webdriver.DesiredCapabilities.FIREFOX.copy()
        try:
            driver.get(get_url_for_ria(p_car))
            p_url = driver.page_source
            driver.close()
            #get search results from page source
            soup = BeautifulSoup(p_url,"html")
            pr_results = cut_search_results_from_page(soup)

            #writes average price in dictionary. Dictionary format key = millage finish, value = average price
            if pr_results:
                dct[i+1]= findAveragePrice(get_all_prices_per_page_usd(pr_results))
            else:
                dct[i+1] = 0
        except:
            print ("Error in get_all_prices_for_all_rates_usd %s" %(i+1))
    return dct







if __name__ == "__main__":
    p = AutoRiaDict()
    p["mark"]="70"
    p["model"]="649"
    p["s_yers"] = '2010'
    p["po_yers"] = '2010'


    driver = webdriver.PhantomJS('/usr/bin/phantomjs/bin/phantomjs')
    webdriver.DesiredCapabilities.FIREFOX.copy()
    driver.get(get_url_for_ria(p))
    p_url = driver.page_source
    driver.close()
    #get search results from page source
    soup = BeautifulSoup(p_url,"html")
    pr_results = cut_search_results_from_page(soup)
    print(get_all_prices_per_page_usd(pr_results))



__author__ = 'Andriy.Malaman'


from bs4 import BeautifulSoup
import urllib.request
import psycopg2
from selenium import webdriver
from datetime import date

class RstDict(dict):
    """
    class defines parameters of url for rst.ua
    """
    def __init__(self):
        self["marka"] = ""
        self["model"] = ""
        self["year"] = ["0","0"]  #years[]=<integer>&years[]=<integer>
        self["engine"]=["0","0"]   #should be integer values in square sm. Example "engine[]=1400&engine[]=1400"
        self["condition"] = 1 # 0 - all condition, 1 - good condition, 2 - normal condition
        self["gear"] = "0" #"0" - any; "2,3,4,5" - mechanic; "1,6,7,8,9" - automatic
        self["fuel"] = "0" #0 - any, "1,3" - benzin, 2 - diesel, 3 - gas/diesel
        self["results"] = 4 #quantity of results per search. (x*10) 4 means 40 results per search

def get_url_for_rst(params):
    """
    Builds URL for rst.ua based on parameters in dictionary params
    return string with correct URL
    """
    fURL= "http://rst.ua/oldcars/%(marka)s/%(model)s/?" % params
    for (k,v) in params.items():
        if k == "marka" or k == "model":
            pass
        else:
            # if value is list then add to URL following &<k>[]=v0&<k>[]=v1
            if isinstance(v,list):
                fURL = fURL+"&%s[]=%s&%s[]=%s" % (k,v[0],k,v[1])
            else:
                fURL = fURL+"&%s=%s" % (k,v)
    return fURL



def get_all_prices_per_page_usd(pr_results):
    """
    pr_results - is a BeautifulSoup tag
    gets all prices per page in USD
    return list of the integer prices in USD
    """
    def _strip_symbols_from_price (price):
        """
        price is (str)
        strips all non numerial symbols from price
        return integer if  stripped str is number or 0 if stripped str contain another symbols
        """
        bad_chars = "($')"
        for c in bad_chars:
            price = price.replace(c, "")
        if price.isalnum():
            return int(price)
        else:
            return 0

    all_tags = pr_results.find_all(class_="rst-ocb-i-d")
    lst = []
    for tag in all_tags:
        try:
            if tag.find(class_="rst-uix-grey"):
                lst.append(_strip_symbols_from_price(tag.find(class_="rst-uix-grey").get_text()))
        except:
            print("Error in get_all_prices_per_page_usd. Parse text:" + tag.find(class_="rst-uix-grey").get_text())
    return lst


if __name__ == "__main__":
    p = RstDict()
    p["marka"] = "Skoda"
    p["model"] = "Fabia"
    p["year"] = ["2008","2008"]
    p["fuel"] = "1,3"
    p["engine"] = ["1200","1600"]

    driver = webdriver.PhantomJS('/usr/bin/phantomjs/bin/phantomjs')
    webdriver.DesiredCapabilities.FIREFOX.copy()

    driver.get((get_url_for_rst(p)))
    pURL = driver.page_source
    soup = BeautifulSoup(pURL,"html")
    print(get_all_prices_per_page_usd(soup))




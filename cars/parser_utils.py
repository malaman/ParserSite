from pip.commands.search import print_results

__author__ = 'andrew'

from bs4 import BeautifulSoup
from selenium import webdriver


class AutoRiaDict(dict):
    """Defines unique identifiers of car with key:value pairs in auto.ria.com database.
    """


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
        self["model"] = "0"  #model in autoriadb = series in parser db
        self["s_yers"] = "0"
        self["po_yers"] = "0"
        self["gearbox"] = "0" #0 - any; -1 - all automatic; 1 - mechanic; 2 - automatic; 3 - tiptronic; 4 - adaptive; 5- variator;
        self["auto_repairs"] = "2" #0 - any; 1 - car for repairs; 2 - car can go


def get_url_for_ria(p_dict):
    """Returns URL of auto.ria.com. URL contains params of searched car.

    Args:
    p_dict - type: dictionary. Contains key-value pairs for crafting correct url

    Returns:
    Builds URL for auto.ria.com based on parameters in dictionary params
    return string with correct URL
    """
    return "http://auto.ria.com/?target=search&event=big&"+"&".join(["%s=%s" % (k,v) for (k,v)in p_dict.items()])

def get_page_source_from_auto_ria(p_dict):
    """Gets page source from auto.ria.com, which contains search results for particular car.

    Args:
        p_dict: A AutoRiaDict class instance. Contains unique identifier of car with auto.ria.com db params.

    Returns:
        bs4 object instance. Contains rendered HTML with search results.
    """
    driver = webdriver.PhantomJS('/usr/bin/phantomjs/bin/phantomjs')
    webdriver.DesiredCapabilities.FIREFOX.copy()
    driver.get(get_url_for_ria(p_dict))
    p_url = driver.page_source
    driver.close()
    return BeautifulSoup(p_url,"html").find(id="search_auto_results")



def get_all_prices_per_page_usd(p_dict):
    """Gets all prices per page

    Args::
        p_dict: A AutoRiaDict class instance. Contains unique identifier of car with auto.ria.com db params.

    Returns:
        lst: type list. Return list of prices in USD. If no prices found of page returns empty list.
    """

    soup = get_page_source_from_auto_ria(p_dict)
    pr_results = soup.find_all(class_="definition-data")
    lst = []
    for soup in pr_results:
        try:
            if soup.find(class_="price").find(class_="green"):
                lst.append(int(soup.find(class_="price").find(class_="green").get_text().replace(" ","")))
        except:
            print ("Error in get_all_prices_per_page_usd. Parse text:"+ soup.find(class_="price").find(class_="green").get_text().replace(" ","") )
    return lst

def get_auto_ria_info(p_dict):
    """Gets info about car from auto.ria.com

    Args:
        p_dict: A AutoRiaDict class instance. Contains unique identifier of car with auto.ria.com db params.

    Returns:
        lst : list of lists, containing information about car.
        Following information is returned.

        Name             |  Race        | Price  |Paid | Fuel        |  Gear       | City     | URL
        Skoda Fabia 2006 |   96 тыс.км. | 8 500  | Yes |  Бензин 1.6 |  Типтроник  |  Одесса  |

    """
    soup = get_page_source_from_auto_ria(p_dict)
    soup = soup.find_all(class_ = "ticket-item paid") + soup.find_all(class_ = "ticket-item")
    lst = []

    for item in soup:
        dict = {}

        item = item.find(class_='content-bar')
        dict['city'] = item.find(class_='head-ticket').find('a').get_text()
        dict['url'] = 'http://auto.ria.com' + item.find('a').get('href')

        item.find("h3").get_text().replace("\n", "").replace("\xa0", "").strip(" ")
        dict['name'] = item.find("h3").get_text().replace("\n", "").replace("\xa0", "").strip(" ")

        definition_item = item.find(class_='definition-data')
        try:
            dict['price'] = definition_item.find(class_='green').get_text()
        except:
            pass

        dict['race'] = definition_item.find(title='Пробег').get_text().replace("\n", "").replace("\xa0", "").strip(" ")
        dict['fuel'] = definition_item.find(title='Тип топлива').get_text().replace("\n", "").replace("\xa0", "").strip(" ")
        dict['gear'] = definition_item.find(title='Тип коробки передач').get_text().replace("\n", "").replace("\xa0", "").strip(" ")










        lst.append(dict)


    return lst



if __name__ == '__main__':
    p = AutoRiaDict()
    p["mark"]="70"
    p["model"]="649"
    p["s_yers"] = '2010'
    p["po_yers"] = '2010'
    print(get_auto_ria_info(p))


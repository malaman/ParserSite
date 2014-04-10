__author__ = 'Andriy.Malaman'

import unittest
import auto_ria_parser
import psycopg2
import urllib.request
from bs4 import BeautifulSoup
import os


def connect_to_url():
    """Read HTML content from http://auto.ria.com"""
    return urllib.request.urlopen("http://auto.ria.com")

def connect_to_db():
    """Connects to the database"""
    return psycopg2.connect(host="localhost",dbname="parserdb",user="dbuser",password="BangBig",port="5432")

class ConnectionTest(unittest.TestCase):
    def testConnectionToURL(self):
        """
        Tests connection to the auto.ria.com site
        """
        try:
            connect_to_url()
            connect_to_url().close()
        except:
            raise (Exception, "Unable to connect to URL")


    def testConnetiontoDB(self):
        """
        Tests connection to the database
        """
        try:
            connect_to_db()
            connect_to_db().close()
        except:
            raise (Exception, "Unable to connect to DB")

class ParserTest(unittest.TestCase):

    def test_get_all_prices_per_page_usd(self):
        """
        Tests functions auto_ria_parser.get_all_prices_per_page_usd and
        auto_ria_parser.cut_search_results_from_page

        input argument for function is locally stored html file
        if function prints some list of values, then test is passed
        """

        f = open(os.path.join(os.path.dirname(__file__), './add/auto_ria_parser_test/SkodaOctaviaSearchHTML.html'), "rb")
        soup = BeautifulSoup(f,"html")
        nResults = auto_ria_parser.cut_search_results_from_page(soup)
        res = auto_ria_parser.get_all_prices_per_page_usd(nResults)
        if res:
            print(res)
        else:
            raise (Exception,"Failure in test_get_all_prices_per_page_usd")


if __name__ == "__main__":
    unittest.main()





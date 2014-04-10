__author__ = 'Andriy.Malaman'

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from bs4 import BeautifulSoup
import urllib.request
import psycopg2
from selenium import webdriver
from datetime import date
import json

from cars.models import CarMarks, CarSeries




def strip_symbols_num (num):
        """
        @param: num - string, which contain additional symbols
        strips all non numerial symbols from num
        return integer if  stripped str is number or 0 if stripped str contain another symbols
        """
        bad_chars = "($') "
        for c in bad_chars:
            num = num.replace(c, "")
        if num.isalnum():
            return int(num)
        else:
            return 0

def get_car_models (soup):
    """
    input argument (soup) - beautiful soup tag; contains page source of main page of auto.ria.com
    returns dictionary with key = 'car model name' and value = car model id in auto ria datbase
    """
    def _clean_car_name (car):
        """
        input argument car - str; contains car name
        param car:
        """
        start = car.find("(")
        return car[:start-1]

    d = {}
    for tag in soup.find(id="select_auto_used_marka").find_all("option"):
        d[_clean_car_name(tag.get_text())] = tag.get("value")
    return d


def write_marks_to_db(d):
    """
    function writes marks to pr_car_mark table
    @param d: - dictionary; contains <mark>:<id_car_mark_auto_ria> pairs
    """
    try:
        # connects to the database
        conn = psycopg2.connect(host="localhost",dbname="parserdb",user="dbuser",password="dbuser",port="5432")
        cur = conn.cursor()
        #writes data to the pr_car_mark table
        for (k,v) in d.items():
            sql = "INSERT INTO pr_car_marks(id_car_mark, name, id_car_mark_auto_ria) values (nextval('id_car_mark_sequence')," \
                  "%s, %s);"
            data = (k,v)
            try:
                cur.execute(sql,data)
                conn.commit()
            except:
                print ("Unable to write to the database %s:%s)" % (k,v))
    except:
        print ("Unable to connect to the database parserdb")
    finally:
        cur.close()
        conn.close()


def get_car_series (json_data):
    """
    Function parses html page in order to get all series of specific mark.
    For example for Skoda (mark) function returns ['Fabia', 'Octavia', 'Yetti',...] list

    @param json_data:json_data received from auto.ria.com
    @return:list of series, each value is string
    """
    dct = {}
    try:
        lst = json.loads(json_data)['modelArr']
        for item in lst:
            dct[item['model_id']] = item['name']
    except:
        print ("Error in get_car_series. Unable to parse json data")
    return dct


def get_ajax_for_car_series(mark):
    """

    @param mark: string; id of the ato mark
    @return: string url for getting ajax information for series
    """
    return "http://auto.ria.com/ajax.php?target=auto&event=load_subcategory&lang_id=1&marka_id="+mark


def write_car_series_to_db_old(car_mark,d):
    """
    functions writes car series to the database
    @param d:{} dictionary; contains <car series>:id_car_series_auto_ria pairs
    @param car_mark: string; contains name of car mark
    """
        # connects to the database
    try:
        conn = psycopg2.connect(host="localhost",dbname="parserdb",user="dbuser",password="dbuser",port="5432")
        cur = conn.cursor()
        try:
            #gets id_car_mark and id_car_mark_auto_riafrom pr_car_marks table based on car name string
            sql = "select (id_car_mark,id_car_mark_auto_ria) from pr_car_marks where name = %s"
            data = (car_mark,)
            cur.execute(sql,data)
            res = cur.fetchone()
            [id_car_mark,id_car_mark_auto_ria] = res[0].split(',')

            try:
                #write into pr_car_series table
                for k,v in d.items():
                    sql = "insert into pr_car_series values (nextval('id_series_sequence'),%s, %s, 1, %s,%s)"
                    data = (v,                                          #name
                            strip_symbols_num(id_car_mark),             #id_car_mark
                            strip_symbols_num(id_car_mark_auto_ria),    # id_car_mark_auto_ria
                            k)                                          #id_series_auto_ria
                    cur.execute(sql,data)
                    conn.commit()
            except:
                print ("Unable to write to the database. Table pr_car_series. Values: %s:%s " % (k,v))
        except:
            print ("Unable to find id_car_mark or id_car_mark_auto_ria for : "+ car_mark)

    except:
        print ("Unable to connect to the database parserdb")
    finally:
        cur.close()
        conn.close()



def write_car_series_to_db (car_mark_name):
    """Writes all car series for one car mark to the database

    Keyword arguments:
    car_mark_name - string. Name of the car mark (for example: "Skoda")

    """
    mark = CarMarks.objects.get(name = car_mark_name)
    if mark:
        auto_ria_url = get_ajax_for_car_series(str(mark.auto_ria_id))
        r = urllib.request.urlopen(auto_ria_url).read()
        series_dict = get_car_series (r.decode())
        for k,v in series_dict.items():
            mark.carseries_set.create(name = v,series_auto_ria_id = int(k))


if __name__ == "__main__":
    pass








import re
import csv
from re import sub
import itertools
from centris import write_to_csv
import pandas as pd
import sys
import numpy as np

def get_houses(file_path):
    current_year = 2020
    p = "first/%s.csv"%(file_path)
    house_list = pd.read_csv(p, keep_default_na=False, header = 0 )
    house_list['price'].replace('', np.nan, inplace=True)
    house_list.dropna(subset = ["small region", "bedroom", "price"], inplace=True)
    house_list = house_list.astype({"price": 'int32'})
    house_list = house_list.astype({"year_built": 'str'})
    house_list["year_built"]=house_list["year_built"].replace(to_replace=r"^Unknown age.*$", value="1800", regex=True)
    pat = r"(?P<one>\d+), Being converted"
    repl = lambda m: m.group('one')
    house_list["year_built"]=house_list["year_built"].str.replace(pat, repl)
    pat2 = r"(?P<one>\d+), Century"
    house_list["year_built"]=house_list["year_built"].str.replace(pat2, repl)
    house_list["year_built"]=house_list["year_built"].replace("", "1800")
    house_list = house_list.astype({"year_built" : 'int32'})

    conditions = [
        (house_list['year_built'] >= (2020-5)),
        (house_list['year_built'] < (2020-5)) & (house_list['year_built'] >= (2020-10)),
        (house_list['year_built'] < (2020-10)) & (house_list['year_built'] >= (2020-20)),
        (house_list['year_built'] < (2020-20)) & (house_list['year_built'] >= (2020-30)),
        (house_list['year_built'] < (2020-30)),
    ]
    choices = ['5 less', '10 less', '20 less', '30 less', '30 more']
    house_list['year'] = np.select(conditions, choices, default='unknown')
    return house_list




if __name__=="__main__":
    input_file = sys.argv[1] 
    houses = get_houses(input_file)
    houses.groupby(["small region","bedroom","year"]).agg(avg_price = ("price","mean"), 
                                                   total = ("price","count")).to_csv('second/%s_summary.csv'%(input_file))

import re
import csv
from re import sub
import itertools
from geopy.geocoders import Nominatim
from centris import write_to_csv
import pandas as pd
import sys
import time


def get_house_list(file_path):
    p = "%s.csv"%(file_path)
    house_list = pd.read_csv(p, keep_default_na=False)
    return house_list.values

def get_previous_count(file_path, batch):
    p = "%s.csv"%(file_path)
    try:
        house_list = pd.read_csv(p, keep_default_na=False)
        return int((len(house_list.values))/batch)
    except:
        return 0


def get_row(row, region, city):
    pattern = re.compile(r"^(\D*)(\d+)(.*)")
    house = {}
    rooms = []
    beroom = []
    baroom = []
    poroom = []
    geo_string = None
    house["centris_no"] = row[0]
    house["property_type"] = row[1]
    house["price"] = sub(r"[^\d.]", "", row[2])
    lower_s = str(row[-4]).lower()
    if lower_s.find("new") >= 0:
        house["year_built"] = 2020
    elif lower_s.find("histo") >= 0:
        house["year_built"] = 1980
    else:
        house["year_built"] = row[-4]
    lot = pattern.match(row[-3])
    if lot is not None:
        house["lot_area"] = lot.group(2)
    else:
        house["lot_area"] = 0

    net = pattern.match(row[-2])
    if net is not None:
        house["net_area"] = net.group(2)
    else:
        house["net_area"] = 0

    # Regions
    """
    geo_string = row[5].strip("Lat:").replace("Lon:", "")
    location = geolocator.geocode(geo_string)
    if location:
        region_list = location.address.split(",")
    else:
        print(row)
        region_list = ["", "", "", ""]
    """
    house["small region"] = region
    house["big region"] = city

    bedroom = re.match(r"^(\D*)(\d+)\s*bedroom(.*)", row[6])
    if bedroom is not None:
        house["bedroom"] = bedroom.group(2)
    else:
        house["bedroom"] = -1

    bathroom = re.match(r"^(\D*)(\d+)\s*bathroom(.*)", row[7])
    if bathroom is not None:
        house["bathroom"] = bathroom.group(2)
    else:
        house["bathroom"] = -1

    house["listing_hyperlink"] = row[-1]
    return house


def main():
    file_p = sys.argv[1] 
    region = sys.argv[2] 
    print(region)
    city = sys.argv[3] 
    date = sys.argv[4] 
    file_path = "first/%s_"%(date) + file_p
    house_list = get_house_list("raw/%s"%(file_p))
    #geolocator = Nominatim(user_agent="realestate_research")
    batch_house_list = [get_row(row, region, city) for row in house_list]
    write_to_csv(batch_house_list, file_path)


if __name__ == "__main__":
    main()

import datetime
import random
from django.core.management.base import BaseCommand
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Sum, Avg
from core.models import User, UserManager, PropertyMaster, Property_TypeMaster, TypeMaster, AvgMaster
import csv
import requests
import schedule
import time
# Scrapper
import requests
import csv
import time
import pdb
import operator
import  csv
from django.db.models import F
import random
import re
import pandas as pd

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.job3()

    def job3(self):
        status_dict = {1: "Active", 2: "Under Contract", 3: "Off Market", 4: "Sold"}
        df = pd.read_csv('zipcodedata.csv')

        zipcodelist = df['zip'].tolist()
        # print(zipcodelist)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }
        try:
            print("Start")
            for zip in zipcodelist:
                print("Inside For Loop")
                # zip=zip[1]
                print("Zip", zip)
                if len(str(zip)) == 4:
                    zip = "0" + str(zip)
                n = 0
                url = "https://www.landwatch.com/api/property/search/1113/zip-" + \
                      str(zip) + "/land/off-market/sold"
                page = 0
                # print(url)
                page = requests.get(url, headers=headers)
                print(page)
                # time.sleep(random.randrange(1, 2))
                while (page == 0):
                    page = requests.get(url, headers=headers)
                    time.sleep(random.randrange(1, 5))
                try:

                    data = page.json()

                    countListing = data['searchResults']['locationSeo']['pageHeaderCount']
                    countListing = re.findall(r'\d+', countListing)
                    if len(countListing) == 3:
                        page_count = int(int(countListing[2]) / 25 + 2)
                    else:
                        page_count = 2
                    # print(countListing)

                    for i in range(1, page_count):
                        url = "https://www.landwatch.com/api/property/search/1113/zip-" + \
                              str(zip) + "/land/off-market/sold/page-" + str(i)
                        # print(url)
                        page = 0
                        page = requests.get(url, headers=headers)
                        # time.sleep(random.randrange(1, 2))
                        while (page == 0):
                            page = requests.get(url, headers=headers)
                            time.sleep(random.randrange(1, 5))
                        data = page.json()
                        for row in PropertyMaster.objects.all().reverse():
                            # print("AJ")
                            if PropertyMaster.objects.filter(lwPropertyId=row.lwPropertyId).count() > 1:
                                if PropertyMaster.objects.filter(accountId=row.accountId, acres=row.acres,
                                                                 adTargetingCountyId=row.adTargetingCountyId,
                                                                 address=row.address, baths=row.baths,
                                                                 beds=row.beds, brokerCompany=row.brokerCompany,
                                                                 brokerName=row['brokerName'],
                                                                 Url="https://www.landwatch.com" + row.canonicalUrl,
                                                                 city=row.city,
                                                                 cityID=row.cityID,
                                                                 companyLogoDocumentId=row.companyLogoDocumentId,
                                                                 county=row['county'], countyId=row.countyId,
                                                                 description=row.description,
                                                                 hasHouse=row.hasHouse,
                                                                 hasVideo=row.hasVideo,
                                                                 hasVirtualTour=row.hasVirtualTour,
                                                                 imageCount=row.imageCount, zip=row.zip,
                                                                 imageAltTextDisplay=row.imageAltTextDisplay,
                                                                 isHeadlineAd=row.isHeadlineAd,
                                                                 types=' '.join(row.types),
                                                                 isALC=row.isALC,
                                                                 latitude=row.latitude, state=row.state,
                                                                 longitude=row.longitude, price=row.price,
                                                                 status=status_dict[row.status],
                                                                 Rate=int(row.price / row.acres),
                                                                 ).exists():
                                    row.delete()
                                    print("Good Bye")
                                else:
                                    PropertyMaster.objects.filter(lwPropertyId=row.lwPropertyId).update(
                                        updated_at=datetime.date.today())
                        # print("Length of data : ",len(data))
                        for item in data['searchResults']['propertyResults']:
                            prop = PropertyMaster.objects.create(accountId=item['accountId'], acres=item['acres'],
                                                                 adTargetingCountyId=item['adTargetingCountyId'],
                                                                 address=item['address'], baths=item['baths'],
                                                                 beds=item['beds'], brokerCompany=item['brokerCompany'],
                                                                 brokerName=item['brokerName'],
                                                                 Url="https://www.landwatch.com" + item['canonicalUrl'],
                                                                 city=item['city'],
                                                                 cityID=item['cityID'],
                                                                 companyLogoDocumentId=item['companyLogoDocumentId'],
                                                                 county=item['county'], countyId=item['countyId'],
                                                                 description=item['description'],
                                                                 hasHouse=item['hasHouse'],
                                                                 hasVideo=item['hasVideo'],
                                                                 hasVirtualTour=item['hasVirtualTour'],
                                                                 imageCount=item['imageCount'], zip=item['zip'],
                                                                 imageAltTextDisplay=item['imageAltTextDisplay'],
                                                                 isHeadlineAd=item['isHeadlineAd'],
                                                                 types=' '.join(item['types']),
                                                                 lwPropertyId=item['lwPropertyId'], isALC=item['isALC'],
                                                                 latitude=item['latitude'], state=item['state'],
                                                                 longitude=item['longitude'], price=item['price'],
                                                                 status=status_dict[item["status"]],
                                                                 Rate=int(item['price'] / item['acres'])
                                                                 )

                except:

                    print("json exception")

        finally:
            zip_code_last = zip
            print("Completed")

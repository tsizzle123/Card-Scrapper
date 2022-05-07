'''
Created by Tariq McLeod on 2022-05-06, yyyy-mm-dd. 
The function of the Get_Average class currently is to return the average price of all items from eBay. 
To accomodate for fake items and bad sellers, there is a 3 standard deviation filter in the get_outliers method. 
The whole class is working as expected, however there is an issue with the way ebay is returning the data.
They data will return 'similar' results to the data and cause it to skew. Using literals through double 
quotes requires exact matches and does not help much. This is being investigated. 

The next step of this project is to create a class that will loop through the data and return the average price of each item.

A future idea is to add historical data tracking to see if the average price has changed over time.
'''
from cmath import nan
import pandas as pd
from bs4 import BeautifulSoup
import requests
from statistics import mean
import numpy as np
from scipy import stats

cards = pd.read_csv('Example-Data.csv')

class Get_Average():

    def __init__(self,cards):
        print(1)
        self.name = cards['Name'].astype(str)
        self.grade = cards.Grade.astype(float)
        

    def build_link(self):
        print(5)
        if self.grade.values[0] == nan:
            link = 'https://www.ebay.com/sch/i.html?_dcat=183454&_fsrp=1&rt=nc&_from=R40&_nkw={name}+{number}&_sacat=0&LH_Sold=1&Grade={grade}'
            return(link.format(name=self.name,grade=self.grade))
        else:
            link = 'https://www.ebay.com/sch/i.html?_dcat=183454&_fsrp=1&rt=nc&_from=R40&_nkw={name}&_sacat=0&LH_Sold=1'
            return(link.format(name=self.name))
    
    def make_request(self):
        print(4)
        link = self.build_link()
        r = requests.get(link)
        content = r.content
        return BeautifulSoup(content, 'html.parser')

    def get_sales(self):
        print(3)
        soup = self.make_request()
        sales = []

        for x in soup.find_all(attrs={'class':'POSITIVE'}): 
            sales.append(x.text)
        sales = [s[1:] for s in sales]
        return pd.DataFrame(sales,columns=['Sale Price']).apply(pd.to_numeric, errors='coerce').dropna().astype(float)
    
    def clean_outliers(self):
        print(2)
        sales = self.get_sales()
        z = np.abs(stats.zscore(sales))
        #3 = 3 standard deviations
        sales = sales[(z < 3).all(axis = 1)]
        return round(sales['Sale Price'].mean(),2)




c = Get_Average(cards.head(1))

print(c.clean_outliers())

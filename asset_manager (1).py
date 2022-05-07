import pandas as pd
from bs4 import BeautifulSoup
import requests
from statistics import mean
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from http.cookies import SimpleCookie


#start of adding cookies and captcha handling to requests
def cookie_parser():
    cookie_string = 'zguid=23|%24ffb86bdb-c960-498d-9168-b6abd8583c43; _ga=GA1.2.1778297916.1616613571; zjs_anonymous_id=%22ffb86bdb-c960-498d-9168-b6abd8583c43%22; _pxvid=dca4342e-8cd5-11eb-94a4-0242ac120004; _gcl_au=1.1.1502668987.1616613574; _pin_unauth=dWlkPVlqWTFNR1UwWXpNdE5EWTRaUzAwTlRsakxXRXdOekV0T0dVM1pUTmlZakUxTkRZMQ; G_ENABLED_IDPS=google; g_state={"i_l":0}; userid=X|3|35390c8d25ee06d%7C3%7CH0Zcwue9PlivLhLfAGKYkodo_Mw_NAii52RsFLk-CWk%3D; loginmemento=1|277f3f7784580fcc1c60e58e774dc8c70eec653b515fbf35810e8b73e72f6c1d; zjs_user_id=%22X1-ZUw9yv06r96l1l_9hc6g%22; zgcus_lbut=; zgcus_lidid=51e0a8b2-8ce1-11eb-a486-d6d721165ced; zgcus_aeut=84597981; zgcus_ludi=51dcff2e-8ce1-11eb-a486-d6d721165ced-84597; __stripe_mid=93215736-1d4b-4bd4-8d28-6daba00f4312465e09; OptanonConsent=isIABGlobal=false&datestamp=Wed+Mar+24+2021+13%3A41%3A35+GMT-0700+(Pacific+Daylight+Time)&version=5.11.0&landingPath=https%3A%2F%2Fwww.zillow.com%2Frenter-hub%2Fapplications%2Flisting%2F50bpvw241fjee%2Frental-application%2F15732870612756924251616618239405%2Foverview%3FinviteId%3D16174132%26utm_source%3Demail%26utm_medium%3Demail%26utm_campaign%3Demo_rachelapplicationinvite_completebutton&groups=1%3A1%2C3%3A1%2C4%3A1; cdn.zillowinc.300524.ka.ck=34e0d35385cd661891520b93873024cb1b5f905e01b92a5934d6d5867401b3e4643e8be97e55f22636d16fe779b2d80101349f3fe20ed0733ef2f6649dbdab054b346c3b4c45943752329cf25a3056dabe402f5d9962602ebae52f2e5c77a658df146cd5e0a7f461ead1b6f1f4a21b4751bcbb81d1720f7ca09e6f8bb9622a10325224d48ea0096578f4989349d246d9ba8f84a2033a985974df7b; optimizelyEndUserId=oeu1617333871848r0.366737008495994; _gid=GA1.2.1182822503.1623280426; KruxPixel=true; __pdst=9cc8ca22eccb40e78b1a7eac19020f24; KruxAddition=true; JSESSIONID=515F8D4C316BA04C9803A134AB4C98B1; zgsession=1|659e8999-23d1-4ea0-930f-f7ea143bb839; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEr8H3dDZX3WqANxNhmrNSQAH9NOhyebWfVK%2FcWxkPlkMZDHah7KJLP7mdSEkgwR%2BNR3Q3TiUQkoY; DoubleClickSession=true; _derived_epik=dj0yJnU9Y1RiVWpLQVlGUzczOTF3UEdvUmRlb0dDbmVCdDJzbVYmbj1jRFJmaVYzRXRXLW9HR2hHMHZHTkd3Jm09NyZ0PUFBQUFBR0RDT3ZBJnJtPTQmcnQ9QUFBQUFHQm1pdk0; utag_main=v_id:017865ad87bd00090bc1b22faba103072005e06a00bd0$_sn:5$_se:1$_ss:1$_st:1623343608897$dc_visit:5$ses_id:1623341808897%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:ff28ceb0-8ca6-46b1-aa20-e6ffcb9086b8%3Bexp-session; _pxff_bsco=1; _gat=1; _px3=9e40fe43e1dbf3f12c7b47982d33ec593e0bce187255130589912418de45fe79:64Pa+mu6M1MmxC11iZRZScdyWffHvAQOZhv0GvMeDVN35ox1QvU7UOI2JwvkdoCygr3frWrs39TYqdkrLAmu/Q==:1000:CRjGI8zma48dJLrG+WkbjPTsjnF1ZptM1BYNge7heCIlMsuA7b7uPfZyUNA4gdchdRGJerEzdi1RdHxQhdTEYfoErrD0n5h1npFClwR50iF8RyGlXhFtbPTqgzuIqzIWkW7zt+K/XDC9He+IPlJtxin7jjVtKEkxuu196ZB5kgbTpOS4AUGcurbe8bhlfcG4JXqGZmSKtMoBu2hsF8UlWw==; _uetsid=57359b50c97811eb98c233e1892b4dbf; _uetvid=5735e310c97811eba386a5e6785af65c; AWSALB=IaT66b05VS6HBE3oOJoYWCDqFQ7Se3oDTE416xd9bqcNs19Ru54zWeoqfDGnHjghLrl8LAK+I79lqWT21OJBtQxzjzj3mgvnxbLA/XZ/2ZT2sxGOlK6JbBnYZB0F; AWSALBCORS=IaT66b05VS6HBE3oOJoYWCDqFQ7Se3oDTE416xd9bqcNs19Ru54zWeoqfDGnHjghLrl8LAK+I79lqWT21OJBtQxzjzj3mgvnxbLA/XZ/2ZT2sxGOlK6JbBnYZB0F; search=6|1625933980428%7Crect%3D48.43488333369821%252C-120.13156612535074%252C45.42759926911309%252C-126.55856807847574%26crid%3D656c360c14X1-CRim1warp14d4u_13ojyu%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26fs%3D0%26fr%3D0%26mmm%3D0%26rs%3D1%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%097153%09%09%09%09%09%09'
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key,morsel in cookie.items():
        cookies[key] = morsel.value
    
    return cookies
#Method takes in an excel file, then looks up the value on ebay 
def compute_stuff(self,name,number,grade):
    #Build the link
    self.name = name 
    #card number
    self.number = number
    self.grade = grade
    link = 'https://www.ebay.com/sch/i.html?_dcat=183454&_fsrp=1&rt=nc&_from=R40&_nkw={name}+{number}+{description1}&_sacat=0&LH_Sold=1&Grade={grade}'
    #BS on the link 
    r = requests.get(link)
    tester = r.content
    soup = BeautifulSoup(tester, "html.parser")


    
   #retrieve sales and store in a list
    sales = []
    for x in soup.find_all(attrs={'class':'POSITIVE'}): 
        sales.append(x.text)
    
    
    
    #Remove the'$'
    sales = [s[1:] for s in sales]

    #Convert to float
   
    sales = list(map(float, sales))
    
    #clean outliers
     
    
    df = pd.DataFrame(sales,columns=['Sales'])
    
    z = np.abs(stats.zscore(df))
    
    df = df[(z < 1).all(axis = 1)]
    

    #print average
    return(round((df['Sales'].sum())/len(df),2))
    



#Create and manipulate the dataframe with the asset spreadsheet
def data_intake(x):
    df = x
    df = pd.read_csv(x, encoding = "utf-8")
    #df = df.astype('str').dtypes
    df['Size'] = df['Size'].astype(str)
    shoe_input = df['Shoe']
    size_input = df['Size']
    print(compute_stuff(shoe_input.loc[1],size_input.loc[1]))
    df['Current Value'] = compute_stuff(df['Shoe'],df['Size'])
    


#print(data_intake(df))
    
x = input()
data_intake(x)

from bs4 import BeautifulSoup as BS
import urllib
import requests
import ast
import time
from fake_useragent import UserAgent
import datetime
import re
import secrets

write_file = 'retrieved.data.log.'+datetime.datetime.utcnow().isoformat()+'.txt'
crawl_log = 'alreadyCrawled.profileCodes.log.'+datetime.datetime.utcnow().isoformat()+'.txt'

print('the write file is : ' + write_file)

org_data = []
records = {}

def getOrgTableData(profileCode):

    url=secrets.url+str(profileCode)

    #create random user agent, based on typical contemporary data
    ua = UserAgent()
    random_ua = {'user-agent': str(ua.random)}

    f = requests.get(url, headers=random_ua)

    #print("Status Code: "+str(f.status_code)+" from "+url)

    if (f.status_code==requests.codes.ok):
        #log successful ID
        with open(crawl_log, 'a') as c_l:
            c_l.write(profileCode+'\n')

        #create BeautifulSoup object with html doc response
        soup = BS(f.text, 'html.parser')

        #find the specific table element containing the data we're after
        table = soup.findAll("table", { "class" : "zebraDivided" })

        for x in table:
            tablesoup=BS(str(x),'html.parser')

            #create dictionary key as organization name
            org_name = tablesoup.select('tr')[0].findChildren()[1].string
            records[org_name]={}

            #find org. info and link them as key value pairs to org. name key
            website=tablesoup.find('td',text=re.compile('Web site:'))
            if (website):
                records[org_name]["website"]=website.parent.findChildren()[1].string
            else:
                records[org_name]["website"]=None

            english_name=tablesoup.find('td',text=re.compile('English'))
            if (english_name):
                records[org_name]["(english_org_name)"]=english_name.parent.findChildren()[1].string
            else:
                records[org_name]["(english_org_name)"]=None

            phone = tablesoup.findAll('td',text=re.compile("Phone:"))
            if (phone):
                phone[:] = [x.parent.findChildren()[1].string for x in phone]
                records[org_name]["phone"]=phone[-1]
            else:
                records[org_name]["phone"]=None

            mailtos = tablesoup.select('a[href^=mailto]')
            mailtos[:] = [x.string for x in mailtos]
            if(mailtos):
                records[org_name]['email']=mailtos[-1]
            else:
                records[org_name]['email']=None

    #write records dictionary to file as it goes
    with open(write_file,'w') as f:
        f.write(str(records))


l=None

#read valid id codes into a list
with open("still_to_go2017-03-30T13:30:59.469647.txt", "r") as id_codes_file:
    codes_list = id_codes_file.read()
    l= ast.literal_eval(codes_list)

#loop through list, call gather data function on each,
#time delay for politeness to friendly servers
for profileCode in l:
    getOrgTableData(profileCode)
    time.sleep(1)

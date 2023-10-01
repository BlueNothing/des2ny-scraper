from requests_html import HTMLSession
import re
from bs4 import BeautifulSoup, SoupStrainer

#Project Goal:
#Initial -  Gather information from light.gg regarding items in Destiny 2.
#Second -  Store that information to a PostgreSQL database.
#Third - Provide a web endpoint to allow queries to the database.

#Weapons - Track their various properties (weapon properties, mod slot options, craftable, etc)

#Armor Pieces - Images? Record whether it's exotic, and if so, what it does.
#Armor (2) - Otherwise, not much to say. Maybe how it's found?

#Other - ???

itemsDict = {}

def first_page():
    
    session = HTMLSession()
    pNum = "1" #Start on the first page.
    for pNum in range(3):
        url = 'https://www.light.gg/db/all/?page=' + str(pNum)
        req = session.get(url) #GET to the first page of the database.
        req.html.render() #Get the JavaScript from light.gg to run so that the actual tables show up.
        with req as response:
            fp = response.content
            itemsPageHTML = SoupStrainer(class_=re.compile("item-row"))
            a_class = SoupStrainer("href")
            soup = BeautifulSoup(fp, features="lxml", parse_only=itemsPageHTML)
            print(soup.prettify())
            for link in soup.find_all('a'):
                if(len(link.get_text(strip=True)) != 0):
                    itemName = link.get_text()
                    pageName = link.get('href')
                    itemsDict[itemName] = pageName
                #print(link.get_text() + " : " + link.get('href'))
        #soup = BeautifulSoup(soup, features="lxml", parse_only=a_class)
        #soup = soup.html.find_all("href")
        #soup = soup.find_all('href')
        
        #Now, there's a formatted block of HTML containing a bunch of stuff that doesn't matter, and 50 entries that do matter.

        #print(soup.prettify()) #This is basically a debug-only line for now.
        #print(itemsDict["itemName"])
    print ("Length of dictionary: " + str(len(itemsDict)))
    #for i, k in enumerate(itemsDict):
    #      if i == 100: break
    #      print((itemsDict[k]))
        
        #for k, v in itemsDict.items():
            #print(k, v)
    print(itemsDict)


#def crupdate_table(table_code):
    #If the specified table doesn't exist or is null, create and populate it.
    #If the specified table exists and is not null, attempt to update it.

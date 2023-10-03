from requests_html import HTMLSession
import pprint
import re
from bs4 import BeautifulSoup, SoupStrainer
import mysql.connector

#Project Goal:
#Initial -  Gather information from light.gg regarding items in Destiny 2.
#Second -  Store that information to a PostgreSQL database.
#Third - Provide a web endpoint to allow queries to the database.

#Weapons - Track their various properties (weapon properties, mod slot options, craftable, etc)

#Armor Pieces - Images? Record whether it's exotic, and if so, what it does.
#Armor (2) - Otherwise, not much to say. Maybe how it's found?

#Other - ???

itemsDict = dict(itemName =  None, #What is the item called?
             pageName = None, #What's the URL for that item's page?
             itemRarity = None, #Is it an exotic?
             itemCategory = None, #Is it a weapon, armor, or something else?
             itemSlot = None, #Armor - Is it a head slot piece or a leg piece? Weapon - Is it a Kinetic Slot, Energy Slot, or Heavy Slot Weapon?
             itemType = None, #Is this weapon a sword? Is this armor a helmet?
             itemClass = None) #Is this item locked to a given class?

def scrape():
    #pwd = input("Please enter the password for your database's root user.") - Avoid hardcoding passwords!
    #conn = mysql.connector.connect(host='localhost', database='des2ny', user='root', password=pwd)
    #print(conn) - Confirms connection.
    
    session = HTMLSession()
    pNum = 1 #Start on the first page.
    printSample = False
    for pNum in range(1): #About 500 pages should suffice for the endgame, but for now, let's keep it to 5 for proof-of-concept.
        url = 'https://www.light.gg/db/all/?page=' + str(pNum)
        req = session.get(url) #GET to the first page of the database.
        req.html.render() #Get the JavaScript from light.gg to run so that the actual tables show up.
        with req as response:
            fp = response.content
            itemsPageHTML = SoupStrainer(class_=re.compile("item-name"))
            a_class = SoupStrainer("href")
            soup = BeautifulSoup(fp, features="lxml", parse_only=itemsPageHTML) #Get the webpage, reduce it to just the entries that matter. We'll populate their properties from their individual pages.
            print(soup.prettify()) #Keeping this for later testing where relevant.
            souprows = soup.find_all(class_=re.compile("item-name"))
            itemName = "Null"
            pageName = "Null"
            itemClass = "Null"
            itemRarity = "Null"
            itemSlot = "Null"
            itemType = "Null"
            for souprow in souprows:
                print("START OF ITEM")
                print (souprow)
                print("{ }")
                itemData = souprow.find_all(class_=re.compile("hidden-sm hidden-md hidden-lg clearfix"))
                print(itemData)
                print("{ }")
                #print(souprowData)
                link = souprow.find("a")
                if(printSample == False):
                    print(link)
                    printSample = True
                if(link != None):
                    if(len(link.get_text(strip=True)) != 0):
                        itemName = link.get_text()
                        pageName = link.get('href')
                        if(itemName in itemsDict):
                            if (itemsDict[itemName] != pageName):
                                itemName = itemName + '- Alt'
                                itemsDict[itemName] = pageName
                        itemsDict[itemName] = pageName
                #print(souprow)
                #data = souprow.find(class_=re.compile("clearfix"))
                #itemDetails = data.get_text()
                print(itemName)
                print(pageName)
                #print(itemDetails)
                #print(itemClass)
                #print(itemRarity)
                #print(itemSlot)
                #print(itemType)
                print("END OF ITEM")
                #print(itemName + ": " + pageName + "; " + itemClass + " ; " + itemRarity + "; " + itemSlot + "; " + itemType)
                #print(link.get_text() + " : " + link.get('href'))
        #soup = BeautifulSoup(soup, features="lxml", parse_only=a_class)
        #soup = soup.html.find_all("href")
        #soup = soup.find_all('href')
        
        #Now, there's a formatted block of HTML containing a bunch of stuff that doesn't matter, and 50 entries that do matter.
        #Now, select every 

        #print(soup.prettify()) #This is basically a debug-only line for now.
        #print(itemsDict["itemName"])
    #print ("Length of dictionary: " + str(len(itemsDict)))
    #pprint.pprint(itemsDict)
    
    #for key in itemsDict.items():
    #    print(key)
    #    for value in itemsDict[key]:
    #        print (key, ':', itemsDict[key][value])
    #      if i == 100: break
    #      print((itemsDict[k]))
        
        #for k, v in itemsDict.items():
            #print(k, v)
    #print(itemsDict)


#def crupdate_table(table_code):
    #If the specified table doesn't exist or is null, create and populate it.
    #If the specified table exists and is not null, attempt to update it.

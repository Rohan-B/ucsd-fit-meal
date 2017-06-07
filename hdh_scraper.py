#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

from lxml import html
import requests
import sys
import re

def main():

    ids = ['64', '18', '24', '11', '05', '01']

    for num in ids:
        page = requests.get('https://hdh.ucsd.edu/DiningMenus/default.aspx?i=' + num)
        tree = html.fromstring(page.content)

        name = tree.xpath('//h2[@id="HoursLocations_locationName"]/text()')[0]

        items = tree.xpath('//td[@class="menuList"]/ul/li/a/text()')

        itemloc = tree.xpath('//td[@class="menuList"]/ul/li/a/@href')

        print(name)
        
        maxy = 0
        name = ""
        maxcal = 0
        maxprotein = 0

        for i in range(0, len(items)):
            #print(items[i])
            itempage = requests.get("https://hdh.ucsd.edu/DiningMenus/" + itemloc[i])
            itemtree = html.fromstring(itempage.content)

            calorie, fat, carb = itemtree.xpath('//span[@style="font-weight:bold;"]/text()')
            nutrition = itemtree.xpath('//td[@style="border-bottom:3px solid #445329;"]/text()')   
            #print(calorie)
            protein = nutrition[len(nutrition) - 2] 
            #print(protein)

            non_decimal = re.compile(r'[^\d.]+')
            num_cal = float(non_decimal.sub('', calorie)) 
            num_protein = float(non_decimal.sub('', protein))
            
            ratio = num_protein / num_cal
            
            #print(ratio)
            
            if ratio > maxy:
                maxy = ratio
                name = items[i]
                maxcal = calorie
                maxprotein = protein
        
        print(name)
        print(maxcal)
        print(maxprotein)

main()


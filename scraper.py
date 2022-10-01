import requests
from bs4 import BeautifulSoup
import sys
import json


# funkcni v cmd
#url = sys.argv[1]
#csv = sys.argv[2]



def main(url):
    odp_serveru = requests.get(url)
    print(odp_serveru.text) # vypise kompletni stranku

    soup = BeautifulSoup(odp_serveru.text,'html.parser')
    print(soup.div)







#def save_csv(path):


# tento zapis funguje pouze v idle. Pro cmd je potreba jen argument URL
main('https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')



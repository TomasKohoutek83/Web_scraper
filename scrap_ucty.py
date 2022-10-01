


def make_soup(URL,payload):
     try:
     r = requests.get(URL, params=payload)
     r.raise_for_status()
     soup = BS(r.text, "html.parser")
     return soup
     except HTTPError:
     print('Could not retrieve the page')
     except:
     print(sys.exc_info()[:1])
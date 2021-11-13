# useful:
# https://towardsdatascience.com/how-to-collect-data-from-any-website-cb8fad9e9ec5
# https://www.dataquest.io/blog/web-scraping-tutorial-python/

from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import time
import requests
import random

title = []
year = []
rating = []

urls = [
"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=200&start=1&view=simple",
"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=200&start=201&view=simple",
"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=200&start=401&view=simple",
"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=200&start=601&view=simple",
"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=200&start=801&view=simple"
]
#urls = ["https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=10&start=40&view=simple"]

rate = [i/50 for i in range(10)]

for url in urls:

  page = requests.get(url)
  soup = bs(page.content, features="html.parser")

  for atag in soup.find_all('a'):
    atagtxt = str(atag)
    if '/title/tt' in atagtxt and 'img alt' not in atagtxt:
      mtitle = atagtxt[atagtxt.find('">')+len('">') : atagtxt.rfind('</a>')]
      mtitle = unicode(mtitle, errors='replace')
      pguideurl = "https://www.imdb.com" + atagtxt[atagtxt.find('<a href="')+len('<a href="') : atagtxt.rfind('">')] + "parentalguide"
      pguidepage = requests.get(pguideurl)
      pguidesoup = bs(pguidepage.content, features="html.parser")
      nudadv = pguidesoup.find_all(id="advisory-nudity")[0]
      nscoretxt = nudadv.find_all(class_="advisory-severity-vote__message")[0].get_text()
      if "mild" in nscoretxt:
        print(mtitle + "  " + pguideurl + "  " + nscoretxt)

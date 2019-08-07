import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.indeed.co.in/jobs?q=data+scientist&l=Hyderabad"

page= requests.get(url)
soup=BeautifulSoup(page.txt, "html.parser")
print(soup.prettify())

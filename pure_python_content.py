import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys

import urllib2
import bs4 
import string

import facepy
import re
import csv
import datetime
import urllib
import io

data_jeremy = pd.read_csv('scraper/data.csv')
links = list(set(list(data_jeremy['link'])))

content = []
driver = webdriver.Firefox()
driver.wait = WebDriverWait(driver, 2)
count = 0
for index, link in enumerate(links):
    driver.get(link)
    time.sleep(2)
    try:
        source = driver.page_source
    except:
        driver.get(link)
        time.sleep(10)
        source = driver.page_source
        time.sleep(10)
        count += 1
        pass
    split = source.split()
    for i, v in enumerate(split):
        if '<' in v or '=' in v or '-' in v or '>' in v or '/' in v or '\\' in v or '\'' in v or '(' in v or ')' in v or '[' in v or ']' in v or '#' in v or ';' in v or '{' in v or '}' in v:
            split[i] = ''
    joined = string.join(split)
    content.append([link, joined])
    print index, count
    print link
    print joined[:100]
    print ''
df = pd.DataFrame(content)
df.columns = ['Links', 'Content']
df.to_csv('content_finished.csv', encoding='utf-8')
driver.quit()

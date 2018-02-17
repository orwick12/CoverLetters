# Created by Brian Orwick
# 12/14/17
# Scrape Indeed for 
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd


max_results_per_city = 100
#cities = ['Columbus', 'sacramento', 'oklahoma city', 'pittsburgh', 'raleigh', 'denver', 'minneapolis', 'Portland%2C+ME', 'ann arbor','boulder', 'chicago', 'bethesda']
cities = ['bethesda']
language = ['java', 'python']
columns = ['Location', 'Job Title', 'Summary', 'Company', 'Link']
job_df = pd.DataFrame(columns = columns)
print('Starting search for ' + str(cities))

for city in cities:
    for lang in language:
        count = 0
        for start in range(0, max_results_per_city, 10):
            # page = requests.get('https://www.indeed.com/jobs?q=epidemiology+and+%28hiv+or+global+health%29&l=' + str(city) + '&start=' + str(start))
            page = requests.get('https://www.indeed.com/jobs?q=' + str(lang) + '&l=' + str(city) + '&start=' + str(start))
            # page = requests.get('https://www.indeed.com/jobs?q=' + str(lang) +'+%28entry+or+junior%29&l=' + str(city) + '&start=' + str(start))
            sleep(1)  # ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'lxml')#, from_encoding='utf-8')
            for div in soup.find_all(name='div', attrs={'class':'row'}):
                # specifying row num for index of job posting in dataframe
                num = (len(job_df) + 1)
                # creating an empty list to hold the data for each posting
                job_post = []
                # grabbing location name
                a = div.findAll('span', attrs={'class': 'location'})
                for span in a:
                    job_post.append(span.text)
                # grabbing job title
                for b in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
                    job_post.append(b['title'])
                # grabbing summary text
                c = div.findAll('span', attrs={'class': 'summary'})
                for span in c:
                    job_post.append(span.text.strip())
                # grabbing company name
                company = div.find_all(name='span', attrs={'class':'company'})
                if len(company) > 0:
                    for d in company:
                        job_post.append(d.text.strip())
                else:
                    sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
                    for span in sec_try:
                        job_post.append(span.text)
                #grab link to page
                for link in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
                    href = 'https://www.indeed.com' + link['href']
                    job_post.append(href)
                job_df.loc[num] = job_post
            count += 1

clean_df = job_df.drop_duplicates(subset=['Summary'])

# If hunting for specific words
# new = clean_df[clean_df['Summary'].str.contains("entry|junior") == True]

# saving sample_df as a local csv file — define your own local path to save contents
clean_df.to_csv('/home/pi/Documents/prospects.csv', encoding='utf-8')
# new.to_csv('/home/pi/Documents/prospectssmall.csv', encoding='utf-8')

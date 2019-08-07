import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re

'''def remove_html_tags(text):
	clean=re.compile('(?i)<(?!span|/span)(?!br).*?>')
	return re.sub(clean,"",text)'''
urls=[]
with open('mahilinks.txt','r',newline="") as f:
    urls=f.readlines()
f.close()
f_urls=[]
for url in urls:
    f_urls.append(url.strip())
with open('techm.csv', 'a', newline="") as csvFile:
    writer = csv.writer(csvFile)
            #print([str(l[i]),str(l2[i]),str(l3[i]),str(l4[i])])
    writer.writerow(["Title","Skills","Openings","Location","Domain","Job Post Date","Job Exp Date","Description"])
csvFile.close()
for url in f_urls:
    page=requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    f=soup.text.split("\n")
    print(url)
    start=f.index("A Bachelor’s or Higher Degree is the minimum entry required for the position")
    end=f.index("Recommend this job to a friend:")
    draft=[]
    skills=[]
    title=[]
    for i in f[start+1:end]:
        if(i.strip()!=""):
            draft.append(i)
    title.append(draft[0])
    skill=draft.index("SkillSet")
    skills.append(draft[skill+1].strip())
    exp=[]
    experience=draft.index('Total Experience')
    exp.append(draft[experience+1].strip())
    opens=[]
    op=draft.index('No of Openings')
    opens.append(draft[op+1].strip())
    loc=[]
    locn=draft.index("Location")
    loc.append(draft[locn+1].strip())
    domain=[]
    d=draft.index("Domain")
    domain.append(draft[d+1].strip())
    post_date=[]
    x=draft.index("Job Post Date")
    post_date.append(draft[x+1].strip())
    exp_date=[]
    e=draft.index("Job Expiry Date")
    exp_date.append(draft[e+1].strip())
    description=[]
    de=draft.index("Job Description")
    stri=draft[de+1].replace('\xa0', ' ')
    s=stri.replace('\xc2\xb7','.')
    description.append(s.strip())
    print(title)
    print(skills)
    print(opens)
    print(loc)
    print(domain)
    print(post_date)
    print(exp_date)
    print(description)
    print("***************************************")
    with open('techm.csv', 'a', newline="") as csvFile:
        writer = csv.writer(csvFile)
            #print([str(l[i]),str(l2[i]),str(l3[i]),str(l4[i])])
        writer.writerow([title[0],skills[0],opens[0],loc[0],domain[0],post_date[0],exp_date[0],description[0]])
    csvFile.close()
    
#redundant
'''designation=[]
for des in soup.find_all(name="h5",attrs={"class":"designation"}):
    des=remove_html_tags(des.text)
    designation.append(des)
print(len(designation))
description=[]
for desc in soup.find_all(name="p",attrs={"class":"jobDesc"}):
    desc=remove_html_tags(desc.text)
    description.append(desc)
print(len(description))
location=[]
for loc in soup.find_all(name="h5",attrs={"class":"location"}):
    loc=remove_html_tags(loc.text)
    location.append(loc)
print(len(location))
country=[]
for c in soup.find_all(name="td",attrs={"width":"5%"}):
    c=remove_html_tags(c.text)
    country.append(c)
print(country)
flink=[]
for l in soup.find_all(name="a",attrs={"class":"apply"}):
    flink.append(l)'''
#print(len(row))
#l5=extract_full_link(soup)
    #l6=extract_external_final_link(l5)
    #[print("Title :: ",l[i],"\nCompany Name ::",l2[i],"\nSalary :: ",l3[i],"\nDescription :: ",l4[i],"\n**********************************") for i in range(len(l))]

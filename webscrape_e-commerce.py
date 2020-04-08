# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
from bs4 import BeautifulSoup


# %%
data=[]
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
base_url='https://www.jumia.co.ke/catalog/?q=shirts&page='

# load the first 3 pages
page_nr=4
for i, page in enumerate(range(1,page_nr,1)):
    print(i, base_url+str(page)) 
    r=requests.get(base_url+str(page),headers=headers)
    c=r.content
    soup=BeautifulSoup(c, 'html.parser')
    all=soup.find_all('div', {'class':'sku -gallery -validate-size'})
    for a in all:
        entry={}
        try:
            title =a.find_all('span',{'class': 'name'})[0].text
            entry['Title']=title
        except:
            entry['Title']=None
        try:
            brand =a.find_all('span',{'class': 'brand'})[0].text
            entry['Brand']=brand
        except:
            entry['Brand']=None
        try:
            price= a.find('span', {'class': 'price'}).text
            entry['Price']=price
        except:
            entry['Price']=None
        for ratings in a.find_all('div', {'class':'total-ratings'}):
            entry['Ratings']=ratings.text[1]
        try:
            sizes=a.find_all('span', {'class': 'js-link sku-size'})
            sizes_list=[]
            for i in sizes:
                sizes_list.append(i.text)
            entry['Sizes']=sizes_list
        except:
            entry['Sizes']=None
        try:
            produrl = a.find('a', {'class': 'link'})['href']
            entry['Product Url']=produrl
        except:
            entry['Product Url']=None
        try:
            img_url= a.find('img', {'class': 'lazy image'})['data-src']
            entry['Image Url']=img_url
        except:
            entry['Image Url']=None
        data.append(entry)


# %%
import pandas
df=pandas.DataFrame(data)


# %%
#prints the dataframe
df


# %%
df.to_csv('websrape.csv')


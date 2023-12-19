#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
# Read the Excel file
df = pd.read_excel('C:/Users/Vijay/Documents/20211030 Test Assignment/Input.xlsx')


# In[13]:


df.head()


# In[203]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Read the Excel 
# Create a directory to store the text files
os.makedirs('articles1', exist_ok=True)

# Iterate over the URLs in the Excel file
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    #print(url_id)
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    all_p_text = ""

    # Find the title of the page
    title = soup.find('h1', {'class': 'tdb-title-text'})
    if title is None:
        title = soup.find('h1', {'class': 'entry-title'})

    if title is not None:
        title = title.text
    else:
        title = ''

    # Find the div with the class 'td-post-content tagdiv-type'
    div = soup.find('div', {'class': 'td-post-content tagdiv-type'})
    c=0
    
    # If the div was not found, try to find a div with the class 'tdb-block-inner td-fix-index'
    if div is None:
        div = soup.find_all('div', {'class': 'tdb-block-inner td-fix-index'}) #tdb-block-inner td-fix-index
        c=1
        
    #print(div)
    # Check if a div was found
    if div is not None:
        # Find all p tags within the div
        if(c==0):
            p_tags = div.find_all('p')

            # Extract the text from each p tag and join them together with a space in between
            article_text = ' '.join(p.text for p in p_tags)
        if(c==1):
            for container in div:
                # Find all <p> elements within the container
                p_elements = container.find_all('p')

                # Concatenate the text content of <p> elements into the variable
                for p_element in p_elements:
                    all_p_text += p_element.get_text(strip=True) + " "
        
            article_text=all_p_text
# Print the concatenated text
        #print(article_text)

            
        # Write the title and article text to a text file
        with open(f'articles1/{url_id}.txt', 'w', encoding='utf-8') as f:
            f.write(title + '\n' + article_text)
    else:
        print(f'No div with class "td-post-content tagdiv-type" or "tdb-block-inner td-fix-index" found in {url}')


# In[ ]:





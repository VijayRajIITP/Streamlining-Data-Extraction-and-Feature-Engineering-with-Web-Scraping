#!/usr/bin/env python
# coding: utf-8

# In[165]:


import nltk
nltk.download('punkt')  # Download the necessary resources for tokenization
from nltk.tokenize import sent_tokenize, word_tokenize
import textstat
import string
from nltk.corpus import stopwords
import re


# In[166]:


stop_words = set(stopwords.words('english'))# stopwords by nltk library


# In[167]:


# stopwords from file given in stopwords folder thats is stored in stop
import os
stop=[]
folder_path = "C:/Users/Vijay/Documents/20211030 Test Assignment/stopwords"

# List all files in the folder
files = os.listdir(folder_path)

# Iterate over each file
for file_name in files:
    # Create the full path to the file
    file_path = os.path.join(folder_path, file_name)

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        file_content = file.read()
        words = file_content.split()

        # Print each word
        for word in words:
            stop.append(word)


# In[168]:


import re

def count_pronouns(text):
    # Define the pronouns to count
    pronouns = ["I", "we", "my", "ours", "us"]
    
    # Initialize a dictionary to store the counts
    counts = {pronoun: 0 for pronoun in pronouns}
    
    # Split the text into words
    words = re.findall(r'\b\w+\b', text)
    
    # Iterate over the words
    for word in words:
        # Check if the word is a pronoun and not 'US'
        if word in pronouns and word != 'US':
            # Increment the count
            counts[word] += 1
    
    return counts

# Test the function



# In[169]:


def average_word_length(text):
    # Split the text into words
    words = text.split()
    
    # Calculate the total number of characters in all words
    total_characters = sum(len(word) for word in words)
    
    # Calculate the total number of words
    total_words = len(words)
    
    # Calculate the average word length
    if(total_words)!=0: 
        average_length = total_characters / total_words
    else:
        average_length=0
    
    return average_length

# Test the function





# In[170]:


# postive words and negative words

f1="C:/Users/Vijay/Documents/20211030 Test Assignment/MasterDictionary/positive-words.txt"
f2="C:/Users/Vijay/Documents/20211030 Test Assignment/MasterDictionary/negative-words.txt"

# Read the positive words
with open(f1, 'r') as f:
    positive_words = [line.strip() for line in f if line.strip() not in stop]

# Read the negative words
with open(f2, 'r') as f:
    negative_words = [line.strip() for line in f if line.strip() not in stop]




# In[171]:


import re

def count_syllables(word):
    # Count the vowels in the word
    count = len(re.findall(r'[aeiouy]', word))

    # Subtract one for each 'es' at the end of the word
    if word.endswith('es'):
        count -= 1

    # Subtract one for each 'ed' at the end of the word
    if word.endswith('ed'):
        count -= 1

    # Ensure the count is at least 0
    count = max(count, 0)

    return count

# Assume 'text' is your text


# Split the text into words





# In[172]:


file_path1="C:/Users/Vijay/Documents/20211030 Test Assignment/articles"


# In[173]:


df = pd.read_excel('C:/Users/Vijay/Documents/20211030 Test Assignment/Output Data Structure.xlsx')


# In[174]:


df.head(1)


# In[175]:


# iterate over each row in the input DataFrame
for index, row in df.iterrows():
    url_id = row['URL_ID']  # go through each urlid
    file_path = os.path.join(file_path1, f'{url_id}.txt')# corresponding txt files
    #print(url_id)
    # open the text file 
    with open(file_path, 'r', encoding='utf-8') as txt_file:
        text = txt_file.read()
    # sentence tokenize
    sentences = sent_tokenize(text)
    # word tokenize
    words = word_tokenize(text)
    # removing stopwords given in StopWords folder
    words = [w for w in words if not w in stop]
    #print(words)
   #  1.postive score
    positive_score=0
    for words2 in words:
        if words2 in positive_words:
            positive_score=positive_score+1
    #print(positive_score)
    # Negative score
    
    negative_score=0
    for words4 in words:
        if words4 in negative_words:
            negative_score=negative_score+1
    # ploarity score
    Polarity_Score = (positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
    # Subjective Score
    Subjectivity_Score = (positive_score + negative_score)/ ((len(file_content)) + 0.000001)
    #AVG SENTENCE LENGTH
    num_sentences = len(sentences)
    num_words = len(words)
    #print(num_words)
    if num_sentences==0:
        average_sentence_length = 0
    else:
        average_sentence_length=num_words / num_sentences
        
    #complex words
    complex_words = [word for word in words if textstat.syllable_count(word) > 2]
    # Calculate the number of complex words
    num_complex_words = len(complex_words)
    # Calculate the percentage of complex words
    if(num_words!=0):
        percentage_complex_words = num_complex_words / num_words * 100
    else:
        percentage_complex_words=0
    # fogindex
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    #AVG NUMBER OF WORDS PER SENTENCE
    if num_sentences !=0:
        average_words_per_sentence = num_words / num_sentences
    else:
        average_words_per_sentence=0
        
    #complex word count
    #num_complex_words
    # WORD COUNT
    # Remove the stop words and punctuation
    cleaned_words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Count the cleaned words
    word_count = len(cleaned_words)
    # SYLLABLE PER WORD

    # Count the syllables in each word
    syllable_counts = [count_syllables(word) for word in words]
    sum1=sum(syllable_counts)
    # personal pernoun
    l1=count_pronouns(text)
    #print(l1)  
    #average_word_length
    t1=average_word_length(text)
    # add the score to the row
    df.loc[index, 'POSITIVE SCORE'] = positive_score  # assuming 'score' is the column name
    df.loc[index, 'NEGATIVE SCORE'] = negative_score
    df.loc[index,'POLARITY SCORE'] =  Polarity_Score
    df.loc[index,'SUBJECTIVITY SCORE']=Subjectivity_Score
    df.loc[index,'AVG SENTENCE LENGTH']=average_sentence_length
    df.loc[index,'PERCENTAGE OF COMPLEX WORDS']=percentage_complex_words
    df.loc[index,'FOG INDEX']=fog_index
    df.loc[index,'AVG NUMBER OF WORDS PER SENTENCE']=average_words_per_sentence
    df.loc[index,'COMPLEX WORD COUNT']=num_complex_words
    df.loc[index,'WORD COUNT']=word_count
    df.loc[index,'PERSONAL PRONOUNS']=sum(l1.values())
    df.loc[index,'AVG WORD LENGTH']=t1
    df.loc[index,'SYLLABLE PER WORD']=sum1
    
# write to output xlsx file
df.to_excel('outputnew.xlsx', index=False)


# In[176]:


df1 = pd.read_excel("outputnew.xlsx")


# In[177]:


df1.head(100)


# In[ ]:





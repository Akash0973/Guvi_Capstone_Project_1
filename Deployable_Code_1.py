import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import datetime
import streamlit as st

#Initialize all the required  variables for data handling
#Inputing hashtag, since, until, and limit from User
    #using streamlit input feature
    
hashtag = st.text_input('Insert Hashtag: ')
since = st.text_input('Insert Start date in (YYYY-MM-DD): ')
until = st.text_input('Insert End date in (YYYY-MM-DD): ')
query = (hashtag
        + ' since:'
        + since
        + ' until:'
        + until)
limit = st.number_input('Insert Limit of Data: ')
results = []

#Scrapping data from Twitter and storing them in list called results

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break
    results.append([tweet.date, tweet.id,tweet.url, 
                    tweet.rawContent, tweet.user.username, 
                    tweet.replyCount, tweet.retweetCount, tweet.lang, 
                    tweet.source, tweet.likeCount])

#Storing the results of scrapping into a DataFrame

tweets_df = pd.DataFrame(results,
                         columns = ['Date', 'Id', 'URL', 'Tweet_Content', 
                                    'User', 'Reply_Count', 'Retweet_Count', 
                                    'Language', 'Source', 'Like_Count'])

#Outputing the DataFrame on screen using streamlit display data feature

st.dataframe(tweets_df)

#Check if user has clicked the "Upload" button

upload = st.button('Click to upload in Database')

#generating CSV file name which will be used to download the CSV file
#Convert DataFrame to CSV format

file_csv_name = (hashtag
                 + ' ('
                 + since
                 + ' to '
                 + until
                 + ') '
                 + str(datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'))
                 + '.csv')
csv_data = tweets_df.to_csv()

#initializing MongoDB Database and creating a collection

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['GUVI_Capstone_Projects']
collection = mydb['Twitter_Scrapping']

#generating JSON file name which will be used to download the JSON file

file_json_name = (hashtag
                  + ' ('
                  + since
                  + ' to '
                  + until
                  + ') '
                  + str(datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'))
                  + '.json')

#convert Dataframe to a list of documents meant for JSON file

json_data = []
col = list(tweets_df.columns)
for df_row in range(tweets_df.shape[0]):
    data = list(tweets_df.loc[df_row])
    col_count = len(data)
    auxdict = {}
    for df_col in range(col_count):
        auxdict[col[df_col]] = str(data[df_col])
    json_data.append(auxdict)

#If User has clicked on the Upload button, Data gets loaded in the collection

if upload:
    savedate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    record = {'Hashtag':hashtag,
              'Query_Date':savedate,
              'Scraped Data':json_data}
    collection.insert_one(record)
    upload=0

#Downloading of CSV and JSON files

st.download_button(label = 'Download CSV file',
                   data = csv_data,
                   file_name = file_csv_name)
st.download_button(label = 'Download JSON file',
                   data = str(json_data),
                   file_name = file_json_name)

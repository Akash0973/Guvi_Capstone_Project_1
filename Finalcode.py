import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import datetime
import streamlit as st

#Initialize all the required  variables for data handling
#Inputing hashtag, since, until, and limit from User
    #using streamlit input feature
    
hashtag=st.text_input('Insert Hashtag: ', 'Example: COVID Vaccine')
since=str(st.date_input('Insert Start date in (YYYY/MM/DD): ', datetime.date(2021,1,1)))
until=str(st.date_input('Insert End date in (YYYY/MM/DD): ', datetime.date(2021,5,31)))
query=hashtag+' since:'+since+' until:'+until
limit=st.number_input('Insert Limit of Data: ', step=1)
results = []

old_data=0      #Variable to check if an old database has been selected or not

#Scrapping data from Twitter and storing them in list called results

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i>=limit:
        break
    results.append([tweet.date, tweet.id,tweet.url, 
                    tweet.rawContent, tweet.user.username, 
                    tweet.replyCount, tweet.retweetCount, tweet.lang, 
                    tweet.source, tweet.likeCount])

#Storing the results of scrapping into a DataFrame

tweets_df = pd.DataFrame(results,
                         columns=['Date', 'Id', 'URL', 'Tweet_Content', 
                                  'User', 'Reply_Count', 'Retweet_Count', 
                                  'Language', 'Source', 'Like_Count'])

#Outputing the DataFrame on screen using streamlit display data feature

st.dataframe(tweets_df)

#Check if user has clicked the "Upload" button

upload=st.button('Click to upload in Database')

#generating CSV file name which will be used to download the CSV file
#Convert DataFrame to CSV format

file_csv_name=(hashtag+' ('+since+' to '+until+') '+
               str(datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'))+
               '.csv')
csv_data=tweets_df.to_csv()

#initializing MongoDB Database and creating a collection

myclient=pymongo.MongoClient('mongodb://localhost:27017/')
mydb=myclient['GUVI_Capstone_Projects']
collection=mydb['Twitter_Scrapping']

#generating JSON file name which will be used to download the JSON file

file_json_name=(hashtag+' ('+since+' to '+until+') '+
                str(datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S'))+
                '.json')

#convert Dataframe to a list of documents meant for JSON file

json_data=[]
col=list(tweets_df.columns)

for df_row in range(tweets_df.shape[0]):
    data=list(tweets_df.loc[df_row])
    col_count=len(data)
    auxdict={}
    for df_col in range(col_count):
        auxdict[col[df_col]]=str(data[df_col])
    json_data.append(auxdict)

savedate=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
record={'Hashtag':hashtag,
        'Query_Date':savedate,
        'Scraped Data':json_data}

#If User has clicked on the Upload button, Data gets loaded in the collection

if upload:
    savedate=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    record={'Hashtag':hashtag,
            'Query_Date':savedate,
            'Scraped Data':json_data}
    collection.insert_one(record)
    upload=0

#Downloading of CSV and JSON files

st.download_button(label='Download CSV file',
                   data=csv_data,
                   file_name=file_csv_name)
st.download_button(label='Download JSON file',
                   data=str(record),
                   file_name=file_json_name)

#Show uploaded data in sidebar

with st.sidebar:
    #Delete all saved data
    if st.button('Clear Database'):
        mydb.drop_collection(collection)
    
    st.write('Uploaded Databases:')
    for i in collection.find():
        if st.button(i['Hashtag']
                     + '_on_'
                     + i['Query_Date']):
            active=i
            old_data=1

#Show selected old data and download

if old_data:
    old_list=active['Scraped Data']
    st.write('Here is the selected Data selected from Database:')
   
    #show old data
   
    st.dataframe(old_list)
    
    old_hashtag=active['Hashtag']
    
    file_csv_name=(hashtag+'_on_'
                   + active['Query_Date']
                   + '.csv')
    csv_data=pd.DataFrame(old_list).to_csv()
    
    # Download Old data in CSV or JSON format
    
    st.download_button(label='Download Old CSV file',
                       data=csv_data,
                       file_name=file_csv_name)
    del active['_id']
    st.download_button(label='Download Old JSON file',
                       data=str(active),
                       file_name=file_json_name)
    old_data=0


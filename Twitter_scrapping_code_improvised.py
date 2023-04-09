import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import datetime
import streamlit as st

# Define Scraping function
def Twitter_Scraper(hashtag,since,until,limit):
    results = []
    for i,tweet in enumerate(
            sntwitter.TwitterSearchScraper(
                f'{hashtag} since:{since} until:{until}').get_items()):
        if i >= limit:
            break
        results.append([tweet.date, tweet.id,tweet.url, 
                        tweet.rawContent, tweet.user.username, 
                        tweet.replyCount, tweet.retweetCount, tweet.lang, 
                        tweet.sourceLabel, tweet.likeCount])
    tweets_df = pd.DataFrame(results,
                             columns=['Date', 'Id', 'URL', 'Tweet_Content', 
                                      'User', 'Reply_Count', 'Retweet_Count', 
                                      'Language', 'Source', 'Like_Count'])
    return tweets_df

# Defining the App
def streamlit_app():
    hashtag = st.text_input('Insert Hashtag: ', 'Example: COVID Vaccine')
    since = str(st.date_input('Insert Start date in (YYYY/MM/DD): ',
                              datetime.date(2021,1,1)))
    until = str(st.date_input('Insert End date in (YYYY/MM/DD): ',
                              datetime.date(2021,5,31)))
    limit = st.number_input('Insert Limit of Data: ', step=1)
    old_data = 0

    tweets_df = Twitter_Scraper(hashtag, since, until, limit)

    # Outputing the DataFrame on screen using streamlit display data feature
    st.dataframe(tweets_df)

    # Generating CSV file name which will be used to download the CSV file
    file_csv_name = (hashtag + ' (' + since + ' to ' + until + ') ' + str(
            datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
        ) + '.csv')

    # Convert DataFrame to CSV format
    csv_data = tweets_df.to_csv()
    
    # Generating JSON file name which will be used to download the JSON file
    file_json_name = (hashtag + ' (' + since + ' to ' + until + ') ' + str(
            datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
        ) + '.json')

    # Convert Dataframe to a list of documents meant for JSON file
    json_data = []
    col = list(tweets_df.columns)

    for df_row in range(tweets_df.shape[0]):
    
        data = list(tweets_df.loc[df_row])
        col_count = len(data)
        auxdict = {}
    
        for df_col in range(col_count):
            auxdict[col[df_col]] = str(data[df_col])
    
        json_data.append(auxdict)

    savedate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    record = {'Hashtag':hashtag,
              'Query_Date':savedate,
              'Scraped Data':json_data}

    # Downloading of CSV and JSON files
    st.download_button(label='Download CSV file',
                       data=csv_data,
                       file_name=file_csv_name)

    st.download_button(label='Download JSON file',
                       data=str(record),
                       file_name=file_json_name)

    # Check if user has clicked the "Upload" button
    upload = st.button('Click to upload in Database')

    # If User has clicked on the Upload button, Data gets loaded in the collection
    if upload:
        savedate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        record = {'Hashtag':hashtag,
                  'Query_Date':savedate,
                  'Scraped Data':json_data}
        collection.insert_one(record)
        upload = 0

    # Generate a sidebar for showing Saved Database
    with st.sidebar:   
        
        # Delete all saved data
        if st.button('Clear Database'):
            mydb.drop_collection(collection)
        
        # Show all uploaded Database
        st.write('Uploaded Databases:')
    
        for i in collection.find():
            if st.button(i['Hashtag'] + '_on_' + i['Query_Date']):
                active = i
                old_data = 1

    # Show selected old data and download
    if old_data:
        old_list = active['Scraped Data']
        st.write('Here is the selected Data selected from Database:')
   
        # Show old data
        st.dataframe(old_list)
    
        old_hashtag = active['Hashtag']
    
        # Generate CSV file name and save data in CSV format
        old_csv_name = (old_hashtag + '_on_' + active['Query_Date'] + '.csv')
        old_csv_data = pd.DataFrame(old_list).to_csv()
    
        # Download Old data in CSV format
        st.download_button(label='Download Old CSV file',
                           data=old_csv_data,
                           file_name=old_csv_name)
    
        # Generate CSV file name and save data in JSON format
        old_json_name = (old_hashtag + '_on_' + active['Query_Date'] + '.json')
        del active['_id']
        old_json_data = str(active)
    
        # Download Old data in JSON format
        st.download_button(label='Download Old JSON file',
                           data=old_json_data,
                           file_name=old_json_name)
    
        old_data = 0

if __name__ == '__main__':
    
    # Initializing MongoDB Database and creating a collection
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['GUVI_Capstone_Projects']
    collection = mydb['Twitter_Scrapping']
    
    # Running the streamlit application
    streamlit_app()
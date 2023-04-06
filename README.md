# Guvi_Capstone_Project_1

## **_Problem Statement:_**

Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, you want to scrape the data from Twitter. You Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.

## **_Approach:_**

By using the “snscrape” Library, Scrape the twitter data from Twitter Reference
Create a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
Store each collection of data into a document into Mongodb along with the hashtag or key word we use to  Scrape from twitter. 

example:

    ({“Scraped Word”           : “Elon Musk”,

     “Scraped Date”            : 15-02-2023,
     
     “Scraped Data”            : [{1000  Scraped data from past 100 days }]})

Create a GUI using streamlit that should contain the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped. After scraping, the data needs to be displayed in the page and need a button to upload the data into Database and download the data into csv and json format.

## **_Results:_**

You have to build a solution that should be able to scrape the twitter data and store that in the database and allow the user to download the data with multiple data formats.

## **_Workflow:_**

1. The code first inputs the Hashtag/Keyword from the user along with Date search range and limit of number of data.
2. The code then scrapes the data from Twitter and stores them in an array.
3. This array is then converted to a DataFrame and displayed on the screen.
4. The DataFrame is then converted to CSV and JSON formats along with eshtablising a connection with MongoDB Database for uploading purposes.
5. If the user clicks on Download options for each of the two data formats, the information gets downloaded in the desired file format.
6. User is then presented with an option of uploading the Data into the Database as initialized in step 4.
7. The code also creates a sidebar which shows all the uploaded Databases along with an option to delete all Databases.
8. Once the User clicks on a previously uploaded database, they are shown the data in a DataFrame format.
9. Additionally, the User is also presented with an option to download the old data in CSV and JSON format.

## **_Concepts involved:_**

1. Python Scripting
2. MongoDB
3. Streamlit
4. Snscrape


## **_HOW TO RUN TWITTER SCRAPER IN YOUR SYSTEM:_**

**_Pre-requisites: Python and MongoDB must be installed in your system._**

Open cmd:

1. > (base) C:\Users\Usernme>pip install virtualenv 
2. > (base) C:\Users\Usernme>virtualenv test_env
3. > (base) C:\Users\Usernme>cd test_env
4. > (base) C:\Users\Usernme\test_env>cd Scripts
5. > (base) C:\Users\Usernme\test_env\Scripts>activate
6. > (test_env) C:\Users\Usernme\test_env\Scripts>mkdir Scraper
7. > (test_env) C:\Users\Usernme\test_env\Scripts>cd Scraper

At this point, download the github files into the folder created by step 7.
This folder is most likely located in Users>Username>test_env>Scripts>Scraper.
You can search for this folder by typing "Scraper" in the "Search this PC" tab in "This PC".

8. > (test_env) C:\Users\Usernme\test_env\Scripts\Scraper>pip install -r requirement.txt
9. > (test_env) C:\Users\Usernme\test_env\Scripts\Scraper>streamlit run Twitter_scrapping_code.py
10. > You can now view your Streamlit app in your browser with URL : http://localhost:8501

Below link contains a demo video explaining how to use the application:
<insert_link>

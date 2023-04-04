# Guvi_Capstone_Project_1

## **_Problem Statement:_**

Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, you want to scrape the data from Twitter. You Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.

## **_Approach:_**

By using the “snscrape” Library, Scrape the twitter data from Twitter Reference
Create a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
Store each collection of data into a document into Mongodb along with the hashtag or key word we use to  Scrape from twitter. 

example:

    ({“Scraped Word”            : “Elon Musk”,

     “Scraped Date”            : 15-02-2023,
     
     “Scraped Data”            : [{1000  Scraped data from past 100 days }]})

Create a GUI using streamlit that should contain the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped. After scraping, the data needs to be displayed in the page and need a button to upload the data into Database and download the data into csv and json format.

## **_Results:_**

You have to build a solution that should be able to scrape the twitter data and store that in the database and allow the user to download the data with multiple data formats.






## **_HOW TO RUN TWITTER SCRAPER IN YOUR MACHINE:_**
open cmd:
1. > C:\Users\mypc> pip install virtualenv 
2. > C:\Users\mypc> virtualenv test_env
3. > C:\Users\mypc> cd test_env
4. > C:\Users\mypc\test_env> cd Scripts
5. > C:\Users\mypc\test_env\Scripts>activate           # It will activate the virtual environment
6. > (test_env)  C:\Users\mypc\> mkdir Scraper         # Create a folder named Scraper
7. > (test_env)  C:\Users\mypc\> cd Scraper

At this point, download the github files into the folder created by step 7.
This folder is most likely located in Users>Username>test_env>Scripts>Scraper.
You can search for this folder by typing "Scraper" in the "Search this PC" tab in "This PC".

8. > (test_env)  C:\Users\mypc\Scraper> pip install -r requirement.txt              # it will install all the required modules in the environment
9. > (test_env)  C:\Users\mypc\Scraper> streamlit run Twitter_scrapping_code.py     # Now run the app using streamlit
10. > You can now view your Streamlit app in your browser with URL:http://localhost:8501

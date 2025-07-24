import streamlit as st
import time
import random as rand
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import math

# importing all the neccesarry libraries
# for data handling
import numpy as np
import pandas as pd
import json

# for web scraping
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import date
from datetime import datetime, timedelta
from dateutil.parser import parse


reveiw_div = r"afkKaa-4T28-"  # list of reviews (list tag)
reviewer_info = r"_0Uufw15R3a4-"  # info about the reveiwers (section tag)
review_class = r"MpiILQAMSSg-"  # info about the reviews (div tag)

# meta data getters
reviewer_place = r"POyqzNMT21k- C7Tp-bANpE4-"  # branch that was reviewed (p tag)
review_info_div = r"_6rFG6U7PA6M-"  # review (div tag)

review_whole_rating = r"yuQYBV659bs-"
rating_info = r"R9NyqT2lRqw-"  # stars div (div tag)
review_stars = r"tSiVMQB9es0-"  # number of stars (div tag)
reviewer_name = "_1p30XHjz2rI-"  # reviewer name

dates_class = "iLkEeQbexGs-"
all_ratings = "gUG3MNkU6Hc-"

today = date.today()  # todays date
formatted_date = today.strftime("%d/%m/%Y")

if "pd_data" not in st.session_state:
    st.session_state["pd_data"] = ""

if "user_dict" not in st.session_state:
    st.session_state['user_dict'] = {}

if "start_date" not in st.session_state:
    st.session_state["start_date"] = ""

if "end_date" not in st.session_state:
    st.session_state["end_date"] = ""

def highlight_substrings(full_string, highlight_dict):
    # Create a copy of the full string to modify
    modified_string = full_string

    # Replace each substring with its highlighted version
    for substring, color in highlight_dict.items():
        if substring != None:
            replacement = f'<span style="background-color:{color}; border-radius:5px;">{substring}</span>'
            modified_string = modified_string.replace(substring, replacement)
    modified_string = (
        f'<span style="color:#000F08; font-size:15px">{modified_string}</span>'
    )
    return modified_string


def format_dates(date_list):
    formatted_dates = []
    today = datetime.now()

    for date_str in date_list:
        date_str = date_str.strip().lower()

        if date_str == "Today":
            date = today
        elif date_str == "Yesterday":
            date = today - timedelta(days=1)
        elif "day" in date_str and "ago" in date_str:
            days_ago = int(date_str.split()[0])  # Extract the number of days
            date = today - timedelta(days=days_ago)
        else:
            # Parse full date strings like "November 11, 2021"
            try:
                date = parse(date_str)
            except Exception:
                formatted_dates.append("Invalid date")
                continue

        formatted_dates.append(date.strftime("%d/%m/%Y"))

    return formatted_dates


def scrapeData(
    driver,
    reviews: list,
    cities: list,
    dates: list,
    stars: list,
    ratings: list,
    names: list,
):
    found = False
    reloaded = False
    while not found:
        XPATH_for_cities = (
            rf"//section[@class='{reviewer_info}']//p[@class='{reviewer_place}']"
        )
        XPATH_for_reviews = (
            rf"//div[@class='{review_class}']//div[@class='{review_info_div}']"
        )
        # Find nested element using XPath
        scrapeCities = driver.find_elements(
            By.XPATH, XPATH_for_cities
        )  # getting cities
        scrapeReviews = driver.find_elements(
            By.XPATH, XPATH_for_reviews
        )  # getting reviews
        scrapeDates = driver.find_elements(
            By.XPATH, f"//p[@class='iLkEeQbexGs-']"
        )  # getting dates
        scrapeStars = driver.find_elements(
            By.CSS_SELECTOR, f".R9NyqT2lRqw- .{review_stars}"
        )  # getting stars
        scrapeRatings = driver.find_elements(
            By.CSS_SELECTOR, f".{all_ratings}"
        )  # getting ratings
        scrapeNames = driver.find_elements(
            By.CSS_SELECTOR, f".{reviewer_name}"
        )  # getting names

        if len(scrapeCities) == 0:
            driver.refresh()  # reload pages if things havent been loaded
            time.sleep(1)
            reloaded = True
            continue

        # print(len(scrapeReviews), len(scrapeCities), len(scrapeDates), len(scrapeStars), )

        for i in range(len(scrapeReviews)):
            if (
                "Read more" not in scrapeReviews[i].text
                and len(scrapeReviews[i].text) < 150
            ):
                reviews.append((scrapeReviews[i].text).replace("\n", " "))
                cities.append(scrapeCities[i].text)
                dates.append(((scrapeDates[i].text).replace("Dined", "")).strip())
                stars.append(scrapeStars[i].get_attribute("innerHTML"))
                ratings.append((scrapeRatings[i].text).replace("\n", " "))
                names.append(scrapeNames[i].text)
        found = True
    return reloaded

    # element = driver.find_elements(By.CSS_SELECTOR, f".{review_class} .{review_info_div}") # commenting for future referencing


def scrapeResturant(driver, limit):
    reviews = []
    cities = []
    dates = []
    stars = []
    ratings = []
    names = []

    next_button_class = "ojKcSDzr190- y4S9mw-uCFI- g-dxt-fQ2ZU- C7Tp-bANpE4-"
    next_ = driver.find_elements(
        By.XPATH, f"//div[@class='TkpxbcBbu80-']//a[@class='{next_button_class}']"
    )
    next_ = next_[1] if len(next_) > 1 else next_[0]

    bar = st.progress(0)
    progress = 0
    while len(reviews) < limit:
        scrapeData(
            driver, reviews, cities, dates, stars, ratings, names
        )  # tells if the page was reloaded

        next_ = driver.find_elements(
            By.XPATH, f"//div[@class='TkpxbcBbu80-']//a[@class='{next_button_class}']"
        )
        next_ = next_[1] if len(next_) > 1 else next_[0]

        progress = int((len(reviews) / limit) * 100)
        if progress > 100:
            progress = 100
        bar.progress(progress)

        # next_.click() # idk why drive click isnt working
        # Using JavaScript to click an element
        driver.execute_script("arguments[0].click();", next_)

        time.sleep(1)
    return (reviews, cities, dates, stars, ratings, names)


def getReviewPerDate(dates, stars):
    reviewsOnDate = {}

    for i in range(len(dates)):
        if dates[i] not in reviewsOnDate:
            reviewsOnDate[dates[i]] = []
        reviewsOnDate[dates[i]].append(stars[i])
    return reviewsOnDate


def scrapeSite(url, limit):
    driver = webdriver.Chrome()
    driver.get(url)
    (reviews, cities, dates, stars, ratings, names) = scrapeResturant(driver, limit)
    driver.quit()
    dates = format_dates(dates)

    return getReviewPerDate(dates, stars)


def getAnalyzedReviews():
    data = {}
    with open("review_analysis.json", "r") as file:
        data = json.load(file)
    return data

def filter_ratings_by_date_range(ratings_dict, start_date, end_date):
    # Convert input dates to datetime objects
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    
    # Filter the dictionary
    filtered_ratings = {}
    for date_str, ratings in ratings_dict.items():
        try:
            current_date = datetime.strptime(date_str, "%d/%m/%Y")
            if start <= current_date <= end:
                filtered_ratings[date_str] = ratings
        except ValueError:
            # Skip invalid date formats
            continue
    
    return filtered_ratings

def createTimeframeRating(df):
    ratingsPday = {}
    for i in range(len(df['date'])):
        if df['date'][i] not in ratingsPday:
            ratingsPday[df['date'][i]] = []
        ratingsPday[df['date'][i]].append(df['stars'][i])
    
    for key, val in ratingsPday.items():
        ratingsPday[key] = sum(val) / len(val)

    return ratingsPday


def getFiltered_ratings(ratings, start_date, end_date):
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    
    # Filter the dictionary
    filtered_ratings = {}
    for date_str, ratings in ratings.items():
        try:
            current_date = datetime.strptime(date_str, "%d/%m/%Y")
            if start <= current_date <= end:
                filtered_ratings[date_str] = ratings
        except ValueError:
            # Skip invalid date formats
            continue
    
    return filtered_ratings

def buildplots(our, user):
    
    # preparing data
    our = createTimeframeRating(our)
    # st.write(our)
    
    
    for key, val in user.items():
        val = np.array(val, dtype='float')
        user[key] = sum(val) / len(val)
        
    col1, col2 = st.columns(2)
    if st.session_state['start_date'] == "":
        start_date = col1.date_input(label="Start Date", format="DD/MM/YYYY")
        st.session_state['start_date'] = start_date
    else:
        start_date = st.session_state['start_date']
      
    if st.session_state['end_date'] == "":
        end_date = col2.date_input(label="End Date", format="DD/MM/YYYY")
        st.session_state['end_date'] = end_date
    else:
        end_date = st.session_state['end_date']
                
    start_date = start_date.strftime("%d/%m/%Y")
    end_date = end_date.strftime("%d/%m/%Y")
    
    col1.write(our)
    col2.write(user)
    
    our = getFiltered_ratings(our, start_date, end_date)
    user = getFiltered_ratings(user, start_date, end_date)
    
    col1.write(our)
    col2.write(user)
    
    col1.write("Nobu's Avg Ratings")
    col1.line_chart(our)
    
    col2.write("User's Restaurant's Avg Ratings")
    col2.line_chart(user)

def compare_sites(df):
    st.divider()

    # Input Section
    col1, col2 = st.columns(2)
    url = col1.text_input(
        "Please Enter the URL of your restaurant:",
        placeholder="https://opentable.com/Nobu",
    )
    num_reviews = col2.number_input(
        "Please Enter the number of reviews to scrape:", min_value=20
    )

    # Submit Button
    if st.button("Submit"):
        if not url or not num_reviews:
            st.error("Please enter both the URL and the number of reviews.")
        else:
            st.success(f"Scraping {int(num_reviews)} reviews from: {url}")
            # Simulating scraping process
            st.divider()
            # Create a placeholder for the progress message
            progress_message = st.empty()
            progress_message.write("Scraping in progress...")

            if st.session_state['user_dict'] == {}:
                user_site = scrapeSite(url, num_reviews)
                st.session_state['user_dict'] = user_site
            else:
                user_site = st.session_state['user_dict']
                
            # Replace the progress message with the completion message
            progress_message.write("Finished Scraping!")
            st.divider()
            st.write(user_site)
            
            buildplots(pd.DataFrame(df), user_site)


def normalizeReviews(reviews_data):
    normalizedReviews = []

    for date, reviews in reviews_data.items():
        for review in reviews:
            base_review = {
                "date": date,
                "name": review["name"],
                "stars": review["stars"],
                "city": review["city"],
                "feedback": review["feedback"],
                "complete_rating": review["rating"],
                "Food": None,
                "Service": None,
                "Environment": None,
            }

            categories = review["categories"]
            for category, description in categories.items():
                base_review[category] = description

            normalizedReviews.append(base_review)
    return normalizedReviews


# Set the page layout to wide
st.set_page_config(layout="wide")
if st.session_state['pd_data'] == "":
    df = normalizeReviews(getAnalyzedReviews())
    st.session_state['pd_data'] = df
else:
    df = st.session_state['pd_data']


def main():
    st.title("Review Scrapper and Comparer!")
    description = st.empty()
    des_text = "Compare your favourite Restaurants to Nobu! 🍥"
    for i in range(len(des_text)):  # printing
        description.text(des_text[: i + 1])
        time.sleep(0.03)

    # Initialize session state if not exists
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Navigation logic
    if st.session_state.page == "home":
        if st.button("Compare Nobu's rating"):
            st.session_state.page = "compare_ratings"
            st.rerun()
        color_system_html = """
        <p> 
            Food
            <span style="
            background-color:#457EAC; 
            display:inline-block; 
            width:50px">&#8205
            </span> 
            <br><br>
            Service
            <span style="
            background-color:#23CE6B; 
            display:inline-block; 
            width:50px">&#8205
            </span>
            <br><br>
            Environment
            <span style="
            background-color:#CBBEB3; 
            display:inline-block; 
            width:50px">&#8205
            </span>
            
        </p>
    """
        st.markdown(color_system_html, unsafe_allow_html=True)
        for review in df:
            # color references
            color_ref = {
                review["Food"]: "#457EAC",
                review["Service"]: "#23CE6B",
                review["Environment"]: "#CBBEB3",
            }
            block_html = f"""
        <div style="
                height:auto;
                width:80vw;
                background-color:#4A4E69;
                color: #F2E9E4;
                padding:20px;
                border-radius:20px;
                margin:20px 20px 20px 0px;
                font-family: Arial, sans-serif;
                ">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex;">
                    <h1 style="margin:0; font-size: 1.5em; color:#F7D08A;">{review['name']}</h1>
                    <p style="margin-top:27px; font-size: 0.8em; color:#C9ADA7 ;font-style:italic;"> 
                        {int(review['stars'])} stars review
                    </p>
                </div>
                <p style="margin:0; font-size: 0.9em; color:#C9ADA7; font-weight:normal;">
                    Dined on <strong>{review['date']}</strong>
                    <br>
                    <span style="font-style:italic; font-size:0.8em;">{review['city']}</span>
                </p>
            </div>
            <hr style="border: 0.5px solid #C9ADA7; margin: 10px 0;">
            <p style="margin: 5px 0; font-size:1em; font-weight:bold;">
                {review['complete_rating']}
            </p>
            <p style="margin: 10px 0; line-height: 1.5; font-size:0.95em;">
                {highlight_substrings(review['feedback'], color_ref)}
            </p>
        </div>
    """

            st.markdown(block_html, unsafe_allow_html=True)

    # Compare Ratings Page
    elif st.session_state.page == "compare_ratings":
        compare_sites(df)

        # Add a back button
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()


# Call the main function
if __name__ == "__main__":
    main()

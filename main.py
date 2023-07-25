# Import necessary libraries
import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
import pytz
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get email and password from environment variables
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# URL of the product to check price
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

# Headers for the request to Amazon.com
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


# Function to check the price of the product
def check_price():
    # Send a request to the URL
    response = requests.get(URL, headers=headers)
    # Get the HTML content of the page
    webpage = response.text
    # Parse the HTML
    soup = BeautifulSoup(webpage, 'html.parser')
    # Extract the price from the HTML and convert it to a float
    pricing = float(soup.select('div#apex_desktop_usedAccordionRow span.a-price span.a-offscreen')[1].getText()[1:])

    # If the price is lower than 100, send an email
    if pricing < 100:
        send_email("nostro37@gmail.com", f"Price is ${pricing}")


# Function to send an email
def send_email(email, content):
    # Login to SMTP server
    my_email = MY_EMAIL
    my_password = MY_PASSWORD
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        # Send the email
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject: Hello \n\n {content}"
        )
        # Close the connection
        connection.close()


# Main loop
while True:
    # Get the current time in Eastern Standard Time
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est)

    # If it's 9 AM, check the price
    if current_time.hour == 9:
        check_price()
        # Sleep for the rest of the day (15 hours)
        time.sleep(60 * 60 * 15)
    else:
        # If it's not 9 AM, sleep for 60 seconds before checking again
        time.sleep(60)

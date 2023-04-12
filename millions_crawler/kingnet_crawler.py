import requests
from pymongo import MongoClient, errors
from urllib.parse import unquote
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Function to remove HTML tags and unwanted characters
def clean_text(text):
    # Remove <br> tags and their variations
    cleaned_text = text.replace("<br>", "").replace("<br/>", "").replace("<br />", "")
    
    # Remove HTML tags
    cleaned_text = re.sub(r"<[^>]*>", "", cleaned_text)
    
    # Remove <span> tags
    cleaned_text = re.sub(r"<span[^>]*>", "", cleaned_text)
    cleaned_text = cleaned_text.replace("</span>", "")
    
    # Remove <font> tags
    cleaned_text = re.sub(r"<font[^>]*>", "", cleaned_text)
    cleaned_text = cleaned_text.replace("</font>", "")
    
    # Remove <p> tags
    cleaned_text = re.sub(r"<p[^>]*>", "", cleaned_text)
    cleaned_text = cleaned_text.replace("</p>", "")
    
    # Remove \n\d+ occurrences
    cleaned_text = re.sub(r"\n\d+", "", cleaned_text)
    
    # Remove escape sequences and white spaces
    cleaned_text = cleaned_text.replace("\\r", "").replace("\\n", "").replace("\\b", "").replace("\n", "").replace("\b", "").replace("\r", "").replace("\t", "").replace("  ", "")
    
    # remove  www.kidneydrfang.com
    cleaned_text = cleaned_text.replace("www.kidneydrfang.com", "")
    
    return cleaned_text


# MongoDB connection string
MONGODB_URI = str(os.getenv(key="MONGODB_URI"))
MONGODB_DATABASE = str(os.getenv(key="MONGODB_DB_NAME"))


# Configure MongoDB
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
collection = db['kingnet_items']

# Create a unique index on the inquiryId field
collection.create_index('inquiryId', unique=True)

# Base API URL
base_url = 'https://www.kingnet.com.tw/ajax/selectInquiryList'

# Parameters
params = {
    'keyword': '',
    'inquiryStatus': 'Y',
    'dataCnt': 30
}

# Function to map inquiryId and reply
def map_reply_to_inquiry(inquiry_list, discuss_list):
    reply_mapping = {item['replyId']: unquote(item['reply']) for item in discuss_list}
    for inquiry in inquiry_list:
        inquiry_id = inquiry['inquiryId']
        inquiry['reply'] = reply_mapping.get(inquiry_id, '')
def fetch_and_save_data(section_id):
    data_index = 0

    while True:
        params['sectionId'] = section_id
        params['dataIndex'] = data_index
        response = requests.get(base_url, params=params)

        # Check for a valid response
        if response.status_code != 200:
            print(f"Failed to fetch data for sectionId {section_id}, dataIndex {data_index}.")
            break

        data = response.json()

        # Check if there is data in the response
        if not data or not data["inquiryList"]:
            print(f"No more data for sectionId {section_id}, dataIndex {data_index}.")
            break

        inquiry_list = data["inquiryList"]
        discuss_list = data["discussList"]

        # Map reply to corresponding inquiry
        map_reply_to_inquiry(inquiry_list, discuss_list)

        # Save the data to MongoDB and filter out duplicates
        for item in tqdm(inquiry_list):
            # Decode the percent-encoded strings
            item['summary'] = unquote(item['summary'])
            item['reply'] = unquote(item['reply'])

            # Clean summary and reply text
            item['summary'] = clean_text(item['summary'])
            item['reply'] = clean_text(item['reply'])

            # Save only the required fields
            document = {
                'inquiryId': item['inquiryId'],
                'summary': item['summary'],
                'reply': item['reply']
            }

            try:
                collection.insert_one(document)
            except errors.DuplicateKeyError:
                pass

        # Increment the data index for the next request
        data_index += 1

# Define the number of threads to use
num_threads = 12

# Iterate over sectionIds from 1 to 126 using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = {executor.submit(fetch_and_save_data, section_id): section_id for section_id in range(1, 127)}

    for future in tqdm(as_completed(futures)):
        section = futures[future]
        try:
            future.result()
            print(f"Completed processing for sectionId {section}.")
        except Exception as e:
            print(f"Error processing sectionId {section}: {e}")

print("Data fetching, decoding, cleaning, and saving complete.")

from pytrends.request import TrendReq
import pandas as pd
import json
import boto3
import csv

# Initialize the pytrends object
pytrends = TrendReq(hl='en-US', tz=360)  # 'hl' is the language, 'tz' is timezone offset

# Get trending searches in Kenya 
trending_searches = pytrends.trending_searches(pn='kenya')

# get 100 top trending topics
top_trennds= trending_searches.head(100)

#Save trending searches to a CSV
trending_searches.columns = ['Trending Topics in Kenya'] 
trending_searches.to_csv('trending_topics_kenya.csv', index=False)
print("Trending topics saved to 'trending_topics_kenya.csv'.")

# Step 3: Categorize trends manually
category_keywords = {
    "Music": ["song", "album", "artist", "music", "track", "lyrics"],
    "News": ["election", "government", "breaking", "policy", "news", "ruto", "gachagua", "court"],
    "Sports": ["match", "team", "football", "league", "tournament","FC", "United", "vs" ],
    "Entertainment": ["movie", "show", "series", "celebrity", "actor"]
}

# Function to categorize topics (case-insensitive matching)
def categorize_topic(topic):
    
    # Check if topic ends with 'FC' or contains 'united'
    topic_lower = topic.strip().lower()#converts topic to lower case
    if 'fc' in topic_lower or 'united' in topic_lower or 'vs' in topic_lower:
        return "Sports"

    # Otherwise, match against predefined keywords
    for category, keywords in category_keywords.items():
        if any(keyword.lower() in topic.lower() for keyword in keywords):
            return category

    return "Other"  # Default category if no match

#Apply categorization
trending_searches['Category'] = trending_searches['Trending Topics in Kenya'].apply(categorize_topic)
#print(trending_searches)

trending_data = trending_searches.to_dict(orient='records')

#save to csv
csv_file= 'googletrends_ke.csv'
with open(csv_file, mode = 'w', newline ='', encoding ='utf-8') as f:
      writer= csv.writer(f)

      #write headers
      writer.writerow(["Trending Topics in Kenya", "Category"])

      #write the data in rows
      writer.writerows(trending_data)

print(f'Categorized trends saved to "googletrends_ke.csv".')

#uploading to AWS s3
def upload_to_aws(file_name, bucket_name, object_name=None):
        """Upload a file to an S3 bucket."""
        s3_client = boto3.client('s3')
        try:
                s3_client.upload_file(file_name, bucket_name, object_name or file_name)
                print(f"Successfully uploaded {file_name} to {bucket_name}")
        except Exception as e:
                print(f"Failed to upload {file_name}: {e}")

#calling function to upload
upload_to_aws(csv_file, 'content-analysis-data-ke')
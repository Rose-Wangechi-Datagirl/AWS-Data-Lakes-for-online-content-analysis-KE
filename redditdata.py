import requests
import json
import boto3
import csv


subreddits= ['Kenya', 'nairobi', 'KenyaOfficial', 'KenyaNews', 'anything_about_kenya', 'KenyanLadies']
enriched_data=[] #empty dict to store new data after enriching it

category_keywords= {
    "Politics": ["election", "government", "policy", "politics", "court", "president"],
    "Sports": ["match", "team", "football", "league", "tournament", "FC", "United", "vs"],
    "Relationships": ["relationship", "love", "dating", "marriage", "breakup", "couple"],
    "Entertainment": ["movie", "music", "show", "celebrity", "series", "concert"]
}

#categorising the data mannually as the api doesnt allow that
def categorise_post(title):
    title_lower=title.lower()
    for category, keywords in category_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    return 'other' #returns after checking all other categories

#loop through the subreddits
for subreddit in subreddits:
#reddit api added to specify limit
    url=f'https://www.reddit.com/r/{subreddit}/top/.json?limit=10'

    headers= {'User-Agent': 'Mozilla/5.0'}

    #fetching data
    response= requests.get(url, headers= headers)

    if response.status_code == 200:
        posts= response.json()['data']['children']
        
        for post in posts:
            post_data= post['data']
            title= post_data ['title']
            likes= post_data.get('ups', 0)
            num_comments= post_data.get('num_comments', 0)
            url= post_data.get('url', '')

            # calling funtion to categorise the posts
            category= categorise_post (title)

            #adding new data to dict
            enriched_data.append([category, title, likes, num_comments, url])
    else:
        print(f"Unable to fetch posts from r/{subreddit} Error:{response.status_code}")

# #save the retrieved data as json
# with open ('reddit_trending_ke.json', 'w') as f:
#     json.dump(enriched_data, f, indent= 4)
    
#     print(f'Reddit data successfully saved as reddit_trending_ke.json')

#save data as csv to be able to querry in athena
csv_file = 'reddit_trending_ke.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header only once
    writer.writerow(['category', 'title', 'likes', 'num_comments', 'url'])
    
    # Write rows (actual data)
    writer.writerows(enriched_data)

#sending the data to aws s3
def upload_to_aws (file_name, bucket_name, object_name=None):
    """Upload the file to s3 bucket"""
    s3_client= boto3.client('s3')
    try:

        s3_client.upload_file(file_name, bucket_name, object_name or file_name)
        print(f'Successfully uploaded {file_name} to {bucket_name}')
    except Exception as e:
        print(f' Failed to upload {file_name}: {e}')

#calling function to upload
upload_to_aws(csv_file, 'content-analysis-data-ke')

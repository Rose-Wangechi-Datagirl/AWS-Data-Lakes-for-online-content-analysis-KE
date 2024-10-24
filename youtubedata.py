from googleapiclient.discovery import build
import requests
import json
import boto3
import csv

#getting You Tube data from API

api_key= 'AIzaSyCmeifUcUdHQ8jjHLZXu6fgQ6Y0N1F8dN4'

#initialise youtube api client
youtube= build('youtube', 'v3', developerKey=api_key)

#getting 100 trending videos in kenya 

requests= youtube.videos().list(
        part= 'snippet,statistics',
        chart='mostPopular',
        regionCode='KE',
        maxResults=100
)

response= requests.execute()

#fetching category details inorder to get category thru' categoryid
category_request= youtube.videoCategories().list(
            part='snippet',
            regionCode='KE'
)

category_response= category_request.execute()

#category maps the id to name as per what yoytube provides
category_map= {item['id']:item['snippet']['title'] for item in category_response['items']}

# print(response)

# selecting relevant data from api response

youtube_data=[]

for video in response ['items']:
        video_id=video['id']
        title=video['snippet']['title']
        views=video['statistics']['viewCount']
        likes= video['statistics'].get('likeCount','N/A')
        category_id= video['snippet']['categoryId']
        category=category_map.get(category_id, 'Unknown')
        date_published= video['snippet']['publishedAt']
        video_url= f'https://www.youtube.com/watch?v={video_id}'

        video_data=[title,views, likes, category, date_published, video_url]

        youtube_data.append(video_data)

#save the extracted selected data as a json file
# with open ('youtube_data.json', 'w') as f:
#         json.dump(youtube_data, f, indent=4)
#         print(f'You Tube data successfully saved as a json file')

#save as csv for earsier querrying in athena
csv_file= 'you_tube_trends_ke.csv'
with open (csv_file, mode= 'w', newline='', encoding='utf-8') as f:
        writer=csv.writer(f)

        #write headers
        writer.writerow(['title', 'views', 'likes', 'category', 'date_published', 'video_url'])
        #write data rows
        writer.writerows(video_data)

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
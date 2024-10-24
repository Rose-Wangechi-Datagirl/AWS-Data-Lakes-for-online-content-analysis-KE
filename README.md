
# **Kenyan Trends Analysis Using APIs, AWS, and Data Lakes**

## **Introduction** 

This project showcases how to work with cloud platforms, build **data lakes**, interact with various **APIs**, and conduct data analysis using **SQL in AWS Athena**. The objective is to extract, enrich, store, and analyze trending data in Kenya from multiple platforms. The results help explore patterns in **news consumption, sports interest, online discussions**, and engagement metrics across social media platforms.

---

## **Objective and Problem Statement**  
Understanding how people engage with online content can reveal key societal interests and behavioral trends. In this project, I aimed to explore:
- What types of content attract the most attention in Kenya?  
- Are **likes** and **comments** reliable indicators of engagement?  
- How does public interest vary across different platforms (YouTube, Google Trends, Reddit)?  

The goal was to develop a **data lake** in AWS for storing the extracted data and to analyze it using SQL to gain actionable insights.

---

## **Key Insights**  
From the analysis, these patterns emerged:  
1. **YouTube** is the go-to platform for news consumption in Kenya.  
2. **Sports** topics dominated the **Google Trends** search data, highlighting a strong public interest.  
3. On **Reddit**, the most popular posts fell into an **"Other" category**, suggesting that discussions are diverse and cover a wide range of issues that don’t fit traditional categories like politics or sports.  
4. **Likes** and **comments** behave differently across platforms:
    - Posts with many **likes** do not always generate a high volume of **comments**.
    - Conversely, posts with numerous **comments** don’t necessarily have many **likes**.

These observations indicate that measuring engagement purely through likes or comments may not accurately reflect user involvement.

---

## **Technologies Used**
- **AWS S3**: Storing extracted data in a data lake for analysis.  
- **AWS Athena**: Querying the stored data with SQL for actionable insights.  
- **Reddit API**: Extracting data on trending discussions from multiple subreddits.  
- **Google Trends API**: Collecting real-time search trends in Kenya.  
- **Python**: Automating data extraction, enrichment, and processing.  
- **boto3**: Interfacing with AWS services from Python to upload data.  
- **Jupyter Notebooks**: Developing, testing, and documenting the workflow.  

---

## **Project Workflow**

1. **Data Extraction from APIs**  
   - Data was collected from multiple **subreddits** using the Reddit API:  
     `Kenya`, `nairobi`, `KenyaOfficial`, `KenyaNews`, `anything_about_kenya`, `KenyanLadies`.
   - I also extracted **top search topics** using the **Google Trends API** to see what was trending in Kenya.

2. **Data Enrichment and Categorization**  
   - I manually **categorized Reddit posts** into groups like **Politics**, **Sports**, **Relationships**, and **Entertainment** based on keywords.  
   - Posts that didn’t fit any specific category were labeled as **"Other."**

3. **Data Storage in AWS S3**  
   - After enriching the data, I uploaded it to an **AWS S3 bucket** using the **boto3** library. The data serves as part of a data lake for future analysis.

4. **Data Analysis Using SQL in AWS Athena**  
   - I queried the data to uncover patterns and insights, such as which topics attract the most engagement and how likes compare to comment volumes.

---

## **Project Structure**
```
/project-folder
│
├── reddit_trending_ke.json     # Enriched Reddit data  
├── google_trends.json          # Google Trends data  
├── s3_upload.py                # Python script to upload data to AWS S3  
├── analysis_queries.sql        # SQL queries for data analysis in Athena  
├── .env                        # API keys and AWS credentials (hidden from GitHub)  
├── requirements.txt            # Python dependencies  
└── README.md                   # This file  
```
---

## **How the Code Works**

1. **Reddit API Integration:**
   - The script loops through specified subreddits and extracts the top 100 posts using the **Reddit API**.
   - Each post is enriched with metadata like **category, number of likes, comments, and post URL**.

2. **Categorization Logic:**
   - Posts are categorized by checking if certain **keywords** (e.g., "football", "election") appear in the title.
   - If no keyword matches, the post is labeled as **"Other."**

3. **Uploading to AWS S3:**
   - The extracted data is saved as **JSON files** and uploaded to an **S3 bucket**.
   - The `boto3` library is used to handle the interaction with AWS services.

---

## **Insights and Conclusion**

- **News Consumption Patterns:**  
  Most Kenyans prefer YouTube for news updates, indicating a shift towards video-based news consumption.  

- **Sports Interest:**  
  **Sports** is the most searched topic on Google, showing the public's enthusiasm for sporting events and leagues.  

- **Diverse Discussions on Reddit:**  
  Reddit discussions were diverse, with many top posts falling into the **"Other" category**. This suggests that users engage with a broad range of topics beyond conventional categories like politics or sports.  

- **Engagement Metrics:**  
  - A high number of **likes** doesn’t always result in many **comments**, and vice versa.
  - This finding highlights the need for more nuanced metrics when measuring social media engagement.  


CREATE database content_analysis

CREATE EXTERNAL TABLE IF NOT EXISTS reddit (
    category STRING,
    title STRING,
    likes INT,
    num_comments INT,
    url STRING
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
LOCATION 's3://content-analysis-data-ke/'
TBLPROPERTIES (
    'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS youtube (
 	title STRING,
	views INT, 
	likes INT, 
	category VARCHRR(55), 
	date_published, 
	video_url STRING
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
LOCATION 's3://content-analysis-data-ke/'
TBLPROPERTIES (
    'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS youtube (
 	title STRING,
	views INT, 
	likes INT, 
	category STRING, 
	date_published STRING, 
	video_url STRING
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
LOCATION 's3://content-analysis-data-ke/'
TBLPROPERTIES (
    'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS googletrends (
 	Trending Topics in Kenya, Category STRING, 
	Category STRING
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
LOCATION 's3://content-analysis-data-ke/'
TBLPROPERTIES (
    'skip.header.line.count' = '1'
);

SELECT category, title, likes, num_comments
FROM reddit
ORDER BY likes DESC
LIMIT 5;

SELECT category, title, likes, num_comments
FROM reddit
ORDER BY num_comments DESC
LIMIT 5;

SELECT category, title, views, likes
FROM youtube
ORDER BY views DESC
LIMIT 10;

SELECT *
FROM googletrends
LIMIT 10;
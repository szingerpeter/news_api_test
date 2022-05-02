# Project description
This project is an implementation for the below description:

Build a Python application to:
- First, retrieve all English language news sources. Use the language filter in
sources end- point.
- Second, create a flattened version of top headlines for each of English language
news source you have retrieved above and save them into a CSV file. CSV file
should have [timestamp]_headlines.csv naming convention. timestamp is current
system timestamp.
- Finally, upload all CSV files a S3 bucket.
[s3_bucket]/[news_source_name]/ [timestamp]_headlines.csv

# Alternative solutions
There has been some decision made for the approach to be taken.

First, the implementation for ingesting data from the news api could have been based on the existing non-official client library. However, for the sake of this assignment, I decided to implement my own minimal client library to achieve the minimum requirements of the assignment in order to propose my own lower-level implementation.

Second, the implementation for fetching the top headlines could have been improved by passing a comma-separated list of sources in order to reduce the number of required API calls to be made. However, the API returns top headlines not in an alphabetical order by source, thus bucketing of the data should have been implemented additionally.

# How to run it
First, install the required dependencies for this project:
```
pip install -f .\requirements.txt
```

Then, you can run the program with the following command: 
```
python main.py --outputfolder ./test/ --configfile config.ini
```

Expected structure of the config file:
```
[news_api]
api_key=XXXXXX
[s3]
access_key_id=XXXXXX
secret_access_key=XXXXXX
```

import argparse
from configparser import ConfigParser
import pandas as pd
import os
from datetime import datetime
import boto3
from newsapi import NewsApi

def news_api_process(api_key, outputfolder):
    newsapi = NewsApi(api_key = api_key)
    files_saved = []
    try:
        sources = newsapi.get_sources()
        if sources:
            sourceid_all = [x.get("id") for x in sources]
            for sourceid in sourceid_all:
                top_headlines_source_raw = newsapi.get_top_headlines(sourceid)
                top_headlines_source_processed = list(map(lambda x: pd.io.json._normalize.nested_to_record(x), top_headlines_source_raw))
                source_output = f"{outputfolder}/{sourceid}"
                if not os.path.exists(source_output):
                    os.makedirs(source_output)
                timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%f")
                output_filename = f"{source_output}/{timestamp}_headlines.csv"
                if len(top_headlines_source_processed) > 0:
                    pd.DataFrame(top_headlines_source_processed).\
                        to_csv(output_filename, header = True, index = False)
                files_saved.append(output_filename)
    except ValueError as e:
        print(f"{str(e)}")
    return files_saved


def upload_files(files_to_upload, access_key, secret_access_key):
    s3_client = boto3.client("s3", aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
    for path in files_to_upload:
        resp = s3_client.upload_file(path, "exadeltest", "/".join(path.split("/")[-2:]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputfolder", type = str, default = "./out")
    parser.add_argument("--configfile", type = str, default = "config.ini")
    args = parser.parse_args()

    outputfolder = args.outputfolder
    config = ConfigParser()
    config.read(args.configfile)
    
    api_key = config["news_api"]["api_key"]
    access_key = config["s3"]["access_key_id"]
    secret_access_key = config["s3"]["secret_access_key"]

    files_saved = news_api_process(api_key, outputfolder)
    upload_files(files_saved, access_key, secret_access_key)
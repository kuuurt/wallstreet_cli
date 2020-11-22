import csv
import glob
import os
import subprocess

def get_filename():
    # show list of all filenames in tmp
    file_list = glob.glob("tmp/*.csv")
    return file_list

def parse_csv(filename):
    # put csv data into a list
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        csv_list = []
        for dct in map(dict, reader):
            csv_list.append(dct)
    return csv_list

def download():
    # download all s3 files from the given date
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    date = get_latest_date_on_s3()
    cmd = f"aws s3 cp s3://deutsche-boerse-xetra-pds/{date}/ tmp --recursive --no-sign-request"
    subprocess.check_output(cmd, shell=True)

def get_stock_from_dataset(dataset):
    # get stock info from dataset
    pass

def get_latest_date_on_s3():
    cmd = "aws s3 ls deutsche-boerse-xetra-pds/ --no-sign-request | sort -r | head -n 1"
    output = subprocess.check_output(cmd, shell=True).decode()
    date = output[-12:-2]
    return date

import csv
import glob
import os
import subprocess

def get_filename():
    # show list of all filenames in tmp
    date = get_latest_date_on_s3()

    file_list = glob.glob(f"tmp/{date}/*.csv")
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
    # TODO more efficient
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    date = get_latest_date_on_s3()
    cmd = f"aws s3 cp s3://deutsche-boerse-xetra-pds/{date}/ tmp/{date} --recursive --no-sign-request"
    subprocess.check_output(cmd, shell=True)


def get_stock_from_dataset(isin, dataset):
    # TODO make more efficient
    # get stock info from dataset
    for ticker_dict in dataset:
        if isin == ticker_dict['ISIN']:
            return ticker_dict['EndPrice']
    print("Isin number not found!")


def get_latest_date_on_s3():
    cmd = "aws s3 ls deutsche-boerse-xetra-pds/ --no-sign-request | sort -r | head -n 1"
    output = subprocess.check_output(cmd, shell=True).decode()
    date = output[-12:-2]
    return date


def pipeline(isin_list,short_command=None):
    # download csvs
    download()

    # get filenames
    file_list = get_filename()

    csv_list_total = []
    for filename in file_list:
        csv_list = parse_csv(filename)
        csv_list_total = csv_list_total + csv_list
    # get the price
    # TODO short output with only price
    if short_command:
        for isin in isin_list:
            print(get_stock_from_dataset(isin, csv_list_total))
    else:
        for isin in isin_list:
            print("ISIN: " + isin + ", Price: " + str(get_stock_from_dataset(isin, csv_list_total)))


def get_xetra_prices(date, isin):
    """Query aws with select object content, and returns
    all price rows of all csv files listed on specific date"""

    # list all csv files on s3 for that date

    # for each file, run the select object query and store the results

    # perhaps post process the results and make them recods

    # return results

    pass
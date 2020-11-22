import subprocess

def parse_csv():
    # parse all the csvs
    pass

def download(date):
    # download all s3 files from the given date
    pass

def get_stock_from_dataset(dataset):
    # get stock info from dataset
    pass


def get_latest_date_on_s3():
    cmd = 'aws s3 ls deutsche-boerse-xetra-pds/ | sort -r | head -n 1'
    output = subprocess.check_output(cmd, shell=True).decode()
    
import boto3
import subprocess

isin = 'DE000A0DJ6J9'

S3_BUCKET = 'deutsche-boerse-xetra-pds'

def list_objects(date, bucket=S3_BUCKET):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=date)
    return [p['Key'] for p in response['Contents']]
date = '2021-02-05'

print(list_objects(date))

s3 = boto3.client('s3')

cmd = "aws s3 ls deutsche-boerse-xetra-pds/ --no-sign-request | sort -r | head -n 1"
output = subprocess.check_output(cmd, shell=True).decode()
date = output[-12:-2]
print(output)

r = s3.select_object_content(
        Bucket=S3_BUCKET,
        Key=f'{date}/',
        ExpressionType='SQL',
        Expression=f"select * from s3object[*] s where s._1 = '{isin}'",
        InputSerialization={'CSV': {}},
        OutputSerialization={'CSV': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)

# f"aws s3 cp s3://deutsche-boerse-xetra-pds/{date}/ tmp/{date} --recursive --no-sign-request"


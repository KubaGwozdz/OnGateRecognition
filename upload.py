import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')
# Upload a new file
data = open('./pictures/other/bmw.jpeg', 'rb')
s3.Bucket('iotaghproject').put_object(Key='pic.jpg', Body=data)
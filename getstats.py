from boto.s3.connection import S3Connection
import settings
import pdb

AWS_ACCESS_KEY_ID = settings.AWS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET

BUCKET_NAME = 'logs.survey2.sebastianbassi.com'

aws_connection = S3Connection(AWS_ACCESS_KEY_ID, 
	AWS_SECRET_ACCESS_KEY)
bucket = aws_connection.get_bucket(BUCKET_NAME)
with open('logout.log', 'w') as outfile:
    for file_key in bucket.list():
        file_key.get_contents_to_file(outfile)


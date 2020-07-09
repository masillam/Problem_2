import boto3
import boto3
import re
from datetime import datetime

BUCKET_NAME="s3buckettests3proj"
uploadfoldr="uploads"
copyfile="testpdf.pdf"

file_timestamp=copyfile+datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
print(file_timestamp)

def s3_client():
    s3=boto3.client('s3')
    return s3
def s3_resource():
    s3_resource=boto3.resource('s3')
    return s3_resource

def read_object_from_bucket():
    object_key='testpdf.pdf'
    return s3_client().list_objects_v2(Bucket='s3buckettests3proj')['Contents']



def hello(event, context):

    objectlist_dict=read_object_from_bucket()

    latest_uploaded_file=max(objectlist_dict,key=lambda x: x['LastModified'])['Key']

    match=re.search('pdf',latest_uploaded_file)

    if not (match):
        raise exception("not a pdf file ")
    # rename with timestamp (copy and delete)

    s3_resource().Object(BUCKET_NAME,file_timestamp).copy_from(CopySource=BUCKET_NAME +  '/' + latest_uploaded_file)

    #move to diffferent folder
    s3_resource().Object(BUCKET_NAME,uploadfoldr).copy_from(CopySource=BUCKET_NAME +  '/' + file_timestamp)

    # s3_resource().Object('BUCKET_NAME','new.pdf').copy_from(CopySource='BUCKET_NAME/latest_uploaded_file.$(date}')

    s3.Object(BUCKET_NAME,latest_uploaded_file).delete()

    return (read_object_from_bucket())

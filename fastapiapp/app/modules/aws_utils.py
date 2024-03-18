from boto3.session import Session
from fastapi import HTTPException

async def upload_file_to_s3(bucket: str, file_path: str, object_name: str):
    session = Session()
    
    s3 = session.resource('s3')
    try:
        s3.Bucket(bucket).upload_file(file_path, object_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
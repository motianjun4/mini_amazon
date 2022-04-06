from faker import Faker
from minio import Minio
import os

minio_host = os.environ['MINIO_HOST']
minio_port = os.environ['MINIO_PORT']
access_key = os.environ['MINIO_ACCESS_KEY']
secret_key = os.environ['MINIO_SECRET_KEY']

minio_client = Minio(f"{minio_host}:{minio_port}", access_key=access_key, secret_key=secret_key, secure=False)
exist_bucket = set()


def put_file(bucket, filename, filepath) -> bool:
    if bucket not in exist_bucket and not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)
    exist_bucket.add(bucket)
    try:
        res = minio_client.fput_object(
            bucket, filename, filepath)
        return True
    except Exception as e:
        print("upload object failed, ", str(e))
        return False


def get_file(bucket:str, filename:str)->str:
    try:
        minio_client.fget_object(bucket, filename, "/tmp/"+filename)
    except Exception as e:
        print("get object failed, ", str(e))
        return None
    return "/tmp/"+filename

if __name__ == "__main__":
    # testing
    fake = Faker()
    image:bytes = fake.image(image_format='jpeg')
    with open('/tmp/test.jpg', 'wb') as f:
        f.write(image)
    put_file("test", "test1.jpg", "/tmp/test.jpg")
    path = get_file("test", "test1.jpg")
    with open(path, 'rb') as f:
        b = f.read()
    assert(b==image)
    print("success!")

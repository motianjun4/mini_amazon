import io
from faker import Faker
from minio import Minio

minio_client = Minio("vcm.tinchun.top:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)
exist_bucket = set()


def put_file(bucket, filename, stream:io.IOBase, length:int) -> bool:
    if bucket not in exist_bucket and not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)
    exist_bucket.add(bucket)
    try:
        minio_client.put_object(
            bucket, filename, stream, length)
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
    stream = io.BytesIO(image)
    put_file("test", "test.jpg", stream, len(image))
    path = get_file("test", "test.jpg")
    with open(path, 'rb') as f:
        b = f.read()
    assert(b==image)
    print("success!")

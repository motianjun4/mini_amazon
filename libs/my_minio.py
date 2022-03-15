from minio import Minio

minio_client = Minio("vcm.tinchun.top:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)

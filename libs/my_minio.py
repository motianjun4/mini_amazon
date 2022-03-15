from minio import Minio

minio_client = Minio("localhost:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)

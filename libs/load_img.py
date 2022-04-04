from my_minio import put_file
from faker import Faker

num_products = 2000


fake = Faker()
for i in range(1, num_products+1):
    image: str = fake.image(image_format='jpeg')
    with open(f'/tmp/{i}.jpg', 'wb') as f:
        f.write(image)
    put_file("image", f"product_{i}.jpg", f"/tmp/{i}.jpg")


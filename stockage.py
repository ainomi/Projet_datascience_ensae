import s3fs
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

MY_BUCKET = "jhajjar"
target_path = f"{MY_BUCKET}/Diffusion/"
try:
    fs.put("/home/onyxia/work/Projet_datascience_ensae/post_processed_listings.csv", target_path)
    print(f"File uploaded to {target_path}")
except Exception as e:
    print(f"Error uploading file: {e}")
    
import s3fs
import pandas as pd
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
MY_BUCKET = "jhajjar"
FILE_PATH_S3 = f"{MY_BUCKET}/Diffusion/listings.csv"
with fs.open(FILE_PATH_S3, "r") as file_in:
    df = pd.read_csv(file_in)

print(df.head())
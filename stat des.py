import s3fs
import pandas as pd
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
MY_BUCKET = "jhajjar"
FILE_PATH_S3 = f"{MY_BUCKET}/Diffusion/listings.csv"
with fs.open(FILE_PATH_S3, "r") as file_in:
    listings = pd.read_csv(file_in)

listings.dropna(inplace=True)
nv_noms = {'hektor-fmpconsults-474' : 'ID', 'Appartement' : 'Type', '3' : 'Number_of_rooms', '75001 Paris 1er (Vendôme)' : 'localisation', '61' : 'sqm2','847 600 €' : 'price'}
listings.rename(columns= nv_noms, inplace=True)
listings = listings.drop(['ID','localisation',axis=1])
print(listings.info())
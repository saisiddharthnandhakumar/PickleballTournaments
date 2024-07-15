import pandas as pd
from google.cloud import storage

try:
    csv_filename = 'bracket_data.csv'

    bucket_name = 'pickleballdata'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination_blob_name = f'{csv_filename}'  # The path to store in GCS

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(csv_filename)

    print(f"File {csv_filename} uploaded to GCS bucket {bucket_name} as {destination_blob_name}")
except Exception as e:
    print("Failed to Upload")
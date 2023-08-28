from google.cloud import storage

def uploadFileToBucket(keyPath, bucketName, filePath, uploadName):
    # Authenticate ourselves using the service account private key
    path_to_private_key = keyPath
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)

    bucket = storage.Bucket(client, bucketName)

    # Name of the file on the GCS once uploaded
    blob = bucket.blob(uploadName)
    # Path of the local file
    blob.upload_from_filename(filePath)
    
    #returns a public url
    return 'gs://' + blob.id[:-(len(str(blob.generation)) + 1)]

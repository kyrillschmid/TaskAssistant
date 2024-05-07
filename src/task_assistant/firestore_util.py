from google.cloud import firestore, storage
from google.oauth2 import service_account
from datetime import datetime
import streamlit as st
import json
import os



def write_to_firestore(data, file_url):
    #db = firestore.Client.from_service_account_json("firestore-key.json")

    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="task-assistant-159ac")
    
    department = data["department"]
    if department == "":
        department = "None"

    doc_ref = db.collection("summaries").document(str(department) + "-" + str(data["id"]))
    now = datetime.now()
    data = {**data, **{"created at": now, "file_url": file_url}}
    doc_ref.set(data)



def upload_summary_file(data):
    
    #storage_client = storage.Client.from_service_account_json("firestore-key.json")

    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    storage_client = storage.Client(credentials=creds, project="task-assistant-159ac")
    
    markdown_file_name = "summary-" + str(data["id"]) + ".md"
    with open(markdown_file_name, "w", encoding="utf-8") as markdown_file:
        print(data["summary"])
        markdown_file.write(data["summary"])

    bucket = storage_client.bucket("task-assistant-159ac.appspot.com")
    blob_path = f"uploads/{str(data['id'])}/{markdown_file_name}"
    blob = bucket.blob(blob_path)

    blob.upload_from_filename(markdown_file_name, content_type="text/markdown")

    blob.make_public()

    os.remove(markdown_file_name)

    return blob.public_url

def read_from_firestore():
    db = firestore.Client.from_service_account_json("firestore-key.json")
    summaries_ref = db.collection("posts")
        
    #for doc in summaries_ref.stream():
    #    st.write("The id is: ", doc.id)
    #    st.write("The contents are: ", doc.to_dict())
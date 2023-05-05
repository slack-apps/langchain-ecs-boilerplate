import logging
import os
from os import path

import boto3
from dotenv import load_dotenv
from flask import Flask, make_response
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from slack_bolt import App, Say, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler

from create_index import DB_DIR
from langchain_ecs_boilerplate.langchain_ecs_boilerplate_stack import INDEX_BUCKET

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ['SLACK_BOT_TOKEN'])
socket_mode_handler = SocketModeHandler(app, os.environ['SLACK_APP_TOKEN'])


def download_index():
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=INDEX_BUCKET)

    if not path.exists(DB_DIR):
        os.mkdir(DB_DIR)

    for content in response['Contents']:
        s3.download_file(INDEX_BUCKET, content['Key'], f'.db/{content["Key"]}')


def query(question: str):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(folder_path=DB_DIR, embeddings=embeddings)

    llm = OpenAI(temperature=0)

    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

    return chain.run(question)


@app.event('app_mention')
def handle_app_mention(event, say: Say, ack: Ack):
    ack()

    result = query(event['text'])
    say(text=result, thread_ts=event['ts'])


flask_app = Flask(__name__)


@flask_app.route('/health', methods=['GET'])
def slack_events():
    if socket_mode_handler.client is not None and socket_mode_handler.client.is_connected():
        return make_response('', 200)
    return make_response("The Socket Mode client is inactive", 503)


if __name__ == '__main__':
    download_index()

    socket_mode_handler.connect()
    flask_app.run(host='0.0.0.0', port=80)

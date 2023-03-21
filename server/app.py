from __future__ import print_function
from config import *

import tiktoken
import pinecone
import uuid
import sys
import logging
import json

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import request

from chatgpt_answer import get_chatgpt_answer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def load_pinecone_index() -> pinecone.Index:
    """
    Load index from Pinecone, raise error if the index can't be found.
    """
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV,
    )
    index_name = PINECONE_INDEX
    if not index_name in pinecone.list_indexes():
        print(pinecone.list_indexes())
        raise KeyError(f"Index '{index_name}' does not exist.")
    index = pinecone.Index(index_name)

    return index

def create_app():
    pinecone_index = load_pinecone_index()
    tokenizer = tiktoken.get_encoding("gpt2")
    app = Flask(__name__)
    app.pinecone_index = pinecone_index
    app.tokenizer = tokenizer

    CORS(app, supports_credentials=True)

    return app

app = create_app()

@app.route("/healthcheck", methods=["GET"])
@cross_origin(supports_credentials=True)
def healthcheck():
    return "OK"

@app.route("/get_bookname_list", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_bookname_list():
    try:
        # load books list from local file
        books_list = []
        with open("books-list.json", "r") as f:
            books_list = json.load(f)

        return jsonify(books_list)    
    except Exception as e:
        return str(e)

@app.route(f"/get_chatgpt_answer", methods=["POST"])
@cross_origin(supports_credentials=True)
def answer_question():
    try:
        params = request.get_json()
        question = params["question"]
        summary_level = params["summary_level"]
        book_name = params["book_name"]
        previous_question = "" #params["previous_question"]
        previous_answer = "" #params["previous_answer"]

        answer_question_response = get_chatgpt_answer(
            summary_level, book_name, question, previous_question, previous_answer, app.pinecone_index)

        return answer_question_response
    except Exception as e:
        return str(e)
    
if __name__ == "__main__":
    app.run(debug=True, port=SERVER_PORT, threaded=True)

# Books Q&A with ChatGPT

Books Q&A is a web app that lets you find answers in your books. You can ask questions related to their content, and the app will use embeddings and GPT to generate answers from the most relevant books. 

## Requirements

To run the app, you need:

- An OpenAI API key. You can create a new API key [here](https://beta.openai.com/account/api-keys).
- A Pinecone API key and index name. You can create a new account and index [here](https://www.pinecone.io/).
- Python 3.7 or higher and pipenv for the Flask server.
- Vue and pnpm 

## Set-Up and Development

### Server

Fill out the config.yaml file with your Pinecone API key, index name and environment.

Run the Flask server:

```
cd server
bash script/start "<your OPENAI_API_KEY>"
```

### Client

Please see README.md in client directory

## Limitations

The app may sometimes generate answers that are not in the files, or hallucinate about the existence of files that are not uploaded.

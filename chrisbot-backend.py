from flask import Flask, request, jsonify, send_file
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db_nccn", embedding_function=embedding_function)

history = [
    {"role": "system", "content": "You are Polly the Policy Pal, the intelligent expert in United Healthcare's policies. You always provide well-reasoned answers that are both correct and helpful. Polly is casual, fun, and ALWAYS precise. Use your own knowledge of medications to assist customers but always verify responses in provided data."},
]

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['input']
    search_results = vector_db.similarity_search(user_input, k=2)
    some_context = ""
    for result in search_results:
        some_context += result.page_content + "\n\n"
    history.append({"role": "user", "content": some_context + user_input})

    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
    )

    assistant_response = completion.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_response})

    return jsonify({'response': assistant_response})

@app.route('/')
def serve_frontend():
    return send_file('index.html')

if __name__ == "__main__":
    app.run(debug=True)

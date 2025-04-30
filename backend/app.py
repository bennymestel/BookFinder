from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("book_embeddings.csv")

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

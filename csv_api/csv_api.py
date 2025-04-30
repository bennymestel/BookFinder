from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV once into memory
df = pd.read_csv("book_embeddings.csv")

@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get("query", "").lower()
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # Find books that match the query in title or author (basic match)
    matches = df[df.apply(lambda row: query in str(row['book_title']).lower() or query in str(row['author']).lower(), axis=1)]

    if matches.empty:
        return jsonify({"message": "No matching books found."}), 404

    # Return top 5 results as JSON
    results = matches.head(5).to_dict(orient="records")
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

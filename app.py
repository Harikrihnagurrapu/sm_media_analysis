from flask import Flask,request,jsonify,render_template
from astrapy import DataAPIClient

app = Flask(__name__,)



client = DataAPIClient("AstraCS:QEaBKWXZNoAepEuJoZmIKxMX:ead3be262dd3fcf252b0bbb1e26c1c1ab6e7f52ee31223e8e05f8159a6a83374")
db = client.get_database_by_api_endpoint(
  "https://089188cf-78c4-4b40-b1c8-0b4dc4b6d731-us-east-2.apps.astra.datastax.com"
)
print(f"Connected to Astra DB: {db.list_collection_names()}"),db 

engagement_collection = db.get_collection("engagement_data")

# @app.route("/insert")
# def insert():
#   # Create a collection for social media engagement data
#   engagement_collection = db.create_collection("engagement_data")

#   # Insert mock engagement data
#   data = [
#       {"post_type": "carousel", "likes": 120, "shares": 15, "comments": 30},
#       {"post_type": "reels", "likes": 200, "shares": 40, "comments": 100},
#       {"post_type": "static_image", "likes": 80, "shares": 10, "comments": 20},
#       {"post_type": "carousel", "likes": 150, "shares": 25, "comments": 50},
#       {"post_type": "reels", "likes": 300, "shares": 60, "comments": 120},
#   ]

#   engagement_collection.insert_many(data)

#   return print("Mock engagement data inserted.")

@app.route('/analyze', methods=['POST'])
def analyze():
    # post_type = request.json.get('post_type')
    post_type = request.json.get('post_type') 
    if not post_type:
        return jsonify({"error": "Post type is required"}), 400
    # Retrieve all the results for the given post type and convert cursor to a list immediately
    results = list(engagement_collection.find({"post_type": post_type}))
    
    # Ensure that we have data to work with
    if not results:
        return jsonify({"error": "No data found for the given post type."}), 400

    # Calculate averages
    likes = [doc["likes"] for doc in results]
    shares = [doc["shares"] for doc in results]
    comments = [doc["comments"] for doc in results]
    
    avg_likes = sum(likes) / len(likes) if likes else 0
    avg_shares = sum(shares) / len(shares) if shares else 0
    avg_comments = sum(comments) / len(comments) if comments else 0
    
    # Return the analysis in a JSON response
    return jsonify({
        "post_type": post_type,
        "average_likes": avg_likes,
        "average_shares": avg_shares,
        "average_comments": avg_comments
    })

@app.route("/")
def test ():
  return render_template("index.html")
  


if __name__ == "__main__":
  app.run(debug=True)
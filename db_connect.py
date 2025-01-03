from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:QEaBKWXZNoAepEuJoZmIKxMX:ead3be262dd3fcf252b0bbb1e26c1c1ab6e7f52ee31223e8e05f8159a6a83374")
db = client.get_database_by_api_endpoint(
  "https://089188cf-78c4-4b40-b1c8-0b4dc4b6d731-us-east-2.apps.astra.datastax.com"
)

print(f"Connected to Astra DB: {db.list_collection_names()}")
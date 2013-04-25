from datamash import Client, Repository

# modify these with your API key - can be found at: https://datamash.io/dashboard
API_KEY = 'your-api-key'
URL = "http://www.bbc.co.uk/news/uk/"

client = datamash.Client(API_KEY)
repository = client.connect(URL)
print repository.resource(1).data["text"]
import datetime
import random
from datamash import Client, Repository

# Modify these with your credentials found at: https://datamash.io/dashboard
API_KEY = 'your-api-key'
REPOSITORY_KEY = 'your-custom-key'

client = Client(API_KEY)

date = datetime.datetime(2012, 1, 1)

for day in range(1, 10):
    # print out the current day we are sending data for
    print date

    data = []
    # 1440 minutes in one day
    for min in range (1, 1441):
        data.append(DataPoint(date, random.random() * 50.0))
        date = date + datetime.timedelta(minutes=1)

    client.write_key(SERIES_KEY, data)
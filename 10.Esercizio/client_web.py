import requests
import pandas as pd

books = requests.get("http://127.0.0.1:5000/api/v1/resources/books/all")
book = requests.get("http://127.0.0.1:5000/api/v1/resources/books", params={"id":'1'})
print(pd.DataFrame(books))
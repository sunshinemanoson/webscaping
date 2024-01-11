import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movie.db'
table_name = 'Top_50'
csv_path = '/home/project/top_50_films.csv'

df = pd.DataFrame(columns=["Average Rank", "Film", "Year", "Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

rows = data.find_all('tr')

for row in rows:
    if count < 10:
        col = row.find_all('td')
        if len(col) > 0:
            year = int(col[2].contents[0])
            if year >= 1000:
                data_dict = {
                    "Average Rank": col[0].contents[0],
                    "Film": col[1].contents[0],
                    "Year": col[2].contents[0],
                    "Rotten Tomatoes' Top 100": col[3].contents[0]
                }
                df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
                count += 1
    else:
        break

print(df)

conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()

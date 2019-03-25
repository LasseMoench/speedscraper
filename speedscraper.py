import requests
import sqlite3
import os
import datetime
from bs4 import BeautifulSoup

if not os.path.exists("speedtraps.db"):
    print("Datenbank tempdata.db nicht vorhanden - Datenbank wird anglegt.")
    connection = sqlite3.connect("speedtraps.db")
    cursor = connection.cursor()
    # Tabelle erzeugen
    sql = 'CREATE TABLE speedTraps(datum TEXT, stadt TEXT, strasse TEXT)'
    cursor.execute(sql)
    connection.commit()
    connection.close()


url = 'https://aachen.polizei.nrw/geschwindigkeitskontrollen-in-aachen'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table_rows = soup.find_all('tr')

print("Guten Morgen!\r\nHeute wird an folgenden Orten geblitzt:")

for row in table_rows:
    cols = row.find_all('td')
    cols = [element.text.strip() for element in cols]
    if cols[1]:
        current_date = datetime.datetime.strptime(cols[1], "%d.%m.%Y").date()
    if current_date == datetime.date.today():
        if cols[2] != '':
            connection = sqlite3.connect('speedtraps.db')
            sql = 'INSERT INTO speedTraps VALUES (' + current_date.strftime("%d.%m.%Y") + ', ' + cols[2] + cols[3] + ')'
            connection.execute(sql)
            connection.commit()
            connection.close()
            str_to_print = cols[2] + ', ' + cols[3].replace(u'\xa0', u' ')
            print(str_to_print)
            # TODO: Send signal Message

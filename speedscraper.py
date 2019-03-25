import requests
import sqlite3
import os
import datetime
import subprocess
from bs4 import BeautifulSoup

phone_nums = ["+4915731234567", "+4915787654321"]

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

message = "Guten Morgen!\r\nIch bin's, der Blitzerbot. Heute wird an folgenden Orten geblitzt:\r\n"

for row in table_rows:
    cols = row.find_all('td')
    cols = [element.text.strip() for element in cols]
    if cols[1]:
        current_date = datetime.datetime.strptime(cols[1], "%d.%m.%Y").date()
    if current_date == datetime.date.today():
        if cols[2] != '':
            connection = sqlite3.connect('speedtraps.db')
            sql = 'INSERT INTO speedTraps VALUES ("' + current_date.strftime("%d.%m.%Y") + '", "' + cols[2] + '","' + cols[3] + '")'
            print(sql)
            connection.execute(sql)
            connection.commit()
            connection.close()
            message = message + cols[2] + ', ' + cols[3].replace(u'\xa0', u' ') + "\r\n"

for phone_num in phone_nums:
    res = subprocess.check_output(["signal-cli", "-u", "+4915731234567", "send", "-m", message, phone_num])
    for line in res:
        print(line)

import sqlite3
import pytz
import datetime
import csv
from django.utils import timezone
import numpy as np

#def import_database_table():
conn = sqlite3.connect('db.sqlite3')
ptr = conn.cursor()

tz=pytz.timezone('America/New_York')
dt=datetime.datetime.now()

 #----------------------------------------------------------------------------------------
with open('ingedients_inventory.csv') as csv_file:
  field_names = ["inventory_id","name","units","price_per_unit","safety_stock","date_purchased"]
  csv_reader = csv.DictReader(csv_file, fieldnames=field_names)
  line_count = 0
  for row in csv_reader:
    params = (int(row["inventory_id"]), row["name"],int(row["units"]),int(row["safety_stock"]), float(row["price_per_unit"]),datetime.date.today())
    ptr.execute("INSERT INTO manageInventory_inventory VALUES (?,?,?,?,?,?)", params)
    conn.commit()
    print(f'{row["inventory_id"]}\t{row["name"]}\t{row["price_per_unit"]}\t{row["safety_stock"]}')
 #-----------------------------------------------------------------------------------------


#ptr.execute("SELECT * FROM home_item WHERE id=8")


#print(ptr.fetchone())
#conn.commit()

conn.close()

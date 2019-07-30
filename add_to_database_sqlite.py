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

 #ptr.execute("""CREATE TABLE Inventory (
 #               id integer,
  #              name text,
   #             price_per_lb real,
    #            stock_in_lbs integer
     #           )""")
 
 #ptr.execute("""CREATE TABLE JDelInventory (
 #               id integer,
 #               name text,
 #               price real,
 #               ingredients text
 #               )""")     
     

 #ptr.execute("INSERT INTO Inventory VALUES (00110, 'SEABASS', 2.15, 15)")
 #conn.commit()

 #----------------------------------------------------------------------------------------
with open('chopt_menu.csv') as csv_file:
  field_names = ["item_id","item_name","price", "ingredients","calories","vegan","image","description"]
  csv_reader = csv.DictReader(csv_file, fieldnames=field_names)
  line_count = 0
  for row in csv_reader:
    params = (int(row["item_id"]),int(row["item_id"]), row["item_name"], float(row["price"]), row["ingredients"],int(row["calories"]),row["vegan"],row["image"],row["description"])
    ptr.execute("INSERT INTO home_item VALUES (?,?,?,?,?,?,?,?,?)", params)
    conn.commit()
    print(f'{row["item_id"]}\t{row["item_name"]}\t{row["price"]}\t{row["calories"]}\t{row["ingredients"]}\n{row["description"]}\t{row["vegan"]}\t{row["image"]}')
 #-----------------------------------------------------------------------------------------


#ptr.execute("SELECT * FROM home_item WHERE id=8")


#print(ptr.fetchone())
#conn.commit()

conn.close()

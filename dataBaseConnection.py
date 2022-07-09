import mysql.connector

# Creating MYSQL connection an d using credicxo Database
mydb = mysql.connector.connect(
  host="db-mysql-nyc3-05367-do-user-7517930-0.b.db.ondigitalocean.com",
  user="doadmin",
  password="AVNS_G00es_hIZywDKVq2TU2",
  port= 25060,
  database="credicxo"
)
print("[*] Database Connected")
mycursor = mydb.cursor()
try:
    # Creating a table to store product Information
    mycursor.execute('''
    CREATE TABLE productInformation 
                     (id INT AUTO_INCREMENT PRIMARY KEY, 
                     link VARCHAR(255), 
                     productTitle VARCHAR(255), 
                     imageURL VARCHAR(255), 
                     productPrice VARCHAR(255), 
                     productDetails LONGTEXT )
    ''')
except:
    pass    # Ignoring this step if database already exists

# Function to execute INSERT command in DB
def dumpInDatabase(jsonData):
    val = []
    # SQL command to INSERT
    sql = "INSERT INTO productInformation (link, productTitle, imageURL, productPrice, productDetails) VALUES (%s, %s, %s, %s, %s)"
    # Serializing for MYSQL
    for link in jsonData:
        val.append((link,jsonData[link]["Product Title"],
                    jsonData[link]["Product Image URL"],
                    jsonData[link]["Price of the Product"],
                    jsonData[link]["Product Details"]))
        
    mycursor.executemany(sql, val)
    mydb.commit()   # Final commit to DB
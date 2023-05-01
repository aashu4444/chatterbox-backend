
import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="ashutosh",
  passwd ="ashu@hackingTools",
  port='3306'
)
 
cursorObject = dataBase.cursor()
 
cursorObject.execute("CREATE DATABASE chatterbox_db")
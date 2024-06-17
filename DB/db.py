# import MySQLdb
import mysql.connector
class Mysqlconfig(): 
# Create a connection to the database
    # mysql=mysql.connector
    error=mysql.connector.Error
    conn = mysql.connector.connect(host='localhost',user='root',password='Friday@123',database='systemadmin')
    cursor=conn.cursor()

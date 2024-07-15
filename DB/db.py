# import MySQLdb
# import mysql.connector
import pymysql
class Mysqlconfig(): 
# Create a connection to the database
    # mysql=mysql.connector
    # error=mysql.connector.Error
    # conn = mysql.connector.connect(host='localhost',user='root',password='Friday@123',database='systemadminapp')
    # cursor=conn.cursor()
    conn=pymysql.connect(host='localhost',
    user='root',
    password='Friday@123',
    database='systemadminapp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    error=pymysql.Error

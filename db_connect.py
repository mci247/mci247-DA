import pymysql.cursors
import MySQLdb
import pymysql
# pymysql.install_as_MySQLdb()


host = "202.92.4.71"
user = "qfzovpphosting_thaitn"
password = "Xngancon9x"
db = "qfzovpphosting_MCI_Database"
database = MySQLdb.connect(host=host, user=user, password=password, db=db)
cursor = database.cursor()


def getMobile():
    query = """ SELECT mobile FROM nhanvien_elead """
    cursor.execute(query)
    result = cursor.fetchall()
    print("I just fetched data from MCI DB")
    return result


def insertData(name, mobile, gender, address, source_lead, note, page_id):
    query = """INSERT INTO nhanvien_elead(name, mobile, gender, email, source_lead, note, study_abroad)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    values = (name, mobile, gender, address, source_lead, note, page_id)
    cursor.execute(query, values)
   


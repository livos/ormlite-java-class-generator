import sys
import sqlite3
from classes.Column import Column
from classes.JavaClass import JavaClass

def main():
    DB_PATH = "full_path_to_db"
    PACKAGE_NAME = "package_name;"

    MESSAGE_PROCESSING = "Processing table "
    QUERY_GET_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
    QUERY_GET_COLUMNS = "PRAGMA table_info('%s')"  


    dbCon = sqlite3.connect(DB_PATH)
    cursor = dbCon.cursor()

    # Get tables
    result = cursor.execute(QUERY_GET_TABLES)
    tableNames = sorted(zip(*result)[0])

    for tableName in tableNames:
        columns = []
        print  MESSAGE_PROCESSING + tableName
        rawColumns = cursor.execute(QUERY_GET_COLUMNS % tableName).fetchall()

        for rawColumn in rawColumns:
            column = Column(rawColumn[1], rawColumn[2], True if rawColumn[5] == 1 else False)
            columns.append(column)

        javaClass = JavaClass(tableName,columns,PACKAGE_NAME)
        javaClass.createJavaFile()
    cursor.close()
    dbCon.close()



if __name__ == '__main__':
    sys.exit(main())
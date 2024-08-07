---
title: python mysql 연동하기
layout: default
parent: DataBase
nav_order: 6
permalink: /db/python_mysql1
---

# python mysql 연동

## 1. mysql

[샘플데이터 다운로드](../data/pub.sql)

## 2. python

### 1. 라이브러리 설치
```bash
pip install mysql-connector-python
```
### 2. 연결테스트
01_connect.py
```python
import mysql.connector

# Initialize a variable to hold the database connection
conn = None

try:
    # Attempt to establish a connection to the MySQL database
    conn = mysql.connector.connect(host='localhost', 
                                   port=3306,
                                   database='pub',
                                   user='<user>',
                                   password='<password>')
    
    # Check if the connection is successfully established
    if conn.is_connected():
        print('Connected to MySQL database')

except mysql.connector.Error as e:
    # Print an error message if a connection error occurs
    print(e)

finally:
    # Close the database connection in the 'finally' block to ensure it happens
    if conn is not None and conn.is_connected():
        conn.close()
```

### 3. 연결정보 configuration file로 분리 작성
app.ini
```ini
[mysql]
host = localhost
port = 3306
database = pub
user = <user>
password = <password>
```

config.py
```python
from configparser import ConfigParser

def read_config(filename='app.ini', section='mysql'):    
    # Create a ConfigParser object to handle INI file parsing
    config = ConfigParser()
    
    # Read the specified INI configuration file
    config.read(filename)

    # Initialize an empty dictionary to store configuration data
    data = {}

    # Check if the specified section exists in the INI file
    if config.has_section(section):
        # Retrieve all key-value pairs within the specified section
        items = config.items(section)

        # Populate the data dictionary with the key-value pairs
        for item in items:
            data[item[0]] = item[1]
    else:
        # Raise an exception if the specified section is not found
        raise Exception(f'{section} section not found in the {filename} file')

    # Return the populated data dictionary
    return data

if __name__ == '__main__':
    # Read the configuration from the default section ('mysql') in the 'app.ini' file
    config = read_config()

    # Display the obtained configuration
    print(config)

```

02_connect.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config


def connect(config):
    """ Connect to MySQL database """
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**config)

        if conn.is_connected():
            print('Connection is established.')
        else:
            print('Connection is failed.')
    except Error as error:
        print(error)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection is closed.')


if __name__ == '__main__':
    config = read_config()
    connect(config)
```

### 4. select 

#### fetchone()

fetchone.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config

def query_with_fetchone(config):
    # Initialize variables for cursor and connection
    cursor = None
    conn = None

    try:
        # Establish a connection to the MySQL database using the provided configuration
        conn = MySQLConnection(**config)
        
        # Create a cursor to interact with the database
        cursor = conn.cursor()
        
        # Execute a SELECT query to retrieve all rows from the 'books' table
        cursor.execute("SELECT * FROM books")

        # Fetch the first row
        row = cursor.fetchone()

        # Loop through all rows and print them
        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        # Print an error message if an error occurs during the execution of the query
        print(e)

    finally:
        # Close the cursor and connection in the 'finally' block to ensure it happens
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    # Read the database configuration from the 'config' module
    config = read_config()
    
    # Call the function with the obtained configuration to execute the query
    query_with_fetchone(config)

```

#### fetchmany()

fetchmany.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config

def iter_row(cursor, size=10):
    # Infinite loop to fetch rows in chunks of 'size' from the result set
    while True:
        rows = cursor.fetchmany(size)
        # Break the loop if there are no more rows to fetch
        if not rows:
            break

        # Yield each row in the fetched chunk
        for row in rows:
            yield row

def query_with_fetchmany(config):
    # Initialize variables for connection and cursor
    conn = None
    cursor = None

    try:
        # Establish a connection to the MySQL database using the provided configuration
        conn = MySQLConnection(**config)
        
        # Create a cursor to interact with the database
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve all rows from the 'books' table
        cursor.execute("SELECT * FROM books")

        # Iterate over rows using the custom iterator function 'iter_row'
        for row in iter_row(cursor, 10):
            print(row)

    except Error as e:
        # Print an error message if an error occurs during the execution of the query
        print(e)

    finally:
        # Close the cursor and connection in the 'finally' block to ensure it happens
        if cursor:
            cursor.close()
        
        if conn:
            conn.close()

if __name__ =='__main__' :
    # Read the database configuration from the 'config' module
    config = read_config()
    
    # Call the function with the obtained configuration to execute the query
    query_with_fetchmany(config)

```

#### fetchall()

fetchall.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config

def query_with_fetchall(config):
    try:
        config = read_config()
        # Establish a connection to the MySQL database using the provided configuration
        conn = MySQLConnection(**config)
        
        # Create a cursor to interact with the database
        cursor = conn.cursor()
        
        # Execute a SELECT query to retrieve all rows from the 'books' table
        cursor.execute("SELECT * FROM books")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print the total number of rows returned by the query
        print('Total Row(s):', cursor.rowcount)
        
        # Loop through all rows and print them
        for row in rows:
            print(row)
        return rows

    except Error as e:
        # Print an error message if an error occurs during the execution of the query
        print(e)

    finally:
        # Close the cursor and connection in the 'finally' block to ensure it happens
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Call the function with the obtained configuration to execute the query
    query_with_fetchall()

```

### 5. insert

insertData.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config

def insert_book(title, isbn):
    query = "INSERT INTO books(title,isbn) " \
            "VALUES(%s,%s)"

    args = (title, isbn)
    book_id = None
    try:
        config = read_config()
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                book_id =  cursor.lastrowid
            conn.commit()
        return book_id
    except Error as error:
        print(error)

if __name__ == '__main__':
    insert_book('A Sudden Light', '9781439187036')
```

### 6. update

updateData.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config

def update_book(book_id, title):
    # read database configuration
    config = read_config()

    # prepare query and data
    query = """ UPDATE books
                SET title = %s
                WHERE id = %s """

    data = (title, book_id)

    affected_rows = 0  # Initialize the variable to store the number of affected rows

    try:
        # connect to the database
        with MySQLConnection(**config) as conn:
            # update book title
            with conn.cursor() as cursor:
                cursor.execute(query, data)

                # get the number of affected rows
                affected_rows = cursor.rowcount

            # accept the changes
            conn.commit()

    except Error as error:
        print(error)

    return affected_rows  # Return the number of affected rows

if __name__ == '__main__':
    affected_rows = update_book(37, 'The Giant on the Hill *** TEST ***')
    print(f'Number of affected rows: {affected_rows}')

```

### 7. delete

deleteData.py
```python
from mysql.connector import MySQLConnection, Error
from config import read_config

def delete_book(book_id):
    # read database configuration
    config = read_config()

    # prepare query and data
    query = "DELETE FROM books WHERE id = %s"

    data = (book_id, ) 

    affected_rows = 0  # Initialize the variable to store the number of affected rows

    try:
        # connect to the database
        with MySQLConnection(**config) as conn:
            # update book title
            with conn.cursor() as cursor:
                cursor.execute(query, data)

                # get the number of affected rows
                affected_rows = cursor.rowcount

            # accept the changes
            conn.commit()

    except Error as error:
        print(error)

    return affected_rows  # Return the number of affected rows

if __name__ == '__main__':
    affected_rows = delete_book(37)
    print(f'Number of affected rows: {affected_rows}')

```

### 8. flask에서 호출

app.py
```python
from flask import Flask,render_template,redirect
from fetchall import query_with_fetchall
from insertData import insert_book
from updateDate import update_book
from deleteData import delete_book

app = Flask(__name__)

@app.route('/')
def index():
  datas = query_with_fetchall()
  return render_template('list.html',datas=datas)

@app.route('/insert/<title>/<isbn>')
def insert(title,isbn):
  insert_book(title, isbn)
  return redirect('/')

@app.route('/update/<int:id>/<title>')
def update(id,title):
  affected_rows = update_book(id, title)
  print(f'Number of affected rows: {affected_rows}')
  return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
  affected_rows = delete_book(id)
  print(f'Number of affected rows: {affected_rows}')
  return redirect('/')

if  __name__ == '__main__':  
    app.run(debug=True)

```

templates/list.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <table border = 1>
    {% for item in datas %}
    
       <tr>
          <td> {{ item }} </td>
       </tr>
       
    {% endfor %}
 </table>

</body>
</html>
```
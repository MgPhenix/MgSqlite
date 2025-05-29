# MgSqlite

**MgSqlite** is a Python module that simplifies the creation and interaction with SQLite databases without the need to write raw SQL commands. Instead, you use built-in functions to create, update, and query your database. It’s particularly well-suited for integration with Tkinter-based GUI applications.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
  - [Database Module](#database-module)
  - [SQL_Execution Module](#sql_execution-module)
  - [Table Module](#table-module)
- [GUI Integration](#gui-integration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **No SQL Required:** Create and interact with SQLite databases using Python functions.
- **Simplified SQL Execution:** Execute any SQL command with proper error handling.
- **Table Management:** Create tables with dynamic column definitions, insert data, update records, and delete tables.
- **Debug Capabilities:** Optionally print SQL commands for troubleshooting.
- **Tkinter GUI Support:** Easily view table data using the built-in TableViewer.
- **Version:** 0.5

## Installation

Make sure you have Python 3.x installed. Both SQLite and Tkinter are part of the standard Python distribution. To install MgSqlite, clone the repository:
```
```bash
git clone https://github.com/MgPhenix/MgSqlite.git
cd MgSqlite
```

Then include the module in your Python project:

```python
from MgSqlite import Database, SQL_Execution, Table
```
Usage
Here’s a simple example to get you started. This example shows how to create a database, define a table, insert data, and query records:

```python
from MgSqlite.database import Database
from MgSqlite.table import Table

# Initialize a new database (creates "my_database.db")
db = Database(name="my_database")
db.turnOnPrintSQL()  # Enable printing of SQL commands for debugging

# Define table columns as a list of tuples.
# Each tuple is structured as: 
#    (column name, Python type, is_primary_key (bool), autoincrement (bool))
columns = (
    ("id", int, True, True),
    ("name", str, False, False),
    ("age", int, False, False)
)

# Create a new table called "users" in the database
users_table = Table(name="users", database=db, value=columns)

# Insert a new record into the "users" table
users_table.addValue(values=(None, "Alice", 30))  # 'None' for auto-incremented primary key

# Query records from the table where age equals 30
result = users_table.selectValues(["id", "name", "age"], ("age", 30))
print(result)
```
In this example, the module creates a SQLite file (my_database.db), sets up a table named users, and demonstrates how to add and fetch records without writing any SQL manually.

## API Reference
### Database Module:
Located in ```database.py```

The Database class is responsible for managing your SQLite database file. It provides the following features:

- **Initialization:** Creates (or connects to) a database file with a .db extension and tests connectivity.

- **Print Control:** Use ```turnOnPrintSQL()``` and ```turnOffPrintSQL()``` to enable or disable the printing of SQL commands for debugging purposes.

- **Deletion Methods**:

  - ```deleteAllTable()```: Deletes all tables that have been created in the current database.

  - ```deleteDatabase()```: Removes the entire database file from your system.

### SQL_Execution Module
Located in ```sql_interraction.py```

The SQL_Execution class provides core functionalities to execute SQL commands:

- ```simpleExecute(database, command, list=[])```: Executes an SQL command on the provided database object. This method:

  - Connects to the SQLite database using the database name.

  - Prints the SQL command and parameters if printSQL is enabled.

  - Executes the command, fetches results (if applicable), commits the transaction, and closes the connection.

  - Returns the fetched results if the command yields any, otherwise returns None.

- ```_tryConnect(databaseName)```: A helper method that attempts to establish a connection to the specified database. If the connection fails, it prints an error message.

### Table Module
Located in ```table.py```

The ```Table``` class encapsulates functionalities to manage a table within the database:

- **Initialization:** When you create a table, you pass parameters (via keyword arguments) including:

  - ```name```: The name of the table.

  - ```database```: A Database object where the table belongs.

  - ```value```: A list of tuples defining the columns. Each tuple should be in the form ```(column_name, type, is_primary_key, autoincrement)```.

  The table is then created by dynamically constructing and executing a ```CREATE TABLE``` SQL command.

- **Column Handling:** Uses private methods:

  - ```__createColumns(args)```: Constructs a string representing the SQL column definitions.

  - ```__checkType(var)```: Converts Python data types (```int```, ```str```, or ```float```) into their corresponding SQLite types (```INTEGER```, ```TEXT```, or ```REAL```).

- **Table Operations:**

  - ```addValue(values, columns=[])```: Inserts a new record into the table.

  - ```updateValue(columnEqualityList, *args)```: Updates specific rows with new values based on provided conditions.

  - ```selectValues(columnsList, *args)```: Retrieves specific columns from table records that match the given conditions (using ```AND``` logic).

  - ```_selectValuesOR(columnsList, args)```: (Temporary function) Retrieves data with conditions joined using ```OR``` instead of ```AND```.

  - ```selectAll()```: Retrieves all records from the table.

  - ```deleteTable()```: Drops the table if it exists.

  - **GUI Integration:** The ```show()``` method calls an external Tkinter-based TableViewer (defined in ```gui.py```) that displays the table’s contents in a graphical window.

## GUI Integration
Although the actual GUI code is maintained in gui.py, you can easily display your table data by calling the ```show()``` method on a Table object:

```python
# Launch a Tkinter window to view the "users" table data
users_table.show()
```
This feature leverages Tkinter to provide a simple, visual representation of your data.

## Contributing
Contributions are welcome! If you have suggestions for improvements or wish to add new features, please follow these steps:

Fork the repository.

Create a new branch:

bash```
git checkout -b feature/MgSqlite```
Commit your changes with a descriptive message:

bash```
git commit -m "Add description of the new feature"```

Push to your branch:

bash```
git push origin feature/MgSqlite```
Open a Pull Request with a clear explanation of your changes.

## License
This project is licensed under the MIT License.


    

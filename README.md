
 📚 Library Management System

<p align="center">
  <strong>A Python & MySQL Database Management Project</strong>
</p>

<p align="center">
  A menu-driven application for managing books, tracking issued records, maintaining member details, and processing book returns.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Interface-CLI-lightgrey" alt="Command Line Interface">
</p>

```text
 📌 Overview

The **Library Management System** is a Python-based application that uses MySQL to store and manage library records.

It provides a simple menu-driven interface for adding and updating books, viewing available records, searching for books, issuing books to members, and managing returns.

The project demonstrates practical implementation of Python programming, relational database connectivity, SQL queries, input validation, and database transaction handling.

 ✨ Features

- **View Books:** Display stored book records and their available quantities.
- **Search Books:** Find books by entering a full or partial book name.
- **Add Books:** Add new books with quantity and price-per-day details.
- **Update Books:** Modify book names, available quantities, and prices.
- **Issue Books:** Record member details and issue dates when books are issued.
- **Member Management:** View issued-book records and search member information.
- **Return Books:** Process book returns using member details and issue records.
- **Return Charge Calculation:** Process the return-date and charge calculation implemented in the application.
- **MySQL Database:** Store book and issue records persistently.
- **Input Validation:** Handle invalid entries and prevent negative quantity or price values.
- **Database Setup:** Create the database and required tables automatically after a successful MySQL connection.

 🛠️ Technologies Used
______________________________________________________________________________
| Technology             | Purpose                                           |
|------------------------|---------------------------------------------------|
| Python                 | Application logic and menu handling               |
| MySQL                  | Persistent storage of library records             |
| MySQL Connector/Python | Connect Python to MySQL                           |
| SQL                    | Create, read, search, and update database records |
| Git & GitHub           | Version control and project hosting               |
------------------------------------------------------------------------------
 ⚙️ Prerequisites

Before running the application, make sure you have:

- Python installed on your computer.
- MySQL Server installed and running.
- A MySQL account with permission to create and modify the project database.
- Internet access to install the required Python package.



 🚀 Installation and Setup

1. Clone the Repository

Open your terminal or PyCharm terminal and run:
```
```bash
git clone https://github.com/divyanshu-sengar/Library-Management-System.git
```

2. Open the Project Directory

```bash
cd Library-Management-System
```

3. Install the Required Dependency

```bash
python -m pip install mysql-connector-python
```

4. Configure the MySQL Connection

Open `Library Management System.py` and locate the database settings near the top of the file.

Configure these values to match your local MySQL installation:

```python
DB_HOST = "localhost"
DB_USER = "your_mysql_username"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "library"
```

Replace the example username and password with your own MySQL credentials.

**Security note:** Do not publish real database passwords or other secrets in your public GitHub repository.

5. Run the Application

Ensure MySQL Server is running, then execute:

```bash
python "Library Management System.py"
```

After a successful connection, the application sets up the required database and tables and displays the main menu.

 🖥️ Main Menu

The application provides these main options:

```text
============================================================
              LIBRARY MANAGEMENT SYSTEM
============================================================

1. View all books
2. Search for a book
3. Issue a book
4. Add new book
5. Update book
6. Member details
7. Exit

============================================================
```

Select an option by entering its corresponding number and follow the on-screen instructions.

 📂 Project Structure

```text
Library-Management-System/
│
├── Library Management System.py
│   └── Main application, MySQL connection,
│       database setup, and library operations
│
└── README.md
    └── Project documentation and setup instructions
```

 🎓 Learning Objectives

This project provides practical experience with:

- Python functions, loops, and conditional statements.
- Exception handling and input validation.
- MySQL database connectivity.
- SQL queries and database table management.
- CRUD operations for library records.
- Book issue and return workflows.
- Database commits and rollbacks.
- Building a menu-driven command-line application.

 🔮 Future Improvements

Potential enhancements for future versions include:

- A graphical user interface (GUI).
- Separate administrator and member login systems.
- Book categories, authors, and ISBN tracking.
- Dedicated return-history and transaction records.
- Improved reports for issued and available books.
- Secure configuration using environment variables.
- Automated tests and improved error reporting.

 👨‍💻 Author

**Divyanshu Sengar**

BCA Student | Python Developer

- **GitHub Profile:** [divyanshu-sengar](https://github.com/divyanshu-sengar)
- **Project Repository:** [Library Management System](https://github.com/divyanshu-sengar/Library-Management-System)

 🙌 Acknowledgements

- [Python](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)

---

<p align="center">
  <strong>Thanks for visiting this project!</strong>
</p>

<p align="center">
  If you find this project useful, consider giving the repository a ⭐ star.
</p>


        



```

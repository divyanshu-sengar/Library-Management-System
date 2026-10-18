import mysql.connector as sqlctr
import sys
from datetime import datetime


# ============================================================
#                    DATABASE SETTINGS
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "galway"
DB_NAME = "library"


# ============================================================
#                    CONNECT TO MYSQL
# ============================================================

try:
    mycon = sqlctr.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

    if not mycon.is_connected():
        print("Unable to connect to MySQL.")
        sys.exit()

    print("\n")
    print("==============================================")
    print("   LIBRARY MANAGEMENT SYSTEM")
    print("   Project prepared by DIVYANSHU SENGAR")
    print("==============================================")

except sqlctr.Error as err:
    print("MySQL connection error:", err)
    sys.exit()


cursor = mycon.cursor()


# ============================================================
#                    DATABASE SETUP
# ============================================================

def setup_database():

    try:
        # Create database
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        # Select database
        cursor.execute(
            f"USE {DB_NAME}"
        )

        # ----------------------------------------------------
        # Create books table if it doesn't exist
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                SN INT NOT NULL AUTO_INCREMENT,
                Book_Name VARCHAR(100) NOT NULL,
                Quantity_Available INT NOT NULL DEFAULT 0,
                Price_Per_Day INT NOT NULL DEFAULT 0,
                PRIMARY KEY (SN)
            )
        """)

        # ----------------------------------------------------
        # Create issue table if it doesn't exist
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issue (
                SN INT NOT NULL AUTO_INCREMENT,
                Member VARCHAR(100) NOT NULL,
                book_issue VARCHAR(100) NOT NULL,
                issue_date DATE NOT NULL,
                contact_no VARCHAR(20) NOT NULL,
                PRIMARY KEY (SN)
            )
        """)

        # ----------------------------------------------------
        # FIX OLD "books" TABLE
        # ----------------------------------------------------

        cursor.execute("SHOW COLUMNS FROM books")
        book_columns = cursor.fetchall()

        book_column_names = [
            column[0] for column in book_columns
        ]

        # Fix SN
        if "SN" in book_column_names:

            try:
                cursor.execute("""
                    ALTER TABLE books
                    MODIFY SN INT NOT NULL AUTO_INCREMENT
                """)
            except sqlctr.Error:
                pass

        # Add missing Book_Name
        if "Book_Name" not in book_column_names:

            cursor.execute("""
                ALTER TABLE books
                ADD COLUMN Book_Name VARCHAR(100) NOT NULL
            """)

        # Add missing Quantity_Available
        if "Quantity_Available" not in book_column_names:

            cursor.execute("""
                ALTER TABLE books
                ADD COLUMN Quantity_Available INT NOT NULL DEFAULT 0
            """)

        # Add missing Price_Per_Day
        if "Price_Per_Day" not in book_column_names:

            cursor.execute("""
                ALTER TABLE books
                ADD COLUMN Price_Per_Day INT NOT NULL DEFAULT 0
            """)

        # ----------------------------------------------------
        # FIX OLD "issue" TABLE
        # ----------------------------------------------------

        cursor.execute("SHOW COLUMNS FROM issue")
        issue_columns = cursor.fetchall()

        issue_column_names = [
            column[0] for column in issue_columns
        ]

        # Fix SN
        if "SN" in issue_column_names:

            try:
                cursor.execute("""
                    ALTER TABLE issue
                    MODIFY SN INT NOT NULL AUTO_INCREMENT
                """)
            except sqlctr.Error:
                pass

        # ----------------------------------------------------
        # OLD PROGRAM USED "date"
        #
        # New program uses "issue_date"
        # ----------------------------------------------------

        if (
            "date" in issue_column_names
            and "issue_date" not in issue_column_names
        ):

            cursor.execute("""
                ALTER TABLE issue
                CHANGE COLUMN date issue_date DATE NOT NULL
            """)

        # If issue_date doesn't exist for some reason
        cursor.execute("SHOW COLUMNS FROM issue")
        issue_columns = cursor.fetchall()

        issue_column_names = [
            column[0] for column in issue_columns
        ]

        if "issue_date" not in issue_column_names:

            cursor.execute("""
                ALTER TABLE issue
                ADD COLUMN issue_date DATE NOT NULL
            """)

        # Add missing Member
        if "Member" not in issue_column_names:

            cursor.execute("""
                ALTER TABLE issue
                ADD COLUMN Member VARCHAR(100) NOT NULL
            """)

        # Add missing book_issue
        if "book_issue" not in issue_column_names:

            cursor.execute("""
                ALTER TABLE issue
                ADD COLUMN book_issue VARCHAR(100) NOT NULL
            """)

        # Fix contact number
        try:
            cursor.execute("""
                ALTER TABLE issue
                MODIFY contact_no VARCHAR(20) NOT NULL
            """)
        except sqlctr.Error:
            pass

        # Add contact number if completely missing
        cursor.execute("SHOW COLUMNS FROM issue")
        issue_columns = cursor.fetchall()

        issue_column_names = [
            column[0] for column in issue_columns
        ]

        if "contact_no" not in issue_column_names:

            cursor.execute("""
                ALTER TABLE issue
                ADD COLUMN contact_no VARCHAR(20) NOT NULL
            """)

        mycon.commit()

        print("\nDatabase setup completed successfully.")

    except sqlctr.Error as err:

        print("\nDatabase setup error:", err)

        try:
            mycon.rollback()
        except:
            pass

        sys.exit()


setup_database()


# ============================================================
#                    UTILITY FUNCTIONS
# ============================================================

def execute_query(sql, values=None):

    try:

        if values is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, values)

        return True

    except sqlctr.Error as err:

        print("\nDatabase error:", err)
        return False


def get_all(sql, values=None):

    if not execute_query(sql, values):
        return []

    try:
        return cursor.fetchall()

    except sqlctr.Error as err:

        print("Error while fetching data:", err)
        return []


def get_one(sql, values=None):

    if not execute_query(sql, values):
        return None

    try:
        return cursor.fetchone()

    except sqlctr.Error as err:

        print("Error while fetching data:", err)
        return None


def pause():

    input("\nPress ENTER to continue...")


# ============================================================
#                    SHOW ALL DATA
# ============================================================

def all_data(table_name):

    allowed_tables = ["books", "issue"]

    if table_name not in allowed_tables:

        print("Invalid table name.")
        return

    try:

        cursor.execute(
            f"DESCRIBE {table_name}"
        )

        columns = cursor.fetchall()

        column_names = []

        for column in columns:
            column_names.append(column[0])

        cursor.execute(
            f"SELECT * FROM {table_name}"
        )

        rows = cursor.fetchall()

        print("\n")
        print("=" * 70)
        print(f"              ALL DATA FROM {table_name.upper()}")
        print("=" * 70)

        print(tuple(column_names))

        if not rows:

            print("No records found.")
            return

        for row in rows:
            print(row)

    except sqlctr.Error as err:

        print("Database error:", err)


# ============================================================
#                    VIEW ALL BOOKS
# ============================================================

def view_books():

    all_data("books")


# ============================================================
#                    SEARCH BOOK
# ============================================================

def search_book():

    search_text = input(
        "\nEnter book name or part of book name: "
    ).strip()

    if search_text == "":

        print("Search text cannot be empty.")
        return

    search_pattern = "%" + search_text + "%"

    # --------------------------------------------------------
    # Search books
    # --------------------------------------------------------

    print("\n")
    print("----------- BOOKS -----------")

    sql = """
        SELECT
            SN,
            Book_Name,
            Quantity_Available,
            Price_Per_Day
        FROM books
        WHERE Book_Name LIKE %s
    """

    rows = get_all(
        sql,
        (search_pattern,)
    )

    if rows:

        print(
            "(SN, Book_Name, Quantity_Available, Price_Per_Day)"
        )

        for row in rows:
            print(row)

    else:

        print("No matching books found.")

    # --------------------------------------------------------
    # Search issued books
    # --------------------------------------------------------

    print("\n")
    print("----------- ISSUE RECORDS -----------")

    sql = """
        SELECT
            SN,
            Member,
            book_issue,
            issue_date,
            contact_no
        FROM issue
        WHERE book_issue LIKE %s
    """

    rows = get_all(
        sql,
        (search_pattern,)
    )

    if rows:

        print(
            "(SN, Member, book_issue, issue_date, contact_no)"
        )

        for row in rows:
            print(row)

    else:

        print("No matching issue records found.")


# ============================================================
#                    ADD NEW BOOK
# ============================================================

def add_book():

    while True:

        print("\n")
        print("=========== ADD NEW BOOK ===========")

        # ----------------------------------------------------
        # Book name
        # ----------------------------------------------------

        book_name = input(
            "Enter Book Name: "
        ).strip()

        if book_name == "":

            print("Book name cannot be empty.")
            continue

        # ----------------------------------------------------
        # Quantity
        # ----------------------------------------------------

        try:

            quantity = int(
                input(
                    "Enter Quantity Available: "
                )
            )

        except ValueError:

            print("Quantity must be a whole number.")
            continue

        if quantity < 0:

            print("Quantity cannot be negative.")
            continue

        # ----------------------------------------------------
        # Price
        # ----------------------------------------------------

        try:

            price = int(
                input(
                    "Enter Price Per Day: "
                )
            )

        except ValueError:

            print("Price must be a whole number.")
            continue

        if price < 0:

            print("Price cannot be negative.")
            continue

        # ----------------------------------------------------
        # Insert
        # ----------------------------------------------------

        sql = """
            INSERT INTO books
            (
                Book_Name,
                Quantity_Available,
                Price_Per_Day
            )
            VALUES (%s, %s, %s)
        """

        if execute_query(
            sql,
            (
                book_name,
                quantity,
                price
            )
        ):

            mycon.commit()

            print(
                "\nBOOK ADDED SUCCESSFULLY."
            )

        else:

            mycon.rollback()

        again = input(
            "\nDo you want to add another book? (Y/N): "
        ).strip().upper()

        if again != "Y":

            break


# ============================================================
#                    ISSUE BOOK
# ============================================================

def issue_book():

    while True:

        print("\n")
        print("=========== AVAILABLE BOOKS ===========")

        sql = """
            SELECT
                SN,
                Book_Name,
                Quantity_Available,
                Price_Per_Day
            FROM books
            WHERE Quantity_Available > 0
            ORDER BY SN
        """

        books = get_all(sql)

        if not books:

            print("No books are currently available.")
            return

        print(
            "\nSN | Book Name | Quantity | Price/Day"
        )

        print("-" * 60)

        for book in books:

            print(
                book[0],
                "|",
                book[1],
                "|",
                book[2],
                "| Rs.",
                book[3]
            )

        # ----------------------------------------------------
        # Select book
        # ----------------------------------------------------

        try:

            book_sn = int(
                input(
                    "\nEnter SN of the book to issue: "
                )
            )

        except ValueError:

            print("SN must be a number.")
            continue

        sql = """
            SELECT
                SN,
                Book_Name,
                Quantity_Available
            FROM books
            WHERE SN = %s
        """

        book = get_one(
            sql,
            (book_sn,)
        )

        if book is None:

            print(
                "No book exists with this SN."
            )

            continue

        selected_sn = book[0]
        book_name = book[1]
        quantity = book[2]

        if quantity <= 0:

            print(
                "This book is currently unavailable."
            )

            continue

        # ----------------------------------------------------
        # Member
        # ----------------------------------------------------

        member = input(
            "Enter Member Name: "
        ).strip()

        if member == "":

            print(
                "Member name cannot be empty."
            )

            continue

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        issue_date = input(
            "Enter Issue Date (YYYY-MM-DD): "
        ).strip()

        try:

            datetime.strptime(
                issue_date,
                "%Y-%m-%d"
            )

        except ValueError:

            print(
                "Invalid date."
            )

            print(
                "Please enter date as YYYY-MM-DD."
            )

            continue

        # ----------------------------------------------------
        # Contact
        # ----------------------------------------------------

        contact = input(
            "Enter Contact Number: "
        ).strip()

        if contact == "":

            print(
                "Contact number cannot be empty."
            )

            continue

        # ----------------------------------------------------
        # INSERT ISSUE RECORD
        #
        # SN is NOT provided because MySQL generates it.
        # ----------------------------------------------------

        sql_insert = """
            INSERT INTO issue
            (
                Member,
                book_issue,
                issue_date,
                contact_no
            )
            VALUES (%s, %s, %s, %s)
        """

        try:

            cursor.execute(
                sql_insert,
                (
                    member,
                    book_name,
                    issue_date,
                    contact
                )
            )

            # ------------------------------------------------
            # Reduce quantity
            # ------------------------------------------------

            sql_update = """
                UPDATE books
                SET Quantity_Available =
                    Quantity_Available - 1
                WHERE SN = %s
                AND Quantity_Available > 0
            """

            cursor.execute(
                sql_update,
                (selected_sn,)
            )

            if cursor.rowcount != 1:

                mycon.rollback()

                print(
                    "Unable to update book quantity."
                )

                continue

            mycon.commit()

            print("\n")
            print("BOOK ISSUED SUCCESSFULLY.")
            print("Book:", book_name)
            print("Member:", member)
            print("Issue date:", issue_date)

        except sqlctr.Error as err:

            mycon.rollback()

            print(
                "\nUnable to issue book:"
            )

            print(err)

        again = input(
            "\nDo you want to issue another book? (Y/N): "
        ).strip().upper()

        if again != "Y":

            break


# ============================================================
#                    MEMBER DETAILS
# ============================================================

def member_details():

    while True:

        print("""
        
========================================
           MEMBER MENU
========================================

1. Show all issued books
2. Search member
3. Return book / calculate fare
4. Go back
5. Exit

""")

        choice = input(
            "Enter your choice: "
        ).strip()

        # ----------------------------------------------------
        # All issued books
        # ----------------------------------------------------

        if choice == "1":

            all_data("issue")

            pause()

        # ----------------------------------------------------
        # Search member
        # ----------------------------------------------------

        elif choice == "2":

            name = input(
                "\nEnter Member Name: "
            ).strip()

            contact = input(
                "Enter Contact Number: "
            ).strip()

            sql = """
                SELECT
                    SN,
                    Member,
                    book_issue,
                    issue_date,
                    contact_no
                FROM issue
                WHERE Member LIKE %s
                AND contact_no = %s
            """

            rows = get_all(
                sql,
                (name, contact)
            )

            print("\n")
            print("----------- MEMBER RECORDS -----------")

            if not rows:

                print(
                    "No records found."
                )

            else:

                for row in rows:
                    print(row)

            pause()

        # ----------------------------------------------------
        # Return book
        # ----------------------------------------------------

        elif choice == "3":

            return_book()

        # ----------------------------------------------------
        # Back
        # ----------------------------------------------------

        elif choice == "4":

            return

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        elif choice == "5":

            close_program()

        else:

            print(
                "Invalid choice."
            )


# ============================================================
#                    RETURN BOOK
# ============================================================

def return_book():

    name = input(
        "\nEnter Member Name: "
    ).strip()

    contact = input(
        "Enter Contact Number: "
    ).strip()

    if name == "" or contact == "":

        print(
            "Member name and contact number are required."
        )

        return

    # --------------------------------------------------------
    # Find all books issued to member
    # --------------------------------------------------------

    sql = """
        SELECT
            SN,
            book_issue,
            issue_date
        FROM issue
        WHERE Member = %s
        AND contact_no = %s
    """

    records = get_all(
        sql,
        (name, contact)
    )

    if not records:

        print(
            "\nNo issued books found for this member."
        )

        return

    print("\n")
    print("=========== ISSUED BOOKS ===========")

    for record in records:

        print(
            "Issue SN:",
            record[0],
            "| Book:",
            record[1],
            "| Issue Date:",
            record[2]
        )

    # --------------------------------------------------------
    # Select issue record
    # --------------------------------------------------------

    try:

        issue_sn = int(
            input(
                "\nEnter Issue SN of book to return: "
            )
        )

    except ValueError:

        print(
            "Issue SN must be a number."
        )

        return

    selected_record = None

    for record in records:

        if record[0] == issue_sn:

            selected_record = record
            break

    if selected_record is None:

        print(
            "Invalid Issue SN."
        )

        return

    book_name = selected_record[1]
    issue_date = selected_record[2]

    # --------------------------------------------------------
    # Return date
    # --------------------------------------------------------

    return_date = input(
        f'\nEnter returning date for "{book_name}" '
        "(YYYY-MM-DD): "
    ).strip()

    try:

        return_date_obj = datetime.strptime(
            return_date,
            "%Y-%m-%d"
        )

    except ValueError:

        print(
            "Invalid return date."
        )

        return

    # --------------------------------------------------------
    # Convert issue date
    # --------------------------------------------------------

    if isinstance(issue_date, datetime):

        issue_date_obj = issue_date

    else:

        issue_date_obj = datetime.combine(
            issue_date,
            datetime.min.time()
        )

    # --------------------------------------------------------
    # Check return date
    # --------------------------------------------------------

    if return_date_obj < issue_date_obj:

        print(
            "Return date cannot be before issue date."
        )

        return

    # --------------------------------------------------------
    # Calculate days
    # --------------------------------------------------------

    days = (
        return_date_obj.date()
        - issue_date_obj.date()
    ).days

    # Minimum one day
    if days == 0:

        days = 1

    # --------------------------------------------------------
    # Get price
    # --------------------------------------------------------

    sql = """
        SELECT
            Price_Per_Day
        FROM books
        WHERE Book_Name = %s
    """

    book_data = get_one(
        sql,
        (book_name,)
    )

    if book_data is None:

        print(
            "Book no longer exists in the books table."
        )

        return

    price_per_day = book_data[0]

    total_price = days * price_per_day

    print("\n")
    print("========================================")
    print("              RETURN DETAILS")
    print("========================================")
    print("Book:", book_name)
    print("Issue date:", issue_date)
    print("Return date:", return_date)
    print("Number of days:", days)
    print("Price per day: Rs.", price_per_day)
    print("Total fare: Rs.", total_price)
    print("========================================")

    paid = input(
        "\nHas the fare been paid and book returned? (Y/N): "
    ).strip().upper()

    if paid != "Y":

        print(
            "\nPlease pay the fare and return the book."
        )

        return

    # --------------------------------------------------------
    # Return book
    # --------------------------------------------------------

    try:

        # Increase quantity
        sql_update = """
            UPDATE books
            SET Quantity_Available =
                Quantity_Available + 1
            WHERE Book_Name = %s
        """

        cursor.execute(
            sql_update,
            (book_name,)
        )

        if cursor.rowcount == 0:

            mycon.rollback()

            print(
                "Unable to update book quantity."
            )

            return

        # Delete issue record
        sql_delete = """
            DELETE FROM issue
            WHERE SN = %s
        """

        cursor.execute(
            sql_delete,
            (issue_sn,)
        )

        if cursor.rowcount != 1:

            mycon.rollback()

            print(
                "Unable to remove issue record."
            )

            return

        mycon.commit()

        print("\n")
        print("BOOK RETURNED SUCCESSFULLY.")
        print(
            "Total fare paid: Rs.",
            total_price
        )

    except sqlctr.Error as err:

        mycon.rollback()

        print(
            "Error while returning book:",
            err
        )


# ============================================================
#                    UPDATE BOOK
# ============================================================

def update_book():

    while True:

        print("\n")
        print("=========== UPDATE BOOK ===========")

        all_data("books")

        print("""
        
What do you want to update?

1. Book Name
2. Quantity Available
3. Price Per Day
4. Go Back

""")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "4":

            return

        if choice == "1":

            column = "Book_Name"

        elif choice == "2":

            column = "Quantity_Available"

        elif choice == "3":

            column = "Price_Per_Day"

        else:

            print(
                "Invalid choice."
            )

            continue

        # ----------------------------------------------------
        # SN
        # ----------------------------------------------------

        try:

            sn = int(
                input(
                    "\nEnter SN of book: "
                )
            )

        except ValueError:

            print(
                "SN must be a number."
            )

            continue

        # ----------------------------------------------------
        # New value
        # ----------------------------------------------------

        new_value = input(
            f"Enter new value for {column}: "
        ).strip()

        if new_value == "":

            print(
                "New value cannot be empty."
            )

            continue

        # ----------------------------------------------------
        # Validate numeric fields
        # ----------------------------------------------------

        if column in [
            "Quantity_Available",
            "Price_Per_Day"
        ]:

            try:

                new_value = int(
                    new_value
                )

            except ValueError:

                print(
                    "Value must be a number."
                )

                continue

            if new_value < 0:

                print(
                    "Value cannot be negative."
                )

                continue

        # ----------------------------------------------------
        # Update
        # ----------------------------------------------------

        sql = f"""
            UPDATE books
            SET {column} = %s
            WHERE SN = %s
        """

        if execute_query(
            sql,
            (
                new_value,
                sn
            )
        ):

            if cursor.rowcount == 0:

                print(
                    "No book found with this SN."
                )

            else:

                mycon.commit()

                print(
                    "\nBOOK UPDATED SUCCESSFULLY."
                )

        else:

            mycon.rollback()

        again = input(
            "\nDo you want to update another book? (Y/N): "
        ).strip().upper()

        if again != "Y":

            break


# ============================================================
#                    CLOSE PROGRAM
# ============================================================

def close_program():

    try:

        mycon.commit()

        if cursor:
            cursor.close()

        if mycon.is_connected():
            mycon.close()

        print(
            "\nConnection closed successfully."
        )

        print(
            "Thank you for using Library Management System."
        )

        sys.exit()

    except sqlctr.Error as err:

        print(
            "Error while closing database:",
            err
        )

        sys.exit()


# ============================================================
#                    MAIN MENU
# ============================================================

def main_menu():

    while True:

        print("""
        
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
""")

        choice = input(
            "Enter your choice: "
        ).strip()

        # ----------------------------------------------------
        # View books
        # ----------------------------------------------------

        if choice == "1":

            view_books()
            pause()

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        elif choice == "2":

            search_book()
            pause()

        # ----------------------------------------------------
        # Issue
        # ----------------------------------------------------

        elif choice == "3":

            issue_book()

        # ----------------------------------------------------
        # Add
        # ----------------------------------------------------

        elif choice == "4":

            add_book()

        # ----------------------------------------------------
        # Update
        # ----------------------------------------------------

        elif choice == "5":

            update_book()

        # ----------------------------------------------------
        # Member
        # ----------------------------------------------------

        elif choice == "6":

            member_details()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        elif choice == "7":

            close_program()

        else:

            print(
                "\nInvalid choice."
            )

            print(
                "Please enter a number from 1 to 7."
            )


# ============================================================
#                    START PROGRAM
# ============================================================

try:

    main_menu()

except KeyboardInterrupt:

    print(
        "\n\nProgram stopped by user."
    )

    try:

        mycon.rollback()

        if cursor:
            cursor.close()

        if mycon.is_connected():
            mycon.close()

    except:
        pass

except Exception as err:

    print(
        "\nUnexpected error:",
        err
    )

    try:

        mycon.rollback()

        if cursor:
            cursor.close()

        if mycon.is_connected():
            mycon.close()

    except:
        pass

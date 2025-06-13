import mysql.connector
from typing import List, Optional
from datetime import date
import os
import configparser

from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail

class ApplicantDatabase:
    def __init__(self, config_path: str = 'data/config.ini'):
        self.config_path = config_path
        self.db_config = self._load_db_config()
        self.conn = None
        self._init_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _load_db_config(self) -> dict:
        config = configparser.ConfigParser()
        if not os.path.exists(self.config_path):
            raise DatabaseError(f"Configuration file '{self.config_path}' not found.")
        config.read(self.config_path)
        if 'database' not in config:
            raise DatabaseError(f"Missing '[database]' section in '{self.config_path}'.")
        db_section = config['database']
        db_type = db_section.get('type')
        if db_type and db_type.lower() != 'mysql':
            raise DatabaseError(f"Unsupported database type '{db_type}' specified.")
        mysql_config = {
            'host': db_section.get('host'),
            'user': db_section.get('user'),
            'password': db_section.get('password'),
            'database': db_section.get('database')
        }
        if not all(mysql_config.values()):
            missing_keys = [k for k, v in mysql_config.items() if v is None]
            raise DatabaseError(f"Incomplete MySQL database configuration. Missing keys: {', '.join(missing_keys)}.")
        mysql_config['type'] = 'mysql'
        return mysql_config

    def _init_db(self) -> None:
        try:
            self.conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )
            cur = self.conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS ApplicantProfile (
                applicant_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                date_of_birth DATE,
                address TEXT,
                phone_number VARCHAR(20)
            )
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS ApplicationDetail (
                detail_id INT AUTO_INCREMENT PRIMARY KEY,
                applicant_id INT NOT NULL,
                application_role VARCHAR(255),
                cv_path TEXT,
                FOREIGN KEY(applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
            )
            ''')
            self.conn.commit()
        except mysql.connector.Error as e:
            error_message = f"MySQL Database initialization failed: {e}. "
            if "Unknown database" in str(e):
                error_message += f"The database '{self.db_config['database']}' might not exist."
            elif "Access denied" in str(e):
                error_message += "Access denied."
            elif "Can't connect to MySQL server" in str(e):
                error_message += f"Could not connect to MySQL server at {self.db_config['host']}."
            raise DatabaseError(error_message)
        except Exception as e:
            raise DatabaseError(f"An unexpected error occurred during database initialization: {e}")

    def close(self) -> None:
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None

    def clear_db(self) -> None:
        try:
            cur = self.conn.cursor()
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("TRUNCATE TABLE ApplicationDetail")
            cur.execute("TRUNCATE TABLE ApplicantProfile")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.conn.commit()
            print("Database cleared successfully.")
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error clearing database: {e}")

    def add_applicant(self, applicant: ApplicantProfile) -> ApplicantProfile:
        try:
            cur = self.conn.cursor()
            cur.execute('''
            INSERT INTO ApplicantProfile 
            (first_name, last_name, date_of_birth, address, phone_number)
            VALUES (%s, %s, %s, %s, %s)
            ''', (applicant.first_name, applicant.last_name, 
                  applicant.date_of_birth.isoformat() if applicant.date_of_birth else None,
                  applicant.address, applicant.phone_number))
            self.conn.commit()
            applicant.applicant_id = cur.lastrowid
            return applicant
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error adding applicant: {e}")

    def add_application_detail(self, detail: ApplicationDetail) -> ApplicationDetail:
        try:
            cur = self.conn.cursor()
            cur.execute('''
            INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
            VALUES (%s, %s, %s)
            ''', (detail.applicant_id, detail.application_role, detail.cv_path))
            self.conn.commit()
            detail.detail_id = cur.lastrowid
            return detail
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error adding application detail: {e}")

    def get_applicant(self, applicant_id: int) -> Optional[ApplicantProfile]:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM ApplicantProfile WHERE applicant_id = %s', (applicant_id,))
            row = cur.fetchone()
            if row:
                return self._row_to_applicant(row)
            return None
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error getting applicant: {e}")

    def get_applicant_with_details(self, applicant_id: int) -> Optional[tuple[ApplicantProfile, List[ApplicationDetail]]]:
        applicant = self.get_applicant(applicant_id)
        if not applicant:
            return None
        details = self.get_applicant_details(applicant_id)
        return (applicant, details)

    def get_applicant_details(self, applicant_id: int) -> List[ApplicationDetail]:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM ApplicationDetail WHERE applicant_id = %s', (applicant_id,))
            rows = cur.fetchall()
            return [self._row_to_application_detail(row) for row in rows]
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error getting applicant details: {e}")

    def search_applicants(self, search_term: str) -> List[ApplicantProfile]:
        try:
            cur = self.conn.cursor()
            search_pattern = f"%{search_term}%"
            cur.execute('''
            SELECT * FROM ApplicantProfile 
            WHERE first_name LIKE %s OR last_name LIKE %s
            ''', (search_pattern, search_pattern))
            return [self._row_to_applicant(row) for row in cur.fetchall()]
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error searching applicants: {e}")

    def update_applicant(self, applicant: ApplicantProfile) -> bool:
        try:
            cur = self.conn.cursor()
            cur.execute('''
            UPDATE ApplicantProfile 
            SET first_name = %s, last_name = %s, date_of_birth = %s, 
                address = %s, phone_number = %s
            WHERE applicant_id = %s
            ''', (applicant.first_name, applicant.last_name,
                  applicant.date_of_birth.isoformat() if applicant.date_of_birth else None,
                  applicant.address, applicant.phone_number,
                  applicant.applicant_id))
            self.conn.commit()
            return cur.rowcount > 0
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error updating applicant: {e}")

    def delete_applicant(self, applicant_id: int) -> bool:
        try:
            cur = self.conn.cursor()
            cur.execute('DELETE FROM ApplicationDetail WHERE applicant_id = %s', (applicant_id,))
            cur.execute('DELETE FROM ApplicantProfile WHERE applicant_id = %s', (applicant_id,))
            self.conn.commit()
            return cur.rowcount > 0
        except mysql.connector.Error as e:
            raise DatabaseError(f"Error deleting applicant: {e}")

    def _row_to_applicant(self, row: tuple) -> ApplicantProfile:
        dob = None
        if row[3]:
            try:
                if isinstance(row[3], date):
                    dob = row[3]
                else:
                    dob = date.fromisoformat(str(row[3])) 
            except (TypeError, ValueError):
                dob = None 
        return ApplicantProfile(
            applicant_id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=dob,
            address=row[4],
            phone_number=row[5]
        )

    def _row_to_application_detail(self, row: tuple) -> ApplicationDetail:
        return ApplicationDetail(
            detail_id=row[0],
            applicant_id=row[1],
            application_role=row[2],
            cv_path=row[3]
        )

class DatabaseError(Exception):
    pass

def test_applicant_database():
    from src.model.applicant_profile import ApplicantProfile
    from src.model.application_detail import ApplicationDetail
    from datetime import date

    try:
        with ApplicantDatabase() as db:
            print("== Starting ApplicantDatabase tests ==")

            # Clear database
            db.clear_db()

            # Add applicant
            applicant = ApplicantProfile(
                applicant_id=None,
                first_name="John",
                last_name="Doe",
                date_of_birth=date(1990, 1, 1),
                address="123 Main St",
                phone_number="1234567890"
            )
            applicant = db.add_applicant(applicant)
            print(f"Added applicant: {applicant}")

            # Get applicant
            fetched = db.get_applicant(applicant.applicant_id)
            print(f"Fetched applicant: {fetched}")

            # Update applicant
            applicant.first_name = "Jane"
            success = db.update_applicant(applicant)
            print(f"Updated applicant: {success}")

            # Search applicant
            results = db.search_applicants("Jane")
            print(f"Search results: {results}")

            # Add application detail
            detail = ApplicationDetail(
                detail_id=None,
                applicant_id=applicant.applicant_id,
                application_role="Engineer",
                cv_path="/path/to/cv.pdf"
            )
            detail = db.add_application_detail(detail)
            print(f"Added application detail: {detail}")

            # Get applicant details
            details = db.get_applicant_details(applicant.applicant_id)
            print(f"Application details: {details}")

            # Get applicant with details
            applicant_bundle = db.get_applicant_with_details(applicant.applicant_id)
            print(f"Applicant with details: {applicant_bundle}")

            # Delete applicant
            deleted = db.delete_applicant(applicant.applicant_id)
            print(f"Deleted applicant: {deleted}")

            # Final check
            empty_check = db.get_applicant(applicant.applicant_id)
            print(f"Check after deletion: {empty_check}")

            print("== Tests completed ==")

    except DatabaseError as e:
        print(f"DatabaseError during tests: {e}")
    except Exception as e:
        print(f"Unexpected error during tests: {e}")


if __name__ == "__main__":
    # test_applicant_database()
    try:
        with ApplicantDatabase() as db: 
            print("Welcome to the Applicant Database SQL shell (MySQL).")
            print("Enter SQL commands. Type 'exit' to quit.")
            while True:
                try:
                    command = input("SQL> ").strip()
                    if command.lower() == 'exit':
                        break
                    if not command:
                        continue
                    cursor = db.conn.cursor()
                    cursor.execute(command)
                    if command.lower().startswith(('insert', 'update', 'delete')):
                        db.conn.commit()
                        print(f"{cursor.rowcount} row(s) affected.")
                    else:
                        rows = cursor.fetchall()
                        if rows:
                            headers = [description[0] for description in cursor.description]
                            print("\t".join(headers))
                            print("-" * (len("\t".join(headers)) + 5))
                            for row in rows:
                                print("\t".join(map(str, row)))
                        else:
                            print("No results.")
                except mysql.connector.Error as e:
                    print(f"SQL Error: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
    except DatabaseError as e:
        print(f"CRITICAL DATABASE ERROR: {e}")
    except mysql.connector.Error as e:
        print(f"MySQL connection error: {e}.")

import sqlite3
from typing import List, Optional
from datetime import date
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
import os

class ApplicantDatabase:
    def __init__(self, db_name: str = 'applicant.db'):
        self.db_name = db_name
        self.conn = None
        self._init_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _init_db(self) -> None:
        try:
            db_dir = os.path.dirname(self.db_name)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)

            self.conn = sqlite3.connect(self.db_name)
            cur = self.conn.cursor()
            
            cur.execute('''
            CREATE TABLE IF NOT EXISTS ApplicantProfile (
                applicant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                date_of_birth TEXT,
                address TEXT,
                phone_number TEXT
            )
            ''')
            
            cur.execute('''
            CREATE TABLE IF NOT EXISTS ApplicationDetail (
                detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                applicant_id INTEGER NOT NULL,
                application_role TEXT,
                cv_path TEXT,
                FOREIGN KEY(applicant_id) REFERENCES ApplicantProfile(applicant_id)
            )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Database initialization failed: {e}")

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def add_applicant(self, applicant: ApplicantProfile) -> ApplicantProfile:
        try:
            cur = self.conn.cursor()
            cur.execute('''
            INSERT INTO ApplicantProfile 
            (first_name, last_name, date_of_birth, address, phone_number)
            VALUES (?, ?, ?, ?, ?)
            ''', (applicant.first_name, applicant.last_name, 
            applicant.date_of_birth.isoformat() if applicant.date_of_birth else None,
            applicant.address, applicant.phone_number))
            
            self.conn.commit()
            applicant.applicant_id = cur.lastrowid
            return applicant
        except sqlite3.Error as e:
            raise DatabaseError(f"Error adding applicant: {e}")

    def add_application_detail(self, detail: ApplicationDetail) -> ApplicationDetail:
        try:
            cur = self.conn.cursor()
            cur.execute('''
            INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
            VALUES (?, ?, ?)
            ''', (detail.applicant_id, detail.application_role, detail.cv_path))
            
            self.conn.commit()
            detail.detail_id = cur.lastrowid
            return detail
        except sqlite3.Error as e:
            raise DatabaseError(f"Error adding application detail: {e}")

    def get_applicant(self, applicant_id: int) -> Optional[ApplicantProfile]:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT * FROM ApplicantProfile WHERE applicant_id = ?', (applicant_id,))
            row = cur.fetchone()
            
            if row:
                return self._row_to_applicant(row)
            return None
        except sqlite3.Error as e:
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
            cur.execute('SELECT * FROM ApplicationDetail WHERE applicant_id = ?', (applicant_id,))
            rows = cur.fetchall()
            
            return [self._row_to_application_detail(row) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error getting applicant details: {e}")

    def search_applicants(self, search_term: str) -> List[ApplicantProfile]:
        try:
            cur = self.conn.cursor()
            search_pattern = f"%{search_term}%"
            cur.execute('''
            SELECT * FROM ApplicantProfile 
            WHERE first_name LIKE ? OR last_name LIKE ?
            ''', (search_pattern, search_pattern))
            
            return [self._row_to_applicant(row) for row in cur.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error searching applicants: {e}")

    def update_applicant(self, applicant: ApplicantProfile) -> bool:
        try:
            cur = self.conn.cursor()
            cur.execute('''
            UPDATE ApplicantProfile 
            SET first_name = ?, last_name = ?, date_of_birth = ?, 
                address = ?, phone_number = ?
            WHERE applicant_id = ?
            ''', (applicant.first_name, applicant.last_name,
            applicant.date_of_birth.isoformat() if applicant.date_of_birth else None,
            applicant.address, applicant.phone_number,
            applicant.applicant_id))
            
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error updating applicant: {e}")

    def delete_applicant(self, applicant_id: int) -> bool:
        try:
            cur = self.conn.cursor()
            
            cur.execute('DELETE FROM ApplicationDetail WHERE applicant_id = ?', (applicant_id,))
            cur.execute('DELETE FROM ApplicantProfile WHERE applicant_id = ?', (applicant_id,))
            
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error deleting applicant: {e}")

    def _row_to_applicant(self, row: tuple) -> ApplicantProfile:
        return ApplicantProfile(
            applicant_id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=date.fromisoformat(row[3]) if row[3] else None,
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

if __name__ == "__main__":
    db_path = 'data/applicants.db' 
    with ApplicantDatabase(db_path) as db:
        print("Welcome to the Applicant Database SQL shell.")
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
            except sqlite3.Error as e:
                print(f"SQL Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
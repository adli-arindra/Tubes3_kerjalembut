import pandas as pd
from datetime import datetime
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.model.sql import ApplicantDatabase
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def seed_database_from_csv(csv_path: str, db_path: str = 'data/applicants.db', rows_per_role: int = 20):
    """
    Seed the database from a CSV file. For each unique application_role, only the first N rows are inserted.
    This will reset the database (delete all data) before seeding.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if 'application_role' not in df.columns:
        raise ValueError("CSV must contain 'application_role' column.")

    # Open DB and reset tables
    with ApplicantDatabase(db_path) as db:
        # Delete all data
        cur = db.conn.cursor()
        cur.execute('DELETE FROM ApplicationDetail')
        cur.execute('DELETE FROM ApplicantProfile')
        db.conn.commit()

        # Group by role and take N rows per role
        for role, group in df.groupby('application_role'):
            group = group.head(rows_per_role)
            for _, row in group.iterrows():
                # Create ApplicantProfile
                dob = None
                if 'date_of_birth' in row and pd.notnull(row['date_of_birth']):
                    try:
                        dob = datetime.strptime(str(row['date_of_birth']), '%Y-%m-%d').date()
                    except Exception:
                        dob = None
                applicant = ApplicantProfile(
                    first_name=row.get('first_name', None),
                    last_name=row.get('last_name', None),
                    date_of_birth=dob,
                    address=row.get('address', None),
                    phone_number=row.get('phone_number', None)
                )
                applicant = db.add_applicant(applicant)

                # Create ApplicationDetail
                detail = ApplicationDetail(
                    applicant_id=applicant.applicant_id,
                    application_role=row.get('application_role', None),
                    cv_path=row.get('cv_path', None)
                )
                db.add_application_detail(detail)

    print(f"Database seeded from {csv_path} with {rows_per_role} rows per role.")


if __name__ == "__main__":
    seed_database_from_csv("data/Resume.csv")
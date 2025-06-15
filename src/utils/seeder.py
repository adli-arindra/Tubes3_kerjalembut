import pandas as pd
from datetime import datetime
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.model.application_pdf import ApplicationPDF
from src.utils.sql import ApplicantDatabase
from src.utils.pdf_reader import PDFReader
import random
from datetime import date, timedelta
from typing import Optional
import os
import sys

def find_path(id: str) -> str:
    root_dir = "data\\pdf"
    for category in os.listdir(root_dir):
        for file in os.listdir(os.path.join(root_dir, category)):
            if file.startswith(id):
                return os.path.join(root_dir, category, file)

def generate_random_applicant_profile(applicant_id: int) -> Optional[ApplicantProfile]:
    first_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi",
        "Ivy", "Jack", "Karen", "Liam", "Mia", "Noah", "Olivia", "Peter",
        "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier",
        "Yara", "Zoe", "David", "Emily", "George", "Hannah", "Isaac", "Julia"
    ]
    last_names = [
        "Smith", "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore",
        "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson",
        "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker",
        "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill"
    ]
    street_types = ["St", "Ave", "Rd", "Ln", "Blvd", "Ct", "Dr", "Pl", "Ter"]
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Bandung", "Surabaya",
        "Jakarta", "Medan", "Semarang", "Yogyakarta", "San Francisco", "Seattle", "Boston",
        "Miami", "Dallas", "Denver", "Atlanta", "Portland", "Nashville", "Orlando", "Austin"
    ]
    states = [
        "CA", "NY", "TX", "FL", "IL", "WV", "JB", "MA", "WA", "GA", "OR", "CO",
        "AZ", "TN", "PA", "OH", "MI", "NC", "VA", "MD", "NJ", "GA", "IN"
    ]
    
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)
    
    today = date.today()
    min_age_years = 18
    max_age_years = 70
    
    max_birth_date = today - timedelta(days=min_age_years * 365.25)
    min_birth_date = today - timedelta(days=max_age_years * 365.25)
    
    time_delta_days = (max_birth_date - min_birth_date).days
    random_days = random.randint(0, time_delta_days)
    random_date_of_birth = min_birth_date + timedelta(days=random_days)
    
    random_address_number = random.randint(1, 9999)
    random_street_name = random.choice(last_names) + random.choice(street_types)
    random_city = random.choice(cities)
    random_state = random.choice(states)
    random_zip_code = f"{random.randint(10000, 99999):05d}"
    random_address = f"{random_address_number} {random_street_name}, {random_city}, {random_state} {random_zip_code}"
    
    phone_formats = [
        "({area_code}) {prefix}-{line}",
        "{area_code}-{prefix}-{line}",
        "{area_code} {prefix} {line}"
    ]
    random_phone_number_format = random.choice(phone_formats)
    random_area_code = random.randint(100, 999)
    random_prefix = random.randint(100, 999)
    random_line = random.randint(1000, 9999)
    random_phone_number = random_phone_number_format.format(
        area_code=random_area_code,
        prefix=random_prefix,
        line=random_line
    )

    new_applicant = ApplicantProfile(
        applicant_id=applicant_id,
        first_name=random_first_name,
        last_name=random_last_name,
        date_of_birth=random_date_of_birth,
        address=random_address,
        phone_number=random_phone_number
    )
    
    return new_applicant

def seed_database_from_csv(db: ApplicantDatabase):
    df = pd.read_csv("data/Resume.csv")
    id = 0

    categories = df['Category'].unique()
    for category in categories:
        category_head = df.loc[df['Category'] == category].head(20)
        
        for index, row in category_head.iterrows():
            cv_path = find_path(str(row.ID))
            new_applicant = generate_random_applicant_profile(id)
            new_application = ApplicationDetail(
                detail_id = row.ID,
                applicant_id = id,
                application_role = category,
                cv_path = cv_path)
            new_pdf = ApplicationPDF(
                detail_id = row.ID,
                cv_text = PDFReader.read_text(cv_path),
                cv_raw = PDFReader.read_raw(cv_path)
            )
            db.add_applicant(new_applicant)
            db.add_application_detail(new_application)
            db.add_application_pdf(new_pdf)
            id += 1
            print(f"added row {id}")

def get_all_cv() -> list[ApplicationPDF]:
    df = pd.read_csv("data/Resume.csv")

    categories = df['Category'].unique()
    ret = []
    for category in categories:
        category_head = df.loc[df['Category'] == category].head(20)
        
        for index, row in category_head.iterrows():
            cv_path = find_path(str(row.ID))
            new_pdf = ApplicationPDF(
                detail_id = row.ID,
                cv_text = PDFReader.read_text(cv_path),
                cv_raw = PDFReader.read_raw(cv_path)
            )
            ret.append(new_pdf)
    
    return ret

def seed_from_sql(db: ApplicantDatabase, sql_file_path: str):
    if not os.path.exists(sql_file_path):
        print(f"SQL file not found: {sql_file_path}")
        return

    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        conn.commit()
        print("Database seeded from SQL file.")
    except Exception as e:
        print(f"Error seeding from SQL: {e}")
        conn.rollback()

def seed_pdf_from_sql_data(db: ApplicantDatabase, sql_file_path: str):
    if not os.path.exists(sql_file_path):
        print(f"SQL file not found: {sql_file_path}")
        return

    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        conn.commit()
        print("Seeded ApplicantProfile and ApplicationDetail tables.")
    except Exception as e:
        print(f"Error executing SQL: {e}")
        conn.rollback()
        return

    try:
        cursor.execute("SELECT detail_id, cv_path FROM ApplicationDetail")
        rows = cursor.fetchall()
        for detail_id, cv_path in rows:
            if not os.path.exists(cv_path):
                print(f"CV not found for detail_id {detail_id}: {cv_path}")
                continue
            pdf = ApplicationPDF(
                detail_id=detail_id,
                cv_text=PDFReader.read_text(cv_path),
                cv_raw=PDFReader.read_raw(cv_path)
            )
            db.add_application_pdf(pdf)
        print("Generated ApplicationPDF entries from ApplicationDetail.")
    except Exception as e:
        print(f"Error generating ApplicationPDF: {e}")


if __name__ == "__main__":
    db = ApplicantDatabase()
    db.clear_db()
    # db.reset_tables()
    seed_database_from_csv(db)
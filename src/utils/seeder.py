import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from datetime import datetime, timedelta
from random import randint, choice
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.utils.sql import ApplicantDatabase


def generate_random_date(start_year=1970, end_year=2000):
    """Generate random date of birth between start and end year."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=randint(0, (end - start).days))

def generate_random_address():
    streets = ["Jl. Sudirman", "Jl. Thamrin", "Jl. Asia Afrika", "Jl. Merdeka", "Jl. Diponegoro"]
    numbers = [str(randint(1, 200)) for _ in range(5)]
    return f"{choice(streets)} No. {choice(numbers)}"

def generate_random_phone():
    return f"08{randint(1000000000, 9999999999)}"

def find_pdf_path(category, filename, pdf_base_dir='data/pdf'):

    # Cek beberapa kemungkinan ekstensi
    possible_exts = ['.pdf', '.PDF']
    for ext in possible_exts:
        pdf_path = os.path.join(pdf_base_dir, str(category), str(filename) + ext)
        if os.path.exists(pdf_path):
            return pdf_path
        # Jika filename sudah ada ekstensi
        pdf_path2 = os.path.join(pdf_base_dir, str(category), str(filename))
        if os.path.exists(pdf_path2):
            return pdf_path2
    return None

def seed_database_from_csv(csv_path: str, rows_per_category: int = 20, pdf_base_dir: str = 'data/pdf'):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    # Cari kolom 'ID' dan 'Category' (case-insensitive)
    id_col = None
    category_col = None
    for col in df.columns:
        if col.strip().lower() == 'id':
            id_col = col
        if col.strip().lower() == 'category':
            category_col = col
    if not id_col or not category_col:
        raise ValueError("CSV must contain 'ID' and 'Category' columns.")

    with ApplicantDatabase() as db:
        db.clear_db()
        total_inserted = 0
        for _, row in df.iterrows():
            category = str(row[category_col])
            file_id = str(row[id_col])
            # Data profil pelamar dari CSV jika ada
            first_name = f"Anon{randint(1000,9999)}"
            last_name = f"User{randint(1000,9999)}"
            address = generate_random_address()
            phone_number = generate_random_phone()
            date_of_birth = generate_random_date().date()
            applicant = ApplicantProfile(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                address=address,
                phone_number=phone_number
            )
            applicant = db.add_applicant(applicant)

            # Data application_detail dari CSV jika ada
            application_role = category
            cv_path = find_pdf_path(category, file_id, pdf_base_dir)
            if not cv_path or not os.path.exists(str(cv_path)):
                print(f"  CV file not found for ID={file_id} in category={category}. Skipped.")
                continue

            detail = ApplicationDetail(
                applicant_id=applicant.applicant_id,
                application_role=application_role,
                cv_path=cv_path
            )
            db.add_application_detail(detail)
            total_inserted += 1
    print(f"Database seeding complete. {total_inserted} applications inserted.")

if __name__ == "__main__":
    seed_database_from_csv("data/Resume.csv")
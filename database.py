"""
Database management module for CampusHire - College Placement & Recruitment Management System.
Supports SQLite (zero-config, instant local execution) with exact schema, tables,
views, triggers, and stored procedures/functions from college_placement_all_in_one.sql.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'college_placement.db')


def get_db_connection():
    """Returns a SQLite connection with row_factory enabled and foreign keys enforced."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # Register custom SQL functions to mirror MySQL functions
    conn.create_function("fn_calculate_overall_placement_percentage", 0, lambda: _calculate_overall_placement_percentage(conn))
    conn.create_function("fn_calculate_department_placement_percentage", 1, lambda dept_id: _calculate_department_placement_percentage(conn, dept_id))
    return conn


def _calculate_overall_placement_percentage(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM students s
        INNER JOIN users u ON s.user_id = u.user_id
        WHERE u.account_status = 'ACTIVE'
    """)
    total = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT COUNT(DISTINCT s.student_id)
        FROM students s
        INNER JOIN applications a ON s.student_id = a.student_id
        INNER JOIN placement_offers o ON a.application_id = o.application_id
        WHERE o.offer_status = 'ACCEPTED'
    """)
    placed = cur.fetchone()[0] or 0

    if total > 0:
        return round((placed * 100.0) / total, 2)
    return 0.00


def _calculate_department_placement_percentage(conn, dept_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM students s
        INNER JOIN users u ON s.user_id = u.user_id
        WHERE s.department_id = ? AND u.account_status = 'ACTIVE'
    """, (dept_id,))
    total = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT COUNT(DISTINCT s.student_id)
        FROM students s
        INNER JOIN applications a ON s.student_id = a.student_id
        INNER JOIN placement_offers o ON a.application_id = o.application_id
        WHERE s.department_id = ? AND o.offer_status = 'ACCEPTED'
    """, (dept_id,))
    placed = cur.fetchone()[0] or 0

    if total > 0:
        return round((placed * 100.0) / total, 2)
    return 0.00


def init_db(reset=False):
    """Initializes tables, views, triggers, and sample data from college_placement_all_in_one.sql."""
    if reset and os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    # Table 1: users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('ADMIN', 'STUDENT', 'RECRUITER')),
        account_status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(account_status IN ('ACTIVE', 'INACTIVE')),
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime'))
    );
    """)

    # Table 2: departments
    cur.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE,
        department_code TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at DATETIME DEFAULT (datetime('now', 'localtime'))
    );
    """)

    # Table 3: students
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        enrollment_number TEXT NOT NULL UNIQUE,
        department_id INTEGER NOT NULL,
        graduation_year INTEGER NOT NULL,
        cgpa REAL NOT NULL CHECK(cgpa >= 0.00 AND cgpa <= 10.00),
        active_backlogs INTEGER NOT NULL DEFAULT 0 CHECK(active_backlogs >= 0),
        phone TEXT,
        resume_url TEXT,
        profile_status TEXT NOT NULL DEFAULT 'VERIFIED' CHECK(profile_status IN ('PENDING_VERIFICATION', 'VERIFIED', 'SUSPENDED')),
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """)

    # Table 4: companies
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL UNIQUE,
        industry TEXT NOT NULL,
        website TEXT,
        company_description TEXT,
        headquarters TEXT,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime'))
    );
    """)

    # Table 5: recruiters
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recruiters (
        recruiter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        company_id INTEGER NOT NULL,
        designation TEXT NOT NULL,
        phone TEXT,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """)

    # Table 6: job_openings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job_openings (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        job_title TEXT NOT NULL,
        job_description TEXT NOT NULL,
        job_type TEXT NOT NULL DEFAULT 'FULL_TIME' CHECK(job_type IN ('FULL_TIME', 'INTERNSHIP', 'INTERN_TO_FTE')),
        location TEXT NOT NULL,
        minimum_cgpa REAL NOT NULL DEFAULT 0.00 CHECK(minimum_cgpa >= 0.00 AND minimum_cgpa <= 10.00),
        maximum_backlogs INTEGER NOT NULL DEFAULT 0 CHECK(maximum_backlogs >= 0),
        package_lpa REAL NOT NULL CHECK(package_lpa >= 0.00),
        application_deadline DATETIME NOT NULL,
        drive_date DATETIME,
        job_status TEXT NOT NULL DEFAULT 'DRAFT' CHECK(job_status IN ('DRAFT', 'OPEN', 'CLOSED', 'CANCELLED')),
        created_by INTEGER NOT NULL,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """)

    # Table 7: job_eligibility_departments
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job_eligibility_departments (
        job_id INTEGER NOT NULL,
        department_id INTEGER NOT NULL,
        PRIMARY KEY (job_id, department_id),
        FOREIGN KEY (job_id) REFERENCES job_openings(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """)

    # Table 8: applications
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        application_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        application_date DATETIME DEFAULT (datetime('now', 'localtime')),
        application_status TEXT NOT NULL DEFAULT 'APPLIED' CHECK(application_status IN ('APPLIED', 'SHORTLISTED', 'REJECTED', 'SELECTED', 'WITHDRAWN')),
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime')),
        UNIQUE (student_id, job_id),
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (job_id) REFERENCES job_openings(job_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """)

    # Table 9: interview_rounds
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interview_rounds (
        round_id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER NOT NULL,
        round_number INTEGER NOT NULL,
        round_name TEXT NOT NULL,
        scheduled_at DATETIME,
        score REAL CHECK(score IS NULL OR (score >= 0.00 AND score <= 100.00)),
        feedback TEXT,
        round_status TEXT NOT NULL DEFAULT 'PENDING' CHECK(round_status IN ('PENDING', 'PASSED', 'FAILED', 'NOT_ATTENDED')),
        evaluated_by INTEGER,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime')),
        UNIQUE (application_id, round_number),
        FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (evaluated_by) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
    );
    """)

    # Table 10: placement_offers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS placement_offers (
        offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER NOT NULL UNIQUE,
        offered_package_lpa REAL NOT NULL CHECK(offered_package_lpa >= 0.00),
        offer_date DATE NOT NULL,
        joining_date DATE,
        offer_status TEXT NOT NULL DEFAULT 'OFFERED' CHECK(offer_status IN ('OFFERED', 'ACCEPTED', 'DECLINED', 'WITHDRAWN')),
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        updated_at DATETIME DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    """)

    # Table 11: audit_logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id INTEGER,
        details TEXT,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
    );
    """)

    # =========================================================================
    # VIEWS
    # =========================================================================
    cur.execute("DROP VIEW IF EXISTS v_student_placement_summary;")
    cur.execute("""
    CREATE VIEW v_student_placement_summary AS
    SELECT 
        s.student_id,
        s.enrollment_number,
        u.full_name AS student_name,
        u.email,
        d.department_code,
        s.cgpa,
        s.active_backlogs,
        COUNT(DISTINCT a.application_id) AS total_applications,
        COUNT(DISTINCT r.round_id) AS total_interviews_scheduled,
        COALESCE(MAX(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 0.00) AS accepted_package_lpa,
        CASE 
            WHEN SUM(CASE WHEN o.offer_status = 'ACCEPTED' THEN 1 ELSE 0 END) > 0 THEN 'PLACED'
            WHEN SUM(CASE WHEN o.offer_status = 'OFFERED' THEN 1 ELSE 0 END) > 0 THEN 'OFFER_RECEIVED'
            ELSE 'UNPLACED'
        END AS placement_status
    FROM students s
    INNER JOIN users u ON s.user_id = u.user_id
    INNER JOIN departments d ON s.department_id = d.department_id
    LEFT JOIN applications a ON s.student_id = a.student_id
    LEFT JOIN interview_rounds r ON a.application_id = r.application_id
    LEFT JOIN placement_offers o ON a.application_id = o.application_id
    GROUP BY s.student_id, s.enrollment_number, u.full_name, u.email, d.department_code, s.cgpa, s.active_backlogs;
    """)

    cur.execute("DROP VIEW IF EXISTS v_job_opening_company_summary;")
    cur.execute("""
    CREATE VIEW v_job_opening_company_summary AS
    SELECT 
        j.job_id,
        c.company_name,
        c.industry,
        j.job_title,
        j.job_type,
        j.package_lpa,
        j.minimum_cgpa,
        j.maximum_backlogs,
        j.location,
        j.application_deadline,
        j.job_status,
        GROUP_CONCAT(DISTINCT d.department_code) AS eligible_departments,
        COUNT(DISTINCT a.application_id) AS total_applicants
    FROM job_openings j
    INNER JOIN companies c ON j.company_id = c.company_id
    LEFT JOIN job_eligibility_departments jed ON j.job_id = jed.job_id
    LEFT JOIN departments d ON jed.department_id = d.department_id
    LEFT JOIN applications a ON j.job_id = a.job_id
    GROUP BY j.job_id, c.company_name, c.industry, j.job_title, j.job_type, j.package_lpa, j.minimum_cgpa, j.maximum_backlogs, j.location, j.application_deadline, j.job_status;
    """)

    cur.execute("DROP VIEW IF EXISTS v_department_placement_statistics;")
    cur.execute("""
    CREATE VIEW v_department_placement_statistics AS
    SELECT 
        d.department_id,
        d.department_code,
        d.department_name,
        COUNT(DISTINCT s.student_id) AS total_students,
        COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) AS placed_students,
        ROUND(
            (COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) * 100.0) / 
            NULLIF(COUNT(DISTINCT s.student_id), 0), 
            2
        ) AS placement_percentage,
        COALESCE(MAX(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 0.00) AS highest_package_lpa,
        COALESCE(ROUND(AVG(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 2), 0.00) AS average_package_lpa
    FROM departments d
    LEFT JOIN students s ON d.department_id = s.department_id
    LEFT JOIN applications a ON s.student_id = a.student_id
    LEFT JOIN placement_offers o ON a.application_id = o.application_id
    GROUP BY d.department_id, d.department_code, d.department_name;
    """)

    # Seed initial data if tables are empty (before triggers so initial batch doesn't trigger audit cascade)
    cur.execute("SELECT COUNT(*) FROM departments;")
    if cur.fetchone()[0] == 0:
        _seed_sample_data(cur)

    # =========================================================================
    # TRIGGERS
    # =========================================================================
    cur.execute("DROP TRIGGER IF EXISTS trg_after_application_insert;")
    cur.execute("""
    CREATE TRIGGER trg_after_application_insert
    AFTER INSERT ON applications
    FOR EACH ROW
    BEGIN
        INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details, created_at)
        VALUES (
            (SELECT user_id FROM students WHERE student_id = NEW.student_id LIMIT 1),
            'NEW_APPLICATION_SUBMITTED',
            'APPLICATION',
            NEW.application_id,
            'Student ID ' || NEW.student_id || ' applied for Job Opening ID ' || NEW.job_id || '. Initial status: ' || NEW.application_status,
            datetime('now', 'localtime')
        );
    END;
    """)

    cur.execute("DROP TRIGGER IF EXISTS trg_after_offer_update;")
    cur.execute("""
    CREATE TRIGGER trg_after_offer_update
    AFTER UPDATE ON placement_offers
    FOR EACH ROW
    WHEN NEW.offer_status = 'ACCEPTED' AND OLD.offer_status <> 'ACCEPTED'
    BEGIN
        UPDATE applications
        SET application_status = 'SELECTED', updated_at = datetime('now', 'localtime')
        WHERE application_id = NEW.application_id;

        INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details, created_at)
        VALUES (
            (SELECT s.user_id FROM applications a JOIN students s ON a.student_id = s.student_id WHERE a.application_id = NEW.application_id LIMIT 1),
            'PLACEMENT_OFFER_ACCEPTED',
            'PLACEMENT_OFFER',
            NEW.offer_id,
            'Offer ID ' || NEW.offer_id || ' accepted. Package: ' || NEW.offered_package_lpa || ' LPA. Application status updated to SELECTED.',
            datetime('now', 'localtime')
        );
    END;
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully at:", DB_PATH)


def _seed_sample_data(cur):
    """Inserts realistic data matching college_placement_all_in_one.sql."""
    # Departments
    cur.executemany("""
    INSERT INTO departments (department_id, department_name, department_code, description) VALUES (?, ?, ?, ?)
    """, [
        (1, 'Computer Science & Engineering', 'CSE', 'Department of Computer Science & Engineering'),
        (2, 'Information Technology', 'IT', 'Department of Information Technology & Software Systems'),
        (3, 'Electronics & Communication Engineering', 'ECE', 'Department of Electronics & Communication'),
        (4, 'Mechanical Engineering', 'MECH', 'Department of Mechanical & Automation Engineering')
    ])

    # Users
    users_data = [
        (1, 'Prof. Anand Sharma', 'admin@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'ADMIN', 'ACTIVE'),
        (2, 'Sarah Jenkins', 'sarah.jenkins@google.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (3, 'Vikram Malhotra', 'vikram.m@microsoft.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (4, 'Rachel Green', 'rachel.g@amazon.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (5, 'Suresh Iyer', 'suresh.i@tcs.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (6, 'Neha Kulkarni', 'neha.k@infosys.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (7, 'David Miller', 'david.m@deloitte.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (101, 'Rahul Verma', 'rahul.verma@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (102, 'Priya Nair', 'priya.nair@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (103, 'Amit Patel', 'amit.patel@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (104, 'Sneha Joshi', 'sneha.joshi@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (105, 'Rohan Gupta', 'rohan.gupta@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (106, 'Ananya Sen', 'ananya.sen@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (107, 'Karthik Rao', 'karthik.rao@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (108, 'Divya Menon', 'divya.menon@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (109, 'Aditya Saxena', 'aditya.saxena@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (110, 'Meera Reddy', 'meera.reddy@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (111, 'Tanmay Deshmukh', 'tanmay.d@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (112, 'Pooja Hegde', 'pooja.hegde@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (113, 'Varun Chopra', 'varun.chopra@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (114, 'Shreya Das', 'shreya.das@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (115, 'Nikhil Kulkarni', 'nikhil.k@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (116, 'Ritu Singhania', 'ritu.s@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (117, 'Gaurav Bhat', 'gaurav.bhat@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (118, 'Isha Kapoor', 'isha.kapoor@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (119, 'Siddharth Roy', 'siddharth.roy@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'),
        (120, 'Kavya Pillai', 'kavya.pillai@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE')
    ]
    cur.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", users_data)

    # Students
    students_data = [
        (1, 101, 'EN2021CSE001', 1, 2025, 9.45, 0, '9876543210', 'https://campushire.edu/resumes/EN2021CSE001.pdf', 'VERIFIED'),
        (2, 102, 'EN2021CSE002', 1, 2025, 9.10, 0, '9876543211', 'https://campushire.edu/resumes/EN2021CSE002.pdf', 'VERIFIED'),
        (3, 103, 'EN2021CSE003', 1, 2025, 8.65, 0, '9876543212', 'https://campushire.edu/resumes/EN2021CSE003.pdf', 'VERIFIED'),
        (4, 104, 'EN2021CSE004', 1, 2025, 8.20, 0, '9876543213', 'https://campushire.edu/resumes/EN2021CSE004.pdf', 'VERIFIED'),
        (5, 105, 'EN2021CSE005', 1, 2025, 7.30, 1, '9876543214', 'https://campushire.edu/resumes/EN2021CSE005.pdf', 'VERIFIED'),
        (6, 106, 'EN2021IT001', 2, 2025, 9.30, 0, '9876543215', 'https://campushire.edu/resumes/EN2021IT001.pdf', 'VERIFIED'),
        (7, 107, 'EN2021IT002', 2, 2025, 8.80, 0, '9876543216', 'https://campushire.edu/resumes/EN2021IT002.pdf', 'VERIFIED'),
        (8, 108, 'EN2021IT003', 2, 2025, 7.90, 0, '9876543217', 'https://campushire.edu/resumes/EN2021IT003.pdf', 'VERIFIED'),
        (9, 109, 'EN2021IT004', 2, 2025, 7.15, 1, '9876543218', 'https://campushire.edu/resumes/EN2021IT004.pdf', 'VERIFIED'),
        (10, 110, 'EN2021IT005', 2, 2025, 6.70, 0, '9876543219', 'https://campushire.edu/resumes/EN2021IT005.pdf', 'VERIFIED'),
        (11, 111, 'EN2021ECE001', 3, 2025, 8.95, 0, '9876543220', 'https://campushire.edu/resumes/EN2021ECE001.pdf', 'VERIFIED'),
        (12, 112, 'EN2021ECE002', 3, 2025, 8.40, 0, '9876543221', 'https://campushire.edu/resumes/EN2021ECE002.pdf', 'VERIFIED'),
        (13, 113, 'EN2021ECE003', 3, 2025, 7.80, 0, '9876543222', 'https://campushire.edu/resumes/EN2021ECE003.pdf', 'VERIFIED'),
        (14, 114, 'EN2021ECE004', 3, 2025, 7.25, 0, '9876543223', 'https://campushire.edu/resumes/EN2021ECE004.pdf', 'VERIFIED'),
        (15, 115, 'EN2021ECE005', 3, 2025, 6.40, 2, '9876543224', 'https://campushire.edu/resumes/EN2021ECE005.pdf', 'VERIFIED'),
        (16, 116, 'EN2021MEC001', 4, 2025, 8.70, 0, '9876543225', 'https://campushire.edu/resumes/EN2021MEC001.pdf', 'VERIFIED'),
        (17, 117, 'EN2021MEC002', 4, 2025, 8.10, 0, '9876543226', 'https://campushire.edu/resumes/EN2021MEC002.pdf', 'VERIFIED'),
        (18, 118, 'EN2021MEC003', 4, 2025, 7.50, 0, '9876543227', 'https://campushire.edu/resumes/EN2021MEC003.pdf', 'VERIFIED'),
        (19, 119, 'EN2021MEC004', 4, 2025, 6.90, 1, '9876543228', 'https://campushire.edu/resumes/EN2021MEC004.pdf', 'VERIFIED'),
        (20, 120, 'EN2021MEC005', 4, 2025, 6.20, 0, '9876543229', 'https://campushire.edu/resumes/EN2021MEC005.pdf', 'VERIFIED')
    ]
    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", students_data)

    # Companies
    companies_data = [
        (1, 'Google India', 'Technology & Internet', 'https://careers.google.com', 'Global technology leader in search, cloud computing, and software.', 'Bengaluru, India'),
        (2, 'Microsoft', 'Enterprise Software & Cloud', 'https://careers.microsoft.com', 'Pioneer in operating systems, Azure cloud, and developer platforms.', 'Hyderabad, India'),
        (3, 'Amazon', 'E-Commerce & Cloud Computing', 'https://amazon.jobs', 'Global leader in e-commerce, cloud infrastructure, and streaming.', 'Bengaluru, India'),
        (4, 'Tata Consultancy Services', 'IT Services & Consulting', 'https://www.tcs.com/careers', 'Largest Indian multinational information technology services provider.', 'Mumbai, India'),
        (5, 'Infosys', 'Information Technology', 'https://www.infosys.com/careers', 'Global leader in next-generation digital services and consulting.', 'Bengaluru, India'),
        (6, 'Deloitte Consulting', 'Management & Technology Consulting', 'https://www2.deloitte.com', 'Leading global provider of audit, consulting, advisory, and tax.', 'Hyderabad, India')
    ]
    cur.executemany("INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", companies_data)

    # Recruiters
    recruiters_data = [
        (1, 2, 1, 'Senior University Recruiter', '9811223344'),
        (2, 3, 2, 'Campus Talent Acquisition Lead', '9822334455'),
        (3, 4, 3, 'Technical Sourcing Specialist', '9833445566'),
        (4, 5, 4, 'Regional Hiring Manager', '9844556677'),
        (5, 6, 5, 'Campus Relations Lead', '9855667788'),
        (6, 7, 6, 'Associate Director - Recruitment', '9866778899')
    ]
    cur.executemany("INSERT INTO recruiters VALUES (?, ?, ?, ?, ?, datetime('now'))", recruiters_data)

    # Job Openings
    jobs_data = [
        (1, 1, 'Software Engineer - Campus', 'Build scalable distributed systems, algorithms, and backend services.', 'FULL_TIME', 'Bengaluru', 8.50, 0, 28.50, '2026-12-31 23:59:59', '2027-01-15 09:00:00', 'OPEN', 1),
        (2, 2, 'Software Development Engineer', 'Design core cloud features for Azure enterprise customers.', 'FULL_TIME', 'Hyderabad', 8.00, 0, 24.00, '2026-12-31 23:59:59', '2027-01-20 09:30:00', 'OPEN', 1),
        (3, 3, 'SDE-1 (Full Stack & Systems)', 'Deliver high-volume payment services and AWS infrastructure tools.', 'FULL_TIME', 'Bengaluru', 7.50, 0, 22.00, '2026-12-31 23:59:59', '2027-01-25 10:00:00', 'OPEN', 1),
        (4, 4, 'TCS Digital Engineer', 'Work on Next-Gen technologies like AI/ML, Cloud, and Big Data.', 'FULL_TIME', 'Pune / Mumbai', 6.50, 1, 7.50, '2026-12-31 23:59:59', '2027-02-05 09:00:00', 'OPEN', 1),
        (5, 4, 'TCS Ninja Associate', 'Foundational software engineering across banking, retail, and healthcare.', 'FULL_TIME', 'PAN India', 6.00, 2, 3.80, '2026-12-31 23:59:59', '2027-02-10 09:00:00', 'OPEN', 1),
        (6, 5, 'Specialist Programmer (SP)', 'High-end coding profile focusing on algorithmic problem solving.', 'FULL_TIME', 'Bengaluru / Pune', 7.00, 0, 9.50, '2026-12-31 23:59:59', '2027-02-15 09:00:00', 'OPEN', 1),
        (7, 6, 'Technology Analyst', 'Consulting on enterprise ERP, cybersecurity, and cloud migration.', 'FULL_TIME', 'Hyderabad / Gurugram', 6.80, 0, 8.50, '2026-12-31 23:59:59', '2027-02-20 09:00:00', 'OPEN', 1),
        (8, 6, 'Core Engineering Consultant', 'Supply chain automation and industrial engineering analytics.', 'FULL_TIME', 'Pune', 6.50, 1, 7.00, '2026-12-31 23:59:59', '2027-02-25 09:00:00', 'OPEN', 1)
    ]
    cur.executemany("INSERT INTO job_openings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", jobs_data)

    # Job Eligibility Departments
    jed_data = [
        (1, 1), (1, 2),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3),
        (4, 1), (4, 2), (4, 3), (4, 4),
        (5, 1), (5, 2), (5, 3), (5, 4),
        (6, 1), (6, 2),
        (7, 1), (7, 2), (7, 3),
        (8, 4)
    ]
    cur.executemany("INSERT INTO job_eligibility_departments VALUES (?, ?)", jed_data)

    # Applications
    apps_data = [
        (1, 1, 1, '2026-09-01 10:00:00', 'SELECTED'),
        (2, 2, 1, '2026-09-01 10:15:00', 'SELECTED'),
        (3, 6, 1, '2026-09-01 10:30:00', 'REJECTED'),
        (4, 7, 1, '2026-09-01 10:45:00', 'SHORTLISTED'),
        (5, 1, 2, '2026-09-02 11:00:00', 'SELECTED'),
        (6, 3, 2, '2026-09-02 11:15:00', 'SELECTED'),
        (7, 6, 2, '2026-09-02 11:30:00', 'SELECTED'),
        (8, 11, 2, '2026-09-02 11:45:00', 'SELECTED'),
        (9, 2, 3, '2026-09-03 09:00:00', 'SELECTED'),
        (10, 4, 3, '2026-09-03 09:15:00', 'SELECTED'),
        (11, 7, 3, '2026-09-03 09:30:00', 'SHORTLISTED'),
        (12, 12, 3, '2026-09-03 09:45:00', 'REJECTED'),
        (13, 4, 4, '2026-09-04 14:00:00', 'SELECTED'),
        (14, 8, 4, '2026-09-04 14:15:00', 'SELECTED'),
        (15, 13, 4, '2026-09-04 14:30:00', 'SELECTED'),
        (16, 16, 4, '2026-09-04 14:45:00', 'SELECTED'),
        (17, 17, 4, '2026-09-04 15:00:00', 'SHORTLISTED'),
        (18, 5, 5, '2026-09-05 10:00:00', 'SELECTED'),
        (19, 9, 5, '2026-09-05 10:15:00', 'SELECTED'),
        (20, 15, 5, '2026-09-05 10:30:00', 'SELECTED'),
        (21, 19, 5, '2026-09-05 10:45:00', 'APPLIED'),
        (22, 3, 6, '2026-09-06 11:00:00', 'SHORTLISTED'),
        (23, 7, 6, '2026-09-06 11:15:00', 'SELECTED'),
        (24, 8, 6, '2026-09-06 11:30:00', 'APPLIED'),
        (25, 12, 7, '2026-09-07 12:00:00', 'SELECTED'),
        (26, 14, 7, '2026-09-07 12:15:00', 'SHORTLISTED'),
        (27, 16, 8, '2026-09-08 14:00:00', 'SELECTED'),
        (28, 18, 8, '2026-09-08 14:15:00', 'SELECTED')
    ]
    cur.executemany("INSERT INTO applications VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))", apps_data)

    # Interview Rounds
    rounds_data = [
        (1, 1, 1, 'Online Coding Assessment', '2026-09-10 10:00:00', 95.00, 'Solved both algorithmic problems with optimal time complexity.', 'PASSED', 2),
        (2, 1, 2, 'Technical Interview - Data Structures', '2026-09-15 14:00:00', 92.50, 'Excellent grasp of binary trees, dynamic programming, and graphs.', 'PASSED', 2),
        (3, 1, 3, 'System Design & Googliness HR', '2026-09-18 16:00:00', 88.00, 'Clear communication and strong cultural alignment.', 'PASSED', 2),
        (4, 2, 1, 'Online Coding Assessment', '2026-09-10 10:00:00', 98.00, 'Scored 100% test cases within 35 minutes.', 'PASSED', 2),
        (5, 2, 2, 'Technical Interview - Algorithms', '2026-09-15 15:00:00', 94.00, 'Outstanding problem-solving intuition and clean code.', 'PASSED', 2),
        (6, 2, 3, 'Managerial & HR Round', '2026-09-18 17:00:00', 90.00, 'Very articulate, team player, ready to join.', 'PASSED', 2),
        (7, 3, 1, 'Online Coding Assessment', '2026-09-10 10:00:00', 82.00, 'Cleared cut-off with 85% test cases passing.', 'PASSED', 2),
        (8, 3, 2, 'Technical Interview - Algorithms', '2026-09-15 16:00:00', 52.00, 'Struggled with memory constraints in graph problem.', 'FAILED', 2),
        (9, 6, 1, 'Online Technical Test', '2026-09-12 11:00:00', 90.00, 'Fast code execution and strong debugging skills.', 'PASSED', 3),
        (10, 6, 2, 'System Architecture & OOPS', '2026-09-16 11:30:00', 87.50, 'Solid understanding of microservices and REST APIs.', 'PASSED', 3),
        (11, 6, 3, 'Partner Round', '2026-09-19 14:00:00', 85.00, 'Recommended for Azure Cloud Core team.', 'PASSED', 3),
        (12, 7, 1, 'Online Technical Test', '2026-09-12 11:00:00', 92.00, 'Flawless logic.', 'PASSED', 3),
        (13, 7, 2, 'Technical Interview', '2026-09-16 14:00:00', 89.00, 'Demonstrated deep understanding of distributed databases.', 'PASSED', 3),
        (14, 7, 3, 'HR & Fitment Round', '2026-09-19 15:30:00', 91.00, 'Great communication, confident candidate.', 'PASSED', 3),
        (15, 11, 1, 'Online Assessment (OA)', '2026-09-14 10:00:00', 85.00, 'Cleared OA with strong debugging score.', 'PASSED', 4),
        (16, 11, 2, 'Technical Round 1', '2026-09-22 11:00:00', None, 'Interview scheduled for upcoming Monday.', 'PENDING', 4)
    ]
    cur.executemany("INSERT INTO interview_rounds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", rounds_data)

    # Placement Offers
    offers_data = [
        (1, 1, 28.50, '2026-09-20', '2025-07-01', 'ACCEPTED'),
        (2, 2, 28.50, '2026-09-20', '2025-07-01', 'ACCEPTED'),
        (3, 5, 24.00, '2026-09-22', '2025-07-15', 'DECLINED'),
        (4, 6, 24.00, '2026-09-22', '2025-07-15', 'ACCEPTED'),
        (5, 7, 24.00, '2026-09-22', '2025-07-15', 'ACCEPTED'),
        (6, 8, 24.00, '2026-09-22', '2025-07-15', 'ACCEPTED'),
        (7, 10, 22.00, '2026-09-25', '2025-08-01', 'ACCEPTED'),
        (8, 14, 7.50, '2026-09-26', '2025-08-15', 'ACCEPTED'),
        (9, 15, 7.50, '2026-09-26', '2025-08-15', 'ACCEPTED'),
        (10, 16, 7.50, '2026-09-26', '2025-08-15', 'ACCEPTED'),
        (11, 23, 9.50, '2026-09-28', '2025-07-20', 'ACCEPTED'),
        (12, 25, 8.50, '2026-09-29', '2025-09-01', 'ACCEPTED'),
        (13, 28, 7.00, '2026-09-30', '2025-09-01', 'OFFERED')
    ]
    cur.executemany("INSERT INTO placement_offers VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", offers_data)

    # Audit Logs
    audit_data = [
        (1, 1, 'CREATE_DATABASE', 'SYSTEM', None, 'College placement system database initialized.'),
        (2, 1, 'CREATE_JOB', 'JOB_OPENING', 1, 'Prof. Anand Sharma published job: Google SDE Campus Drive.'),
        (3, 101, 'SUBMIT_APPLICATION', 'APPLICATION', 1, 'Rahul Verma submitted application for Google SDE.'),
        (4, 2, 'RECORD_INTERVIEW_RESULT', 'INTERVIEW_ROUND', 3, 'Sarah Jenkins marked Round 3 as PASSED for Rahul Verma.'),
        (5, 2, 'GENERATE_OFFER', 'PLACEMENT_OFFER', 1, 'Sarah Jenkins rolled out 28.50 LPA offer to Rahul Verma.'),
        (6, 101, 'ACCEPT_OFFER', 'PLACEMENT_OFFER', 1, 'Rahul Verma accepted the placement offer from Google India.')
    ]
    cur.executemany("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?, ?, datetime('now'))", audit_data)


# =============================================================================
# STORED PROCEDURES & CURSORS EXECUTORS
# =============================================================================

def sp_get_eligible_students(job_id):
    """Executes procedure sp_get_eligible_students(job_id)."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT minimum_cgpa, maximum_backlogs, job_title FROM job_openings WHERE job_id = ?", (job_id,))
    job = cur.fetchone()
    if not job:
        conn.close()
        raise ValueError(f"Job ID {job_id} does not exist.")

    min_cgpa = job['minimum_cgpa']
    max_backlogs = job['maximum_backlogs']

    cur.execute("""
        SELECT 
            s.student_id,
            s.enrollment_number,
            u.full_name AS student_name,
            d.department_code,
            s.cgpa,
            s.active_backlogs,
            CASE 
                WHEN a.application_id IS NOT NULL THEN 'ALREADY_APPLIED'
                ELSE 'NOT_APPLIED'
            END AS application_status
        FROM students s
        INNER JOIN users u ON s.user_id = u.user_id
        INNER JOIN departments d ON s.department_id = d.department_id
        INNER JOIN job_eligibility_departments jed ON s.department_id = jed.department_id AND jed.job_id = ?
        LEFT JOIN applications a ON s.student_id = a.student_id AND a.job_id = ?
        WHERE u.account_status = 'ACTIVE'
          AND s.cgpa >= ?
          AND s.active_backlogs <= ?
        ORDER BY s.cgpa DESC;
    """, (job_id, job_id, min_cgpa, max_backlogs))

    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return {
        'job_title': job['job_title'],
        'minimum_cgpa': min_cgpa,
        'maximum_backlogs': max_backlogs,
        'eligible_students': results
    }


def sp_get_company_placement_summary():
    """Executes procedure sp_get_company_placement_summary()."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            c.company_id,
            c.company_name,
            c.industry,
            COUNT(DISTINCT j.job_id) AS total_drives_posted,
            COUNT(DISTINCT a.application_id) AS total_applications_received,
            COUNT(DISTINCT r.round_id) AS interviews_conducted,
            COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN a.student_id END) AS candidates_hired,
            COALESCE(MAX(o.offered_package_lpa), 0.00) AS highest_package_lpa,
            COALESCE(ROUND(AVG(o.offered_package_lpa), 2), 0.00) AS average_package_lpa
        FROM companies c
        LEFT JOIN job_openings j ON c.company_id = j.company_id
        LEFT JOIN applications a ON j.job_id = a.job_id
        LEFT JOIN interview_rounds r ON a.application_id = r.application_id
        LEFT JOIN placement_offers o ON a.application_id = o.application_id
        GROUP BY c.company_id, c.company_name, c.industry
        ORDER BY candidates_hired DESC, highest_package_lpa DESC;
    """)
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results


def sp_get_department_placement_report(grad_year=None):
    """Executes procedure sp_get_department_placement_report(grad_year)."""
    conn = get_db_connection()
    cur = conn.cursor()
    if grad_year:
        cur.execute("""
            SELECT 
                d.department_code,
                d.department_name,
                COUNT(DISTINCT s.student_id) AS total_students,
                COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) AS placed_students,
                (COUNT(DISTINCT s.student_id) - COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END)) AS unplaced_students,
                ROUND(
                    (COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) * 100.0) / 
                    NULLIF(COUNT(DISTINCT s.student_id), 0), 
                    2
                ) AS placement_percentage,
                COALESCE(MAX(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 0.00) AS max_package_lpa,
                COALESCE(ROUND(AVG(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 2), 0.00) AS avg_package_lpa
            FROM departments d
            LEFT JOIN students s ON d.department_id = s.department_id AND s.graduation_year = ?
            LEFT JOIN applications a ON s.student_id = a.student_id
            LEFT JOIN placement_offers o ON a.application_id = o.application_id
            GROUP BY d.department_id, d.department_code, d.department_name
            ORDER BY placement_percentage DESC;
        """, (grad_year,))
    else:
        cur.execute("""
            SELECT 
                d.department_code,
                d.department_name,
                COUNT(DISTINCT s.student_id) AS total_students,
                COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) AS placed_students,
                (COUNT(DISTINCT s.student_id) - COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END)) AS unplaced_students,
                ROUND(
                    (COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) * 100.0) / 
                    NULLIF(COUNT(DISTINCT s.student_id), 0), 
                    2
                ) AS placement_percentage,
                COALESCE(MAX(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 0.00) AS max_package_lpa,
                COALESCE(ROUND(AVG(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 2), 0.00) AS avg_package_lpa
            FROM departments d
            LEFT JOIN students s ON d.department_id = s.department_id
            LEFT JOIN applications a ON s.student_id = a.student_id
            LEFT JOIN placement_offers o ON a.application_id = o.application_id
            GROUP BY d.department_id, d.department_code, d.department_name
            ORDER BY placement_percentage DESC;
        """)
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results


def sp_cursor_interview_round_statistics():
    """Simulates PL/SQL Cursor: cur_rounds iterating over interview_rounds."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Emulate SQL cursor iteration
    cur.execute("SELECT round_status, score FROM interview_rounds;")
    
    total_rounds = 0
    passed_count = 0
    failed_count = 0
    pending_count = 0
    not_attended_count = 0
    total_score = 0.0
    scored_rounds = 0

    while True:
        row = cur.fetchone()
        if row is None:
            break
        
        status = row['round_status']
        score = row['score']
        total_rounds += 1

        if status == 'PASSED':
            passed_count += 1
        elif status == 'FAILED':
            failed_count += 1
        elif status == 'PENDING':
            pending_count += 1
        elif status == 'NOT_ATTENDED':
            not_attended_count += 1

        if score is not None:
            total_score += score
            scored_rounds += 1

    avg_score = round(total_score / scored_rounds, 2) if scored_rounds > 0 else 0.00
    conn.close()

    return {
        'total_interview_rounds': total_rounds,
        'total_passed': passed_count,
        'total_failed': failed_count,
        'total_pending': pending_count,
        'total_not_attended': not_attended_count,
        'average_score_of_evaluated_rounds': avg_score
    }


def execute_custom_query(query):
    """Executes custom SQL query entered by user in SQL Terminal."""
    conn = get_db_connection()
    cur = conn.cursor()
    query_stripped = query.strip()
    
    is_select = query_stripped.upper().startswith(("SELECT", "PRAGMA", "EXPLAIN"))
    
    try:
        start_time = datetime.now()
        cur.execute(query)
        duration_ms = round((datetime.now() - start_time).total_seconds() * 1000, 2)

        if is_select:
            rows = [dict(row) for row in cur.fetchall()]
            columns = [desc[0] for desc in cur.description] if cur.description else []
            conn.close()
            return {
                'success': True,
                'is_select': True,
                'columns': columns,
                'rows': rows,
                'row_count': len(rows),
                'duration_ms': duration_ms
            }
        else:
            conn.commit()
            affected = cur.rowcount
            conn.close()
            return {
                'success': True,
                'is_select': False,
                'affected_rows': affected,
                'duration_ms': duration_ms
            }
    except Exception as e:
        conn.close()
        return {
            'success': False,
            'error': str(e)
        }

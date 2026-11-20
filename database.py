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
    """Inserts realistic college-level placement drive data (50 students, 16 companies, 18 drives)."""
    import expand_dataset
    expand_dataset.seed_college_dataset(cur)


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

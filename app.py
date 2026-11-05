"""
CampusHire - College Placement & Recruitment Management System
Flask Web Application with Full Data Manipulation (CRUD), Triggers,
Stored Procedures, Views, Cursors, and Interactive SQL Terminal.
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'campushire-secret-key-del-project-2026'

# Ensure database is initialized on startup
database.init_db(reset=False)


@app.context_processor
def inject_global_stats():
    """Injects key summary metrics into every template."""
    try:
        conn = database.get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0] or 0
        
        cur.execute("SELECT COUNT(*) FROM job_openings WHERE job_status = 'OPEN'")
        open_jobs = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(*) FROM companies")
        total_companies = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(*) FROM placement_offers WHERE offer_status = 'ACCEPTED'")
        placed_students = cur.fetchone()[0] or 0

        cur.execute("SELECT fn_calculate_overall_placement_percentage()")
        placement_rate = cur.fetchone()[0] or 0.0

        conn.close()
        return {
            'nav_total_students': total_students,
            'nav_open_jobs': open_jobs,
            'nav_total_companies': total_companies,
            'nav_placed_students': placed_students,
            'nav_placement_rate': placement_rate
        }
    except Exception:
        return {}


# =============================================================================
# 1. DASHBOARD & ANALYTICS
# =============================================================================

@app.route('/')
def dashboard():
    conn = database.get_db_connection()
    cur = conn.cursor()

    # Department placement stats view
    cur.execute("SELECT * FROM v_department_placement_statistics ORDER BY placement_percentage DESC")
    dept_stats = [dict(row) for row in cur.fetchall()]

    # Company summary
    cur.execute("SELECT * FROM v_job_opening_company_summary WHERE job_status = 'OPEN' LIMIT 5")
    open_drives = [dict(row) for row in cur.fetchall()]

    # Recent offers
    cur.execute("""
        SELECT o.offer_id, u.full_name AS student_name, c.company_name, j.job_title, 
               o.offered_package_lpa, o.offer_status, o.offer_date
        FROM placement_offers o
        JOIN applications a ON o.application_id = a.application_id
        JOIN students s ON a.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY o.offer_date DESC LIMIT 6
    """)
    recent_offers = [dict(row) for row in cur.fetchall()]

    # Recent Audit Logs (Triggers & actions)
    cur.execute("""
        SELECT a.audit_id, u.full_name AS user_name, a.action, a.entity_type, a.details, a.created_at
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.user_id
        ORDER BY a.audit_id DESC LIMIT 8
    """)
    recent_logs = [dict(row) for row in cur.fetchall()]

    # Stats metrics
    cur.execute("SELECT MAX(offered_package_lpa), AVG(offered_package_lpa) FROM placement_offers WHERE offer_status = 'ACCEPTED'")
    pkg_row = cur.fetchone()
    max_pkg = pkg_row[0] or 0.00
    avg_pkg = round(pkg_row[1] or 0.00, 2)

    conn.close()

    return render_template(
        'dashboard.html',
        dept_stats=dept_stats,
        open_drives=open_drives,
        recent_offers=recent_offers,
        recent_logs=recent_logs,
        max_package=max_pkg,
        avg_package=avg_pkg
    )


# =============================================================================
# 2. STUDENTS MANAGEMENT (CRUD & DATA MANIPULATION)
# =============================================================================

@app.route('/students')
def students():
    conn = database.get_db_connection()
    cur = conn.cursor()

    dept_filter = request.args.get('dept', '')
    status_filter = request.args.get('status', '')
    search = request.args.get('q', '').strip()

    query = "SELECT * FROM v_student_placement_summary WHERE 1=1"
    params = []

    if dept_filter:
        query += " AND department_code = ?"
        params.append(dept_filter)
    if status_filter:
        query += " AND placement_status = ?"
        params.append(status_filter)
    if search:
        query += " AND (student_name LIKE ? OR enrollment_number LIKE ? OR email LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard])

    query += " ORDER BY cgpa DESC"
    cur.execute(query, params)
    students_list = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT department_id, department_name, department_code FROM departments ORDER BY department_name")
    departments = [dict(row) for row in cur.fetchall()]

    conn.close()
    return render_template('students.html', students=students_list, departments=departments, dept_filter=dept_filter, status_filter=status_filter, search=search)


@app.route('/students/create', methods=['POST'])
def create_student():
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    enrollment_number = request.form.get('enrollment_number', '').strip()
    department_id = request.form.get('department_id')
    graduation_year = request.form.get('graduation_year')
    cgpa = request.form.get('cgpa')
    active_backlogs = request.form.get('active_backlogs', 0)
    phone = request.form.get('phone', '').strip()
    resume_url = request.form.get('resume_url', '').strip()

    if not full_name or not email or not enrollment_number or not cgpa:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('students'))

    try:
        cgpa_val = float(cgpa)
        if cgpa_val < 0.0 or cgpa_val > 10.0:
            flash('CGPA must be between 0.00 and 10.00.', 'danger')
            return redirect(url_for('students'))
    except ValueError:
        flash('Invalid CGPA format.', 'danger')
        return redirect(url_for('students'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        # Create user record
        cur.execute("""
            INSERT INTO users (full_name, email, password_hash, role, account_status)
            VALUES (?, ?, '$2a$10$defaultHashPasswordDemoStudent1234567890', 'STUDENT', 'ACTIVE')
        """, (full_name, email))
        user_id = cur.lastrowid

        # Create student record
        cur.execute("""
            INSERT INTO students (user_id, enrollment_number, department_id, graduation_year, cgpa, active_backlogs, phone, resume_url, profile_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'VERIFIED')
        """, (user_id, enrollment_number, department_id, graduation_year, cgpa_val, active_backlogs, phone, resume_url))
        student_id = cur.lastrowid

        # Audit log
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'CREATE_STUDENT', 'STUDENT', ?, ?)
        """, (1, student_id, f'New student enrolled: {full_name} ({enrollment_number}) in Dept {department_id}'))

        conn.commit()
        flash(f'Student "{full_name}" registered successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error adding student: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('students'))


@app.route('/students/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    cgpa = request.form.get('cgpa')
    active_backlogs = request.form.get('active_backlogs')
    phone = request.form.get('phone', '').strip()
    resume_url = request.form.get('resume_url', '').strip()
    profile_status = request.form.get('profile_status', 'VERIFIED')

    try:
        cgpa_val = float(cgpa)
        backlogs_val = int(active_backlogs)
        if cgpa_val < 0.0 or cgpa_val > 10.0:
            flash('CGPA must be between 0.00 and 10.00.', 'danger')
            return redirect(url_for('students'))
        if backlogs_val < 0:
            flash('Backlogs cannot be negative.', 'danger')
            return redirect(url_for('students'))
    except ValueError:
        flash('Invalid numeric inputs.', 'danger')
        return redirect(url_for('students'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE students
            SET cgpa = ?, active_backlogs = ?, phone = ?, resume_url = ?, profile_status = ?, updated_at = datetime('now', 'localtime')
            WHERE student_id = ?
        """, (cgpa_val, backlogs_val, phone, resume_url, profile_status, student_id))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'UPDATE_STUDENT_PROFILE', 'STUDENT', ?, ?)
        """, (1, student_id, f'Updated student ID {student_id}: CGPA={cgpa_val}, Backlogs={backlogs_val}, Status={profile_status}'))

        conn.commit()
        flash('Student record updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating student: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('students'))


@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id, enrollment_number FROM students WHERE student_id = ?", (student_id,))
        row = cur.fetchone()
        if not row:
            flash('Student not found.', 'danger')
            return redirect(url_for('students'))

        user_id = row['user_id']
        enrollment = row['enrollment_number']

        # Delete dependent placement offers and applications if any
        cur.execute("""
            DELETE FROM placement_offers 
            WHERE application_id IN (SELECT application_id FROM applications WHERE student_id = ?)
        """, (student_id,))

        cur.execute("""
            DELETE FROM interview_rounds
            WHERE application_id IN (SELECT application_id FROM applications WHERE student_id = ?)
        """, (student_id,))

        cur.execute("DELETE FROM applications WHERE student_id = ?", (student_id,))
        cur.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'DELETE_STUDENT', 'STUDENT', ?, ?)
        """, (1, student_id, f'Deleted student {enrollment} and associated records.'))

        conn.commit()
        flash(f'Student {enrollment} deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('students'))


@app.route('/students/<int:student_id>/details')
def student_details(student_id):
    conn = database.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.*, u.full_name, u.email, d.department_name, d.department_code
        FROM students s
        JOIN users u ON s.user_id = u.user_id
        JOIN departments d ON s.department_id = d.department_id
        WHERE s.student_id = ?
    """, (student_id,))
    student = cur.fetchone()
    if not student:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404

    # Applications and offers
    cur.execute("""
        SELECT a.application_id, a.application_date, a.application_status,
               j.job_title, j.package_lpa, c.company_name,
               o.offer_id, o.offered_package_lpa, o.offer_status
        FROM applications a
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN placement_offers o ON a.application_id = o.application_id
        WHERE a.student_id = ?
        ORDER BY a.application_date DESC
    """, (student_id,))
    apps = [dict(r) for r in cur.fetchall()]

    conn.close()
    return jsonify({'student': dict(student), 'applications': apps})


# =============================================================================
# 3. COMPANIES & JOB DRIVES (CRUD & DATA MANIPULATION)
# =============================================================================

@app.route('/jobs')
def jobs():
    conn = database.get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM v_job_opening_company_summary ORDER BY job_id DESC")
    jobs_list = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM companies ORDER BY company_name")
    companies_list = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM departments ORDER BY department_name")
    departments = [dict(row) for row in cur.fetchall()]

    conn.close()
    return render_template('jobs.html', jobs=jobs_list, companies=companies_list, departments=departments)


@app.route('/companies/create', methods=['POST'])
def create_company():
    company_name = request.form.get('company_name', '').strip()
    industry = request.form.get('industry', '').strip()
    website = request.form.get('website', '').strip()
    headquarters = request.form.get('headquarters', '').strip()
    company_description = request.form.get('company_description', '').strip()

    if not company_name or not industry:
        flash('Company name and industry are required.', 'danger')
        return redirect(url_for('jobs'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO companies (company_name, industry, website, headquarters, company_description)
            VALUES (?, ?, ?, ?, ?)
        """, (company_name, industry, website, headquarters, company_description))
        company_id = cur.lastrowid

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'REGISTER_COMPANY', 'COMPANY', ?, ?)
        """, (1, company_id, f'Registered new partner company: {company_name}'))

        conn.commit()
        flash(f'Company "{company_name}" added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error registering company: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('jobs'))


@app.route('/jobs/create', methods=['POST'])
def create_job():
    company_id = request.form.get('company_id')
    job_title = request.form.get('job_title', '').strip()
    job_description = request.form.get('job_description', '').strip()
    job_type = request.form.get('job_type', 'FULL_TIME')
    location = request.form.get('location', '').strip()
    minimum_cgpa = request.form.get('minimum_cgpa', 0.0)
    maximum_backlogs = request.form.get('maximum_backlogs', 0)
    package_lpa = request.form.get('package_lpa')
    application_deadline = request.form.get('application_deadline')
    drive_date = request.form.get('drive_date') or None
    job_status = request.form.get('job_status', 'OPEN')
    dept_ids = request.form.getlist('department_ids')

    if not company_id or not job_title or not package_lpa or not application_deadline:
        flash('Please fill in all mandatory job opening fields.', 'danger')
        return redirect(url_for('jobs'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO job_openings (company_id, job_title, job_description, job_type, location,
                                     minimum_cgpa, maximum_backlogs, package_lpa, application_deadline,
                                     drive_date, job_status, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (company_id, job_title, job_description, job_type, location,
              float(minimum_cgpa), int(maximum_backlogs), float(package_lpa),
              application_deadline, drive_date, job_status))
        job_id = cur.lastrowid

        for dept_id in dept_ids:
            cur.execute("""
                INSERT INTO job_eligibility_departments (job_id, department_id)
                VALUES (?, ?)
            """, (job_id, dept_id))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'POST_JOB_DRIVE', 'JOB_OPENING', ?, ?)
        """, (1, job_id, f'Posted recruitment drive: {job_title} ({package_lpa} LPA)'))

        conn.commit()
        flash(f'Job opening "{job_title}" created successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error posting job: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('jobs'))


@app.route('/jobs/update/<int:job_id>', methods=['POST'])
def update_job(job_id):
    job_title = request.form.get('job_title', '').strip()
    job_type = request.form.get('job_type', 'FULL_TIME')
    location = request.form.get('location', '').strip()
    package_lpa = request.form.get('package_lpa')
    minimum_cgpa = request.form.get('minimum_cgpa', 0.0)
    maximum_backlogs = request.form.get('maximum_backlogs', 0)
    application_deadline = request.form.get('application_deadline')
    job_status = request.form.get('job_status', 'OPEN')

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE job_openings
            SET job_title = ?, job_type = ?, location = ?, package_lpa = ?,
                minimum_cgpa = ?, maximum_backlogs = ?, application_deadline = ?,
                job_status = ?, updated_at = datetime('now', 'localtime')
            WHERE job_id = ?
        """, (job_title, job_type, location, float(package_lpa), float(minimum_cgpa),
              int(maximum_backlogs), application_deadline, job_status, job_id))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'UPDATE_JOB_DRIVE', 'JOB_OPENING', ?, ?)
        """, (1, job_id, f'Updated job drive ID {job_id} ({job_title}, {package_lpa} LPA)'))

        conn.commit()
        flash(f'Job opening "{job_title}" updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating job: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('jobs'))


@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        # Check dependent applications
        cur.execute("SELECT COUNT(*) FROM applications WHERE job_id = ?", (job_id,))
        app_count = cur.fetchone()[0]

        cur.execute("DELETE FROM job_eligibility_departments WHERE job_id = ?", (job_id,))
        cur.execute("DELETE FROM applications WHERE job_id = ?", (job_id,))
        cur.execute("DELETE FROM job_openings WHERE job_id = ?", (job_id,))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'DELETE_JOB_DRIVE', 'JOB_OPENING', ?, ?)
        """, (1, job_id, f'Deleted Job Opening ID {job_id} and {app_count} associated applications.'))

        conn.commit()
        flash(f'Job opening #{job_id} deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting job: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('jobs'))


@app.route('/jobs/update_status/<int:job_id>', methods=['POST'])
def update_job_status(job_id):
    new_status = request.form.get('job_status')
    if new_status not in ['OPEN', 'CLOSED', 'DRAFT', 'CANCELLED']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('jobs'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE job_openings SET job_status = ?, updated_at = datetime('now', 'localtime') WHERE job_id = ?", (new_status, job_id))
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'UPDATE_JOB_STATUS', 'JOB_OPENING', ?, ?)
        """, (1, job_id, f'Recruitment drive status updated to {new_status}'))
        conn.commit()
        flash(f'Job ID {job_id} status updated to {new_status}.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('jobs'))


# =============================================================================
# 4. APPLICATIONS (CRUD & TRIGGER DEMONSTRATION)
# =============================================================================

@app.route('/applications')
def applications():
    conn = database.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT a.application_id, a.application_date, a.application_status,
               s.student_id, s.enrollment_number, u.full_name AS student_name, s.cgpa, d.department_code,
               j.job_id, j.job_title, j.package_lpa, c.company_name
        FROM applications a
        JOIN students s ON a.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN departments d ON s.department_id = d.department_id
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_id DESC
    """)
    apps = [dict(row) for row in cur.fetchall()]

    # Students for dropdown
    cur.execute("""
        SELECT s.student_id, u.full_name, s.enrollment_number, d.department_code, s.cgpa
        FROM students s
        JOIN users u ON s.user_id = u.user_id
        JOIN departments d ON s.department_id = d.department_id
        ORDER BY u.full_name
    """)
    students_list = [dict(row) for row in cur.fetchall()]

    # Open jobs for dropdown
    cur.execute("""
        SELECT j.job_id, j.job_title, c.company_name, j.minimum_cgpa, j.maximum_backlogs
        FROM job_openings j
        JOIN companies c ON j.company_id = c.company_id
        WHERE j.job_status = 'OPEN'
        ORDER BY j.job_title
    """)
    jobs_list = [dict(row) for row in cur.fetchall()]

    conn.close()
    return render_template('applications.html', applications=apps, students=students_list, jobs=jobs_list)


@app.route('/applications/create', methods=['POST'])
def create_application():
    student_id = request.form.get('student_id')
    job_id = request.form.get('job_id')

    if not student_id or not job_id:
        flash('Please select both student and job opening.', 'danger')
        return redirect(url_for('applications'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        # Check job status and deadline (mirroring trg_before_application_insert_check)
        cur.execute("SELECT job_status, application_deadline, minimum_cgpa, maximum_backlogs FROM job_openings WHERE job_id = ?", (job_id,))
        job = cur.fetchone()
        if not job:
            flash('Selected job opening does not exist.', 'danger')
            return redirect(url_for('applications'))

        if job['job_status'] != 'OPEN':
            flash('Validation Error: Applications can only be submitted for OPEN recruitment drives.', 'danger')
            return redirect(url_for('applications'))

        # Check student eligibility
        cur.execute("SELECT cgpa, active_backlogs, department_id FROM students WHERE student_id = ?", (student_id,))
        student = cur.fetchone()
        if student['cgpa'] < job['minimum_cgpa']:
            flash(f"Student CGPA ({student['cgpa']}) is below minimum requirement ({job['minimum_cgpa']}).", 'warning')
            return redirect(url_for('applications'))
        if student['active_backlogs'] > job['maximum_backlogs']:
            flash(f"Student backlogs ({student['active_backlogs']}) exceed maximum allowed ({job['maximum_backlogs']}).", 'warning')
            return redirect(url_for('applications'))

        # Check department eligibility
        cur.execute("SELECT 1 FROM job_eligibility_departments WHERE job_id = ? AND department_id = ?", (job_id, student['department_id']))
        if not cur.fetchone():
            flash('Student department is not eligible for this recruitment drive.', 'warning')
            return redirect(url_for('applications'))

        # Insert application - TRIGGER trg_after_application_insert will automatically execute!
        cur.execute("""
            INSERT INTO applications (student_id, job_id, application_status)
            VALUES (?, ?, 'APPLIED')
        """, (student_id, job_id))

        conn.commit()
        flash('Application submitted successfully! (Trigger trg_after_application_insert automatically logged this to Audit Logs)', 'success')
    except sqlite3.IntegrityError as ie:
        conn.rollback()
        flash('Error: This student has already applied for this job drive.', 'danger')
    except Exception as e:
        conn.rollback()
        flash(f'Error applying: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('applications'))


@app.route('/applications/update_status/<int:app_id>', methods=['POST'])
def update_application_status(app_id):
    new_status = request.form.get('application_status')
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE applications SET application_status = ?, updated_at = datetime('now', 'localtime') WHERE application_id = ?", (new_status, app_id))
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'UPDATE_APPLICATION_STATUS', 'APPLICATION', ?, ?)
        """, (1, app_id, f'Application ID {app_id} status updated to {new_status}'))
        conn.commit()
        flash(f'Application ID {app_id} updated to {new_status}.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating application: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('applications'))


@app.route('/applications/delete/<int:app_id>', methods=['POST'])
def delete_application(app_id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM placement_offers WHERE application_id = ?", (app_id,))
        cur.execute("DELETE FROM interview_rounds WHERE application_id = ?", (app_id,))
        cur.execute("DELETE FROM applications WHERE application_id = ?", (app_id,))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'DELETE_APPLICATION', 'APPLICATION', ?, ?)
        """, (1, app_id, f'Withdrawn/Deleted Application ID {app_id}'))

        conn.commit()
        flash(f'Application #{app_id} deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting application: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('applications'))


# =============================================================================
# 5. INTERVIEW ROUNDS (CRUD)
# =============================================================================

@app.route('/interviews')
def interviews():
    conn = database.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT r.round_id, r.round_number, r.round_name, r.scheduled_at, r.score, r.feedback, r.round_status,
               a.application_id, u.full_name AS student_name, s.enrollment_number,
               j.job_title, c.company_name, eval.full_name AS evaluator_name
        FROM interview_rounds r
        JOIN applications a ON r.application_id = a.application_id
        JOIN students s ON a.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN users eval ON r.evaluated_by = eval.user_id
        ORDER BY r.round_id DESC
    """)
    rounds = [dict(row) for row in cur.fetchall()]

    # Applications for scheduling rounds
    cur.execute("""
        SELECT a.application_id, u.full_name, c.company_name, j.job_title
        FROM applications a
        JOIN students s ON a.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.application_status IN ('APPLIED', 'SHORTLISTED')
        ORDER BY a.application_id DESC
    """)
    apps = [dict(row) for row in cur.fetchall()]

    # Recruiters for evaluators
    cur.execute("""
        SELECT u.user_id, u.full_name, c.company_name
        FROM recruiters r
        JOIN users u ON r.user_id = u.user_id
        JOIN companies c ON r.company_id = c.company_id
    """)
    evaluators = [dict(row) for row in cur.fetchall()]

    conn.close()
    return render_template('interviews.html', rounds=rounds, applications=apps, evaluators=evaluators)


@app.route('/interviews/create', methods=['POST'])
def create_interview():
    application_id = request.form.get('application_id')
    round_number = request.form.get('round_number')
    round_name = request.form.get('round_name', '').strip()
    scheduled_at = request.form.get('scheduled_at') or None
    evaluated_by = request.form.get('evaluated_by') or None

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO interview_rounds (application_id, round_number, round_name, scheduled_at, evaluated_by, round_status)
            VALUES (?, ?, ?, ?, ?, 'PENDING')
        """, (application_id, round_number, round_name, scheduled_at, evaluated_by))
        round_id = cur.lastrowid

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'SCHEDULE_INTERVIEW', 'INTERVIEW_ROUND', ?, ?)
        """, (evaluated_by or 1, round_id, f'Scheduled {round_name} (Round {round_number}) for Application {application_id}'))

        conn.commit()
        flash(f'Interview round scheduled successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error scheduling round: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('interviews'))


@app.route('/interviews/evaluate/<int:round_id>', methods=['POST'])
def evaluate_interview(round_id):
    score = request.form.get('score')
    feedback = request.form.get('feedback', '').strip()
    round_status = request.form.get('round_status')

    score_val = float(score) if score else None
    if score_val is not None and (score_val < 0.0 or score_val > 100.0):
        flash('Score must be between 0.00 and 100.00.', 'danger')
        return redirect(url_for('interviews'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE interview_rounds
            SET score = ?, feedback = ?, round_status = ?, updated_at = datetime('now', 'localtime')
            WHERE round_id = ?
        """, (score_val, feedback, round_status, round_id))

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'RECORD_INTERVIEW_RESULT', 'INTERVIEW_ROUND', ?, ?)
        """, (1, round_id, f'Evaluated Round {round_id}: Status={round_status}, Score={score_val}'))

        conn.commit()
        flash(f'Interview round {round_id} evaluated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error saving evaluation: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('interviews'))


@app.route('/interviews/delete/<int:round_id>', methods=['POST'])
def delete_interview(round_id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM interview_rounds WHERE round_id = ?", (round_id,))
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'DELETE_INTERVIEW_ROUND', 'INTERVIEW_ROUND', ?, ?)
        """, (1, round_id, f'Deleted interview round #{round_id}'))
        conn.commit()
        flash(f'Interview round #{round_id} removed.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting round: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('interviews'))


# =============================================================================
# 6. PLACEMENT OFFERS & TRIGGER DEMONSTRATION
# =============================================================================

@app.route('/offers')
def offers():
    conn = database.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT o.offer_id, o.offered_package_lpa, o.offer_date, o.joining_date, o.offer_status,
               a.application_id, a.application_status,
               u.full_name AS student_name, s.enrollment_number, d.department_code,
               j.job_title, c.company_name
        FROM placement_offers o
        JOIN applications a ON o.application_id = a.application_id
        JOIN students s ON a.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN departments d ON s.department_id = d.department_id
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY o.offer_id DESC
    """)
    offers_list = [dict(row) for row in cur.fetchall()]

    # Eligible applications for rolling out new offer
    cur.execute("""
        SELECT a.application_id, u.full_name, c.company_name, j.job_title, j.package_lpa
        FROM applications a
        JOIN students s ON a.student_id = s.student_id
        JOIN users u ON s.user_id = u.user_id
        JOIN job_openings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        LEFT JOIN placement_offers o ON a.application_id = o.application_id
        WHERE o.offer_id IS NULL AND a.application_status IN ('APPLIED', 'SHORTLISTED', 'SELECTED')
        ORDER BY a.application_id DESC
    """)
    eligible_apps = [dict(row) for row in cur.fetchall()]

    conn.close()
    return render_template('offers.html', offers=offers_list, applications=eligible_apps)


@app.route('/offers/create', methods=['POST'])
def create_offer():
    application_id = request.form.get('application_id')
    offered_package_lpa = request.form.get('offered_package_lpa')
    offer_date = request.form.get('offer_date') or datetime.now().strftime('%Y-%m-%d')
    joining_date = request.form.get('joining_date') or None

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO placement_offers (application_id, offered_package_lpa, offer_date, joining_date, offer_status)
            VALUES (?, ?, ?, ?, 'OFFERED')
        """, (application_id, float(offered_package_lpa), offer_date, joining_date))
        offer_id = cur.lastrowid

        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'GENERATE_OFFER', 'PLACEMENT_OFFER', ?, ?)
        """, (1, offer_id, f'Rolled out offer ID {offer_id} with package {offered_package_lpa} LPA'))

        conn.commit()
        flash('Placement offer rolled out successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error creating offer: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('offers'))


@app.route('/offers/update_status/<int:offer_id>', methods=['POST'])
def update_offer_status(offer_id):
    new_status = request.form.get('offer_status')
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        # Updating placement_offers to 'ACCEPTED' activates TRIGGER trg_after_offer_update!
        cur.execute("""
            UPDATE placement_offers 
            SET offer_status = ?, updated_at = datetime('now', 'localtime')
            WHERE offer_id = ?
        """, (new_status, offer_id))
        conn.commit()

        if new_status == 'ACCEPTED':
            flash(f'Offer ID {offer_id} marked as ACCEPTED! Database TRIGGER "trg_after_offer_update" executed: Application status automatically set to SELECTED and logged to Audit Logs!', 'success')
        else:
            flash(f'Offer ID {offer_id} status updated to {new_status}.', 'info')
    except Exception as e:
        conn.rollback()
        flash(f'Error updating offer: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('offers'))


@app.route('/offers/delete/<int:offer_id>', methods=['POST'])
def delete_offer(offer_id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM placement_offers WHERE offer_id = ?", (offer_id,))
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'DELETE_PLACEMENT_OFFER', 'PLACEMENT_OFFER', ?, ?)
        """, (1, offer_id, f'Deleted placement offer #{offer_id}'))
        conn.commit()
        flash(f'Offer #{offer_id} removed.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error removing offer: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('offers'))


# =============================================================================
# 6.1 DEPARTMENTS MANAGEMENT (CRUD)
# =============================================================================

@app.route('/departments')
def departments_view():
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.*, COUNT(s.student_id) AS student_count
        FROM departments d
        LEFT JOIN students s ON d.department_id = s.department_id
        GROUP BY d.department_id
        ORDER BY d.department_code
    """)
    depts = [dict(r) for r in cur.fetchall()]
    conn.close()
    return render_template('departments.html', departments=depts)


@app.route('/departments/create', methods=['POST'])
def create_department():
    dept_name = request.form.get('department_name', '').strip()
    dept_code = request.form.get('department_code', '').strip().upper()
    description = request.form.get('description', '').strip()

    if not dept_name or not dept_code:
        flash('Department name and code are required.', 'danger')
        return redirect(url_for('departments_view'))

    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO departments (department_name, department_code, description)
            VALUES (?, ?, ?)
        """, (dept_name, dept_code, description))
        dept_id = cur.lastrowid
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'CREATE_DEPARTMENT', 'DEPARTMENT', ?, ?)
        """, (1, dept_id, f'Added department {dept_code}: {dept_name}'))
        conn.commit()
        flash(f'Department "{dept_code}" created successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error creating department: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('departments_view'))


@app.route('/departments/delete/<int:dept_id>', methods=['POST'])
def delete_department(dept_id):
    conn = database.get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM students WHERE department_id = ?", (dept_id,))
        if cur.fetchone()[0] > 0:
            flash('Cannot delete department with active enrolled students.', 'warning')
            return redirect(url_for('departments_view'))

        cur.execute("DELETE FROM job_eligibility_departments WHERE department_id = ?", (dept_id,))
        cur.execute("DELETE FROM departments WHERE department_id = ?", (dept_id,))
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
            VALUES (?, 'DELETE_DEPARTMENT', 'DEPARTMENT', ?, ?)
        """, (1, dept_id, f'Deleted department #{dept_id}'))
        conn.commit()
        flash('Department deleted successfully.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting department: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('departments_view'))


# =============================================================================
# 6.2 ANALYTICS CHARTS API (FOR CHART.JS DASHBOARD)
# =============================================================================

@app.route('/api/analytics/charts')
def api_chart_data():
    conn = database.get_db_connection()
    cur = conn.cursor()

    # 1. Dept placement rates
    cur.execute("SELECT department_code, placement_percentage, average_package_lpa FROM v_department_placement_statistics")
    dept_rows = cur.fetchall()
    dept_labels = [r['department_code'] for r in dept_rows]
    dept_pct = [r['placement_percentage'] or 0.0 for r in dept_rows]
    dept_avg_pkg = [r['average_package_lpa'] or 0.0 for r in dept_rows]

    # 2. Status distribution
    cur.execute("""
        SELECT placement_status, COUNT(*) as count 
        FROM v_student_placement_summary 
        GROUP BY placement_status
    """)
    status_rows = cur.fetchall()
    status_dict = {r['placement_status']: r['count'] for r in status_rows}

    # 3. Top companies by package
    cur.execute("""
        SELECT c.company_name, MAX(j.package_lpa) as max_pkg
        FROM companies c
        JOIN job_openings j ON c.company_id = j.company_id
        GROUP BY c.company_name
        ORDER BY max_pkg DESC
        LIMIT 6
    """)
    comp_rows = cur.fetchall()
    comp_labels = [r['company_name'] for r in comp_rows]
    comp_packages = [r['max_pkg'] for r in comp_rows]

    conn.close()
    return jsonify({
        'departments': {'labels': dept_labels, 'percentages': dept_pct, 'avg_packages': dept_avg_pkg},
        'status_distribution': status_dict,
        'companies': {'labels': comp_labels, 'packages': comp_packages}
    })


# =============================================================================
# 7. STORED PROCEDURES & FUNCTIONS CONSOLE
# =============================================================================

@app.route('/procedures')
def procedures():
    conn = database.get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT job_id, job_title, package_lpa FROM job_openings ORDER BY job_id")
    jobs = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT department_id, department_name, department_code FROM departments ORDER BY department_name")
    departments = [dict(row) for row in cur.fetchall()]

    conn.close()
    return render_template('procedures.html', jobs=jobs, departments=departments)


@app.route('/api/procedures/eligible_students/<int:job_id>')
def api_eligible_students(job_id):
    try:
        data = database.sp_get_eligible_students(job_id)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/procedures/company_summary')
def api_company_summary():
    try:
        data = database.sp_get_company_placement_summary()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/procedures/department_report')
def api_department_report():
    grad_year = request.args.get('year')
    year_val = int(grad_year) if grad_year else None
    try:
        data = database.sp_get_department_placement_report(year_val)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/procedures/cursor_statistics')
def api_cursor_statistics():
    try:
        data = database.sp_cursor_interview_round_statistics()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/functions/overall_percentage')
def api_overall_percentage():
    try:
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT fn_calculate_overall_placement_percentage()")
        rate = cur.fetchone()[0] or 0.0
        conn.close()
        return jsonify({'success': True, 'overall_placement_percentage': rate})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# =============================================================================
# 8. INTERACTIVE SQL TERMINAL / QUERY RUNNER
# =============================================================================

@app.route('/sql')
def sql_terminal():
    return render_template('sql_terminal.html')


@app.route('/api/sql/execute', methods=['POST'])
def api_sql_execute():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'success': False, 'error': 'Query string cannot be empty.'}), 400

    result = database.execute_custom_query(query)
    return jsonify(result)


# =============================================================================
# 9. ER DIAGRAM, SCHEMA & 3NF NORMALIZATION
# =============================================================================

@app.route('/schema')
def schema():
    return render_template('schema.html')


# =============================================================================
# 10. AUDIT LOGS
# =============================================================================

@app.route('/audit')
def audit_logs():
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.*, u.full_name AS user_name
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.user_id
        ORDER BY a.audit_id DESC
    """)
    logs = [dict(row) for row in cur.fetchall()]
    conn.close()
    return render_template('audit.html', logs=logs)


# =============================================================================
# 11. DATABASE RESET
# =============================================================================

@app.route('/database/reset', methods=['POST'])
def reset_database():
    try:
        database.init_db(reset=True)
        flash('Database reset to original sample dataset successfully!', 'success')
    except Exception as e:
        flash(f'Failed to reset database: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    import socket
    # Listen on all network interfaces (0.0.0.0) so colleagues on Wi-Fi/Hotspot can access
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        local_ip = "127.0.0.1"

    print("\n" + "=" * 70)
    print("  🚀 CampusHire Web Application is LIVE!")
    print(f"  📍 Open on YOUR Laptop:         http://127.0.0.1:5000")
    print(f"  🔗 Share Link with Colleagues:   http://{local_ip}:5000")
    print("     (Colleagues can view and make real-time database changes)")
    print("=" * 70 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)

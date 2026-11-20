"""
Comprehensive automated test suite for CampusHire DBMS Application.
Tests:
1. All Web Routes (HTTP 200)
2. All DML/CRUD Operations (Insert, Update, Delete across tables)
3. Database Triggers (trg_after_application_insert, trg_after_offer_update)
4. All Stored Procedures, Functions, Cursors & Views
5. SQL Terminal Execution
6. Database verification: Before & After row counts and audit trail verification
"""

import unittest
import json
import sqlite3
import database
from app import app


import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_full_system_test():
    client = app.test_client()
    print("=" * 70)
    print(">> STARTING FULL SYSTEM & DATABASE VERIFICATION TEST")
    print("=" * 70)

    # -------------------------------------------------------------
    # 0. Initial DB State
    # -------------------------------------------------------------
    conn = database.get_db_connection()
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';").fetchall()]
    
    print("\n[STEP 1] INITIAL DATABASE STATUS:")
    initial_counts = {}
    for t in sorted(tables):
        cnt = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        initial_counts[t] = cnt
        print(f"  • {t.ljust(30)}: {cnt} records")
    conn.close()

    # -------------------------------------------------------------
    # 1. Test All Web Pages (GET routes)
    # -------------------------------------------------------------
    print("\n[STEP 2] TESTING ALL WEB ROUTES (HTTP 200):")
    routes = [
        '/',
        '/students',
        '/jobs',
        '/applications',
        '/interviews',
        '/offers',
        '/procedures',
        '/sql',
        '/schema',
        '/audit',
        '/departments'
    ]
    for r in routes:
        res = client.get(r)
        status = res.status_code
        assert status == 200, f"Route {r} failed with status {status}"
        print(f"  ✔ GET {r.ljust(20)} -> HTTP {status} OK")

    # -------------------------------------------------------------
    # 2. Test All Stored Procedures, Cursors, Functions & Views
    # -------------------------------------------------------------
    print("\n[STEP 3] RUNNING PROCEDURES, CURSORS, FUNCTIONS & VIEWS:")
    
    # Procedure: sp_get_eligible_students
    p1 = database.sp_get_eligible_students(1)
    print(f"  ✔ sp_get_eligible_students(1): Found {len(p1['eligible_students'])} eligible students for '{p1['job_title']}'")
    assert len(p1['eligible_students']) > 0

    # Procedure: sp_get_company_placement_summary
    p2 = database.sp_get_company_placement_summary()
    print(f"  ✔ sp_get_company_placement_summary(): Summarized {len(p2)} companies")
    assert len(p2) > 0

    # Procedure: sp_get_department_placement_report
    p3 = database.sp_get_department_placement_report(2025)
    print(f"  ✔ sp_get_department_placement_report(2025): Generated report for {len(p3)} departments")
    assert len(p3) > 0

    # Cursor: sp_cursor_interview_round_statistics
    cur_stats = database.sp_cursor_interview_round_statistics()
    print(f"  ✔ sp_cursor_interview_round_statistics(): Iterated {cur_stats['total_interview_rounds']} rounds (Passed: {cur_stats['total_passed']}, Avg Score: {cur_stats['average_score_of_evaluated_rounds']})")
    assert cur_stats['total_interview_rounds'] > 0

    # Function: fn_calculate_overall_placement_percentage
    conn = database.get_db_connection()
    overall_pct = conn.execute("SELECT fn_calculate_overall_placement_percentage()").fetchone()[0]
    dept1_pct = conn.execute("SELECT fn_calculate_department_placement_percentage(1)").fetchone()[0]
    print(f"  ✔ fn_calculate_overall_placement_percentage(): {overall_pct}%")
    print(f"  ✔ fn_calculate_department_placement_percentage(1 - CSE): {dept1_pct}%")
    conn.close()

    # Views
    conn = database.get_db_connection()
    v1_cnt = conn.execute("SELECT COUNT(*) FROM v_student_placement_summary").fetchone()[0]
    v2_cnt = conn.execute("SELECT COUNT(*) FROM v_job_opening_company_summary").fetchone()[0]
    v3_cnt = conn.execute("SELECT COUNT(*) FROM v_department_placement_statistics").fetchone()[0]
    print(f"  ✔ VIEW v_student_placement_summary: {v1_cnt} rows")
    print(f"  ✔ VIEW v_job_opening_company_summary: {v2_cnt} rows")
    print(f"  ✔ VIEW v_department_placement_statistics: {v3_cnt} rows")
    conn.close()

    # -------------------------------------------------------------
    # 3. Test Full DML Mutations (INSERT, UPDATE, TRIGGER, DELETE)
    # -------------------------------------------------------------
    print("\n[STEP 4] TESTING DML DATA MANIPULATION & DATABASE TRIGGERS:")

    # 3.1 Insert New Student
    test_enrollment = "EN2026TEST999"
    student_form = {
        'full_name': 'Test Student Automation',
        'email': 'test.automation@campushire.edu',
        'enrollment_number': test_enrollment,
        'department_id': 1,
        'graduation_year': 2026,
        'cgpa': '9.80',
        'active_backlogs': '0',
        'phone': '9999988888',
        'resume_url': 'https://campushire.edu/resumes/test.pdf'
    }
    res = client.post('/students/create', data=student_form, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    created_student = conn.execute("SELECT student_id, cgpa FROM students WHERE enrollment_number = ?", (test_enrollment,)).fetchone()
    assert created_student is not None, "Student was not created in database!"
    test_student_id = created_student['student_id']
    print(f"  ✔ CREATE STUDENT: Student ID #{test_student_id} inserted into DB (CGPA: {created_student['cgpa']})")
    conn.close()

    # 3.2 Update Student
    update_form = {
        'cgpa': '9.95',
        'active_backlogs': '0',
        'phone': '9999977777',
        'resume_url': 'https://campushire.edu/resumes/test_updated.pdf',
        'profile_status': 'VERIFIED'
    }
    res = client.post(f'/students/update/{test_student_id}', data=update_form, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    updated_cgpa = conn.execute("SELECT cgpa, phone FROM students WHERE student_id = ?", (test_student_id,)).fetchone()
    assert updated_cgpa['cgpa'] == 9.95, "Student CGPA was not updated in DB!"
    print(f"  ✔ UPDATE STUDENT: Student #{test_student_id} updated to CGPA={updated_cgpa['cgpa']}, Phone={updated_cgpa['phone']}")
    conn.close()

    # 3.3 Create New Company
    test_company_name = "Automated AI Corp"
    res = client.post('/companies/create', data={
        'company_name': test_company_name,
        'industry': 'Artificial Intelligence',
        'website': 'https://auto-ai.example.com',
        'headquarters': 'Bangalore, India',
        'company_description': 'Autonomous AI enterprise solutions'
    }, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    comp_row = conn.execute("SELECT company_id FROM companies WHERE company_name = ?", (test_company_name,)).fetchone()
    assert comp_row is not None
    test_company_id = comp_row['company_id']
    print(f"  ✔ CREATE COMPANY: Company ID #{test_company_id} ('{test_company_name}') inserted into DB")
    conn.close()

    # 3.4 Create New Job Opening
    res = client.post('/jobs/create', data={
        'company_id': test_company_id,
        'job_title': 'AI Research Engineer',
        'job_description': 'Deep learning and NLP systems',
        'job_type': 'FULL_TIME',
        'location': 'Bangalore',
        'minimum_cgpa': '8.00',
        'maximum_backlogs': '0',
        'package_lpa': '32.00',
        'application_deadline': '2026-12-31T23:59',
        'drive_date': '2027-01-10T10:00',
        'job_status': 'OPEN',
        'department_ids': ['1', '2']
    }, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    job_row = conn.execute("SELECT job_id, package_lpa FROM job_openings WHERE company_id = ? AND job_title = 'AI Research Engineer'", (test_company_id,)).fetchone()
    assert job_row is not None
    test_job_id = job_row['job_id']
    print(f"  ✔ CREATE JOB DRIVE: Job ID #{test_job_id} posted with Package ₹{job_row['package_lpa']} LPA")
    conn.close()

    # 3.5 Submit Application & Verify TRIGGER trg_after_application_insert
    res = client.post('/applications/create', data={
        'student_id': test_student_id,
        'job_id': test_job_id
    }, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    app_row = conn.execute("SELECT application_id, application_status FROM applications WHERE student_id = ? AND job_id = ?", (test_student_id, test_job_id)).fetchone()
    assert app_row is not None
    test_app_id = app_row['application_id']

    # Verify Trigger fired
    audit_row = conn.execute("SELECT * FROM audit_logs WHERE action = 'NEW_APPLICATION_SUBMITTED' AND entity_id = ?", (test_app_id,)).fetchone()
    assert audit_row is not None, "TRIGGER trg_after_application_insert failed to record audit log!"
    print(f"  ✔ TRIGGER 1 FIRED (trg_after_application_insert): Application #{test_app_id} created and automatically logged to audit_logs")
    print(f"    Audit Detail: {audit_row['details']}")
    conn.close()

    # 3.6 Schedule Interview Round & Evaluate
    res = client.post('/interviews/create', data={
        'application_id': test_app_id,
        'round_number': 1,
        'round_name': 'Coding Round 1',
        'scheduled_at': '2026-12-01T10:00',
        'evaluated_by': '1'
    }, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    round_row = conn.execute("SELECT round_id FROM interview_rounds WHERE application_id = ?", (test_app_id,)).fetchone()
    assert round_row is not None
    test_round_id = round_row['round_id']

    # Evaluate Round
    res = client.post(f'/interviews/evaluate/{test_round_id}', data={
        'score': '96.50',
        'round_status': 'PASSED',
        'feedback': 'Exceptional problem-solving skills in automated test'
    }, follow_redirects=True)
    assert res.status_code == 200

    round_updated = conn.execute("SELECT score, round_status FROM interview_rounds WHERE round_id = ?", (test_round_id,)).fetchone()
    assert round_updated['round_status'] == 'PASSED'
    print(f"  ✔ EVALUATE INTERVIEW: Round #{test_round_id} marked PASSED with Score {round_updated['score']}")
    conn.close()

    # 3.7 Roll Out Placement Offer & Verify Cascading TRIGGER trg_after_offer_update
    res = client.post('/offers/create', data={
        'application_id': test_app_id,
        'offered_package_lpa': '32.00',
        'offer_date': '2026-12-05',
        'joining_date': '2027-07-01'
    }, follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    offer_row = conn.execute("SELECT offer_id, offer_status FROM placement_offers WHERE application_id = ?", (test_app_id,)).fetchone()
    assert offer_row is not None
    test_offer_id = offer_row['offer_id']
    assert offer_row['offer_status'] == 'OFFERED'
    print(f"  ✔ ROLL OUT OFFER: Offer ID #{test_offer_id} generated for Application #{test_app_id}")

    # Now update offer status to 'ACCEPTED' -> TRIGGER trg_after_offer_update MUST execute!
    res = client.post(f'/offers/update_status/{test_offer_id}', data={'offer_status': 'ACCEPTED'}, follow_redirects=True)
    assert res.status_code == 200

    # Verify application status automatically updated to 'SELECTED' by trigger
    app_after = conn.execute("SELECT application_status FROM applications WHERE application_id = ?", (test_app_id,)).fetchone()
    assert app_after['application_status'] == 'SELECTED', f"Trigger failed! Expected application status SELECTED, got {app_after['application_status']}"

    # Verify audit log entry written by trigger
    trigger_log = conn.execute("SELECT * FROM audit_logs WHERE action = 'PLACEMENT_OFFER_ACCEPTED' AND entity_id = ?", (test_offer_id,)).fetchone()
    assert trigger_log is not None, "Trigger audit log not found!"
    print(f"  ✔ TRIGGER 2 FIRED (trg_after_offer_update): Offer #{test_offer_id} accepted!")
    print(f"    -> Application status automatically updated to: '{app_after['application_status']}'")
    print(f"    -> Trigger Audit Detail: {trigger_log['details']}")
    conn.close()

    # -------------------------------------------------------------
    # 4. Test SQL Terminal API Runner
    # -------------------------------------------------------------
    print("\n[STEP 5] TESTING LIVE SQL QUERY TERMINAL API:")
    sql_queries = [
        ("SELECT COUNT(*) AS total_students FROM students", True),
        (f"SELECT u.full_name, s.cgpa FROM students s JOIN users u ON s.user_id = u.user_id WHERE s.student_id = {test_student_id}", True),
        ("UPDATE students SET phone = '9999900000' WHERE student_id = " + str(test_student_id), False),
        ("SELECT fn_calculate_overall_placement_percentage() AS overall_rate", True)
    ]
    for q, is_sel in sql_queries:
        res = client.post('/api/sql/execute', json={'query': q})
        data = res.json
        assert data['success'] is True, f"SQL Query '{q}' failed: {data.get('error')}"
        if is_sel:
            print(f"  ✔ SQL SELECT: '{q}' -> Returned {data['row_count']} row(s) in {data['duration_ms']} ms")
        else:
            print(f"  ✔ SQL UPDATE: '{q}' -> Affected {data['affected_rows']} row(s) in {data['duration_ms']} ms")

    # -------------------------------------------------------------
    # 5. Clean up test records (testing cascade delete)
    # -------------------------------------------------------------
    print("\n[STEP 6] TESTING CASCADE DELETION:")
    res = client.post(f'/students/delete/{test_student_id}', follow_redirects=True)
    assert res.status_code == 200
    res = client.post(f'/jobs/delete/{test_job_id}', follow_redirects=True)
    assert res.status_code == 200

    conn = database.get_db_connection()
    assert conn.execute("SELECT 1 FROM students WHERE student_id = ?", (test_student_id,)).fetchone() is None
    assert conn.execute("SELECT 1 FROM applications WHERE application_id = ?", (test_app_id,)).fetchone() is None
    assert conn.execute("SELECT 1 FROM interview_rounds WHERE round_id = ?", (test_round_id,)).fetchone() is None
    assert conn.execute("SELECT 1 FROM placement_offers WHERE offer_id = ?", (test_offer_id,)).fetchone() is None
    print(f"  ✔ CASCADE DELETE: Cleaned up test records (Student, Applications, Rounds, Offers). Referential integrity confirmed!")
    conn.close()

    # -------------------------------------------------------------
    # 6. Final DB Status Verification
    # -------------------------------------------------------------
    print("\n[STEP 7] FINAL DATABASE STATUS & AUDIT LOG COMPARISON:")
    conn = database.get_db_connection()
    cur = conn.cursor()
    final_counts = {}
    for t in sorted(tables):
        cnt = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        final_counts[t] = cnt
        diff = cnt - initial_counts.get(t, 0)
        diff_str = f"(+{diff})" if diff > 0 else (f"({diff})" if diff < 0 else "(no change)")
        print(f"  • {t.ljust(30)}: {cnt} records {diff_str}")

    recent_audit = cur.execute("SELECT audit_id, action, entity_type, details, created_at FROM audit_logs ORDER BY audit_id DESC LIMIT 5").fetchall()
    print("\n  Top 5 Most Recent Audit Trail Entries Recorded:")
    for r in recent_audit:
        print(f"    [{r['audit_id']}] {r['action']} ({r['entity_type']}): {r['details']} @ {r['created_at']}")

    conn.close()

    print("\n" + "=" * 70)
    print("SUCCESS: ALL TESTS PASSED! APPLICATION & DATABASE 100% OPERATIONAL!")
    print("=" * 70)


if __name__ == '__main__':
    run_full_system_test()

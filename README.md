# CampusHire — College Placement & Recruitment Management System
### DBMS Mini Project (5th Semester) — Full-Stack Working Website

---

## 📌 Project Overview & Syllabus Mapping

This project fulfills all requirements outlined in the **DBMS Mini Project Syllabus** (Option 1):

| Syllabus Requirement | Implementation in CampusHire |
|---|---|
| **Real-World Domain** | College Placement and Campus Recruitment Management System |
| **ER Design** | 11 Normalized Entities connected via 1:1, 1:M, and M:N relationships |
| **Relational Schema with Constraints** | Primary Keys (PK), Foreign Keys (FK) with `ON DELETE RESTRICT/CASCADE`, `UNIQUE`, `CHECK` constraints (CGPA 0–10, score 0–100, backlogs &ge; 0) |
| **Normalization (at least till 3NF)** | Strictly normalized to **3NF** (eliminated repeating groups, partial dependencies, and transitive dependencies) |
| **DML Operations (CRUD)** | Complete interactive website allowing users to **INSERT, UPDATE, DELETE, and SELECT** records across all entities |
| **PL/SQL Procedures** | `sp_get_eligible_students`, `sp_get_company_placement_summary`, `sp_get_department_placement_report` |
| **PL/SQL Cursors** | `sp_cursor_interview_round_statistics` (declares cursor, loops row-by-row with `NOT FOUND` handler) |
| **PL/SQL Functions** | `fn_calculate_overall_placement_percentage`, `fn_calculate_department_placement_percentage` |
| **PL/SQL Triggers** | `trg_after_application_insert`, `trg_after_offer_update`, `trg_before_application_insert_check` |
| **SQL Views** | `v_student_placement_summary`, `v_job_opening_company_summary`, `v_department_placement_statistics` |

---

## 🚀 How to Run the Website

### Option A: 1-Click Launch (Recommended for Windows)
Simply double-click the file:
```
run_website.bat
```
This starts the web server and automatically opens **`http://127.0.0.1:5000`** in your default web browser!

### Option B: Terminal Command
```bash
# Navigate to this folder
cd "c:\Nikhil\5th Sem\DEL\Mini Project"

# Run Flask application
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 👥 How to Share with Colleagues in Real-Time

You have two instant, free methods to share the website with your group members or teacher so they can interact and manipulate database records in real-time:

### Method 1: Local Network / Wi-Fi Sharing (Same College Wi-Fi / Hotspot)
1. Make sure your laptop and your colleagues' laptops/phones are connected to the **same Wi-Fi** or **Mobile Hotspot**.
2. Run `run_website.bat` or `python app.py`.
3. In the black console window, look for the line:
   ```
   🔗 Share Link with Colleagues: http://<Your-IP>:5000  (e.g., http://10.166.149.221:5000)
   ```
4. Copy that URL and send it to your friends.
5. They can open it in Chrome/Safari on their phone or laptop. Any student they add, job they post, or offer they accept will update the database in **real-time** on everyone's screens!

### Method 2: Public Internet Link (If Colleagues are at Home / Remote)
1. Keep `run_website.bat` open and running.
2. Double-click [`share_online_public_link.bat`](file:///c:/Nikhil/5th%20Sem/DEL/Mini%20Project/share_online_public_link.bat).
3. It will generate a secure public URL (e.g. `https://xxxx.loca.lt`).
4. Share that link with your friends or teacher anywhere in the world! They can perform full DML operations live.

---

## 🌐 Website Features & Data Manipulation Modules

### 1. 📊 Placement Analytics Dashboard (`/`)
- Summary cards: Overall Placement %, Placed Students Count, Highest Package (LPA), Average Package (LPA).
- **Interactive Chart.js Visualizations**:
  - Live **Department Placement Rate (%) & Average Package (₹ LPA)** dual-axis bar chart.
  - Live **Placement Distribution Doughnut Chart** (Placed vs Offer Received vs Unplaced).
- Department placement breakdown using SQL View `v_department_placement_statistics`.
- Active recruitment drives using SQL View `v_job_opening_company_summary`.
- Recent offers and live audit log stream.

### 2. 🎓 Students Management (`/students`)
- **CREATE**: Add new student with full validation (CGPA, backlogs, department, unique enrollment number).
- **READ**: Search by name or enrollment number; filter by department and placement status (`PLACED`, `OFFER_RECEIVED`, `UNPLACED`).
- **UPDATE**: Edit student CGPA, active backlogs, phone number, resume link, and profile verification status (pre-populated dynamically).
- **DELETE**: Remove student record (with cascade checks and audit log entry).
- **DOSSIER**: 1-click modal viewing all job applications, interview round results, and rolled-out offers.
- **EXPORT CSV**: 1-click export of the student dataset into a formatted `.csv` file.

### 3. 🏢 Companies & Job Openings (`/jobs`)
- **CREATE**: Register partner recruiting companies and publish new campus placement drives.
- **EDIT**: Full modal to edit job title, package LPA, requirements, deadline, and drive status.
- **DELETE**: Delete recruitment drives with cascade checks.
- **ELIGIBILITY MAPPING**: Map M:N relationship of job drives to eligible branches (`job_eligibility_departments`).
- **UPDATE STATUS**: Instantly change drive status (`OPEN`, `CLOSED`, `DRAFT`, `CANCELLED`).

### 4. 🏫 Departments Management (`/departments`)
- Complete data manipulation for academic departments (add new branch, view student count, delete unused branches).

### 4. 📝 Applications Pipeline (`/applications`)
- **APPLY**: Submit candidate applications to open drives.
- **CONSTRAINT CHECK**: Enforces minimum CGPA, maximum backlogs, and branch eligibility before submission.
- **TRIGGER**: Submitting an application fires `trg_after_application_insert` which records a security entry into `audit_logs`.
- **UPDATE STATUS**: Progress applicants through stages (`APPLIED`, `SHORTLISTED`, `REJECTED`, `SELECTED`, `WITHDRAWN`).

### 5. 🗣️ Interview Rounds & Evaluations (`/interviews`)
- **SCHEDULE**: Schedule assessment rounds (Coding, Technical, HR).
- **EVALUATE**: Enter recruiter score (0–100), detailed feedback, and pass/fail status.
- Connects directly to the PL/SQL cursor `sp_cursor_interview_round_statistics`.

### 6. 🏆 Placement Offers & Cascading Triggers (`/offers`)
- **ROLL OUT**: Issue formal placement offers with package in LPA, offer date, and joining date.
- **TRIGGER DEMONSTRATION**: Updating offer status to **`ACCEPTED`** immediately invokes `trg_after_offer_update`, which:
  1. Automatically updates the linked application status to **`SELECTED`**.
  2. Creates an audit trail log in `audit_logs`.

### 7. ⚙️ Stored Procedures & Cursors Console (`/procedures`)
- 1-Click execution interface with real-time tabular output:
  - `CALL sp_get_eligible_students(job_id)`
  - `CALL sp_get_company_placement_summary()`
  - `CALL sp_get_department_placement_report(grad_year)`
  - `CALL sp_cursor_interview_round_statistics()`
  - `SELECT fn_calculate_overall_placement_percentage()`

### 8. 💻 Live SQL Query Terminal (`/sql`)
- Interactive web-based SQL query editor.
- Type and run ANY SQL command (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN`, `GROUP BY`).
- Includes preset query buttons, query execution timer (ms), and affected row counter.

### 9. 📐 ER Diagram & 3NF Schema Documentation (`/schema`)
- Interactive Mermaid ER diagram showing all 11 entities, relationships, and cardinalities.
- Formal academic proof of **1NF**, **2NF**, and **3NF** normalization.
- Table of primary keys, foreign keys, candidate keys, and check constraints.

### 10. ⚡ Audit Logs Explorer (`/audit`)
- Complete immutable log of database actions and trigger executions.

---

## 🗄️ Database Architecture (3NF Normalized)

### The 11 Tables:
1. `users` — Base user credentials, roles (`ADMIN`, `STUDENT`, `RECRUITER`), and account statuses.
2. `departments` — Academic branches (`CSE`, `IT`, `ECE`, `MECH`).
3. `students` — Extends `users` (1:1), enrollment number (UNIQUE), CGPA, backlogs, department (FK).
4. `companies` — Corporate recruiters, industries, websites, headquarters.
5. `recruiters` — Extends `users` (1:1), associated company (FK).
6. `job_openings` — Campus drives, salary packages, eligibility thresholds, deadlines.
7. `job_eligibility_departments` — Associative table resolving M:N relationship between drives and departments.
8. `applications` — Tracks student applications to jobs (`UNIQUE(student_id, job_id)`).
9. `interview_rounds` — Multi-stage evaluations (`round_number`, `score`, `round_status`).
10. `placement_offers` — Formal job offers (`offered_package_lpa`, `offer_status`).
11. `audit_logs` — Trigger-generated audit trail of all critical database operations.

---

## 🎓 Viva Questions & Answers for Examination

**Q1: Why is this schema in 3NF?**  
*A:*
- **1NF**: All column values are atomic (indivisible scalars). Repeating groups (like eligible departments) are moved to a separate associative table (`job_eligibility_departments`).
- **2NF**: No partial dependency exists. In composite keys, non-prime attributes depend on the entire key.
- **3NF**: No transitive dependencies ($X \to Y \to Z$). For example, company attributes (`industry`, `headquarters`) are not stored in `job_openings`; only `company_id` is referenced.

**Q2: What is the purpose of the Trigger `trg_after_offer_update`?**  
*A:* When an offer's status changes to `'ACCEPTED'`, the trigger automatically updates the linked candidate's application status to `'SELECTED'` and records an event in `audit_logs`, guaranteeing data consistency without manual intervention.

**Q3: How does the Cursor `cur_rounds` work?**  
*A:* It fetches round records row-by-row using `FETCH cur_rounds INTO ...`, tracks counts for PASSED, FAILED, PENDING, and accumulates scores to compute the average evaluated score.

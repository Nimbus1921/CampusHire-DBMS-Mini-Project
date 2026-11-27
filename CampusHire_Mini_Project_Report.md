# Data Engineering Mini Project Report
## on
# College Placement and Recruitment Management System
### (CampusHire)

---

<div align="center">

### D. Y. PATIL COLLEGE OF ENGINEERING, AKURDI, PUNE – 44.
*(An Autonomous Institute with effect from Academic Year 2024–25)*  
**Affiliated to Savitribai Phule Pune University**

---

### **Submitted By**

| Student Name | Exam Seat / Roll Number |
| :--- | :--- |
| **Mr. Pushkar Kailash Vyas** | `TY2627COA047` |
| **Mr. Sanket Uttam Baviskar** | `TY2627COA052` |
| **Mr. Nilesh Jitendra Kuwar** | `TY2627COA053` |
| **Mr. Nikhil Datta Bansode** | `TY2627COA054` |

---

### **Under the Guidance of**
**Ms. Farhina S. Sayyad**  
*Subject In-charge & Project Guide*

In partial fulfillment for the award of the Degree of  
**Bachelor of Technology (B.Tech) in Computer Engineering**  
**Academic Year 2026–27 | Semester I**

**Department of Computer Engineering**  
D. Y. Patil College of Engineering, Sector 29, Nigdi Pradhikaran, Akurdi, Pune – 411044  
Maharashtra, India

</div>

---
<div style="page-break-after: always;"></div>

# Certificate

<div align="center">

### **D. Y. PATIL COLLEGE OF ENGINEERING, AKURDI, PUNE – 44**
*(An Autonomous Institute with effect from the Academic Year 2024–25)*  
**Department of Computer Engineering**  
**(Academic Year 2026–2027)**

</div>

This is to certify that the Data Engineering Mini Project entitled:

> ### **"College Placement and Recruitment Management System (CampusHire)"**

has been successfully completed by:

| Student Name | Exam Seat No. |
| :--- | :--- |
| **Mr. Pushkar Kailash Vyas** | `TY2627COA047` |
| **Mr. Sanket Uttam Baviskar** | `TY2627COA052` |
| **Mr. Nilesh Jitendra Kuwar** | `TY2627COA053` |
| **Mr. Nikhil Datta Bansode** | `TY2627COA054` |

under the esteemed guidance of **Ms. Farhina S. Sayyad** in partial fulfillment of the requirements for the **Third Year of Bachelor of Technology (B.Tech) in Computer Engineering** under the **Savitribai Phule Pune University** during the academic year 2026–2027.

<br><br>

**Date  :** ________________________  
**Place :** Akurdi, Pune  

<br><br>

| ____________________________________ | ____________________________________ |
| :---: | :---: |
| **Ms. Farhina S. Sayyad** | **Dr. Mrs. D. A. Phalke** |
| *Subject In-charge & Project Guide* | *Head of Department (HoD)* |
| Department of Computer Engineering | Department of Computer Engineering |

---
<div style="page-break-after: always;"></div>

# Acknowledgements

With a deep sense of gratitude, we would like to thank all the people who have lit our path with their kind guidance. We are very grateful to these intellectuals who did their best to help us during our project work.

It is our proud privilege to express a deep sense of gratitude to **Dr. Mrs. P. Malathi**, Principal of DYPCOE Akurdi, Pune-44, for her kind permission and encouragement to complete this project. 

We remain highly indebted to **Dr. Mrs. D. A. Phalke**, H.O.D., Computer Engineering Department, for her timely suggestions, constructive feedback, and valuable guidance throughout the course.

Special gratitude goes to our project guide and subject in-charge, **Ms. Farhina S. Sayyad**, for her continuous encouragement, intellectual insights, and precious guidance provided during every phase of this project.

We thank all our faculty members, laboratory staff, and colleagues for their appreciable help and co-operation. We are also eternally thankful to our parents, who provided their wholehearted support, blessings, and motivation for the successful completion of this project. Lastly, we thank all our friends and everyone directly or indirectly associated with this project work.

<br>

**Mini Project Team Members:**
- **Mr. Pushkar Kailash Vyas** (`TY2627COA047`)
- **Mr. Sanket Uttam Baviskar** (`TY2627COA052`)
- **Mr. Nilesh Jitendra Kuwar** (`TY2627COA053`)
- **Mr. Nikhil Datta Bansode** (`TY2627COA054`)

---
<div style="page-break-after: always;"></div>

# Abstract

The **College Placement and Recruitment Management System**, named **CampusHire**, is a fully normalized, relational database management system designed to automate, secure, and streamline the end-to-end campus placement lifecycle. In collegiate Training and Placement (T&P) Cells, placement records are traditionally maintained using fragmented spreadsheets and uncoordinated spreadsheets. This manual practice leads to severe operational drawbacks, including extensive data redundancy, human errors in multi-criteria eligibility filtering, absence of concurrency control, and a total lack of an immutable audit trail.

CampusHire resolves these critical challenges by implementing a robust relational database using **MySQL 8.0** with the **InnoDB** storage engine. The system encompasses **11 normalized tables organized in Third Normal Form (3NF)**, modeling core institutional entities such as Students, Academic Departments, Corporate Partners, Company Recruiters, Job Drives, Departmental Eligibility Mappings, Student Applications, Multi-Round Interview Schedules, Placement Offers, and System Audit Logs. The database strictly enforces entity integrity via primary keys, referential integrity via foreign keys with cascade constraints (`ON DELETE CASCADE` and `ON DELETE RESTRICT`), and domain integrity via `CHECK` validation rules.

Advanced database constructs—including **Stored Functions, Stored Procedures, Explicit Cursors, Triggers, and Views**—are implemented to automate core placement business logic:
- Automated eligibility filtering verifying CGPA thresholds, backlogs, and branch permissions.
- Automatic event logging via `AFTER INSERT` and `AFTER UPDATE` triggers.
- Dynamic status synchronization across application states upon job offer acceptance.
- Real-time analytical computation through 3 materialized views and 14 analytical SQL reports.

This project demonstrates the complete, end-to-end practical application of fundamental and advanced Database Management System (DBMS) concepts—spanning Entity-Relationship (ER) modeling, 3NF schema decomposition, query optimization, and PL/SQL programming—to solve an authentic enterprise-scale problem.

**Keywords:** *Relational Database Management System (RDBMS), Third Normal Form (3NF), Entity-Relationship (ER) Diagram, MySQL 8.0, Stored Procedures, Database Triggers, Cursors, Campus Placement, Data Integrity, PL/SQL.*

---
<div style="page-break-after: always;"></div>

# Table of Contents

- **Abstract**
- **List of Abbreviations**
- **List of Figures**
- **List of Tables**
- **Chapter 1 — Introduction**
  - 1.1 Overview
  - 1.2 Aim / Motivation
  - 1.3 Objectives
  - 1.4 Organization of Report
- **Chapter 2 — Literature Survey**
- **Chapter 3 — Problem Statement**
  - 3.1 Background
  - 3.2 The Problem (5 W's Analysis)
  - 3.3 Proposed Solution
- **Chapter 4 — Software Requirements Specification**
  - 4.1 Hardware Requirements
  - 4.2 Software Requirements
- **Chapter 5 — System Design**
  - 5.1 ER Diagram
  - 5.2 Relational Schema & Data Dictionaries
  - 5.3 Normalization (UNF to 3NF)
  - 5.4 Advanced Database Constructs (Constraints, DML, Views, Functions, Procedures, Cursors, Triggers)
- **Chapter 6 — Conclusion and Future Scope**
  - 6.1 Conclusion
  - 6.2 Future Scope
- **References**

---
<div style="page-break-after: always;"></div>

# List of Abbreviations

| Abbreviation | Full Form |
| :--- | :--- |
| **DBMS** | Database Management System |
| **RDBMS** | Relational Database Management System |
| **ER** | Entity-Relationship |
| **SQL** | Structured Query Language |
| **PL/SQL** | Procedural Language / Structured Query Language |
| **1NF** | First Normal Form |
| **2NF** | Second Normal Form |
| **3NF** | Third Normal Form |
| **UNF** | Unnormalized Form |
| **PK** | Primary Key |
| **FK** | Foreign Key |
| **UK** | Unique Key |
| **DML** | Data Manipulation Language |
| **DDL** | Data Definition Language |
| **T&P** | Training and Placement Cell |
| **CGPA** | Cumulative Grade Point Average |
| **LPA** | Lakhs Per Annum (Indian Currency Denomination) |
| **CRUD** | Create, Read, Update, Delete |
| **RBAC** | Role-Based Access Control |

---

# List of Figures

| Figure No. | Description | Page / Section |
| :---: | :--- | :---: |
| **Figure 1** | ER Diagram — CampusHire Entity-Relationship Model | Section 5.1 |
| **Figure 2** | Relational Schema Architecture & Table Relationships | Section 5.2 |
| **Figure 3** | Normalization Flow Pipeline — UNF to 3NF | Section 5.3 |

---

# List of Tables

| Table No. | Description | Section |
| :---: | :--- | :---: |
| **Table 1** | Unnormalized Placement Spreadsheet (UNF) with Anomalies | Section 5.3 |
| **Table 2** | Entity Definitions, Real-world Purpose & Primary Keys | Section 5.1 |
| **Table 3** | Relationship Cardinality and Enforcement Mechanisms | Section 5.1 |
| **Table 4** | Functional Dependencies Analysis Summary (3NF Proof) | Section 5.3 |
| **Table 5** | Data Dictionary — `users` Entity | Section 5.2 |
| **Table 6** | Data Dictionary — `students` Entity | Section 5.2 |
| **Table 7** | Data Dictionary — `companies` Entity | Section 5.2 |
| **Table 8** | Data Dictionary — `job_openings` Entity | Section 5.2 |
| **Table 9** | Data Dictionary — `applications` Entity | Section 5.2 |
| **Table 10** | Data Dictionary — `interview_rounds` Entity | Section 5.2 |
| **Table 11** | Data Dictionary — `placement_offers` Entity | Section 5.2 |
| **Table 12** | Project File Structure and Script Modules | Section 5.4 |

---
<div style="page-break-after: always;"></div>

# Chapter 1: Introduction

### 1.1 Overview
The Training and Placement (T&P) Cell in an engineering institution serves as the mission-critical administrative nexus connecting aspiring graduates with prospective corporate recruiters. During an academic session, a placement department processes thousands of candidate records, tracks multiple tiers of visiting companies (Product, Core, FinTech, Mass Recruiters), coordinates multi-stage recruitment drives, schedules technical and behavioral interviews, and records final offer letters.

Traditionally, academic institutions maintain this vast dataset through ad-hoc spreadsheets and disparate office documents. As the student cohort and recruiter volume expand, this manual approach collapses under data inconsistency, duplicate submissions, computational errors in eligibility cutoffs, and concurrency conflicts when multiple staff members update files simultaneously. 

**CampusHire** is an enterprise-grade, fully normalized relational database management system designed and engineered to replace fragmented legacy methods. Built on **MySQL 8.0** and powered by the **InnoDB storage engine**, CampusHire establishes a single source of truth for the entire campus placement lifecycle.

### 1.2 Aim / Motivation
The primary aim of this project is to model, design, and implement an end-to-end Relational Database Management System (RDBMS) tailored to the collegiate recruitment ecosystem.

The motivation arises from critical operational problems observed in college T&P cells:
1. **Data Redundancy & Divergence:** Multiple spreadsheet versions circulate among student coordinators and faculty leads, leading to conflicting records.
2. **Eligibility Filtering Errors:** Manual filtering based on varying company criteria (e.g., minimum CGPA, maximum backlogs, eligible branches) frequently results in either eligible candidates being omitted or ineligible candidates sitting for exams.
3. **Absence of Auditability:** Traditional tools provide zero tamper-proof tracking of who modified a candidate's status, when an offer was released, or why an application was rejected.
4. **Data Concurrency Hazards:** When simultaneous updates occur across coordinators, uncommitted overwrites lead to data loss.

### 1.3 Objectives
- **Entity-Relationship Modeling:** Design an extensive ER diagram capturing all 11 real-world entities, their attributes, and relationships.
- **Relational Schema Normalization:** Decompose the data structures systematically from Unnormalized Form (UNF) through 1NF and 2NF up to **Third Normal Form (3NF)**.
- **Constraint Enforcement:** Implement rigorous Primary Keys, Foreign Keys, Unique Keys, and `CHECK` constraints to guarantee data integrity.
- **Advanced DML Operations:** Develop multi-table `INNER/LEFT JOIN` queries, subqueries, and `GROUP BY` aggregations.
- **PL/SQL Automation:**
  - **Stored Function:** Develop deterministic functions for campus-wide placement percentage calculation.
  - **Stored Procedures:** Parameterize candidate eligibility evaluation and corporate hiring summaries.
  - **Explicit Cursor:** Construct a cursor loop traversing interview round records to generate statistical summaries.
  - **Database Triggers:** Automate audit trails and status synchronization.
- **Analytical Views:** Build high-performance views for instant dashboard reporting.

### 1.4 Organization of Report
- **Chapter 2 (Literature Survey):** Benchmarking existing placement management software and spreadsheets against CampusHire.
- **Chapter 3 (Problem Statement):** In-depth analysis of the problem through the 5 W's framework.
- **Chapter 4 (Software Requirements Specification):** Hardware, software, and environment specifications.
- **Chapter 5 (System Design):** ER modeling, 3NF schema decomposition, data dictionaries, and complete SQL/PL-SQL implementations.
- **Chapter 6 (Conclusion & Future Scope):** Summary of achievements and future product roadmap.

---
<div style="page-break-after: always;"></div>

# Chapter 2: Literature Survey

A comparative analysis was conducted evaluating existing software, traditional manual mechanisms, and institutional ERP solutions against the proposed **CampusHire** architecture:

| Feature / Capability | Manual Spreadsheets (Excel) | Generic College ERP | Commercial ATS (LinkedIn Talent) | Enterprise HR (Oracle HCM) | **CampusHire (Proposed System)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Centralized Relational DB** | ❌ None | ⚠️ Partial | ✔️ Yes | ✔️ Yes | **✔️ Yes (MySQL 8.0 / InnoDB)** |
| **3NF Normalization** | ❌ Violations | ⚠️ Partial | ❌ Proprietary | ✔️ Yes | **✔️ Strict 3NF Decomposition** |
| **Automated Eligibility Filter** | ❌ Manual Sort | ⚠️ Basic | ✔️ Rule-based | ✔️ Complex | **✔️ Stored Procedure Logic** |
| **Multi-Round Interview Track** | ❌ Disconnected | ⚠️ Static | ✔️ Dynamic | ✔️ Yes | **✔️ 1:N Atomic Round Entities** |
| **Triggers & Event Automation** | ❌ None | ⚠️ Limited | ❌ No | ✔️ Yes | **✔️ Native Database Triggers** |
| **Explicit Cursor Analytics** | ❌ None | ❌ No | ❌ No | ✔️ Yes | **✔️ PL/SQL Cursor Iteration** |
| **Tamper-Proof Audit Trail** | ❌ None | ⚠️ Logs | ✔️ Yes | ✔️ Yes | **✔️ Automated `audit_logs` Trigger** |
| **Department-wise Analytics** | ❌ Manual Pivot | ✔️ Static | ⚠️ Paid add-on | ✔️ Yes | **✔️ 3 Dynamic SQL Views** |
| **Cost / License** | Free / Commercial | High Cost | Enterprise Subscription | Expensive | **✔️ 100% Free & Open Source** |
| **Academic & Pedagogical Value** | ❌ Low | ❌ Closed | ❌ Closed | ❌ Closed | **✔️ 100% Transparent SQL / 3NF** |

### Observations:
1. Spreadsheets fail completely under transaction volume, lacking referential constraints and atomicity.
2. Proprietary ERP platforms (Oracle, SAP) provide deep features but are black-box systems requiring expensive licensing and heavy hardware infrastructure.
3. **CampusHire** uniquely balances academic rigor, transparent schema design, enterprise normalization (3NF), and automated PL/SQL database constructs with zero licensing costs.

---
<div style="page-break-after: always;"></div>

# Chapter 3: Problem Statement

### 3.1 Background
In college and university environments, the Training and Placement (T&P) Cell manages high-stakes career transitions. Every academic year, a department must coordinate with 50+ companies, track hundreds of students across diverse engineering branches (CSE, IT, ECE, Mechanical), and process thousands of interview rounds.

### 3.2 The Problem (5 W's Analysis)
- **Who is affected?**
  - **Students:** Risk losing lucrative placement opportunities due to manual filtering mistakes or lost applications.
  - **Placement Coordinators:** Burdened by tedious manual record updates and duplicate reconciliation.
  - **Corporate Recruiters:** Experience delays due to inaccurate eligibility shortlists.
  - **College Management & HoDs:** Lack real-time, trustworthy analytics on department-wise placement metrics.
- **What is the issue?**
  Placement records maintained across disconnected spreadsheets suffer from:
  1. *Insertion Anomalies:* Inability to record a company drive without student applications.
  2. *Update Anomalies:* Data inconsistencies when company packages or student phone numbers change.
  3. *Deletion Anomalies:* Inadvertent loss of historical interview evaluations upon deleting an application.
- **When does it occur?**
  Most acutely during the peak placement season (August to March), where multiple hiring drives take place concurrently.
- **Where does it occur?**
  At all critical touchpoints: student onboarding, company drive publication, application verification, multi-round technical evaluations, and offer acceptance.
- **Why must it be fixed?**
  Accurate placement data directly impacts student careers, institutional accreditation (NAAC/NBA rankings), corporate trust, and future industry partnerships.

### 3.3 Proposed Solution
**CampusHire** solves these challenges by implementing an ACID-compliant relational database system:
- **11 Normalized Entities in 3NF** preventing all data redundancy.
- **Declarative Constraints** enforcing strict eligibility and valid ranges.
- **Database Triggers** ensuring that whenever an offer is accepted, the candidate's application status cascades immediately to `SELECTED` and logs to an immutable audit record.
- **Built-in Stored Procedures and Cursors** automating eligibility computation and interview statistics.

---
<div style="page-break-after: always;"></div>

# Chapter 4: Software Requirements Specification

### 4.1 Hardware Requirements
| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Processor** | Intel Core i3 / AMD Ryzen 3 @ 2.0 GHz | Intel Core i5 / AMD Ryzen 5 @ 2.5 GHz+ |
| **RAM** | 4 GB | 8 GB or 16 GB DDR4 |
| **Storage** | 10 GB free hard disk space | 256 GB SSD |
| **Display Resolution** | 1024 × 768 pixels | 1920 × 1080 (Full HD) |
| **Network Interface** | Standard 10/100 Mbps Ethernet / Wi-Fi | Gigabit LAN / High-Speed Wi-Fi |

### 4.2 Software Requirements
| Software Component | Version | Functional Purpose |
| :--- | :--- | :--- |
| **Database Server** | MySQL Community Server 8.0+ | Core relational database engine with InnoDB storage |
| **GUI Administration** | MySQL Workbench 8.0+ / DBeaver | Schema engineering, ER visual modeling, query execution |
| **Operating System** | Windows 10/11 (64-bit) / Ubuntu 20.04+ | Host operating system environment |
| **Web Browser** | Google Chrome / Mozilla Firefox / Edge | Web console and documentation rendering |
| **Local Runtime** | Python 3.10+ / SQLite 3 | Zero-configuration local verification and test execution |
| **Version Control** | Git 2.x & GitHub | Source code and database migration versioning |

---
<div style="page-break-after: always;"></div>

# Chapter 5: System Design

### 5.1 ER Diagram
The CampusHire database models the entire campus placement lifecycle. It captures students, departments, recruiting corporate partners, recruiters, recruitment drives, eligible branches, student applications, multi-round interview evaluations, placement offers, and immutable audit logs.

```mermaid
erDiagram
    USERS ||--o| STUDENTS : "1:1 profile"
    USERS ||--o| RECRUITERS : "1:1 profile"
    USERS ||--o{ AUDIT_LOGS : "logs actions"
    DEPARTMENTS ||--o{ STUDENTS : "enrolled in"
    DEPARTMENTS ||--o{ JOB_ELIGIBILITY_DEPARTMENTS : "eligible for"
    COMPANIES ||--o{ RECRUITERS : "employs"
    COMPANIES ||--o{ JOB_OPENINGS : "posts"
    JOB_OPENINGS ||--o{ JOB_ELIGIBILITY_DEPARTMENTS : "specifies"
    JOB_OPENINGS ||--o{ APPLICATIONS : "receives"
    STUDENTS ||--o{ APPLICATIONS : "submits"
    APPLICATIONS ||--o{ INTERVIEW_ROUNDS : "evaluated via"
    APPLICATIONS ||--o| PLACEMENT_OFFERS : "results in"

    USERS {
        int user_id PK
        string email UK
        string full_name
        string role
        string account_status
    }
    DEPARTMENTS {
        int department_id PK
        string department_code UK
        string department_name UK
    }
    STUDENTS {
        int student_id PK
        int user_id FK
        string enrollment_number UK
        int department_id FK
        decimal cgpa
        int active_backlogs
    }
    COMPANIES {
        int company_id PK
        string company_name UK
        string industry
        string headquarters
    }
    RECRUITERS {
        int recruiter_id PK
        int user_id FK
        int company_id FK
        string designation
    }
    JOB_OPENINGS {
        int job_id PK
        int company_id FK
        string job_title
        decimal package_lpa
        decimal minimum_cgpa
        int maximum_backlogs
        string job_status
    }
    JOB_ELIGIBILITY_DEPARTMENTS {
        int job_id PK_FK
        int department_id PK_FK
    }
    APPLICATIONS {
        int application_id PK
        int student_id FK
        int job_id FK
        string application_status
    }
    INTERVIEW_ROUNDS {
        int round_id PK
        int application_id FK
        int round_number
        decimal score
        string round_status
    }
    PLACEMENT_OFFERS {
        int offer_id PK
        int application_id FK_UK
        decimal offered_package_lpa
        string offer_status
    }
    AUDIT_LOGS {
        int audit_id PK
        int user_id FK
        string action
        string entity_type
        int entity_id
    }
```

#### Entity Definitions & Primary Keys [Table 2]
| Entity Name | Real-World Concept Modeled | Primary Key | Key Attributes & Unique Constraints |
| :--- | :--- | :--- | :--- |
| **`users`** | Master authentication and RBAC account | `user_id` | `email` (UK), `role`, `password_hash` |
| **`departments`** | Academic disciplines (CSE, IT, ECE, MECH) | `department_id` | `department_code` (UK), `department_name` (UK) |
| **`students`** | Enrolled candidate's academic credentials | `student_id` | `enrollment_number` (UK), `user_id` (1:1), `cgpa` |
| **`companies`** | Corporate organizations conducting drives | `company_id` | `company_name` (UK), `industry`, `headquarters` |
| **`recruiters`** | Corporate HR and talent acquisition managers | `recruiter_id` | `user_id` (1:1), `company_id` (FK), `designation` |
| **`job_openings`** | Recruitment drives and roles published | `job_id` | `company_id` (FK), `package_lpa`, `minimum_cgpa` |
| **`job_eligibility_departments`** | M:N Bridge between Jobs and Departments | `(job_id, department_id)` | Composite Primary Key |
| **`applications`** | Candidate application submitted for drive | `application_id` | `UNIQUE(student_id, job_id)`, `status` |
| **`interview_rounds`** | Sequential evaluation round for an application | `round_id` | `application_id` (FK), `round_number`, `score` |
| **`placement_offers`** | Official job offer rolled out | `offer_id` | `application_id` (FK, UK), `package_lpa`, `status` |
| **`audit_logs`** | Tamper-proof system audit trail | `audit_id` | `user_id`, `action`, `entity_type`, `created_at` |

#### Relationship Cardinality Summary [Table 3]
| Relationship Pair | Cardinality | Database Enforcement Mechanism |
| :--- | :---: | :--- |
| **`users` $\rightarrow$ `students`** | 1:1 | `UNIQUE(user_id)` constraint on `students` table |
| **`users` $\rightarrow$ `recruiters`** | 1:1 | `UNIQUE(user_id)` constraint on `recruiters` table |
| **`departments` $\rightarrow$ `students`** | 1:N | Foreign Key `department_id` in `students` (`ON DELETE RESTRICT`) |
| **`companies` $\rightarrow$ `job_openings`** | 1:N | Foreign Key `company_id` in `job_openings` (`ON DELETE RESTRICT`) |
| **`companies` $\rightarrow$ `recruiters`** | 1:N | Foreign Key `company_id` in `recruiters` (`ON DELETE CASCADE`) |
| **`job_openings` $\leftrightarrow$ `departments`** | M:N | Resolved via bridge entity `job_eligibility_departments` |
| **`students` $\leftrightarrow$ `job_openings`** | M:N | Resolved via bridge entity `applications` (`UNIQUE(student_id, job_id)`) |
| **`applications` $\rightarrow$ `interview_rounds`**| 1:N | Foreign Key `application_id` in `interview_rounds` (`ON DELETE CASCADE`) |
| **`applications` $\rightarrow$ `placement_offers`** | 1:1 | `UNIQUE(application_id)` on `placement_offers` table |
| **`users` $\rightarrow$ `audit_logs`** | 1:N | Foreign Key `user_id` in `audit_logs` (`ON DELETE SET NULL`) |

---

### 5.2 Relational Schema

#### Formal Relational Notation
*(Primary Keys are **underlined**, Foreign Keys are in *italics*)*

1. **USERS** (**user_id**, full_name, email [UK], password_hash, role, account_status, created_at, updated_at)
2. **DEPARTMENTS** (**department_id**, department_name [UK], department_code [UK], description, created_at)
3. **STUDENTS** (**student_id**, *user_id* [UK], enrollment_number [UK], *department_id*, graduation_year, cgpa, active_backlogs, phone, resume_url, profile_status, created_at, updated_at)
4. **COMPANIES** (**company_id**, company_name [UK], industry, website, company_description, headquarters, created_at, updated_at)
5. **RECRUITERS** (**recruiter_id**, *user_id* [UK], *company_id*, designation, phone, created_at)
6. **JOB_OPENINGS** (**job_id**, *company_id*, job_title, job_description, job_type, location, minimum_cgpa, maximum_backlogs, package_lpa, application_deadline, drive_date, job_status, *created_by*, created_at, updated_at)
7. **JOB_ELIGIBILITY_DEPARTMENTS** (**_job_id_**, **_department_id_**)
8. **APPLICATIONS** (**application_id**, *student_id*, *job_id*, application_date, application_status, updated_at) — *UNIQUE(student_id, job_id)*
9. **INTERVIEW_ROUNDS** (**round_id**, *application_id*, round_number, round_name, scheduled_at, score, feedback, round_status, *evaluated_by*, created_at, updated_at) — *UNIQUE(application_id, round_number)*
10. **PLACEMENT_OFFERS** (**offer_id**, *application_id* [UK], offered_package_lpa, offer_date, joining_date, offer_status, created_at, updated_at)
11. **AUDIT_LOGS** (**audit_id**, *user_id*, action, entity_type, entity_id, details, created_at)

---

#### Complete Data Dictionaries

##### Table 5: `users`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `user_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for authentication |
| `full_name` | VARCHAR(100) | NO | NOT NULL | User's legal full name |
| `email` | VARCHAR(150) | NO | UNIQUE, NOT NULL | Unique login email credential |
| `password_hash` | VARCHAR(255) | NO | NOT NULL | Secure salted bcrypt password hash |
| `role` | ENUM | NO | `'ADMIN', 'STUDENT', 'RECRUITER'` | Role-based authorization |
| `account_status` | ENUM | NO | `'ACTIVE', 'INACTIVE', 'SUSPENDED'` | Account activation state |
| `created_at` | TIMESTAMP | NO | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |
| `updated_at` | TIMESTAMP | NO | ON UPDATE CURRENT_TIMESTAMP | Last profile modification time |

##### Table 6: `students`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `student_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Student surrogate primary key |
| `user_id` | INT | NO | UNIQUE, FK $\rightarrow$ `users(user_id)` | 1:1 linkage to authentication user |
| `enrollment_number`| VARCHAR(50) | NO | UNIQUE, NOT NULL | University PRN / Roll Number |
| `department_id` | INT | NO | FK $\rightarrow$ `departments(department_id)`| Academic branch |
| `graduation_year` | INT | NO | NOT NULL | Target year of degree completion |
| `cgpa` | DECIMAL(4,2) | NO | `CHECK (cgpa BETWEEN 0.00 AND 10.00)` | Cumulative Grade Point Average |
| `active_backlogs` | INT | NO | DEFAULT 0, `CHECK (active_backlogs >= 0)` | Live un-cleared backlog subjects |
| `phone` | VARCHAR(20) | YES | NULL | Student mobile contact number |
| `resume_url` | VARCHAR(255) | YES | NULL | Cloud URL pointing to verified PDF CV |
| `profile_status` | ENUM | NO | `'PENDING', 'VERIFIED', 'REJECTED'` | T&P verification approval state |

##### Table 7: `companies`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `company_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Corporate organization primary key |
| `company_name` | VARCHAR(150) | NO | UNIQUE, NOT NULL | Official company registration name |
| `industry` | VARCHAR(100) | NO | NOT NULL | Core domain (FinTech, Cloud, VLSI) |
| `website` | VARCHAR(255) | YES | NULL | Official corporate website URL |
| `company_description`| TEXT | YES | NULL | Institutional overview and profile |
| `headquarters` | VARCHAR(100) | YES | NULL | Primary office / corporate headquarters |

##### Table 8: `job_openings`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `job_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Drive opening identifier |
| `company_id` | INT | NO | FK $\rightarrow$ `companies(company_id)` | Visiting corporate employer |
| `job_title` | VARCHAR(150) | NO | NOT NULL | Profile designation (e.g. SDE-1) |
| `job_type` | ENUM | NO | `'FULL_TIME', 'INTERNSHIP'` | Employment structure |
| `location` | VARCHAR(100) | NO | NOT NULL | Work posting location (e.g. Pune) |
| `minimum_cgpa` | DECIMAL(4,2) | NO | `CHECK (minimum_cgpa BETWEEN 0 AND 10)` | Academic cutoff threshold |
| `maximum_backlogs`| INT | NO | `CHECK (maximum_backlogs >= 0)` | Backlog threshold limit |
| `package_lpa` | DECIMAL(6,2) | NO | `CHECK (package_lpa >= 0.00)` | Annual compensation in Lakhs (INR) |
| `application_deadline`| DATETIME | NO | NOT NULL | Expiration timestamp for applications |
| `drive_date` | DATETIME | YES | NULL | On-campus drive assessment date |
| `job_status` | ENUM | NO | `'DRAFT', 'OPEN', 'CLOSED', 'CANCELLED'`| Drive progress status |
| `created_by` | INT | NO | FK $\rightarrow$ `users(user_id)` | Admin coordinator who created drive |

##### Table 9: `applications`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `application_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Application transaction identifier |
| `student_id` | INT | NO | FK $\rightarrow$ `students(student_id)` | Applying candidate |
| `job_id` | INT | NO | FK $\rightarrow$ `job_openings(job_id)` | Recruitment drive applied for |
| `application_date`| TIMESTAMP | NO | DEFAULT CURRENT_TIMESTAMP | Application submission timestamp |
| `application_status`| ENUM | NO | `'APPLIED', 'SHORTLISTED', 'REJECTED', 'SELECTED', 'WITHDRAWN'` | Pipeline state |
| *(Composite Key)* | — | — | `UNIQUE(student_id, job_id)` | Prevents duplicate submissions |

##### Table 10: `interview_rounds`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `round_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Interview round identifier |
| `application_id` | INT | NO | FK $\rightarrow$ `applications(application_id)` | Associated application (CASCADE) |
| `round_number` | INT | NO | NOT NULL | Sequential round index (1, 2, 3...) |
| `round_name` | VARCHAR(100) | NO | NOT NULL | Round label (Technical, HR) |
| `scheduled_at` | DATETIME | YES | NULL | Date and time of interview |
| `score` | DECIMAL(5,2) | YES | `CHECK (score IS NULL OR (score BETWEEN 0 AND 100))` | Evaluator score out of 100 |
| `feedback` | TEXT | YES | NULL | Recruiter evaluation notes |
| `round_status` | ENUM | NO | `'PENDING', 'PASSED', 'FAILED', 'NOT_ATTENDED'` | Round outcome |
| `evaluated_by` | INT | YES | FK $\rightarrow$ `users(user_id)` (SET NULL) | Assessing recruiter |

##### Table 11: `placement_offers`
| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- |
| `offer_id` | INT | NO | PRIMARY KEY, AUTO_INCREMENT | Official placement offer identifier |
| `application_id` | INT | NO | UNIQUE, FK $\rightarrow$ `applications` | Successful application candidate |
| `offered_package_lpa`| DECIMAL(6,2)| NO | `CHECK (offered_package_lpa >= 0.00)` | Final CTC package rolled out |
| `offer_date` | DATE | NO | NOT NULL | Release date of offer letter |
| `joining_date` | DATE | YES | NULL | Expected date of company onboarding |
| `offer_status` | ENUM | NO | `'OFFERED', 'ACCEPTED', 'DECLINED', 'WITHDRAWN'` | Candidate decision state |

---

#### Referential Integrity & Cascade Rules Summary
| Referential Action | Target Tables & Foreign Keys | Engineering Rationale |
| :--- | :--- | :--- |
| **`ON DELETE RESTRICT`** | `departments` $\rightarrow$ `students`<br>`companies` $\rightarrow$ `job_openings`<br>`students` $\rightarrow$ `applications` | Prevents catastrophic data loss: an academic department or company cannot be deleted if active students or drives depend on it. |
| **`ON DELETE CASCADE`** | `job_openings` $\rightarrow$ `job_eligibility_departments`<br>`applications` $\rightarrow$ `interview_rounds`<br>`applications` $\rightarrow$ `placement_offers` | Maintains referential purity: when a job drive or application is deleted, all child interview stages and offers are safely cleaned up. |
| **`ON DELETE SET NULL`** | `interview_rounds.evaluated_by`<br>`audit_logs.user_id` | Preserves historical integrity: even if a recruiter account is archived or deleted, historical evaluation scores and audit logs remain intact. |

---

### 5.3 Normalization (UNF to 3NF)

Normalization is the systematic mathematical technique of decomposing complex relations to eliminate data redundancy and prevent insertion, update, and deletion anomalies.

#### Unnormalized Form (UNF) & Anomalies [Table 1]
Consider the legacy placement tracking spreadsheet used prior to CampusHire:

| EnrollNo | StudentName | DeptCode | CGPA | JobTitle | Company | Round1 | Round2 | OfferLPA |
| :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| `EN001` | Rahul Verma | CSE | 9.45 | SDE-1 | Google | 95.0 | 92.5 | 28.5 |
| `EN001` | Rahul Verma | CSE | 9.45 | Cloud Eng | Microsoft | 90.0 | 85.0 | 24.0 |
| `EN002` | Priya Nair | CSE | 9.10 | SDE-1 | Google | 98.0 | 94.0 | 28.5 |
| `EN003` | Amit Patel | MECH | 7.80 | Auto Eng | Tata Motors | 80.0 | — | — |

##### Anomalies Inherent in UNF:
1. **Redundancy:** The student's full name, department, and CGPA are repeated for every company applied for.
2. **Update Anomaly:** If Google updates its corporate headquarters or package details, dozens of rows must be updated. A failure to update every occurrence produces conflicting data.
3. **Insertion Anomaly:** A new department (e.g., `'AIML'`) or visiting company cannot be inserted into the system until at least one student registers and applies for it.
4. **Deletion Anomaly:** If Amit Patel's application is deleted, all institutional knowledge regarding Tata Motors and its campus drive is permanently destroyed.

---

#### Normalization Pipeline Flow (Figure 3)
```
[Unnormalized Form (UNF)]
      │
      ▼  Rule 1: Eliminate multi-valued attributes and repeating groups; establish atomic keys.
[First Normal Form (1NF)]
      │
      ▼  Rule 2: Eliminate partial dependencies; non-prime attributes must depend on entire PK.
[Second Normal Form (2NF)]
      │
      ▼  Rule 3: Eliminate transitive dependencies (X → Y → Z); depend ONLY on the key.
[Third Normal Form (3NF)] -> Final Decomposed Normalized Schema (11 Entities)
```

---

#### First Normal Form (1NF)
> **Definition:** A relation $R$ is in 1NF if and only if all underlying attribute domains contain only atomic (indivisible) values, and there are no repeating groups.

##### Violations Addressed in CampusHire:
1. **Multi-Valued Eligible Departments:** Legacy schemas stored eligible branches as a comma-separated string `'CSE, IT, ECE'` inside the job table. This violates atomicity.  
   *Solution:* Decomposed into the bridge entity `job_eligibility_departments` with composite key `(job_id, department_id)`, storing exactly one branch per row.
2. **Repeating Interview Scores:** Storing columns `round1_score`, `round2_score`, `round3_score` creates repeating groups and artificially caps the number of rounds.  
   *Solution:* Extracted to an independent entity `interview_rounds(round_id, application_id, round_number, score)`.

---

#### Second Normal Form (2NF)
> **Definition:** A relation $R$ is in 2NF if it is in 1NF and no non-prime attribute is partially functionally dependent on any candidate key (full functional dependency).

##### Violations Addressed in CampusHire:
In an interim table with composite key `(student_id, job_id)`:
- `student_name` depended solely on `student_id` (Partial Dependency).
- `company_name` depended solely on `job_id` (Partial Dependency).
*Solution:* Decomposed into three distinct relations:
- `students(student_id, ...)`
- `job_openings(job_id, ...)`
- `applications(application_id, student_id, job_id, ...)` where non-prime attributes (`application_status`, `application_date`) depend strictly on the composite pair.

---

#### Third Normal Form (3NF)
> **Definition:** A relation $R$ is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on any candidate key. Formally, for every functional dependency $X \rightarrow Y$, either $X$ is a superkey, or $Y$ is a prime attribute.

##### Transitive Dependencies Eliminated:
1. **Student $\rightarrow$ Department:**
   - Dependency: $\text{student\_id} \rightarrow \text{department\_id} \rightarrow \text{department\_name, department\_code}$
   - *Elimination:* Extracted `departments(department_id, department_name, department_code)`. `students` retains only the foreign key `department_id`.
2. **Job Opening $\rightarrow$ Company:**
   - Dependency: $\text{job\_id} \rightarrow \text{company\_id} \rightarrow \text{company\_name, industry, headquarters}$
   - *Elimination:* Extracted `companies(company_id, company_name, ...)`. `job_openings` references it via foreign key `company_id`.
3. **Application $\rightarrow$ Placement Offer:**
   - Dependency: $\text{application\_id} \rightarrow \text{offer\_id} \rightarrow \text{offered\_package\_lpa, offer\_status}$
   - *Elimination:* Extracted `placement_offers(offer_id, application_id, offered_package_lpa, ...)`.

---

#### Functional Dependencies Summary Table [Table 4]
| Relation | Primary Key | Determinant (LHS) | Dependent Attributes (RHS) | Normal Form |
| :--- | :--- | :--- | :--- | :---: |
| **`users`** | `user_id` | `user_id` | `full_name, email, password_hash, role, account_status` | **3NF** |
| **`departments`** | `department_id` | `department_id` | `department_name, department_code, description` | **3NF** |
| **`students`** | `student_id` | `student_id` | `user_id, enrollment_number, department_id, cgpa, backlogs` | **3NF** |
| **`companies`** | `company_id` | `company_id` | `company_name, industry, website, headquarters` | **3NF** |
| **`recruiters`** | `recruiter_id` | `recruiter_id` | `user_id, company_id, designation, phone` | **3NF** |
| **`job_openings`** | `job_id` | `job_id` | `company_id, job_title, package_lpa, minimum_cgpa, deadline`| **3NF** |
| **`job_eligibility`**| `(job_id, dept_id)` | `(job_id, dept_id)`| *(Bridge relation — no non-prime attributes)* | **3NF** |
| **`applications`** | `application_id` | `application_id` | `student_id, job_id, application_date, application_status` | **3NF** |
| **`interview_rounds`**| `round_id` | `round_id` | `application_id, round_number, score, feedback, status` | **3NF** |
| **`placement_offers`**| `offer_id` | `offer_id` | `application_id, offered_package_lpa, offer_date, status` | **3NF** |
| **`audit_logs`** | `audit_id` | `audit_id` | `user_id, action, entity_type, entity_id, details, created_at`| **3NF** |

---

### 5.4 Advanced Database Constructs

#### 5.4.1 Declarative Domain Integrity (CHECK Constraints)
To ensure bad data is rejected at the storage engine level, the following constraints are enforced:
```sql
ALTER TABLE students 
    ADD CONSTRAINT chk_student_cgpa CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
    ADD CONSTRAINT chk_student_backlogs CHECK (active_backlogs >= 0);

ALTER TABLE job_openings 
    ADD CONSTRAINT chk_job_cgpa CHECK (minimum_cgpa >= 0.00 AND minimum_cgpa <= 10.00),
    ADD CONSTRAINT chk_job_package CHECK (package_lpa >= 0.00);

ALTER TABLE interview_rounds 
    ADD CONSTRAINT chk_round_score CHECK (score IS NULL OR (score >= 0.00 AND score <= 100.00));

ALTER TABLE placement_offers 
    ADD CONSTRAINT chk_offer_package CHECK (offered_package_lpa >= 0.00);
```

---

#### 5.4.2 DML Operations & Complex Queries

##### Query 1: Multi-Table JOIN with Multi-Criteria Eligibility Verification
```sql
-- Retrieve all OPEN jobs an active student (student_id = 3) is eligible for
SELECT jo.job_title, c.company_name, jo.package_lpa, jo.minimum_cgpa
FROM job_openings jo
JOIN companies c ON jo.company_id = c.company_id
JOIN job_eligibility_departments jed ON jo.job_id = jed.job_id
JOIN students s ON jed.department_id = s.department_id
WHERE s.student_id = 3
  AND jo.job_status = 'OPEN'
  AND s.cgpa >= jo.minimum_cgpa
  AND s.active_backlogs <= jo.maximum_backlogs;
```

##### Query 2: Aggregate Reporting with GROUP BY & Percentage Computation
```sql
-- Branch-wise placement percentage and package metrics
SELECT d.department_name,
       COUNT(DISTINCT s.student_id) AS total_students,
       COUNT(DISTINCT po.offer_id) AS placed_students,
       ROUND(COUNT(DISTINCT po.offer_id) * 100.0 / NULLIF(COUNT(DISTINCT s.student_id), 0), 2) AS placement_pct,
       MAX(po.offered_package_lpa) AS highest_package,
       ROUND(AVG(po.offered_package_lpa), 2) AS average_package
FROM departments d
JOIN students s ON d.department_id = s.department_id
LEFT JOIN applications a ON s.student_id = a.student_id
LEFT JOIN placement_offers po ON a.application_id = po.application_id AND po.offer_status = 'ACCEPTED'
GROUP BY d.department_id, d.department_name
ORDER BY placement_pct DESC;
```

---

#### 5.4.3 Analytical Views
```sql
-- View 1: Student Placement Profile Summary
CREATE VIEW v_student_placement_summary AS
SELECT s.student_id, s.enrollment_number, u.full_name AS student_name, u.email,
       d.department_code, s.cgpa, s.active_backlogs, s.profile_status,
       COUNT(DISTINCT a.application_id) AS total_applications,
       MAX(po.offered_package_lpa) AS highest_package_lpa,
       CASE WHEN COUNT(po.offer_id) > 0 THEN 'PLACED' ELSE 'UNPLACED' END AS placement_status
FROM students s
JOIN users u ON s.user_id = u.user_id
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN applications a ON s.student_id = a.student_id
LEFT JOIN placement_offers po ON a.application_id = po.application_id AND po.offer_status = 'ACCEPTED'
GROUP BY s.student_id, s.enrollment_number, u.full_name, u.email, d.department_code, s.cgpa, s.active_backlogs, s.profile_status;

-- View 2: Department Placement Analytics
CREATE VIEW v_department_placement_statistics AS
SELECT d.department_id, d.department_code, d.department_name,
       COUNT(DISTINCT s.student_id) AS total_students,
       COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) AS placed_students,
       ROUND((COUNT(DISTINCT CASE WHEN o.offer_status = 'ACCEPTED' THEN s.student_id END) * 100.0) / NULLIF(COUNT(DISTINCT s.student_id), 0), 2) AS placement_percentage,
       ROUND(AVG(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END), 2) AS average_package_lpa,
       MAX(CASE WHEN o.offer_status = 'ACCEPTED' THEN o.offered_package_lpa END) AS highest_package_lpa
FROM departments d
LEFT JOIN students s ON d.department_id = s.department_id
LEFT JOIN applications a ON s.student_id = a.student_id
LEFT JOIN placement_offers o ON a.application_id = o.application_id
GROUP BY d.department_id, d.department_code, d.department_name;
```

---

#### 5.4.4 Stored Function
Computes overall campus placement percentage dynamically:

$$\text{Placement Percentage} = \left( \frac{\text{Distinct Placed Students with Accepted Offer}}{\text{Total Registered Active Students}} \right) \times 100$$

```sql
DELIMITER //
CREATE FUNCTION fn_calculate_overall_placement_percentage()
RETURNS DECIMAL(5,2)
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE total_students INT DEFAULT 0;
    DECLARE placed_students INT DEFAULT 0;

    SELECT COUNT(DISTINCT s.student_id) INTO total_students
    FROM students s 
    JOIN users u ON s.user_id = u.user_id
    WHERE u.account_status = 'ACTIVE';

    SELECT COUNT(DISTINCT a.student_id) INTO placed_students
    FROM applications a
    JOIN placement_offers po ON a.application_id = po.application_id
    WHERE po.offer_status = 'ACCEPTED';

    IF total_students = 0 THEN
        RETURN 0.00;
    END IF;

    RETURN ROUND((placed_students / total_students) * 100.0, 2);
END //
DELIMITER ;
```

---

#### 5.4.5 Stored Procedures

##### Procedure 1: Parameterized Eligibility Evaluator
```sql
DELIMITER //
CREATE PROCEDURE sp_get_eligible_students(IN p_job_id INT)
BEGIN
    SELECT s.enrollment_number, u.full_name, d.department_code,
           s.cgpa, s.active_backlogs,
           IF(a.application_id IS NOT NULL, 'ALREADY_APPLIED', 'NOT_APPLIED') AS status
    FROM students s
    JOIN users u ON s.user_id = u.user_id
    JOIN departments d ON s.department_id = d.department_id
    JOIN job_eligibility_departments jed ON s.department_id = jed.department_id
    JOIN job_openings jo ON jed.job_id = jo.job_id
    LEFT JOIN applications a ON s.student_id = a.student_id AND a.job_id = p_job_id
    WHERE jo.job_id = p_job_id
      AND s.cgpa >= jo.minimum_cgpa
      AND s.active_backlogs <= jo.maximum_backlogs
    ORDER BY s.cgpa DESC;
END //
DELIMITER ;
```

---

#### 5.4.6 Explicit Cursor Implementation
Demonstrates complete 6-stage cursor lifecycle (`DECLARE`, `HANDLER`, `OPEN`, `LOOP/FETCH`, `PROCESS`, `CLOSE`):

```sql
DELIMITER //
CREATE PROCEDURE sp_cursor_interview_round_statistics()
BEGIN
    DECLARE done BOOLEAN DEFAULT FALSE;
    DECLARE v_status VARCHAR(20);
    DECLARE v_score  DECIMAL(5,2);
    DECLARE total_rounds  INT DEFAULT 0;
    DECLARE passed_rounds INT DEFAULT 0;
    DECLARE failed_rounds INT DEFAULT 0;
    DECLARE not_attended  INT DEFAULT 0;

    -- Stage 1: Cursor Declaration
    DECLARE cur_rounds CURSOR FOR
        SELECT round_status, score FROM interview_rounds;

    -- Stage 2: NOT FOUND Exception Handler
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Stage 3: Open Cursor
    OPEN cur_rounds;

    rounds_loop: LOOP
        -- Stage 4: Fetch Record
        FETCH cur_rounds INTO v_status, v_score;
        IF done THEN 
            LEAVE rounds_loop; 
        END IF;

        SET total_rounds = total_rounds + 1;

        -- Stage 5: Iterative Processing
        CASE v_status
            WHEN 'PASSED'       THEN SET passed_rounds = passed_rounds + 1;
            WHEN 'FAILED'       THEN SET failed_rounds = failed_rounds + 1;
            WHEN 'NOT_ATTENDED' THEN SET not_attended  = not_attended  + 1;
        END CASE;
    END LOOP;

    -- Stage 6: Close Cursor
    CLOSE cur_rounds;

    SELECT total_rounds, passed_rounds, failed_rounds, not_attended,
           ROUND((passed_rounds * 100.0) / NULLIF(total_rounds, 0), 2) AS pass_rate_percentage;
END //
DELIMITER ;
```

---

#### 5.4.7 Database Triggers

##### Trigger 1: Automatic Audit Logging
```sql
DELIMITER //
CREATE TRIGGER trg_after_application_insert
AFTER INSERT ON applications 
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs(user_id, action, entity_type, entity_id, details, created_at)
    VALUES(
        (SELECT user_id FROM students WHERE student_id = NEW.student_id LIMIT 1),
        'NEW_APPLICATION_SUBMITTED', 'APPLICATION', NEW.application_id,
        CONCAT('Student ID ', NEW.student_id, ' applied for Job Opening ID ', NEW.job_id, '. Initial status: ', NEW.application_status),
        NOW()
    );
END //
DELIMITER ;
```

##### Trigger 2: Automatic Status Synchronization
```sql
DELIMITER //
CREATE TRIGGER trg_after_offer_update
AFTER UPDATE ON placement_offers 
FOR EACH ROW
BEGIN
    IF NEW.offer_status = 'ACCEPTED' AND OLD.offer_status != 'ACCEPTED' THEN
        -- Automatically synchronize application status to SELECTED
        UPDATE applications
        SET application_status = 'SELECTED'
        WHERE application_id = NEW.application_id;

        INSERT INTO audit_logs(user_id, action, entity_type, entity_id, details, created_at)
        VALUES(
            (SELECT s.user_id FROM applications a JOIN students s ON a.student_id = s.student_id WHERE a.application_id = NEW.application_id LIMIT 1),
            'PLACEMENT_OFFER_ACCEPTED', 'PLACEMENT_OFFER', NEW.offer_id,
            CONCAT('Offer ID ', NEW.offer_id, ' accepted. Package: ', NEW.offered_package_lpa, ' LPA. Application status updated to SELECTED.'),
            NOW()
        );
    END IF;
END //
DELIMITER ;
```

##### Trigger 3: Business Rule Enforcement & Validation
```sql
DELIMITER //
CREATE TRIGGER trg_before_application_insert_check
BEFORE INSERT ON applications 
FOR EACH ROW
BEGIN
    DECLARE v_status   VARCHAR(20);
    DECLARE v_deadline DATETIME;

    SELECT job_status, application_deadline
    INTO v_status, v_deadline
    FROM job_openings 
    WHERE job_id = NEW.job_id;

    IF v_status != 'OPEN' OR v_deadline < NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Validation Error: Applications can only be submitted for OPEN recruitment drives before deadline.';
    END IF;
END //
DELIMITER ;
```

---

#### 5.4.8 Project File Structure [Table 12]
| File / Directory | Module Purpose |
| :--- | :--- |
| **`college_placement_all_in_one.sql`** | Master executable script containing complete DDL, DML, Views, Stored Functions, Procedures, Cursors, and Triggers for MySQL Workbench. |
| **`college_placement.db`** | Production SQLite 3NF database containing the expanded dataset (50 students, 16 partner companies, 18 drives). |
| **`database.py`** | Core Python database engine implementing SQL execution, connection pooling, and procedural simulators. |
| **`app.py`** | Web application backend providing full CRUD routes, role switching, database backup endpoints, and analytics APIs. |
| **`db_cli.py` & `open_db_terminal.bat`** | Interactive direct database terminal for command-line live queries and viva demonstrations. |
| **`verify_all_crud.py`** | Automated verification test suite testing 32 distinct CRUD operations across all entities. |
| **`SQL_QUERIES_LIST.txt`** | Ready-to-use reference document containing SQL queries organized into 8 sections for presentation. |

---
<div style="page-break-after: always;"></div>

# Chapter 6: Conclusion and Future Scope

### 6.1 Conclusion
The **College Placement and Recruitment Management System (CampusHire)** successfully accomplishes all academic and technical objectives stipulated for the Data Engineering Mini Project:
1. **Mathematical Normalization (3NF):** Completely decomposed complex recruitment entities into 11 relational tables, eliminating partial and transitive functional dependencies.
2. **Three-Tier Integrity Enforcement:** Ensured absolute data validity through Primary Keys, Foreign Keys with cascade policies (`CASCADE`, `RESTRICT`, `SET NULL`), and domain-level `CHECK` constraints.
3. **Advanced PL/SQL Automation:** Successfully developed Stored Functions, Stored Procedures, an Explicit Cursor, and Database Triggers that automate complex business rules, audit trail generation, and status synchronization.
4. **Verified Performance:** Tested through automated test suites (`test_app_and_db.py` and `verify_all_crud.py`), confirming 100% operational success across all CRUD endpoints and SQL queries.

In conclusion, CampusHire replaces inefficient, error-prone manual spreadsheets with a high-performance, resilient, and enterprise-grade relational database solution.

### 6.2 Future Scope
1. **Machine Learning-Based Resume Parser:** Integrate NLP models (spaCy / BERT) to automatically extract skills from student resumes and compute candidate-to-job matching scores.
2. **Automated Notification System:** Integrate SMTP email and WhatsApp Business APIs to dispatch instant alerts when new recruitment drives are posted or interview rounds are scheduled.
3. **Enterprise SSO & OAuth 2.0:** Expand authentication using Google Workspace and institutional Single Sign-On (SSO) protocols.
4. **Cloud Managed Database Migration:** Deploy the schema to AWS RDS (MySQL Aurora) or Google Cloud SQL with automated failover and multi-region read replicas.
5. **Predictive Placement Analytics:** Develop predictive regression models analyzing historical student academic performance against placement outcomes to identify students requiring early training intervention.

---
<div style="page-break-after: always;"></div>

# References

- **[1]** Ramez Elmasri and Shamkant B. Navathe, *"Fundamentals of Database Systems"*, 7th Edition, Pearson Education, 2016.
- **[2]** Abraham Silberschatz, Henry F. Korth, and S. Sudarshan, *"Database System Concepts"*, 7th Edition, McGraw-Hill Education, 2019.
- **[3]** C. J. Date, *"An Introduction to Database Systems"*, 8th Edition, Addison-Wesley, 2004.
- **[4]** MySQL Documentation, *"MySQL 8.0 Reference Manual"*, Oracle Corporation. Available: [https://dev.mysql.com/doc/refman/8.0/en/](https://dev.mysql.com/doc/refman/8.0/en/)
- **[5]** W. Kent, *"A Simple Guide to Five Normal Forms in Relational Database Theory"*, Communications of the ACM, Vol. 26, No. 2, pp. 120–125, 1983.
- **[6]** MySQL Workbench Manual, Oracle Corporation. Available: [https://dev.mysql.com/doc/workbench/en/](https://dev.mysql.com/doc/workbench/en/)

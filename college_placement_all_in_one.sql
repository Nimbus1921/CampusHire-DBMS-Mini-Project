-- ============================================================================
-- Project: CampusHire — College Placement and Recruitment Management System
-- File: college_placement_all_in_one.sql
-- Description: Complete, standalone SQL script for MySQL Workbench.
--              Includes Database Creation, Tables (3NF), Sample Data, Views,
--              Stored Functions, Stored Procedures, Cursors, Triggers & Reports.
-- Instructions for MySQL Workbench:
--   1. Open this file in MySQL Workbench (File -> Open SQL Script...)
--   2. Click the Lightning Icon (Execute) to run the entire script.
-- ============================================================================

-- ============================================================================
-- PART 1: CREATE DATABASE
-- ============================================================================
DROP DATABASE IF EXISTS college_placement_db;

CREATE DATABASE college_placement_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE college_placement_db;


-- ============================================================================
-- PART 2: CREATE NORMALIZED TABLES (3NF)
-- ============================================================================

-- Table 1: users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'STUDENT', 'RECRUITER') NOT NULL,
    account_status ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_role_status (role, account_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 2: departments
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 3: students
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    enrollment_number VARCHAR(50) NOT NULL UNIQUE,
    department_id INT NOT NULL,
    graduation_year INT NOT NULL,
    cgpa DECIMAL(4, 2) NOT NULL,
    active_backlogs INT NOT NULL DEFAULT 0,
    phone VARCHAR(20),
    resume_url VARCHAR(255) NULL,
    profile_status ENUM('PENDING_VERIFICATION', 'VERIFIED', 'SUSPENDED') NOT NULL DEFAULT 'VERIFIED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_student_cgpa CHECK (cgpa >= 0.00 AND cgpa <= 10.00),
    CONSTRAINT chk_student_backlogs CHECK (active_backlogs >= 0),
    CONSTRAINT fk_students_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_students_department FOREIGN KEY (department_id) 
        REFERENCES departments(department_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_students_dept_grad (department_id, graduation_year),
    INDEX idx_students_cgpa (cgpa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 4: companies
CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL UNIQUE,
    industry VARCHAR(100) NOT NULL,
    website VARCHAR(255),
    company_description TEXT,
    headquarters VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_companies_industry (industry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 5: recruiters
CREATE TABLE recruiters (
    recruiter_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    company_id INT NOT NULL,
    designation VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recruiters_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_recruiters_company FOREIGN KEY (company_id) 
        REFERENCES companies(company_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_recruiters_company (company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 6: job_openings
CREATE TABLE job_openings (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    job_title VARCHAR(150) NOT NULL,
    job_description TEXT NOT NULL,
    job_type ENUM('FULL_TIME', 'INTERNSHIP', 'INTERN_TO_FTE') NOT NULL DEFAULT 'FULL_TIME',
    location VARCHAR(100) NOT NULL,
    minimum_cgpa DECIMAL(4, 2) NOT NULL DEFAULT 0.00,
    maximum_backlogs INT NOT NULL DEFAULT 0,
    package_lpa DECIMAL(6, 2) NOT NULL,
    application_deadline DATETIME NOT NULL,
    drive_date DATETIME NULL,
    job_status ENUM('DRAFT', 'OPEN', 'CLOSED', 'CANCELLED') NOT NULL DEFAULT 'DRAFT',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_job_cgpa CHECK (minimum_cgpa >= 0.00 AND minimum_cgpa <= 10.00),
    CONSTRAINT chk_job_backlogs CHECK (maximum_backlogs >= 0),
    CONSTRAINT chk_job_package CHECK (package_lpa >= 0.00),
    CONSTRAINT fk_jobs_company FOREIGN KEY (company_id) 
        REFERENCES companies(company_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_jobs_created_by FOREIGN KEY (created_by) 
        REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_jobs_status_deadline (job_status, application_deadline),
    INDEX idx_jobs_company (company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 7: job_eligibility_departments
CREATE TABLE job_eligibility_departments (
    job_id INT NOT NULL,
    department_id INT NOT NULL,
    PRIMARY KEY (job_id, department_id),
    CONSTRAINT fk_jed_job FOREIGN KEY (job_id) 
        REFERENCES job_openings(job_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_jed_department FOREIGN KEY (department_id) 
        REFERENCES departments(department_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 8: applications
CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    job_id INT NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_status ENUM('APPLIED', 'SHORTLISTED', 'REJECTED', 'SELECTED', 'WITHDRAWN') NOT NULL DEFAULT 'APPLIED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_student_job UNIQUE (student_id, job_id),
    CONSTRAINT fk_app_student FOREIGN KEY (student_id) 
        REFERENCES students(student_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_app_job FOREIGN KEY (job_id) 
        REFERENCES job_openings(job_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_app_status (application_status),
    INDEX idx_app_student (student_id),
    INDEX idx_app_job (job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 9: interview_rounds
CREATE TABLE interview_rounds (
    round_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    round_number INT NOT NULL,
    round_name VARCHAR(100) NOT NULL,
    scheduled_at DATETIME NULL,
    score DECIMAL(5, 2) NULL,
    feedback TEXT NULL,
    round_status ENUM('PENDING', 'PASSED', 'FAILED', 'NOT_ATTENDED') NOT NULL DEFAULT 'PENDING',
    evaluated_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_app_round UNIQUE (application_id, round_number),
    CONSTRAINT chk_round_score CHECK (score IS NULL OR (score >= 0.00 AND score <= 100.00)),
    CONSTRAINT fk_rounds_application FOREIGN KEY (application_id) 
        REFERENCES applications(application_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_rounds_evaluated_by FOREIGN KEY (evaluated_by) 
        REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_rounds_status (round_status),
    INDEX idx_rounds_application (application_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 10: placement_offers
CREATE TABLE placement_offers (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL UNIQUE,
    offered_package_lpa DECIMAL(6, 2) NOT NULL,
    offer_date DATE NOT NULL,
    joining_date DATE NULL,
    offer_status ENUM('OFFERED', 'ACCEPTED', 'DECLINED', 'WITHDRAWN') NOT NULL DEFAULT 'OFFERED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_offer_package CHECK (offered_package_lpa >= 0.00),
    CONSTRAINT fk_offers_application FOREIGN KEY (application_id) 
        REFERENCES applications(application_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_offers_status (offer_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 11: audit_logs
CREATE TABLE audit_logs (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    details TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_audit_entity (entity_type, entity_id),
    INDEX idx_audit_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================================
-- PART 3: INSERT REALISTIC SAMPLE DATA
-- ============================================================================

-- Departments
INSERT INTO departments (department_id, department_name, department_code, description) VALUES
(1, 'Computer Science & Engineering', 'CSE', 'Department of Computer Science & Engineering'),
(2, 'Information Technology', 'IT', 'Department of Information Technology & Software Systems'),
(3, 'Electronics & Communication Engineering', 'ECE', 'Department of Electronics & Communication'),
(4, 'Mechanical Engineering', 'MECH', 'Department of Mechanical & Automation Engineering');

-- Users (Admin, Recruiters, Students)
INSERT INTO users (user_id, full_name, email, password_hash, role, account_status) VALUES
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
(120, 'Kavya Pillai', 'kavya.pillai@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE');

-- Students
INSERT INTO students (student_id, user_id, enrollment_number, department_id, graduation_year, cgpa, active_backlogs, phone, resume_url, profile_status) VALUES
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
(20, 120, 'EN2021MEC005', 4, 2025, 6.20, 0, '9876543229', 'https://campushire.edu/resumes/EN2021MEC005.pdf', 'VERIFIED');

-- Companies
INSERT INTO companies (company_id, company_name, industry, website, company_description, headquarters) VALUES
(1, 'Google India', 'Technology & Internet', 'https://careers.google.com', 'Global technology leader in search, cloud computing, and software.', 'Bengaluru, India'),
(2, 'Microsoft', 'Enterprise Software & Cloud', 'https://careers.microsoft.com', 'Pioneer in operating systems, Azure cloud, and developer platforms.', 'Hyderabad, India'),
(3, 'Amazon', 'E-Commerce & Cloud Computing', 'https://amazon.jobs', 'Global leader in e-commerce, cloud infrastructure, and streaming.', 'Bengaluru, India'),
(4, 'Tata Consultancy Services', 'IT Services & Consulting', 'https://www.tcs.com/careers', 'Largest Indian multinational information technology services provider.', 'Mumbai, India'),
(5, 'Infosys', 'Information Technology', 'https://www.infosys.com/careers', 'Global leader in next-generation digital services and consulting.', 'Bengaluru, India'),
(6, 'Deloitte Consulting', 'Management & Technology Consulting', 'https://www2.deloitte.com', 'Leading global provider of audit, consulting, advisory, and tax.', 'Hyderabad, India');

-- Recruiters
INSERT INTO recruiters (recruiter_id, user_id, company_id, designation, phone) VALUES
(1, 2, 1, 'Senior University Recruiter', '9811223344'),
(2, 3, 2, 'Campus Talent Acquisition Lead', '9822334455'),
(3, 4, 3, 'Technical Sourcing Specialist', '9833445566'),
(4, 5, 4, 'Regional Hiring Manager', '9844556677'),
(5, 6, 5, 'Campus Relations Lead', '9855667788'),
(6, 7, 6, 'Associate Director - Recruitment', '9866778899');

-- Job Openings
INSERT INTO job_openings (job_id, company_id, job_title, job_description, job_type, location, minimum_cgpa, maximum_backlogs, package_lpa, application_deadline, drive_date, job_status, created_by) VALUES
(1, 1, 'Software Engineer - Campus', 'Build scalable distributed systems, algorithms, and backend services.', 'FULL_TIME', 'Bengaluru', 8.50, 0, 28.50, '2026-12-31 23:59:59', '2027-01-15 09:00:00', 'OPEN', 1),
(2, 2, 'Software Development Engineer', 'Design core cloud features for Azure enterprise customers.', 'FULL_TIME', 'Hyderabad', 8.00, 0, 24.00, '2026-12-31 23:59:59', '2027-01-20 09:30:00', 'OPEN', 1),
(3, 3, 'SDE-1 (Full Stack & Systems)', 'Deliver high-volume payment services and AWS infrastructure tools.', 'FULL_TIME', 'Bengaluru', 7.50, 0, 22.00, '2026-12-31 23:59:59', '2027-01-25 10:00:00', 'OPEN', 1),
(4, 4, 'TCS Digital Engineer', 'Work on Next-Gen technologies like AI/ML, Cloud, and Big Data.', 'FULL_TIME', 'Pune / Mumbai', 6.50, 1, 7.50, '2026-12-31 23:59:59', '2027-02-05 09:00:00', 'OPEN', 1),
(5, 4, 'TCS Ninja Associate', 'Foundational software engineering across banking, retail, and healthcare.', 'FULL_TIME', 'PAN India', 6.00, 2, 3.80, '2026-12-31 23:59:59', '2027-02-10 09:00:00', 'OPEN', 1),
(6, 5, 'Specialist Programmer (SP)', 'High-end coding profile focusing on algorithmic problem solving.', 'FULL_TIME', 'Bengaluru / Pune', 7.00, 0, 9.50, '2026-12-31 23:59:59', '2027-02-15 09:00:00', 'OPEN', 1),
(7, 6, 'Technology Analyst', 'Consulting on enterprise ERP, cybersecurity, and cloud migration.', 'FULL_TIME', 'Hyderabad / Gurugram', 6.80, 0, 8.50, '2026-12-31 23:59:59', '2027-02-20 09:00:00', 'OPEN', 1),
(8, 6, 'Core Engineering Consultant', 'Supply chain automation and industrial engineering analytics.', 'FULL_TIME', 'Pune', 6.50, 1, 7.00, '2026-12-31 23:59:59', '2027-02-25 09:00:00', 'OPEN', 1);

-- Job Eligibility
INSERT INTO job_eligibility_departments (job_id, department_id) VALUES 
(1, 1), (1, 2),
(2, 1), (2, 2), (2, 3),
(3, 1), (3, 2), (3, 3),
(4, 1), (4, 2), (4, 3), (4, 4),
(5, 1), (5, 2), (5, 3), (5, 4),
(6, 1), (6, 2),
(7, 1), (7, 2), (7, 3),
(8, 4);

-- Applications
INSERT INTO applications (application_id, student_id, job_id, application_date, application_status) VALUES
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
(28, 18, 8, '2026-09-08 14:15:00', 'SELECTED');

-- Interview Rounds
INSERT INTO interview_rounds (round_id, application_id, round_number, round_name, scheduled_at, score, feedback, round_status, evaluated_by) VALUES
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
(16, 11, 2, 'Technical Round 1', '2026-09-22 11:00:00', NULL, 'Interview scheduled for upcoming Monday.', 'PENDING', 4);

-- Placement Offers
INSERT INTO placement_offers (offer_id, application_id, offered_package_lpa, offer_date, joining_date, offer_status) VALUES
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
(13, 28, 7.00, '2026-09-30', '2025-09-01', 'OFFERED');

-- Audit Logs
INSERT INTO audit_logs (audit_id, user_id, action, entity_type, entity_id, details) VALUES
(1, 1, 'CREATE_DATABASE', 'SYSTEM', NULL, 'College placement system database initialized.'),
(2, 1, 'CREATE_JOB', 'JOB_OPENING', 1, 'Prof. Anand Sharma published job: Google SDE Campus Drive.'),
(3, 101, 'SUBMIT_APPLICATION', 'APPLICATION', 1, 'Rahul Verma submitted application for Google SDE.'),
(4, 2, 'RECORD_INTERVIEW_RESULT', 'INTERVIEW_ROUND', 3, 'Sarah Jenkins marked Round 3 as PASSED for Rahul Verma.'),
(5, 2, 'GENERATE_OFFER', 'PLACEMENT_OFFER', 1, 'Sarah Jenkins rolled out 28.50 LPA offer to Rahul Verma.'),
(6, 101, 'ACCEPT_OFFER', 'PLACEMENT_OFFER', 1, 'Rahul Verma accepted the placement offer from Google India.');


-- ============================================================================
-- PART 4: CREATE VIEWS
-- ============================================================================

DROP VIEW IF EXISTS v_student_placement_summary;
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


DROP VIEW IF EXISTS v_job_opening_company_summary;
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
    GROUP_CONCAT(DISTINCT d.department_code ORDER BY d.department_code SEPARATOR ', ') AS eligible_departments,
    COUNT(DISTINCT a.application_id) AS total_applicants
FROM job_openings j
INNER JOIN companies c ON j.company_id = c.company_id
LEFT JOIN job_eligibility_departments jed ON j.job_id = jed.job_id
LEFT JOIN departments d ON jed.department_id = d.department_id
LEFT JOIN applications a ON j.job_id = a.job_id
GROUP BY j.job_id, c.company_name, c.industry, j.job_title, j.job_type, j.package_lpa, j.minimum_cgpa, j.maximum_backlogs, j.location, j.application_deadline, j.job_status;


DROP VIEW IF EXISTS v_department_placement_statistics;
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


-- ============================================================================
-- PART 5: STORED FUNCTIONS
-- ============================================================================

DROP FUNCTION IF EXISTS fn_calculate_overall_placement_percentage;
DROP FUNCTION IF EXISTS fn_calculate_department_placement_percentage;

DELIMITER $$

CREATE FUNCTION fn_calculate_overall_placement_percentage()
RETURNS DECIMAL(5, 2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total_students INT DEFAULT 0;
    DECLARE v_placed_students INT DEFAULT 0;
    DECLARE v_percentage DECIMAL(5, 2) DEFAULT 0.00;

    SELECT COUNT(*) 
    INTO v_total_students
    FROM students s
    INNER JOIN users u ON s.user_id = u.user_id
    WHERE u.account_status = 'ACTIVE';

    SELECT COUNT(DISTINCT s.student_id)
    INTO v_placed_students
    FROM students s
    INNER JOIN applications a ON s.student_id = a.student_id
    INNER JOIN placement_offers o ON a.application_id = o.application_id
    WHERE o.offer_status = 'ACCEPTED';

    IF v_total_students > 0 THEN
        SET v_percentage = ROUND((v_placed_students * 100.0) / v_total_students, 2);
    ELSE
        SET v_percentage = 0.00;
    END IF;

    RETURN v_percentage;
END$$

CREATE FUNCTION fn_calculate_department_placement_percentage(p_dept_id INT)
RETURNS DECIMAL(5, 2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total_dept_students INT DEFAULT 0;
    DECLARE v_placed_dept_students INT DEFAULT 0;
    DECLARE v_percentage DECIMAL(5, 2) DEFAULT 0.00;

    SELECT COUNT(*)
    INTO v_total_dept_students
    FROM students s
    INNER JOIN users u ON s.user_id = u.user_id
    WHERE s.department_id = p_dept_id AND u.account_status = 'ACTIVE';

    SELECT COUNT(DISTINCT s.student_id)
    INTO v_placed_dept_students
    FROM students s
    INNER JOIN applications a ON s.student_id = a.student_id
    INNER JOIN placement_offers o ON a.application_id = o.application_id
    WHERE s.department_id = p_dept_id AND o.offer_status = 'ACCEPTED';

    IF v_total_dept_students > 0 THEN
        SET v_percentage = ROUND((v_placed_dept_students * 100.0) / v_total_dept_students, 2);
    ELSE
        SET v_percentage = 0.00;
    END IF;

    RETURN v_percentage;
END$$

DELIMITER ;


-- ============================================================================
-- PART 6: STORED PROCEDURES
-- ============================================================================

DROP PROCEDURE IF EXISTS sp_get_eligible_students;
DROP PROCEDURE IF EXISTS sp_get_company_placement_summary;
DROP PROCEDURE IF EXISTS sp_get_department_placement_report;

DELIMITER $$

CREATE PROCEDURE sp_get_eligible_students(IN p_job_id INT)
BEGIN
    DECLARE v_job_exists INT DEFAULT 0;
    DECLARE v_min_cgpa DECIMAL(4, 2);
    DECLARE v_max_backlogs INT;
    DECLARE v_job_title VARCHAR(150);

    SELECT COUNT(*), minimum_cgpa, maximum_backlogs, job_title
    INTO v_job_exists, v_min_cgpa, v_max_backlogs, v_job_title
    FROM job_openings
    WHERE job_id = p_job_id
    GROUP BY job_id;

    IF v_job_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Job ID does not exist in the database.';
    ELSE
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
        INNER JOIN job_eligibility_departments jed ON s.department_id = jed.department_id AND jed.job_id = p_job_id
        LEFT JOIN applications a ON s.student_id = a.student_id AND a.job_id = p_job_id
        WHERE u.account_status = 'ACTIVE'
          AND s.cgpa >= v_min_cgpa
          AND s.active_backlogs <= v_max_backlogs
        ORDER BY s.cgpa DESC;
    END IF;
END$$

CREATE PROCEDURE sp_get_company_placement_summary()
BEGIN
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
END$$

CREATE PROCEDURE sp_get_department_placement_report(IN p_grad_year INT)
BEGIN
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
        AND (p_grad_year IS NULL OR s.graduation_year = p_grad_year)
    LEFT JOIN applications a ON s.student_id = a.student_id
    LEFT JOIN placement_offers o ON a.application_id = o.application_id
    GROUP BY d.department_id, d.department_code, d.department_name
    ORDER BY placement_percentage DESC;
END$$

DELIMITER ;


-- ============================================================================
-- PART 7: CURSORS
-- ============================================================================

DROP PROCEDURE IF EXISTS sp_cursor_interview_round_statistics;

DELIMITER $$

CREATE PROCEDURE sp_cursor_interview_round_statistics()
BEGIN
    DECLARE v_status VARCHAR(20);
    DECLARE v_score DECIMAL(5, 2);
    DECLARE done INT DEFAULT FALSE;

    DECLARE v_total_rounds INT DEFAULT 0;
    DECLARE v_passed_count INT DEFAULT 0;
    DECLARE v_failed_count INT DEFAULT 0;
    DECLARE v_pending_count INT DEFAULT 0;
    DECLARE v_not_attended_count INT DEFAULT 0;
    DECLARE v_total_score DECIMAL(10, 2) DEFAULT 0.00;
    DECLARE v_scored_rounds INT DEFAULT 0;
    DECLARE v_avg_score DECIMAL(5, 2) DEFAULT 0.00;

    DECLARE cur_rounds CURSOR FOR 
        SELECT round_status, score 
        FROM interview_rounds;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur_rounds;

    round_loop: LOOP
        FETCH cur_rounds INTO v_status, v_score;

        IF done THEN
            LEAVE round_loop;
        END IF;

        SET v_total_rounds = v_total_rounds + 1;

        IF v_status = 'PASSED' THEN
            SET v_passed_count = v_passed_count + 1;
        ELSEIF v_status = 'FAILED' THEN
            SET v_failed_count = v_failed_count + 1;
        ELSEIF v_status = 'PENDING' THEN
            SET v_pending_count = v_pending_count + 1;
        ELSEIF v_status = 'NOT_ATTENDED' THEN
            SET v_not_attended_count = v_not_attended_count + 1;
        END IF;

        IF v_score IS NOT NULL THEN
            SET v_total_score = v_total_score + v_score;
            SET v_scored_rounds = v_scored_rounds + 1;
        END IF;

    END LOOP round_loop;

    CLOSE cur_rounds;

    IF v_scored_rounds > 0 THEN
        SET v_avg_score = ROUND(v_total_score / v_scored_rounds, 2);
    END IF;

    SELECT 
        v_total_rounds AS total_interview_rounds,
        v_passed_count AS total_passed,
        v_failed_count AS total_failed,
        v_pending_count AS total_pending,
        v_not_attended_count AS total_not_attended,
        v_avg_score AS average_score_of_evaluated_rounds;
END$$

DELIMITER ;


-- ============================================================================
-- PART 8: TRIGGERS
-- ============================================================================

DROP TRIGGER IF EXISTS trg_after_application_insert;
DROP TRIGGER IF EXISTS trg_after_offer_update;
DROP TRIGGER IF EXISTS trg_before_application_insert_check;

DELIMITER $$

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
        CONCAT('Student ID ', NEW.student_id, ' applied for Job Opening ID ', NEW.job_id, '. Initial status: ', NEW.application_status),
        NOW()
    );
END$$

CREATE TRIGGER trg_after_offer_update
AFTER UPDATE ON placement_offers
FOR EACH ROW
BEGIN
    IF NEW.offer_status = 'ACCEPTED' AND OLD.offer_status <> 'ACCEPTED' THEN
        UPDATE applications
        SET application_status = 'SELECTED', updated_at = NOW()
        WHERE application_id = NEW.application_id;

        INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details, created_at)
        VALUES (
            (SELECT s.user_id FROM applications a JOIN students s ON a.student_id = s.student_id WHERE a.application_id = NEW.application_id LIMIT 1),
            'PLACEMENT_OFFER_ACCEPTED',
            'PLACEMENT_OFFER',
            NEW.offer_id,
            CONCAT('Offer ID ', NEW.offer_id, ' accepted. Package: ', NEW.offered_package_lpa, ' LPA. Application status updated to SELECTED.'),
            NOW()
        );
    END IF;
END$$

CREATE TRIGGER trg_before_application_insert_check
BEFORE INSERT ON applications
FOR EACH ROW
BEGIN
    DECLARE v_job_status VARCHAR(20);
    DECLARE v_deadline DATETIME;

    SELECT job_status, application_deadline
    INTO v_job_status, v_deadline
    FROM job_openings
    WHERE job_id = NEW.job_id;

    IF v_job_status <> 'OPEN' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Validation Error: Applications can only be submitted for OPEN recruitment drives.';
    END IF;

    IF v_deadline < NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Validation Error: Application deadline for this recruitment drive has expired.';
    END IF;
END$$

DELIMITER ;


-- ============================================================================
-- PART 9: INITIAL DEMONSTRATION & VERIFICATION OUTPUTS
-- ============================================================================

-- 1. Overall Placement Rate
SELECT fn_calculate_overall_placement_percentage() AS `Overall Placement %`;

-- 2. Department Statistics View
SELECT * FROM v_department_placement_statistics;

-- 3. Procedure: Eligible Students for Google SDE
CALL sp_get_eligible_students(1);

-- 4. Cursor: Interview Round Statistics
CALL sp_cursor_interview_round_statistics();

SELECT '=================================================================' AS Banner;
SELECT 'CampusHire Database Deployed & Fully Initialized Successfully!' AS Status;
SELECT '=================================================================' AS Banner;

"""
Data Expander for CampusHire College Placement Management System.
Expands the dataset to realistic college-level scale:
- 16 Top-Tier Companies (FAANG, FinTech, Tier-1 Product, Core VLSI/Auto, Consulting)
- 16 Recruiters
- 18 Diverse Campus Recruitment Drives (Packages from 3.8 LPA up to 36 LPA)
- 50 Students across CSE, IT, ECE, MECH with realistic CGPA distributions and profiles
- 60+ Applications
- 35+ Interview Rounds
- 30+ Placement Offers (Dream offers, Core offers, Mass offers)
- Rich Audit Trail & Trigger Events
"""

import sqlite3
import os
import database

def seed_college_dataset(cur):
    """Populates the database with realistic college-level placement drive data."""
    # 1. Departments
    depts = [
        (1, 'Computer Science & Engineering', 'CSE', 'Department of Computer Science & Engineering'),
        (2, 'Information Technology', 'IT', 'Department of Information Technology & Software Systems'),
        (3, 'Electronics & Communication Engineering', 'ECE', 'Department of Electronics & Communication'),
        (4, 'Mechanical Engineering', 'MECH', 'Department of Mechanical & Automation Engineering')
    ]
    cur.executemany("INSERT INTO departments VALUES (?, ?, ?, ?, datetime('now'))", depts)

    # 2. Users: Admin + 16 Recruiters + 50 Students
    users = [
        (1, 'Prof. Anand Sharma', 'admin@campushire.edu', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'ADMIN', 'ACTIVE'),
        (2, 'Sarah Jenkins', 'sarah.j@google.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (3, 'Vikram Malhotra', 'vikram.m@microsoft.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (4, 'Rachel Green', 'rachel.g@amazon.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (5, 'Suresh Iyer', 'suresh.i@tcs.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (6, 'Neha Kulkarni', 'neha.k@infosys.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (7, 'David Miller', 'david.m@deloitte.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (8, 'Aditi Singhania', 'aditi.s@goldmansachs.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (9, 'Kabir Mehta', 'kabir.m@adobe.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (10, 'Elena Rostova', 'elena.r@nvidia.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (11, 'Arjun Nambiar', 'arjun.n@cisco.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (12, 'Pooja Chawla', 'pooja.c@qualcomm.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (13, 'Ramesh Nair', 'ramesh.n@ti.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (14, 'Manish Deshmukh', 'manish.d@tatamotors.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (15, 'Sanjay Verma', 'sanjay.v@ltts.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (16, 'Sophie Taylor', 'sophie.t@atlassian.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE'),
        (17, 'Karan Grover', 'karan.g@jpmorgan.com', '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'RECRUITER', 'ACTIVE')
    ]

    # 50 Student Users (IDs 101 to 150)
    student_names = [
        "Rahul Verma", "Priya Nair", "Amit Patel", "Sneha Joshi", "Rohan Gupta",
        "Ananya Sen", "Karthik Rao", "Divya Menon", "Aditya Saxena", "Meera Reddy",
        "Tanmay Deshmukh", "Pooja Hegde", "Varun Chopra", "Shreya Das", "Nikhil Kulkarni",
        "Ritu Singhania", "Gaurav Bhat", "Isha Kapoor", "Siddharth Roy", "Kavya Pillai",
        "Ayush Agarwal", "Riya Sen", "Manav Sethi", "Swati Bhatt", "Harshit Jain",
        "Yash Vardhan", "Kunal Goswami", "Neha Tiwari", "Abhishek Yadav", "Simran Kaur",
        "Chirag Bansal", "Muskan Sharma", "Tushar Pandita", "Shruti Vats", "Akash Mishra",
        "Deepika Soni", "Mayank Rawat", "Prerna Jha", "Saurabh Pandey", "Aishwarya Iyer",
        "Naveen Kumar", "Pallavi Roy", "Deepak George", "Komal Walia", "Bhavesh Dave",
        "Sakshi Mahajan", "Vikas Rathore", "Tarun Bhasin", "Ritika Sengupta", "Ankit Tripathi"
    ]

    for idx, name in enumerate(student_names, start=101):
        email_prefix = name.lower().replace(" ", ".")
        users.append((idx, name, f"{email_prefix}@campushire.edu", '$2a$10$wT8K4e6K8FzQv5Q7b3Z0k.5Y0wX6t7L0c8n9Y4p3O2r1s0t123456', 'STUDENT', 'ACTIVE'))

    cur.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", users)

    # 3. Companies (16 realistic corporate partners)
    companies = [
        (1, 'Google India', 'Technology & Internet', 'https://careers.google.com', 'Global technology leader in search, AI, cloud computing, and operating systems.', 'Bengaluru, India'),
        (2, 'Microsoft', 'Enterprise Software & Cloud', 'https://careers.microsoft.com', 'Pioneer in Azure cloud, enterprise software, AI, and developer tools.', 'Hyderabad, India'),
        (3, 'Amazon', 'E-Commerce & Cloud Infrastructure', 'https://amazon.jobs', 'Global leader in AWS cloud, logistics infrastructure, and digital streaming.', 'Bengaluru, India'),
        (4, 'Tata Consultancy Services', 'IT Services & Consulting', 'https://www.tcs.com/careers', 'Largest Indian multinational information technology services provider.', 'Mumbai, India'),
        (5, 'Infosys', 'Information Technology', 'https://www.infosys.com/careers', 'Global leader in next-generation digital services, AI, and consulting.', 'Bengaluru, India'),
        (6, 'Deloitte Consulting', 'Management & Technology Consulting', 'https://www2.deloitte.com', 'Global provider of audit, strategy, technology consulting, and enterprise ERP.', 'Hyderabad, India'),
        (7, 'Goldman Sachs', 'Investment Banking & FinTech', 'https://www.goldmansachs.com/careers', 'Leading global financial institution and algorithmic trading platforms.', 'Bengaluru, India'),
        (8, 'Adobe Systems', 'Digital Media & Software', 'https://www.adobe.com/careers', 'World leader in creative cloud, digital marketing, and PDF workflows.', 'Noida, India'),
        (9, 'NVIDIA Graphics', 'AI, GPU & Hardware Computing', 'https://www.nvidia.com/en-in/about-nvidia/careers', 'Pioneer in accelerated GPU computing, CUDA architecture, and autonomous AI.', 'Pune, India'),
        (10, 'Cisco Systems', 'Networking & Cybersecurity', 'https://jobs.cisco.com', 'Global technology leader in enterprise routers, SD-WAN, and zero-trust security.', 'Bengaluru, India'),
        (11, 'Qualcomm India', 'Semiconductors & Wireless Telecom', 'https://www.qualcomm.com/company/careers', 'Pioneer in Snapdragon processors, 5G wireless modem, and RF systems.', 'Hyderabad, India'),
        (12, 'Texas Instruments', 'Analog & Embedded Semiconductors', 'https://careers.ti.com', 'World leader in analog electronics, embedded processing, and DSP chips.', 'Bengaluru, India'),
        (13, 'Tata Motors', 'Automotive & EV Mobility', 'https://www.tatamotors.com/careers', 'India largest automobile manufacturer leading electric passenger vehicles.', 'Pune, India'),
        (14, 'L&T Technology Services', 'Industrial Automation & Engineering', 'https://www.ltts.com/careers', 'Global engineering R&D services in robotics, plant engineering, and IoT.', 'Vadodara, India'),
        (15, 'Atlassian', 'Collaboration & Cloud Software', 'https://www.atlassian.com/company/careers', 'Makers of Jira, Confluence, Bitbucket, and modern agile collaboration suites.', 'Bengaluru, India'),
        (16, 'JPMorgan Chase & Co.', 'Global Banking & Quant Technology', 'https://careers.jpmorgan.com', 'Global investment banking powerhouse engineering real-time payment rails.', 'Mumbai, India')
    ]
    cur.executemany("INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", companies)

    # 4. Recruiters
    recruiters = [
        (1, 2, 1, 'Senior University Recruiter', '9811223344'),
        (2, 3, 2, 'Campus Talent Acquisition Lead', '9822334455'),
        (3, 4, 3, 'Technical Sourcing Specialist', '9833445566'),
        (4, 5, 4, 'Regional Hiring Manager', '9844556677'),
        (5, 6, 5, 'Campus Relations Lead', '9855667788'),
        (6, 7, 6, 'Associate Director - Recruitment', '9866778899'),
        (7, 8, 7, 'Vice President - Campus Hiring', '9877889900'),
        (8, 9, 8, 'Principal Talent Partner', '9888990011'),
        (9, 10, 9, 'Senior AI Talent Strategist', '9899001122'),
        (10, 11, 10, 'University Relations Specialist', '9800112233'),
        (11, 12, 11, 'Hardware Engineering Hiring Lead', '9811334455'),
        (12, 13, 12, 'Analog Design Recruiter', '9822445566'),
        (13, 14, 13, 'Chief HR Manager - Operations', '9833556677'),
        (14, 15, 14, 'Engineering Talent Lead', '9844667788'),
        (15, 16, 15, 'APAC Campus Talent Lead', '9855778899'),
        (16, 17, 16, 'Quantitative Technology Sourcing Head', '9866889900')
    ]
    cur.executemany("INSERT INTO recruiters VALUES (?, ?, ?, ?, ?, datetime('now'))", recruiters)

    # 5. Students (50 students: 13 CSE, 12 IT, 13 ECE, 12 MECH)
    # CGPA distributions: top-tier (9.0+), middle (7.5-8.9), average (6.1-7.4)
    cgpas = [
        9.75, 9.45, 9.10, 8.85, 8.65, 8.40, 8.20, 7.95, 7.65, 7.30, 7.05, 6.80, 6.45, # CSE (1-13)
        9.60, 9.30, 8.90, 8.80, 8.50, 8.15, 7.90, 7.55, 7.15, 6.90, 6.70, 6.25,       # IT (14-25)
        9.50, 9.20, 8.95, 8.70, 8.40, 8.10, 7.80, 7.50, 7.25, 6.95, 6.75, 6.40, 6.15, # ECE (26-38)
        9.35, 9.05, 8.70, 8.45, 8.10, 7.85, 7.50, 7.20, 6.90, 6.65, 6.35, 6.10        # MECH (39-50)
    ]
    backlogs = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, # CSE
        0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2,    # IT
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, # ECE
        0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 1     # MECH
    ]

    students = []
    for i in range(50):
        stud_id = i + 1
        user_id = 101 + i
        if i < 13:
            dept_id = 1
            code = "CSE"
            num = i + 1
        elif i < 25:
            dept_id = 2
            code = "IT"
            num = i - 12
        elif i < 38:
            dept_id = 3
            code = "ECE"
            num = i - 24
        else:
            dept_id = 4
            code = "MEC"
            num = i - 37
        enrollment = f"EN2021{code}{num:03d}"
        phone = f"98765{10000 + i}"
        resume = f"https://campushire.edu/resumes/{enrollment}.pdf"
        students.append((stud_id, user_id, enrollment, dept_id, 2025, cgpas[i], backlogs[i], phone, resume, 'VERIFIED'))

    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", students)

    # 6. Job Openings (18 diverse campus recruitment drives)
    jobs = [
        (1, 1, 'Software Engineer - Campus', 'Build scalable distributed systems, algorithms, and backend services.', 'FULL_TIME', 'Bengaluru', 8.50, 0, 28.50, '2026-12-31 23:59:59', '2027-01-15 09:00:00', 'OPEN', 1),
        (2, 2, 'Software Development Engineer', 'Design core cloud features for Azure enterprise customers.', 'FULL_TIME', 'Hyderabad', 8.00, 0, 24.00, '2026-12-31 23:59:59', '2027-01-20 09:30:00', 'OPEN', 1),
        (3, 3, 'SDE-1 (Full Stack & Systems)', 'Deliver high-volume payment services and AWS infrastructure tools.', 'FULL_TIME', 'Bengaluru', 7.50, 0, 22.00, '2026-12-31 23:59:59', '2027-01-25 10:00:00', 'OPEN', 1),
        (4, 15, 'Associate Software Engineer', 'Engineer mission-critical cloud collaboration tools with Jira and Confluence.', 'FULL_TIME', 'Bengaluru', 8.50, 0, 36.00, '2026-12-31 23:59:59', '2027-01-12 09:00:00', 'OPEN', 1),
        (5, 7, 'Quantitative FinTech SDE', 'Algorithmic trading systems, high-frequency execution pipelines, and risk modeling.', 'FULL_TIME', 'Bengaluru', 8.20, 0, 30.00, '2026-12-31 23:59:59', '2027-01-18 10:00:00', 'OPEN', 1),
        (6, 8, 'Member of Technical Staff (MTS)', 'Creative cloud rendering algorithms, GPU image pipelines, and digital media engine.', 'FULL_TIME', 'Noida', 8.00, 0, 26.00, '2026-12-31 23:59:59', '2027-01-22 09:30:00', 'OPEN', 1),
        (7, 9, 'Deep Learning Systems Engineer', 'CUDA optimization, TensorRT acceleration, and autonomous vehicle compute engines.', 'FULL_TIME', 'Pune', 8.00, 0, 25.00, '2026-12-31 23:59:59', '2027-01-28 10:00:00', 'OPEN', 1),
        (8, 10, 'Network Security Engineer', 'Design enterprise SD-WAN routing, zero-trust cloud proxies, and threat detection.', 'FULL_TIME', 'Bengaluru', 7.50, 0, 18.50, '2026-12-31 23:59:59', '2027-02-02 09:00:00', 'OPEN', 1),
        (9, 11, 'VLSI & 5G Modem Engineer', 'Digital ASIC physical design, timing closure, and 5G baseband DSP architectures.', 'FULL_TIME', 'Hyderabad', 7.80, 0, 21.00, '2026-12-31 23:59:59', '2027-02-04 09:00:00', 'OPEN', 1),
        (10, 12, 'Analog & Mixed-Signal Design', 'Precision operational amplifiers, power management ICs, and high-speed converters.', 'FULL_TIME', 'Bengaluru', 8.00, 0, 22.50, '2026-12-31 23:59:59', '2027-02-08 09:30:00', 'OPEN', 1),
        (11, 16, 'Corporate Technology Analyst', 'Global settlement platforms, blockchain infrastructure, and low-latency liquidity engines.', 'FULL_TIME', 'Mumbai', 7.50, 0, 19.00, '2026-12-31 23:59:59', '2027-02-10 10:00:00', 'OPEN', 1),
        (12, 13, 'Electric Vehicle Systems Trainee', 'Battery management systems (BMS), electric powertrain thermal analytics, and telematics.', 'FULL_TIME', 'Pune', 7.00, 1, 9.50, '2026-12-31 23:59:59', '2027-02-14 09:00:00', 'OPEN', 1),
        (13, 14, 'Industrial Automation Engineer', 'Robotics vision guidance, PLC automation, and digital twin simulation for factories.', 'FULL_TIME', 'Vadodara / Chennai', 6.80, 1, 7.80, '2026-12-31 23:59:59', '2027-02-18 09:30:00', 'OPEN', 1),
        (14, 6, 'Technology Consulting Analyst', 'Consulting on enterprise cloud migration, cybersecurity audits, and SAP S/4HANA.', 'FULL_TIME', 'Hyderabad / Gurugram', 6.80, 0, 8.50, '2026-12-31 23:59:59', '2027-02-20 09:00:00', 'OPEN', 1),
        (15, 6, 'Core Engineering Consultant', 'Supply chain automation, lean manufacturing, and industrial engineering analytics.', 'FULL_TIME', 'Pune', 6.50, 1, 7.00, '2026-12-31 23:59:59', '2027-02-22 09:00:00', 'OPEN', 1),
        (16, 4, 'TCS Digital Engineer', 'High-end engineering tracks in Generative AI, cloud modernization, and IoT platforms.', 'FULL_TIME', 'Pune / Bengaluru', 6.50, 1, 7.50, '2026-12-31 23:59:59', '2027-02-25 09:00:00', 'OPEN', 1),
        (17, 4, 'TCS Ninja Associate', 'Foundational software engineering across banking, retail, and healthcare applications.', 'FULL_TIME', 'PAN India', 6.00, 2, 3.80, '2026-12-31 23:59:59', '2027-03-01 09:00:00', 'OPEN', 1),
        (18, 5, 'Specialist Programmer (SP)', 'High-end coding profile focusing on algorithmic problem solving and distributed tech.', 'FULL_TIME', 'Bengaluru / Pune', 7.00, 0, 9.50, '2026-12-31 23:59:59', '2027-03-05 09:00:00', 'OPEN', 1)
    ]
    cur.executemany("INSERT INTO job_openings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", jobs)

    # 7. Job Eligibility Mapping (M:N)
    jed = [
        (1, 1), (1, 2),                   # Google: CSE, IT
        (2, 1), (2, 2), (2, 3),           # Microsoft: CSE, IT, ECE
        (3, 1), (3, 2), (3, 3),           # Amazon: CSE, IT, ECE
        (4, 1), (4, 2),                   # Atlassian: CSE, IT
        (5, 1), (5, 2),                   # Goldman: CSE, IT
        (6, 1), (6, 2),                   # Adobe: CSE, IT
        (7, 1), (7, 2), (7, 3),           # NVIDIA: CSE, IT, ECE
        (8, 1), (8, 2), (8, 3),           # Cisco: CSE, IT, ECE
        (9, 3), (9, 1),                   # Qualcomm: ECE, CSE
        (10, 3),                          # Texas Instruments: ECE
        (11, 1), (11, 2), (11, 3),        # JPMorgan: CSE, IT, ECE
        (12, 4), (12, 3),                 # Tata Motors: MECH, ECE
        (13, 4), (13, 3),                 # LTTS: MECH, ECE
        (14, 1), (14, 2), (14, 3),        # Deloitte Tech: CSE, IT, ECE
        (15, 4),                          # Deloitte Core: MECH
        (16, 1), (16, 2), (16, 3), (16, 4),# TCS Digital: All
        (17, 1), (17, 2), (17, 3), (17, 4),# TCS Ninja: All
        (18, 1), (18, 2), (18, 3)         # Infosys SP: CSE, IT, ECE
    ]
    cur.executemany("INSERT INTO job_eligibility_departments VALUES (?, ?)", jed)

    # 8. Applications (65 realistic applications across tier-1, core, and mass drives)
    apps = [
        # Dream Tier (Jobs 1 to 7)
        (1, 1, 1, '2026-09-01 10:00:00', 'SELECTED'),      # Rahul Verma -> Google
        (2, 2, 1, '2026-09-01 10:15:00', 'SELECTED'),      # Priya Nair -> Google
        (3, 14, 1, '2026-09-01 10:30:00', 'SELECTED'),     # Ayush Agarwal (IT) -> Google
        (4, 15, 4, '2026-09-02 09:00:00', 'SELECTED'),     # Riya Sen (IT) -> Atlassian (36 LPA)
        (5, 3, 4, '2026-09-02 09:15:00', 'SELECTED'),      # Amit Patel (CSE) -> Atlassian (36 LPA)
        (6, 1, 2, '2026-09-03 11:00:00', 'SELECTED'),      # Rahul -> Microsoft
        (7, 4, 2, '2026-09-03 11:15:00', 'SELECTED'),      # Sneha -> Microsoft
        (8, 16, 2, '2026-09-03 11:30:00', 'SELECTED'),     # Manav -> Microsoft
        (9, 26, 2, '2026-09-03 11:45:00', 'SELECTED'),     # Deepika (ECE) -> Microsoft
        (10, 5, 3, '2026-09-04 09:00:00', 'SELECTED'),     # Rohan -> Amazon
        (11, 17, 3, '2026-09-04 09:15:00', 'SELECTED'),    # Swati -> Amazon
        (12, 6, 5, '2026-09-05 10:00:00', 'SELECTED'),     # Ananya -> Goldman Sachs (30 LPA)
        (13, 18, 5, '2026-09-05 10:15:00', 'SELECTED'),    # Harshit -> Goldman Sachs (30 LPA)
        (14, 7, 6, '2026-09-06 10:00:00', 'SELECTED'),     # Karthik -> Adobe (26 LPA)
        (15, 27, 7, '2026-09-07 10:00:00', 'SELECTED'),    # Mayank (ECE) -> NVIDIA (25 LPA)
        (16, 8, 7, '2026-09-07 10:15:00', 'SELECTED'),     # Divya -> NVIDIA (25 LPA)
        (17, 19, 8, '2026-09-08 11:00:00', 'SELECTED'),    # Yash -> Cisco (18.5 LPA)
        (18, 28, 8, '2026-09-08 11:15:00', 'SELECTED'),    # Prerna (ECE) -> Cisco (18.5 LPA)
        # Core ECE Drives (Jobs 9, 10)
        (19, 26, 9, '2026-09-10 10:00:00', 'SELECTED'),    # Deepika -> Qualcomm (21 LPA)
        (20, 27, 9, '2026-09-10 10:15:00', 'SELECTED'),    # Mayank -> Qualcomm (21 LPA)
        (21, 29, 9, '2026-09-10 10:30:00', 'SELECTED'),    # Saurabh -> Qualcomm (21 LPA)
        (22, 28, 10, '2026-09-11 10:00:00', 'SELECTED'),   # Prerna -> Texas Instruments (22.5 LPA)
        (23, 30, 10, '2026-09-11 10:15:00', 'SELECTED'),   # Aishwarya -> Texas Instruments (22.5 LPA)
        (24, 31, 10, '2026-09-11 10:30:00', 'SHORTLISTED'),# Naveen -> Texas Instruments
        # FinTech & Consulting (Jobs 11, 14, 15)
        (25, 9, 11, '2026-09-12 11:00:00', 'SELECTED'),    # Aditya -> JPMorgan (19 LPA)
        (26, 20, 11, '2026-09-12 11:15:00', 'SELECTED'),   # Kunal -> JPMorgan (19 LPA)
        (27, 32, 11, '2026-09-12 11:30:00', 'SELECTED'),   # Pallavi (ECE) -> JPMorgan (19 LPA)
        (28, 10, 14, '2026-09-14 14:00:00', 'SELECTED'),   # Meera -> Deloitte Tech
        (29, 21, 14, '2026-09-14 14:15:00', 'SELECTED'),   # Neha -> Deloitte Tech
        (30, 33, 14, '2026-09-14 14:30:00', 'SELECTED'),   # Deepak (ECE) -> Deloitte Tech
        (31, 39, 15, '2026-09-15 14:00:00', 'SELECTED'),   # Bhavesh (MECH) -> Deloitte Core (7 LPA)
        (32, 40, 15, '2026-09-15 14:15:00', 'SELECTED'),   # Sakshi (MECH) -> Deloitte Core (7 LPA)
        # Core Mechanical & Auto (Jobs 12, 13)
        (33, 39, 12, '2026-09-16 10:00:00', 'SELECTED'),   # Bhavesh -> Tata Motors EV (9.5 LPA)
        (34, 41, 12, '2026-09-16 10:15:00', 'SELECTED'),   # Vikas -> Tata Motors EV (9.5 LPA)
        (35, 42, 12, '2026-09-16 10:30:00', 'SELECTED'),   # Tarun -> Tata Motors EV (9.5 LPA)
        (36, 43, 13, '2026-09-17 11:00:00', 'SELECTED'),   # Ritika -> LTTS Automation (7.8 LPA)
        (37, 44, 13, '2026-09-17 11:15:00', 'SELECTED'),   # Ankit -> LTTS Automation (7.8 LPA)
        # Mass & Foundation Drives (Jobs 16, 17, 18)
        (38, 11, 16, '2026-09-18 10:00:00', 'SELECTED'),   # Tanmay -> TCS Digital (7.5 LPA)
        (39, 22, 16, '2026-09-18 10:15:00', 'SELECTED'),   # Abhishek -> TCS Digital (7.5 LPA)
        (40, 34, 16, '2026-09-18 10:30:00', 'SELECTED'),   # Komal -> TCS Digital (7.5 LPA)
        (41, 45, 16, '2026-09-18 10:45:00', 'SELECTED'),   # Yash V -> TCS Digital (7.5 LPA)
        (42, 12, 18, '2026-09-19 11:00:00', 'SELECTED'),   # Pooja H -> Infosys SP (9.5 LPA)
        (43, 23, 18, '2026-09-19 11:15:00', 'SELECTED'),   # Simran -> Infosys SP (9.5 LPA)
        (44, 35, 18, '2026-09-19 11:30:00', 'SELECTED'),   # Chirag -> Infosys SP (9.5 LPA)
        (45, 13, 17, '2026-09-20 10:00:00', 'SELECTED'),   # Varun -> TCS Ninja (3.8 LPA)
        (46, 24, 17, '2026-09-20 10:15:00', 'SELECTED'),   # Muskan -> TCS Ninja (3.8 LPA)
        (47, 36, 17, '2026-09-20 10:30:00', 'SELECTED'),   # Tushar -> TCS Ninja (3.8 LPA)
        (48, 46, 17, '2026-09-20 10:45:00', 'SELECTED'),   # Shruti -> TCS Ninja (3.8 LPA)
        (49, 47, 17, '2026-09-20 11:00:00', 'SELECTED'),   # Akash -> TCS Ninja (3.8 LPA)
        (50, 48, 17, '2026-09-20 11:15:00', 'SELECTED'),   # Soni -> TCS Ninja (3.8 LPA)
        # Shortlisted & Applied Candidates
        (51, 10, 1, '2026-09-22 10:00:00', 'SHORTLISTED'),
        (52, 21, 2, '2026-09-22 10:15:00', 'SHORTLISTED'),
        (53, 37, 9, '2026-09-22 10:30:00', 'SHORTLISTED'),
        (54, 49, 12, '2026-09-22 10:45:00', 'SHORTLISTED'),
        (55, 50, 13, '2026-09-22 11:00:00', 'APPLIED'),
        (56, 25, 16, '2026-09-22 11:15:00', 'APPLIED'),
        (57, 38, 17, '2026-09-22 11:30:00', 'APPLIED'),
        (58, 49, 17, '2026-09-22 11:45:00', 'APPLIED'),
        (59, 13, 2, '2026-09-22 12:00:00', 'REJECTED'),
        (60, 24, 3, '2026-09-22 12:15:00', 'REJECTED')
    ]
    cur.executemany("INSERT INTO applications VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))", apps)

    # 9. Interview Rounds (35 comprehensive interview evaluations)
    rounds = [
        (1, 1, 1, 'Online Coding Assessment', '2026-09-08 10:00:00', 95.0, 'Optimal DP approach and clean logic.', 'PASSED', 2),
        (2, 1, 2, 'Data Structures & Algorithms', '2026-09-12 14:00:00', 92.5, 'Expert tree and graph traversal solutions.', 'PASSED', 2),
        (3, 1, 3, 'System Design & Googliness', '2026-09-16 16:00:00', 90.0, 'Scalable architecture and strong cultural fit.', 'PASSED', 2),
        (4, 2, 1, 'Online Coding Assessment', '2026-09-08 10:00:00', 98.0, '100% test cases cleared in 25 minutes.', 'PASSED', 2),
        (5, 2, 2, 'DSA & Graph Algorithms', '2026-09-12 15:00:00', 94.0, 'Excellent code optimization and time complexity.', 'PASSED', 2),
        (6, 4, 1, 'Atlassian Coding Challenge', '2026-09-09 10:00:00', 96.0, 'Clean OOP design and test-driven development.', 'PASSED', 16),
        (7, 4, 2, 'Systems & Concurrency Round', '2026-09-14 11:00:00', 93.5, 'Understood race conditions, locks, and thread safety.', 'PASSED', 16),
        (8, 4, 3, 'Values & Leadership Fit', '2026-09-18 15:00:00', 95.0, 'Outstanding team collaboration mindset.', 'PASSED', 16),
        (9, 5, 1, 'Atlassian Coding Challenge', '2026-09-09 10:00:00', 97.5, 'Highest score in campus batch.', 'PASSED', 16),
        (10, 5, 2, 'Systems Architecture', '2026-09-14 14:00:00', 91.0, 'Impressive knowledge of microservices and caching.', 'PASSED', 16),
        (11, 12, 1, 'Goldman Quantitative Math & Logic', '2026-09-10 10:00:00', 94.0, 'Exceptional probability and combinatorics mastery.', 'PASSED', 8),
        (12, 12, 2, 'Data Structures & High Frequency Tech', '2026-09-15 14:00:00', 92.0, 'Rapid algorithm implementation.', 'PASSED', 8),
        (13, 13, 1, 'Goldman Quantitative Math & Logic', '2026-09-10 10:00:00', 91.5, 'Quick mental calculations and clean code.', 'PASSED', 8),
        (14, 14, 1, 'Adobe Creative Algorithms Test', '2026-09-11 11:00:00', 90.0, 'Strong 2D matrix transformations and geometry logic.', 'PASSED', 9),
        (15, 14, 2, 'C++ Performance & Memory', '2026-09-16 11:30:00', 88.5, 'Solid grasp of pointers, move semantics, and cache lines.', 'PASSED', 9),
        (16, 15, 1, 'NVIDIA CUDA & Systems Assessment', '2026-09-12 10:00:00', 95.0, 'Outstanding understanding of GPU threads and memory.', 'PASSED', 10),
        (17, 15, 2, 'Computer Architecture & OOPS', '2026-09-17 14:00:00', 92.0, 'Deep understanding of pipelining and SIMD registers.', 'PASSED', 10),
        (18, 19, 1, 'Qualcomm Digital Electronics & Verilog', '2026-09-14 10:00:00', 93.0, 'Flawless FSM design and setup/hold time analysis.', 'PASSED', 12),
        (19, 19, 2, 'VLSI Architecture Interview', '2026-09-19 11:00:00', 91.0, 'Strong grasp of static timing analysis and CMOS.', 'PASSED', 12),
        (20, 22, 1, 'TI Analog Circuit Design Test', '2026-09-15 10:00:00', 94.5, 'Excellent small-signal analysis and bode plots.', 'PASSED', 13),
        (21, 22, 2, 'Op-Amp & Filter Design Round', '2026-09-20 11:30:00', 90.5, 'Accurate noise analysis and feedback stability design.', 'PASSED', 13),
        (22, 25, 1, 'JPMorgan Tech Assessment', '2026-09-16 10:00:00', 89.0, 'Solved both coding problems in 40 minutes.', 'PASSED', 17),
        (23, 25, 2, 'Distributed Systems & Cloud', '2026-09-21 14:00:00', 87.0, 'Understood eventual consistency and message queues.', 'PASSED', 17),
        (24, 33, 1, 'Tata Motors Mechanical Core Test', '2026-09-18 10:00:00', 88.0, 'Strong thermodynamics and EV powertrain physics.', 'PASSED', 14),
        (25, 33, 2, 'Thermal & Battery Management Interview', '2026-09-23 11:00:00', 86.5, 'Good conceptual clarity on lithium-ion cooling cycles.', 'PASSED', 14),
        (26, 36, 1, 'LTTS Industrial Automation Test', '2026-09-19 10:00:00', 85.0, 'Strong ladder logic and robotics kinematics concepts.', 'PASSED', 15),
        (27, 38, 1, 'TCS National Qualifier Test (NQT)', '2026-09-20 10:00:00', 91.0, 'Cleared cut-off with 95 percentile score.', 'PASSED', 5),
        (28, 42, 1, 'Infosys SP HackWithInfy Final', '2026-09-21 10:00:00', 92.5, 'Solved dynamic programming problem with optimal space.', 'PASSED', 6),
        (29, 45, 1, 'TCS Ninja Aptitude & Basic Coding', '2026-09-22 10:00:00', 78.0, 'Cleared foundational cut-offs.', 'PASSED', 5),
        (30, 51, 1, 'Online Technical Test', '2026-09-24 10:00:00', 84.0, 'Cleared OA with strong code efficiency.', 'PASSED', 2),
        (31, 52, 1, 'Technical Round 1', '2026-09-24 11:30:00', 82.5, 'Good problem solving in binary search.', 'PASSED', 3),
        (32, 53, 1, 'Digital Design Screening', '2026-09-24 14:00:00', 81.0, 'Cleared basic gate-level optimization.', 'PASSED', 12),
        (33, 54, 1, 'Mechanical Design Screening', '2026-09-24 15:30:00', 80.0, 'Good CAD and material science score.', 'PASSED', 14),
        (34, 59, 1, 'Online Assessment', '2026-09-25 10:00:00', 48.0, 'Failed time complexity constraints in graph problem.', 'FAILED', 3),
        (35, 60, 1, 'Online Coding Test', '2026-09-25 11:30:00', 51.0, 'Unable to pass dynamic programming test cases.', 'FAILED', 4)
    ]
    cur.executemany("INSERT INTO interview_rounds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", rounds)

    # 10. Placement Offers (32 offers representing authentic college placement tiers)
    offers = [
        # Super Dream (30 - 36 LPA)
        (1, 4, 36.00, '2026-09-20', '2025-07-01', 'ACCEPTED'), # Riya Sen -> Atlassian (36 LPA)
        (2, 5, 36.00, '2026-09-20', '2025-07-01', 'ACCEPTED'), # Amit Patel -> Atlassian (36 LPA)
        (3, 12, 30.00, '2026-09-21', '2025-07-15', 'ACCEPTED'),# Ananya -> Goldman Sachs (30 LPA)
        (4, 13, 30.00, '2026-09-21', '2025-07-15', 'ACCEPTED'),# Harshit -> Goldman Sachs (30 LPA)
        # Dream Tech (20 - 28.5 LPA)
        (5, 1, 28.50, '2026-09-22', '2025-07-01', 'ACCEPTED'),  # Rahul -> Google (28.5 LPA)
        (6, 2, 28.50, '2026-09-22', '2025-07-01', 'ACCEPTED'),  # Priya -> Google (28.5 LPA)
        (7, 3, 28.50, '2026-09-22', '2025-07-01', 'ACCEPTED'),  # Ayush -> Google (28.5 LPA)
        (8, 14, 26.00, '2026-09-23', '2025-07-10', 'ACCEPTED'), # Karthik -> Adobe (26 LPA)
        (9, 15, 25.00, '2026-09-23', '2025-07-15', 'ACCEPTED'), # Mayank -> NVIDIA (25 LPA)
        (10, 16, 25.00, '2026-09-23', '2025-07-15', 'ACCEPTED'),# Divya -> NVIDIA (25 LPA)
        (11, 6, 24.00, '2026-09-24', '2025-07-15', 'DECLINED'), # Rahul -> Microsoft (Declined for Google)
        (12, 7, 24.00, '2026-09-24', '2025-07-15', 'ACCEPTED'), # Sneha -> Microsoft (24 LPA)
        (13, 8, 24.00, '2026-09-24', '2025-07-15', 'ACCEPTED'), # Manav -> Microsoft (24 LPA)
        (14, 9, 24.00, '2026-09-24', '2025-07-15', 'ACCEPTED'), # Deepika -> Microsoft (24 LPA)
        (15, 10, 22.00, '2026-09-25', '2025-08-01', 'ACCEPTED'),# Rohan -> Amazon (22 LPA)
        (16, 11, 22.00, '2026-09-25', '2025-08-01', 'ACCEPTED'),# Swati -> Amazon (22 LPA)
        # Core Semiconductor & VLSI (21 - 22.5 LPA)
        (17, 22, 22.50, '2026-09-25', '2025-07-15', 'ACCEPTED'),# Prerna -> TI (22.5 LPA)
        (18, 23, 22.50, '2026-09-25', '2025-07-15', 'ACCEPTED'),# Aishwarya -> TI (22.5 LPA)
        (19, 19, 21.00, '2026-09-26', '2025-08-01', 'DECLINED'),# Deepika -> Qualcomm (Declined for Microsoft)
        (20, 20, 21.00, '2026-09-26', '2025-08-01', 'DECLINED'),# Mayank -> Qualcomm (Declined for NVIDIA)
        (21, 21, 21.00, '2026-09-26', '2025-08-01', 'ACCEPTED'),# Saurabh -> Qualcomm (21 LPA)
        # Networking & FinTech (18.5 - 19 LPA)
        (22, 17, 18.50, '2026-09-27', '2025-08-01', 'ACCEPTED'),# Yash -> Cisco (18.5 LPA)
        (23, 25, 19.00, '2026-09-27', '2025-07-20', 'ACCEPTED'),# Aditya -> JPMorgan (19 LPA)
        (24, 26, 19.00, '2026-09-27', '2025-07-20', 'ACCEPTED'),# Kunal -> JPMorgan (19 LPA)
        (25, 27, 19.00, '2026-09-27', '2025-07-20', 'ACCEPTED'),# Pallavi -> JPMorgan (19 LPA)
        # Core Auto & Industrial (7.8 - 9.5 LPA)
        (26, 33, 9.50, '2026-09-28', '2025-08-15', 'ACCEPTED'), # Bhavesh -> Tata Motors (9.5 LPA)
        (27, 34, 9.50, '2026-09-28', '2025-08-15', 'ACCEPTED'), # Vikas -> Tata Motors (9.5 LPA)
        (28, 35, 9.50, '2026-09-28', '2025-08-15', 'ACCEPTED'), # Tarun -> Tata Motors (9.5 LPA)
        (29, 36, 7.80, '2026-09-29', '2025-08-15', 'ACCEPTED'), # Ritika -> LTTS (7.8 LPA)
        (30, 37, 7.80, '2026-09-29', '2025-08-15', 'ACCEPTED'), # Ankit -> LTTS (7.8 LPA)
        # Consulting, Digital & Mass Offers (3.8 - 9.5 LPA)
        (31, 28, 8.50, '2026-09-30', '2025-08-01', 'ACCEPTED'), # Meera -> Deloitte (8.5 LPA)
        (32, 29, 8.50, '2026-09-30', '2025-08-01', 'ACCEPTED'), # Neha -> Deloitte (8.5 LPA)
        (33, 31, 7.00, '2026-09-30', '2025-08-01', 'DECLINED'), # Bhavesh -> Deloitte Core (Declined for Tata Motors)
        (34, 32, 7.00, '2026-09-30', '2025-08-01', 'ACCEPTED'), # Sakshi -> Deloitte Core (7 LPA)
        (35, 38, 7.50, '2026-10-01', '2025-08-01', 'ACCEPTED'), # Tanmay -> TCS Digital (7.5 LPA)
        (36, 39, 7.50, '2026-10-01', '2025-08-01', 'ACCEPTED'), # Abhishek -> TCS Digital (7.5 LPA)
        (37, 40, 7.50, '2026-10-01', '2025-08-01', 'ACCEPTED'), # Komal -> TCS Digital (7.5 LPA)
        (38, 42, 9.50, '2026-10-02', '2025-07-20', 'ACCEPTED'), # Pooja H -> Infosys SP (9.5 LPA)
        (39, 43, 9.50, '2026-10-02', '2025-07-20', 'ACCEPTED'), # Simran -> Infosys SP (9.5 LPA)
        (40, 44, 9.50, '2026-10-02', '2025-07-20', 'OFFERED'),  # Chirag -> Infosys SP (9.5 LPA) - Active Offer
        (41, 45, 3.80, '2026-10-03', '2025-09-01', 'ACCEPTED'), # Varun -> TCS Ninja (3.8 LPA)
        (42, 46, 3.80, '2026-10-03', '2025-09-01', 'ACCEPTED'), # Muskan -> TCS Ninja (3.8 LPA)
        (43, 47, 3.80, '2026-10-03', '2025-09-01', 'ACCEPTED'), # Tushar -> TCS Ninja (3.8 LPA)
        (44, 48, 3.80, '2026-10-03', '2025-09-01', 'OFFERED')   # Shruti -> TCS Ninja (3.8 LPA) - Active Offer
    ]
    cur.executemany("INSERT INTO placement_offers VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))", offers)

    # 11. Audit Logs (Rich historical events)
    audit = [
        (1, 1, 'CREATE_DATABASE', 'SYSTEM', None, 'Campus placement database initialized for 2024-2025 academic recruitment cycle.', '2026-08-15 09:00:00'),
        (2, 1, 'POST_JOB_DRIVE', 'JOB_OPENING', 4, 'Published marquee recruitment drive: Atlassian Associate Software Engineer (36.00 LPA).', '2026-08-20 10:00:00'),
        (3, 1, 'POST_JOB_DRIVE', 'JOB_OPENING', 1, 'Published recruitment drive: Google India Software Engineer (28.50 LPA).', '2026-08-20 11:00:00'),
        (4, 1, 'POST_JOB_DRIVE', 'JOB_OPENING', 5, 'Published recruitment drive: Goldman Sachs Quantitative FinTech SDE (30.00 LPA).', '2026-08-20 12:00:00'),
        (5, 101, 'NEW_APPLICATION_SUBMITTED', 'APPLICATION', 1, 'Student ID 1 (Rahul Verma) applied for Google India.', '2026-09-01 10:00:00'),
        (6, 115, 'NEW_APPLICATION_SUBMITTED', 'APPLICATION', 4, 'Student ID 15 (Riya Sen) applied for Atlassian.', '2026-09-02 09:00:00'),
        (7, 16, 'RECORD_INTERVIEW_RESULT', 'INTERVIEW_ROUND', 8, 'Sophie Taylor marked Round 3 as PASSED for Riya Sen.', '2026-09-18 15:00:00'),
        (8, 16, 'GENERATE_OFFER', 'PLACEMENT_OFFER', 1, 'Sophie Taylor rolled out 36.00 LPA offer to Riya Sen.', '2026-09-20 10:00:00'),
        (9, 115, 'PLACEMENT_OFFER_ACCEPTED', 'PLACEMENT_OFFER', 1, 'Offer ID 1 accepted. Package: 36.00 LPA. Application status updated to SELECTED.', '2026-09-20 12:00:00'),
        (10, 2, 'GENERATE_OFFER', 'PLACEMENT_OFFER', 5, 'Sarah Jenkins rolled out 28.50 LPA offer to Rahul Verma.', '2026-09-22 10:00:00'),
        (11, 101, 'PLACEMENT_OFFER_ACCEPTED', 'PLACEMENT_OFFER', 5, 'Offer ID 5 accepted. Package: 28.50 LPA. Application status updated to SELECTED.', '2026-09-22 11:00:00')
    ]
    cur.executemany("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?, ?, ?)", audit)


def build_college_level_data():
    conn = database.get_db_connection()
    cur = conn.cursor()

    # Drop all triggers first so seeding doesn't cascade
    cur.execute("DROP TRIGGER IF EXISTS trg_after_application_insert;")
    cur.execute("DROP TRIGGER IF EXISTS trg_after_offer_update;")

    # Clear existing data cleanly in reverse foreign-key order
    cur.execute("DELETE FROM audit_logs;")
    cur.execute("DELETE FROM placement_offers;")
    cur.execute("DELETE FROM interview_rounds;")
    cur.execute("DELETE FROM applications;")
    cur.execute("DELETE FROM job_eligibility_departments;")
    cur.execute("DELETE FROM job_openings;")
    cur.execute("DELETE FROM recruiters;")
    cur.execute("DELETE FROM companies;")
    cur.execute("DELETE FROM students;")
    cur.execute("DELETE FROM users;")
    cur.execute("DELETE FROM departments;")

    seed_college_dataset(cur)

    # Recreate Triggers
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
    print("College-Level Dataset Generation Complete!")

if __name__ == '__main__':
    build_college_level_data()

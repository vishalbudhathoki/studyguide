#!/usr/bin/env python3
"""
================================================================================
🎓 DBMS INTERACTIVE EXAM SIMULATOR & PRACTICAL CODING SUITE
================================================================================
Target: Full Score in University, College & Technical Competitive Examinations.
Standard Library Only: sqlite3, sys, random, os, time, textwrap.
Zero external pip dependencies required.

Features:
 [1] Practice MCQs (Randomized question bank, immediate feedback, score report)
 [2] Interactive SQL Coding Challenges & Sandbox (In-memory SQLite engine)
 [3] Rapid Fire Key Terms & Differences Quiz (Exam flashcard drills)
================================================================================
"""

import sqlite3
import sys
import random
import os
import time
import textwrap

# ==============================================================================
# COLOR & TERMINAL UI UTILITIES
# ==============================================================================
IS_WINDOWS = os.name == 'nt'

# Enable virtual terminal processing on Windows if possible
if IS_WINDOWS:
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        HAS_COLOR = True
    except Exception:
        HAS_COLOR = True
else:
    HAS_COLOR = True

class Color:
    RESET   = "\033[0m"  if HAS_COLOR else ""
    BOLD    = "\033[1m"  if HAS_COLOR else ""
    DIM     = "\033[2m"  if HAS_COLOR else ""
    RED     = "\033[91m" if HAS_COLOR else ""
    GREEN   = "\033[92m" if HAS_COLOR else ""
    YELLOW  = "\033[93m" if HAS_COLOR else ""
    BLUE    = "\033[94m" if HAS_COLOR else ""
    MAGENTA = "\033[95m" if HAS_COLOR else ""
    CYAN    = "\033[96m" if HAS_COLOR else ""
    WHITE   = "\033[97m" if HAS_COLOR else ""

def clear_screen():
    # Keep output visible in non-interactive terminals, or clear if interactive
    if sys.stdout.isatty():
        os.system('cls' if IS_WINDOWS else 'clear')

def banner(title, subtitle=""):
    width = 78
    print(f"\n{Color.CYAN}{'=' * width}{Color.RESET}")
    print(f"{Color.BOLD}{Color.WHITE} {title.center(width - 2)} {Color.RESET}")
    if subtitle:
        print(f"{Color.DIM}{subtitle.center(width)}{Color.RESET}")
    print(f"{Color.CYAN}{'=' * width}{Color.RESET}\n")

def section_box(title):
    print(f"\n{Color.MAGENTA}┌{'─' * 76}┐{Color.RESET}")
    print(f"{Color.MAGENTA}│{Color.BOLD}{Color.YELLOW} {title.ljust(74)} {Color.MAGENTA}│{Color.RESET}")
    print(f"{Color.MAGENTA}└{'─' * 76}┘{Color.RESET}")

def print_table(headers, rows):
    """Renders a clean ASCII table."""
    if not headers and not rows:
        print(f"    {Color.DIM}[Empty Result Set - 0 Rows]{Color.RESET}")
        return

    col_names = [str(h) for h in headers]
    col_widths = [len(h) for h in col_names]
    
    # Calculate widths
    formatted_rows = []
    for row in rows:
        formatted_row = [str(val if val is not None else "NULL") for val in row]
        formatted_rows.append(formatted_row)
        for i, val_str in enumerate(formatted_row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(val_str))
            else:
                col_widths.append(len(val_str))

    sep = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    print("    " + sep)
    header_line = "|" + "|".join([f" {col_names[i].ljust(col_widths[i])} " for i in range(len(col_names))]) + "|"
    print("    " + Color.BOLD + header_line + Color.RESET)
    print("    " + sep)
    for r in formatted_rows:
        row_str = "|" + "|".join([f" {r[i].ljust(col_widths[i])} " for i in range(len(r))]) + "|"
        print("    " + row_str)
    print("    " + sep)
    print(f"    {Color.DIM}Total rows: {len(rows)}{Color.RESET}")

def wait_for_enter(prompt="Press [Enter] to continue..."):
    try:
        input(f"\n{Color.DIM}{prompt}{Color.RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

# ==============================================================================
# SECTION 1: COMPREHENSIVE MCQ BANK & ENGINE
# ==============================================================================
MCQ_BANK = [
    {
        "id": 1,
        "topic": "File Systems vs DBMS",
        "question": "Which of the following is a major limitation of traditional File Processing Systems compared to a DBMS?",
        "options": [
            "File systems cannot store structured data at all.",
            "File systems cause data redundancy leading to data inconsistency.",
            "File systems cannot be stored on persistent secondary storage.",
            "File systems use SQL which is slower than declarative code."
        ],
        "answer": 1, # B
        "explanation": "In traditional file systems, data is duplicated across independent department files without centralized coordination. Modifying one copy leaves others stale, causing data inconsistency."
    },
    {
        "id": 2,
        "topic": "ACID Properties",
        "question": "Which ACID property guarantees that once a transaction is committed, its modifications will permanently survive system crashes or power failures?",
        "options": [
            "Atomicity",
            "Consistency",
            "Isolation",
            "Durability"
        ],
        "answer": 3, # D
        "explanation": "Durability guarantees that committed data is written to non-volatile storage (WAL/redo logs) and persists across system restarts or hardware failures."
    },
    {
        "id": 3,
        "topic": "ANSI-SPARC Architecture",
        "question": "The ability to alter the internal (physical) storage layout or create new index structures without altering the conceptual schema is known as:",
        "options": [
            "Logical Data Independence",
            "Physical Data Independence",
            "View Level Independence",
            "Referential Transparency"
        ],
        "answer": 1, # B
        "explanation": "Physical Data Independence decouples the physical storage structures (internal level) from the logical/conceptual schema. Adding B-Trees or changing disk partitions requires no conceptual alterations."
    },
    {
        "id": 4,
        "topic": "Schema vs Instance",
        "question": "In database terminology, the overall design and structure of the database (which changes very infrequently) is called the __________, while the actual data stored at a specific moment is called the __________.",
        "options": [
            "Instance; Schema",
            "Extension; Intension",
            "Schema (Intension); Instance (Extension)",
            "System Catalog; Metadata"
        ],
        "answer": 2, # C
        "explanation": "Schema (Intension) represents the design/blueprint; Instance (Extension) represents the actual snapshot of records at a given point in time."
    },
    {
        "id": 5,
        "topic": "Keys Classification",
        "question": "A Candidate Key is defined as:",
        "options": [
            "Any attribute that can take NULL values.",
            "A minimal Super Key that uniquely identifies tuples in a relation.",
            "A foreign key that references another candidate key.",
            "A key automatically generated by the database sequence engine."
        ],
        "answer": 1, # B
        "explanation": "A Candidate Key is a minimal super key: it possesses the uniqueness property, and no proper subset of its attributes can uniquely identify tuples."
    },
    {
        "id": 6,
        "topic": "ER Modeling",
        "question": "In an Entity-Relationship (ER) diagram, how is a MULTIVALUED attribute (such as multiple phone numbers) standardly represented?",
        "options": [
            "A dashed oval",
            "A double oval",
            "A diamond inside a rectangle",
            "A double rectangle"
        ],
        "answer": 1, # B
        "explanation": "In Chen's notation: Double Oval = Multivalued attribute, Dashed Oval = Derived attribute, Double Rectangle = Weak entity, Double Diamond = Identifying relationship."
    },
    {
        "id": 7,
        "topic": "Relational Integrity",
        "question": "Entity Integrity Constraint mandates that:",
        "options": [
            "Foreign keys must never reference deleted primary keys.",
            "No primary key value (or component of a composite primary key) can be NULL.",
            "All column values must fall strictly within their predefined data types.",
            "A table cannot have more than 10 candidate keys."
        ],
        "answer": 1, # B
        "explanation": "Entity Integrity states that primary keys serve as unique tuple identifiers; allowing NULL would violate the ability to identify that entity instance."
    },
    {
        "id": 8,
        "topic": "Relational Algebra",
        "question": "Which of the following Relational Algebra operations is NOT a fundamental (primitive) operator?",
        "options": [
            "Selection (σ)",
            "Projection (π)",
            "Cartesian Product (×)",
            "Natural Join (⋈)"
        ],
        "answer": 3, # D
        "explanation": "The 5 fundamental operators are: Selection (σ), Projection (π), Cartesian Product (×), Set Union (∪), and Set Difference (−). Join is a derived operator: R ⋈ S = σ_condition(R × S)."
    },
    {
        "id": 9,
        "topic": "SQL DDL vs DML",
        "question": "Which of the following SQL statements belongs strictly to DDL (Data Definition Language)?",
        "options": [
            "INSERT INTO Students VALUES (1, 'Alice');",
            "ALTER TABLE Students ADD COLUMN email VARCHAR(100);",
            "UPDATE Students SET cgpa = 3.9 WHERE student_id = 1;",
            "SELECT * FROM Students;"
        ],
        "answer": 1, # B
        "explanation": "ALTER TABLE modifies the table's schema (DDL). INSERT and UPDATE are DML (Data Manipulation Language); SELECT is DQL."
    },
    {
        "id": 10,
        "topic": "SQL Filtering with NULL",
        "question": "What will be the result of evaluating: `SELECT * FROM Employees WHERE bonus = NULL;`?",
        "options": [
            "All rows where bonus has a NULL value.",
            "A SQL compilation error.",
            "An empty result set (0 rows), because comparison with NULL using '=' yields UNKNOWN (Falsy).",
            "All rows where bonus is 0 or NULL."
        ],
        "answer": 2, # C
        "explanation": "In SQL three-valued logic, `col = NULL` evaluates to UNKNOWN. WHERE filters require TRUE to include a row. Thus, it returns 0 rows. The correct syntax is `IS NULL`."
    },
    {
        "id": 11,
        "topic": "GROUP BY and HAVING",
        "question": "Which statement accurately describes the difference between WHERE and HAVING in SQL?",
        "options": [
            "WHERE can filter aggregate functions, whereas HAVING cannot.",
            "WHERE filters rows BEFORE grouping occurs; HAVING filters grouped summaries AFTER grouping.",
            "HAVING is executed before the FROM clause.",
            "WHERE is mandatory whenever GROUP BY is specified."
        ],
        "answer": 1, # B
        "explanation": "WHERE filters individual candidate tuples before grouping; HAVING applies predicate conditions to the aggregated groups formed by GROUP BY."
    },
    {
        "id": 12,
        "topic": "SQL Joins",
        "question": "In a LEFT OUTER JOIN `A LEFT JOIN B ON A.id = B.id`, what happens to records in table A that have no matching records in table B?",
        "options": [
            "They are completely excluded from the result set.",
            "They are included, with NULL filled in for all columns originating from table B.",
            "The query terminates with a referential integrity error.",
            "They are matched with the first available record of table B."
        ],
        "answer": 1, # B
        "explanation": "A LEFT JOIN preserves every row from the left table (A). If no match exists in B, B's columns evaluate to NULL."
    },
    {
        "id": 13,
        "topic": "Subqueries & NOT IN",
        "question": "Suppose table `Audit` contains rows with IDs {1, 2, NULL}. What is returned by: `SELECT * FROM Users WHERE user_id NOT IN (SELECT id FROM Audit);`?",
        "options": [
            "Users whose user_id is not 1 and not 2.",
            "All users because NULL is disregarded.",
            "Zero rows (Empty set), because `user_id <> NULL` evaluates to UNKNOWN.",
            "A runtime syntax exception."
        ],
        "answer": 2, # C
        "explanation": "The 'NOT IN NULL trap': `x NOT IN (1, 2, NULL)` expands to `x <> 1 AND x <> 2 AND x <> NULL`. Since `x <> NULL` is UNKNOWN, the entire conjunct is UNKNOWN/FALSE, returning 0 rows!"
    },
    {
        "id": 14,
        "topic": "Correlated Subqueries",
        "question": "Why is a correlated subquery generally slower than an uncorrelated subquery?",
        "options": [
            "Because it cannot use indexes.",
            "Because it references columns from the outer query and must re-execute for every candidate row evaluated by the outer query.",
            "Because it can only execute on primary key attributes.",
            "Because it requires creating temporary disk tables on each invocation."
        ],
        "answer": 1, # B
        "explanation": "A correlated subquery has a dependency on outer query columns; hence the database engine logically executes it once per outer row unless optimized by decorrelation."
    },
    {
        "id": 15,
        "topic": "Set Operations",
        "question": "What is the primary difference between `UNION` and `UNION ALL` in SQL?",
        "options": [
            "UNION operates on tables with different column counts, while UNION ALL requires exact counts.",
            "UNION eliminates duplicate rows via sorting/hashing; UNION ALL retains all duplicates and is faster.",
            "UNION preserves duplicates, whereas UNION ALL removes them.",
            "UNION ALL can only be applied to numerical data types."
        ],
        "answer": 1, # B
        "explanation": "UNION filters out identical duplicate rows between the sets, requiring sorting overhead. UNION ALL simply concatenates the two streams directly."
    },
    {
        "id": 16,
        "topic": "Relational Division",
        "question": "Which real-world query scenario corresponds directly to the Relational Division (÷) operator?",
        "options": [
            "Find employees earning more than the average salary.",
            "Find students who have enrolled in ALL mandatory courses in a curriculum.",
            "Calculate the total salary spent per department.",
            "Find customers with duplicate email addresses."
        ],
        "answer": 1, # B
        "explanation": "Relational division corresponds to universal quantification (the 'FOR ALL' condition): finding entities associated with ALL elements of a given target relation."
    },
    {
        "id": 17,
        "topic": "DROP vs TRUNCATE vs DELETE",
        "question": "Which of the following commands removes ALL rows from a table, does NOT log individual row deletions, cannot be rolled back in some RDBMS, and resets identity seeds?",
        "options": [
            "DELETE FROM table_name;",
            "TRUNCATE TABLE table_name;",
            "DROP TABLE table_name;",
            "ALTER TABLE table_name CLEAR;"
        ],
        "answer": 1, # B
        "explanation": "TRUNCATE TABLE is a DDL operation that deallocates data pages directly. It removes all rows much faster than DELETE and resets counters, while DROP deletes the schema itself."
    },
    {
        "id": 18,
        "topic": "ER to Relational Mapping",
        "question": "When converting a 1:N (One-to-Many) relationship between Departments (1) and Employees (N) into a relational schema, where should the Foreign Key be placed?",
        "options": [
            "In the Departments table, referencing Employees.",
            "In the Employees table, referencing Departments.",
            "In a mandatory 3rd bridge table, regardless of constraints.",
            "In both tables simultaneously."
        ],
        "answer": 1, # B
        "explanation": "In 1:N relationships, the primary key of the '1' side (Departments) is placed as a Foreign Key in the 'N' side (Employees), avoiding multi-valued attributes and NULL clutter."
    },
    {
        "id": 19,
        "topic": "Data Control Language",
        "question": "Which SQL statement is used to revoke previously granted database privileges from a user?",
        "options": [
            "REMOVE SELECT ON Students FROM user1;",
            "DENY SELECT ON Students TO user1;",
            "REVOKE SELECT ON Students FROM user1;",
            "DROP PRIVILEGE SELECT ON Students FROM user1;"
        ],
        "answer": 2, # C
        "explanation": "The standard DCL pair is GRANT <privileges> ON <object> TO <user> and REVOKE <privileges> ON <object> FROM <user>."
    },
    {
        "id": 20,
        "topic": "Aggregates and NULLs",
        "question": "If a column contains values {10, 20, NULL, 30}, what will `COUNT(column_name)` and `COUNT(*)` return respectively?",
        "options": [
            "4 and 4",
            "3 and 4",
            "3 and 3",
            "4 and 3"
        ],
        "answer": 1, # B
        "explanation": "`COUNT(column_name)` ignores NULL values and counts only valid non-null entries (3). `COUNT(*)` counts total rows in the relation regardless of nulls (4)."
    }
]

def run_mcq_session():
    clear_screen()
    banner("DBMS EXAM SIMULATOR: MULTIPLE CHOICE QUESTIONS", "Full Syllabus Comprehensive Testing Engine")
    
    print(f"{Color.BOLD}Select Quiz Mode:{Color.RESET}")
    print("  [1] Full Exam Simulation (20 Random Questions)")
    print("  [2] Quick Drill (5 Random Questions)")
    print("  [3] Comprehensive Master Review (All Questions in Bank)")
    print("  [0] Return to Main Menu")
    
    choice = input(f"\n{Color.YELLOW}Enter choice [0-3]: {Color.RESET}").strip()
    if choice == '0':
        return
    elif choice == '1':
        selected = random.sample(MCQ_BANK, min(20, len(MCQ_BANK)))
    elif choice == '2':
        selected = random.sample(MCQ_BANK, min(5, len(MCQ_BANK)))
    elif choice == '3':
        selected = list(MCQ_BANK)
        random.shuffle(selected)
    else:
        print(f"{Color.RED}Invalid choice. Defaulting to Quick Drill (5 questions).{Color.RESET}")
        selected = random.sample(MCQ_BANK, 5)

    score = 0
    total = len(selected)
    topic_stats = {}

    clear_screen()
    print(f"\n{Color.BOLD}{Color.GREEN}>>> Starting MCQ Session: {total} Questions Loaded. Good Luck! <<<{Color.RESET}\n")

    for i, q in enumerate(selected, 1):
        print(f"\n{Color.CYAN}─────────────────────────────────────────────────────────────────────────────{Color.RESET}")
        print(f"{Color.BOLD}Question {i} of {total} {Color.YELLOW}[Topic: {q['topic']}]{Color.RESET}")
        print(f"{Color.BOLD}{Color.WHITE}{q['question']}{Color.RESET}\n")
        
        # Format options
        opts = q['options']
        labels = ['A', 'B', 'C', 'D']
        for idx, opt in enumerate(opts):
            print(f"  {Color.BOLD}{labels[idx]}){Color.RESET} {opt}")
            
        user_ans = ""
        while True:
            try:
                user_ans = input(f"\n{Color.YELLOW}Your Answer (A/B/C/D or 'Q' to quit): {Color.RESET}").strip().upper()
            except (KeyboardInterrupt, EOFError):
                print("\nSession aborted.")
                return
            if user_ans in ['A', 'B', 'C', 'D', 'Q']:
                break
            print(f"{Color.RED}Please enter A, B, C, or D.{Color.RESET}")

        if user_ans == 'Q':
            print(f"\n{Color.YELLOW}Session ended early by user.{Color.RESET}")
            break

        user_idx = labels.index(user_ans)
        correct_idx = q['answer']
        topic = q['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}
        topic_stats[topic]["total"] += 1

        if user_idx == correct_idx:
            score += 1
            topic_stats[topic]["correct"] += 1
            print(f"\n{Color.GREEN}{Color.BOLD}✓ CORRECT!{Color.RESET} {Color.GREEN}Well done!{Color.RESET}")
        else:
            print(f"\n{Color.RED}{Color.BOLD}✗ INCORRECT!{Color.RESET}")
            print(f"  Your answer:    {Color.RED}{labels[user_idx]}) {opts[user_idx]}{Color.RESET}")
            print(f"  Correct answer: {Color.GREEN}{Color.BOLD}{labels[correct_idx]}) {opts[correct_idx]}{Color.RESET}")

        print(f"\n{Color.BOLD}💡 Concept Breakdown:{Color.RESET}")
        for line in textwrap.wrap(q['explanation'], width=72):
            print(f"  {Color.DIM}{line}{Color.RESET}")

        if i < total:
            wait_for_enter("Press [Enter] for next question...")
            clear_screen()

    # ================= SCORECARD REPORT =================
    clear_screen()
    banner("EXAM PERFORMANCE SCORE REPORT")
    pct = (score / total) * 100 if total > 0 else 0
    grade = "A+ (Outstanding)" if pct >= 90 else "A (Excellent)" if pct >= 80 else "B (Good)" if pct >= 70 else "C (Pass)" if pct >= 50 else "F (Needs Intensive Revision)"
    grade_color = Color.GREEN if pct >= 75 else Color.YELLOW if pct >= 50 else Color.RED

    print(f"  {Color.BOLD}Questions Attempted:{Color.RESET} {total}")
    print(f"  {Color.BOLD}Correct Answers:    {Color.RESET} {Color.GREEN}{score}{Color.RESET}")
    print(f"  {Color.BOLD}Accuracy Percentage:{Color.RESET} {grade_color}{pct:.1f}%{Color.RESET}")
    print(f"  {Color.BOLD}Assessment Grade:   {Color.RESET} {grade_color}{grade}{Color.RESET}\n")

    section_box("TOPIC-BY-TOPIC BREAKDOWN")
    for top, data in topic_stats.items():
        c = data["correct"]
        t = data["total"]
        p = (c / t) * 100
        bar = "█" * int(p / 10) + "░" * (10 - int(p / 10))
        status_color = Color.GREEN if p == 100 else Color.YELLOW if p >= 50 else Color.RED
        print(f"  • {top.ljust(25)} : {c}/{t} ({status_color}{p:5.1f}%{Color.RESET}) [{status_color}{bar}{Color.RESET}]")

    wait_for_enter("Press [Enter] to return to Main Menu...")

# ==============================================================================
# SECTION 2: INTERACTIVE SQL CODING CHALLENGES & SANDBOX
# ==============================================================================
CHALLENGE_CATALOG = [
    {
        "id": 1,
        "title": "Above-Average Salary Earners (Scalar Subquery)",
        "difficulty": "⭐ Medium",
        "description": "Find all employees whose salary is strictly greater than the overall company average salary.\nDisplay: name, department, salary.\nOrder by salary descending.",
        "setup_sql": """
            DROP TABLE IF EXISTS Employees;
            CREATE TABLE Employees (
                emp_id INT PRIMARY KEY,
                name VARCHAR(50),
                department VARCHAR(50),
                salary DECIMAL(10, 2)
            );
            INSERT INTO Employees VALUES
            (1, 'Alice', 'Engineering', 95000.00),
            (2, 'Bob', 'Engineering', 80000.00),
            (3, 'Charlie', 'Marketing', 60000.00),
            (4, 'Diana', 'Marketing', 55000.00),
            (5, 'Evan', 'HR', 50000.00),
            (6, 'Fiona', 'Engineering', 105000.00);
        """,
        "solution_sql": """
            SELECT name, department, salary
            FROM Employees
            WHERE salary > (SELECT AVG(salary) FROM Employees)
            ORDER BY salary DESC;
        """,
        "hint": "Use a scalar subquery `WHERE salary > (SELECT AVG(salary) FROM Employees)`."
    },
    {
        "id": 2,
        "title": "Department Payroll & Headcount (GROUP BY & HAVING)",
        "difficulty": "⭐ Medium",
        "description": "Find departments that have at least 2 employees and whose average salary is strictly greater than 70,000.\nDisplay: department, headcount (COUNT(*)), and avg_salary (rounded to 2 decimals).\nOrder by avg_salary descending.",
        "setup_sql": """
            DROP TABLE IF EXISTS Employees;
            CREATE TABLE Employees (
                emp_id INT PRIMARY KEY,
                name VARCHAR(50),
                department VARCHAR(50),
                salary DECIMAL(10, 2)
            );
            INSERT INTO Employees VALUES
            (1, 'Alice', 'Engineering', 95000.00),
            (2, 'Bob', 'Engineering', 85000.00),
            (3, 'Charlie', 'Finance', 75000.00),
            (4, 'Diana', 'Finance', 71000.00),
            (5, 'Evan', 'HR', 45000.00),
            (6, 'Fred', 'HR', 48000.00),
            (7, 'George', 'Legal', 90000.00);
        """,
        "solution_sql": """
            SELECT department, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary
            FROM Employees
            GROUP BY department
            HAVING COUNT(*) >= 2 AND AVG(salary) > 70000.00
            ORDER BY avg_salary DESC;
        """,
        "hint": "Use `GROUP BY department HAVING COUNT(*) >= 2 AND AVG(salary) > 70000.00`."
    },
    {
        "id": 3,
        "title": "Unassigned Developers (LEFT OUTER JOIN / Anti-Join)",
        "difficulty": "⭐ Medium",
        "description": "Identify all developers who are currently NOT assigned to any project.\nDisplay: dev_id, dev_name.\nOrder by dev_id ascending.",
        "setup_sql": """
            DROP TABLE IF EXISTS Devs;
            DROP TABLE IF EXISTS Projects;
            DROP TABLE IF EXISTS Assignments;
            CREATE TABLE Devs (dev_id INT PRIMARY KEY, dev_name VARCHAR(50));
            CREATE TABLE Projects (proj_id INT PRIMARY KEY, proj_name VARCHAR(50));
            CREATE TABLE Assignments (dev_id INT, proj_id INT);
            INSERT INTO Devs VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana');
            INSERT INTO Projects VALUES (10, 'Cloud Migration'), (20, 'Mobile App');
            INSERT INTO Assignments VALUES (1, 10), (1, 20), (2, 10);
        """,
        "solution_sql": """
            SELECT d.dev_id, d.dev_name
            FROM Devs d
            LEFT JOIN Assignments a ON d.dev_id = a.dev_id
            WHERE a.dev_id IS NULL
            ORDER BY d.dev_id ASC;
        """,
        "hint": "Perform a LEFT JOIN between Devs and Assignments, then filter `WHERE a.dev_id IS NULL`."
    },
    {
        "id": 4,
        "title": "Employee-Manager Hierarchy (SELF JOIN)",
        "difficulty": "⭐⭐ Hard",
        "description": "Given a table of staff with manager_id referencing emp_id, list every employee's name along with their manager's name.\nIf an employee has no manager (the CEO), display 'TOP EXECUTIVE' as the manager's name.\nDisplay: employee_name, manager_name.\nOrder by employee_name ascending.",
        "setup_sql": """
            DROP TABLE IF EXISTS Staff;
            CREATE TABLE Staff (
                emp_id INT PRIMARY KEY,
                emp_name VARCHAR(50),
                manager_id INT
            );
            INSERT INTO Staff VALUES
            (1, 'Eleanor', NULL),
            (2, 'Michael', 1),
            (3, 'Tahani', 1),
            (4, 'Chidi', 2),
            (5, 'Jason', 3);
        """,
        "solution_sql": """
            SELECT 
                e.emp_name AS employee_name,
                COALESCE(m.emp_name, 'TOP EXECUTIVE') AS manager_name
            FROM Staff e
            LEFT JOIN Staff m ON e.manager_id = m.emp_id
            ORDER BY employee_name ASC;
        """,
        "hint": "Use a self `LEFT JOIN Staff m ON e.manager_id = m.emp_id` and `COALESCE(m.emp_name, 'TOP EXECUTIVE')`."
    },
    {
        "id": 5,
        "title": "The 2nd Highest Distinct Salary (Subqueries)",
        "difficulty": "⭐⭐ Hard",
        "description": "Find the 2nd highest distinct salary in the company without using LIMIT or OFFSET.\nDisplay column: second_highest_salary.",
        "setup_sql": """
            DROP TABLE IF EXISTS Salaries;
            CREATE TABLE Salaries (
                emp_id INT PRIMARY KEY,
                emp_name VARCHAR(50),
                salary DECIMAL(10, 2)
            );
            INSERT INTO Salaries VALUES
            (1, 'Alice', 95000.00),
            (2, 'Bob', 95000.00),
            (3, 'Charlie', 82000.00),
            (4, 'Diana', 70000.00),
            (5, 'Evan', 82000.00);
        """,
        "solution_sql": """
            SELECT MAX(salary) AS second_highest_salary
            FROM Salaries
            WHERE salary < (SELECT MAX(salary) FROM Salaries);
        """,
        "hint": "Filter salaries strictly less than the overall maximum: `WHERE salary < (SELECT MAX(salary) FROM Salaries)`."
    },
    {
        "id": 6,
        "title": "Skill Gap Analysis (INTERSECT & EXCEPT)",
        "difficulty": "⭐ Medium",
        "description": "Find candidates certified in 'SQL' but NOT in 'Python'.\nDisplay: candidate_name.\nOrder alphabetically.",
        "setup_sql": """
            DROP TABLE IF EXISTS Skills;
            CREATE TABLE Skills (candidate_name VARCHAR(50), skill_name VARCHAR(30));
            INSERT INTO Skills VALUES
            ('Alice', 'SQL'), ('Alice', 'Python'),
            ('Bob', 'SQL'), ('Bob', 'Java'),
            ('Charlie', 'Python'),
            ('Diana', 'SQL'), ('Diana', 'Python');
        """,
        "solution_sql": """
            SELECT candidate_name FROM Skills WHERE skill_name = 'SQL'
            EXCEPT
            SELECT candidate_name FROM Skills WHERE skill_name = 'Python'
            ORDER BY candidate_name;
        """,
        "hint": "Use the `EXCEPT` set operator between the SQL query and the Python query."
    }
]

def execute_user_query(conn, query_text):
    """Executes a query and returns (columns, rows, error_string)."""
    cur = conn.cursor()
    try:
        cur.execute(query_text)
        if cur.description:
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            return cols, rows, None
        else:
            conn.commit()
            return [], [], f"Statement executed. Rows affected: {cur.rowcount}"
    except Exception as e:
        return [], [], str(e)

def run_challenge_mode():
    clear_screen()
    banner("SQL CODING CHALLENGE MODE", "Practice Graded Exam Queries in SQLite Sandbox")
    
    print(f"{Color.BOLD}Select a Challenge to Solve:{Color.RESET}\n")
    for ch in CHALLENGE_CATALOG:
        print(f"  [{ch['id']}] {Color.BOLD}{ch['title']}{Color.RESET} ({ch['difficulty']})")
    print("  [0] Return to Main Menu\n")
    
    choice = input(f"{Color.YELLOW}Enter Challenge #[1-{len(CHALLENGE_CATALOG)}]: {Color.RESET}").strip()
    if choice == '0' or not choice.isdigit():
        return
    
    target_ch = next((c for c in CHALLENGE_CATALOG if c["id"] == int(choice)), None)
    if not target_ch:
        print(f"{Color.RED}Invalid challenge selection.{Color.RESET}")
        time.sleep(1)
        return

    # Set up in-memory DB
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(target_ch["setup_sql"])

    # Calculate expected result
    exp_cols, exp_rows, _ = execute_user_query(conn, target_ch["solution_sql"])

    while True:
        clear_screen()
        banner(f"CHALLENGE #{target_ch['id']}: {target_ch['title']}", target_ch['difficulty'])
        print(f"{Color.BOLD}📋 Problem Description:{Color.RESET}")
        for line in target_ch["description"].split("\n"):
            print(f"  {line}")
            
        print(f"\n{Color.BOLD}🎯 Expected Result:{Color.RESET}")
        print_table(exp_cols, exp_rows)

        print(f"\n{Color.BOLD}Actions:{Color.RESET}")
        print("  [1] Enter your SQL solution")
        print("  [2] View Hint")
        print("  [3] Reveal Model Solution Query & Explanation")
        print("  [0] Return to Challenge Menu")

        act = input(f"\n{Color.YELLOW}Select action [0-3]: {Color.RESET}").strip()
        if act == '0':
            break
        elif act == '2':
            print(f"\n{Color.YELLOW}💡 HINT:{Color.RESET} {target_ch['hint']}")
            wait_for_enter()
        elif act == '3':
            print(f"\n{Color.GREEN}⭐ OPTIMAL MODEL SQL SOLUTION:{Color.RESET}")
            print(f"{Color.CYAN}{target_ch['solution_sql'].strip()}{Color.RESET}\n")
            wait_for_enter()
        elif act == '1':
            print(f"\n{Color.CYAN}Enter your SQL query below.{Color.RESET}")
            print(f"{Color.DIM}(Tip: Type or paste your SQL. End with ';' or hit Enter on an empty line to run):{Color.RESET}")
            lines = []
            while True:
                try:
                    line = input(f"{Color.MAGENTA}SQL> {Color.RESET}" if not lines else f"{Color.MAGENTA}...> {Color.RESET}")
                except (KeyboardInterrupt, EOFError):
                    lines = []
                    break
                if not line.strip() and lines:
                    break
                lines.append(line)
                if line.strip().endswith(";"):
                    break
            
            user_sql = "\n".join(lines).strip()
            if not user_sql:
                continue

            # Run user query
            user_cols, user_rows, err = execute_user_query(conn, user_sql)
            
            print(f"\n{Color.BOLD}--- YOUR QUERY OUTPUT ---{Color.RESET}")
            if err and not user_cols:
                print(f"  {Color.RED}Query Execution Error: {err}{Color.RESET}")
            else:
                print_table(user_cols, user_rows)

                # Validate against expected
                # Normalize row data for comparison
                norm_user = [[str(x).strip() if x is not None else "NULL" for x in r] for r in user_rows]
                norm_exp = [[str(x).strip() if x is not None else "NULL" for x in r] for r in exp_rows]

                if norm_user == norm_exp:
                    print(f"\n{Color.GREEN}{Color.BOLD}🎉 CONGRATULATIONS! TEST PASSED!{Color.RESET}")
                    print(f"{Color.GREEN}Your query produced the exact expected output tuples!{Color.RESET}")
                else:
                    print(f"\n{Color.RED}{Color.BOLD}❌ TEST FAILED:{Color.RESET} Output mismatch.")
                    if len(norm_user) != len(norm_exp):
                        print(f"  Row count difference: Expected {len(norm_exp)}, got {len(norm_user)}.")
                    else:
                        print("  Row values or column order differ from the target output.")
            
            wait_for_enter()

def run_free_sandbox():
    clear_screen()
    banner("FREE SQL INTERACTIVE SANDBOX", "Pre-loaded with Departments, Employees, Projects & Students")
    
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # Pre-load full relational dataset
    conn.executescript("""
        CREATE TABLE Departments (
            dept_id INT PRIMARY KEY,
            dept_name VARCHAR(50) NOT NULL UNIQUE
        );
        INSERT INTO Departments VALUES (10, 'Engineering'), (20, 'Research'), (30, 'Sales'), (40, 'Executive');

        CREATE TABLE Employees (
            emp_id INT PRIMARY KEY,
            emp_name VARCHAR(50) NOT NULL,
            dept_id INT,
            salary DECIMAL(10,2),
            manager_id INT,
            FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
        );
        INSERT INTO Employees VALUES
        (1, 'Alice Vance', 10, 95000.00, NULL),
        (2, 'Bob Builder', 10, 80000.00, 1),
        (3, 'Charlie Day', 20, 75000.00, 1),
        (4, 'Diana Prince', 30, 62000.00, NULL),
        (5, 'Evan Wright', 30, 58000.00, 4),
        (6, 'Fiona Glen', 10, 105000.00, 1);

        CREATE TABLE Projects (
            proj_id INT PRIMARY KEY,
            proj_name VARCHAR(50)
        );
        INSERT INTO Projects VALUES (101, 'Apollo'), (102, 'Bifrost'), (103, 'Cerebro');

        CREATE TABLE Assignments (
            emp_id INT,
            proj_id INT,
            hours INT,
            PRIMARY KEY (emp_id, proj_id)
        );
        INSERT INTO Assignments VALUES (1, 101, 20), (1, 102, 15), (2, 101, 35), (3, 103, 40);
    """)

    print(f"{Color.GREEN}Pre-loaded Tables: Departments, Employees, Projects, Assignments.{Color.RESET}")
    print(f"{Color.DIM}Commands: '.tables' (show schema), '.sample <table>' (preview data), 'exit' (return to menu){Color.RESET}\n")

    while True:
        try:
            line = input(f"{Color.CYAN}sqlite> {Color.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not line:
            continue
        if line.lower() in ['exit', 'quit', 'exit;']:
            break
        if line.lower() == '.tables':
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tbls = [r[0] for r in cur.fetchall()]
            print(f"  {Color.BOLD}Tables in Sandbox:{Color.RESET} {', '.join(tbls)}")
            continue
        if line.lower().startswith('.sample'):
            parts = line.split()
            if len(parts) > 1:
                tname = parts[1]
                cols, rows, err = execute_user_query(conn, f"SELECT * FROM {tname} LIMIT 5;")
                if err:
                    print(f"  {Color.RED}{err}{Color.RESET}")
                else:
                    print_table(cols, rows)
            continue

        # Execute general SQL
        cols, rows, msg = execute_user_query(conn, line)
        if cols or rows:
            print_table(cols, rows)
        elif msg:
            if "Error" in msg or "error" in msg:
                print(f"  {Color.RED}[ERROR] {msg}{Color.RESET}")
            else:
                print(f"  {Color.GREEN}{msg}{Color.RESET}")

# ==============================================================================
# SECTION 3: RAPID FIRE KEY TERMS & DIFFERENCES QUIZ
# ==============================================================================
RAPID_FIRE_CONCEPTS = [
    {
        "term": "Physical vs Logical Data Independence",
        "question": "What is the critical distinction between Physical and Logical Data Independence in the ANSI-SPARC 3-Schema Architecture?",
        "points": [
            "Physical Data Independence: Modifying internal storage structures (indexes, file organization, partitions) WITHOUT changing the conceptual schema. (Easier to achieve).",
            "Logical Data Independence: Modifying the conceptual schema (adding/splitting entities or attributes) WITHOUT requiring changes to external schemas or user applications. (Harder to achieve).",
            "Exam Mnemonic: Physical = Hard drives & performance; Logical = Entities & business definitions."
        ]
    },
    {
        "term": "Primary Key vs Unique Key",
        "question": "How do PRIMARY KEY and UNIQUE constraints differ regarding NULL values and quantity per table?",
        "points": [
            "Quantity: A table can have ONLY ONE Primary Key, but MULTIPLE Unique keys.",
            "NULL Handling: Primary Key columns strictly forbid NULL values (Entity Integrity). Unique constraints allow NULL values (one or more depending on RDBMS dialect).",
            "Clustering: In many engines (e.g. MySQL InnoDB, SQL Server), the Primary Key creates a clustered index by default."
        ]
    },
    {
        "term": "Candidate Key vs Super Key",
        "question": "What mathematical relationship connects Candidate Keys and Super Keys?",
        "points": [
            "Super Key: Any set of attributes that uniquely identifies a tuple within a relation.",
            "Candidate Key: A MINIMAL Super Key. It contains no redundant attributes. Removing even one attribute destroys its uniqueness.",
            "Relationship: Every Candidate Key is a Super Key, but NOT every Super Key is a Candidate Key!"
        ]
    },
    {
        "term": "Strong Entity vs Weak Entity",
        "question": "What distinguishes a Strong Entity from a Weak Entity, and how is it represented in an ER diagram?",
        "points": [
            "Strong Entity: Has its own Primary Key and can exist independently. Represented by a SINGLE rectangle.",
            "Weak Entity: Lacks a primary key of its own; depends on an identifying (strong) owner entity for existence. Has a Partial Key (Discriminator, dashed underline).",
            "Representation: Weak Entity = DOUBLE rectangle; Identifying Relationship = DOUBLE diamond."
        ]
    },
    {
        "term": "Degree vs Cardinality of a Relation",
        "question": "What do Degree and Cardinality measure in the Relational Model?",
        "points": [
            "Degree (Arity): Total number of ATTRIBUTES (columns) in the relation schema. (Rarely changes).",
            "Cardinality: Total number of TUPLES (rows) currently stored in the relation instance. (Changes constantly).",
            "Exam Mnemonic: 'Degree' is vertical (columns); 'Cardinality' is horizontal count (rows)."
        ]
    },
    {
        "term": "WHERE vs HAVING Clause",
        "question": "When must you use HAVING instead of WHERE in SQL?",
        "points": [
            "WHERE: Filters individual tuples BEFORE aggregation. Cannot contain aggregate functions (e.g. `WHERE AVG(salary) > 5000` is illegal).",
            "HAVING: Filters summary groups AFTER `GROUP BY` aggregation. Can directly evaluate aggregate functions.",
            "Execution Order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY."
        ]
    },
    {
        "term": "DROP vs TRUNCATE vs DELETE",
        "question": "What are the structural, performance, and transactional differences between DROP, TRUNCATE, and DELETE?",
        "points": [
            "DELETE: DML operation. Deletes rows row-by-row with individual rollback logs. Slower. Schema remains.",
            "TRUNCATE: DDL operation. Deallocates data pages directly. Ultra-fast. Resets auto-increment seeds. Schema remains.",
            "DROP: DDL operation. Destroys the table schema, constraints, data, and metadata from the data dictionary permanently."
        ]
    },
    {
        "term": "INNER JOIN vs NATURAL JOIN",
        "question": "Why is NATURAL JOIN considered dangerous in production compared to explicit INNER JOIN?",
        "points": [
            "INNER JOIN: Explicitly matches rows using an `ON tableA.col = tableB.col` predicate specified by the developer.",
            "NATURAL JOIN: Automatically joins on ALL columns in both tables that share the EXACT same name, suppressing duplicates.",
            "Danger: If a developer adds a new common column (e.g. `created_at` or `status`) to both tables, a NATURAL JOIN will silently break by joining on that column too!"
        ]
    },
    {
        "term": "Correlated vs Non-Correlated Subquery",
        "question": "How do execution semantics differ between correlated and uncorrelated subqueries?",
        "points": [
            "Non-Correlated: Self-contained. Executes ONCE independently; its result set is passed to the outer query.",
            "Correlated: References outer query columns (e.g. `WHERE d.dept_id = e.dept_id`). Executes ONCE PER outer candidate row.",
            "Performance: Correlated subqueries can be $O(N \\times M)$ unless rewritten as joins or decorrelated."
        ]
    },
    {
        "term": "Specialization vs Generalization in EER",
        "question": "What is the directionality difference between Specialization and Generalization?",
        "points": [
            "Generalization: BOTTOM-UP abstraction. Unifies multiple entity sets with common features into a higher-level superclass (e.g., Car and Truck -> Vehicle).",
            "Specialization: TOP-DOWN refinement. Decomposes a higher-level superclass into specialized subclasses with specific attributes (e.g., Employee -> Engineer, Secretary)."
        ]
    }
]

def run_rapid_fire_session():
    clear_screen()
    banner("RAPID FIRE KEY TERMS & DIFFERENCES", "Last-Minute High-Yield Conceptual Memory Drills")
    
    deck = list(RAPID_FIRE_CONCEPTS)
    random.shuffle(deck)
    total = len(deck)
    review_list = []

    print(f"{Color.GREEN}Loaded {total} core exam concepts. Test yourself before viewing the model answer!{Color.RESET}\n")
    wait_for_enter("Press [Enter] to start flashcards...")

    for idx, item in enumerate(deck, 1):
        clear_screen()
        section_box(f"CONCEPT #{idx}/{total}: {item['term'].upper()}")
        print(f"\n{Color.BOLD}{Color.WHITE}❓ Question:{Color.RESET} {item['question']}\n")
        
        input(f"{Color.YELLOW}Press [Enter] to reveal the Exam Distinction Matrix...{Color.RESET}")
        
        print(f"\n{Color.GREEN}{Color.BOLD}🎯 KEY EXAM POINTS & DISTINCTIONS:{Color.RESET}")
        for pt in item["points"]:
            print(f"  {Color.CYAN}•{Color.RESET} {pt}")

        print(f"\n{Color.BOLD}Self-Assessment:{Color.RESET}")
        resp = input(f"Did you know this concept? ({Color.GREEN}[y] Mastered{Color.RESET} / {Color.RED}[n] Need Review{Color.RESET}): ").strip().lower()
        if resp != 'y':
            review_list.append(item['term'])

    clear_screen()
    banner("RAPID FIRE MASTERY SUMMARY")
    mastered_count = total - len(review_list)
    print(f"  {Color.BOLD}Total Concepts Tested:{Color.RESET} {total}")
    print(f"  {Color.BOLD}Concepts Mastered:    {Color.RESET} {Color.GREEN}{mastered_count}{Color.RESET}")
    print(f"  {Color.BOLD}Concepts to Revisit:  {Color.RESET} {Color.RED}{len(review_list)}{Color.RESET}\n")

    if review_list:
        section_box("⚠️ CONCEPTS FLAGGED FOR FINAL EXAM REVISION")
        for term in review_list:
            print(f"  {Color.RED}• {term}{Color.RESET}")
        print(f"\n{Color.DIM}Review these in 'DBMS_EXAM_QUICK_REVISION_AND_CHEATSHEET.md' tonight!{Color.RESET}")
    else:
        print(f"{Color.GREEN}{Color.BOLD}🔥 PERFECT RECALL! You are fully prepped on theoretical distinctions!{Color.RESET}")

    wait_for_enter()

# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def main_menu():
    while True:
        clear_screen()
        banner("DBMS PRACTICAL CODING & EXAM SIMULATOR", "Version 2.0 | Complete Study & Testing Suite")
        print(f"{Color.BOLD}SELECT AN EXAM SIMULATOR MODULE:{Color.RESET}\n")
        print(f"  {Color.BOLD}[1]{Color.RESET} {Color.CYAN}Practice Multiple Choice Questions (MCQs){Color.RESET}")
        print(f"      {Color.DIM}Randomized 20-question mock exam or quick drills with instant rationale.{Color.RESET}\n")
        print(f"  {Color.BOLD}[2]{Color.RESET} {Color.YELLOW}Practice SQL Coding Challenges & Interactive Sandbox{Color.RESET}")
        print(f"      {Color.DIM}In-memory SQLite practical tests with automated pass/fail verification.{Color.RESET}\n")
        print(f"  {Color.BOLD}[3]{Color.RESET} {Color.MAGENTA}Rapid Fire Key Terms & Differences Drill{Color.RESET}")
        print(f"      {Color.DIM}Flashcards covering the top 10 most tested oral and written distinctions.{Color.RESET}\n")
        print(f"  {Color.BOLD}[4]{Color.RESET} {Color.WHITE}Open Free Interactive SQL Sandbox REPL{Color.RESET}")
        print(f"      {Color.DIM}Directly query preloaded university and corporate database tables.{Color.RESET}\n")
        print(f"  {Color.BOLD}[0]{Color.RESET} Exit Simulator\n")
        
        try:
            choice = input(f"{Color.YELLOW}Enter your selection [0-4]: {Color.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye and best of luck on your exam!")
            break

        if choice == '1':
            run_mcq_session()
        elif choice == '2':
            run_challenge_mode()
        elif choice == '3':
            run_rapid_fire_session()
        elif choice == '4':
            run_free_sandbox()
        elif choice == '0':
            print(f"\n{Color.GREEN}Best of luck on your DBMS Exam tomorrow! You're going to ace it! 🎓{Color.RESET}\n")
            break
        else:
            print(f"{Color.RED}Invalid selection. Please choose 0 to 4.{Color.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProcess terminated. Good luck on your exams!")
        sys.exit(0)

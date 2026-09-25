# 🏆 DBMS PRACTICAL CODING CHALLENGES: 25 GRADED EXAM PROBLEMS
**Target: 100% Practical & Query Mastery for DBMS University, College, and Competitive Technical Examinations**  
**Database Dialect: ANSI SQL & SQLite 3 Compatible (Standard Relational Syntax)**  

---

## 📋 QUICK REFERENCE ROADMAP

| # | Challenge Name | Core Concept | Difficulty |
|---|---|---|---|
| 01 | University Enrollment Schema | DDL: Composite PK, FKs, DEFAULT, CHECK | ⭐ Easy |
| 02 | E-Commerce Inventory & Constraints | DDL: UNIQUE, CHECK Ranges, CASCADE | ⭐ Easy |
| 03 | Corporate Hierarchy Schema | DDL: Self-Referencing FK, SET NULL | ⭐⭐ Medium |
| 04 | Bulk Data Ingestion & Fallbacks | DML: Multi-Row INSERT & DEFAULTs | ⭐ Easy |
| 05 | Tiered Merit Salary Update | DML: Conditional UPDATE with CASE | ⭐⭐ Medium |
| 06 | Safe Cascading Account Pruning | DML: DELETE with Referential Integrity | ⭐⭐ Medium |
| 07 | Pattern Matching & Wildcard Searches | DQL: LIKE, `%`, `_`, ESCAPE sequences | ⭐ Easy |
| 08 | Three-Valued Logic & Null Handling | DQL: IS NULL, IS NOT NULL, COALESCE | ⭐ Easy |
| 09 | Multi-Column Sorting & Pagination | DQL: ORDER BY Multi-column, LIMIT, OFFSET | ⭐ Easy |
| 10 | Departmental Payroll Summaries | AGGREGATES: COUNT, SUM, AVG, MIN, MAX | ⭐ Easy |
| 11 | Department Headcount & Salary Thresholds | GROUP BY & HAVING Filtering | ⭐⭐ Medium |
| 12 | Multi-Level Sales Aggregation | GROUP BY Multiple Columns & HAVING | ⭐⭐ Medium |
| 13 | Complete Academic Transcript Sheet | 3-Table INNER JOIN & Aliasing | ⭐⭐ Medium |
| 14 | Unassigned Employees & Dormant Projects | LEFT OUTER JOIN & Anti-Joins | ⭐⭐ Medium |
| 15 | Reconciling Discrepant Warehouses | FULL OUTER JOIN Emulation via UNION | ⭐⭐⭐ Hard |
| 16 | Manager-Employee Organizational Tree | SELF JOIN for Hierarchical Traversal | ⭐⭐ Medium |
| 17 | Round-Robin Tournament Match Matrix | CROSS JOIN with Anti-Mirror Conditions | ⭐⭐ Medium |
| 18 | Above-Average Payroll Outliers | Scalar Subqueries in WHERE & SELECT | ⭐⭐ Medium |
| 19 | High-Value Customers & The NULL Trap | Multi-row Subqueries with IN & NOT IN | ⭐⭐ Medium |
| 20 | Departmental Pay Leaders | Correlated Subquery with External Scope | ⭐⭐⭐ Hard |
| 21 | The N-th Highest Salary | Correlated Subquery Without Window Funcs | ⭐⭐⭐ Hard |
| 22 | Relational Division (EXISTS / NOT EXISTS) | Double Negation & Universal Quantification | ⭐⭐⭐ Hard |
| 23 | Merging Contact Books Without Duplication | Set Operations: UNION vs UNION ALL | ⭐ Easy |
| 24 | Technical Skill Gap Analysis | Set Operations: INTERSECT & EXCEPT | ⭐⭐ Medium |
| 25 | Executive Capstone Analytics Report | Master Combination: Joins, Aggregates & Cases | ⭐⭐⭐ Hard |

---

# SECTION 1: DATA DEFINITION LANGUAGE (DDL) & INTEGRITY CONSTRAINTS

---

### Challenge 01: University Enrollment Schema with Composite Primary Key
**Category:** DDL & Integrity Constraints  
**Difficulty:** ⭐ Easy (Foundational)

#### 1. Problem Statement
Design a relational schema for a university course enrollment system. You must create two tables:
1. `Students`:
   - `student_id`: Integer, Primary Key.
   - `full_name`: Variable character up to 60 characters, cannot be empty (`NOT NULL`).
   - `email`: Variable character up to 100 characters, must be unique across all students (`UNIQUE`), cannot be empty (`NOT NULL`).
   - `standing`: Character string up to 15 characters, defaults to `'Freshman'` (`DEFAULT`).
   - `cgpa`: Decimal (3, 2), must be between `0.00` and `4.00` inclusive (`CHECK`).
2. `Enrollments`:
   - `student_id`: Integer, references `Students(student_id)` with cascading deletion (`ON DELETE CASCADE`).
   - `course_code`: Fixed character length 6 (e.g., `'CS101'`), cannot be null.
   - `semester`: Variable character up to 10 (e.g., `'Fall 2026'`), cannot be null.
   - `grade_points`: Decimal (3, 2) allowed to be null (if course is in progress), but if entered, must be between `0.00` and `4.00` (`CHECK`).
   - A student can enroll in multiple courses, and a course has many students, but a student cannot enroll in the *same* course during the *same* semester more than once. Establish a **Composite Primary Key** on `(student_id, course_code, semester)`.

#### 2. Table Schema DDL Solution
```sql
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    full_name VARCHAR(60) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    standing VARCHAR(15) DEFAULT 'Freshman',
    cgpa DECIMAL(3, 2) CHECK (cgpa >= 0.00 AND cgpa <= 4.00)
);

CREATE TABLE Enrollments (
    student_id INT NOT NULL,
    course_code VARCHAR(6) NOT NULL,
    semester VARCHAR(10) NOT NULL,
    grade_points DECIMAL(3, 2) CHECK (grade_points IS NULL OR (grade_points >= 0.00 AND grade_points <= 4.00)),
    PRIMARY KEY (student_id, course_code, semester),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);
```

#### 3. Verification Test
```sql
-- Valid Insert
INSERT INTO Students (student_id, full_name, email, cgpa) 
VALUES (101, 'Alice Smith', 'alice@univ.edu', 3.85);

INSERT INTO Enrollments (student_id, course_code, semester, grade_points)
VALUES (101, 'CS101', 'Fall 2026', 4.00);

-- Should FAIL due to Duplicate Composite Key:
-- INSERT INTO Enrollments (student_id, course_code, semester, grade_points) VALUES (101, 'CS101', 'Fall 2026', 3.50);

-- Should FAIL due to CHECK constraint violation:
-- INSERT INTO Students (student_id, full_name, email, cgpa) VALUES (102, 'Bob', 'bob@univ.edu', 4.50);
```

#### 4. Common Pitfalls & Exam Traps
- **Trap 1:** Placing `PRIMARY KEY` on each column separately in `Enrollments`. A table can have only **one** `PRIMARY KEY` clause. For composite keys, use table-level syntax: `PRIMARY KEY (col1, col2, col3)`.
- **Trap 2:** Forgetting `ON DELETE CASCADE`. If omitted, deleting a student whose records exist in `Enrollments` will either fail with a referential integrity violation or leave orphan records.
- **Trap 3:** In CHECK constraints, forgetting that `NULL` values evaluate to `UNKNOWN` in SQL. `grade_points BETWEEN 0.0 AND 4.0` actually allows `NULL` in standard SQL, but explicitly writing `grade_points IS NULL OR ...` is best practice for clarity.

---

### Challenge 02: E-Commerce Catalog with Multi-Column Foreign Keys & Checks
**Category:** DDL & Integrity Constraints  
**Difficulty:** ⭐ Easy (Foundational)

#### 1. Problem Statement
Create two tables for an e-commerce inventory management subsystem:
1. `Categories`:
   - `category_id`: Integer, Primary Key.
   - `category_name`: String (40), unique and non-null.
   - `is_active`: Small integer or boolean, default `1` (active), restricted to `0` or `1`.
2. `Products`:
   - `product_id`: Integer, Primary Key.
   - `sku`: String (20), must be unique, non-null, and uppercase.
   - `product_name`: String (100), non-null.
   - `unit_price`: Decimal (10, 2), must be strictly greater than 0.
   - `stock_quantity`: Integer, defaults to 0, cannot be negative (`>= 0`).
   - `category_id`: Integer, references `Categories(category_id)`. If the parent category is deleted, disallow deletion (`ON DELETE RESTRICT` / `NO ACTION`).

#### 2. Table Schema DDL Solution
```sql
CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(40) NOT NULL UNIQUE,
    is_active INT DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    sku VARCHAR(20) NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0.00),
    stock_quantity INT DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE RESTRICT
);
```

#### 3. Common Pitfalls & Exam Traps
- **Difference between `RESTRICT` and `CASCADE`:** In an exam, if asked *"Prevent deletion of parent if children exist"*, the answer is `ON DELETE RESTRICT` (or `NO ACTION`). If asked *"Automatically delete children"*, the answer is `CASCADE`.
- **Negative Stock Values:** Forgetting `CHECK (stock_quantity >= 0)` allows inventory bugs where stock drops to `-5`.

---

### Challenge 03: Corporate Hierarchy with Self-Referencing Foreign Key
**Category:** DDL & Recursive Relationships  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
Create a table `Staff` representing employees in a corporation where every employee (except the CEO) reports to another employee within the same table.
- `emp_id`: Integer, Primary Key.
- `emp_name`: String (50), non-null.
- `role`: String (30), non-null.
- `manager_id`: Integer, Foreign Key referencing `Staff(emp_id)`.
- If a manager leaves the company and their record is deleted, their subordinates should not be erased; instead, their `manager_id` should automatically be set to `NULL` pending reassignment.

#### 2. Table Schema DDL Solution
```sql
CREATE TABLE Staff (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    role VARCHAR(30) NOT NULL,
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES Staff(emp_id) ON DELETE SET NULL
);
```

#### 3. Verification Test
```sql
-- CEO (manager_id is NULL)
INSERT INTO Staff VALUES (1, 'Eleanor Vance', 'CEO', NULL);
-- VP reporting to CEO
INSERT INTO Staff VALUES (2, 'Mark Chen', 'VP Engineering', 1);
-- Engineer reporting to VP
INSERT INTO Staff VALUES (3, 'Sara Connor', 'Lead Architect', 2);

-- Deleting VP (emp_id = 2) should update Sara's manager_id to NULL
DELETE FROM Staff WHERE emp_id = 2;
-- Query Staff: Sara Connor now has manager_id = NULL
```

#### 4. Common Pitfalls & Exam Traps
- **NOT NULL on Self-Referencing Key:** If you mark `manager_id INT NOT NULL`, you will create a chicken-and-egg deadlock: you cannot insert the CEO (who has no manager), and `ON DELETE SET NULL` will throw an error because the column cannot accept NULL.

---

# SECTION 2: DATA MANIPULATION LANGUAGE (DML)

---

### Challenge 04: Bulk Data Ingestion with Constraint Adherence
**Category:** DML Operations  
**Difficulty:** ⭐ Easy

#### 1. Problem Statement
Given the table:
```sql
CREATE TABLE Warehouses (
    wh_id INT PRIMARY KEY,
    wh_code VARCHAR(10) NOT NULL UNIQUE,
    city VARCHAR(50) NOT NULL,
    capacity INT DEFAULT 5000 CHECK (capacity >= 1000)
);
```
Write a single SQL statement to insert three warehouse records:
1. ID: `1`, Code: `'WH-EAST-1'`, City: `'Boston'`, Capacity: `12000`.
2. ID: `2`, Code: `'WH-WEST-1'`, City: `'Seattle'`, using the default capacity.
3. ID: `3`, Code: `'WH-CENT-1'`, City: `'Chicago'`, Capacity: `8500`.

#### 2. Optimal SQL Solution Query
```sql
INSERT INTO Warehouses (wh_id, wh_code, city, capacity) VALUES
(1, 'WH-EAST-1', 'Boston', 12000),
(2, 'WH-WEST-1', 'Seattle', DEFAULT),
(3, 'WH-CENT-1', 'Chicago', 8500);
```
*(In SQLite where the `DEFAULT` keyword in `VALUES` is not supported, omit the column name:)*
```sql
INSERT INTO Warehouses (wh_id, wh_code, city, capacity) VALUES (1, 'WH-EAST-1', 'Boston', 12000);
INSERT INTO Warehouses (wh_id, wh_code, city) VALUES (2, 'WH-WEST-1', 'Seattle');
INSERT INTO Warehouses (wh_id, wh_code, city, capacity) VALUES (3, 'WH-CENT-1', 'Chicago', 8500);
```

#### 3. Expected Result
| wh_id | wh_code | city | capacity |
|---|---|---|---|
| 1 | WH-EAST-1 | Boston | 12000 |
| 2 | WH-WEST-1 | Seattle | 5000 |
| 3 | WH-CENT-1 | Chicago | 8500 |

#### 4. Common Pitfalls & Exam Traps
- Omitting the column list in `INSERT INTO Warehouses VALUES (...)` requires providing every value in exact ordinal order. Specifying column lists is far safer and allows columns with `DEFAULT` or `AUTOINCREMENT` to be skipped.

---

### Challenge 05: Tiered Merit Salary Update
**Category:** DML Operations  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
The board has approved performance-based raises for the `Personnel` table:
- Employees in department `'Research'` get a 10% raise.
- Employees in department `'Sales'` get a 5% raise, plus a flat \$500 bonus.
- All other employees get a flat \$300 raise.
- However, no employee's salary can exceed \$95,000. Cap any salary that would exceed \$95,000 at exactly \$95,000.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE Personnel (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(30),
    salary DECIMAL(10, 2)
);

INSERT INTO Personnel VALUES
(1, 'Alice', 'Research', 80000.00),
(2, 'Bob', 'Sales', 50000.00),
(3, 'Charlie', 'Research', 92000.00),
(4, 'Diana', 'HR', 45000.00);
```

#### 3. Optimal SQL Solution Query
```sql
UPDATE Personnel
SET salary = CASE 
    WHEN department = 'Research' THEN 
        CASE WHEN salary * 1.10 > 95000.00 THEN 95000.00 ELSE salary * 1.10 END
    WHEN department = 'Sales' THEN 
        CASE WHEN (salary * 1.05) + 500 > 95000.00 THEN 95000.00 ELSE (salary * 1.05) + 500 END
    ELSE 
        CASE WHEN salary + 300 > 95000.00 THEN 95000.00 ELSE salary + 300 END
END;
```
*(Or cleanly using the `MIN()` or nested `CASE` expression)*:
```sql
UPDATE Personnel
SET salary = CASE 
    WHEN (CASE 
            WHEN department = 'Research' THEN salary * 1.10 
            WHEN department = 'Sales' THEN (salary * 1.05) + 500 
            ELSE salary + 300 
          END) > 95000.00 THEN 95000.00
    ELSE (CASE 
            WHEN department = 'Research' THEN salary * 1.10 
            WHEN department = 'Sales' THEN (salary * 1.05) + 500 
            ELSE salary + 300 
          END)
END;
```

#### 4. Expected Result
| emp_id | name | department | salary |
|---|---|---|---|
| 1 | Alice | Research | 88000.00 |
| 2 | Bob | Sales | 53000.00 |
| 3 | Charlie | Research | 95000.00 |
| 4 | Diana | HR | 45300.00 |

*Note: Charlie's 10% raise on 92,000 would be 101,200, but is capped at 95,000.00.*

#### 5. Common Pitfalls & Exam Traps
- **Running multiple sequential UPDATEs without transactions:** If you run `UPDATE Personnel SET salary = salary * 1.10 WHERE ...` followed by other statements, rows might be updated multiple times if criteria overlap.
- **Floating point arithmetic:** In monetary calculations, always use `DECIMAL(10, 2)` or round appropriately.

---

### Challenge 06: Safe Record Pruning with Subquery Validation
**Category:** DML Operations  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
In an online banking system, delete all accounts belonging to customers who registered before the year 2020 (`registration_date < '2020-01-01'`) AND whose current balance is strictly 0. Accounts with positive balances or active loans must never be deleted.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE Customers (
    cust_id INT PRIMARY KEY,
    cust_name VARCHAR(50),
    registration_date DATE
);

CREATE TABLE BankAccounts (
    acc_no INT PRIMARY KEY,
    cust_id INT,
    balance DECIMAL(12, 2),
    has_active_loan INT, -- 1 = True, 0 = False
    FOREIGN KEY (cust_id) REFERENCES Customers(cust_id)
);

INSERT INTO Customers VALUES
(1, 'John Doe', '2018-05-12'),
(2, 'Jane Roe', '2019-11-20'),
(3, 'Jim Beam', '2021-03-15');

INSERT INTO BankAccounts VALUES
(1001, 1, 0.00, 0),    -- Eligible for deletion (Pre-2020, balance 0, no loan)
(1002, 1, 150.00, 0),  -- NOT eligible (balance > 0)
(1003, 2, 0.00, 1),    -- NOT eligible (has active loan)
(1004, 3, 0.00, 0);    -- NOT eligible (registered 2021)
```

#### 3. Optimal SQL Solution Query
```sql
DELETE FROM BankAccounts
WHERE balance = 0.00 
  AND has_active_loan = 0
  AND cust_id IN (
      SELECT cust_id 
      FROM Customers 
      WHERE registration_date < '2020-01-01'
  );
```

#### 4. Expected Result
Remaining records in `BankAccounts`:
| acc_no | cust_id | balance | has_active_loan |
|---|---|---|---|
| 1002 | 1 | 150.00 | 0 |
| 1003 | 2 | 0.00 | 1 |
| 1004 | 3 | 0.00 | 0 |

#### 5. Common Pitfalls & Exam Traps
- **Accidental Truncation:** Omitting the `WHERE` clause deletes the entire table!
- **Joining in DELETE:** Standard ANSI SQL does not allow `DELETE BankAccounts FROM BankAccounts JOIN Customers ...` (that is a T-SQL/MySQL extension). The standard ANSI SQL portable way is using a `WHERE cust_id IN (SELECT ...)`.

---

# SECTION 3: DATA QUERY LANGUAGE (DQL) — FILTERING, SORTING & NULLs

---

### Challenge 07: Complex Pattern Matching & Wildcard Searching
**Category:** DQL & String Functions  
**Difficulty:** ⭐ Easy

#### 1. Problem Statement
A telecommunications provider stores network service tickets. Retrieve all tickets where:
1. The `ticket_code` starts with `'NET_'` (note that the underscore must be treated as a literal character, not as a single-character wildcard!).
2. The `description` contains the word `'failure'` (case-insensitive where possible).
3. The `customer_phone` has `'555'` anywhere as its middle 3 digits.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE ServiceTickets (
    ticket_id INT PRIMARY KEY,
    ticket_code VARCHAR(20),
    description VARCHAR(200),
    customer_phone VARCHAR(15)
);

INSERT INTO ServiceTickets VALUES
(1, 'NET_9011', 'Server hardware failure detected', '011-555-9081'),
(2, 'NET-8820', 'Power failure in switch room', '011-555-4432'),
(3, 'NET_3021', 'Scheduled routine maintenance', '011-555-1212'),
(4, 'SYS_4412', 'Network link failure on rack 4', '011-444-5550'),
(5, 'NET_1009', 'Switch power Failure reboot', '011-555-7788');
```

#### 3. Optimal SQL Solution Query
```sql
SELECT ticket_id, ticket_code, description, customer_phone
FROM ServiceTickets
WHERE ticket_code LIKE 'NET\_%' ESCAPE '\'
  AND LOWER(description) LIKE '%failure%'
  AND customer_phone LIKE '%-555-%';
```

#### 4. Expected Result
| ticket_id | ticket_code | description | customer_phone |
|---|---|---|---|
| 1 | NET_9011 | Server hardware failure detected | 011-555-9081 |
| 5 | NET_1009 | Switch power Failure reboot | 011-555-7788 |

#### 5. Common Pitfalls & Exam Traps
- **The Underscore `_` Trap:** In SQL `LIKE`, `_` matches *any single character*. If you write `LIKE 'NET_%'`, it will also match `'NET-8820'` (as in record 2)! To match a literal underscore, you MUST escape it: `LIKE 'NET\_%' ESCAPE '\'`.
- **Case Sensitivity:** In PostgreSQL and standard SQL, `LIKE` is case-sensitive. Wrapping the column in `LOWER()` guarantees portable case-insensitive matching.

---

### Challenge 08: Three-Valued Logic & The NULL Trap
**Category:** DQL & Logic Operations  
**Difficulty:** ⭐ Easy

#### 1. Problem Statement
The sales commission ledger contains agents, base salaries, and optional commission rates.
Write a query to calculate the `total_compensation` for all agents.
- If `commission_pct` is not null, `total_compensation = base_salary + (base_salary * commission_pct / 100)`.
- If `commission_pct` is null, total compensation is simply `base_salary`.
- Display columns: `agent_name`, `base_salary`, `commission_pct` (display `'N/A'` if null), and `total_compensation`.
- Filter to display only agents whose total compensation is greater than or equal to \$50,000.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE SalesAgents (
    agent_id INT PRIMARY KEY,
    agent_name VARCHAR(50),
    base_salary DECIMAL(10, 2),
    commission_pct DECIMAL(5, 2) -- Can be NULL
);

INSERT INTO SalesAgents VALUES
(1, 'Amanda', 60000.00, 10.00),
(2, 'Brian', 52000.00, NULL),
(3, 'Chloe', 45000.00, 8.00),   -- 45000 + 3600 = 48600 (< 50000)
(4, 'David', 48000.00, 5.00),   -- 48000 + 2400 = 50400 (>= 50000)
(5, 'Evelyn', 40000.00, NULL);
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    agent_name,
    base_salary,
    COALESCE(CAST(commission_pct AS VARCHAR(10)), 'N/A') AS commission_pct,
    base_salary + (base_salary * COALESCE(commission_pct, 0.0) / 100.0) AS total_compensation
FROM SalesAgents
WHERE base_salary + (base_salary * COALESCE(commission_pct, 0.0) / 100.0) >= 50000.00
ORDER BY total_compensation DESC;
```

#### 4. Expected Result
| agent_name | base_salary | commission_pct | total_compensation |
|---|---|---|---|
| Amanda | 60000.00 | 10.0 | 66000.00 |
| Brian | 52000.00 | N/A | 52000.00 |
| David | 48000.00 | 5.0 | 50400.00 |

#### 5. Common Pitfalls & Exam Traps
- **Arithmetic with NULL:** In SQL, `52000 + NULL` evaluates to `NULL`, NOT `52000`! If you omit `COALESCE(commission_pct, 0)`, Brian will evaluate to `NULL >= 50000`, which is `UNKNOWN`, and he will be omitted from the output.
- **Using `= NULL` in WHERE:** Never write `WHERE commission_pct = NULL`. Always write `IS NULL` or `IS NOT NULL`.

---

### Challenge 09: Deterministic Multi-Column Sorting & Pagination
**Category:** DQL & Result Set Shaping  
**Difficulty:** ⭐ Easy

#### 1. Problem Statement
Retrieve the 2nd page of results (page size = 3 rows) from the `Leaderboard` table.
- Sort primarily by `score` in descending order (highest score first).
- For ties in `score`, sort by `completion_time_sec` in ascending order (faster time wins).
- For ties in both score and time, sort alphabetically by `player_name` ascending to make the pagination completely deterministic.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE Leaderboard (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(50),
    score INT,
    completion_time_sec INT
);

INSERT INTO Leaderboard VALUES
(1, 'Zane', 1000, 140),
(2, 'Aaron', 1000, 120),  -- Tie 1000, faster time
(3, 'Bella', 1000, 120),  -- Tie 1000, tie 120, alphabetical tie-breaker
(4, 'Chris', 950, 110),
(5, 'Diana', 950, 115),
(6, 'Evan', 900, 100),
(7, 'Fiona', 850, 95);
```

#### 3. Optimal SQL Solution Query
```sql
SELECT player_name, score, completion_time_sec
FROM Leaderboard
ORDER BY score DESC, completion_time_sec ASC, player_name ASC
LIMIT 3 OFFSET 3;
```

#### 4. Expected Result
*Page 1 (Rows 1-3) would be: Aaron (1000, 120), Bella (1000, 120), Zane (1000, 140).*  
*Page 2 (Rows 4-6, OFFSET 3, LIMIT 3) is:*
| player_name | score | completion_time_sec |
|---|---|---|
| Chris | 950 | 110 |
| Diana | 950 | 115 |
| Evan | 900 | 100 |

#### 5. Common Pitfalls & Exam Traps
- **Non-deterministic Pagination:** If `ORDER BY` does not establish a total ordering (i.e. unique tie-breaker), the database engine is free to return tied rows in any physical disk order. Rows can appear on both Page 1 and Page 2!
- **OFFSET formula:** Page $N$ with size $S$ has `OFFSET = (N - 1) * S`. For Page 2 with size 3, `OFFSET = (2 - 1) * 3 = 3`.

---

# SECTION 4: AGGREGATE FUNCTIONS, GROUP BY & HAVING

---

### Challenge 10: Departmental Payroll Summaries with Aggregates
**Category:** Aggregates & GROUP BY  
**Difficulty:** ⭐ Easy

#### 1. Problem Statement
Generate an executive payroll summary grouped by `department`. For each department, calculate:
1. `headcount`: Total number of employees.
2. `total_payroll`: Sum of all salaries.
3. `avg_salary`: Average salary rounded to 2 decimal places.
4. `min_salary`: Minimum salary in that department.
5. `max_salary`: Maximum salary in that department.
Order the output by `total_payroll` descending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE EmpDirectory (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO EmpDirectory VALUES
(1, 'Alice', 'Engineering', 95000.00),
(2, 'Bob', 'Engineering', 85000.00),
(3, 'Charlie', 'Engineering', 105000.00),
(4, 'Diana', 'Marketing', 62000.00),
(5, 'Edward', 'Marketing', 58000.00),
(6, 'Fiona', 'HR', 71000.00);
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    department,
    COUNT(*) AS headcount,
    SUM(salary) AS total_payroll,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM EmpDirectory
GROUP BY department
ORDER BY total_payroll DESC;
```

#### 4. Expected Result
| department | headcount | total_payroll | avg_salary | min_salary | max_salary |
|---|---|---|---|---|---|
| Engineering | 3 | 285000.00 | 95000.00 | 85000.00 | 105000.00 |
| Marketing | 2 | 120000.00 | 60000.00 | 58000.00 | 62000.00 |
| HR | 1 | 71000.00 | 71000.00 | 71000.00 | 71000.00 |

#### 5. Common Pitfalls & Exam Traps
- **Selecting Non-Aggregated Columns:** In ANSI SQL, any column in the `SELECT` list that is not wrapped in an aggregate function (`COUNT`, `SUM`, etc.) **MUST** appear in the `GROUP BY` clause. Writing `SELECT name, department, AVG(salary) GROUP BY department` is illegal in standard SQL!

---

### Challenge 11: Department Headcount & Salary Thresholds (HAVING vs WHERE)
**Category:** GROUP BY & HAVING  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
Find all departments that have:
1. At least 2 employees earning more than \$60,000 individually.
2. An average salary among those employees strictly greater than \$75,000.
Display the department name, the qualifying headcount, and the average salary rounded to 2 decimal places.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE StaffSalaries (
    staff_id INT PRIMARY KEY,
    staff_name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO StaffSalaries VALUES
(1, 'Alex', 'IT', 90000.00),
(2, 'Beth', 'IT', 80000.00),
(3, 'Chad', 'IT', 45000.00),   -- Below 60k filter
(4, 'Dave', 'Finance', 70000.00),
(5, 'Emma', 'Finance', 72000.00), -- Avg of 70k + 72k = 71k (<= 75k)
(6, 'Fred', 'Legal', 95000.00),
(7, 'Gina', 'Legal', 85000.00),
(8, 'Hank', 'Support', 65000.00); -- Only 1 person
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    department,
    COUNT(*) AS qualifying_headcount,
    ROUND(AVG(salary), 2) AS avg_qualifying_salary
FROM StaffSalaries
WHERE salary > 60000.00
GROUP BY department
HAVING COUNT(*) >= 2 
   AND AVG(salary) > 75000.00;
```

#### 4. Expected Result
| department | qualifying_headcount | avg_qualifying_salary |
|---|---|---|
| IT | 2 | 85000.00 |
| Legal | 2 | 90000.00 |

*(Finance is excluded because its average 71,000.00 is not > 75,000. Support is excluded because headcount = 1).*

#### 5. Common Pitfalls & Exam Traps
- **THE #1 SQL EXAM MISTAKE:** Putting group conditions in `WHERE` or row conditions in `HAVING`.
  - `WHERE` filters **individual rows BEFORE grouping**.
  - `HAVING` filters **aggregated groups AFTER grouping**.
  - Writing `WHERE AVG(salary) > 75000` is an immediate syntax error.

---

### Challenge 12: Multi-Level Sales Aggregation
**Category:** GROUP BY & HAVING  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
An international distributor tracks sales across multiple countries and product categories.
Write a query to identify high-performing segments:
- Group records by both `country` and `category`.
- Calculate the total units sold (`SUM(units_sold)`) and total revenue (`SUM(units_sold * unit_price)`).
- Filter out segments where total revenue is less than \$10,000.
- Order by country alphabetically, then by total revenue descending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE GlobalSales (
    sale_id INT PRIMARY KEY,
    country VARCHAR(30),
    category VARCHAR(30),
    units_sold INT,
    unit_price DECIMAL(10, 2)
);

INSERT INTO GlobalSales VALUES
(1, 'Canada', 'Electronics', 10, 600.00),   -- 6000
(2, 'Canada', 'Electronics', 15, 600.00),   -- 9000 -> Total Canada Electronics = 15000 (Keep)
(3, 'Canada', 'Furniture', 5, 400.00),      -- 2000 -> Total Canada Furniture = 2000 (Drop < 10k)
(4, 'Germany', 'Electronics', 20, 800.00),  -- 16000 -> Keep
(5, 'Germany', 'Auto', 8, 1500.00),         -- 12000 -> Keep
(6, 'Japan', 'Hardware', 50, 100.00);       -- 5000 -> Drop < 10k
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    country,
    category,
    SUM(units_sold) AS total_units,
    SUM(units_sold * unit_price) AS total_revenue
FROM GlobalSales
GROUP BY country, category
HAVING SUM(units_sold * unit_price) >= 10000.00
ORDER BY country ASC, total_revenue DESC;
```

#### 4. Expected Result
| country | category | total_units | total_revenue |
|---|---|---|---|
| Canada | Electronics | 25 | 15000.00 |
| Germany | Electronics | 20 | 16000.00 |
| Germany | Auto | 8 | 12000.00 |

#### 5. Common Pitfalls & Exam Traps
- **Grouping by only one column:** If you write `GROUP BY country`, SQLite/MySQL might produce arbitrary values for `category`. You must group by `country, category`.

---

# SECTION 5: SQL JOINS MASTERCLASS

---

### Challenge 13: Three-Table Inner Join (Student-Course Grade Sheet)
**Category:** INNER JOIN  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
Generate an official academic transcript report linking three relations: `Students`, `Enrollments`, and `Courses`.
Display: `student_name`, `course_title`, `credits`, and the letter `grade`.
Filter for only enrollments in the `'Fall 2026'` semester.
Sort primarily by `student_name` ascending, and secondarily by `credits` descending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE AcadStudents (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE AcadCourses (
    course_id INT PRIMARY KEY,
    course_title VARCHAR(50),
    credits INT
);

CREATE TABLE AcadEnrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    semester VARCHAR(15),
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES AcadStudents(student_id),
    FOREIGN KEY (course_id) REFERENCES AcadCourses(course_id)
);

INSERT INTO AcadStudents VALUES (1, 'Alice Walker'), (2, 'Bob Harris'), (3, 'Clara Oswald');
INSERT INTO AcadCourses VALUES (101, 'Database Systems', 4), (102, 'Operating Systems', 4), (103, 'Discrete Math', 3);
INSERT INTO AcadEnrollments VALUES
(1, 1, 101, 'Fall 2026', 'A'),
(2, 1, 103, 'Fall 2026', 'A-'),
(3, 2, 102, 'Fall 2026', 'B+'),
(4, 2, 101, 'Spring 2026', 'A'), -- Filtered out by semester
(5, 3, 103, 'Fall 2026', 'B');
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    s.student_name,
    c.course_title,
    c.credits,
    e.grade
FROM AcadEnrollments e
INNER JOIN AcadStudents s ON e.student_id = s.student_id
INNER JOIN AcadCourses c ON e.course_id = c.course_id
WHERE e.semester = 'Fall 2026'
ORDER BY s.student_name ASC, c.credits DESC;
```

#### 4. Expected Result
| student_name | course_title | credits | grade |
|---|---|---|---|
| Alice Walker | Database Systems | 4 | A |
| Alice Walker | Discrete Math | 3 | A- |
| Bob Harris | Operating Systems | 4 | B+ |
| Clara Oswald | Discrete Math | 3 | B |

#### 5. Common Pitfalls & Exam Traps
- **Ambiguous column names:** If both `Students` and `Courses` have `name` or `title`, omitting table aliases (`s.` or `c.`) causes an ambiguous column name syntax error.
- **Join condition omission:** Forgetting `ON e.student_id = s.student_id` degenerates the query into a massive Cartesian Product ($N \times M \times P$ rows).

---

### Challenge 14: Unassigned Employees & Dormant Projects (Anti-Join Pattern)
**Category:** LEFT OUTER JOIN  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
An IT firm maintains `DevStaff` and `ActiveProjects`. An association table `Assignments` links developers to the projects they work on.
Write two queries:
- **Part A:** Find all developers who are currently NOT assigned to ANY project (bench staff).
- **Part B:** Find all projects that currently have ZERO developers assigned.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE DevStaff (
    dev_id INT PRIMARY KEY,
    dev_name VARCHAR(50)
);

CREATE TABLE ActiveProjects (
    proj_id INT PRIMARY KEY,
    proj_name VARCHAR(50)
);

CREATE TABLE Assignments (
    dev_id INT,
    proj_id INT,
    PRIMARY KEY (dev_id, proj_id),
    FOREIGN KEY (dev_id) REFERENCES DevStaff(dev_id),
    FOREIGN KEY (proj_id) REFERENCES ActiveProjects(proj_id)
);

INSERT INTO DevStaff VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'David');
INSERT INTO ActiveProjects VALUES (10, 'Cloud Migration'), (20, 'Mobile App'), (30, 'AI Copilot');
INSERT INTO Assignments VALUES (1, 10), (2, 10), (1, 20);
-- Charlie and David have no projects.
-- AI Copilot (30) has no developers.
```

#### 3. Optimal SQL Solution Query
```sql
-- Part A: Bench developers (Left Anti-Join)
SELECT d.dev_id, d.dev_name
FROM DevStaff d
LEFT JOIN Assignments a ON d.dev_id = a.dev_id
WHERE a.dev_id IS NULL;

-- Part B: Dormant projects (Right Anti-Join simulated via Left Join)
SELECT p.proj_id, p.proj_name
FROM ActiveProjects p
LEFT JOIN Assignments a ON p.proj_id = a.proj_id
WHERE a.proj_id IS NULL;
```

#### 4. Expected Result
**Part A Output:**
| dev_id | dev_name |
|---|---|
| 3 | Charlie |
| 4 | David |

**Part B Output:**
| proj_id | proj_name |
|---|---|
| 30 | AI Copilot |

#### 5. Common Pitfalls & Exam Traps
- **WHERE condition placed in ON:** If you write `LEFT JOIN Assignments a ON d.dev_id = a.dev_id AND a.dev_id IS NULL`, you will receive *all* employees with NULL join columns! The `IS NULL` check belongs in the `WHERE` clause to filter out matches.

---

### Challenge 15: Reconciling Discrepant Warehouses (FULL OUTER JOIN Emulation)
**Category:** FULL OUTER JOIN & Set Emulation  
**Difficulty:** ⭐⭐⭐ Hard

#### 1. Problem Statement
Two corporate branches maintain parts inventories: `WarehouseEast` and `WarehouseWest`.
- Some parts exist only in East.
- Some parts exist only in West.
- Some parts exist in both with differing quantities.
Write a query to perform a **Full Outer Join** reconciliation. Display:
`part_id`, `part_name`, `east_qty`, and `west_qty`. If a part does not exist in a warehouse, display `0`.
*(Note: Because SQLite and MySQL lack native `FULL OUTER JOIN`, you must write standard portable SQL using `LEFT JOIN` and `UNION`)*.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE WarehouseEast (
    part_id INT PRIMARY KEY,
    part_name VARCHAR(50),
    qty INT
);

CREATE TABLE WarehouseWest (
    part_id INT PRIMARY KEY,
    part_name VARCHAR(50),
    qty INT
);

INSERT INTO WarehouseEast VALUES (1, 'Gearbox', 50), (2, 'Bearing', 120), (3, 'Camshaft', 15);
INSERT INTO WarehouseWest VALUES (2, 'Bearing', 80), (3, 'Camshaft', 15), (4, 'Piston', 45);
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    e.part_id,
    e.part_name,
    e.qty AS east_qty,
    COALESCE(w.qty, 0) AS west_qty
FROM WarehouseEast e
LEFT JOIN WarehouseWest w ON e.part_id = w.part_id

UNION

SELECT 
    w.part_id,
    w.part_name,
    COALESCE(e.qty, 0) AS east_qty,
    w.qty AS west_qty
FROM WarehouseWest w
LEFT JOIN WarehouseEast e ON w.part_id = e.part_id
ORDER BY part_id;
```

#### 4. Expected Result
| part_id | part_name | east_qty | west_qty |
|---|---|---|---|
| 1 | Gearbox | 50 | 0 |
| 2 | Bearing | 120 | 80 |
| 3 | Camshaft | 15 | 15 |
| 4 | Piston | 0 | 45 |

#### 5. Common Pitfalls & Exam Traps
- **Using UNION ALL instead of UNION:** `UNION` removes duplicate rows produced by both sides for the overlapping keys (parts 2 and 3). `UNION ALL` would output duplicate rows for Bearing and Camshaft!

---

### Challenge 16: Organizational Hierarchy Reporting (SELF JOIN)
**Category:** SELF JOIN  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
Given an `Employees` table with a self-referencing `manager_id`, write a single query that lists every employee along with their immediate manager's name and their manager's role.
- If an employee does not have a manager (the CEO), display `'[TOP EXECUTIVE]'` for both manager name and role.
- Order by `emp_id` ascending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE CorpStaff (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    role VARCHAR(30),
    manager_id INT
);

INSERT INTO CorpStaff VALUES
(1, 'Arthur Dent', 'CEO', NULL),
(2, 'Ford Prefect', 'VP Technology', 1),
(3, 'Tricia McMillan', 'VP Operations', 1),
(4, 'Marvin Android', 'DevOps Specialist', 2),
(5, 'Zaphod Beeblebrox', 'Logistics Analyst', 3);
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.role AS employee_role,
    COALESCE(m.emp_name, '[TOP EXECUTIVE]') AS manager_name,
    COALESCE(m.role, '[TOP EXECUTIVE]') AS manager_role
FROM CorpStaff e
LEFT JOIN CorpStaff m ON e.manager_id = m.emp_id
ORDER BY e.emp_id ASC;
```

#### 4. Expected Result
| emp_id | employee_name | employee_role | manager_name | manager_role |
|---|---|---|---|---|
| 1 | Arthur Dent | CEO | [TOP EXECUTIVE] | [TOP EXECUTIVE] |
| 2 | Ford Prefect | VP Technology | Arthur Dent | CEO |
| 3 | Tricia McMillan | VP Operations | Arthur Dent | CEO |
| 4 | Marvin Android | DevOps Specialist | Ford Prefect | VP Technology |
| 5 | Zaphod Beeblebrox | Logistics Analyst | Tricia McMillan | VP Operations |

#### 5. Common Pitfalls & Exam Traps
- **Using INNER JOIN instead of LEFT JOIN:** An `INNER JOIN` matches only rows where `e.manager_id = m.emp_id`. Because Arthur Dent has `manager_id = NULL`, he would be completely eliminated from the output. In an exam, the CEO must never disappear from employee reports!

---

### Challenge 17: Round-Robin Tournament Pairing (CROSS JOIN with Logic)
**Category:** CROSS JOIN  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
A chess league has a table `ChessClubs`. Generate a schedule where every team plays every other team exactly once (no home/away duplicates, and a team never plays against itself).
Display: `home_team`, `away_team`.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE ChessClubs (
    club_id INT PRIMARY KEY,
    club_name VARCHAR(50)
);

INSERT INTO ChessClubs VALUES (1, 'Knights'), (2, 'Bishops'), (3, 'Rooks'), (4, 'Pawns');
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    c1.club_name AS home_team,
    c2.club_name AS away_team
FROM ChessClubs c1
CROSS JOIN ChessClubs c2
WHERE c1.club_id < c2.club_id
ORDER BY home_team, away_team;
```

#### 4. Expected Result
| home_team | away_team |
|---|---|
| Bishops | Pawns |
| Bishops | Rooks |
| Knights | Bishops |
| Knights | Pawns |
| Knights | Rooks |
| Pawns | Rooks |

*Total unique pairings for 4 teams: $\frac{4 \times 3}{2} = 6$ matches.*

#### 5. Common Pitfalls & Exam Traps
- **Using `c1.club_id <> c2.club_id`:** This filters out self-play, but produces 12 matches (both Knights vs Bishops AND Bishops vs Knights). To guarantee single round-robin without duplicates, use strictly `<`.

---

# SECTION 6: COMPLEX SUBQUERIES & NESTED QUERIES

---

### Challenge 18: Above-Average Payroll Outliers (Scalar Subqueries)
**Category:** Scalar Subqueries  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
Find all employees whose salary is strictly above the overall company average salary.
Display: `emp_name`, `salary`, `company_avg_salary` (rounded to 2 decimal places), and `difference` (how much higher their salary is than average).
Order by `difference` descending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE SubqStaff (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO SubqStaff VALUES
(1, 'Alice', 90000.00),
(2, 'Bob', 60000.00),
(3, 'Charlie', 75000.00),
(4, 'Diana', 45000.00),
(5, 'Evan', 80000.00);
-- Average salary = (90k + 60k + 75k + 45k + 80k) / 5 = 350k / 5 = 70000.00
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    emp_name,
    salary,
    ROUND((SELECT AVG(salary) FROM SubqStaff), 2) AS company_avg_salary,
    ROUND(salary - (SELECT AVG(salary) FROM SubqStaff), 2) AS difference
FROM SubqStaff
WHERE salary > (SELECT AVG(salary) FROM SubqStaff)
ORDER BY difference DESC;
```

#### 4. Expected Result
| emp_name | salary | company_avg_salary | difference |
|---|---|---|---|
| Alice | 90000.00 | 70000.00 | 20000.00 |
| Evan | 80000.00 | 70000.00 | 10000.00 |
| Charlie | 75000.00 | 70000.00 | 5000.00 |

#### 5. Common Pitfalls & Exam Traps
- **Writing `WHERE salary > AVG(salary)`:** Direct aggregate calls are forbidden in `WHERE` clauses. An inner `(SELECT AVG(...) FROM ...)` scalar subquery is required.

---

### Challenge 19: High-Ticket Customers & The NOT IN NULL Trap
**Category:** Multi-Row Subqueries  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
Given `Clients` and `Invoices`. Find all clients who have **NEVER** received an invoice with an amount over \$1,000.
(Be extremely vigilant: `Invoices` contains a row with `client_id IS NULL`!).

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE Clients (
    client_id INT PRIMARY KEY,
    client_name VARCHAR(50)
);

CREATE TABLE Invoices (
    invoice_id INT PRIMARY KEY,
    client_id INT,
    amount DECIMAL(10, 2)
);

INSERT INTO Clients VALUES (1, 'Acme Corp'), (2, 'Globex'), (3, 'Soylent'), (4, 'Initech');
INSERT INTO Invoices VALUES
(101, 1, 1500.00), -- Over 1000
(102, 2, 800.00),  -- Under 1000
(103, 2, 450.00),  -- Under 1000
(104, NULL, 5000.00); -- NULL client_id over 1000!
-- Initech has zero invoices. Soylent has zero invoices.
```

#### 3. Optimal SQL Solution Query
```sql
-- Solution using NOT IN with NULL safety
SELECT client_id, client_name
FROM Clients
WHERE client_id NOT IN (
    SELECT client_id 
    FROM Invoices 
    WHERE amount > 1000.00 
      AND client_id IS NOT NULL
)
ORDER BY client_id;
```
*(Or the universally safer NOT EXISTS)*:
```sql
SELECT c.client_id, c.client_name
FROM Clients c
WHERE NOT EXISTS (
    SELECT 1 
    FROM Invoices i 
    WHERE i.client_id = c.client_id 
      AND i.amount > 1000.00
)
ORDER BY c.client_id;
```

#### 4. Expected Result
| client_id | client_name |
|---|---|
| 2 | Globex |
| 3 | Soylent |
| 4 | Initech |

#### 5. Common Pitfalls & Exam Traps
- **THE DEADLY `NOT IN (NULL)` TRAP:** If the subquery evaluates to a set containing a `NULL` (e.g. `{1, NULL}`), then `client_id NOT IN (1, NULL)` expands to:
  `client_id <> 1 AND client_id <> NULL`.
  Since `client_id <> NULL` is `UNKNOWN`, the entire condition evaluates to `UNKNOWN` or `FALSE` for every single row! **The query returns zero rows!**
  Always filter out `NULL` in `NOT IN` subqueries or use `NOT EXISTS`.

---

### Challenge 20: Departmental Pay Leaders (Correlated Subquery)
**Category:** Correlated Subqueries  
**Difficulty:** ⭐⭐⭐ Hard

#### 1. Problem Statement
Find all employees who earn strictly more than the average salary of **their own department**.
Display: `emp_id`, `emp_name`, `dept_id`, and `salary`.
Order by `dept_id`, then `salary` descending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE DeptStaff (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    dept_id INT,
    salary DECIMAL(10, 2)
);

INSERT INTO DeptStaff VALUES
(1, 'Alice', 10, 95000.00),  -- Dept 10 avg: (95k + 75k + 70k) / 3 = 80000 -> KEEP
(2, 'Bob', 10, 75000.00),
(3, 'Charlie', 10, 70000.00),
(4, 'Diana', 20, 60000.00),  -- Dept 20 avg: (60k + 40k) / 2 = 50000 -> KEEP
(5, 'Evan', 20, 40000.00),
(6, 'Fiona', 30, 85000.00);  -- Dept 30 avg: 85000 -> NOT strictly greater
```

#### 3. Optimal SQL Solution Query
```sql
SELECT e.emp_id, e.emp_name, e.dept_id, e.salary
FROM DeptStaff e
WHERE e.salary > (
    SELECT AVG(d.salary)
    FROM DeptStaff d
    WHERE d.dept_id = e.dept_id
)
ORDER BY e.dept_id, e.salary DESC;
```

#### 4. Expected Result
| emp_id | emp_name | dept_id | salary |
|---|---|---|---|
| 1 | Alice | 10 | 95000.00 |
| 4 | Diana | 20 | 60000.00 |

#### 5. Common Pitfalls & Exam Traps
- **Scope resolution:** In a correlated subquery, the inner query references the outer query row via `e.dept_id`. The inner query executes once for *every candidate row* evaluated by the outer query. Forgetting the correlation condition `WHERE d.dept_id = e.dept_id` calculates the global company average instead!

---

### Challenge 21: The N-th Highest Salary Without Window Functions
**Category:** Correlated Subqueries  
**Difficulty:** ⭐⭐⭐ Hard

#### 1. Problem Statement
Find the **2nd highest distinct salary** in the `Compensation` table without using window functions (`DENSE_RANK()`) or `LIMIT / OFFSET`. This is the classic university viva and written examination question.
Also explain how the formula generalizes to the $N$-th highest salary.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE Compensation (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO Compensation VALUES
(1, 'Alice', 120000.00),  -- 1st highest
(2, 'Bob', 120000.00),    -- Tied 1st highest
(3, 'Charlie', 95000.00), -- 2nd highest distinct!
(4, 'Diana', 95000.00),   -- Tied 2nd highest
(5, 'Evan', 80000.00),    -- 3rd highest
(6, 'Fiona', 70000.00);   -- 4th highest
```

#### 3. Optimal SQL Solution Query
```sql
-- Standard Approach for 2nd Highest:
SELECT MAX(salary) AS second_highest_salary
FROM Compensation
WHERE salary < (SELECT MAX(salary) FROM Compensation);

-- General Correlated Subquery Approach for N-th Highest (Here N = 2):
-- Finds the salary where exactly (N - 1) distinct salaries are strictly greater than it.
SELECT DISTINCT c1.salary AS nth_highest_salary
FROM Compensation c1
WHERE (
    SELECT COUNT(DISTINCT c2.salary)
    FROM Compensation c2
    WHERE c2.salary > c1.salary
) = 1; -- For 2nd highest, (N - 1) = 2 - 1 = 1
```

#### 4. Expected Result
| second_highest_salary |
|---|---|
| 95000.00 |

#### 5. Common Pitfalls & Exam Traps
- **Using `LIMIT 1 OFFSET 1` without DISTINCT:** Because Alice and Bob are tied at 120,000, `ORDER BY salary DESC LIMIT 1 OFFSET 1` returns 120,000! You must use `DISTINCT`.
- **Exam strictness:** Many professors explicitly forbid `LIMIT` in theoretical exams because `LIMIT` is non-standard SQL (Oracle uses `ROWNUM` / `FETCH FIRST`, SQL Server uses `TOP`). The correlated `COUNT(DISTINCT c2.salary) = N - 1` formula is 100% ANSI compliant on every database on earth.

---

### Challenge 22: Relational Division via Double Negation (EXISTS / NOT EXISTS)
**Category:** Universal Quantification  
**Difficulty:** ⭐⭐⭐ Hard

#### 1. Problem Statement
Find all students who have enrolled in **EVERY** course offered in the `MandatoryCourses` catalog.
This represents the classic mathematical **Relational Division** operator ($A \div B$).
Formulate this using correlated `NOT EXISTS` (double negation: "Find students for whom there does NOT exist a mandatory course that they have NOT enrolled in").

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE DivStudents (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE MandatoryCourses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50)
);

CREATE TABLE CourseRegistrations (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO DivStudents VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO MandatoryCourses VALUES (101, 'DB'), (102, 'OS'), (103, 'Networks');

-- Alice enrolled in all 3
INSERT INTO CourseRegistrations VALUES (1, 101), (1, 102), (1, 103);
-- Bob enrolled in 2 (DB, OS)
INSERT INTO CourseRegistrations VALUES (2, 101), (2, 102);
-- Charlie enrolled in 1 (Networks)
INSERT INTO CourseRegistrations VALUES (3, 103);
```

#### 3. Optimal SQL Solution Query
```sql
SELECT s.student_id, s.student_name
FROM DivStudents s
WHERE NOT EXISTS (
    SELECT c.course_id
    FROM MandatoryCourses c
    WHERE NOT EXISTS (
        SELECT 1
        FROM CourseRegistrations r
        WHERE r.student_id = s.student_id
          AND r.course_id = c.course_id
    )
);
```

#### 4. Expected Result
| student_id | student_name |
|---|---|
| 1 | Alice |

#### 5. Common Pitfalls & Exam Traps
- **Attempting `COUNT(DISTINCT course_id) = (SELECT COUNT(*) FROM MandatoryCourses)`:** While group counting works for simple cases, it breaks down if students take optional courses outside the mandatory catalog, or if courses change. In university theory exams, professors explicitly test the `NOT EXISTS ... NOT EXISTS` double negation pattern.

---

# SECTION 7: SET OPERATIONS

---

### Challenge 23: Consolidating Directories (UNION vs UNION ALL)
**Category:** Set Operations  
**Difficulty:** ⭐ Easy

#### 1. Problem Statement
A company maintains two contact tables: `Suppliers` and `Customers`.
Write a query to create a unified marketing phone directory.
1. Extract name, phone, and party type (`'Supplier'` or `'Customer'`).
2. Then write a second query to extract only the unique phone numbers across both tables, comparing `UNION` vs `UNION ALL`.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE ContactsSuppliers (
    supp_id INT PRIMARY KEY,
    supp_name VARCHAR(50),
    phone VARCHAR(20)
);

CREATE TABLE ContactsCustomers (
    cust_id INT PRIMARY KEY,
    cust_name VARCHAR(50),
    phone VARCHAR(20)
);

INSERT INTO ContactsSuppliers VALUES
(1, 'Industrial Steel Ltd', '555-0100'),
(2, 'Apex Fasteners', '555-0200'),
(3, 'Metro Logistics', '555-0300');

INSERT INTO ContactsCustomers VALUES
(101, 'Global Retail', '555-0400'),
(102, 'Apex Fasteners', '555-0200'); -- Shares phone with Supplier #2
```

#### 3. Optimal SQL Solution Query
```sql
-- Query 1: Tagged contact list
SELECT supp_name AS contact_name, phone, 'Supplier' AS party_type 
FROM ContactsSuppliers
UNION ALL
SELECT cust_name AS contact_name, phone, 'Customer' AS party_type 
FROM ContactsCustomers
ORDER BY contact_name;

-- Query 2: Pure unique phone numbers
SELECT phone FROM ContactsSuppliers
UNION
SELECT phone FROM ContactsCustomers
ORDER BY phone;
```

#### 4. Expected Result
**Query 2 Output (De-duplicated):**
| phone |
|---|
| 555-0100 |
| 555-0200 |
| 555-0300 |
| 555-0400 |

#### 5. Common Pitfalls & Exam Traps
- **UNION vs UNION ALL Performance:** `UNION` performs an internal sort/hash to remove duplicate rows. `UNION ALL` simply concatenates result sets without deduplication and is much faster.
- **Column compatibility:** The number and data types of columns in all `SELECT` statements must match.

---

### Challenge 24: Technical Skill Gap Analysis (INTERSECT & EXCEPT)
**Category:** Set Operations  
**Difficulty:** ⭐⭐ Medium

#### 1. Problem Statement
The hiring department maintains candidate certifications:
`Certifications (candidate_id, candidate_name, skill_name)`.
Write two queries:
- **Part A:** Find names of candidates who are certified in **BOTH** `'SQL'` and `'Python'` (use `INTERSECT`).
- **Part B:** Find names of candidates who are certified in `'SQL'` but **NOT** in `'Python'` (use `EXCEPT` / `MINUS`).

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE CandidateSkills (
    candidate_id INT,
    candidate_name VARCHAR(50),
    skill_name VARCHAR(30)
);

INSERT INTO CandidateSkills VALUES
(1, 'Alice', 'SQL'),
(1, 'Alice', 'Python'),
(1, 'Alice', 'Docker'),
(2, 'Bob', 'SQL'),
(2, 'Bob', 'Java'),
(3, 'Charlie', 'Python'),
(4, 'Diana', 'SQL'),
(4, 'Diana', 'Python');
```

#### 3. Optimal SQL Solution Query
```sql
-- Part A: Certified in BOTH SQL and Python
SELECT candidate_name
FROM CandidateSkills
WHERE skill_name = 'SQL'
INTERSECT
SELECT candidate_name
FROM CandidateSkills
WHERE skill_name = 'Python'
ORDER BY candidate_name;

-- Part B: Certified in SQL but NOT Python
SELECT candidate_name
FROM CandidateSkills
WHERE skill_name = 'SQL'
EXCEPT
SELECT candidate_name
FROM CandidateSkills
WHERE skill_name = 'Python'
ORDER BY candidate_name;
```

#### 4. Expected Result
**Part A (BOTH SQL & Python):**
| candidate_name |
|---|
| Alice |
| Diana |

**Part B (SQL but NOT Python):**
| candidate_name |
|---|
| Bob |

#### 5. Common Pitfalls & Exam Traps
- **Dialect Difference:** In Oracle, the operator is `MINUS`. In ANSI SQL, PostgreSQL, SQLite, and MS SQL Server, the operator is `EXCEPT`. In exams, always note: *"EXCEPT (or MINUS in Oracle)"*.

---

# SECTION 8: COMPREHENSIVE CAPSTONE EXAM CHALLENGE

---

### Challenge 25: Executive Departmental Health & Analytics Dashboard
**Category:** Comprehensive Capstone (DDL, Aggregates, Multi-Table Joins, Subqueries, Conditional CASE)  
**Difficulty:** ⭐⭐⭐ Hard

#### 1. Problem Statement
Produce an end-to-end organizational audit report for executive leadership across `Departments`, `Staffers`, and `ProjectWork`.
For every department:
1. `dept_name`: Name of the department.
2. `total_staff`: Total employees assigned. Include departments with 0 staff!
3. `active_projects`: Count of distinct projects staff in this department are assigned to.
4. `total_payroll`: Total monthly salary spend (0 if no staff).
5. `avg_salary`: Average employee salary rounded to 2 decimals (0 if no staff).
6. `compensation_tier`:
   - `'Tier 1 - High'` if average salary >= \$80,000.
   - `'Tier 2 - Mid'` if average salary is between \$50,000 and \$79,999.
   - `'Tier 3 - Entry'` if average salary > 0 and < \$50,000.
   - `'Unstaffed'` if no staff.
Order by `total_payroll` descending, then `dept_name` ascending.

#### 2. Table Schema & Seed Data
```sql
CREATE TABLE OrgDepts (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE OrgStaff (
    staff_id INT PRIMARY KEY,
    staff_name VARCHAR(50) NOT NULL,
    dept_id INT,
    salary DECIMAL(10, 2),
    FOREIGN KEY (dept_id) REFERENCES OrgDepts(dept_id)
);

CREATE TABLE OrgAssignments (
    staff_id INT,
    proj_code VARCHAR(10),
    PRIMARY KEY (staff_id, proj_code),
    FOREIGN KEY (staff_id) REFERENCES OrgStaff(staff_id)
);

INSERT INTO OrgDepts VALUES (10, 'Engineering'), (20, 'Research'), (30, 'Operations'), (40, 'Incubation');
INSERT INTO OrgStaff VALUES
(1, 'Alice', 10, 95000.00),
(2, 'Bob', 10, 85000.00),
(3, 'Charlie', 20, 72000.00),
(4, 'Diana', 30, 42000.00),
(5, 'Evan', 30, 46000.00);
-- Incubation (40) has no staff.

INSERT INTO OrgAssignments VALUES
(1, 'PRJ-A'), (1, 'PRJ-B'), (2, 'PRJ-A'), -- Eng has 2 distinct projects (PRJ-A, PRJ-B)
(3, 'PRJ-C'),                             -- Res has 1 distinct project
(4, 'PRJ-D');                             -- Ops has 1 distinct project (Evan not assigned)
```

#### 3. Optimal SQL Solution Query
```sql
SELECT 
    d.dept_name,
    COUNT(DISTINCT s.staff_id) AS total_staff,
    COUNT(DISTINCT a.proj_code) AS active_projects,
    COALESCE(SUM(s.salary), 0.00) AS total_payroll,
    COALESCE(ROUND(AVG(s.salary), 2), 0.00) AS avg_salary,
    CASE 
        WHEN COUNT(s.staff_id) = 0 THEN 'Unstaffed'
        WHEN AVG(s.salary) >= 80000.00 THEN 'Tier 1 - High'
        WHEN AVG(s.salary) >= 50000.00 THEN 'Tier 2 - Mid'
        ELSE 'Tier 3 - Entry'
    END AS compensation_tier
FROM OrgDepts d
LEFT JOIN OrgStaff s ON d.dept_id = s.dept_id
LEFT JOIN OrgAssignments a ON s.staff_id = a.staff_id
GROUP BY d.dept_id, d.dept_name
ORDER BY total_payroll DESC, d.dept_name ASC;
```

#### 4. Expected Result
| dept_name | total_staff | active_projects | total_payroll | avg_salary | compensation_tier |
|---|---|---|---|---|---|
| Engineering | 2 | 2 | 180000.00 | 90000.00 | Tier 1 - High |
| Operations | 2 | 1 | 88000.00 | 44000.00 | Tier 3 - Entry |
| Research | 1 | 1 | 72000.00 | 72000.00 | Tier 2 - Mid |
| Incubation | 0 | 0 | 0.00 | 0.00 | Unstaffed |

#### 5. Common Pitfalls & Exam Traps
- **The Multiple-Join Multiplication Trap:** When joining `OrgStaff` with `OrgAssignments`, Alice has two assignments (`PRJ-A`, `PRJ-B`). If you write `COUNT(s.staff_id)`, Alice will be counted TWICE, making Engineering staff count appear as 3! You MUST use `COUNT(DISTINCT s.staff_id)` and `COUNT(DISTINCT a.proj_code)`.
- **Forgetting `d.dept_id` in GROUP BY:** Always include primary key columns in `GROUP BY` to handle departments that share identical names.

---
*End of DBMS Practical Coding Challenges. Master these 25 challenges to guarantee a top score in practical lab exams!*

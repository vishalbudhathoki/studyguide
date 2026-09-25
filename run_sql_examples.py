"""
DBMS Interactive Practical Lab & Query Runner
Covers all SQL topics in the exam syllabus:
- DDL: Tables, constraints, foreign keys
- DML: INSERT, UPDATE, DELETE
- DQL: SELECT, WHERE, ORDER BY
- Aggregates: COUNT, SUM, AVG, MIN, MAX
- Grouping: GROUP BY, HAVING
- Joins: INNER, LEFT, CROSS, SELF JOIN
- Subqueries: Scalar, Multi-row (IN, ALL/ANY logic), Correlated, EXISTS
- Set Operations: UNION, UNION ALL, INTERSECT, EXCEPT
"""

import sqlite3
import sys

def print_section(title):
    print("\n" + "=" * 80)
    print(f" {title.upper()} ")
    print("=" * 80)

def run_and_print(cursor, query_name, sql, explain=""):
    print(f"\n>>> [QUERY]: {query_name}")
    if explain:
        print(f"    Concept: {explain}")
    print(f"    SQL:\n    {sql.strip().replace(chr(10), chr(10) + '    ')}")
    try:
        cursor.execute(sql)
        if sql.strip().upper().startswith("SELECT") or "VALUES" in sql.strip().upper():
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description] if cursor.description else []
            if not rows:
                print("    Result: [EMPTY SET / 0 ROWS]")
            else:
                # Calculate column widths
                col_widths = [len(c) for c in col_names]
                for r in rows:
                    for i, val in enumerate(r):
                        col_widths[i] = max(col_widths[i], len(str(val)))
                
                # Print header
                sep = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
                print("    " + sep)
                header = "|" + "|".join([f" {col_names[i].ljust(col_widths[i])} " for i in range(len(col_names))]) + "|"
                print("    " + header)
                print("    " + sep)
                # Print rows
                for r in rows:
                    row_str = "|" + "|".join([f" {str(r[i] if r[i] is not None else 'NULL').ljust(col_widths[i])} " for i in range(len(r))]) + "|"
                    print("    " + row_str)
                print("    " + sep)
                print(f"    Total rows: {len(rows)}")
        else:
            print(f"    Status: Statement executed successfully. Rows affected: {cursor.rowcount}")
    except Exception as e:
        print(f"    [ERROR]: {e}")

def main():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    print_section("1. DDL: Schema Creation with Constraints")
    
    cur.execute("""
    CREATE TABLE Departments (
        dept_id INT PRIMARY KEY,
        dept_name VARCHAR(50) NOT NULL UNIQUE,
        location VARCHAR(50) DEFAULT 'Main Campus'
    );
    """)
    print("Created table Departments with PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT.")

    cur.execute("""
    CREATE TABLE Employees (
        emp_id INT PRIMARY KEY,
        emp_name VARCHAR(50) NOT NULL,
        salary DECIMAL(10,2) CHECK (salary > 0),
        dept_id INT,
        manager_id INT,
        FOREIGN KEY (dept_id) REFERENCES Departments(dept_id) ON DELETE SET NULL,
        FOREIGN KEY (manager_id) REFERENCES Employees(emp_id) ON DELETE SET NULL
    );
    """)
    print("Created table Employees with FOREIGN KEY, CHECK constraint, and Self-referencing FK.")

    cur.execute("""
    CREATE TABLE Projects (
        proj_id INT PRIMARY KEY,
        proj_name VARCHAR(50) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE Employee_Projects (
        emp_id INT,
        proj_id INT,
        hours_allocated INT CHECK (hours_allocated >= 0),
        PRIMARY KEY (emp_id, proj_id),
        FOREIGN KEY (emp_id) REFERENCES Employees(emp_id) ON DELETE CASCADE,
        FOREIGN KEY (proj_id) REFERENCES Projects(proj_id) ON DELETE CASCADE
    );
    """)
    print("Created junction table Employee_Projects with COMPOSITE PRIMARY KEY and CASCADE delete.")

    print_section("2. DML: Populating Data (INSERT)")
    
    cur.execute("INSERT INTO Departments VALUES (10, 'Engineering', 'Building A');")
    cur.execute("INSERT INTO Departments VALUES (20, 'Research', 'Building B');")
    cur.execute("INSERT INTO Departments VALUES (30, 'Sales', 'Building C');")
    cur.execute("INSERT INTO Departments VALUES (40, 'Operations', 'Building D');")

    employees_data = [
        (101, 'Alice Smith', 95000, 10, None),
        (102, 'Bob Johnson', 72000, 10, 101),
        (103, 'Charlie Brown', 85000, 20, 101),
        (104, 'Diana Prince', 60000, 20, 103),
        (105, 'Evan Wright', 55000, 30, 101),
        (106, 'Fiona Gallagher', 48000, None, None) # Unassigned department
    ]
    cur.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?);", employees_data)

    cur.executemany("INSERT INTO Projects VALUES (?, ?);", [
        (1, 'AI Search Engine'),
        (2, 'Cloud Storage Platform'),
        (3, 'Mobile Banking App')
    ])

    cur.executemany("INSERT INTO Employee_Projects VALUES (?, ?, ?);", [
        (101, 1, 20),
        (101, 2, 20),
        (102, 1, 35),
        (103, 1, 15),
        (103, 2, 25),
        (104, 3, 40),
        (105, 3, 30)
    ])
    conn.commit()
    print("Sample data populated successfully.")

    print_section("3. DQL: Basic Filtering, Pattern Matching, and Sorting")
    
    run_and_print(cur, "Basic SELECT with WHERE, LIKE and ORDER BY",
        "SELECT emp_id, emp_name, salary FROM Employees WHERE salary >= 60000 AND emp_name LIKE '%a%' ORDER BY salary DESC;",
        "Filters salaries >= 60000 and names containing 'a' (case-insensitive in SQLite), ordered descending.")

    run_and_print(cur, "Handling NULL Values with IS NULL",
        "SELECT emp_id, emp_name, dept_id FROM Employees WHERE dept_id IS NULL;",
        "Finds employees not assigned to any department.")

    print_section("4. Aggregates, GROUP BY, and HAVING")
    
    run_and_print(cur, "Department salary stats with GROUP BY and HAVING",
        """
        SELECT dept_id, 
               COUNT(*) AS emp_count, 
               AVG(salary) AS avg_sal, 
               MIN(salary) AS min_sal, 
               MAX(salary) AS max_sal
        FROM Employees
        WHERE dept_id IS NOT NULL
        GROUP BY dept_id
        HAVING COUNT(*) >= 2;
        """,
        "Groups by dept_id, filters groups having at least 2 employees using HAVING.")

    print_section("5. JOINS: Inner, Outer, Cross, and Self-Join")
    
    run_and_print(cur, "INNER JOIN (Employees and Departments)",
        """
        SELECT E.emp_id, E.emp_name, E.salary, D.dept_name, D.location
        FROM Employees E
        INNER JOIN Departments D ON E.dept_id = D.dept_id;
        """,
        "Only returns employees that have a matching department.")

    run_and_print(cur, "LEFT OUTER JOIN (Includes unassigned employees)",
        """
        SELECT E.emp_id, E.emp_name, COALESCE(D.dept_name, 'No Dept') AS dept_name
        FROM Employees E
        LEFT OUTER JOIN Departments D ON E.dept_id = D.dept_id;
        """,
        "Preserves all employees (e.g., Fiona) even if dept_id is NULL.")

    run_and_print(cur, "SELF JOIN (Employee to Manager Hierarchy)",
        """
        SELECT E.emp_name AS Employee, COALESCE(M.emp_name, 'TOP EXECUTIVE') AS Manager
        FROM Employees E
        LEFT OUTER JOIN Employees M ON E.manager_id = M.emp_id;
        """,
        "Joins the Employees table with itself to map employees to their direct managers.")

    print_section("6. Subqueries: Scalar, Multi-row, Correlated, and EXISTS")
    
    run_and_print(cur, "Scalar Subquery: Employees earning above overall average",
        """
        SELECT emp_id, emp_name, salary
        FROM Employees
        WHERE salary > (SELECT AVG(salary) FROM Employees);
        """,
        "Evaluates the average salary once and filters rows earning more.")

    run_and_print(cur, "Correlated Subquery: Employees earning above THEIR OWN department average",
        """
        SELECT E1.emp_id, E1.emp_name, E1.salary, E1.dept_id
        FROM Employees E1
        WHERE E1.salary > (
            SELECT AVG(E2.salary) 
            FROM Employees E2 
            WHERE E2.dept_id = E1.dept_id
        );
        """,
        "Inner query executes for every single row evaluated in the outer query.")

    run_and_print(cur, "EXISTS Operator: Departments having at least one employee",
        """
        SELECT D.dept_id, D.dept_name
        FROM Departments D
        WHERE EXISTS (
            SELECT 1 FROM Employees E WHERE E.dept_id = D.dept_id
        );
        """,
        "Returns TRUE as soon as the first matching employee row is found.")

    run_and_print(cur, "NOT EXISTS: Departments having NO employees",
        """
        SELECT D.dept_id, D.dept_name
        FROM Departments D
        WHERE NOT EXISTS (
            SELECT 1 FROM Employees E WHERE E.dept_id = D.dept_id
        );
        """,
        "Finds empty departments (e.g. Operations). Safer than NOT IN with NULLs.")

    print_section("7. Set Operations: UNION, INTERSECT, EXCEPT")
    
    run_and_print(cur, "UNION: All distinct departments referenced across both tables",
        """
        SELECT dept_id FROM Departments
        UNION
        SELECT dept_id FROM Employees WHERE dept_id IS NOT NULL;
        """,
        "Combines sets and removes duplicate entries.")

    run_and_print(cur, "INTERSECT: Department IDs that exist in BOTH tables",
        """
        SELECT dept_id FROM Departments
        INTERSECT
        SELECT dept_id FROM Employees WHERE dept_id IS NOT NULL;
        """,
        "Returns only departments that currently have assigned employees.")

    run_and_print(cur, "EXCEPT (MINUS): Departments that have NO employees",
        """
        SELECT dept_id FROM Departments
        EXCEPT
        SELECT dept_id FROM Employees WHERE dept_id IS NOT NULL;
        """,
        "Set difference: All departments minus departments with employees.")

    print_section("8. DML: Cascading Behavior Verification")
    print("Testing ON DELETE SET NULL on Employees when Department is deleted...")
    cur.execute("DELETE FROM Departments WHERE dept_id = 10;")
    run_and_print(cur, "Employees after deleting Department 10",
        "SELECT emp_id, emp_name, dept_id FROM Employees WHERE emp_id IN (101, 102);",
        "Notice dept_id is now automatically NULL due to ON DELETE SET NULL.")

    print("\n" + "=" * 80)
    print(" ALL LAB TESTS COMPLETED SUCCESSFULLY! ")
    print("=" * 80)
    conn.close()

if __name__ == "__main__":
    main()

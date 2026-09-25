# DBMS EXAM RAPID REVISION & HIGH-YIELD CHEAT SHEET
**Target: 100% Score in University / College / Competitive Exams**

---

## 📑 TABLE OF CONTENTS
1. [Core Notation & Symbol Cheat Sheet](#1-core-notation--symbol-cheat-sheet)
2. [The "Top 20 Distinguish Between" Master Tables](#2-the-top-20-distinguish-between-master-tables)
3. [The Golden Conversion Algorithm (ER to Relational Schema)](#3-the-golden-conversion-algorithm-er-to-relational-schema)
4. [Relational Algebra Operator Quick Reference](#4-relational-algebra-operator-quick-reference)
5. [SQL Logical Execution Order & Clause Map](#5-sql-logical-execution-order--clause-map)
6. [SQL Join Matrix (Visual Guide & Traps)](#6-sql-join-matrix-visual-guide--traps)
7. [Subquery Archetypes & The NULL Danger](#7-subquery-archetypes--the-null-danger)
8. [High-Frequency Viva / Short-Answer Questions](#8-high-frequency-viva--short-answer-questions)
9. [Exam Hall Golden Rules & Mark-Maximizing Strategy](#9-exam-hall-golden-rules--mark-maximizing-strategy)

---

## 1. CORE NOTATION & SYMBOL CHEAT SHEET

### A. Entity-Relationship (ER) Diagram Symbols (Chen Notation)
| Shape / Symbol | Meaning | Example |
| :--- | :--- | :--- |
| **Rectangle** | Strong Entity Set | `Student`, `Employee` |
| **Double Rectangle** | Weak Entity Set | `Dependent`, `Loan_Payment` |
| **Diamond** | Relationship Set | `Enrolled_In`, `Works_For` |
| **Double Diamond** | Identifying Relationship (for Weak Entity) | `Dependents_Of` |
| **Ellipse / Oval** | Attribute | `Age`, `Salary` |
| **Underlined Text in Ellipse** | Primary Key (Identifier) | `<u>Roll_No</u>`, `<u>Emp_ID</u>` |
| **Dashed / Dotted Underlined Text**| Partial Key / Discriminator (Weak Entity)| `Name` in `Dependent` |
| **Double Ellipse** | Multivalued Attribute | `Phone_Numbers`, `Skills` |
| **Dashed / Dotted Ellipse** | Derived Attribute | `Age` (derived from `DOB`) |
| **Component Ellipses connected to Ellipse** | Composite Attribute | `Address` (`City`, `Zip`, `Street`) |
| **Double Line (between Entity and Relationship)** | Total Participation (Existence Dependency) | Every student must be enrolled |
| **Single Line (between Entity and Relationship)** | Partial Participation | Some instructors may not advise |
| **Arrow pointing to Entity** | Cardinality "1" (One) | One department head |
| **Undirected Line to Entity** | Cardinality "Many" | Many employees in department |

---

### B. Relational Algebra Formal Notations
| Symbol | Operation Name | Formal Syntax | Meaning |
| :--- | :--- | :--- | :--- |
| $\sigma$ (sigma) | Selection | $\sigma_{predicate}(R)$ | Filters rows (horizontal slicing) |
| $\Pi$ (pi) | Projection | $\Pi_{A_1, A_2, \dots, A_k}(R)$ | Selects columns, removes duplicates |
| $\times$ | Cartesian Product | $R \times S$ | All pairwise combinations of tuples |
| $\cup$ | Union | $R \cup S$ | Tuples in $R$ or $S$ or both (must be union-compatible) |
| $\cap$ | Intersection | $R \cap S$ | Tuples present in both $R$ and $S$ |
| $-$ | Set Difference | $R - S$ | Tuples in $R$ that are NOT in $S$ |
| $\bowtie$ | Natural Join | $R \bowtie S$ | Equijoin on all common attribute names |
| $\bowtie_{\theta}$ | Theta Join | $R \bowtie_{R.A > S.B} S$ | Condition-based join |
| $\div$ | Division | $R \div S$ | "Find tuples in $R$ associated with ALL tuples in $S$" |
| $\rho$ (rho) | Rename | $\rho_{S}(R)$ or $\rho_{S(B_1, \dots, B_n)}(R)$ | Renames relation and/or attributes |
| $\leftouterjoin$ | Left Outer Join | $R \leftouterjoin S$ | All $R$ tuples + matched $S$ (unmatched padded with NULL) |
| $\rightouterjoin$ | Right Outer Join | $R \rightouterjoin S$ | All $S$ tuples + matched $R$ |
| $\fullouterjoin$ | Full Outer Join | $R \fullouterjoin S$ | All tuples from both sides padded with NULL |

---

## 2. THE "TOP 20 DISTINGUISH BETWEEN" MASTER TABLES
*(Examiners frequently allocate 30–40% of marks to comparison questions. Learn these exact technical distinctions).*

### Comparison 1: File Processing System vs. DBMS
| Feature | File Processing System | Database Management System (DBMS) |
| :--- | :--- | :--- |
| **Data Redundancy** | High; same data duplicated across isolated files | Minimal; centralized control avoids redundant storage |
| **Data Inconsistency** | High; updates to one file do not propagate to others | Avoided; single source of truth ensures consistency |
| **Data Isolation** | Data scattered in different files and formats | Unified; standard relational schemas |
| **Data Access** | Requires writing new programs in C/C++/Java for queries | Declarative querying via SQL without procedural code |
| **Integrity Checks** | Enforced manually inside application code | Enforced automatically by DBMS constraints (`CHECK`, `FK`) |
| **Concurrency Control** | Absent or crude file-level locking; leads to anomalies | Granular (row/page/table level), strict ACID compliance |
| **Crash Recovery** | Difficult; partial updates leave files corrupted | Automatic via write-ahead logging (WAL) and checkpoints |
| **Security** | Basic OS file permissions (read/write/execute) | Granular access control via DCL (`GRANT`, `REVOKE`) |

---

### Comparison 2: Schema vs. Instance
| Dimension | Schema | Instance |
| :--- | :--- | :--- |
| **Definition** | The overall structural design and blueprint of the database | The actual data populated in the database at a specific snapshot in time |
| **Analogy in Programming** | Class definition / Data type (e.g., `struct Student`) | An object instance / Variable value at runtime |
| **Frequency of Change** | Rarely changed (requires DDL schema migration) | Changes frequently with every `INSERT`, `UPDATE`, `DELETE` |
| **State** | Static | Dynamic |
| **Example** | `STUDENT(RollNo INT, Name VARCHAR, GPA FLOAT)` | `(101, 'Alice', 3.9), (102, 'Bob', 3.5)` at 10:00 AM |

---

### Comparison 3: Physical vs. Logical Data Independence
| Characteristic | Physical Data Independence | Logical Data Independence |
| :--- | :--- | :--- |
| **Definition** | Capacity to change internal physical storage/indices without altering logical schema | Capacity to modify conceptual schema without altering external views/programs |
| **Level Affected** | Internal / Physical Level $\leftrightarrow$ Conceptual Level | Conceptual Level $\leftrightarrow$ External / View Level |
| **Difficulty to Achieve** | Easier to achieve | Much harder to achieve |
| **Trigger Examples** | Changing B+ Tree to Hash index; moving from SSD to HDD; compression | Splitting an entity, adding new attributes, modifying relationships |
| **Impact on Users** | Zero impact on user queries and application logic | Existing queries continue working through views |

---

### Comparison 4: Strong Entity Set vs. Weak Entity Set
| Parameter | Strong Entity Set | Weak Entity Set |
| :--- | :--- | :--- |
| **Primary Key** | Possesses its own unique Primary Key | Does not possess sufficient attributes to form a Primary Key |
| **Identifier** | Independent identifier | Partial Key (Discriminator) + Primary Key of Identifying Entity |
| **Existence Dependency** | Independent of any other entity | Existence dependent on Owner/Identifying entity |
| **ER Diagram Symbol** | Single rectangle | Double rectangle |
| **Relationship Symbol**| Single diamond | Double diamond (Identifying relationship) |
| **Participation** | Can be partial or total | Always **Total** in the identifying relationship |
| **Example** | `EMPLOYEE (Emp_ID, Name, Salary)` | `DEPENDENT (Emp_ID, Dep_Name, Age, Relation)` |

---

### Comparison 5: Super Key vs. Candidate Key vs. Primary Key vs. Alternate Key
```
┌────────────────────────────────────────────────────────┐
│                      SUPER KEYS                        │
│   (Any set of attributes that uniquely identifies)     │
│   ┌────────────────────────────────────────────────┐   │
│   │                CANDIDATE KEYS                  │   │
│   │         (MINIMAL Super Keys - No fat)          │   │
│   │   ┌───────────────┐        ┌───────────────┐   │   │
│   │   │  PRIMARY KEY  │        │ ALTERNATE KEY │   │   │
│   │   │ (Selected 1)  │        │ (Remaining CK)│   │   │
│   │   └───────────────┘        └───────────────┘   │   │
│   └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```
| Key Type | Formal Definition | Example in `STUDENT(RollNo, RegNo, Email, Name)` |
| :--- | :--- | :--- |
| **Super Key** | Any set of attributes whose values uniquely identify a tuple. May contain redundant attributes. | `{RollNo}`, `{RollNo, Name}`, `{RegNo, Email, Name}` |
| **Candidate Key** | A **minimal** super key; no proper subset is a super key. | `{RollNo}`, `{RegNo}`, `{Email}` |
| **Primary Key** | The single candidate key selected by the DBA to uniquely identify tuples. Cannot be `NULL`. | `{RollNo}` |
| **Alternate Key** | Candidate keys that were **not** chosen as the Primary Key. | `{RegNo}`, `{Email}` |
| **Foreign Key** | Attribute(s) in relation $R_1$ that reference the Primary Key of relation $R_2$. | `Dept_ID` in `EMPLOYEE` referencing `DEPARTMENT` |

---

### Comparison 6: Primary Key vs. Unique Key Constraint
| Feature | PRIMARY KEY | UNIQUE Constraint |
| :--- | :--- | :--- |
| **NULL values** | Strictly **NO** `NULL` values permitted | Permits `NULL` values (usually one or multiple depending on SQL engine) |
| **Limit per Table** | Exactly **ONE** Primary Key per table | **Multiple** `UNIQUE` constraints allowed per table |
| **Index Generated** | Clustered Index (by default in engines like MySQL InnoDB, SQL Server) | Non-clustered Index (by default) |
| **Purpose** | Uniquely identifies each record as the entity identifier | Prevents duplicate entries in non-primary columns (e.g., `Email`, `SSN`) |

---

### Comparison 7: DROP vs. TRUNCATE vs. DELETE
| Criterion | DELETE | TRUNCATE | DROP |
| :--- | :--- | :--- | :--- |
| **Command Type** | **DML** (Data Manipulation) | **DDL** (Data Definition) | **DDL** (Data Definition) |
| **Scope** | Deletes specific rows (or all rows if no `WHERE`) | Removes **ALL** rows in the table | Deletes table schema, data, indices, triggers |
| **WHERE Clause** | **Supported** (`WHERE age < 18`) | **Not supported** (operates on entire table) | **Not supported** |
| **Speed / Performance** | Slow; logs row-by-row deletion | Very Fast; deallocates data pages | Fastest; removes dictionary metadata |
| **Rollback / Undo** | **Can be rolled back** within transaction | **Cannot be rolled back** in standard MySQL/Oracle | **Cannot be rolled back** |
| **Triggers** | Fires `ON DELETE` row triggers | Does **NOT** fire `DELETE` triggers | Does **NOT** fire triggers |
| **Identity / Auto-Increment** | Preserves current auto-increment counter | Resets auto-increment counter to base value | Destroys table entirely |
| **Table Structure** | Preserved | Preserved | **Destroyed** (table no longer exists) |

---

### Comparison 8: WHERE Clause vs. HAVING Clause
| Property | WHERE Clause | HAVING Clause |
| :--- | :--- | :--- |
| **Filtering Target** | Filters individual **rows** before grouping | Filters **groups** after grouping |
| **Aggregate Functions** | **Cannot** contain aggregate functions (`WHERE SUM(sal) > 5000` is **SYNTAX ERROR**) | **Can and usually does** contain aggregates (`HAVING AVG(sal) > 5000`) |
| **Execution Order** | Executes **before** `GROUP BY` | Executes **after** `GROUP BY` |
| **Applicability** | Can be used with `SELECT`, `UPDATE`, `DELETE` | Used almost exclusively with `GROUP BY` in `SELECT` |
| **Index Utilization** | Can utilize B-tree table indexes effectively | Cannot use regular indexes directly (operates on grouped summary) |

---

### Comparison 9: INNER JOIN vs. NATURAL JOIN
| Property | INNER JOIN | NATURAL JOIN |
| :--- | :--- | :--- |
| **Condition Specification** | Explicitly stated using `ON` or `USING` clause (`ON A.id = B.id`) | Implicit; matches on **all columns having identical names and data types** |
| **Duplicate Columns** | Retains duplicate columns unless specified in `SELECT` | Automatically coalesces and returns common columns only **once** |
| **Risk / Maintainability**| Safe and resilient to schema changes | **Dangerous in production**; adding a column with a common name silently breaks logic |
| **Syntax** | `FROM R INNER JOIN S ON R.id = S.id` | `FROM R NATURAL JOIN S` |

---

### Comparison 10: UNION vs. UNION ALL
| Metric | UNION | UNION ALL |
| :--- | :--- | :--- |
| **Duplicate Handling** | Removes duplicate rows (distinct set union) | Retains all duplicates |
| **Performance** | Slower; performs expensive sorting/hashing to deduplicate | Fast; simply appends result sets sequentially |
| **Output Cardinality** | $|R \cup S| \le |R| + |S|$ | $|R \cup_{all} S| = |R| + |S|$ |
| **Memory / CPU Usage** | High memory/tempdb usage due to sort-unique pass | Minimal memory footprint |

---

### Comparison 11: Correlated Subquery vs. Non-Correlated Subquery
| Dimension | Non-Correlated Subquery | Correlated Subquery |
| :--- | :--- | :--- |
| **Dependency** | Independent of outer query | Dependent on column values from the current outer row |
| **Execution Frequency** | Executes **exactly once**; result passed to outer query | Executes **once for every single row** evaluated by outer query |
| **Execution Direction** | Inside-out (inner runs first, then outer) | Outside-in (outer fetches candidate row, inner validates it) |
| **Performance** | Fast ($O(N)$ or $O(N \log M)$) | Slow ($O(N \times M)$) unless optimized by query planner |
| **Example** | `WHERE sal > (SELECT AVG(sal) FROM Emp)` | `WHERE sal > (SELECT AVG(sal) FROM Emp E2 WHERE E2.dept = E1.dept)` |

---

### Comparison 12: IN vs. EXISTS Operator
| Property | `IN` Operator | `EXISTS` Operator |
| :--- | :--- | :--- |
| **Evaluation Mechanism** | Evaluates inner query completely to build list of values, then tests membership | Evaluates row-by-row; stops scanning as soon as 1 match is found (Short-circuit Boolean) |
| **Return Value** | Compares concrete values | Returns Boolean `TRUE` or `FALSE` |
| **Handling of NULL Values** | **Dangerous**: If inner query returns a `NULL`, `NOT IN` returns empty set! | **Safe**: `EXISTS` and `NOT EXISTS` handle `NULL` properly |
| **Best Used When** | Inner subquery result set is very small | Outer query is small and inner query is large with an indexed foreign key |

---

### Comparison 13: 1-Tier vs. 2-Tier vs. 3-Tier Architecture
| Dimension | 1-Tier Architecture | 2-Tier (Client-Server) | 3-Tier Architecture |
| :--- | :--- | :--- | :--- |
| **Separation** | Client, logic, and DB on same machine | Client (Presentation + Logic) $\leftrightarrow$ DB Server | Client $\leftrightarrow$ Application Server $\leftrightarrow$ DB Server |
| **Business Logic** | Embedded in local app | Resides on client or inside stored procedures | Resides on middle-tier Application Server |
| **Security** | Low (direct access to storage) | Medium (direct DB connection credentials on client) | High (clients never touch database directly) |
| **Scalability** | Single user only | Limited (each client consumes DB connection pool) | Highly scalable (connection pooling, load balancing) |
| **Typical Use** | Local MS Access / SQLite testing | Legacy desktop enterprise ERPs | Modern Web and Mobile applications |

---

### Comparison 14: Relational Algebra vs. Relational Calculus (SQL)
| Property | Relational Algebra | Relational Calculus / SQL |
| :--- | :--- | :--- |
| **Paradigm** | **Procedural** query language | **Declarative / Non-procedural** query language |
| **Focus** | Specifies **HOW** to obtain results (order of operations) | Specifies **WHAT** data is required without implementation steps |
| **Target Audience** | Theoretical foundation, DBMS Query Optimizer target | End users, application developers, database engineers |
| **Equivalence** | Algebra and Safe Calculus are mathematically equivalent (Codd's Theorem) | SQL is based on Tuple Relational Calculus (TRC) |

---

### Comparison 15: Specialization vs. Generalization
| Dimension | Generalization | Specialization |
| :--- | :--- | :--- |
| **Direction** | **Bottom-Up** approach | **Top-Down** approach |
| **Process** | Combines multiple lower-level entities into a higher-level entity | Breaks down a higher-level entity into specialized sub-entities |
| **Commonality** | Identifies shared common attributes | Identifies distinctive, subclass-specific attributes |
| **Example** | `Car` and `Truck` generalized into `Vehicle` | `Employee` specialized into `Developer` and `Manager` |

---

## 3. THE GOLDEN CONVERSION ALGORITHM (ER TO RELATIONAL SCHEMA)

```
                       ┌─────────────────────────┐
                       │  ER DIAGRAM CONVERSION  │
                       └────────────┬────────────┘
                                    │
    ┌───────────────┬───────────────┼───────────────┬───────────────┐
    ▼               ▼               ▼               ▼               ▼
1. Strong      2. Weak         3. 1:1 & 1:N    4. M:N          5. Multivalued
   Entity         Entity          Relations       Relations       Attributes
 (Direct PK)    (Owner PK +     (FK on 'N' or   (Junction Table (Separate Table
                 Partial Key)    total side)     Composite PK)   PK = (Owner PK + Attr))
```

### Step 1: Strong Entity Sets
- For each strong entity $E$, create relation $R$.
- Include all simple attributes.
- For composite attributes, include only flat simple components (e.g., `Name` $\rightarrow$ `First_Name`, `Last_Name`).
- **Primary Key**: Same as primary key of $E$.

### Step 2: Weak Entity Sets
- For each weak entity $W$ with owner entity $O$:
- Create relation $R$.
- Include all simple attributes of $W$.
- Add Primary Key of $O$ as Foreign Key in $R$.
- **Primary Key of $R$**: **Composite Key** = $(\text{Primary Key of } O) + (\text{Partial Key / Discriminator of } W)$.
- **Foreign Key constraint**: References $O$ with `ON DELETE CASCADE`.

### Step 3: 1:1 Binary Relationship Sets
Let relationship be $R$ between entities $S$ and $T$:
- **Option A (Total Participation on one side - Preferred)**: Add Primary Key of the partial side as Foreign Key into the relation having **Total Participation**. Also copy any relationship attributes there.
- **Option B (Both Total)**: Merge both entities and the relationship into a single unified table.
- **Option C (Both Partial)**: Choose either table to hold the Foreign Key (add `UNIQUE` constraint to the FK column).

### Step 4: 1:N (or N:1) Binary Relationship Sets
- Identify the entity on the **Many ($N$) side**.
- Place the Primary Key of the **$1$-side** entity as a **Foreign Key** in the $N$-side relation.
- Copy any descriptive attributes of the relationship into the $N$-side relation.
- *Rule to remember*: "The Many side holds the Foreign Key."

### Step 5: M:N (Many-to-Many) Binary Relationship Sets
- Create a brand-new **Junction / Associative Table** $R$.
- Include Primary Keys of both participating entities as Foreign Keys.
- Include any descriptive attributes of the relationship.
- **Primary Key of $R$**: **Composite Key** formed by combining both Foreign Keys.

### Step 6: Multivalued Attributes
- For each multivalued attribute $A$ of entity $E$:
- Create a new relation $R_A$.
- Include the attribute $A$ along with the Primary Key $K$ of entity $E$ as Foreign Key.
- **Primary Key of $R_A$**: **Composite Key** = $(K, A)$.

---

## 4. RELATIONAL ALGEBRA OPERATOR QUICK REFERENCE

### Fundamental Operations & Concrete Equivalents

#### 1. Selection ($\sigma$)
- **Formal**: $\sigma_{\text{Salary} > 50000}(\text{EMPLOYEE})$
- **SQL Equivalent**: `SELECT * FROM EMPLOYEE WHERE Salary > 50000;`
- **Output**: Subsets of rows; degree remains unchanged, cardinality $\le$ original relation.

#### 2. Projection ($\Pi$)
- **Formal**: $\Pi_{\text{Name}, \text{Salary}}(\text{EMPLOYEE})$
- **SQL Equivalent**: `SELECT DISTINCT Name, Salary FROM EMPLOYEE;`
- **Output**: Subsets of columns; duplicate tuples are automatically removed.

#### 3. Cartesian Product ($\times$)
- **Formal**: $\text{EMPLOYEE} \times \text{DEPARTMENT}$
- **Degree**: $\text{Degree}(R \times S) = \text{Degree}(R) + \text{Degree}(S)$
- **Cardinality**: $\text{Card}(R \times S) = \text{Card}(R) \times \text{Card}(S)$

#### 4. Natural Join ($\bowtie$)
- **Formal**: $R \bowtie S = \Pi_{\text{all attributes}}(\sigma_{R.A_1=S.A_1 \land \dots \land R.A_k=S.A_k}(R \times S))$
- Combines tuples on identical attribute names and eliminates duplicate column copies.

#### 5. Division Operator ($\div$) — The Universal Quantifier
- **Formal**: $R(A, B) \div S(B)$
- **Definition**: Produces all tuples in $A$ that are paired with **EVERY** tuple in $S$.
- **Algebraic Derivation**:
  $$R \div S = \Pi_A(R) - \Pi_A((\Pi_A(R) \times S) - R)$$
- **Canonical Exam Problem**: *"Find Student IDs who have enrolled in ALL courses offered by the CS department."*

---

## 5. SQL LOGICAL EXECUTION ORDER & CLAUSE MAP

> [!IMPORTANT]
> SQL is not executed in the written syntax order! Understanding the logical order is the #1 secret to solving grouping and alias errors.

### Syntactic Order (How you write it):
```sql
SELECT DISTINCT col1, AGG(col2)
FROM Table1
JOIN Table2 ON condition
WHERE filter_condition
GROUP BY col1
HAVING agg_condition
ORDER BY col1 ASC
LIMIT n;
```

### Logical Order of Execution (How the database executes it):
```
┌───────┐
│ 1. FROM & JOIN     │  Determines source tables, computes cross products, applies ON filters
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 2. WHERE          │  Filters individual base rows (NO aggregates allowed here!)
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 3. GROUP BY       │  Collapses rows into aggregate buckets
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 4. HAVING         │  Filters grouped buckets (Aggregates evaluated here)
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 5. SELECT         │  Computes expressions, window functions, and assigns aliases
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 6. DISTINCT       │  Deduplicates matching output rows
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 7. ORDER BY       │  Sorts output (Can reference SELECT aliases)
└───────┬───────────┘
        ▼
┌───────┴───────────┐
│ 8. LIMIT / OFFSET │  Restricts returned row count
└───────────────────┘
```

---

## 6. SQL JOIN MATRIX (VISUAL GUIDE & TRAPS)

Given two sample relations:
**`Emp`**: `(1, 'Alice', 10), (2, 'Bob', 20), (3, 'Charlie', NULL)`
**`Dept`**: `(10, 'HR'), (20, 'IT'), (30, 'Finance')`

```
   Emp (Left)                   Dept (Right)
┌────┬─────────┬────────┐     ┌────┬─────────┐
│ ID │ Name    │ DeptID │     │ ID │ DName   │
├────┼─────────┼────────┤     ├────┼─────────┤
│ 1  │ Alice   │ 10     │     │ 10 │ HR      │
│ 2  │ Bob     │ 20     │     │ 20 │ IT      │
│ 3  │ Charlie │ NULL   │     │ 30 │ Finance │
└────┴─────────┴────────┘     └────┴─────────┘
```

### 1. `INNER JOIN`
Returns only records with a match in both tables:
```
(1, 'Alice', 10, 10, 'HR')
(2, 'Bob',   20, 20, 'IT')
```
*(Charlie and Finance are omitted)*

### 2. `LEFT OUTER JOIN`
Returns all records from Left table + matching Right table (NULL if no match):
```
(1, 'Alice', 10,   10,   'HR')
(2, 'Bob',   20,   20,   'IT')
(3, 'Charlie', NULL, NULL, NULL)
```

### 3. `RIGHT OUTER JOIN`
Returns all records from Right table + matching Left table (NULL if no match):
```
(1,    'Alice', 10, 10, 'HR')
(2,    'Bob',   20, 20, 'IT')
(NULL, NULL,  NULL, 30, 'Finance')
```

### 4. `FULL OUTER JOIN`
Returns all records from both tables, filling missing sides with NULL:
```
(1,    'Alice',   10,   10,   'HR')
(2,    'Bob',     20,   20,   'IT')
(3,    'Charlie', NULL, NULL, NULL)
(NULL, NULL,    NULL, 30,   'Finance')
```

---

## 7. SUBQUERY ARCHETYPES & THE NULL DANGER

### The Classic `NOT IN` vs `NULL` Trap (Examiner Favorite!)
Consider:
```sql
SELECT Name 
FROM Student 
WHERE Student_ID NOT IN (SELECT Mentor_ID FROM Mentorship);
```
**Trap**: If the `Mentorship` table contains even **A SINGLE ROW** where `Mentor_ID IS NULL`, the entire query returns **EMPTY SET (0 rows)**!
- **Reason**: `NOT IN (1, 2, NULL)` translates to:
  `Student_ID <> 1 AND Student_ID <> 2 AND Student_ID <> NULL`
  Since `Student_ID <> NULL` evaluates to `UNKNOWN`, the boolean `AND` chain evaluates to `UNKNOWN`, so no rows qualify.
- **The Bulletproof Fix (Use NOT EXISTS)**:
```sql
SELECT S.Name 
FROM Student S 
WHERE NOT EXISTS (
    SELECT 1 
    FROM Mentorship M 
    WHERE M.Mentor_ID = S.Student_ID
);
```

---

## 8. HIGH-FREQUENCY VIVA / SHORT-ANSWER QUESTIONS

**Q1: What are ACID properties?**
- **Atomicity**: "All or nothing" execution (ensured by Transaction Manager / Recovery Manager via undo logs).
- **Consistency**: Database transitions from one valid state satisfying all constraints to another (ensured by constraints + application logic).
- **Isolation**: Concurrent execution produces same state as serial execution (ensured by Concurrency Control Manager / 2-Phase Locking).
- **Durability**: Committed updates persist even after power failure / crash (ensured by Recovery Manager / redo logs / WAL).

**Q2: Can a Primary Key contain NULL?**
- **No**. By the **Entity Integrity Constraint**, no component of a Primary Key can be `NULL` because it serves as the unique tuple identifier.

**Q3: Can a Foreign Key contain NULL?**
- **Yes**, provided the foreign key column is not explicitly declared as `NOT NULL`. A `NULL` foreign key indicates no association (e.g., an unassigned employee having `Dept_ID = NULL`).

**Q4: What is the difference between Single-row and Multi-row subqueries?**
- **Single-row subquery**: Returns at most 1 row/value. Uses standard scalar comparison operators (`=`, `<`, `>`, `<=`, `>=`, `!=`).
- **Multi-row subquery**: Returns a list of values. Uses set comparison operators (`IN`, `NOT IN`, `ANY`, `ALL`, `EXISTS`).

**Q5: What is `WITH GRANT OPTION` in DCL?**
- Allows the user who received a privilege to propagate and grant that same privilege to other users. If revoked with `CASCADE`, all privileges granted down the chain are automatically revoked.

---

## 9. EXAM HALL GOLDEN RULES & MARK-MAXIMIZING STRATEGY

1. **Always draw Schema / ER diagrams using proper notation**:
   - Double lines for total participation.
   - Double border for weak entities and identifying relationships.
   - Underline Primary Keys.
2. **When asked for SQL queries**:
   - Always verify if `NULL` values could break `WHERE` conditions.
   - Check if you need `DISTINCT` when joining tables to avoid duplicated rows.
   - In `GROUP BY`, every column in the `SELECT` list that is not inside an aggregate function **must** appear in the `GROUP BY` list.
3. **When converting ER to Relational schema**:
   - State the Primary Key and Foreign Key constraints explicitly for every generated table.
   - Remember that M:N relationships always produce a new table with a composite primary key.
4. **Time Allocation in Exam**:
   - Part A (Definitions & Differences): Write concise points with tables and examples.
   - Part B (ER Modeling & Relational Algebra): Draw clean diagrams and step-by-step algebraic derivations.
   - Part C (SQL Queries): Write clean SQL syntax with keywords capitalized.

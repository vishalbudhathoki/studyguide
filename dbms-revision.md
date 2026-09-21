# DBMS — MCQ Revision Notes

---

## 1. Introduction: File Systems vs DBMS

**File system**: data stored in OS files; application code handles structure and access.

Problems with file systems:
- **Data redundancy** — same data duplicated across files
- **Inconsistency** — update one copy, others go stale
- **No/weak concurrency control** — lost updates
- **No atomicity** — partial writes on crash
- **Difficult access** — every new query needs a new program
- **No integrity enforcement** — rules live in code, not data
- **Security is all-or-nothing** — file-level, not row/column level

**DBMS** = software that stores, manages, and provides controlled access to data. Gives: data independence, concurrency control, recovery, integrity, security, declarative querying (ask *what*, not *how*).

**ACID** (transaction properties — frequent MCQ):
- **A**tomicity — all or nothing
- **C**onsistency — valid state → valid state
- **I**solation — concurrent txns don't interfere
- **D**urability — committed changes survive crashes

---

## 2. DBMS Architecture

### Three-level (ANSI/SPARC) architecture

| Level | Also called | Contains |
|---|---|---|
| **External** | View level | Many user-specific views; hides irrelevant data |
| **Conceptual** | Logical level | Whole DB: entities, attributes, relationships, constraints |
| **Internal** | Physical level | Storage layout, files, indexes, access paths |

**Mappings**: external↔conceptual, conceptual↔internal.

**Data independence**:
- **Logical data independence** — change conceptual schema without changing external schemas/apps. *Harder to achieve.*
- **Physical data independence** — change internal schema (add index, change file org) without touching conceptual schema. *Easier.*

### Tier architectures
- **1-tier** — user directly on the DB (local)
- **2-tier** — client app → DB server (ODBC/JDBC)
- **3-tier** — client → application server → DB server (most web apps; better scalability + security)

---

## 3. Users, Schema, Instance, Metadata

- **Schema** — the *design/structure* of the DB. Changes rarely. (Also called intension.)
- **Instance** — the *data* in the DB at a given moment. Changes constantly. (Also called extension / snapshot / state.)
  - Mnemonic: schema = variable declaration, instance = its current value.
- **Metadata** — "data about data": table names, column names, types, constraints, users, indexes. Stored in the **data dictionary / system catalog**.

**Users**:
| Role | Does what |
|---|---|
| **DBA** | Schema definition, grants/revokes, backup & recovery, tuning. Highest authority. |
| **Database designer** | Identifies data, designs schema |
| **Application programmer** | Writes programs with embedded SQL |
| **End user** (naive / sophisticated) | Naive = uses forms/apps; sophisticated = writes own queries |
| **System analyst** | Determines end-user requirements |

**Data Definition vs Manipulation language processor**, **query optimizer**, **storage manager**, **transaction manager**, **buffer manager** are DBMS internal components.

---

## 4. Keys

Given a relation, keys are about **uniqueness**:

- **Super key** — any set of attributes that uniquely identifies a tuple (may have extras).
- **Candidate key** — a *minimal* super key (no proper subset is a super key).
- **Primary key** — the candidate key chosen by the designer. **Unique + NOT NULL**. Only one per relation.
- **Alternate / secondary key** — candidate keys not chosen as primary.
- **Composite key** — a key made of ≥2 attributes.
- **Foreign key** — attribute(s) in one relation referencing the primary key of another (possibly the same) relation. Enforces **referential integrity**. *Can* be NULL (unless declared NOT NULL); *can* have duplicates.
- **Surrogate key** — system-generated artificial key (e.g. auto-increment id), no business meaning.

Relationships between them: **Primary ⊆ Candidate ⊆ Super**.

**Constraint types (integrity)**:
- **Domain constraint** — value must be from the attribute's domain / datatype
- **Entity integrity** — PK cannot be NULL
- **Referential integrity** — FK must match an existing PK value or be NULL
- **Key constraint** — no two tuples have the same key value

---

## 5. Entities, Relationships, ER Modelling

**Entity** — a distinguishable real-world object. **Entity set** — collection of similar entities (becomes a table).
- **Strong entity** — has its own primary key. Drawn as a rectangle.
- **Weak entity** — no sufficient key of its own; depends on an owner/identifying entity. Drawn as a **double rectangle**, connected by a **double diamond** (identifying relationship) with **total participation**. Has a **partial key / discriminator** (dashed underline).

**Attributes** (ellipse):
- **Simple** vs **Composite** (has sub-attributes, e.g. Name → First, Last)
- **Single-valued** vs **Multivalued** (double ellipse, e.g. PhoneNumbers)
- **Derived** (dashed ellipse, e.g. Age from DOB) vs **Stored**
- **Key attribute** — underlined
- **Complex** — composite + multivalued combined

**Relationship** (diamond) — association among entities. **Degree** = number of participating entity sets: unary/recursive (1), binary (2), ternary (3), n-ary.

**Cardinality ratio** (for binary): 1:1, 1:N, N:1, M:N.

**Participation constraint**:
- **Total participation** (double line) — every entity must participate. = existence dependency, mandatory.
- **Partial participation** (single line) — optional.

**Extended ER (EER)**:
- **Specialization** — top-down, split a superclass into subclasses
- **Generalization** — bottom-up, combine entities into a superclass
- **Aggregation** — treat a whole relationship as one higher-level entity so another relationship can connect to it
- **Disjoint (d)** vs **Overlapping (o)** constraint; **total** vs **partial** completeness
- **Inheritance** — subclasses inherit attributes + relationships of superclass

---

## 6. Relational Model Basics

A **relation** = a table. Formally, a subset of the Cartesian product of its domains.

Terminology (know both columns — MCQs love this):

| Formal | Informal |
|---|---|
| Relation | Table |
| Tuple | Row / record |
| Attribute | Column / field |
| Degree / arity | Number of **attributes** |
| Cardinality | Number of **tuples** |
| Domain | Set of allowed atomic values for an attribute |
| Relation schema | R(A1, A2, …, An) |

Properties:
- Tuples are **unordered**; attributes are unordered (by name)
- **No duplicate tuples** (a relation is a set)
- All values are **atomic** (1NF by definition)
- **NULL** = unknown / not applicable / missing. NULL ≠ 0 and NULL ≠ ''.

**Referential actions** on FK: `ON DELETE / ON UPDATE` → `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT`, `NO ACTION`.

Proposed by **E. F. Codd** (1970). Codd's 12 rules define a fully relational DBMS.

---

## 7. ER → Relational Model Conversion

| ER construct | Relational result |
|---|---|
| **Strong entity** | Table; key attribute → PK |
| **Weak entity** | Table with PK = (owner's PK + partial key); FK to owner, `ON DELETE CASCADE` |
| **Composite attribute** | One column per simple sub-attribute (flatten) |
| **Multivalued attribute** | **New table**: (entity PK, the multivalued attr) with both as composite PK |
| **Derived attribute** | Usually **not stored** (compute it) |
| **1:1 relationship** | Add FK to either side — prefer the side with **total participation**; or merge tables |
| **1:N relationship** | Add FK on the **N (many) side** pointing to the 1 side. No new table needed. |
| **M:N relationship** | **New relationship table**: PK = both FKs combined, plus any descriptive attributes |
| **n-ary (n≥3)** | New table with FKs to all participants |
| **Generalization/specialization** | Options: (a) one table per subclass with inherited attrs, (b) superclass table + subclass tables sharing PK, (c) single table with a type discriminator |

Rule of thumb for MCQs: **minimum number of tables** for two entities with a 1:N relation = 2; with M:N = 3.

---

## 8. Relational Algebra

**Procedural** query language; closed (output of an operation is a relation, so operations compose).

**Basic / fundamental operators (5)**: σ (select), π (project), ∪ (union), − (set difference), × (Cartesian product). Also ρ (rename).

**Derived operators**: ∩ (intersection), ⋈ (join), ÷ (division).

### Selection — σ
`σ_condition(R)` — picks **rows**. Horizontal subset. Degree unchanged, cardinality ≤ original.
- Condition uses =, ≠, <, ≤, >, ≥ and ∧ ∨ ¬.
- σ is **commutative**: σ_c1(σ_c2(R)) = σ_c2(σ_c1(R)).
- SQL equivalent: `WHERE`.

### Projection — π
`π_A1,A2(R)` — picks **columns**. Vertical subset. **Removes duplicate rows** (set semantics!). Cardinality ≤ original.
- SQL equivalent: `SELECT` list — but SQL keeps duplicates unless you write `DISTINCT`.
- Not commutative in general: π_A(π_{A,B}(R)) is valid, the reverse isn't.

### Set operations
∪, ∩, − require **union compatibility**: same number of attributes AND corresponding domains compatible. (Names need not match.)
- ∪ and ∩ are commutative and associative; **− is not**.
- R ∩ S = R − (R − S)

### Cartesian product — ×
R(m attrs, x tuples) × S(n attrs, y tuples) → degree **m+n**, cardinality **x·y**. No union compatibility needed.

### Joins
- **Theta join** `R ⋈_θ S` = σ_θ(R × S)
- **Equi join** — theta join where θ uses only `=`
- **Natural join** `R ⋈ S` — equi-join on all common attribute names, with the duplicate column removed. If no common attributes → behaves like Cartesian product.
- **Outer joins** — preserve unmatched tuples, padding with NULLs: left ⟕, right ⟖, full ⟗
- **Semi join**, **anti join** — keep only left-side attributes

### Division — ÷
`R ÷ S` — answers "**for all**" queries: e.g. students who took *every* course. Result attributes = attrs(R) − attrs(S).

### Others
- **Rename** ρ_S(R) or ρ_{S(a,b)}(R)
- **Assignment** ←
- **Generalized projection** — allows arithmetic in the projection list
- **Aggregation** — 𝒢 (script G), e.g. `dept 𝒢 SUM(salary)(Emp)`

**Relational calculus** (contrast): **non-procedural/declarative**; TRC (tuple) and DRC (domain). Relational algebra and safe relational calculus are **equivalent in expressive power** — both are *relationally complete* but weaker than Turing-complete.

---

## 9. SQL Command Categories

| Category | Commands | Note |
|---|---|---|
| **DDL** | CREATE, ALTER, DROP, TRUNCATE, RENAME | Auto-commit; structure |
| **DML** | INSERT, UPDATE, DELETE, (MERGE) | Data; can be rolled back |
| **DQL/DRL** | SELECT | Retrieval |
| **DCL** | GRANT, REVOKE | Permissions |
| **TCL** | COMMIT, ROLLBACK, SAVEPOINT | Transactions |

SQL is **non-procedural / declarative**. Based on relational algebra + tuple calculus. Uses **multiset (bag)** semantics — duplicates allowed unless DISTINCT.

---

## 10. DDL

```sql
CREATE TABLE Student (
  roll_no   INT PRIMARY KEY,
  name      VARCHAR(50) NOT NULL,
  age       INT CHECK (age >= 17),
  email     VARCHAR(50) UNIQUE,
  city      VARCHAR(30) DEFAULT 'Delhi',
  dept_id   INT,
  FOREIGN KEY (dept_id) REFERENCES Dept(dept_id) ON DELETE SET NULL
);

ALTER TABLE Student ADD  COLUMN cgpa DECIMAL(3,2);
ALTER TABLE Student DROP COLUMN cgpa;
ALTER TABLE Student MODIFY name VARCHAR(80);        -- Oracle/MySQL
ALTER TABLE Student ALTER COLUMN name VARCHAR(80);  -- SQL Server
ALTER TABLE Student RENAME COLUMN city TO town;
ALTER TABLE Student ADD CONSTRAINT chk_age CHECK (age < 100);
ALTER TABLE Student DROP CONSTRAINT chk_age;

DROP TABLE Student;
```

**DROP vs TRUNCATE vs DELETE** — classic MCQ:

| | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| Type | DML | DDL | DDL |
| Removes | Selected rows (WHERE) | All rows | Rows **+ structure** |
| WHERE allowed | Yes | No | No |
| Rollback | Yes | No (auto-commit) | No |
| Speed | Slow (row-by-row, logged) | Fast (deallocates pages) | Fast |
| Fires triggers | Yes | No | No |
| Resets identity | No | Yes | — |

Constraints available: `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `DEFAULT`.
- `UNIQUE` **allows** NULLs (one in most DBs); `PRIMARY KEY` does not.

---

## 11. DML

```sql
INSERT INTO Student (roll_no, name, age) VALUES (1, 'Asha', 19);
INSERT INTO Student VALUES (2, 'Bilal', 20, 'b@x.com', 'Pune', 3);   -- all cols, in order
INSERT INTO Student VALUES (3, 'Cara', 21), (4, 'Dev', 22);          -- multi-row
INSERT INTO Alumni SELECT * FROM Student WHERE year = 2024;          -- from query

UPDATE Student SET age = age + 1 WHERE city = 'Pune';
UPDATE Student SET city = 'Delhi', age = 20 WHERE roll_no = 3;

DELETE FROM Student WHERE age < 18;
DELETE FROM Student;          -- all rows, structure stays
```

**Forgetting `WHERE` in UPDATE/DELETE affects every row** — common trick question.

---

## 12. DQL: SELECT, WHERE, ORDER BY

```sql
SELECT DISTINCT dept, name AS student_name
FROM   Student
WHERE  age > 18
ORDER  BY dept ASC, age DESC
LIMIT  10;                    -- MySQL/Postgres; Oracle: FETCH FIRST 10 ROWS ONLY
```

**Logical order of evaluation** (very common MCQ — note SELECT is *not* first):

```
FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

Consequence: a column **alias** defined in SELECT cannot be used in WHERE (it isn't computed yet), but **can** be used in ORDER BY.

### WHERE operators
- Comparison: `= <> != < <= > >=`
- `BETWEEN a AND b` — **inclusive** of both ends
- `IN (v1, v2, …)` / `NOT IN`
- `LIKE` — `%` = zero or more chars, `_` = exactly one char. `ESCAPE` clause for literal % or _.
- `IS NULL` / `IS NOT NULL` — **never** `= NULL`
- `AND`, `OR`, `NOT`; precedence: `NOT` > `AND` > `OR`

### NULL behaviour (high-yield)
- Any arithmetic with NULL → NULL (`5 + NULL = NULL`)
- Any comparison with NULL → **UNKNOWN**, so the row is not returned
- `NOT IN` with a NULL in the subquery list → returns **no rows** (trap!)
- Aggregates **ignore NULLs**, except `COUNT(*)`
- `ORDER BY`: NULLs sort together (first or last depending on DBMS; `NULLS FIRST/LAST` in Oracle/Postgres)
- Three-valued logic: TRUE / FALSE / UNKNOWN

### ORDER BY
- Default is **ASC**
- Can order by column name, alias, expression, or **column position** (`ORDER BY 2`)
- Multiple keys sort left-to-right
- Always the **last** clause executed

---

## 13. Aggregate Functions & Grouping

| Function | NULLs | Notes |
|---|---|---|
| `COUNT(*)` | counted | counts all rows |
| `COUNT(col)` | **ignored** | non-NULL values only |
| `COUNT(DISTINCT col)` | ignored | distinct non-NULL |
| `SUM(col)` | ignored | numeric only |
| `AVG(col)` | ignored | = SUM/COUNT of **non-NULL** — so AVG ≠ SUM/COUNT(*) when NULLs exist |
| `MIN` / `MAX` | ignored | works on numbers, strings, dates |

Aggregates return **one row** when there's no GROUP BY. They cannot be nested directly (`MAX(AVG(x))` needs a subquery/GROUP BY inside).

### GROUP BY
```sql
SELECT   dept, COUNT(*) AS cnt, AVG(salary) AS avg_sal
FROM     Employee
WHERE    salary > 10000          -- filters ROWS first
GROUP BY dept
HAVING   COUNT(*) > 5            -- filters GROUPS after aggregation
ORDER BY avg_sal DESC;
```

**Rule**: every column in SELECT must be either in GROUP BY or inside an aggregate function. (MySQL is lenient by default; standard SQL and most others reject it.)

- `GROUP BY` puts rows with equal values into one group; one output row per group.
- `GROUP BY a, b` groups on the **combination**.
- NULLs are grouped together as a single group.

### WHERE vs HAVING — classic MCQ

| | WHERE | HAVING |
|---|---|---|
| Filters | individual rows | groups |
| Runs | **before** GROUP BY | **after** GROUP BY |
| Aggregates allowed | **No** | **Yes** |
| Needs GROUP BY | No | Practically yes (without it, whole table = one group) |

---

## 14. Joins

```sql
SELECT s.name, d.dept_name
FROM   Student s
JOIN   Dept d ON s.dept_id = d.dept_id;
```

| Join | Returns |
|---|---|
| **INNER JOIN** | Only matching rows from both tables |
| **LEFT (OUTER) JOIN** | All left rows + matches; NULLs where no right match |
| **RIGHT (OUTER) JOIN** | All right rows + matches; NULLs where no left match |
| **FULL (OUTER) JOIN** | All rows from both; NULLs on either side where unmatched |
| **CROSS JOIN** | Cartesian product, m×n rows, no ON clause |
| **NATURAL JOIN** | Auto-joins on all same-named columns; common column appears once |
| **SELF JOIN** | Table joined to itself using aliases (e.g. employee → manager) |

Key facts:
- `A LEFT JOIN B` ≡ `B RIGHT JOIN A`
- INNER JOIN is **commutative**; outer joins are **not**
- Rows returned by INNER JOIN on a FK: ≤ rows in the many-side table
- `ON` vs `WHERE` in an outer join: a condition on the right table in `WHERE` filters out the NULL-padded rows and silently turns it into an inner join — put it in `ON` instead.
- `USING (col)` — shorthand for equality on a shared column name
- MySQL has no `FULL OUTER JOIN`; emulate with `LEFT UNION RIGHT`

Find unmatched rows (anti-join):
```sql
SELECT s.* FROM Student s
LEFT JOIN Dept d ON s.dept_id = d.dept_id
WHERE d.dept_id IS NULL;
```

---

## 15. Nested Queries / Subqueries

**Scalar subquery** — returns one value:
```sql
SELECT name FROM Emp WHERE salary > (SELECT AVG(salary) FROM Emp);
```

**Multi-row subquery** — needs `IN`, `ANY`/`SOME`, `ALL`:
```sql
SELECT name FROM Emp WHERE dept_id IN (SELECT dept_id FROM Dept WHERE loc='Pune');
SELECT name FROM Emp WHERE salary > ALL (SELECT salary FROM Emp WHERE dept='HR');
SELECT name FROM Emp WHERE salary > ANY (SELECT salary FROM Emp WHERE dept='HR');
```
- `> ALL` ≡ greater than the **maximum**
- `> ANY` ≡ greater than the **minimum**
- `= ANY` ≡ `IN`; `<> ALL` ≡ `NOT IN`

**Correlated subquery** — inner query references the outer query; re-evaluated **per outer row** (slower):
```sql
SELECT e.name FROM Emp e
WHERE e.salary > (SELECT AVG(salary) FROM Emp WHERE dept_id = e.dept_id);
```

**EXISTS / NOT EXISTS** — returns TRUE/FALSE, stops at the first match; safe with NULLs (unlike `NOT IN`):
```sql
SELECT d.dept_name FROM Dept d
WHERE EXISTS (SELECT 1 FROM Emp e WHERE e.dept_id = d.dept_id);
```

**Subquery placement**: SELECT list (scalar), FROM (**derived table / inline view** — must be aliased), WHERE, HAVING, and inside INSERT/UPDATE/DELETE.

Nth highest salary:
```sql
SELECT MAX(salary) FROM Emp
WHERE salary < (SELECT MAX(salary) FROM Emp);     -- 2nd highest
```

Comparison: non-correlated subquery runs **once**; correlated runs **once per outer row**. `NOT EXISTS` is the standard way to express relational **division** / "for all".

---

## 16. Set Operations in SQL

Require the operands to have the **same number of columns** with **compatible types** (union compatibility). Column names come from the **first** SELECT.

| Operator | Meaning | Duplicates |
|---|---|---|
| `UNION` | All rows from both | **Removed** (implicit DISTINCT → sorts, slower) |
| `UNION ALL` | All rows from both | **Kept** (fastest) |
| `INTERSECT` | Rows in both | Removed |
| `MINUS` (Oracle) / `EXCEPT` (SQL Server, Postgres, standard) | Rows in first but not second | Removed |

```sql
SELECT name FROM Student
UNION
SELECT name FROM Alumni
ORDER BY name;        -- ORDER BY only once, at the very end
```

- `ORDER BY` can appear only at the end, applying to the whole result.
- `UNION`/`INTERSECT` are commutative; `MINUS`/`EXCEPT` is **not**.
- Precedence: `INTERSECT` binds tighter than `UNION`/`EXCEPT` in the standard — use parentheses.
- MySQL lacks `INTERSECT`/`EXCEPT` in older versions (emulate with joins / `NOT IN`).
- These are **set** operations (dedupe); joins combine columns, set ops stack rows.

---

## 17. DCL: GRANT and REVOKE

```sql
GRANT SELECT, INSERT ON Student TO user1;
GRANT ALL PRIVILEGES ON Student TO user1 WITH GRANT OPTION;
GRANT UPDATE (name, city) ON Student TO user2;    -- column-level

REVOKE INSERT ON Student FROM user1;
REVOKE ALL PRIVILEGES ON Student FROM user1;
```

- Privileges: `SELECT, INSERT, UPDATE, DELETE, REFERENCES, EXECUTE, ALL PRIVILEGES`
- `WITH GRANT OPTION` — lets the grantee pass the privilege on to others.
- `PUBLIC` — grants to all users.
- **Cascading revoke**: revoking a privilege that was granted onward also removes it from those downstream grantees (Oracle: `REVOKE ... CASCADE CONSTRAINTS`; SQL Server: `CASCADE`).
- The **owner** of an object has all privileges on it automatically; the **DBA** grants/revokes at system level.
- **Roles** — named bundles of privileges: `CREATE ROLE`, `GRANT role TO user`.
- **Views** are also an authorization mechanism: grant SELECT on a view instead of the base table to restrict rows/columns.

---

## Quick MCQ Traps Checklist

1. `SELECT` is evaluated **after** WHERE/GROUP BY/HAVING — aliases unusable in WHERE.
2. `COUNT(*)` counts NULL rows; `COUNT(col)` doesn't.
3. `π` removes duplicates in relational algebra, `SELECT` doesn't in SQL.
4. `BETWEEN` is inclusive.
5. `= NULL` never matches — use `IS NULL`.
6. `NOT IN` + NULL in subquery → empty result.
7. TRUNCATE can't be rolled back; DELETE can.
8. Primary key ⇒ NOT NULL; UNIQUE allows NULL.
9. 1:N → FK goes on the **many** side; M:N → new table.
10. Degree = columns, Cardinality = rows.
11. Schema is design, instance is data.
12. `MINUS`/`EXCEPT` and outer joins are **not** commutative.
13. `HAVING` can use aggregates; `WHERE` cannot.
14. Basic relational algebra operators = 5 (σ, π, ∪, −, ×).
15. `UNION` dedupes and sorts; `UNION ALL` is faster.

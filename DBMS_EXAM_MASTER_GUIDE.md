# 🎓 DATABASE MANAGEMENT SYSTEMS (DBMS) — COMPREHENSIVE EXAM MASTER GUIDE
**Target: 100% Full Score in University, College & Competitive Technical Examinations**  
**Syllabus Coverage: Complete Theory, Architectures, ER Modeling, Relational Algebra, and End-to-End SQL**

---

## 📑 TABLE OF CONTENTS
1. [Module 1: Introduction to DBMS & File Systems](#module-1-introduction-to-dbms--file-systems)
2. [Module 2: DBMS Architecture & ANSI-SPARC 3-Schema Architecture](#module-2-dbms-architecture--ansi-sparc-3-schema-architecture)
3. [Module 3: Users, Schema, Instance, Metadata & Data Dictionary](#module-3-users-schema-instance-metadata--data-dictionary)
4. [Module 4: Keys Taxonomy & Classification](#module-4-keys-taxonomy--classification)
5. [Module 5: Entity-Relationship (ER) Modeling](#module-5-entity-relationship-er-modeling)
6. [Module 6: Relational Model Basics & Integrity Constraints](#module-6-relational-model-basics--integrity-constraints)
7. [Module 7: Conversion of ER to Relational Model (The 7-Step Algorithm)](#module-7-conversion-of-er-to-relational-model-the-7-step-algorithm)
8. [Module 8: Relational Algebra (Procedural Query Language)](#module-8-relational-algebra-procedural-query-language)
9. [Module 9: SQL Data Definition Language (DDL) — CREATE, ALTER, DROP](#module-9-sql-data-definition-language-ddl--create-alter-drop)
10. [Module 10: SQL Data Manipulation Language (DML) — INSERT, UPDATE, DELETE](#module-10-sql-data-manipulation-language-dml--insert-update-delete)
11. [Module 11: SQL Data Query Language (DQL) — SELECT, WHERE, ORDER BY](#module-11-sql-data-query-language-dql--select-where-order-by)
12. [Module 12: Aggregate Functions, GROUP BY & HAVING](#module-12-aggregate-functions-group-by--having)
13. [Module 13: SQL Joins Masterclass (Inner, Left, Right, Full, Self, Natural)](#module-13-sql-joins-masterclass-inner-left-right-full-self-natural)
14. [Module 14: Nested Queries & Subqueries (Single-row, Multi-row, Correlated, EXISTS)](#module-14-nested-queries--subqueries-single-row-multi-row-correlated-exists)
15. [Module 15: Set Operations (UNION, INTERSECT, MINUS / EXCEPT)](#module-15-set-operations-union-intersect-minus--except)
16. [Module 16: SQL Data Control Language (DCL) — GRANT & REVOKE](#module-16-sql-data-control-language-dcl--grant--revoke)
17. [Module 17: Exam Practice Bank — Top 20 Tricky Questions & Model Answers](#module-17-exam-practice-bank--top-20-tricky-questions--model-answers)

---

# MODULE 1: INTRODUCTION TO DBMS & FILE SYSTEMS

### 1.1 What is a File Processing System?
A **File Processing System** is a traditional method of storing, retrieving, and manipulating data where records are stored directly in operating system flat files (such as `.txt`, `.dat`, `.csv`) and accessed using customized application programs written in procedural languages (e.g., C, C++, COBOL, Pascal).

#### Limitations of Traditional File Processing Systems:
1. **Data Redundancy & Inconsistency**:
   - The same information is duplicated in multiple independent files (e.g., a student's address in both the Library file and Fee Department file).
   - Updating one file without updating the other leads to inconsistent data states across the organization.
2. **Difficulty in Accessing Data**:
   - Ad-hoc queries are impossible. To answer a simple question like *"List students with GPA > 3.5 in CS"*, a programmer must write a dedicated C/Java program from scratch.
3. **Data Isolation & Decentralization**:
   - Files are stored in different physical formats (binary, ASCII, custom delimiters), making cross-file correlation and integration extremely complex.
4. **Integrity Problems**:
   - Business constraints (e.g., `Account_Balance >= 500`) must be hardcoded into every application program. When rules change, every program must be rewritten, recompiled, and redeployed.
5. **Atomicity Problems**:
   - In a fund transfer of \$100 from Account A to Account B, if the machine crashes after debiting A but before crediting B, the file system leaves the data in an inconsistent state (\$100 is lost).
6. **Concurrent Access Anomalies**:
   - If two users attempt to update the same file simultaneously without locking mechanisms, race conditions occur, leading to lost updates.
7. **Security & Access Control Issues**:
   - File systems only offer coarse-grained OS permissions (read, write, execute on the entire file). They cannot restrict a user to see only specific columns or specific rows (e.g., allowing HR to see names but hiding salaries).

---

### 1.2 What is a Database Management System (DBMS)?
A **DBMS** is a collection of interrelated data and a set of system software programs that allow users to define, construct, manipulate, query, and share databases securely among various users and applications.

#### Foundational Advantages of DBMS:
- **Centralized Data Management**: Reduces redundant data to a controlled minimum.
- **Data Independence**: Decouples application programs from physical storage mechanisms and logical structure.
- **Enforcement of Integrity Constraints**: Constraints (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `NOT NULL`) are declared in the schema and enforced by the engine.
- **Transaction Support (ACID Properties)**: Guarantees reliable data processing during crashes and concurrent access:
  - **Atomicity**: The entire transaction completes, or none of it takes effect ("All or Nothing"). Managed by the *Recovery Manager* using Write-Ahead Logging (WAL).
  - **Consistency**: The database transitions from one valid state satisfying all constraints to another.
  - **Isolation**: Concurrent transactions execute as if they were running sequentially in isolation. Managed by the *Concurrency Control Manager* (e.g., Two-Phase Locking / 2PL).
  - **Durability**: Once committed, changes survive power outages, crashes, and media failures. Managed by *Redo logs* / checkpoints.
- **Declarative Querying**: Users specify *what* data they need via SQL; the DBMS query optimizer determines *how* to retrieve it efficiently.

#### When is a File System Preferred Over a DBMS?
- Extremely low memory / embedded devices with severe CPU constraints.
- Single-user applications with simple, strictly sequential data storage (e.g., simple loggers).
- When the overhead of a database engine (licensing, memory footprint, configuration) exceeds the project scale.

---

# MODULE 2: DBMS ARCHITECTURE & ANSI-SPARC 3-SCHEMA ARCHITECTURE

### 2.1 Multi-Tier DBMS Architectures

```
1-TIER ARCHITECTURE:
┌─────────────────────────────────────────┐
│   User Interface + Business Logic       │  (All residing on a single local PC,
│   + Database Engine + Data Storage      │   e.g., MS Access, SQLite testing)
└─────────────────────────────────────────┘

2-TIER (CLIENT-SERVER) ARCHITECTURE:
┌──────────────────────┐             ┌──────────────────────┐
│     CLIENT TIER      │   ODBC/JDBC │     SERVER TIER      │
│ Presentation Layer   │ ──────────> │ Database Engine      │
│ + Business Logic     │ <────────── │ + Storage Management │
└──────────────────────┘             └──────────────────────┘

3-TIER ARCHITECTURE (MODERN WEB/ENTERPRISE):
┌──────────────────┐      HTTP/REST    ┌──────────────────┐    ODBC/JDBC   ┌──────────────────┐
│   CLIENT TIER    │ ────────────────> │ APPLICATION TIER │ ─────────────> │  DATABASE TIER   │
│ Web/Mobile UI    │ <──────────────── │ Business Logic,  │ <───────────── │ Relational DBMS  │
│ (Thin Client)    │                   │ APIs, Security   │                │ Storage & Query  │
└──────────────────┘                   └──────────────────┘                └──────────────────┘
```

#### Comparison of Tiers:
| Parameter | 1-Tier | 2-Tier | 3-Tier |
| :--- | :--- | :--- | :--- |
| **Layers** | Single integrated tier | Client Tier + DB Server Tier | Client + Application Server + DB Server |
| **Client Type** | Standalone | Fat Client (contains application logic) | Thin Client (only renders UI / HTML / JSON) |
| **Scalability** | Single user | Limited (connection pool bottleneck) | Highly Scalable (stateless app servers, load balancers) |
| **Security** | None | Low (DB credentials stored on client) | High (Client has no direct access to database) |

---

### 2.2 The ANSI-SPARC 3-Schema Architecture
Proposed in 1975 to achieve **Data Independence** by separating user views from physical storage.

```
                  ┌──────────────────────┐   ┌──────────────────────┐
                  │   External View 1    │   │   External View 2    │  (External / View Level)
                  │ (Student Portal View)│   │  (Faculty Grade View)│
                  └──────────┬───────────┘   └──────────┬───────────┘
                             │                          │
                 ════════════╪══════════════════════════╪═════════════  Logical Data Independence
                             ▼                          ▼
                  ┌─────────────────────────────────────────────────┐
                  │                 CONCEPTUAL SCHEMA               │  (Conceptual / Logical Level)
                  │ Entities, Attributes, Relationships, Constraints│
                  └────────────────────────┬────────────────────────┘
                                           │
                 ══════════════════════════╪══════════════════════════  Physical Data Independence
                                           ▼
                  ┌─────────────────────────────────────────────────┐
                  │                 INTERNAL SCHEMA                 │  (Internal / Physical Level)
                  │ File structures, B+ Trees, Block sizes, Hashing │
                  └─────────────────────────────────────────────────┘
```

#### The Three Levels:
1. **Internal / Physical Level (Lowest)**:
   - Describes *how* data is physically stored on disk (block allocation, clustering, B+ Tree indices, compression, record formats).
2. **Conceptual / Logical Level (Middle)**:
   - Describes *what* data is stored in the entire database and the relationships among data items.
   - Hides low-level physical storage details. Built using ER diagrams converted to relational tables.
3. **External / View Level (Highest)**:
   - Tailored views for individual user groups. Hides irrelevant or sensitive data (e.g., student sees marks, not professor salaries).

---

### 2.3 Data Independence: Physical vs. Logical
**Data Independence** is the capacity to change the schema at one level of a database system without having to change the schema at the next higher level.

| Dimension | Physical Data Independence | Logical Data Independence |
| :--- | :--- | :--- |
| **Definition** | Ability to modify the internal schema without altering the conceptual schema. | Ability to modify the conceptual schema without altering external schemas/views. |
| **Interface** | Internal Level $\leftrightarrow$ Conceptual Level | Conceptual Level $\leftrightarrow$ External Level |
| **Examples** | Switching from HDD to SSD; changing index from Hash to B+ Tree; reorganizing record clustering. | Adding new columns (`LinkedIn_Profile`); splitting a table into two normalized tables; adding a new entity. |
| **Ease of Achievement** | **Easier** to achieve; handled transparently by DB engine. | **Difficult** to achieve; requires creating views to emulate the old schema. |

---

# MODULE 3: USERS, SCHEMA, INSTANCE, METADATA & DATA DICTIONARY

### 3.1 Classification of DBMS Users
1. **Naive / Parametric Users**:
   - End users who interact with the system through pre-built graphical user interfaces without knowing SQL (e.g., ATM customers, railway reservation clerks).
2. **Application Programmers / Software Engineers**:
   - Write backend programs in Python, Java, C# using database drivers (JDBC, SQLAlchemy) to interact with the DBMS.
3. **Sophisticated Users**:
   - Engineers, business analysts, and data scientists who write custom ad-hoc SQL queries and analytical scripts directly to analyze data.
4. **Specialized Users**:
   - Write specialized database applications (e.g., Expert Systems, CAD systems, Spatial GIS databases).
5. **Database Administrator (DBA)**:
   - The central authority with complete administrative control over the DBMS.
   - **Key Responsibilities of DBA**:
     - Schema definition and storage structure configuration.
     - Granting security authorizations and user permissions (`GRANT`, `REVOKE`).
     - Routine maintenance, backup scheduling, and disaster recovery.
     - Performance tuning, indexing, and resource monitoring.

---

### 3.2 Schema vs. Instance
- **Database Schema**: The skeleton structure and blueprint of the database.
  - Specified during database design and modified very rarely (via DDL).
  - Equivalent to a **Type declaration** or `class` in programming.
- **Database Instance**: The actual collection of data populated in the database at a specific snapshot in time.
  - Changes constantly as rows are inserted, updated, and deleted (via DML).
  - Equivalent to the **runtime state / value of a variable**.

---

### 3.3 Metadata & The Data Dictionary (System Catalog)
- **Metadata**: "Data about data". Describes schemas, constraints, column types, storage parameters, and access privileges.
- **Data Dictionary / System Catalog**: A specialized repository within the DBMS that stores all metadata.
  - The query optimizer uses the data dictionary to check table existence, column types, available indices, and table statistics before executing a query plan.
  - Can be **Active** (automatically updated by the DBMS whenever DDL commands execute) or **Passive** (updated manually for documentation).

---

# MODULE 4: KEYS TAXONOMY & CLASSIFICATION

A **Key** is an attribute or set of attributes that helps uniquely identify an entity within an entity set, or a tuple within a relation.

```
┌────────────────────────────────────────────────────────┐
│                       SUPER KEYS                       │
│      Any attribute set that guarantees uniqueness      │
│   ┌────────────────────────────────────────────────┐   │
│   │                 CANDIDATE KEYS                 │   │
│   │      Minimal Super Keys (No extra baggage)     │   │
│   │   ┌───────────────┐        ┌───────────────┐   │   │
│   │   │  PRIMARY KEY  │        │ ALTERNATE KEY │   │   │
│   │   │  (Chosen One) │        │ (The Runners) │   │   │
│   │   └───────────────┘        └───────────────┘   │   │
│   └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

### Complete Key Taxonomy:
1. **Super Key**:
   - Any set of one or more attributes that taken collectively allows us to uniquely identify a tuple in the relation.
   - *Example* in `Student(RollNo, RegNo, Email, Name, Dept)`:
     - `{RollNo}`, `{RollNo, Name}`, `{RegNo, Email, Dept}`, `{RollNo, RegNo, Email, Name, Dept}` are all valid super keys.
2. **Candidate Key**:
   - A **minimal super key** — meaning no proper subset of the attribute set is itself a super key.
   - *Formal condition*: $K$ is a candidate key of $R$ if:
     1. Uniqueness: No two distinct tuples have identical values on $K$.
     2. Minimality: If any attribute $A \in K$ is removed, the remaining set is no longer unique.
   - *Example*: `{RollNo}`, `{RegNo}`, `{Email}` are distinct candidate keys.
3. **Primary Key**:
   - The specific candidate key chosen by the database designer as the principal means of identifying tuples.
   - **Entity Integrity Rule**: Cannot contain `NULL` values.
   - Exactly **one** Primary Key per table.
4. **Alternate / Secondary Key**:
   - All candidate keys that were **not** chosen as the Primary Key.
   - *Example*: If `{RollNo}` is Primary Key, then `{RegNo}` and `{Email}` are Alternate Keys.
5. **Foreign Key**:
   - An attribute (or set of attributes) in a relation $R_1$ (referencing relation) whose values must match the Candidate/Primary Key of relation $R_2$ (referenced relation) or be `NULL`.
   - Establishes referential integrity between tables.
6. **Composite Key**:
   - A key (candidate, primary, or foreign) composed of **two or more attributes**.
   - *Example*: In `Enrollment(Student_ID, Course_ID, Semester)`, the primary key is the composite pair `(Student_ID, Course_ID)`.
7. **Surrogate Key**:
   - An artificial, system-generated unique identifier added to an entity when natural keys are cumbersome or non-existent (e.g., auto-incrementing integer `ID`, UUID).

---

# MODULE 5: ENTITY-RELATIONSHIP (ER) MODELING

### 5.1 Basic ER Concepts
The ER model represents real-world systems as **Entities** and **Relationships**.

#### 1. Entity & Entity Sets:
- **Entity**: A real-world object or concept distinguishable from other objects (e.g., Student "Alice", Car "XYZ-123").
- **Entity Set**: A collection of similar entities sharing the same properties (e.g., the set of all students in a college).
- **Strong Entity**: Has an independent primary key. Represented by a **single rectangle**.
- **Weak Entity**: Cannot be uniquely identified by its own attributes alone. Depends on an identifying strong entity. Represented by a **double rectangle**.

#### 2. Attribute Types:
| Attribute Category | Explanation | ER Diagram Notation | Real-World Example |
| :--- | :--- | :--- | :--- |
| **Simple / Atomic** | Cannot be divided into smaller subparts | Single Oval | `Age`, `Gender`, `Salary` |
| **Composite** | Can be subdivided into sub-attributes | Oval connected to component ovals | `Name` (`First_Name`, `Last_Name`), `Address` |
| **Single-Valued** | Has exactly one value for a given entity | Single Oval | `DOB`, `Social_Security_Number` |
| **Multi-Valued** | Can have multiple values for one entity | **Double Oval** | `Phone_Numbers`, `Degrees`, `Skills` |
| **Stored** | Physically saved in database | Single Oval | `Date_of_Birth` |
| **Derived** | Computed dynamically from stored attributes| **Dashed / Dotted Oval** | `Age` (computed from current date - `DOB`) |
| **Key Attribute** | Uniquely identifies each entity instance | **Underlined text in Oval** | `<u>Roll_No</u>`, `<u>Emp_ID</u>` |

---

### 5.2 Relationships, Degree, and Cardinality Constraints

#### 1. Degree of a Relationship:
Number of participating entity sets:
- **Unary / Recursive (Degree 1)**: Entity related to itself (e.g., `Employee` *manages* other `Employees`).
- **Binary (Degree 2)**: Two entity sets participate (e.g., `Student` *enrolled in* `Course`).
- **Ternary (Degree 3)**: Three entity sets participate simultaneously (e.g., `Doctor`, `Patient`, and `Medicine` in a `Prescription`).

#### 2. Cardinality Ratios (Binary Relationships):
- **One-to-One (1:1)**: An entity in A is associated with at most one in B, and vice versa (e.g., `Citizen` has one `Passport`).
- **One-to-Many (1:N)**: An entity in A is associated with many in B, but an entity in B is associated with at most one in A (e.g., `Department` employs many `Employees`).
- **Many-to-One (N:1)**: Multiple entities in A map to one in B (e.g., Many `Students` belong to one `Department`).
- **Many-to-Many (M:N)**: An entity in A maps to many in B, and vice versa (e.g., `Students` enroll in many `Courses`).

#### 3. Participation Constraints:
- **Total Participation (Existence Dependency)**:
  - Every entity in the entity set MUST participate in at least one relationship instance.
  - Represented by a **double line** connecting entity set to the relationship diamond.
  - *Example*: Every `Employee` MUST work for a `Department`.
- **Partial Participation**:
  - Some entities may NOT participate in the relationship.
  - Represented by a **single line**.
  - *Example*: Not every `Employee` manages a `Department`.

---

### 5.3 Weak Entity Sets & Identifying Relationships
- A weak entity set does not have a primary key of its own.
- It possesses a **Partial Key / Discriminator** (represented by a **dashed underline**).
- It is linked to an identifying strong entity set through an **Identifying Relationship** (represented by a **double diamond**).
- **Rule**: Participation of a weak entity set in its identifying relationship is **ALWAYS TOTAL**.
- **Primary Key of Weak Entity**:
  $$\text{Primary Key} = (\text{Primary Key of Owner Entity}) + (\text{Discriminator of Weak Entity})$$

```
┌──────────────┐                 ╔══════════════╗                 ╔══════════════╗
│   EMPLOYEE   │─────────────────╣ DEPENDENTS_OF╠═════════════════╣  DEPENDENT   │
│ (Emp_ID,Name)│                 ╚══════════════╝                 ║ (Dep_Name)   │
└──────────────┘                 Identifying Rel.                 ╚══════════════╝
  Strong Entity                                                     Weak Entity
```

---

### 5.4 Extended ER (EER) Features
1. **Specialization (Top-Down)**:
   - Breaking down a higher-level entity into specialized lower-level subclasses based on distinctive attributes.
   - *Example*: `Employee` specialized into `FullTime_Employee` and `PartTime_Employee`.
2. **Generalization (Bottom-Up)**:
   - Synthesizing shared attributes of multiple lower-level entities into a unified generalized superclass.
   - *Example*: `Car` and `Truck` generalized into `Vehicle`.
3. **Constraints on Specialization/Generalization**:
   - **Disjointness Constraint**:
     - *Disjoint (`d`)*: An entity can belong to at most one subclass (e.g., a person is either Male or Female).
     - *Overlapping (`o`)*: An entity can belong to multiple subclasses simultaneously (e.g., a university person can be both an Employee and a Student).
   - **Completeness Constraint**:
     - *Total Specialization (Double Line)*: Every superclass entity MUST belong to at least one subclass.
     - *Partial Specialization (Single Line)*: An entity may belong only to the superclass without belonging to any subclass.
4. **Aggregation**:
   - An abstraction through which a relationship between entities is treated as a higher-level entity set so it can participate in other relationships.

---

# MODULE 6: RELATIONAL MODEL BASICS & INTEGRITY CONSTRAINTS

### 6.1 Formal Terminology
Introduced by Dr. E.F. Codd in 1970 based on first-order predicate logic and set theory.

| Relational Model Term | Informal SQL Term | Formal Definition |
| :--- | :--- | :--- |
| **Relation** | Table | A mathematical subset of the Cartesian product of a list of domains: $R \subseteq D_1 \times D_2 \times \dots \times D_n$. |
| **Tuple** | Row / Record | An ordered list of values representing an individual record. |
| **Attribute** | Column / Field | A named property or characteristic of a relation. |
| **Domain** | Data Type & Valid Range| The set of all permissible atomic values for an attribute. |
| **Degree (Arity)** | Column Count | Total number of attributes in the relation schema. |
| **Cardinality** | Row Count | Total number of tuples currently stored in the relation instance. |

#### Formal Properties of Relations:
1. **Tuples are Unordered**: The ordering of rows has no mathematical significance.
2. **Attributes are Unordered**: Columns are identified by name, not index.
3. **Values are Atomic**: First Normal Form (1NF) rule — composite or multivalued attributes are forbidden in a normalized relational tuple.
4. **All Tuples are Distinct**: A relation is a mathematical set; no two identical tuples can exist.

---

### 6.2 Relational Integrity Constraints
Constraints are rules that every valid state of the database must satisfy:

1. **Domain Constraint**:
   - Every attribute value in a tuple must be an atomic element belonging to the attribute's defined domain.
2. **Key Constraint**:
   - No two distinct tuples in any valid relation state can have identical values for all attributes in a Candidate Key.
3. **Entity Integrity Constraint**:
   - No attribute part of the **Primary Key** can take a `NULL` value.
   - *Justification*: The primary key is used to address individual tuples. If a key contains `NULL`, the tuple cannot be uniquely identified or referenced.
4. **Referential Integrity Constraint**:
   - A value appearing in a **Foreign Key** column of a referencing table $R_1$ must either:
     1. Match an existing **Primary Key** value in the referenced table $R_2$, OR
     2. Be explicitly `NULL` (signifying no association).

#### Foreign Key Referential Actions:
When a referenced row is deleted or updated, the DBMS enforces one of the following rules:
- `ON DELETE / UPDATE RESTRICT` (or `NO ACTION`): Blocks the deletion/update with an integrity violation error.
- `ON DELETE / UPDATE CASCADE`: Propagates the deletion/update to all referencing rows.
- `ON DELETE / UPDATE SET NULL`: Sets the foreign key column in all referencing rows to `NULL`.
- `ON DELETE / UPDATE SET DEFAULT`: Sets the foreign key column in referencing rows to its default value.

---

# MODULE 7: CONVERSION OF ER TO RELATIONAL MODEL (THE 7-STEP ALGORITHM)

```
                       ┌─────────────────────────┐
                       │  ER TO SCHEMA MAPPING   │
                       └────────────┬────────────┘
                                    │
    ┌───────────────┬───────────────┼───────────────┬───────────────┐
    ▼               ▼               ▼               ▼               ▼
1. Strong      2. Weak         3. 1:1 & 1:N    4. M:N          5. Multivalued
   Entity         Entity          Relations       Relations       Attributes
 (Direct PK)    (Owner PK +     (FK on 'N' or   (Junction Table (Separate Table
                 Partial Key)    total side)     Composite PK)   PK = (Owner PK + Attr))
```

### Step 1: Mapping Strong Entity Sets
- For each strong entity set $E$, create a relation $R$.
- Include all simple attributes.
- For composite attributes, flatten and include only simple sub-attributes (e.g., `Name` with `FName`, `LName` becomes columns `FName` and `LName`).
- **Primary Key of $R$** = Primary Key of $E$.

### Step 2: Mapping Weak Entity Sets
- For each weak entity set $W$ with owner entity set $O$:
- Create a relation $R_W$.
- Include all simple attributes of $W$.
- Add the Primary Key of $O$ as a Foreign Key in $R_W$.
- **Primary Key of $R_W$**: Composite Key = $(\text{Primary Key of } O) + (\text{Discriminator of } W)$.
- **Foreign Key**: `FOREIGN KEY (Owner_PK) REFERENCES O(Owner_PK) ON DELETE CASCADE`.

### Step 3: Mapping 1:1 Binary Relationship Sets
Let $R$ be a 1:1 relationship between entity sets $S$ and $T$:
- **Approach 1 (Foreign Key Approach - Standard)**:
  - Choose one relation (preferably the one with **Total Participation**).
  - Add the Primary Key of the other relation as a Foreign Key with a `UNIQUE` constraint.
  - Include any descriptive attributes of the relationship in that table.
- **Approach 2 (Merged Relation)**:
  - If **both** sides have Total Participation, merge $S$, $T$, and the relationship into a single unified table.
- **Approach 3 (Cross-Reference / Junction Table)**:
  - Create a third table with primary keys of both $S$ and $T$. Rarely used for 1:1 due to unnecessary join overhead.

### Step 4: Mapping 1:N (or N:1) Binary Relationship Sets
- Identify the entity on the **Many ($N$) side**.
- Take the Primary Key of the **$1$-side** entity and place it as a **Foreign Key** in the $N$-side relation.
- Copy any attributes of the relationship into the $N$-side relation.
- *Memory Rule*: *"The Foreign Key always goes to the Many side."*

### Step 5: Mapping M:N Binary Relationship Sets
- Create a dedicated **Junction / Associative Relation** $R$.
- Include the Primary Keys of both participating entity sets as Foreign Keys.
- Include any descriptive attributes of the relationship.
- **Primary Key of $R$**: **Composite Key** formed by combining both Foreign Keys.

### Step 6: Mapping Multivalued Attributes
- For each multivalued attribute $A$ in entity $E$:
- Create a new relation $R_A$.
- Include attribute $A$ and the Primary Key $K$ of entity $E$ as a Foreign Key.
- **Primary Key of $R_A$**: **Composite Key** $= (K, A)$.

### Step 7: Mapping Specialization / Generalization (Inheritance)
1. **Option 4A: Multiple Relations for Superclass and Subclasses**:
   - Superclass table with PK and common attributes.
   - Subclass tables with subclass attributes + Superclass PK as both Primary Key and Foreign Key.
   - *Best for*: General case (disjoint or overlapping).
2. **Option 4B: Subclass Relations Only**:
   - Tables only for subclasses; each table replicates all superclass attributes.
   - *Best for*: Total and Disjoint specialization only.
3. **Option 4C: Single Relation with Type / Discriminator Attribute**:
   - One giant table with all attributes of superclass and all subclasses, plus a `Type` column. Subclass-specific columns will be `NULL` for other types.
   - *Best for*: Disjoint specialization with few subclass-specific attributes.

---

# MODULE 8: RELATIONAL ALGEBRA (PROCEDURAL QUERY LANGUAGE)

Relational Algebra is a formal, mathematical procedural query language. It takes one or two relations as input and yields a new relation as output (**Closure Property**).

### 8.1 Fundamental Operators

#### 1. Selection ($\sigma$): Horizontal Filtering
- **Syntax**: $\sigma_{\text{predicate}}(R)$
- Filters tuples that satisfy the boolean condition.
- *Example*: Find employees in department 10 earning more than 50,000:
  $$\sigma_{\text{Dept\_ID} = 10 \land \text{Salary} > 50000}(\text{EMPLOYEE})$$

#### 2. Projection ($\Pi$): Vertical Slicing
- **Syntax**: $\Pi_{A_1, A_2, \dots, A_k}(R)$
- Selects specified columns and **automatically removes duplicate tuples** (since relations are sets).
- *Example*: List names and salaries of all employees:
  $$\Pi_{\text{Name}, \text{Salary}}(\text{EMPLOYEE})$$

#### 3. Cartesian Product ($\times$): Cross Combination
- **Syntax**: $R \times S$
- Concatenates every tuple of $R$ with every tuple of $S$.
- Degree = $\text{Degree}(R) + \text{Degree}(S)$
- Cardinality = $\text{Card}(R) \times \text{Card}(S)$

#### 4. Union ($\cup$): Set Union
- **Syntax**: $R \cup S$
- Returns all tuples present in $R$, $S$, or both.
- **Precondition (Union Compatibility)**:
  1. $R$ and $S$ must have the exact same degree (number of attributes).
  2. The domains of corresponding $i$-th attributes must be compatible.

#### 5. Set Difference ($-$)
- **Syntax**: $R - S$
- Returns tuples in $R$ that are **NOT** present in $S$. Must be union-compatible.

#### 6. Rename ($\rho$)
- **Syntax**: $\rho_{S(B_1, B_2, \dots, B_n)}(R)$ or $\rho_S(R)$
- Renames relation $R$ to $S$ and optionally renames attributes.

---

### 8.2 Derived Operators

#### 1. Set Intersection ($\cap$)
- **Syntax**: $R \cap S$
- Mathematically derived as: $R \cap S = R - (R - S)$

#### 2. Theta Join ($\bowtie_\theta$)
- Combines Cartesian product with a selection condition:
  $$R \bowtie_\theta S = \sigma_\theta(R \times S)$$

#### 3. Natural Join ($\bowtie$)
- Equijoin performed on all common attribute names; duplicate column copies are eliminated.
  $$R \bowtie S = \Pi_{\text{Distinct Attrs}}(\sigma_{R.A_1=S.A_1 \land \dots \land R.A_k=S.A_k}(R \times S))$$

#### 4. Division Operator ($\div$) — The Universal Quantifier
- Used for queries with the word **"ALL"** or **"EVERY"**.
- Let $R(A, B)$ and $S(B)$. $R \div S$ returns all values of $A$ in $R$ that are associated with **EVERY** value of $B$ in $S$.
- **Formal Algebraic Derivation using primitives**:
  $$R \div S = \Pi_A(R) - \Pi_A\Big((\Pi_A(R) \times S) - R\Big)$$
- *Exam Step-by-Step Breakdown*:
  1. $\Pi_A(R)$: All candidate values of $A$.
  2. $\Pi_A(R) \times S$: All possible pairs of candidates with all target items.
  3. $(\Pi_A(R) \times S) - R$: Pairs that did **NOT** occur in reality (the "disqualifiers").
  4. $\Pi_A(\dots)$: Candidates who missed at least one required item.
  5. $\Pi_A(R) - \text{Disqualified}$: Candidates who completed **ALL** items.

---

### 8.3 10 Standard Relational Algebra Query Problems
Given Schema:
- $\text{STUDENT}(\underline{\text{SID}}, \text{SName}, \text{GPA})$
- $\text{COURSE}(\underline{\text{CID}}, \text{CName}, \text{Credits})$
- $\text{ENROLLED}(\underline{\text{SID}, \text{CID}}, \text{Grade})$

**Q1: Find names of students enrolled in course 'CS101'.**
$$\Pi_{\text{SName}}\Big(\text{STUDENT} \bowtie \sigma_{\text{CID} = '\text{CS101}'}(\text{ENROLLED})\Big)$$

**Q2: Find names of students who have NEVER enrolled in any course.**
$$\Pi_{\text{SName}}\Big(\text{STUDENT} \bowtie \big(\Pi_{\text{SID}}(\text{STUDENT}) - \Pi_{\text{SID}}(\text{ENROLLED})\big)\Big)$$

**Q3: Find names of students enrolled in BOTH 'CS101' and 'CS102'.**
$$\Pi_{\text{SName}}\Big(\text{STUDENT} \bowtie \big(\Pi_{\text{SID}}(\sigma_{\text{CID}='CS101'}(\text{ENROLLED})) \cap \Pi_{\text{SID}}(\sigma_{\text{CID}='CS102'}(\text{ENROLLED}))\big)\Big)$$

**Q4: Find names of students enrolled in 'CS101' OR 'CS102'.**
$$\Pi_{\text{SName}}\Big(\text{STUDENT} \bowtie \big(\Pi_{\text{SID}}(\sigma_{\text{CID}='CS101' \lor \text{CID}='CS102'}(\text{ENROLLED}))\big)\Big)$$

**Q5: Find students enrolled in ALL courses (The Division Problem).**
$$\Pi_{\text{SName}}\Big(\text{STUDENT} \bowtie \big(\Pi_{\text{SID}, \text{CID}}(\text{ENROLLED}) \div \Pi_{\text{CID}}(\text{COURSE})\big)\Big)$$

**Q6: Find courses that have at least two students enrolled.**
$$\Pi_{\text{CID}}\Big(\sigma_{E1.\text{SID} \ne E2.\text{SID}}\big(\rho_{E1}(\text{ENROLLED}) \bowtie_{E1.\text{CID} = E2.\text{CID}} \rho_{E2}(\text{ENROLLED})\big)\Big)$$

**Q7: Find the highest GPA among all students without using aggregate functions.**
- *Step 1 (Find all GPAs that are NOT the highest)*:
  $$\text{LowerGPAs} \leftarrow \Pi_{S1.\text{GPA}}\Big(\rho_{S1}(\text{STUDENT}) \bowtie_{S1.\text{GPA} < S2.\text{GPA}} \rho_{S2}(\text{STUDENT})\Big)$$
- *Step 2 (Subtract from all GPAs)*:
  $$\text{MaxGPA} \leftarrow \Pi_{\text{GPA}}(\text{STUDENT}) - \text{LowerGPAs}$$

**Q8: Find names of students whose GPA is strictly higher than 'Bob'.**
$$\Pi_{S1.\text{SName}}\Big(\rho_{S1}(\text{STUDENT}) \bowtie_{S1.\text{GPA} > S2.\text{GPA}} \sigma_{S2.\text{SName}='Bob'}(\rho_{S2}(\text{STUDENT}))\Big)$$

**Q9: Find students who have taken only 4-credit courses.**
$$\Pi_{\text{SID}}(\text{ENROLLED}) - \Pi_{\text{SID}}\Big(\text{ENROLLED} \bowtie \sigma_{\text{Credits} \ne 4}(\text{COURSE})\Big)$$

**Q10: Find pairs of students who share the exact same GPA.**
$$\Pi_{S1.\text{SName}, S2.\text{SName}}\Big(\sigma_{S1.\text{SID} < S2.\text{SID} \land S1.\text{GPA}=S2.\text{GPA}}\big(\rho_{S1}(\text{STUDENT}) \times \rho_{S2}(\text{STUDENT})\big)\Big)$$

---

# MODULE 9: SQL DATA DEFINITION LANGUAGE (DDL)

DDL commands define, modify, and destroy the database schema and structure.

### 9.1 CREATE TABLE with Complete Constraints
```sql
CREATE TABLE Departments (
    dept_id     INT PRIMARY KEY,
    dept_name   VARCHAR(50) NOT NULL UNIQUE,
    budget      DECIMAL(12,2) CHECK (budget > 0),
    location    VARCHAR(50) DEFAULT 'Main Campus'
);

CREATE TABLE Employees (
    emp_id      INT PRIMARY KEY,
    emp_name    VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    salary      DECIMAL(10,2) CHECK (salary >= 20000),
    dept_id     INT,
    manager_id  INT,
    -- Foreign Key referencing Departments
    CONSTRAINT fk_emp_dept 
        FOREIGN KEY (dept_id) 
        REFERENCES Departments(dept_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    -- Self-referencing Foreign Key
    CONSTRAINT fk_emp_mgr 
        FOREIGN KEY (manager_id) 
        REFERENCES Employees(emp_id) 
        ON DELETE RESTRICT
);
```

---

### 9.2 ALTER TABLE Syntax & Modifications
Used to change table structure after creation:

```sql
-- 1. Add a new column
ALTER TABLE Employees ADD date_of_joining DATE;

-- 2. Drop an existing column
ALTER TABLE Employees DROP COLUMN date_of_joining;

-- 3. Modify column data type / constraint
ALTER TABLE Employees MODIFY salary DECIMAL(12,2) NOT NULL; -- MySQL
-- ALTER TABLE Employees ALTER COLUMN salary DECIMAL(12,2); -- SQL Server / Postgres

-- 4. Add a named constraint
ALTER TABLE Employees ADD CONSTRAINT chk_emp_name_len CHECK (LENGTH(emp_name) >= 2);

-- 5. Drop a constraint
ALTER TABLE Employees DROP CONSTRAINT chk_emp_name_len;
```

---

### 9.3 DROP TABLE vs. TRUNCATE TABLE vs. DELETE
The most frequent comparison question in exams:

| Feature | DELETE | TRUNCATE | DROP |
| :--- | :--- | :--- | :--- |
| **Command Category** | **DML** (Data Manipulation) | **DDL** (Data Definition) | **DDL** (Data Definition) |
| **Operation** | Deletes specific tuples | Removes all tuples | Destroys entire table & schema |
| **WHERE Clause** | **Supported** (`WHERE id=5`) | **Not supported** | **Not supported** |
| **Rollback Support** | **Yes** (inside transaction) | **No** (implicit auto-commit) | **No** (implicit auto-commit) |
| **Speed** | Slow (row-by-row logging) | Very Fast (deallocates pages) | Instantaneous |
| **Auto-Increment ID** | Counter retained | Counter reset to initial seed | Table destroyed |
| **Triggers** | Fires `ON DELETE` triggers | Does **NOT** fire triggers | Does **NOT** fire triggers |
| **Table Structure** | Remains intact | Remains intact | Completely deleted from catalog |

---

# MODULE 10: SQL DATA MANIPULATION LANGUAGE (DML)

### 10.1 INSERT Statement
```sql
-- 1. Inserting single record with all column values
INSERT INTO Departments VALUES (10, 'Computer Science', 500000.00, 'Block A');

-- 2. Inserting specific columns (remaining take default or NULL)
INSERT INTO Departments (dept_id, dept_name) VALUES (20, 'Mechanical');

-- 3. Inserting multiple records in one batch
INSERT INTO Employees (emp_id, emp_name, salary, dept_id, manager_id) VALUES 
(101, 'Alice Smith', 95000, 10, NULL),
(102, 'Bob Jones', 72000, 10, 101),
(103, 'Charlie Day', 60000, 20, 101);

-- 4. INSERT INTO ... SELECT (Populating from another query)
INSERT INTO High_Earners (emp_id, emp_name, salary)
SELECT emp_id, emp_name, salary FROM Employees WHERE salary > 80000;
```

---

### 10.2 UPDATE Statement
```sql
-- Conditional update
UPDATE Employees
SET salary = salary * 1.10
WHERE dept_id = 10 AND salary < 80000;

-- Multi-column update with subquery
UPDATE Employees
SET salary = 90000, dept_id = 20
WHERE emp_id = 103;
```

---

### 10.3 DELETE Statement
```sql
-- Conditional delete
DELETE FROM Employees
WHERE dept_id = 20 AND salary < 50000;

-- Delete all rows (DML approach, retains schema)
DELETE FROM Employees;
```

---

# MODULE 11: SQL DATA QUERY LANGUAGE (DQL)

### 11.1 The SELECT Statement, Expressions & Aliases
```sql
SELECT emp_name AS Employee, salary, salary * 0.15 AS Estimated_Tax
FROM Employees;

-- Eliminating duplicates
SELECT DISTINCT dept_id FROM Employees;
```

---

### 11.2 The WHERE Clause & Filtering Operators
1. **Comparison Operators**: `=`, `<>`, `!=`, `<`, `>`, `<=`, `>=`.
2. **Logical Operators**: `AND`, `OR`, `NOT` (precedence: `NOT` > `AND` > `OR`).
3. **Range Operator (`BETWEEN ... AND ...`)**:
   ```sql
   SELECT * FROM Employees WHERE salary BETWEEN 60000 AND 90000; -- Inclusive
   ```
4. **List Membership Operator (`IN`, `NOT IN`)**:
   ```sql
   SELECT * FROM Employees WHERE dept_id IN (10, 20, 30);
   ```
5. **Pattern Matching (`LIKE`)**:
   - `%` matches 0 or more characters.
   - `_` matches exactly 1 character.
   ```sql
   SELECT * FROM Employees WHERE emp_name LIKE 'A%e'; -- Starts with A, ends with e
   SELECT * FROM Employees WHERE emp_name LIKE '_o%'; -- Second character is 'o'
   ```
6. **Testing for NULLs (`IS NULL`, `IS NOT NULL`)**:
   - *Never use `= NULL`!* In SQL 3-valued logic, `col = NULL` evaluates to `UNKNOWN`.
   ```sql
   SELECT * FROM Employees WHERE manager_id IS NULL;
   ```

---

### 11.3 Sorting with ORDER BY
```sql
-- Multi-column sort: Department ascending, then salary descending
SELECT emp_name, dept_id, salary
FROM Employees
ORDER BY dept_id ASC, salary DESC;
```

---

# MODULE 12: AGGREGATE FUNCTIONS, GROUP BY & HAVING

### 12.1 The 5 Standard Aggregate Functions
Aggregate functions compute a single summary value over a set of rows:
1. `COUNT(*)`: Returns the total count of rows, including `NULL` values.
2. `COUNT(column)`: Returns the count of non-NULL values in that column.
3. `SUM(column)`: Returns the arithmetic sum of non-NULL numeric values.
4. `AVG(column)`: Returns arithmetic mean of non-NULL numeric values.
5. `MIN(column)` / `MAX(column)`: Returns minimum/maximum non-NULL value.

---

### 12.2 GROUP BY Mechanics & Golden Rules
The `GROUP BY` clause condenses rows that have the same values in specified columns into summary rows.

> [!IMPORTANT]
> **The Golden Rule of GROUP BY**:
> When a query contains a `GROUP BY` clause, every column in the `SELECT` list that is **NOT** wrapped in an aggregate function **MUST** appear in the `GROUP BY` clause!

```sql
-- Valid
SELECT dept_id, COUNT(*) AS emp_count, AVG(salary) AS avg_sal
FROM Employees
GROUP BY dept_id;

-- INVALID (Syntax Error in ANSI SQL):
-- SELECT dept_id, emp_name, AVG(salary) FROM Employees GROUP BY dept_id;
-- 'emp_name' is neither grouped nor aggregated!
```

---

### 12.3 WHERE vs. HAVING
| Property | WHERE Clause | HAVING Clause |
| :--- | :--- | :--- |
| **Operation Target** | Filters individual **rows** before grouping | Filters **groups / buckets** after grouping |
| **Aggregate Functions** | **FORBIDDEN** (`WHERE SUM(sal) > 5000` is illegal) | **ALLOWED** (`HAVING AVG(salary) > 50000`) |
| **Execution Timing** | Before `GROUP BY` | After `GROUP BY` |

```sql
SELECT dept_id, AVG(salary) AS avg_dept_salary
FROM Employees
WHERE salary > 30000            -- 1. Filter out base rows under 30k
GROUP BY dept_id               -- 2. Group surviving rows by department
HAVING COUNT(*) >= 2;          -- 3. Keep only departments with at least 2 people
```

---

### 12.4 Exact Logical SQL Execution Order
```
1. FROM & JOIN     --> Identify source tables and perform join cartesian/matching
2. WHERE           --> Filter individual tuples (no aggregates allowed)
3. GROUP BY        --> Form groups of tuples based on grouping columns
4. HAVING          --> Filter groups based on group aggregate properties
5. SELECT          --> Evaluate expressions and select requested columns
6. DISTINCT        --> Eliminate duplicate output tuples
7. ORDER BY        --> Sort final output rows
8. LIMIT / OFFSET  --> Restrict final returned slice
```

---

# MODULE 13: SQL JOINS MASTERCLASS

Let's use a unified sample dataset to demonstrate all join types:

**Table `Employees` (`E`)**:
| emp_id | emp_name | salary | dept_id | manager_id |
| :--- | :--- | :--- | :--- | :--- |
| 101 | Alice | 95000 | 10 | NULL |
| 102 | Bob | 72000 | 10 | 101 |
| 103 | Charlie | 85000 | 20 | 101 |
| 104 | Diana | 60000 | NULL | 103 |

**Table `Departments` (`D`)**:
| dept_id | dept_name |
| :--- | :--- |
| 10 | Engineering |
| 20 | Research |
| 30 | Marketing |

---

### 13.1 INNER JOIN
Returns only matching rows from both tables:
```sql
SELECT E.emp_name, D.dept_name
FROM Employees E
INNER JOIN Departments D ON E.dept_id = D.dept_id;
```
**Output**:
| emp_name | dept_name |
| :--- | :--- |
| Alice | Engineering |
| Bob | Engineering |
| Charlie | Research |

*(Diana is excluded because `dept_id` is NULL; Marketing is excluded because it has no employees).*

---

### 13.2 LEFT OUTER JOIN
Returns all rows from Left table (`Employees`), plus matching Right table attributes; fills unmatched columns with `NULL`:
```sql
SELECT E.emp_name, COALESCE(D.dept_name, 'Unassigned') AS dept_name
FROM Employees E
LEFT OUTER JOIN Departments D ON E.dept_id = D.dept_id;
```
**Output**:
| emp_name | dept_name |
| :--- | :--- |
| Alice | Engineering |
| Bob | Engineering |
| Charlie | Research |
| Diana | Unassigned |

---

### 13.3 RIGHT OUTER JOIN
Returns all rows from Right table (`Departments`), plus matching Left table attributes; fills unmatched with `NULL`:
```sql
SELECT E.emp_name, D.dept_name
FROM Employees E
RIGHT OUTER JOIN Departments D ON E.dept_id = D.dept_id;
```
**Output**:
| emp_name | dept_name |
| :--- | :--- |
| Alice | Engineering |
| Bob | Engineering |
| Charlie | Research |
| NULL | Marketing |

---

### 13.4 FULL OUTER JOIN
Combines LEFT and RIGHT joins; returns all rows from both tables padded with NULLs:
```sql
SELECT E.emp_name, D.dept_name
FROM Employees E
FULL OUTER JOIN Departments D ON E.dept_id = D.dept_id;
```
*(In SQLite / MySQL which lack native FULL JOIN, emulate with `LEFT JOIN ... UNION ... RIGHT JOIN`).*

---

### 13.5 SELF JOIN
A table joined with itself to model hierarchical or recursive relationships (e.g., Employee $\rightarrow$ Manager):
```sql
SELECT E.emp_name AS Employee, COALESCE(M.emp_name, 'No Manager (CEO)') AS Manager
FROM Employees E
LEFT OUTER JOIN Employees M ON E.manager_id = M.emp_id;
```
**Output**:
| Employee | Manager |
| :--- | :--- |
| Alice | No Manager (CEO) |
| Bob | Alice |
| Charlie | Alice |
| Diana | Charlie |

---

### 13.6 NATURAL JOIN & CROSS JOIN
- **NATURAL JOIN**: Automatically joins tables on all columns sharing the same name and datatype.
  ```sql
  SELECT * FROM Employees NATURAL JOIN Departments;
  ```
- **CROSS JOIN**: Produces Cartesian product ($M \times N$ rows).
  ```sql
  SELECT * FROM Employees CROSS JOIN Departments;
  ```

---

# MODULE 14: NESTED QUERIES & SUBQUERIES

A subquery is a query nested within another SQL statement.

### 14.1 Subquery Types by Returned Cardinality
1. **Scalar Subquery**: Returns exactly 1 row and 1 column. Uses scalar operators (`=`, `<`, `>`).
   ```sql
   -- Find employees earning more than the company average
   SELECT emp_name, salary
   FROM Employees
   WHERE salary > (SELECT AVG(salary) FROM Employees);
   ```
2. **Multi-Row Subquery**: Returns a column of values. Uses set comparison operators (`IN`, `NOT IN`, `ANY`, `ALL`):
   - `> ALL (...)`: Greater than the maximum in the subquery.
   - `> ANY (...)`: Greater than at least one (greater than minimum).
   ```sql
   -- Employees earning more than ALL employees in Department 20
   SELECT emp_name, salary
   FROM Employees
   WHERE salary > ALL (SELECT salary FROM Employees WHERE dept_id = 20);
   ```

---

### 14.2 Correlated vs. Non-Correlated Subqueries
- **Non-Correlated Subquery**: Independent of outer query. Executes **once**; result is passed to outer query.
- **Correlated Subquery**: References columns from the outer query's current candidate row. Executes **once for every candidate row** of the outer query.

```sql
-- Find employees who earn more than the average of THEIR OWN department:
SELECT E1.emp_name, E1.salary, E1.dept_id
FROM Employees E1
WHERE E1.salary > (
    SELECT AVG(E2.salary)
    FROM Employees E2
    WHERE E2.dept_id = E1.dept_id
);
```

---

### 14.3 EXISTS and NOT EXISTS
Tests for the presence or absence of rows. Short-circuits immediately upon finding the first matching tuple:

```sql
-- Find departments that have at least one employee
SELECT D.dept_name
FROM Departments D
WHERE EXISTS (
    SELECT 1 FROM Employees E WHERE E.dept_id = D.dept_id
);

-- Find empty departments (No employees)
SELECT D.dept_name
FROM Departments D
WHERE NOT EXISTS (
    SELECT 1 FROM Employees E WHERE E.dept_id = D.dept_id
);
```

> [!CAUTION]
> **The `NOT IN` with `NULL` Trap (Examiner Favorite!)**:
> If the subquery returns even **one NULL**, `NOT IN` will return **empty set**! Always prefer `NOT EXISTS` over `NOT IN` for subqueries.

---

# MODULE 15: SET OPERATIONS (UNION, INTERSECT, MINUS / EXCEPT)

Set operations combine the results of two or more queries into a single result set.

### 15.1 Union Compatibility Rules
1. Both queries must specify the **exact same number of columns**.
2. The data types of corresponding columns must be compatible.

---

### 15.2 The Operators
```sql
-- 1. UNION: Combines results and eliminates duplicate rows
SELECT dept_id FROM Departments
UNION
SELECT dept_id FROM Employees;

-- 2. UNION ALL: Combines results without removing duplicates (much faster)
SELECT dept_id FROM Departments
UNION ALL
SELECT dept_id FROM Employees;

-- 3. INTERSECT: Returns only rows that appear in BOTH query results
SELECT dept_id FROM Departments
INTERSECT
SELECT dept_id FROM Employees;

-- 4. MINUS / EXCEPT: Returns rows in Query 1 that do NOT appear in Query 2
SELECT dept_id FROM Departments
EXCEPT  -- In Oracle: MINUS
SELECT dept_id FROM Employees;
```

---

# MODULE 16: SQL DATA CONTROL LANGUAGE (DCL) — GRANT & REVOKE

DCL statements manage privileges and permissions on database objects.

### 16.1 Object Privileges vs. System Privileges
- **System Privileges**: Global capabilities (e.g., `CREATE TABLE`, `CREATE USER`, `DROP ANY TABLE`).
- **Object Privileges**: Permissions on specific database objects (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REFERENCES` on a specific table/view).

---

### 16.2 The GRANT Statement
```sql
-- Syntax:
-- GRANT privilege_list ON object_name TO user_or_role [WITH GRANT OPTION];

-- Granting read and insert permissions to user 'analyst_bob'
GRANT SELECT, INSERT ON Employees TO analyst_bob;

-- Granting all permissions with authority to re-grant to others
GRANT ALL ON Departments TO manager_alice WITH GRANT OPTION;
```

---

### 16.3 The REVOKE Statement
```sql
-- Syntax:
-- REVOKE privilege_list ON object_name FROM user_or_role [CASCADE | RESTRICT];

-- Revoke INSERT permission
REVOKE INSERT ON Employees FROM analyst_bob;

-- Cascading Revocation:
-- If Alice was granted WITH GRANT OPTION and granted privileges to Charlie,
-- revoking from Alice with CASCADE will automatically revoke from Charlie as well.
REVOKE ALL ON Departments FROM manager_alice CASCADE;
```

---

# MODULE 17: EXAM PRACTICE BANK — TOP 20 TRICKY QUESTIONS & MODEL ANSWERS

#### Q1: Find the 2nd Highest Salary in the Company without using `LIMIT` / `TOP`.
```sql
SELECT MAX(salary) AS Second_Highest_Salary
FROM Employees
WHERE salary < (SELECT MAX(salary) FROM Employees);
```

#### Q2: Find the N-th Highest Salary generically.
```sql
SELECT E1.salary
FROM Employees E1
WHERE (N - 1) = (
    SELECT COUNT(DISTINCT E2.salary)
    FROM Employees E2
    WHERE E2.salary > E1.salary
);
```

#### Q3: Find departments that have more than 5 employees and their total salary expenditure.
```sql
SELECT dept_id, COUNT(*) AS emp_count, SUM(salary) AS total_expense
FROM Employees
GROUP BY dept_id
HAVING COUNT(*) > 5;
```

#### Q4: Delete all duplicate rows from a table while keeping the one with the smallest ID.
```sql
DELETE FROM Employees
WHERE emp_id NOT IN (
    SELECT MIN(emp_id)
    FROM Employees
    GROUP BY emp_name, dept_id, salary
);
```

#### Q5: Find employees who work on ALL projects (Relational Division in SQL).
```sql
SELECT E.emp_id, E.emp_name
FROM Employees E
WHERE NOT EXISTS (
    SELECT P.proj_id 
    FROM Projects P
    WHERE NOT EXISTS (
        SELECT 1 
        FROM Employee_Projects EP
        WHERE EP.emp_id = E.emp_id AND EP.proj_id = P.proj_id
    )
);
```

---

## 🏁 FINAL CHECKLIST FOR EXAM DAY
1. **Be prepared to draw tables**: In subjective exams, always draw small sample input tables and result tables when writing queries or join explanations.
2. **Double lines in ER diagrams**: Remember to use double lines for total participation and double borders for weak entities.
3. **Primary Key underline**: Always underline primary key attributes in relational schemas and ER diagrams.
4. **Capitalize SQL Keywords**: Write `SELECT`, `FROM`, `WHERE`, `JOIN` in uppercase for maximum readability and instructor appeal.

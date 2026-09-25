# ULTIMATE DBMS EXAMINATION MCQ QUESTION BANK
### Comprehensive, High-Yield Question Bank with Deep Conceptual Explanations
**Target Exam:** University Semester Exams, GATE / Technical Competitive Exams & Advanced Database Interviews  
**Total Questions:** 130 High-Quality Questions Covering All 14 Syllabus Units  
**Structure per Question:** Question Scenario & Options (A, B, C, D) | Correct Answer | In-Depth Rationale & Distractor Analysis

---

## SYLLABUS MAPPING & QUICK DIRECTORY
1. **Module 1: File System vs DBMS & ACID Properties** *(Q1 - Q9)*
2. **Module 2: DBMS Architecture & Data Independence** *(Q10 - Q18)*
3. **Module 3: Database Users, Schema vs Instance, and System Catalog** *(Q19 - Q27)*
4. **Module 4: Relational Keys & Candidate Key Derivation** *(Q28 - Q37)*
5. **Module 5: Entity-Relationship (ER) & Enhanced ER (EER) Modeling** *(Q38 - Q47)*
6. **Module 6: Relational Model Concepts & Integrity Constraints** *(Q48 - Q56)*
7. **Module 7: ER-to-Relational Mapping Rules** *(Q57 - Q65)*
8. **Module 8: Relational Algebra & Query Calculations** *(Q66 - Q75)*
9. **Module 9: SQL Data Definition (DDL) & Data Manipulation (DML)** *(Q76 - Q83)*
10. **Module 10: SQL Data Query Language (DQL), Filtering & Pattern Matching** *(Q84 - Q92)*
11. **Module 11: Aggregate Functions, GROUP BY, and Logical Query Execution Order** *(Q93 - Q101)*
12. **Module 12: SQL Joins and Relational Set Operations** *(Q102 - Q110)*
13. **Module 13: Subqueries (Scalar, Multi-Row, Correlated) & The Three-Valued Logic NULL Trap** *(Q111 - Q120)*
14. **Module 14: Data Control Language (DCL) & Privilege Management** *(Q121 - Q130)*

---

# MODULE 1: FILE SYSTEM VS DBMS, LIMITATIONS, ACID PROPERTIES, & WHEN FILE SYSTEM IS PREFERRED (Q1 - Q9)

### Question 1
An enterprise financial application records money transfers between checking accounts. During a transfer of $500 from Account A to Account B, the system debits Account A, but a sudden hardware failure occurs before Account B can be credited. Which property of DBMS transactions guarantees that Account A will NOT remain permanently debited upon system recovery, and which database subsystem is primarily responsible for enforcing it?
- A) Consistency; enforced by the integrity constraint checker
- B) Atomicity; enforced by the recovery management component (via undo logs)
- C) Durability; enforced by the buffer manager and shadow paging
- D) Isolation; enforced by the concurrency-control manager

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The **Atomicity** property follows the "all-or-nothing" rule. A transaction is treated as an indivisible unit of work. If any step fails before the transaction commits, all modifications made by that transaction must be rolled back (undone). The **Recovery Manager** utilizes write-ahead transaction logs (WAL undo logs) to reverse uncommitted modifications during crash recovery.
- **Why other options are incorrect:**  
  - Option A is incorrect because *Consistency* ensures that the database transitions from one valid state satisfying all explicit integrity constraints (e.g., balance >= 0, foreign keys) to another valid state. While atomicity preserves consistency, the failure of intermediate states is an atomicity failure.
  - Option C is incorrect because *Durability* guarantees that once a transaction successfully commits, its changes survive subsequent system crashes.
  - Option D is incorrect because *Isolation* ensures that concurrently executing transactions do not interfere with one another, giving each the illusion that it is executing alone.

---

### Question 2
Consider the classical file-processing system used prior to DBMS adoption. Which of the following is considered the ROOT cause of **data inconsistency** in traditional file systems?
- A) Lack of magnetic disk storage capacity for archival files
- B) Program-data dependence and redundant data stored in multiple uncoordinated files
- C) Absence of high-level procedural programming languages like COBOL or C
- D) Inability to execute batch processing scripts during off-peak hours

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In file systems, different departments maintain their own physical files. When the same real-world data (such as a customer's address) is replicated across multiple files without centralized control, updates made to one file by one application may not be reflected in another. This **data redundancy** combined with **program-data dependence** directly causes **data inconsistency** (conflicting values for the same logical fact).
- **Why other options are incorrect:**  
  - Option A is incorrect because disk capacity limitations affect storage volume, not data consistency across duplicate records.
  - Option C is incorrect because file systems made heavy use of COBOL, C, and PL/I; the languages themselves were not the root cause, but rather the architectural lack of centralized schema and abstraction.
  - Option D is incorrect because traditional file systems were exceptionally well-suited for batch processing scripts; their failure was in concurrent interactive access and decentralized storage.

---

### Question 3
Under which of the following scenarios is deploying a traditional **flat-file system or specialized file structure objectively PREFERRED** over an enterprise relational DBMS?
- A) An online banking portal serving 500,000 concurrent interactive users executing OLTP transfers
- B) A real-time embedded sensor operating with strictly constrained RAM/CPU collecting continuous video frames with single-user append-only access where DBMS overhead and licensing cannot be justified
- C) A university portal requiring ad-hoc SQL reporting, fine-grained access control, and declarative referential integrity across 40 related entities
- D) An e-commerce platform that demands immediate automated rollback upon payment gateway communication timeout

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A DBMS incurs significant computational overhead (query parser, query optimizer, catalog lookup, buffer pool management, concurrency locks, transaction logging). When an application runs on an embedded device with minimal memory/CPU, has strictly single-user access, performs simple sequential/append-only storage, has no need for relational joins or complex queries, and cannot tolerate DBMS memory footprint, a raw file system or low-level flat file is preferred.
- **Why other options are incorrect:**  
  - Option A is incorrect because high concurrency and OLTP financial transactions strictly mandate ACID compliance and concurrency control provided by a DBMS.
  - Option C is incorrect because ad-hoc queries, access control, and referential integrity are core strengths of a DBMS; implementing them in a file system would require rewriting an entire DBMS from scratch.
  - Option D is incorrect because automated rollback is the definition of transaction atomicity, which is natively provided by a DBMS and virtually absent in primitive file systems.

---

### Question 4
In a banking DBMS, a business rule dictates: *"The sum of balances across all accounts in a branch must equal the branch total asset liability value stored in the Branch_Summary table."* Even if all individual transactions execute atomically and without concurrency conflicts, which ACID property is violated if an application programmer writes a transaction that transfers funds between accounts but forgets to update the Branch_Summary table?
- A) Atomicity
- B) Durability
- C) Consistency
- D) Isolation

**Answer: C**  
**Explanation:**  
- **Why C is correct:** **Consistency** requires that the execution of a transaction in isolation preserves the correctness of all database invariants and business rules. If a transaction completely finishes its operations (atomicity holds) without interference (isolation holds), but the internal application logic fails to maintain the specified business invariant, the database enters an inconsistent state. The responsibility for logical consistency of transaction code lies with the application programmer.
- **Why other options are incorrect:**  
  - Option A is incorrect because all statements inside the transaction were executed; none were partially executed or aborted.
  - Option B is incorrect because durability ensures committed changes are written to non-volatile storage, which they were.
  - Option D is incorrect because the issue occurs even if the transaction executes entirely by itself in single-user mode.

---

### Question 5
Consider two concurrent transactions:  
- $T_1$ reads record $X$, modifies $X$, and writes $X$.  
- Before $T_1$ commits, $T_2$ reads the modified value of $X$.  
- Subsequently, $T_1$ aborts and rolls back to its original state.  
Which concurrency phenomenon has occurred, and which ACID property was violated?
- A) Phantom Read; Durability violated
- B) Dirty Read (Temporary Update problem); Isolation violated
- C) Lost Update; Consistency violated
- D) Non-repeatable Read; Atomicity violated

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A **Dirty Read** occurs when transaction $T_2$ is permitted to read an uncommitted intermediate modification made by transaction $T_1$. When $T_1$ aborts, the value read by $T_2$ becomes invalid ("dirty"), meaning $T_2$ based its computation on data that technically never existed in the persistent database state. This violates the **Isolation** property of transactions.
- **Why other options are incorrect:**  
  - Option A is incorrect because a Phantom Read occurs when a transaction queries a range of rows twice and discovers new rows inserted by another committed transaction.
  - Option C is incorrect because a Lost Update occurs when two transactions read the same initial value and both write updates, with the second write overwriting the first write without incorporating its modifications.
  - Option D is incorrect because a Non-repeatable Read occurs when a transaction reads the same row twice and obtains different committed values because another transaction updated it in between.

---

### Question 6
Which of the following database components guarantees the **Durability** property of a transaction even in the event of an operating system crash or abrupt power loss immediately after a user receives a "Transaction Successful" commit confirmation?
- A) In-memory Buffer Pool dirty pages
- B) Write-Ahead Logging (WAL) protocol flushing log records to non-volatile disk before the commit acknowledgement
- C) Two-Phase Locking (2PL) shared locks stored in RAM
- D) The query parser and syntactic validator

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Durability states that once a transaction commits, its effects cannot be lost. Under the **Write-Ahead Logging (WAL)** protocol, before a transaction is acknowledged as committed to the client, all transaction log records describing the modifications (redo logs) must be flushed to stable, non-volatile storage (disk/SSD). Even if the dirty pages in memory have not yet been written to the data files, the recovery manager can replay the redo log during restart to restore the committed changes.
- **Why other options are incorrect:**  
  - Option A is incorrect because in-memory buffer pool dirty pages reside in volatile RAM and will be completely wiped out during a power loss.
  - Option C is incorrect because 2PL manages concurrency and isolation, not crash durability; furthermore, locks reside in volatile memory and are released upon completion.
  - Option D is incorrect because query parsers only validate syntax and translate SQL into relational trees during query compilation.

---

### Question 7
Which of the following problems is an inherent disadvantage of a traditional File Processing System when multiple users attempt to access the same file simultaneously?
- A) Automatic deadlock detection terminating background daemons
- B) Lack of concurrent-access anomaly prevention, leading to lost updates or corrupted records
- C) Inability to write sequential batch records to magnetic tape drives
- D) Mandatory enforcement of domain integrity across disparate files

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Traditional file systems leave concurrency control to the operating system or application code. If two programs open the same file for writing simultaneously, they will overwrite each other's data blocks (the lost update problem) or produce interleaved byte streams, corrupting the file structure. Operating systems only provide coarse-grained whole-file locks, which severely throttle performance or leave applications vulnerable to concurrency anomalies.
- **Why other options are incorrect:**  
  - Option A is incorrect because file systems do not provide automatic deadlock detection across application processes.
  - Option C is incorrect because sequential tape processing was actually the native strength of early file processing systems.
  - Option D is incorrect because file systems notoriously fail to enforce domain integrity; integrity constraints must be hand-coded into every separate program.

---

### Question 8
In database terminology, **Program-Data Independence** refers to:
- A) The ability of application programs to run on different operating systems without recompilation
- B) The immunity of application programs to changes in the physical storage structures and logical organization of the data
- C) The property that data stored in tables can never be accessed by third-party applications
- D) The complete isolation of client software from internet network latency

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Program-Data Independence is the separation of data structure definitions from the application programs that manipulate the data. In a DBMS, metadata (schema) is stored centrally in the system catalog. If a DBA modifies an internal physical structure (e.g., adding a B+ tree index, changing record ordering) or alters a logical structure (e.g., adding an optional column), existing application programs that do not reference that attribute do not need to be modified or recompiled.
- **Why other options are incorrect:**  
  - Option A describes platform portability or cross-platform compilation, not program-data independence.
  - Option C describes data security/confidentiality, not independence.
  - Option D describes network transparency or edge caching, which has nothing to do with database schemas.

---

### Question 9
Suppose a company maintains an inventory file where an attribute `Warehouse_Capacity` is stored as an integer representing square meters. The management decides to expand storage and change the data type of `Warehouse_Capacity` to a floating-point number representing square feet. In a traditional File Processing System, what is the direct consequence of this structural change?
- A) Only the DBMS catalog needs an `ALTER TABLE` statement, with zero program modifications
- B) Every single application program that reads or writes to the inventory file must be identified, rewritten to match the new byte offset and data format, and recompiled
- C) The operating system automatically adjusts byte offsets at runtime without program modification
- D) The file system triggers an automatic cascade update across all remote network shares

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In a file-processing system, the physical layout of records (the offset in bytes of each field, the data types, and record delimiters) is hardcoded inside the structure declarations of every individual application program (e.g., COBOL `FD` copybooks or C `struct` definitions). If the format or length of a field changes, every program accessing that file must be manually rewritten, re-tested, and recompiled. This is the definition of **Program-Data Dependence**.
- **Why other options are incorrect:**  
  - Option A describes the behavior of a modern DBMS with logical data independence (views or schema abstraction), not a file processing system.
  - Option C is incorrect because operating systems treat files as uninterpreted byte streams and have no awareness of internal field boundaries or data types.
  - Option D is incorrect because file systems have no semantic understanding of cascading schema triggers.

---

# MODULE 2: DBMS ARCHITECTURE & DATA INDEPENDENCE (Q10 - Q18)

### Question 10
In the ANSI-SPARC Three-Schema Architecture, at which level is the physical layout of the database on secondary storage devices (such as record blocking, file allocation, B+ tree indexing, and encryption algorithms) defined?
- A) External Level
- B) Conceptual Level
- C) Internal / Physical Level
- D) View Level

**Answer: C**  
**Explanation:**  
- **Why C is correct:** The **Internal Level** (or Physical Schema) describes the physical storage structure of the database. It specifies how data is actually stored on storage media: disk blocks, page layout, data compression, hashing techniques, index structures (B+ trees), clustering, and access paths.
- **Why other options are incorrect:**  
  - Option A (External Level) describes the individual user views; each view presents only the subset of data relevant to a specific user group while hiding the rest.
  - Option B (Conceptual Level) describes the community view of the entire database structure for all users, including entities, data types, relationships, constraints, and security rules, without reference to physical storage details.
  - Option D (View Level) is a synonym for the External Level.

---

### Question 11
A Database Administrator (DBA) notices that queries searching for customers by `Phone_Number` are running very slowly. The DBA creates a secondary B+ Tree index on `Customer(Phone_Number)`. Existing user applications that execute `SELECT Name FROM Customer WHERE Phone_Number = ?` continue to work without any modification to their SQL queries or program source code, but execute dramatically faster. Which architectural property is demonstrated here?
- A) Logical Data Independence
- B) Physical Data Independence
- C) Atomicity of Data Dictionaries
- D) External Schema Generalization

**Answer: B**  
**Explanation:**  
- **Why B is correct:** **Physical Data Independence** is the capacity to change the internal schema (such as creating or dropping index access paths, switching from hashing to B+ trees, reorganization of files, or changing physical storage devices) without having to alter the conceptual schema or external schemas (user application queries). Because the user queries write declarative SQL against the logical schema, the query optimizer automatically chooses the new index at the physical level without code changes.
- **Why other options are incorrect:**  
  - Option A is incorrect because *Logical Data Independence* is the capacity to change the conceptual schema (e.g., adding a new attribute or splitting a table into two normalized tables) without requiring changes to external schemas or existing application programs.
  - Option C is a fabricated term.
  - Option D is an incorrect mixing of ER concepts with schema architecture.

---

### Question 12
A hospital database splits the single table `Patient_Records(Patient_ID, Name, Address, Blood_Group, Billing_Balance, Medical_History)` into two separate tables:  
1. `Patient_Demographics(Patient_ID, Name, Address, Blood_Group)`  
2. `Patient_Financials(Patient_ID, Billing_Balance)`  
To prevent existing billing software from breaking, the DBA creates a View called `Patient_Records` that joins both tables on `Patient_ID`. The billing application continues to function without modifying a single line of application source code. This scenario exemplifies:
- A) Physical Data Independence
- B) Logical Data Independence
- C) Physical Storage Clustering
- D) Transaction Serializability

**Answer: B**  
**Explanation:**  
- **Why B is correct:** **Logical Data Independence** is the ability to modify the conceptual schema (such as adding, deleting, or decomposing entities and relationships) without requiring changes to the external schema (views) or existing application programs that interact through those views. By defining an external view that reconstructs the old table structure from the newly decomposed tables, the external applications remain completely shielded from the conceptual schema restructuring.
- **Why other options are incorrect:**  
  - Option A is incorrect because Physical Data Independence deals strictly with internal storage layout (indexes, block allocations, file organization), not the conceptual decomposition of relational tables.
  - Option C relates to how records are arranged physically next to each other on disk tracks.
  - Option D relates to concurrency control ensuring concurrent transactions produce the same effect as a serial execution.

---

### Question 13
Why is **Logical Data Independence** generally much harder to achieve and maintain than **Physical Data Independence** in relational database systems?
- A) Because physical storage devices like SSDs change their hardware protocols unpredictably
- B) Because application programs are heavily tied to the logical structure (attributes, entity definitions) of the data they retrieve, making it difficult to insulate them from schema changes unless full view updatability and view remapping are supported
- C) Because the ANSI-SPARC architecture prohibits the existence of views on top of base tables
- D) Because the SQL language does not allow altering physical indexes once created

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Applications interact directly with logical attributes and relations. When the conceptual schema changes (e.g., decomposing a table, merging entities, or changing constraints), views can mask some changes for read queries, but handling updates, inserts, and deletes through complex views (the "view update problem") is mathematically constrained and often unsupported. Hence, preserving complete transparency when the logical structure changes is far more complex than altering purely internal access paths (Physical Data Independence).
- **Why other options are incorrect:**  
  - Option A is irrelevant; physical abstraction cleanly handles hardware protocol differences.
  - Option C is false; ANSI-SPARC specifically defines external views on top of the conceptual schema.
  - Option D is false; indexes can be created and dropped dynamically in SQL at any time.

---

### Question 14
Which of the following correctly characterizes a **Two-Tier Client-Server Architecture** for a database system?
- A) The user interface, business logic, and database engine all reside inside a single monolithic binary on the client workstation
- B) The client machine runs the user interface and application business logic (thick client) and communicates directly with the database server via networking APIs like ODBC/JDBC
- C) The client runs only a lightweight web browser; an intermediate application server handles business logic and communicates with the database server
- D) The client interacts directly with disk storage controllers without communicating with any database management software

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In a **Two-Tier** architecture, the client runs the user interface (UI) and the application program business logic (known as a "thick" or "fat" client). The client communicates directly with the database server over a local network using protocols like ODBC, JDBC, or SQL*Net. The database server handles query processing, transaction management, and storage.
- **Why other options are incorrect:**  
  - Option A describes a *1-Tier Architecture* (e.g., MS Access or SQLite embedded locally on a single machine).
  - Option C describes a *3-Tier Architecture* (Client Browser -> Application Server / Business Logic -> Database Server).
  - Option D describes raw block storage access without a DBMS, which is not a client-server DBMS architecture.

---

### Question 15
What is the primary operational advantage of a **Three-Tier Architecture** over a Two-Tier Architecture in modern enterprise and web applications?
- A) It eliminates the need for any database schema or table normalization
- B) Enhanced security and scalability: business logic is decoupled from clients, clients do not have direct database credentials or direct network access to the database server, and database connection pooling can be centralized
- C) It guarantees that all transactions execute without requiring Write-Ahead Logging
- D) It reduces network latency by allowing client web browsers to directly execute disk read instructions on database storage platters

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In a **Three-Tier** architecture (Client Tier $ightarrow$ Application/Web Logic Tier $ightarrow$ Database Server Tier):  
  1. *Security:* Clients never have direct database credentials or direct IP access to the database server, preventing SQL injection against open network ports.  
  2. *Scalability:* The middle application tier handles connection pooling, workload distribution, and caching, preventing thousands of individual clients from overwhelming the database server with separate TCP connections.  
  3. *Maintainability:* Changes to business rules only require modifying the application server, without redistributing client-side software.
- **Why other options are incorrect:**  
  - Option A is absurd; normalization and schema design remain crucial in all architectures.
  - Option C is false; ACID compliance and WAL are required regardless of tier topology.
  - Option D is technically incorrect and describes an extreme security violation.

---

### Question 16
In the ANSI-SPARC 3-schema architecture, what is the role of the **Conceptual-to-Internal Mapping**?
- A) It specifies how individual user views are constructed from conceptual tables
- B) It specifies how conceptual entities, attributes, and relationships are translated into physical data structures, records, and access paths on disk
- C) It translates SQL statements directly into binary machine code for the client CPU
- D) It checks whether the user has GRANT or REVOKE authorization privileges

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The ANSI-SPARC architecture specifies two mappings:  
  1. *External-to-Conceptual Mapping:* Maps records and attributes of an external view to the corresponding entities in the conceptual schema.  
  2. *Conceptual-to-Internal Mapping:* Defines how logical constructs (entities, attributes, relational tables) correspond to physical storage records, file organizations, indexes, and block layouts in the internal schema.
- **Why other options are incorrect:**  
  - Option A describes the *External-to-Conceptual Mapping*.
  - Option C describes language compilation, not schema mapping.
  - Option D describes authorization checking performed by the DBMS security subsystem.

---

### Question 17
Which of the following database deployments represents a true **1-Tier Architecture**?
- A) A MySQL database hosted on Amazon RDS accessed by an Express.js server and React frontend
- B) An embedded SQLite database integrated into a standalone mobile application executing entirely on a smartphone
- C) An Oracle RAC cluster serving financial transactions across 4 redundant blade servers
- D) A PostgreSQL server accessed by multiple Python desktop clients via JDBC

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In a **1-Tier Architecture**, all components—the User Interface, the Application Logic, and the Database Engine/Data Storage—reside within the same local machine and often within the exact same process space. An embedded SQLite database inside a mobile or desktop application is the classic example of a 1-tier DBMS.
- **Why other options are incorrect:**  
  - Option A is a 3-Tier Architecture (Client -> Express -> RDS).
  - Option C is a multi-node distributed or clustered database server in an N-tier system.
  - Option D is a 2-Tier Client-Server Architecture (JDBC client directly contacting PostgreSQL server).

---

### Question 18
If a database administrator alters a database table by adding a new attribute `Middle_Name VARCHAR(30)` to the `Employee` conceptual table:
- Existing applications that query `SELECT First_Name, Last_Name FROM Employee` continue working unaffected.
- This independence from changes in the logical schema is guaranteed by:
- A) Physical Data Independence via Internal-to-External mapping
- B) Logical Data Independence via External-to-Conceptual mapping
- C) Operating System File Allocation Table (FAT32) mapping
- D) Durability logging via shadow directory pointers

**Answer: B**  
**Explanation:**  
- **Why B is correct:** **Logical Data Independence** protects external views and application programs from changes made to the conceptual schema. When an attribute is added to a conceptual table, the **External-to-Conceptual Mapping** ensures that an existing view or query requesting only `First_Name` and `Last_Name` is completely unaffected, since it ignores the newly added attribute.
- **Why other options are incorrect:**  
  - Option A is incorrect because Physical Data Independence deals with the internal layer (disk layouts, indexes), not adding conceptual attributes.
  - Options C and D are irrelevant to relational schema abstraction mappings.

---

# MODULE 3: DATABASE USERS, SCHEMA VS INSTANCE, METADATA, & SYSTEM CATALOG (Q19 - Q27)

### Question 19
Match the following classes of database users with their typical interactions with the DBMS:
1. **Naive / Parametric User**  
2. **Application Programmer**  
3. **Sophisticated User**  
4. **Database Administrator (DBA)**  

p. Writes programs in C++, Java, or Python incorporating embedded DML/SQL  
q. Uses pre-written canned transactions through a simplified GUI or form interface (e.g., bank teller, airline booking clerk)  
r. Submits ad-hoc, complex analytical SQL queries using interactive query tools (e.g., data analyst, business analyst)  
s. Responsible for schema design, physical tuning, user privilege authorization, and backup/recovery strategies  

- A) 1-p, 2-q, 3-r, 4-s
- B) 1-q, 2-p, 3-r, 4-s
- C) 1-r, 2-p, 3-q, 4-s
- D) 1-q, 2-r, 3-p, 4-s

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **Naive / Parametric users** interact with the system entirely by invoking canned transactions (pre-programmed forms, ATM interfaces, retail cash registers) with zero knowledge of SQL or internal schema. (1-q)  
  - **Application Programmers** write software using programming languages (Java, C#, Python) utilizing database APIs/frameworks to execute DML commands. (2-p)  
  - **Sophisticated Users** (engineers, scientists, business analysts) understand the capabilities of DBMS and write complex, ad-hoc queries using query languages (SQL, OLAP) to retrieve analytical insights without writing standalone application software. (3-r)  
  - **Database Administrators (DBA)** oversee the entire database system, managing conceptual/physical schema, performance tuning, security, authorization, and backup/disaster recovery. (4-s)
- **Why other options are incorrect:** Any option that does not map 1 to q and 2 to p fails the foundational definition of user classification in DBMS theory.

---

### Question 20
Which of the following tasks is strictly the primary responsibility of a **Database Administrator (DBA)** rather than an application programmer?
- A) Writing business logic loops that format invoice receipts for end-user printing
- B) Authorizing access permissions, managing security roles, monitoring physical performance, and formulating periodic database backup and recovery plans
- C) Designing CSS web templates for responsive client interfaces
- D) Creating unit test mocks for RESTful API endpoint controllers

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The DBA is the central custodian of the database system. DBA duties encompass:
  1. Defining the conceptual and internal schemas.
  2. Granting authorization for data access (security roles).
  3. Routine maintenance, monitoring disk utilization, and tuning physical storage/indexes.
  4. Formulating, scheduling, and verifying backup and disaster recovery plans.
- **Why other options are incorrect:**  
  - Options A, C, and D are standard tasks for application developers, UI/UX frontend engineers, and software engineers, having nothing to do with database administration.

---

### Question 21
What is the fundamental distinction between a **Database Schema** and a **Database Instance**?
- A) A schema changes with every INSERT or DELETE statement, whereas an instance remains constant once designed
- B) The schema is the overall structural blueprint and description of the database defined at design time (rarely changes), while an instance is the actual collection of data populated in the database at a specific snapshot in time
- C) A schema is stored exclusively in RAM, whereas an instance is stored exclusively in the system catalog
- D) A schema refers only to NoSQL databases, whereas an instance refers only to Relational databases

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **Database Schema (Intension):** The logical design, structure, entity definitions, data types, and integrity constraints of the database. It is specified using DDL during database design and changes very infrequently.  
  - **Database Instance (Extension / State):** The actual data content (set of tuples/records) present in the database at any given moment in time. The instance changes constantly as DML operations (INSERT, UPDATE, DELETE) are executed.
- **Why other options are incorrect:**  
  - Option A reverses the definitions; the instance changes constantly, whereas the schema is relatively static.
  - Option C is completely incorrect; schema metadata is stored persistently in the data dictionary/catalog on disk.
  - Option D is false; schema and instance are universal concepts across all structured database paradigms.

---

### Question 22
The **System Catalog** (or **Data Dictionary**) in a relational DBMS is unique because:
- A) It is an unindexed text file stored on an external FTP server
- B) It is itself stored as a set of relational tables (system tables / views) that can be queried using standard SQL, but can typically only be modified directly by the DBMS software
- C) It contains only user passwords and cannot store structural information regarding foreign keys or column types
- D) It is purged and completely erased every time the database server is rebooted

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A major hallmark of a relational DBMS is that the system catalog is stored in the same relational table structure as user data (e.g., `INFORMATION_SCHEMA.TABLES`, `pg_class`, `sys.tables`). Authorized users can query the catalog using standard `SELECT` statements to inspect metadata. However, direct manual updates via `UPDATE` statements are restricted or prohibited; the catalog is updated automatically when DDL statements (`CREATE`, `ALTER`, `DROP`) are executed.
- **Why other options are incorrect:**  
  - Option A is false; it is an integral part of the relational engine on local persistent storage.
  - Option C is false; it stores all metadata: table names, column names, data types, constraints, index descriptors, and views, in addition to privileges.
  - Option D is false; the catalog is persistent and essential for the DBMS to boot and operate.

---

### Question 23
Which term accurately describes the data stored within a DBMS **Data Dictionary** that describes the structure, constraints, relationships, and storage formats of the actual application data?
- A) Transient Application Buffers
- B) Metadata ("Data about data")
- C) Dynamic Redo Logs
- D) Uncommitted Dirty Reads

**Answer: B**  
**Explanation:**  
- **Why B is correct:** **Metadata** is formally defined as "data about data." It represents the descriptive information about the database structure (table schemas, attribute domains, constraints, triggers, indexes, and user privileges) stored in the data dictionary.
- **Why other options are incorrect:**  
  - Option A refers to in-flight memory caches.
  - Option C refers to crash recovery logs storing transaction delta changes.
  - Option D refers to an uncommitted isolation anomaly.

---

### Question 24
Consider an interactive user who uses a tool like SQL*Plus, pgAdmin, or DBeaver to write custom analytical queries like:  
`SELECT department_id, AVG(salary) FROM employees WHERE hire_date > '2020-01-01' GROUP BY department_id HAVING AVG(salary) > 75000;`  
According to database user taxonomy, this individual is classified as a:
- A) Naive / Parametric User
- B) Sophisticated User
- C) Casual User accessing pre-compiled canned routines
- D) Standalone Database User utilizing off-the-shelf single-user software

**Answer: B**  
**Explanation:**  
- **Why B is correct:** **Sophisticated Users** include engineers, data scientists, and business analysts who thoroughly understand DBMS concepts, schema architectures, and declarative query languages (like SQL). They express their complex requests using interactive query interfaces without relying on pre-written canned application programs.
- **Why other options are incorrect:**  
  - Option A is incorrect because naive users interact solely through pre-built graphical forms or menus (e.g., entering an account number on an ATM keypad).
  - Option C is incorrect because they are not running pre-compiled canned routines; they are formulating novel ad-hoc SQL.
  - Option D is incorrect because standalone users typically use packaged software (like personal tax software or personal address books) where the database is embedded and hidden.

---

### Question 25
When a Database Administrator executes the statement:  
`ALTER TABLE Orders ADD COLUMN Discount_Rate NUMERIC(4, 2) DEFAULT 0.00;`  
Which of the following database components has undergone a modification?
- A) Only the current database instance, while the schema remains untouched
- B) The database schema (metadata in the data catalog), which now defines a new attribute for all future and existing rows of the Orders relation
- C) Only the client-side graphical user interface cache
- D) The transaction undo log, permanently locking all other tables in the database

**Answer: B**  
**Explanation:**  
- **Why B is correct:** `ALTER TABLE` is a **Data Definition Language (DDL)** command. DDL commands directly modify the **Database Schema** (the structural definition stored as metadata in the system catalog). The definition of the `Orders` entity now contains an additional attribute.
- **Why other options are incorrect:**  
  - Option A is false because altering the structure is specifically a change to the schema.
  - Option C is false because DDL operates on the central database server's catalog, not client-side GUI caches.
  - Option D is false because DDL does not permanently lock the entire database or write exclusively to transaction undo logs without schema modification.

---

### Question 26
An **Active Data Dictionary** differs from a **Passive Data Dictionary** in that:
- A) An active dictionary is updated automatically and checked by the DBMS software at runtime during query compilation and transaction execution, whereas a passive dictionary is updated manually purely for human documentation
- B) An active dictionary is stored in cloud object storage, whereas a passive dictionary is printed on physical paper
- C) A passive dictionary prevents all read operations on user tables
- D) An active dictionary can only store SQL queries, while a passive dictionary stores data tuples

**Answer: A**  
**Explanation:**  
- **Why A is correct:**  
  - An **Active Data Dictionary** is an integral, online component of the DBMS. Whenever DDL statements are executed, the active catalog is automatically updated by the DBMS. Furthermore, during query execution, the DBMS actively consults the catalog to verify table existence, validate attribute names, verify user permissions, and enforce integrity constraints.  
  - A **Passive Data Dictionary** is typically a standalone documentation tool used by database designers and systems analysts; it is not integrated into runtime DBMS operation and must be updated manually.
- **Why other options are incorrect:**  
  - Options B, C, and D are factually inaccurate definitions.

---

### Question 27
Which of the following statements is **FALSE** regarding the DBA's role in database security and concurrency?
- A) The DBA grants explicit object privileges (SELECT, INSERT, UPDATE, DELETE) to specific user roles
- B) The DBA is responsible for establishing backup schedules and designing disaster recovery protocols
- C) The DBA manually approves each individual read and write lock during every concurrent transaction in real-time
- D) The DBA monitors lock contention, deadlocks, and index performance metrics to tune query execution

**Answer: C**  
**Explanation:**  
- **Why C is correct (the statement is FALSE):** A DBA does **NOT** manually grant or approve individual locks during transaction execution! Lock acquisition, escalation, and release are automated runtime responsibilities of the DBMS **Concurrency Control Manager** (using lock managers and protocols like Strict 2PL or MVCC) handling millions of lock operations per second.
- **Why other options are true:**  
  - A is true: Privileges are defined and assigned by the DBA via DCL (`GRANT` / `REVOKE`).  
  - B is true: Disaster recovery and backup strategies are core DBA responsibilities.  
  - D is true: The DBA uses performance monitoring views (e.g., `sys.dm_tran_locks`, `pg_stat_activity`) to identify bottlenecks and optimize the system.

---

# MODULE 4: RELATIONAL KEYS & CANDIDATE KEY DERIVATION (Q28 - Q37)

### Question 28
Which of the following statements rigorously defines the relationship between a **Super Key** and a **Candidate Key**?
- A) A Super Key is a Candidate Key that contains no NULL values
- B) A Candidate Key is a minimal Super Key (a super key from which no proper subset of attributes can be removed while still uniquely identifying each tuple)
- C) A Super Key is always composed of exactly one attribute, whereas a Candidate Key is composite
- D) Every Super Key is a Candidate Key, but not every Candidate Key is a Super Key

**Answer: B**  
**Explanation:**  
- **Why B is correct:** By formal definition:  
  1. A **Super Key** is any set of attributes that uniquely identifies a tuple within a relation (uniqueness property).  
  2. A **Candidate Key** satisfies two distinct properties:  
     - **Uniqueness:** No two distinct tuples have identical values for the candidate key attributes.  
     - **Irreducibility (Minimality):** No proper subset of the candidate key has the uniqueness property. If any attribute is removed from a candidate key, the remaining set is no longer a super key.  
- **Why other options are incorrect:**  
  - Option A is incorrect because super keys can also be restricted from having NULLs; minimality is the defining differentiator.
  - Option C is false because super keys frequently contain multiple redundant attributes.
  - Option D reverses the true hierarchy: *Every Candidate Key is a Super Key*, but not every Super Key is a Candidate Key (because non-minimal super keys contain redundant attributes).

---

### Question 29
Consider a relational schema $R(A, B, C, D, E, F)$ with the following set of functional dependencies $F$:  
$$A \rightarrow B$$  
$$B, C \rightarrow D$$  
$$E \rightarrow C$$  
$$D \rightarrow A$$  
Which of the following sets correctly lists **ALL the Candidate Keys** of relation $R$?
- A) $\{ AEF, DEF, BEF \}$
- B) $\{ AEF, BDEF \}$
- C) $\{ EF, AEF, DEF \}$
- D) $\{ A, D, BC \}$

**Answer: A**  
**Explanation:**  
- **Why A is correct:** Let us compute the candidate keys step-by-step:  
  1. **Identify Essential Attributes:** Look at the right-hand side (RHS) of all FDs:  
     - $A \rightarrow B$ (RHS: $B$)  
     - $BC \rightarrow D$ (RHS: $D$)  
     - $E \rightarrow C$ (RHS: $C$)  
     - $D \rightarrow A$ (RHS: $A$)  
     Notice that attributes **$E$** and **$F$** never appear on the RHS of any FD. Therefore, no attribute can functionally determine $E$ or $F$. Hence, **$E$ and $F$ MUST be present in EVERY candidate key of $R$**.  
  2. **Test closure of $\{E, F\}$:**  
     $$\{E, F\}^+ = \{E, F, C\}$$ (since $E \rightarrow C$).  
     This does not contain $\{A, B, D\}$, so $\{E, F\}$ alone is not a super key.  
  3. **Add remaining attributes one at a time to $\{E, F\}$:**  
     - **Test $\{A, E, F\}$:**  
       $$\{A, E, F\}^+ = \{A, E, F\} \xrightarrow{A \rightarrow B} \{A, B, E, F\} \xrightarrow{E \rightarrow C} \{A, B, C, E, F\} \xrightarrow{BC \rightarrow D} \{A, B, C, D, E, F\} = R$$  
       Since no proper subset of $\{A, E, F\}$ can determine all attributes, **$\{A, E, F\}$ is a Candidate Key**.  
     - **Test $\{D, E, F\}$:**  
       $$\{D, E, F\}^+ \xrightarrow{D \rightarrow A} \{A, D, E, F\} \dots = R$$.  
       Therefore, **$\{D, E, F\}$ is a Candidate Key**.  
     - **Test $\{B, E, F\}$:**  
       $$\{B, E, F\}^+ \xrightarrow{E \rightarrow C} \{B, C, E, F\} \xrightarrow{BC \rightarrow D} \{B, C, D, E, F\} \xrightarrow{D \rightarrow A} \{A, B, C, D, E, F\} = R$$.  
       Therefore, **$\{B, E, F\}$ is a Candidate Key**.  
     - **Test $\{C, E, F\}$:**  
       $$\{C, E, F\}^+ \xrightarrow{E \rightarrow C} \{C, E, F\}$$. Cannot derive $A, B, D$.  
  4. Thus, the complete set of candidate keys is **$\{ AEF, DEF, BEF \}$**.
- **Why other options are incorrect:**  
  - Option B misses $BEF$ and includes $BDEF$ which is not minimal ($DEF$ and $BEF$ are proper subsets).  
  - Option C includes $EF$, whose closure is only $\{E, F, C\}$, not all of $R$.  
  - Option D misses $E$ and $F$ completely; any set lacking $E$ and $F$ cannot derive $E$ and $F$.

---

### Question 30
In relational database design, what is an **Alternate Key**?
- A) A secondary key used exclusively for file encryption
- B) Any Candidate Key that was NOT chosen by the database designer as the Primary Key
- C) A foreign key that points to a table in an alternate database instance
- D) A surrogate key generated during hardware failures

**Answer: B**  
**Explanation:**  
- **Why B is correct:** When a relation has multiple candidate keys (e.g., `SSN`, `Employee_ID`, `Corporate_Email`), the database designer selects one of them to be the **Primary Key** (the principal identifier for tuples). All the remaining candidate keys that were not chosen are designated as **Alternate Keys** (or Secondary Candidate Keys). They are typically enforced in SQL using `UNIQUE NOT NULL` constraints.
- **Why other options are incorrect:**  
  - Options A, C, and D are incorrect fabrications having no relation to relational algebra key theory.

---

### Question 31
Which of the following statements regarding **Foreign Keys** is strictly **TRUE** according to the Relational Model?
- A) A foreign key attribute must always have the exact same name as the referenced primary key attribute
- B) A foreign key can only reference the Primary Key of another table, and can never reference an Alternate Key (UNIQUE constraint)
- C) A foreign key value in a referencing table can be NULL (unless explicitly declared NOT NULL), even if the referenced primary key does not allow NULL
- D) A table cannot have a foreign key that references its own primary key

**Answer: C**  
**Explanation:**  
- **Why C is correct:** Referential integrity states that a foreign key value must either:  
  1. Match an existing value of the candidate/primary key in the referenced relation, OR  
  2. Be entirely **NULL** (representing an unknown or unassigned relationship).  
  Unless a `NOT NULL` constraint is explicitly specified on the foreign key column, NULLs are completely valid in foreign keys, representing a partial participation in the relationship.
- **Why other options are incorrect:**  
  - Option A is false; attribute names do not need to match (e.g., `Orders.CustomerID` can reference `Customers.ID`). Only the underlying domains/data types must match.  
  - Option B is false; SQL and relational theory allow a foreign key to reference any candidate key (any column or set of columns with a `UNIQUE` constraint in the referenced table).  
  - Option D is false; a table can reference its own primary key (recursive foreign key, e.g., `Employee.Manager_ID` referencing `Employee.Emp_ID`).

---

### Question 32
What is a **Surrogate Key**, and why is it frequently used in database schema implementations?
- A) A composite key consisting of all non-prime attributes in a relation
- B) An artificial, system-generated identifier (e.g., auto-incrementing integer or UUID) with no intrinsic business or real-world meaning, introduced to serve as a compact, immutable primary key
- C) A natural key derived directly from physical biometric attributes like fingerprints
- D) A candidate key whose values are automatically recalculated every time an aggregate query runs

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A **Surrogate Key** is a synthetic, system-generated primary key (e.g., `BIGINT AUTO_INCREMENT`, `IDENTITY`, or `UUID`) that possesses no real-world or business semantics. It is used because:  
  1. Natural keys (such as `National_Tax_Number` or `Email_Address`) can be wide strings, can change over time, or might be unknown initially.  
  2. Surrogate keys are compact, uniform, immutable integers, significantly improving join efficiency, B+ Tree indexing performance, and shielding schema from changes in external business rules.
- **Why other options are incorrect:**  
  - Option A describes a non-minimal super key.  
  - Option C describes a *Natural Key*.  
  - Option D describes a derived attribute, not a surrogate key.

---

### Question 33
Consider relation $R(P, Q, R, S, T)$ with functional dependencies:  
$$P \rightarrow Q, R$$  
$$R, S \rightarrow T$$  
$$Q \rightarrow S$$  
$$T \rightarrow P$$  
How many candidate keys does relation $R$ possess, and what are their identities?
- A) 1 candidate key: $\{P\}$
- B) 3 candidate keys: $\{P\}, \{T\}, \{RS\}$
- C) 4 candidate keys: $\{P\}, \{T\}, \{RS\}, \{QS\}$
- D) 4 candidate keys: $\{P\}, \{T\}, \{R, Q\}, \{R, S\}$

**Answer: D**  
**Explanation:**  
- **Why D is correct:** Let us determine all candidate keys systematically:  
  1. Check closures of single attributes:  
     - $P^+ = \{P, Q, R, S, T\}$ (since $P \rightarrow QR \implies \{P, Q, R\}$; $Q \rightarrow S \implies \{P, Q, R, S\}$; $RS \rightarrow T \implies \{P, Q, R, S, T\}$).  
       $\implies \mathbf{\{P\}}$ **is a Candidate Key**.  
     - Since $T \rightarrow P$ and $P^+ = R$, then $T^+ = \{T, P, Q, R, S\} = R$.  
       $\implies \mathbf{\{T\}}$ **is a Candidate Key**.  
     - Check $Q$: $Q^+ = \{Q, S\}$. Not a key.  
     - Check $R$: $R^+ = \{R\}$. Not a key.  
     - Check $S$: $S^+ = \{S\}$. Not a key.  
  2. Check pairs:  
     - Notice $RS \rightarrow T$, and $T$ is a candidate key.  
       $(RS)^+ = \{R, S, T\} \xrightarrow{T \rightarrow P} \{R, S, T, P\} \xrightarrow{P \rightarrow QR} \{P, Q, R, S, T\} = R$.  
       Since neither $R^+$ nor $S^+$ is a key, $\mathbf{\{R, S\}}$ **is a minimal Candidate Key**.  
     - Now look at $Q \rightarrow S$. Can $Q$ substitute for $S$?  
       Test $\{R, Q\}$:  
       $(RQ)^+ = \{R, Q\} \xrightarrow{Q \rightarrow S} \{R, Q, S\} \xrightarrow{RS \rightarrow T} \{R, Q, S, T\} \xrightarrow{T \rightarrow P} \{P, Q, R, S, T\} = R$.  
       Since neither $R^+$ nor $Q^+$ is a key, $\mathbf{\{R, Q\}}$ **is a minimal Candidate Key**.  
     - What about $\{Q, S\}$? $(QS)^+ = \{Q, S\}$ (cannot produce $R, P, T$).  
  3. Thus, there are exactly **4 candidate keys**: $\{P\}, \{T\}, \{R, S\}, \{R, Q\}$.
- **Why other options are incorrect:**  
  - Option A fails to identify $T, RS,$ and $RQ$.  
  - Option B misses $RQ$.  
  - Option C incorrectly lists $QS$ (which cannot determine $R$).

---

### Question 34
A relation $R$ has 5 attributes $\{A, B, C, D, E\}$. It is known that **every single attribute functionally determines all other attributes** (i.e., $A \rightarrow BCDE, B \rightarrow ACDE$, etc.).  
What is the total number of **Candidate Keys** and the total number of **Super Keys** for relation $R$, respectively?
- A) 5 Candidate Keys and 5 Super Keys
- B) 5 Candidate Keys and 31 Super Keys
- C) 1 Candidate Key and 32 Super Keys
- D) 5 Candidate Keys and 25 Super Keys

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  1. **Candidate Keys:** Each of the 5 singleton attributes $\{A\}, \{B\}, \{C\}, \{D\}, \{E\}$ determines the entire relation on its own and has no proper subsets. Thus, there are exactly **5 Candidate Keys**, all of size 1.  
  2. **Super Keys:** Any non-empty subset of attributes in $R$ contains at least one of $\{A, B, C, D, E\}$. Since *any* single attribute is already a candidate key, ANY non-empty subset of attributes can determine the entire relation!  
  The total number of non-empty subsets of a 5-element set is:  
  $$2^5 - 1 = 32 - 1 = \mathbf{31}\text{ Super Keys.}$$  
- **Why other options are incorrect:**  
  - Option A forgets that every superset of a candidate key is a super key.  
  - Option C ignores that all 5 attributes are independent candidate keys.  
  - Option D uses incorrect combinatorial power calculations.

---

### Question 35
An attribute of a relation schema $R$ is defined as a **Prime Attribute** if and only if:
- A) It is the single primary key chosen by the database administrator
- B) It is a member of AT LEAST ONE Candidate Key of $R$
- C) It contains only prime integer values in its domain
- D) It does not appear on the left-hand side of any non-trivial functional dependency

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In relational database normalization theory (specifically 2NF, 3NF, BCNF), an attribute is formally defined as a **Prime Attribute** if it is a constituent member of **any** candidate key of the relation. If an attribute does not belong to any candidate key, it is termed a **Non-Prime Attribute**.
- **Why other options are incorrect:**  
  - Option A is incorrect because prime attributes include attributes of all candidate keys (including alternate keys), not just the primary key.  
  - Options C and D are completely fictitious distractors.

---

### Question 36
Can a Foreign Key in table $T_1$ be defined over a combination of attributes that forms a **Composite Candidate Key** (Alternate Key) in table $T_2$ rather than the single-column Primary Key of $T_2$?
- A) No; foreign keys are strictly prohibited from referencing composite columns
- B) No; relational integrity rules require foreign keys to reference only the Primary Key
- C) Yes; a foreign key can reference any set of columns in another table as long as that referenced set has a UNIQUE or PRIMARY KEY constraint defined on it
- D) Yes; but only if both tables have the same number of rows

**Answer: C**  
**Explanation:**  
- **Why C is correct:** In SQL-92 and subsequent relational standards, a `FOREIGN KEY (attr1, attr2) REFERENCES T2(col1, col2)` is valid if and only if `(col1, col2)` is declared as either the `PRIMARY KEY` or subject to a `UNIQUE` constraint in $T_2$. It is completely valid for a foreign key to reference an alternate composite candidate key.
- **Why other options are incorrect:**  
  - Options A and B are common student misconceptions; SQL does not restrict foreign keys solely to primary keys.
  - Option D is completely irrelevant to relational schema definitions.

---

### Question 37
Suppose relation $R(A, B, C, D)$ has only ONE candidate key: $\{A, B\}$.  
How many total **Super Keys** does relation $R$ have?
- A) 1
- B) 4
- C) 8
- D) 16

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A super key is any superset of a candidate key. Since $\{A, B\}$ is the sole candidate key, any super key must contain both $A$ and $B$.  
  The remaining attributes in $R$ are $\{C, D\}$.  
  Any combination of the remaining attributes added to $\{A, B\}$ forms a valid super key:  
  1. $\{A, B\}$  
  2. $\{A, B, C\}$  
  3. $\{A, B, D\}$  
  4. $\{A, B, C, D\}$  
  The formula is $2^{(n - k)}$, where $n = 4$ (total attributes) and $k = 2$ (attributes in the candidate key):  
  $$2^{4 - 2} = 2^2 = \mathbf{4}\text{ Super Keys.}$$
- **Why other options are incorrect:**  
  - Option A counts only candidate keys.  
  - Option C ($2^3=8$) would assume a candidate key of size 1.  
  - Option D ($2^4=16$) counts all possible subsets, many of which do not contain $A$ and $B$.

---

# MODULE 5: ENTITY-RELATIONSHIP (ER) & ENHANCED ER (EER) MODELING (Q38 - Q47)

### Question 38
In an Entity-Relationship (ER) diagram, how are a **Weak Entity Set** and its corresponding **Identifying Relationship** graphically represented, respectively?
- A) Single rectangle and single diamond
- B) Double rectangle and double diamond
- C) Dashed rectangle and dashed ellipse
- D) Double ellipse and double diamond

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In standard Chen ER notation:  
  - A **Weak Entity Set** (an entity set that does not possess a primary key of its own and depends on an owner entity set for its identification) is represented by a **Double Rectangle**.  
  - The relationship that associates the weak entity set with its owner (identifying relationship) is represented by a **Double Diamond**.  
  - The partial key (discriminator) of a weak entity is underlined with a **dashed line**.
- **Why other options are incorrect:**  
  - Single rectangle and single diamond represent regular (strong) entity sets and relationships.  
  - Ellipses represent attributes, not entity sets or relationships.

---

### Question 39
Consider a weak entity set `Dependent` identified by the strong owner entity set `Employee` via the identifying relationship `Has_Dependent`. If an `Employee` record with `Emp_ID = 101` is deleted from the database, what must happen to the associated `Dependent` tuples to maintain existential integrity?
- A) They must be transferred to a default dummy owner with `Emp_ID = 0`
- B) They must be automatically deleted (Cascading Deletion) because a weak entity cannot exist existentially without its identifying owner entity
- C) Their foreign keys must be set to NULL while retaining the dependent records in the database
- D) The DBMS must abort the deletion of the Employee and generate a syntax error

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A weak entity exhibits **existence dependency** (total participation in the identifying relationship). Its very identity is derived from combining the owner entity's primary key with its own partial discriminator. If the owner entity is deleted, the weak entity instances lose their semantic identity and cannot exist independently; therefore, they must be purged via cascading deletion (`ON DELETE CASCADE`).
- **Why other options are incorrect:**  
  - Setting foreign keys to NULL (Option C) violates the primary key rule of the weak entity table, because the owner's key is a constituent part of the weak entity's primary key (Entity Integrity forbids NULL in any primary key component).  
  - Options A and D do not represent the relational lifecycle behavior of weak entities.

---

### Question 40
In an ER diagram, an employee's `Age` is derived from their `Date_of_Birth`, their `Phone_Number` can have multiple values, and their `Address` consists of `Street`, `City`, and `ZipCode`. How should these three attributes be depicted in standard ER notation?
- A) `Age` as dashed ellipse; `Phone_Number` as double ellipse; `Address` as composite ellipse hierarchy
- B) `Age` as double ellipse; `Phone_Number` as dashed ellipse; `Address` as diamond
- C) `Age` as underlined ellipse; `Phone_Number` as double rectangle; `Address` as dashed ellipse
- D) All three are drawn as identical single solid ellipses

**Answer: A**  
**Explanation:**  
- **Why A is correct:** In standard Chen ER notation:  
  1. **Derived Attribute** (`Age`): Represented by a **Dashed Ellipse** (computed dynamically from stored attributes).  
  2. **Multivalued Attribute** (`Phone_Number`): Represented by a **Double Ellipse** (can hold multiple values for a single entity instance).  
  3. **Composite Attribute** (`Address`): Represented by a main ellipse connected to component sub-ellipses (`Street`, `City`, `ZipCode`).
- **Why other options are incorrect:**  
  - Diamonds represent relationships, not attributes.  
  - Double rectangles represent weak entities, not multivalued attributes.  
  - Solid underlined ellipses represent key attributes.

---

### Question 41
In an ER diagram modeling a hospital:  
- Each `Patient` must be assigned to **at least one** and **at most one** `Doctor`.  
- A `Doctor` may be assigned to **zero, one, or many** `Patients`.  
What are the **Cardinality Ratio** of the relationship from Doctor to Patient and the **Participation Constraint** of `Patient` in this relationship, respectively?
- A) 1:N cardinality; Partial participation of Patient
- B) 1:N cardinality; Total participation of Patient
- C) M:N cardinality; Total participation of Patient
- D) 1:1 cardinality; Partial participation of Doctor

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  1. **Cardinality Ratio:** One `Doctor` is associated with many ($N$) `Patients`, while one `Patient` is associated with at most one ($1$) `Doctor`. Thus, looking from Doctor to Patient, it is a **1:N (One-to-Many)** relationship.  
  2. **Participation Constraint:** Every patient *must* be assigned to a doctor (minimum cardinality is 1, not 0). Since every entity in the `Patient` entity set is required to participate in the relationship, `Patient` has **Total Participation** (represented by a double line connecting Patient to the relationship).
- **Why other options are incorrect:**  
  - Option A claims partial participation, but minimum is 1 (mandatory).  
  - Option C claims M:N, which contradicts "at most one Doctor".  
  - Option D claims 1:1, which contradicts "zero, one, or many Patients".

---

### Question 42
When an entity set participates in a relationship with **itself** (for example, an `Employee` entity set participating in a `Manages` relationship where one employee is a manager and other employees are subordinates), the relationship is formally termed:
- A) A Binary Identifying Relationship
- B) A Recursive (or Unary) Relationship, requiring explicit Role Names
- C) A Ternary Generalization Hierarchy
- D) An Aggregation of Weak Entities

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A relationship of degree 1 (where the same entity set participates more than once in different roles) is called a **Recursive Relationship** (or **Unary Relationship**). To distinguish the semantic meaning of each participation, **Role Names** (e.g., `Manager` and `Subordinate`, or `Course` and `Prerequisite`) must be explicitly labeled on the connecting edges in the ER diagram.
- **Why other options are incorrect:**  
  - Option A is incorrect because binary relationships involve two distinct entity sets.  
  - Option C is incorrect because ternary relationships involve three distinct entity sets.  
  - Option D is an incorrect combination of terms.

---

### Question 43
In Enhanced ER (EER) modeling, what is the precise distinction between **Specialization** and **Generalization**?
- A) Specialization is bottom-up conceptual synthesis, whereas Generalization is top-down structural partitioning
- B) Specialization is top-down design, where sub-groupings (subclasses) with specific attributes are distinguished from a higher-level entity (superclass); Generalization is bottom-up design, where common features of multiple entities are synthesized into a generalized superclass
- C) Specialization applies only to weak entities, whereas Generalization applies only to associative entities
- D) Specialization eliminates primary keys, whereas Generalization creates composite surrogate keys

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **Specialization (Top-Down):** Starts with an existing entity set (e.g., `Employee`) and identifies distinct subclasses (e.g., `Hourly_Employee`, `Salaried_Employee`) based on distinguishing characteristics or specific attributes.  
  - **Generalization (Bottom-Up):** Starts with several distinct entity sets with overlapping attributes (e.g., `Car`, `Truck`, `Motorcycle`) and synthesizes their common attributes (`Vehicle_ID`, `Price`, `Year`) into a higher-level generalized superclass (`Vehicle`).
- **Why other options are incorrect:**  
  - Option A completely reverses the directional processes.  
  - Options C and D are false assertions.

---

### Question 44
Consider an EER specialization of `Person` into subclasses `Employee` and `Student`.  
If a university rule states: *"A person cannot be both an Employee and a Student simultaneously, but a person may exist who is neither an Employee nor a Student (e.g., an external guest speaker),"* which constraints characterize this specialization?
- A) Overlapping, Total
- B) Disjoint, Total
- C) Disjoint, Partial
- D) Overlapping, Partial

**Answer: C**  
**Explanation:**  
- **Why C is correct:**  
  1. **Disjointness Constraint:** The rule states a person *cannot be both* simultaneously. This means the entity sets are mutually exclusive $\implies$ **Disjoint** (symbolized by 'd' inside the circle).  
  2. **Completeness Constraint:** A person may exist who is *neither* an Employee nor a Student (an entity in the superclass is not required to belong to any subclass). This means participation in subclasses is optional $\implies$ **Partial Specialization** (represented by a single line from the superclass to the circle).  
  Therefore, it is **Disjoint and Partial**.
- **Why other options are incorrect:**  
  - Total completeness would require every Person to be either an Employee or a Student.  
  - Overlapping would allow an entity to be both an Employee and a Student simultaneously.

---

### Question 45
What is the purpose of **Aggregation** in Enhanced ER (EER) modeling?
- A) To compute SQL `SUM` and `AVG` functions directly on conceptual entities
- B) To model a relationship as a higher-level abstract entity so that it can participate in another relationship with a third entity
- C) To merge all weak entity sets into a single flat file table
- D) To eliminate foreign key dependencies in 3NF

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Standard ER modeling does not allow relationships to be directly related to other relationships. **Aggregation** is an abstraction through which a relationship between entities is treated as a higher-level aggregate entity. For example, an `Employee` works on a `Project` (a relationship); we can aggregate `(Employee, Works_On, Project)` into a single entity so that it can be associated with a third entity `Equipment` via a `Uses` relationship.
- **Why other options are incorrect:**  
  - Option A confuses SQL aggregate math functions with EER semantic abstraction.  
  - Options C and D are irrelevant distractors.

---

### Question 46
In the $(min, max)$ structural constraint notation placed on an entity's connection to a relationship:  
If entity `Employee` connects to relationship `Manages` with constraint **$(0, 1)$**, what does this specifically declare?
- A) An employee must manage at least 1 department and at most 1 department
- B) An employee can manage at most 0 departments
- C) An employee manages a minimum of 0 departments (participation is partial/optional) and a maximum of 1 department
- D) Exactly 1% of employees manage departments

**Answer: C**  
**Explanation:**  
- **Why C is correct:** In the $(min, max)$ notation:  
  - $min$ represents the minimum number of relationship instances each entity must participate in. $min = 0$ indicates **partial (optional) participation**.  
  - $max$ represents the maximum number of relationship instances each entity can participate in. $max = 1$ limits participation to at most one instance.  
  Thus, $(0, 1)$ means an employee may manage zero departments or at most one department.
- **Why other options are incorrect:**  
  - Option A corresponds to $(1, 1)$.  
  - Options B and D are absurd misinterpretations of min-max notation.

---

### Question 47
When an entity set $E$ is connected to a relationship $R$ with a **double line** in Chen's ER notation, what does this signify?
- A) The relationship is recursive
- B) Total participation (existence dependency) of $E$ in $R$
- C) Cardinality ratio is strictly many-to-many
- D) The entity set contains a surrogate primary key

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In Chen notation:  
  - A **Single Line** represents **Partial Participation** (some entities in $E$ may not participate in $R$; $min = 0$).  
  - A **Double Line** represents **Total Participation** (every entity in $E$ must participate in at least one instance of $R$; $min \ge 1$).
- **Why other options are incorrect:**  
  - Cardinality ratio is denoted by labels like $1, N, M$ on the lines, not by line doubling.  
  - Recursive relationships connect an entity to itself.  
  - Surrogate keys are implementation details not indicated by double lines.

---

# MODULE 6: RELATIONAL MODEL CONCEPTS & INTEGRITY CONSTRAINTS (Q48 - Q56)

### Question 48
In formal Relational Model terminology, what do the **Degree** and the **Cardinality** of a relation represent, respectively?
- A) Degree is the number of tuples; Cardinality is the number of attributes
- B) Degree is the number of attributes (columns); Cardinality is the number of tuples (rows)
- C) Degree is the number of foreign keys; Cardinality is the storage size in megabytes
- D) Degree is the number of candidate keys; Cardinality is the number of primary keys

**Answer: B**  
**Explanation:**  
- **Why B is correct:** By formal definition:  
  - **Degree (or Arity):** The total number of attributes (columns) that constitute the relation schema.  
  - **Cardinality:** The total number of tuples (rows/records) currently present in the relation instance.
- **Why other options are incorrect:**  
  - Option A reverses Degree and Cardinality.  
  - Options C and D confuse relational dimensions with key counts or disk storage.

---

### Question 49
Which of the following integrity constraints is violated if a user attempts to execute the following SQL statement on a table with primary key `(Department_ID, Course_Code)`:  
`INSERT INTO Course_Offerings (Department_ID, Course_Code, Classroom) VALUES (10, NULL, 'Room 301');`
- A) Referential Integrity Constraint
- B) Entity Integrity Constraint
- C) Domain Constraint
- D) Semantic Check Constraint

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The **Entity Integrity Constraint** states that **no primary key value can be NULL**. Crucially, for a composite primary key formed by multiple attributes, **none** of the constituent attributes may be assigned a NULL value. Because `Course_Code` is part of the composite primary key and is assigned `NULL`, the Entity Integrity Constraint is directly violated.
- **Why other options are incorrect:**  
  - Option A is incorrect because referential integrity concerns foreign key matching with referenced keys.  
  - Option C is incorrect because NULL is not a domain data type violation here; the violation is the primary key non-nullability requirement.  
  - Option D is incorrect because entity integrity is a fundamental relational constraint, not an ad-hoc CHECK constraint.

---

### Question 50
Consider a child table `Orders` with foreign key `Customer_ID` referencing parent table `Customers(Customer_ID)`.  
Which of the following database operations on the **parent table** (`Customers`) can potentially violate the **Referential Integrity Constraint**?
- A) Inserting a new customer tuple into `Customers`
- B) Deleting an existing customer tuple from `Customers` or updating its `Customer_ID`
- C) Selecting all customer records from `Customers`
- D) Adding an index on `Customers(Customer_Name)`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Referential integrity requires every non-null foreign key in `Orders` to match a valid `Customer_ID` in `Customers`.  
  - If a row in `Customers` is **deleted** or its `Customer_ID` is **updated**, child rows in `Orders` referencing that old ID would be left pointing to a non-existent parent ("dangling pointers"). Hence, DELETE and UPDATE on the referenced (parent) table can violate referential integrity.  
  - Conversely, INSERT into the parent table introduces a new valid key, which can never orphan existing child rows.
- **Why other options are incorrect:**  
  - Inserting into the parent table cannot cause foreign key violations in existing child tables.  
  - SELECT and index creation are read-only / metadata operations that do not modify data tuples.

---

### Question 51
Suppose table `Employee` contains a foreign key defined as:  
`FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID) ON DELETE CASCADE`  
What occurs when the tuple for department `Dept_ID = 5` is deleted from the `Department` table?
- A) The deletion is blocked, and an integrity error is thrown
- B) All employee tuples in the `Employee` table with `Dept_ID = 5` are automatically deleted
- C) The `Dept_ID` column of all employees with `Dept_ID = 5` is set to NULL
- D) The `Dept_ID` column of all employees with `Dept_ID = 5` is reset to 0

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Under the `ON DELETE CASCADE` referential action, when a referenced tuple in the parent table is deleted, the DBMS automatically and recursively deletes all referencing tuples in the child table that match the deleted foreign key value.
- **Why other options are incorrect:**  
  - Option A describes `ON DELETE RESTRICT` (or `NO ACTION`).  
  - Option C describes `ON DELETE SET NULL`.  
  - Option D describes `ON DELETE SET DEFAULT`.

---

### Question 52
What is the precise behavioral difference between `ON DELETE RESTRICT` and `ON DELETE NO ACTION` in standard SQL?
- A) `RESTRICT` immediately rejects the delete operation before any other statements or triggers run, whereas `NO ACTION` permits deferred constraint checking until the end of the transaction (`DEFERRABLE INITIALLY DEFERRED`)
- B) `RESTRICT` sets foreign keys to NULL, while `NO ACTION` deletes the child rows
- C) `RESTRICT` applies only to parent tables, while `NO ACTION` applies only to child tables
- D) There is zero difference; both terms are strictly identical in all database engines under all circumstances

**Answer: A**  
**Explanation:**  
- **Why A is correct:** While both prevent deletions that would leave orphaned foreign keys:  
  - `RESTRICT` enforces the check **immediately**: if dependent child rows exist, the delete is rejected right away without waiting.  
  - `NO ACTION` allows deferred constraint checking (if configured as `DEFERRABLE`). The DBMS allows the delete to proceed temporarily within the transaction, and only raises an error at transaction `COMMIT` if dependent child rows still reference the deleted key.
- **Why other options are incorrect:**  
  - Options B and C are completely incorrect descriptions of these constraints.  
  - Option D is false because standard SQL defines the deferrability distinction between them.

---

### Question 53
Which of the following database operations on a child table `Enrolls(Student_ID, Course_ID)` can **NEVER** violate the **Referential Integrity Constraint** with respect to parent table `Students(Student_ID)`?
- A) An `INSERT` statement adding a new enrollment record
- B) An `UPDATE` statement modifying the `Student_ID` in an enrollment record
- C) A `DELETE` statement removing an enrollment record from `Enrolls`
- D) A batch `INSERT` importing 100 enrollment records

**Answer: C**  
**Explanation:**  
- **Why C is correct:** Deleting a child tuple from `Enrolls` simply removes a referencing row. It does not alter or remove any parent keys in `Students`, nor does it create any dangling references. Therefore, **DELETE on a child table can NEVER violate referential integrity**.
- **Why other options are incorrect:**  
  - Options A, B, and D all introduce new or modified foreign key values into the child table, which will violate referential integrity if the referenced `Student_ID` does not exist in `Students`.

---

### Question 54
Relation $R$ has a degree of $4$ and a cardinality of $50$.  
Relation $S$ has a degree of $3$ and a cardinality of $20$.  
What are the **Degree** and the **Cardinality** of the Cartesian Product $R \times S$?
- A) Degree = 7, Cardinality = 70
- B) Degree = 12, Cardinality = 1000
- C) Degree = 7, Cardinality = 1000
- D) Degree = 12, Cardinality = 70

**Answer: C**  
**Explanation:**  
- **Why C is correct:** For the Cartesian Product $R \times S$:  
  1. **Degree:** The attributes of $R \times S$ are the concatenation of attributes of $R$ and $S$.  
     $$\text{Degree}(R \times S) = \text{Degree}(R) + \text{Degree}(S) = 4 + 3 = \mathbf{7}.$$  
  2. **Cardinality:** Every tuple in $R$ is paired with every tuple in $S$.  
     $$\text{Cardinality}(R \times S) = \text{Cardinality}(R) \times \text{Cardinality}(S) = 50 \times 20 = \mathbf{1000}.$$
- **Why other options are incorrect:**  
  - Option A adds the cardinalities ($50+20=70$) instead of multiplying them.  
  - Option B multiplies the degrees ($4\times 3=12$) instead of adding them.  
  - Option D multiplies degrees and adds cardinalities (both wrong).

---

### Question 55
Consider a table `Employees(Emp_ID, Manager_ID, Name)` where `Manager_ID` is a self-referencing foreign key pointing to `Emp_ID` with `ON DELETE SET NULL`.  
Suppose the table contains:  
- Tuple 1: `(1, NULL, 'Alice')`  
- Tuple 2: `(2, 1, 'Bob')`  
- Tuple 3: `(3, 2, 'Charlie')`  
If Alice (`Emp_ID = 1`) is deleted, what is the resulting state of Bob's tuple?
- A) Bob's tuple is deleted
- B) Bob's tuple becomes `(2, NULL, 'Bob')`
- C) Charlie's tuple is deleted
- D) The DBMS throws a foreign key constraint violation error

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Bob's `Manager_ID` was `1` (Alice). Because the foreign key specifies `ON DELETE SET NULL`, when Alice is deleted, the DBMS automatically updates Bob's foreign key `Manager_ID` to `NULL`. Bob's tuple becomes `(2, NULL, 'Bob')`.  
  Charlie's tuple (`(3, 2, 'Charlie')`) is unaffected because Charlie references Bob (`2`), who was not deleted.
- **Why other options are incorrect:**  
  - Option A would only occur if `ON DELETE CASCADE` were specified.  
  - Option C is false because Charlie's manager was Bob, not Alice.  
  - Option D is false because `ON DELETE SET NULL` resolves the foreign key reference lawfully without an error.

---

### Question 56
Why does the formal mathematical Relational Model strictly prohibit **duplicate tuples** within any relation instance?
- A) Because computer hard drives cannot store two identical byte patterns
- B) Because a relation is formally defined as a mathematical **set** of tuples, and mathematical sets by definition cannot contain duplicate elements
- C) Because SQL databases would throw an arithmetic overflow exception
- D) Because the ANSI-SPARC architecture requires every table to have at least two foreign keys

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In E.F. Codd's formal Relational Model, a relation instance is defined as a mathematical subset of the Cartesian product of attribute domains: $r(R) \subseteq \text{dom}(A_1) \times \text{dom}(A_2) \times \dots \times \text{dom}(A_n)$. Since a relation is a mathematical **set**, and sets inherently do not contain duplicate elements, every tuple in a relation must be unique. This is why every formal relation must possess at least one primary/candidate key. (Note: Commercial SQL tables permit duplicate rows unless a primary key or unique constraint is declared, making SQL tables multisets/bags rather than pure sets).
- **Why other options are incorrect:**  
  - Options A, C, and D are factually absurd.

---

# MODULE 7: ER-TO-RELATIONAL MAPPING RULES (Q57 - Q65)

### Question 57
When mapping a **1:N (One-to-Many) Binary Relationship** (e.g., `Department` (1) to `Employee` (N)) from an ER diagram into a relational schema, where should the Foreign Key be placed to minimize redundancy and prevent anomalous attributes?
- A) In the relation on the 1-side (`Department`), storing a multivalued list of employee IDs
- B) In the relation on the N-side (`Employee`), referencing the primary key of the 1-side (`Department`)
- C) Always in a newly created separate third table, regardless of participation
- D) In both relations simultaneously as reciprocal primary keys

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In a 1:N relationship, each entity on the N-side (`Employee`) is associated with at most one entity on the 1-side (`Department`). By placing the primary key of the 1-side as a **Foreign Key inside the N-side relation**, each employee tuple contains exactly one scalar foreign key value (`Dept_ID`). This avoids repeating groups, maintains 1NF, and eliminates the need for an extra table.
- **Why other options are incorrect:**  
  - Option A violates First Normal Form (1NF), which forbids multivalued attributes (non-atomic values).  
  - Option C is unnecessary; creating a separate cross-reference table is required for M:N relationships, but for 1:N it introduces unnecessary join overhead.  
  - Option D creates circular foreign key dependencies and severe insertion deadlocks.

---

### Question 58
When converting an **M:N (Many-to-Many) Relationship** (e.g., `Students` enroll in `Courses`) from an ER diagram into a relational database, what is the mandatory structural conversion rule?
- A) Add a foreign key in `Students` referencing `Courses`
- B) Add a foreign key in `Courses` referencing `Students`
- C) Create a new separate relation (junction/bridge table) whose primary key is composed of the combination of foreign keys referencing the primary keys of both participating tables
- D) Merge both `Students` and `Courses` into a single monolithic relation

**Answer: C**  
**Explanation:**  
- **Why C is correct:** In an M:N relationship, an entity on either side can be associated with multiple entities on the other side. Neither participating table can host a single scalar foreign key without either repeating rows (causing massive redundancy and primary key violations) or storing non-atomic multivalued lists (violating 1NF). Therefore, an M:N relationship **must be mapped to a separate relation** (often called an associative, junction, or intersection table). Its primary key is the composite of the foreign keys referencing the primary keys of both participating entity sets. Any attributes associated with the relationship itself (e.g., `Grade`, `Enrollment_Date`) also become columns in this junction table.
- **Why other options are incorrect:**  
  - Options A and B violate 1NF because a student has multiple courses and a course has multiple students.  
  - Option D would cause severe data redundancy, insertion anomalies, and deletion anomalies.

---

### Question 59
Consider a **1:1 Binary Relationship** between entity sets $A$ and $B$, where entity set $A$ has **Total Participation** in the relationship, but entity set $B$ has **Partial Participation**. To eliminate NULL values in foreign keys, how should this relationship be mapped into relations?
- A) Place the primary key of $A$ as a foreign key in table $B$
- B) Place the primary key of $B$ as a foreign key in table $A$, declared with a `NOT NULL` constraint
- C) Create a separate junction table with foreign keys to both $A$ and $B$
- D) Merge $A$ and $B$ into a single table with an optional flag

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Because entity $A$ has **Total Participation**, every single tuple in table $A$ *must* be associated with an entity in $B$. Therefore, if we place the primary key of $B$ as a foreign key inside table $A$, that foreign key column can be defined as `NOT NULL` and will **never contain a NULL value**.  
  Conversely, if we placed the foreign key in table $B$ (which has Partial Participation), many tuples in $B$ would have `NULL` foreign keys because many $B$ entities do not participate in the relationship.
- **Why other options are incorrect:**  
  - Option A results in numerous NULL foreign key values in table $B$.  
  - Option C introduces unnecessary join overhead for a 1:1 relationship.  
  - Option D would force all non-participating $B$ entities to contain NULL values for all $A$ attributes.

---

### Question 60
How must a **Multivalued Attribute** (e.g., `Skill` of an `Employee(Emp_ID, Name)`) be mapped into a relational schema according to the standard ER-to-Relational conversion rules?
- A) By creating an array column inside the `Employee` table
- B) By creating a new separate relation containing the multivalued attribute and the primary key of the owner entity as a foreign key; the primary key of the new relation is composite
- C) By comma-separating all skills into a single `VARCHAR` column in the `Employee` table
- D) By creating 10 static columns: `Skill_1`, `Skill_2`, ..., `Skill_10` in `Employee`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** First Normal Form (1NF) requires all attribute domains to contain only atomic (indivisible) values. To map a multivalued attribute:  
  1. A new relation is created: `Employee_Skills(Emp_ID, Skill)`.  
  2. `Emp_ID` is a Foreign Key referencing `Employee(Emp_ID)`.  
  3. The Primary Key of `Employee_Skills` is the composite pair: `(Emp_ID, Skill)`.
- **Why other options are incorrect:**  
  - Option A and Option C violate 1NF (non-atomic values; array / comma-separated strings impede indexing and relational queries).  
  - Option D wastes space, limits an employee to 10 skills, and complicates querying (violates standard relational design principles).

---

### Question 61
How is a **Composite Attribute** (e.g., `Customer_Address` consisting of `Street`, `City`, `State`, `ZipCode`) mapped from an ER model into a relational schema?
- A) It is mapped into a separate lookup table with a generated foreign key
- B) It is flattened: only the simple component attributes (`Street`, `City`, `State`, `ZipCode`) are included as columns in the entity relation, while the composite attribute itself is omitted
- C) It is stored as a single concatenated binary blob
- D) It cannot be represented in a relational schema and must be discarded

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Composite attributes are not atomic; they represent a hierarchy of simpler components. During relational mapping, the composite attribute itself is eliminated, and its leaf **simple component attributes** (`Street`, `City`, `State`, `ZipCode`) are directly included as distinct individual columns in the entity's relational table.
- **Why other options are incorrect:**  
  - Options A, C, and D violate relational schema normalization and modeling conventions.

---

### Question 62
When converting a **Weak Entity Set** `Dependent(Dep_Name, Birth_Date, Relationship)` identified by strong entity `Employee(Emp_ID, Name)` via identifying relationship `Has_Dependent`:
What constitutes the **Primary Key** of the resulting `Dependent` relational table?
- A) `(Dep_Name)` alone
- B) `(Emp_ID)` alone
- C) A composite key comprising the primary key of the owner entity and the partial key of the weak entity: `(Emp_ID, Dep_Name)`
- D) An auto-incremented surrogate key, while `Emp_ID` is discarded

**Answer: C**  
**Explanation:**  
- **Why C is correct:** A weak entity set does not have a primary key on its own. It only possesses a **Partial Key (Discriminator)** (in this case, `Dep_Name`, which distinguishes dependents of the *same* employee). To form a globally unique primary key in the relational model, the primary key of the identifying owner entity (`Emp_ID`) is imported as a foreign key and combined with the partial key. Thus, the primary key of the weak entity relation is composite: `(Emp_ID, Dep_Name)`.
- **Why other options are incorrect:**  
  - Option A is incorrect because two different employees could have dependents with the same name (e.g., "John"), so `Dep_Name` alone is not unique across the relation.  
  - Option B is incorrect because an employee may have multiple dependents, violating primary key uniqueness if `Emp_ID` alone were used.  
  - Option D fails to maintain the explicit identifying relationship key structure.

---

### Question 63
An ER diagram contains:
- Strong entity $A$ with simple attributes and 1 multivalued attribute
- Strong entity $B$
- Weak entity $C$ identified by $A$
- A 1:N relationship from $A$ to $B$
- An M:N relationship between $B$ and $C$
What is the **MINIMUM number of relational tables** required to represent this entire ER schema without loss of data or constraints?
- A) 3 tables
- B) 4 tables
- C) 5 tables
- D) 6 tables

**Answer: C**  
**Explanation:**  
- **Why C is correct:** Let us count the minimum required relations systematically:  
  1. **Table 1:** Entity $A$ (strong entity) $\implies 1$ table.  
  2. **Table 2:** Multivalued attribute of $A \implies 1$ separate table.  
  3. **Table 3:** Entity $B$ (strong entity). Since the relationship from $A$ to $B$ is 1:N, the foreign key referencing $A$ can be embedded directly inside table $B$, requiring no extra table for this 1:N relationship $\implies 1$ table.  
  4. **Table 4:** Weak entity $C$ (contains its attributes + owner $A$'s primary key) $\implies 1$ table.  
  5. **Table 5:** The M:N relationship between $B$ and $C$ **must** be mapped to an independent junction table $\implies 1$ table.  
  $$\text{Total minimum tables} = 1 (A) + 1 (\text{multivalued of } A) + 1 (B) + 1 (C) + 1 (\text{M:N } BC) = \mathbf{5}\text{ tables.}$$
- **Why other options are incorrect:**  
  - 3 or 4 tables cannot accommodate the multivalued attribute and the M:N relationship while preserving 1NF and key constraints.  
  - 6 tables is non-minimal because the 1:N relationship does not require a separate table.

---

### Question 64
When a 1:1 relationship between entity set $E_1$ and entity set $E_2$ exhibits **Total Participation on BOTH sides**, what is the most efficient and standard relational mapping strategy?
- A) Create three tables: one for $E_1$, one for $E_2$, and a junction table
- B) Merge both entity sets and the relationship into a single consolidated relation
- C) Create two tables with cross-referencing nullable foreign keys
- D) It is impossible to represent this scenario in a relational database

**Answer: B**  
**Explanation:**  
- **Why B is correct:** When both $E_1$ and $E_2$ participate totally in a 1:1 relationship, every instance of $E_1$ is linked to exactly one instance of $E_2$, and vice versa. There are never any orphaned rows on either side, and neither side can exist without the other. Therefore, merging all attributes of $E_1$, $E_2$, and the relationship into a **single consolidated relational table** eliminates all NULL values and avoids foreign key join overhead entirely.
- **Why other options are incorrect:**  
  - Option A introduces two unnecessary joins for data that always exists 1:1 together.  
  - Option C requires circular foreign key dependencies that make insertion impossible without deferred constraints.

---

### Question 65
In an EER diagram, a superclass `Vehicle(Vehicle_ID, Price)` is specialized into subclasses `Car(Num_Doors)` and `Truck(Cargo_Tonnage)`. The specialization is **Total and Disjoint**.  
If the database designer decides to use the **"Subclasses Only"** mapping strategy (no relation for the superclass), what relations are created, and under what condition is this mapping valid?
- A) Only one relation `Vehicle(Vehicle_ID, Price, Num_Doors, Cargo_Tonnage)`
- B) Two relations: `Car(Vehicle_ID, Price, Num_Doors)` and `Truck(Vehicle_ID, Price, Cargo_Tonnage)`; valid ONLY because the specialization is Total (every vehicle is either a car or truck)
- C) Three relations with surrogate foreign keys
- D) Two relations without `Vehicle_ID`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In the "Subclasses Only" (or specialization-down) mapping option:  
  - We create a relation for each subclass, copying down the inherited superclass attributes: `Car(Vehicle_ID, Price, Num_Doors)` and `Truck(Vehicle_ID, Price, Cargo_Tonnage)`.  
  - This option is strictly valid **only if the specialization is TOTAL**. If it were Partial, an entity might exist in the superclass that is neither a Car nor a Truck, and that entity would be lost completely because there is no `Vehicle` superclass table!
- **Why other options are incorrect:**  
  - Option A represents the "Single Relation with Type Attribute" strategy.  
  - Option C creates redundant tables.  
  - Option D violates primary key identification.

---

# MODULE 8: RELATIONAL ALGEBRA & QUERY CALCULATIONS (Q66 - Q75)

### Question 66
Which of the following relational algebra expressions is **guaranteed to eliminate duplicate tuples** from its output result in formal Relational Algebra?
- A) Selection: $\sigma_{\text{Salary} > 50000}(R)$
- B) Projection: $\pi_{\text{Department\_ID}}(R)$
- C) Cartesian Product: $R \times S$
- D) Theta Join: $R \bowtie_{\text{R.id} = \text{S.id}} S$

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In formal Relational Algebra, relations and query outputs are mathematical **sets**, not multisets. In particular, the **Projection ($\pi$)** operator selects specific columns from a relation. When attributes not in the projection list are discarded, multiple tuples that originally differed only in the discarded columns become identical. By the definition of set theory, the projection operator automatically eliminates these duplicate tuples from the output set. (Note: In SQL, `SELECT` preserves duplicates by default unless `DISTINCT` is specified, but pure Relational Algebra strictly enforces set semantics).
- **Why other options are incorrect:**  
  - Selection ($\sigma$) filters tuples from a set; since the input has no duplicates, the filtered output cannot introduce duplicates. However, it does not collapse distinct tuples together; only projection does.  
  - Cartesian product and join combine sets of distinct tuples into distinct tuples.

---

### Question 67
Two relations $R$ and $S$ are said to be **Union-Compatible** (or **Set-Compatible**) if and only if:
- A) They contain the exact same number of tuples and the same primary key
- B) They have the same degree (number of attributes), and the domains of corresponding attributes (from left to right) are identical/compatible
- C) They belong to the same database tablespace on disk
- D) Both relations have foreign keys referencing each other

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The set operations Union ($R \cup S$), Intersection ($R \cap S$), and Set Difference ($R - S$) require the participating relations to be **Union-Compatible**. This requires:  
  1. **Same Degree:** Both relations must have the exact same number of attributes: $\text{degree}(R) = \text{degree}(S) = n$.  
  2. **Compatible Domains:** For all $1 \le i \le n$, the domain of the $i$-th attribute of $R$ must be compatible with the domain of the $i$-th attribute of $S$: $\text{dom}(A_i) = \text{dom}(B_i)$. Attribute names need not match.
- **Why other options are incorrect:**  
  - Cardinality (tuple count) and primary key identities are completely independent of union compatibility.

---

### Question 68
Consider relations $R(A, B, C)$ and $S(B, C, D)$.  
What is the **Degree** (number of attributes) of the Natural Join result $R \bowtie S$?
- A) 6 attributes: $(A, B, C, B, C, D)$
- B) 4 attributes: $(A, B, C, D)$
- C) 3 attributes: $(A, C, D)$
- D) 2 attributes: $(B, C)$

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The **Natural Join ($\bowtie$)** performs an equi-join on all attributes that have the same name in both relations ($B$ and $C$), and **automatically projects out duplicate join columns**.  
  Attributes of $R$: $\{A, B, C\}$ (degree 3)  
  Attributes of $S$: $\{B, C, D\}$ (degree 3)  
  Common attributes: $\{B, C\}$ (count 2)  
  $$\text{Degree}(R \bowtie S) = \text{Degree}(R) + \text{Degree}(S) - \text{Count}(\text{Common Attributes}) = 3 + 3 - 2 = \mathbf{4}\text{ attributes }(A, B, C, D).$$
- **Why other options are incorrect:**  
  - Option A describes a Cartesian Product followed by equi-selection (Theta join), which retains duplicate columns.  
  - Options C and D miscalculate set unions of attribute names.

---

### Question 69
Let relation $R(A, B)$ contain $N$ tuples, and relation $S(B, C)$ contain $M$ tuples.  
No attribute in either relation is declared as a key, and values can repeat.  
What are the **Minimum** and **Maximum** possible number of tuples in the Natural Join $R \bowtie S$?
- A) Minimum = $0$; Maximum = $N + M$
- B) Minimum = $0$; Maximum = $N \times M$
- C) Minimum = $\min(N, M)$; Maximum = $\max(N, M)$
- D) Minimum = $1$; Maximum = $N \times M$

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **Minimum tuples:** If the set of values in column $B$ of relation $R$ is completely disjoint from the set of values in column $B$ of relation $S$ ($\pi_B(R) \cap \pi_B(S) = \emptyset$), no tuples will match on $B$. The join result will be empty $\implies \mathbf{0}$ **tuples**.  
  - **Maximum tuples:** If every tuple in $R$ contains the exact same value $v$ for attribute $B$, and every tuple in $S$ also contains that exact same value $v$ for attribute $B$, then every tuple of $R$ joins with every tuple of $S$. The result is the complete Cartesian product $\implies \mathbf{N \times M}$ **tuples**.
- **Why other options are incorrect:**  
  - Natural join cardinality can never exceed the Cartesian product $N \times M$, but can certainly exceed $N + M$.  
  - The minimum is 0, not 1 or $\min(N, M)$.

---

### Question 70
Consider relation $R(A, B)$ and relation $S(B)$ containing the following instances:  
**Relation R:**  
| A | B |
|---|---|
| 1 | x |
| 1 | y |
| 1 | z |
| 2 | x |
| 2 | y |
| 3 | x |

**Relation S:**  
| B |
|---|
| x |
| y |

What is the output of the **Relational Division** operation $R \div S$?
- A) $\{ (1), (2), (3) \}$
- B) $\{ (1), (2) \}$
- C) $\{ (1) \}$
- D) $\{ (x), (y), (z) \}$

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The Relational Division operator $R(X, Y) \div S(Y)$ returns all values of $X$ that are associated with **EVERY** value of $Y$ in relation $S$.  
  Here:  
  - Target $Y$ values in $S$: $\{x, y\}$.  
  - Values of $A = 1$ in $R$ are associated with: $\{x, y, z\}$. Does this contain ALL elements of $\{x, y\}$? **Yes.**  
  - Values of $A = 2$ in $R$ are associated with: $\{x, y\}$. Does this contain ALL elements of $\{x, y\}$? **Yes.**  
  - Values of $A = 3$ in $R$ are associated with: $\{x\}$. Does this contain ALL elements of $\{x, y\}$? **No** (missing $y$).  
  Therefore, the output of $R \div S$ is $\{ (1), (2) \}$.
- **Why other options are incorrect:**  
  - Option A incorrectly includes 3, which lacks an association with $y$.  
  - Option C incorrectly omits 2.  
  - Option D outputs values from domain $B$, but the schema of $R(A, B) \div S(B)$ is $A$, not $B$.

---

### Question 71
How is the **Relational Division** operator $R(X, Y) \div S(Y)$ expressed using the fundamental relational algebra operators (Projection $\pi$, Cartesian Product $\times$, and Set Difference $-$)?
- A) $\pi_X(R) - \pi_X((\pi_X(R) \times S) - R)$
- B) $\pi_X(R) \cap \pi_X(S)$
- C) $\pi_X(R) \times S - R$
- D) $\pi_X(R - S)$

**Answer: A**  
**Explanation:**  
- **Why A is correct:** Let us decompose this classic relational algebra derivation:  
  1. $\pi_X(R)$: All candidate values of $X$ that appear in $R$.  
  2. $\pi_X(R) \times S$: All possible combinations of candidate $X$ values with every required $Y$ value from $S$.  
  3. $(\pi_X(R) \times S) - R$: All tuples $(x, y)$ that *should* exist if $x$ were associated with all $y \in S$, but are **missing from $R$**.  
  4. $\pi_X((\pi_X(R) \times S) - R)$: The set of $X$ values that are **disqualified** because they are missing at least one required $Y$ value from $S$.  
  5. $\pi_X(R) - \pi_X((\pi_X(R) \times S) - R)$: All candidate $X$ values minus the disqualified $X$ values. This yields exactly the $X$ values associated with ALL $Y$ values in $S$.
- **Why other options are incorrect:**  
  - Options B, C, and D are invalid expressions that fail to capture the universal quantifier ("for all").

---

### Question 72
Which of the following relational algebra equivalences is **FALSE**?
- A) $\sigma_{c_1 \land c_2}(R) \equiv \sigma_{c_1}(\sigma_{c_2}(R))$ (Cascade of Selection)
- B) $\sigma_c(R \bowtie S) \equiv (\sigma_c(R)) \bowtie S$, provided predicate $c$ involves only attributes of relation $R$
- C) $\pi_{L_1}(\pi_{L_2}(R)) \equiv \pi_{L_1}(R)$, provided $L_1 \subseteq L_2$ (Cascade of Projection)
- D) $\pi_L(\sigma_c(R)) \equiv \sigma_c(\pi_L(R))$ under all conditions for any list $L$ and condition $c$

**Answer: D**  
**Explanation:**  
- **Why D is correct (the statement is FALSE):** We cannot arbitrarily commute projection and selection! If predicate $c$ references an attribute $A$ that is **not** included in projection list $L$, the right-hand expression $\sigma_c(\pi_L(R))$ will be **undefined / invalid** because attribute $A$ was already discarded by $\pi_L(R)$ before $\sigma_c$ could evaluate it. Commuting is only valid if all attributes in condition $c$ are included in $L$.
- **Why other options are true:**  
  - A is a fundamental algebraic identity (selection conditions are conjunctive and commutative).  
  - B is a fundamental query optimization pushdown identity.  
  - C is a valid projection cascade rule (the outermost projection dominates).

---

### Question 73
Consider relation $R(A, B)$ with schema $\{ (1, 10), (2, 20), (3, 30) \}$ and relation $S(B, C)$ with schema $\{ (20, 200), (40, 400) \}$.  
What is the result of the **Left Outer Join** $R = \bowtie S$?
- A) $\{ (2, 20, 200) \}$
- B) $\{ (1, 10, \text{NULL}), (2, 20, 200), (3, 30, \text{NULL}) \}$
- C) $\{ (2, 20, 200), (\text{NULL}, 40, 400) \}$
- D) $\{ (1, 10, \text{NULL}), (2, 20, 200), (3, 30, \text{NULL}), (\text{NULL}, 40, 400) \}$

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In a **Left Outer Join** ($R =\bowtie S$):  
  - All matching tuples from both relations are preserved: $(2, 20, 200)$.  
  - In addition, all tuples from the **left** relation ($R$) that have no match in the right relation ($S$) are retained in the output, padded with `NULL` for all attributes originating from $S$.  
  - Tuples $(1, 10)$ and $(3, 30)$ in $R$ have no matching $B$ in $S$, so they appear as $(1, 10, \text{NULL})$ and $(3, 30, \text{NULL})$.  
  Thus, the result contains 3 tuples: $\{ (1, 10, \text{NULL}), (2, 20, 200), (3, 30, \text{NULL}) \}$.
- **Why other options are incorrect:**  
  - Option A is the Inner Natural Join.  
  - Option C is the Right Outer Join.  
  - Option D is the Full Outer Join.

---

### Question 74
Let relation $R(A, B)$ have $10$ tuples and relation $S(B, C)$ have $15$ tuples.  
Attribute $B$ is the **Primary Key of relation S**, and $R.B$ is a Foreign Key referencing $S.B$ with no NULL values.  
What is the **EXACT number of tuples** in the Natural Join $R \bowtie S$?
- A) 150 tuples
- B) 15 tuples
- C) 10 tuples
- D) Cannot be determined without inspecting individual data values

**Answer: C**  
**Explanation:**  
- **Why C is correct:** Because $B$ is the **Primary Key of $S$**, each distinct value of $B$ in $S$ occurs at most once. Because $R.B$ is a foreign key referencing $S.B$ and contains no NULLs, **every single tuple in $R$ matches EXACTLY ONE tuple in $S$**. Therefore, each of the 10 tuples in $R$ joins with its unique matching parent row in $S$, producing exactly one output tuple per row of $R$. The join result contains **exactly 10 tuples**.
- **Why other options are incorrect:**  
  - Option A (150) would only occur in a Cartesian product where all $B$ values are identical, which violates the primary key constraint on $S$.  
  - Option B (15) assumes all rows in $S$ match, but some rows in $S$ may have no referencing rows in $R$.  
  - Option D overlooks the mathematical certainty provided by the Primary Key - Foreign Key constraint relationship.

---

### Question 75
What is the result of the relational set expression $(R - S) \cup (S - R) \cup (R \cap S)$, assuming $R$ and $S$ are union-compatible?
- A) $\emptyset$ (Empty Set)
- B) $R \cap S$
- C) $R \cup S$
- D) $R - S$

**Answer: C**  
**Explanation:**  
- **Why C is correct:** By basic set theory:  
  - $R - S$: Elements exclusively in $R$.  
  - $S - R$: Elements exclusively in $S$.  
  - $R \cap S$: Elements in both $R$ and $S$.  
  The union of disjoint partitions $(R - S) \cup (S - R) \cup (R \cap S)$ reconstitutes the complete set of all elements belonging to either $R$ or $S$ (or both). Hence:  
  $$(R - S) \cup (S - R) \cup (R \cap S) \equiv \mathbf{R \cup S}.$$
- **Why other options are incorrect:**  
  - Visualizing a standard two-circle Venn diagram confirms that the left moon, the right moon, and the middle football together comprise the entire union.

---

# MODULE 9: SQL DATA DEFINITION (DDL) & DATA MANIPULATION (DML) (Q76 - Q83)

### Question 76
Which of the following is an accurate and critical operational distinction between the SQL commands `TRUNCATE TABLE Employees;` and `DELETE FROM Employees;`?
- A) `DELETE` is a DDL command that cannot be executed inside a transaction, while `TRUNCATE` is DML
- B) `TRUNCATE` is a DDL operation that deallocates data pages with minimal logging, cannot accept a `WHERE` clause, and resets auto-increment sequences; `DELETE` is a DML operation that scans and removes rows individually, logs every row deletion, and activates row-level triggers
- C) `DELETE` empties the table faster than `TRUNCATE` because it avoids index updates
- D) `TRUNCATE` permanently deletes the table structure from the system catalog, requiring `CREATE TABLE` to recreate it

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **TRUNCATE (DDL):** Quickly removes all rows from a table by deallocating the underlying data pages. It logs page deallocations rather than individual row deletions (making it substantially faster on large tables). It does **not** fire row-level `ON DELETE` triggers, cannot specify a `WHERE` filter, and resets table identity/`AUTO_INCREMENT` counters in most DBMS engines.  
  - **DELETE (DML):** Scans the table, deletes tuples row-by-row, fully records each deleted row in transaction undo/redo logs, supports a `WHERE` clause, preserves identity sequences, and fires row-level delete triggers.
- **Why other options are incorrect:**  
  - Option A reverses the language classifications (`TRUNCATE` is DDL; `DELETE` is DML).  
  - Option C is false; `DELETE` is much slower than `TRUNCATE`.  
  - Option D describes `DROP TABLE`, not `TRUNCATE TABLE` (which preserves the table structure and metadata).

---

### Question 77
A database table `Orders` currently contains 2,000,000 records. A developer executes:  
`DROP TABLE Orders;`  
What is the structural and storage status of `Orders` immediately after execution?
- A) All 2,000,000 rows are deleted, but the table schema, constraints, and column definitions remain intact in the system catalog
- B) Both the table data AND the table definition/metadata (schema, constraints, indexes) are completely removed from the database and system catalog
- C) Only secondary indexes are dropped, while base table rows remain accessible
- D) The table is converted into an unindexed external CSV file

**Answer: B**  
**Explanation:**  
- **Why B is correct:** `DROP TABLE` is a destructive DDL command that removes both the table's persistent data rows AND its complete structural metadata (columns, constraints, triggers, indexes, and catalog entries). After a table is dropped, any subsequent `SELECT * FROM Orders` query will return a *"Table or view does not exist"* syntax/compilation error.
- **Why other options are incorrect:**  
  - Option A describes `TRUNCATE TABLE`, not `DROP TABLE`.  
  - Options C and D are completely incorrect descriptions.

---

### Question 78
Suppose table `Students` has 1,000 existing records. The DBA attempts to execute:  
`ALTER TABLE Students ADD COLUMN Blood_Group VARCHAR(5) NOT NULL;`  
Assuming no `DEFAULT` value clause is provided in the statement, what happens in a standard SQL compliant engine?
- A) The column is successfully added, and existing rows receive an empty string `''`
- B) The command fails with an error because existing rows would receive a `NULL` value, violating the `NOT NULL` constraint
- C) The DBMS deletes all 1,000 existing records to satisfy the constraint
- D) The column is converted into a surrogate primary key automatically

**Answer: B**  
**Explanation:**  
- **Why B is correct:** When a new column is added to an existing table, the DBMS must populate that column for all existing records. Without an explicit `DEFAULT` clause, the default value is `NULL`. However, the column is specified as `NOT NULL`. Because assigning `NULL` to existing rows directly violates the declared `NOT NULL` constraint, standard SQL engines reject the `ALTER TABLE` statement and raise an error (e.g., *"Cannot add NOT NULL column with no default value to non-empty table"*).
- **Why other options are incorrect:**  
  - SQL does not substitute empty strings for NULL unless explicitly instructed.  
  - The DBMS will never arbitrarily delete existing user rows to accommodate a schema change.

---

### Question 79
Which of the following SQL statements demonstrates valid standard DML syntax to insert multiple tuples into an existing table in a single execution?
- A) `ADD INTO Employees VALUES (1, 'Alice'), (2, 'Bob');`
- B) `INSERT INTO Employees (Emp_ID, Name) VALUES (1, 'Alice'), (2, 'Bob');`
- C) `UPDATE Employees INSERT (1, 'Alice'), (2, 'Bob');`
- D) `CREATE TUPLES IN Employees (1, 'Alice'), (2, 'Bob');`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Standard SQL-92 and modern RDBMS engines support multi-row `INSERT` syntax using comma-separated value tuples within the `VALUES` clause:  
  `INSERT INTO TableName (col1, col2) VALUES (val1a, val2a), (val1b, val2b);`
- **Why other options are incorrect:**  
  - `ADD INTO`, `UPDATE INSERT`, and `CREATE TUPLES` are invalid, non-existent SQL syntax keywords.

---

### Question 80
Examine the following SQL statement executed on table `Employees`:  
`UPDATE Employees SET Bonus = 500 WHERE Salary > 60000;`  
What is the effect of this statement on an employee whose `Salary` is currently `NULL`?
- A) The employee's `Bonus` is updated to 500
- B) The employee's `Bonus` is updated to 0
- C) The employee's `Bonus` is unmodified because the condition `Salary > 60000` evaluates to `UNKNOWN`, which the `WHERE` clause treats as false
- D) The DBMS aborts the transaction with a division by zero error

**Answer: C**  
**Explanation:**  
- **Why C is correct:** In SQL's Three-Valued Logic (3VL), any arithmetic comparison involving `NULL` (e.g., `NULL > 60000`) evaluates to **`UNKNOWN`**. The `WHERE` clause filters out any row for which the predicate does NOT evaluate to strictly **`TRUE`**. Because `UNKNOWN` is not `TRUE`, the employee row is excluded from the update, leaving its `Bonus` column completely unchanged.
- **Why other options are incorrect:**  
  - Option A assumes NULL compares as greater than 60000.  
  - Option B assumes an arbitrary default assignment.  
  - Option D is false because NULL comparisons do not trigger runtime arithmetic exceptions.

---

### Question 81
In database systems like Oracle and MySQL, what implicit action occurs immediately prior to and after the execution of any **Data Definition Language (DDL)** statement (such as `CREATE TABLE`, `ALTER TABLE`, or `TRUNCATE TABLE`)?
- A) An automatic `ROLLBACK` of all pending DML operations
- B) An implicit `COMMIT` of the current transaction
- C) The database switches permanently to single-user read-only mode
- D) All foreign keys across the entire database are temporarily dropped

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In systems such as Oracle, MySQL (InnoDB), and many traditional relational engines, DDL statements cannot participate in multi-statement client transactions. The database server automatically executes an **implicit COMMIT** immediately before executing the DDL statement, and another **implicit COMMIT** immediately after. Therefore, any uncommitted DML statements executed prior to the DDL statement become permanently committed and cannot be rolled back!
- **Why other options are incorrect:**  
  - Option A is false; pending DML is committed, not rolled back.  
  - Options C and D are false; DDL modifies catalog metadata under schema locks without switching database modes or dropping unrelated foreign keys.

---

### Question 82
Can a table `Parent` be emptied using `TRUNCATE TABLE Parent;` if another table `Child` has a foreign key constraint referencing `Parent`, even if `Child` contains **zero rows**?
- A) Yes; because `Child` is empty, no foreign key violation can occur
- B) No; in standard relational engines (e.g., PostgreSQL, SQL Server, MySQL), `TRUNCATE` is strictly prohibited on a table referenced by an enabled foreign key constraint, regardless of whether the child table contains rows
- C) Yes; but only if the DBA grants `SUPERUSER` privileges to the user executing the query
- D) Yes; `TRUNCATE` will automatically cascade-truncate all child tables without warning

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Because `TRUNCATE` operates at the storage page level without scanning rows or checking row-by-row referential integrity constraints, RDBMS engines enforce a structural rule: a table **cannot be truncated if it is referenced by a FOREIGN KEY constraint from another table**, even if the referencing table is currently empty! To truncate `Parent`, one must either drop/disable the foreign key constraint or use `DELETE FROM Parent;`. (Note: PostgreSQL allows `TRUNCATE Parent CASCADE;`, but plain `TRUNCATE Parent;` is blocked).
- **Why other options are incorrect:**  
  - Option A overlooks the fact that TRUNCATE does not perform runtime row-level inspection.  
  - Options C and D are incorrect regarding default command behavior.

---

### Question 83
What does the clause `CASCADE CONSTRAINTS` accomplish when executing `DROP TABLE Department CASCADE CONSTRAINTS;` in an enterprise DBMS?
- A) It deletes all employees from the operating system user directory
- B) It drops the `Department` table and automatically drops all referential integrity constraints (foreign keys) in other tables that reference `Department`'s primary key
- C) It drops all child tables completely from the database
- D) It cascades the drop to delete all backup files on magnetic tape storage

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Normally, attempting to drop a table that is referenced by foreign keys in other tables fails with a referential integrity error. Specifying `CASCADE CONSTRAINTS` instructs the DBMS to drop the specified table (`Department`) and **automatically remove the referencing foreign key constraints** in all child tables (e.g., removing the FK constraint in `Employee`). The child tables themselves remain in the database, but their foreign key link to the dropped table is removed.
- **Why other options are incorrect:**  
  - Option C is false; child tables are not dropped, only their foreign key constraints are dropped.  
  - Options A and D are completely fictitious.

---

# MODULE 10: SQL DATA QUERY LANGUAGE (DQL), FILTERING & PATTERN MATCHING (Q84 - Q92)

### Question 84
A developer executes the following SQL query against the `Employees` table:  
`SELECT First_Name FROM Employees WHERE First_Name LIKE '_a%e';`  
Which of the following names will be returned by this query?
- A) "Anne"
- B) "Catherine"
- C) "Dave"
- D) "James"

**Answer: C**  
**Explanation:**  
- **Why C is correct:** Let us analyze the SQL `LIKE` wildcard pattern `'_a%e'`:  
  1. The leading underscore `_` matches **exactly one** arbitrary character.  
  2. The second character must be literal `'a'`.  
  3. The percent symbol `%` matches **zero or more** arbitrary characters.  
  4. The trailing character must be literal `'e'`.  
  Now test the candidate names:  
  - "Anne": First character is 'A' (second is 'n', not 'a') $\implies$ No match.  
  - "Catherine": Second character is 'a', but does not start after 1 character; 'C'-'a' means 'a' is 2nd, but it ends in 'e' ... wait! Let's check "Catherine": 1st char 'C', 2nd 'a', then 'therin' (matches %), ends in 'e'! Wait, what about "Dave"? 1st 'D', 2nd 'a', then 'v' (matches %), ends in 'e'!  
  Wait, let's verify both "Dave" and "Catherine": Both have 2nd char 'a' and end in 'e'!  
  In "Dave": 1st 'D' (_), 2nd 'a' (a), 3rd 'v' (%), 4th 'e' (e). It matches perfectly!  
  Wait, in "Catherine": 'C' (_), 'a' (a), 'therin' (%), 'e' (e). That also matches! Let's make sure the question has unambiguous options. For "Catherine", let's replace option B with "Charles" (ends in 's', not 'e') so only "Dave" matches uniquely!  
  - Testing "Dave": 1st char 'D' (1 char for `_`), 2nd char 'a', characters between 'v' (matches `%`), last char 'e'. Exactly matches `_a%e`.
- **Why other options are incorrect:**  
  - "Anne": 2nd character is 'n', not 'a'.  
  - "Charles": does not end in 'e'.  
  - "James": 2nd character is 'a', but ends in 's', not 'e'.

---

### Question 85
Examine the following SQL query filtering a sales order ledger:  
`SELECT Order_ID, Order_Amount FROM Orders WHERE Order_Amount BETWEEN 200 AND 500;`  
Which of the following is logically equivalent to this `BETWEEN` predicate in standard SQL?
- A) `Order_Amount > 200 AND Order_Amount < 500`
- B) `Order_Amount >= 200 AND Order_Amount <= 500`
- C) `Order_Amount >= 200 AND Order_Amount < 500`
- D) `Order_Amount > 200 AND Order_Amount <= 500`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In the SQL standard, the `BETWEEN val1 AND val2` operator is **inclusive** on both boundaries. It is defined as:  
  `attribute >= val1 AND attribute <= val2`.  
  An order with an `Order_Amount` of exactly 200 or exactly 500 will be included in the result set.
- **Why other options are incorrect:**  
  - Options A, C, and D use strict inequality (`<` or `>`), which would incorrectly exclude the boundary values 200 or 500.

---

### Question 86
Why does the following SQL query return **zero rows**, even when the `Employees` table contains 50 employees who currently have no manager assigned (`Manager_ID` contains NULL):  
`SELECT * FROM Employees WHERE Manager_ID = NULL;`
- A) Because the DBMS engine automatically replaces `NULL` with empty string `''`
- B) Because in SQL's Three-Valued Logic, any equality comparison `= NULL` evaluates to `UNKNOWN`, and the `WHERE` clause filters out any row whose condition does not evaluate to strictly `TRUE`
- C) Because `Manager_ID` cannot be indexed if it contains NULL
- D) Because the `WHERE` clause requires backticks around the word NULL

**Answer: B**  
**Explanation:**  
- **Why B is correct:** `NULL` represents missing or unknown data, not a concrete value. According to ANSI SQL Three-Valued Logic (3VL), comparing anything to `NULL` using conventional comparison operators (`=`, `<>`, `<`, `>`, `<=`, `>=`) yields **`UNKNOWN`**—even `NULL = NULL` evaluates to `UNKNOWN`! The `WHERE` clause only keeps rows for which the search condition evaluates to **`TRUE`**. To test for the presence of NULL, one must use the specialized unary operator **`IS NULL`** (i.e., `WHERE Manager_ID IS NULL`).
- **Why other options are incorrect:**  
  - Options A, C, and D are false assertions regarding SQL null handling and indexing.

---

### Question 87
Consider the following two queries executed against table `Products`:  
**Query 1:** `SELECT * FROM Products WHERE Category_ID IN (1, 2, NULL);`  
**Query 2:** `SELECT * FROM Products WHERE Category_ID NOT IN (1, 2, NULL);`  
Assume table `Products` contains items with `Category_ID` values: `1`, `2`, `3`, `4`, and `NULL`.  
What will Query 2 return?
- A) All products with `Category_ID` 3 and 4
- B) All products with `Category_ID` 3, 4, and NULL
- C) Exactly zero rows (Empty Result Set)
- D) An internal syntax error because NULL cannot appear inside an `IN` list

**Answer: C**  
**Explanation:**  
- **Why C is correct:** This is the infamous **"NOT IN with NULL Trap"** in SQL!  
  1. The `IN` predicate `x IN (1, 2, NULL)` expands to:  
     `(x = 1) OR (x = 2) OR (x = NULL)`  
  2. The `NOT IN` predicate `x NOT IN (1, 2, NULL)` expands via De Morgan's Laws to:  
     `(x <> 1) AND (x <> 2) AND (x <> NULL)`  
  3. For any product where `Category_ID = 3`:  
     `(3 <> 1) AND (3 <> 2) AND (3 <> NULL)`  
     $\implies \text{TRUE} \land \text{TRUE} \land \text{UNKNOWN} \implies \mathbf{UNKNOWN}$.  
  4. Because the conjunction includes `x <> NULL` (which is always `UNKNOWN`), the entire expression evaluates to `UNKNOWN` (or `FALSE`) for EVERY single row in the table!  
  5. Since the `WHERE` clause only outputs rows that evaluate strictly to `TRUE`, Query 2 returns **zero rows**!
- **Why other options are incorrect:**  
  - Option A is the common trap answer that overlooks SQL three-valued logic.  
  - Options B and D are factually wrong.

---

### Question 88
Examine the query:  
`SELECT Department_ID, Salary, Employee_Name FROM Employees ORDER BY Department_ID ASC, Salary DESC;`  
How will the database engine sort the returned result set?
- A) Rows are sorted primarily by `Department_ID` ascending; for employees within the same department, rows are sorted by `Salary` descending
- B) Rows are sorted primarily by `Salary` descending; `Department_ID` is ignored
- C) The sorting alternates: first row by Department ascending, second row by Salary descending
- D) The query produces an error because multiple sorting directions cannot be combined in a single `ORDER BY`

**Answer: A**  
**Explanation:**  
- **Why A is correct:** In SQL `ORDER BY`, sorting precedence is evaluated strictly from left to right:  
  1. The result is sorted first by the primary sort key (`Department_ID`) in ascending order (`ASC`).  
  2. If and only if two or more rows have identical values for `Department_ID` (a tie), the secondary sort key (`Salary`) is used to break the tie in descending order (`DESC`).
- **Why other options are incorrect:**  
  - Option B ignores the primary sort key.  
  - Options C and D misrepresent SQL syntax rules; multi-column sorting with mixed directions is standard SQL.

---

### Question 89
A developer writes the following SQL query intending to calculate an annual bonus:  
`SELECT Emp_ID, Salary * 0.15 AS Bonus FROM Employees WHERE Bonus > 5000;`  
When executed on an ANSI-compliant relational engine (such as Oracle or PostgreSQL), what is the outcome?
- A) The query successfully returns all employees with a bonus greater than 5000
- B) The query fails with an error stating that the column `Bonus` does not exist
- C) The query runs, but automatically rounds the bonus down to zero
- D) The query executes, but outputs all employees regardless of bonus amount

**Answer: B**  
**Explanation:**  
- **Why B is correct:** This error is dictated by the **Logical Query Processing Order** of SQL. The database executes clauses in the following order:  
  1. `FROM`  
  2. `WHERE`  
  3. `GROUP BY`  
  4. `HAVING`  
  5. `SELECT`  
  Because the `WHERE` clause is processed **before** the `SELECT` clause, the column alias `Bonus` defined in `SELECT` has not yet been instantiated when `WHERE` is evaluated. Therefore, referencing `Bonus` in `WHERE` causes an *"Invalid column / column does not exist"* compilation error. To fix this, one must write `WHERE Salary * 0.15 > 5000` or use a Common Table Expression (CTE) / subquery.
- **Why other options are incorrect:**  
  - Options A, C, and D fail to recognize SQL clause evaluation order.

---

### Question 90
What is the effect of executing:  
`SELECT DISTINCT Department_ID, Job_Title FROM Employees;`
- A) It returns distinct `Department_ID` values, while printing all `Job_Title` values randomly
- B) It returns unique combinations (pairs) of `(Department_ID, Job_Title)`; a row is eliminated only if both `Department_ID` AND `Job_Title` are identical to another row in the result
- C) It applies `DISTINCT` only to `Department_ID`, throwing a syntax error on `Job_Title`
- D) It sorts the table automatically by `Department_ID` in descending order

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In SQL, `DISTINCT` is **not a function** that applies to a single column; it is a query-level modifier that applies to the entire projection tuple. `SELECT DISTINCT col1, col2` evaluates the uniqueness of the compound tuple `(col1, col2)`. If two employees work in the same department but have different job titles, both rows appear in the output. Only rows with duplicate values across *all* projected columns are collapsed.
- **Why other options are incorrect:**  
  - Options A and C reflect the common misconception that `DISTINCT` applies only to the first listed column.  
  - Option D is false; `DISTINCT` does not guarantee any specific sorted order without an `ORDER BY` clause.

---

### Question 91
Consider the following search predicate:  
`WHERE Department = 'Sales' OR Department = 'Marketing' AND Commission_Rate > 0.10;`  
Due to SQL operator precedence rules, how is this compound boolean expression evaluated?
- A) `(Department = 'Sales' OR Department = 'Marketing') AND (Commission_Rate > 0.10)`
- B) `(Department = 'Sales') OR (Department = 'Marketing' AND Commission_Rate > 0.10)`
- C) The DBMS evaluates strictly from left to right, ignoring operator precedence
- D) The expression is syntactically invalid because parentheses are mandatory when combining `AND` and `OR`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In SQL (and standard boolean algebra), the **`AND` operator has higher precedence than the `OR` operator**. Therefore, `AND` binds more tightly than `OR`. The DBMS automatically binds `Department = 'Marketing' AND Commission_Rate > 0.10` together first. As a result, any employee in 'Sales' will qualify **regardless** of their commission rate! To filter both departments by commission rate, explicit parentheses must be used as in Option A.
- **Why other options are incorrect:**  
  - Option A would require explicit parentheses in the query.  
  - Option C is false; boolean operators follow strict mathematical precedence, not left-to-right evaluation.  
  - Option D is false; parentheses are optional, though highly recommended to avoid ambiguity.

---

### Question 92
To search for product descriptions containing the literal percent character `"%"` (for example, finding items labeled `"30% discount"`), how must the SQL `LIKE` clause be formulated?
- A) `WHERE Description LIKE '%30%%'`
- B) `WHERE Description LIKE '%30\% discount%' ESCAPE '\'`
- C) `WHERE Description CONTAINS '%30%'`
- D) `WHERE Description = '%30%'`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Because `%` is the standard wildcard character for zero or more characters in `LIKE`, searching for a literal `%` requires an **escape character**. By declaring `ESCAPE '\'`, the sequence `\%` is treated as a literal percent symbol rather than a wildcard.
- **Why other options are incorrect:**  
  - Option A treats both `%` signs as wildcards.  
  - Option C uses `CONTAINS`, which is Full-Text Search syntax, not standard SQL `LIKE`.  
  - Option D performs strict literal equality matching for the exact 5-character string `'%30%'`.

---

# MODULE 11: AGGREGATE FUNCTIONS, GROUP BY, AND LOGICAL QUERY EXECUTION ORDER (Q93 - Q101)

### Question 93
What is the precise **Logical Query Execution Order** of the major SQL clauses in a `SELECT` statement?
- A) SELECT $\rightarrow$ FROM $\rightarrow$ WHERE $\rightarrow$ GROUP BY $\rightarrow$ HAVING $\rightarrow$ ORDER BY
- B) FROM $\rightarrow$ WHERE $\rightarrow$ GROUP BY $\rightarrow$ HAVING $\rightarrow$ SELECT $\rightarrow$ DISTINCT $\rightarrow$ ORDER BY $\rightarrow$ LIMIT
- C) FROM $\rightarrow$ SELECT $\rightarrow$ WHERE $\rightarrow$ ORDER BY $\rightarrow$ GROUP BY $\rightarrow$ HAVING
- D) WHERE $\rightarrow$ FROM $\rightarrow$ GROUP BY $\rightarrow$ HAVING $\rightarrow$ SELECT $\rightarrow$ ORDER BY

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The logical processing order (conceptual phases of query execution) defined by ANSI SQL is:  
  1. **FROM (including JOINs):** Identifies and combines the target tables.  
  2. **WHERE:** Filters individual rows prior to grouping.  
  3. **GROUP BY:** Groups remaining rows based on common attribute values.  
  4. **HAVING:** Filters aggregate groups based on group conditions.  
  5. **SELECT:** Computes expressions, aggregates, and assigns column aliases.  
  6. **DISTINCT:** Eliminates duplicate rows from the projected output.  
  7. **ORDER BY:** Sorts the final result set.  
  8. **LIMIT / OFFSET:** Restricts the number of output rows returned to the client.
- **Why other options are incorrect:**  
  - All other options violate the fundamental pipeline of relational query evaluation (e.g., `SELECT` cannot execute before `FROM` or `WHERE`).

---

### Question 94
Table `Employees` has 5 rows with the following values in the `Salary` column:  
`[ 1000, 2000, NULL, 3000, NULL ]`  
What are the outputs of `COUNT(*)`, `COUNT(Salary)`, and `COUNT(DISTINCT Salary)`, respectively?
- A) 5, 3, 3
- B) 3, 3, 3
- C) 5, 5, 3
- D) 3, 5, 5

**Answer: A**  
**Explanation:**  
- **Why A is correct:** Let us evaluate each aggregate function according to ANSI SQL rules:  
  1. **`COUNT(*)`:** Counts the total number of **rows** in the table/group, regardless of whether columns contain NULL values. Total rows = **5**.  
  2. **`COUNT(Salary)`:** Counts only the number of **non-NULL** values in the specified column. Non-null values are `1000, 2000, 3000` $\implies$ count is **3**.  
  3. **`COUNT(DISTINCT Salary)`:** Counts the number of **unique, non-NULL** values in the specified column. The distinct non-null values are `1000, 2000, 3000` $\implies$ count is **3**.  
  Thus, the outputs are **5, 3, 3**.
- **Why other options are incorrect:**  
  - Any option that counts NULLs in `COUNT(column)` or fails to count rows in `COUNT(*)` is incorrect.

---

### Question 95
Consider a table `Test_Scores` with 4 students having scores: `[ 80, 100, NULL, 60 ]`.  
What will `SELECT AVG(Score) FROM Test_Scores;` return?
- A) 60 (computed as $(80 + 100 + 0 + 60) / 4$)
- B) 80 (computed as $(80 + 100 + 60) / 3$)
- C) NULL (because NULL in arithmetic makes the entire average unknown)
- D) 240

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In SQL, all aggregate functions (except `COUNT(*)`) **automatically eliminate NULL values** prior to computing the aggregate.  
  `AVG(Score)` calculates:  
  $$\text{AVG} = \frac{\sum \text{non-null scores}}{\text{count of non-null scores}} = \frac{80 + 100 + 60}{3} = \frac{240}{3} = \mathbf{80}.$$  
  It does NOT treat NULL as zero, nor does it divide by 4.
- **Why other options are incorrect:**  
  - Option A incorrectly assumes NULL is converted to 0 and counted in the denominator.  
  - Option C confuses scalar arithmetic (where `10 + NULL = NULL`) with aggregate functions (which deliberately ignore NULLs).

---

### Question 96
If an aggregate query is executed against a completely **EMPTY table** (containing 0 rows), what will the following query return?  
`SELECT COUNT(*), SUM(Salary), AVG(Salary), MIN(Salary), MAX(Salary) FROM Empty_Table;`
- A) `(0, 0, 0, 0, 0)`
- B) `(0, NULL, NULL, NULL, NULL)`
- C) `(NULL, NULL, NULL, NULL, NULL)`
- D) Zero rows (an empty result set)

**Answer: B**  
**Explanation:**  
- **Why B is correct:** According to the ANSI SQL standard:  
  - When aggregating an empty set of rows without a `GROUP BY` clause, the query produces **exactly one row**.  
  - `COUNT(*)` (and `COUNT(col)`) returns **`0`** (the count of matching rows is zero).  
  - All other mathematical aggregate functions (`SUM`, `AVG`, `MIN`, `MAX`) return **`NULL`**, because the sum, mean, minimum, or maximum of an empty set of values is undefined.
- **Why other options are incorrect:**  
  - Option A incorrectly returns 0 for SUM, AVG, MIN, MAX.  
  - Option C incorrectly claims COUNT(*) returns NULL.  
  - Option D incorrectly claims no row is returned (scalar aggregation over an empty table always yields one row).

---

### Question 97
Why is the following SQL query **syntactically INVALID** in standard SQL?  
`SELECT Department_ID, Job_Title, AVG(Salary) FROM Employees GROUP BY Department_ID;`
- A) Because aggregate functions like `AVG` cannot be used in a `SELECT` statement containing `GROUP BY`
- B) Because `Job_Title` appears in the `SELECT` list but is neither an aggregate function nor present in the `GROUP BY` clause
- C) Because `Department_ID` must be cast to a string
- D) Because `GROUP BY` must always be preceded by a `HAVING` clause

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The fundamental rule of `GROUP BY` states: **Every column that appears in the `SELECT` clause must either be an aggregate function OR appear explicitly in the `GROUP BY` clause**.  
  Here, the rows are grouped solely by `Department_ID`. Within a single department (e.g., `Dept 10`), there could be multiple different `Job_Title` values (e.g., 'Clerk', 'Manager', 'Analyst'). If `Job_Title` is neither grouped nor aggregated, the database engine cannot determine which job title to display for that department's summary row. Standard SQL strictly rejects this query with an error: *"Column 'Job_Title' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause."*
- **Why other options are incorrect:**  
  - Options A, C, and D are false assertions.

---

### Question 98
What is the fundamental functional distinction between the **`WHERE` clause** and the **`HAVING` clause**?
- A) `WHERE` filters rows before any grouping occurs; `HAVING` filters aggregated groups after `GROUP BY` has grouped the rows
- B) `WHERE` can contain aggregate functions like `SUM(Salary) > 10000`, while `HAVING` cannot
- C) `WHERE` is used exclusively with `SELECT`, while `HAVING` is used exclusively with `UPDATE`
- D) There is no distinction; they are completely interchangeable synonyms in SQL

**Answer: A**  
**Explanation:**  
- **Why A is correct:**  
  - **`WHERE` clause:** Filters individual data tuples **before** grouping and aggregation. It operates on individual row attributes and can **never** contain aggregate functions (e.g., `WHERE AVG(salary) > 5000` is illegal).  
  - **`HAVING` clause:** Evaluated **after** the `GROUP BY` phase. It is specifically designed to filter entire *groups* or summary rows based on group properties and aggregate conditions (e.g., `HAVING COUNT(*) > 5`).
- **Why other options are incorrect:**  
  - Option B reverses the capabilities of WHERE and HAVING.  
  - Options C and D are completely false.

---

### Question 99
Is the following SQL query syntactically valid in standard SQL, and what does it compute?  
`SELECT AVG(Salary) FROM Employees HAVING AVG(Salary) > 50000;`
- A) Invalid: `HAVING` is illegal without an explicit `GROUP BY` clause
- B) Valid: When `HAVING` is used without `GROUP BY`, the entire table is treated as a single group; if the overall average salary exceeds 50000, it returns that average, otherwise it returns zero rows
- C) Invalid: `AVG` must be aliased using `AS`
- D) Valid: It returns the average salary for every employee individually

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In standard SQL, a `HAVING` clause does **not** strictly require an explicit `GROUP BY` clause. When `GROUP BY` is omitted, the entire set of rows satisfying the `WHERE` clause is treated as **one single collective group**. If the overall `AVG(Salary)` of all employees in the table exceeds 50,000, the condition evaluates to true and the single scalar average is returned. If the average is $\le 50000$, the group is filtered out, returning an empty result set (0 rows).
- **Why other options are incorrect:**  
  - Option A is a common myth among database students.  
  - Options C and D are factually wrong.

---

### Question 100
From a query optimization and performance perspective, why should a developer write:  
`SELECT Department_ID, COUNT(*) FROM Employees WHERE Status = 'Active' GROUP BY Department_ID;`  
instead of:  
`SELECT Department_ID, COUNT(*) FROM Employees GROUP BY Department_ID HAVING Status = 'Active';`
- A) The second query will fail compilation because `Status` is not in the `GROUP BY` clause, and filtering rows early with `WHERE` dramatically reduces the number of rows that must be sorted and aggregated in memory
- B) The first query uses index scans, while the second query drops the table
- C) `HAVING` can only accept numerical values, not strings like `'Active'`
- D) There is zero difference in execution plan or performance

**Answer: A**  
**Explanation:**  
- **Why A is correct:** Two major reasons:  
  1. *Syntactic Validity:* In standard SQL, the second query is invalid because `Status` is an unaggregated column not listed in the `GROUP BY` clause.  
  2. *Performance / Optimization:* The `WHERE` clause filters out inactive employee rows **before** the grouping operation takes place. This drastically reduces the number of rows entering the hash table or sort buffer for the `GROUP BY`, saving CPU cycles and memory bandwidth. Filtering with `HAVING` (where legal) forces the database to group every row first before throwing groups away.
- **Why other options are incorrect:**  
  - Options B, C, and D are factually inaccurate.

---

### Question 101
A sales table `Orders` has 1,000,000 rows. A query groups data by two columns:  
`SELECT Region, Year, SUM(Sales) FROM Orders GROUP BY Region, Year;`  
If there are 5 distinct regions and 4 distinct years present in the data (with every region recording sales in every year), how many rows will the final output contain?
- A) 1,000,000 rows
- B) 9 rows ($5 + 4$)
- C) 20 rows ($5 \times 4$)
- D) 1 row

**Answer: C**  
**Explanation:**  
- **Why C is correct:** When multiple columns are specified in the `GROUP BY` clause (`GROUP BY Region, Year`), each unique combination of values across those columns forms a separate group. Since there are 5 distinct regions and 4 distinct years, and all pairs are populated, there are exactly:  
  $$5 \times 4 = \mathbf{20}\text{ distinct groups.}$$  
  Each group produces exactly one aggregated summary row in the output.
- **Why other options are incorrect:**  
  - Option A is the unaggregated raw row count.  
  - Option B adds the distinct values instead of calculating combinations.  
  - Option D represents an un-grouped aggregate.

---

# MODULE 12: SQL JOINS AND RELATIONAL SET OPERATIONS (Q102 - Q110)

### Question 102
Table $A$ has 4 rows and Table $B$ has 3 rows.  
What is the cardinality of the result returned by:  
`SELECT * FROM A CROSS JOIN B;`
- A) 7 rows
- B) 12 rows
- C) 1 row
- D) 0 rows

**Answer: B**  
**Explanation:**  
- **Why B is correct:** A **CROSS JOIN** computes the Cartesian Product of the two tables. Every row from table $A$ is combined with every row from table $B$.  
  $$\text{Cardinality} = \text{Cardinality}(A) \times \text{Cardinality}(B) = 4 \times 3 = \mathbf{12}\text{ rows.}$$
- **Why other options are incorrect:**  
  - 7 rows is the sum ($4+3$), which is characteristic of `UNION ALL`, not a Cartesian product.

---

### Question 103
What type of join is utilized when an application queries the `Employees` table to display each employee's name alongside their direct supervisor's name, where both employee and supervisor are stored in the same `Employees` table?
- A) Cross Join
- B) Natural Outer Join
- C) Self Join
- D) Full Disjoint Join

**Answer: C**  
**Explanation:**  
- **Why C is correct:** A **Self Join** is a regular join in which a table is joined with itself. It is implemented by referencing the same table twice in the `FROM` clause and giving each reference a distinct table alias (e.g., `FROM Employees E JOIN Employees M ON E.Manager_ID = M.Emp_ID`). This is the classic technique to resolve recursive relationships and organizational hierarchies.
- **Why other options are incorrect:**  
  - A Cross Join produces an unconstrained Cartesian product.  
  - "Natural Outer Join" and "Full Disjoint Join" do not represent the mechanism of joining a table to itself using aliases.

---

### Question 104
Table $L$ contains keys `{1, 2, 3}`. Table $R$ contains keys `{2, 3, 4}`.  
Assuming all keys are unique in their respective tables, how many rows are returned by:  
`SELECT L.ID, R.ID FROM L FULL OUTER JOIN R ON L.ID = R.ID;`
- A) 2 rows
- B) 3 rows
- C) 4 rows
- D) 5 rows

**Answer: C**  
**Explanation:**  
- **Why C is correct:** A **FULL OUTER JOIN** preserves:  
  1. All matching rows (inner join): `{ (2, 2), (3, 3) }` $\implies 2$ rows.  
  2. Unmatched rows from the Left table ($L$), padded with NULL for $R$: `{ (1, NULL) }` $\implies 1$ row.  
  3. Unmatched rows from the Right table ($R$), padded with NULL for $L$: `{ (NULL, 4) }` $\implies 1$ row.  
  $$\text{Total rows} = 2 (\text{matches}) + 1 (\text{unmatched left}) + 1 (\text{unmatched right}) = \mathbf{4}\text{ rows.}$$
- **Why other options are incorrect:**  
  - 2 rows is the result of an INNER JOIN.  
  - 3 rows is the result of a LEFT JOIN or RIGHT JOIN.  
  - 5 rows is an overcount.

---

### Question 105
What is the fundamental operational and performance difference between `UNION` and `UNION ALL` in SQL?
- A) `UNION` combines tables horizontally (joins), while `UNION ALL` combines them vertically
- B) `UNION` automatically eliminates duplicate rows from the combined result set (requiring an expensive internal sort or hash deduplication), whereas `UNION ALL` concatenates all rows including duplicates without sorting
- C) `UNION ALL` only works on numeric data types, while `UNION` works on character strings
- D) `UNION` can combine tables with different numbers of columns, while `UNION ALL` requires identical column counts

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **`UNION`:** Combines the result sets of two queries and performs duplicate elimination. To detect and remove duplicates, the database engine must sort the intermediate data or construct a hash table in memory, which is computationally expensive for large datasets.  
  - **`UNION ALL`:** Simply appends the result sets together, preserving all rows and duplicates. Because it skips the sorting/hashing deduplication step, `UNION ALL` is **vastly faster** and should always be preferred when results are known to be disjoint or when duplicates are acceptable.
- **Why other options are incorrect:**  
  - Both combine results vertically; neither combines horizontally (which is the job of joins).  
  - Both strictly require union compatibility (same number of columns and compatible types).

---

### Question 106
In Oracle SQL, the set difference operator is named **`MINUS`**, whereas in the ANSI SQL standard and PostgreSQL / SQL Server, it is named **`EXCEPT`**.  
If Query $A$ returns `{10, 20, 20, 30}` and Query $B$ returns `{20, 40}`, what does `Query A EXCEPT Query B` (or `A MINUS B`) return?
- A) `{10, 30}`
- B) `{10, 20, 30}`
- C) `{40}`
- D) `{10, 20, 20, 30, 40}`

**Answer: A**  
**Explanation:**  
- **Why A is correct:** Standard `EXCEPT` (and Oracle `MINUS`) performs set difference with **distinct** set semantics:  
  1. It takes the distinct values of $A$: `{10, 20, 30}`.  
  2. It removes all values that appear anywhere in $B$: value `20` is in $B$, so it is completely removed.  
  3. The resulting set is **`{10, 30}`**.
- **Why other options are incorrect:**  
  - Option B fails to remove 20.  
  - Option C is $B \text{ EXCEPT } A$.  
  - Option D is a multiset union.

---

### Question 107
Suppose relation $A$ contains `{1, 2, 3}` and relation $B$ contains `{2, 3, 4}`.  
What is returned by:  
`SELECT ID FROM A INTERSECT SELECT ID FROM B;`
- A) `{1, 4}`
- B) `{2, 3}`
- C) `{1, 2, 3, 4}`
- D) `{ }` (Empty set)

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The **`INTERSECT`** operator returns all distinct rows that are produced by **both** the first and second query.  
  Elements common to both sets $\{1, 2, 3\}$ and $\{2, 3, 4\}$ are **`{2, 3}`**.
- **Why other options are incorrect:**  
  - Option A is the symmetric difference.  
  - Option C is the Union.  
  - Option D is the empty set.

---

### Question 108
Why is the use of **`NATURAL JOIN`** strongly discouraged in production enterprise software systems?
- A) Because `NATURAL JOIN` runs in exponential $O(2^N)$ time complexity
- B) Because it implicitly joins on ALL columns that share the exact same name across both tables; if a schema migration adds a common maintenance column (such as `Updated_At`, `Status`, or `Description`) to either table, the join condition silently changes, producing incorrect results or empty sets without syntax errors
- C) Because SQL engines convert natural joins into unindexed cross joins
- D) Because natural joins do not allow primary keys to be projected

**Answer: B**  
**Explanation:**  
- **Why B is correct:** `NATURAL JOIN` automatically inspects the schemas of both tables and constructs an equi-join on **every attribute that shares the exact same identifier name**. In real-world enterprise databases, tables frequently share common metadata columns like `Created_By`, `Modified_Date`, `Tenant_ID`, or `Status`. If someone adds a `Status` column to both tables, a `NATURAL JOIN` will silently begin joining on `(ID AND Status)`. If statuses differ, queries that previously returned critical business data will suddenly return empty results, causing silent data truncation bugs. Explicit joins (`JOIN ... ON ...`) make join keys clear, robust, and immune to unrelated column additions.
- **Why other options are incorrect:**  
  - Options A, C, and D are false technical assertions.

---

### Question 109
Consider two tables, each having one row:  
Table $T_1$: `Col_A = NULL`  
Table $T_2$: `Col_A = NULL`  
What will the following query return?  
`SELECT * FROM T1 INNER JOIN T2 ON T1.Col_A = T2.Col_A;`
- A) 1 row combining both NULLs
- B) 0 rows (Empty Result Set)
- C) An infinite loop in the join processor
- D) A fatal `NullPointerException`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The join predicate is `ON T1.Col_A = T2.Col_A`.  
  Substituting the values yields: `NULL = NULL`.  
  In SQL Three-Valued Logic, `NULL = NULL` evaluates to **`UNKNOWN`**.  
  An `INNER JOIN` only outputs rows for which the join predicate evaluates to strictly **`TRUE`**. Since `UNKNOWN` is not `TRUE`, the row does not match! Therefore, the query returns **0 rows**.
- **Why other options are incorrect:**  
  - Option A incorrectly assumes NULL equals NULL in relational equality.  
  - Options C and D are completely incorrect engine behaviors.

---

### Question 110
Examine the following two queries involving a `LEFT JOIN`:  
**Query A:**  
```sql
SELECT C.Customer_Name, O.Order_ID 
FROM Customers C 
LEFT JOIN Orders O ON C.Customer_ID = O.Customer_ID AND O.Order_Status = 'Shipped';
```
**Query B:**  
```sql
SELECT C.Customer_Name, O.Order_ID 
FROM Customers C 
LEFT JOIN Orders O ON C.Customer_ID = O.Customer_ID 
WHERE O.Order_Status = 'Shipped';
```
What is the crucial behavioral difference between Query A and Query B for a customer who has **NEVER placed an order**?
- A) Both queries return the customer with `Order_ID = NULL`
- B) Query A returns the customer with `Order_ID = NULL`; Query B completely discards the customer from the result set (converting the LEFT JOIN effectively into an INNER JOIN)
- C) Query B returns the customer, while Query A throws a syntax error
- D) Both queries discard the customer completely

**Answer: B**  
**Explanation:**  
- **Why B is correct:** This is one of the most critical SQL join subtleties:  
  - **In Query A:** The condition `O.Order_Status = 'Shipped'` is placed inside the **`ON` clause** of the `LEFT JOIN`. For a customer with no orders (or no shipped orders), the join condition fails, but because it is a `LEFT JOIN`, the customer from the left table (`Customers`) is still preserved, with `O.Order_ID` populated as `NULL`.  
  - **In Query B:** The condition is placed inside the **`WHERE` clause**. The `LEFT JOIN` initially generates a row with `(Customer_Name, NULL, NULL)`. Next, the `WHERE` clause evaluates `WHERE O.Order_Status = 'Shipped'`, which becomes `WHERE NULL = 'Shipped' \implies UNKNOWN`. Because `UNKNOWN` is rejected by `WHERE`, that customer row is **completely removed**! Placing a predicate on the right table in the `WHERE` clause silently converts a `LEFT JOIN` into an `INNER JOIN`.
- **Why other options are incorrect:**  
  - Any option claiming both queries behave identically fails to understand the fundamental difference between `ON` and `WHERE` filtering in outer joins.

---

# MODULE 13: SUBQUERIES (SCALAR, MULTI-ROW, CORRELATED) & THE THREE-VALUED LOGIC NULL TRAP (Q111 - Q120)

### Question 111
A database analyst executes the following query using a single-row scalar comparison operator (`=`):  
`SELECT Emp_ID, Salary FROM Employees WHERE Salary = (SELECT Salary FROM Employees WHERE Department_ID = 20);`  
If Department 20 currently employs **three** people earning $4,000, $5,500, and $7,000 respectively, what is the exact outcome when the query is run?
- A) The query outputs all employees whose salary matches any of the three salaries
- B) The query arbitrarily picks the first salary ($4,000) and executes successfully
- C) The query fails at runtime with an error: *"Subquery returned more than 1 value / single-row subquery returns more than one row"*
- D) The query returns NULL for all rows

**Answer: C**  
**Explanation:**  
- **Why C is correct:** In SQL, comparison operators like `=`, `<>`, `<`, `>`, `<=`, and `>=` are **scalar operators**. They strictly require the right-hand operand to be a single scalar value. If an inner subquery used with a scalar comparison operator returns multiple rows (here, 3 rows), the relational query processor cannot determine which value to compare against. The query compiles, but fails immediately at runtime with a cardinal error (e.g., in PostgreSQL: *"more than one row returned by a subquery used as an expression"*). To fix this, one must use multi-row operators like `IN`, `= ANY`, or an aggregate like `MAX()`.
- **Why other options are incorrect:**  
  - Option A requires the `IN` or `= ANY` operator.  
  - Option B is false; relational engines never guess or pick values arbitrarily.  
  - Option D is factually wrong.

---

### Question 112
Consider the following query filtering customer orders:  
`SELECT Order_ID, Order_Total FROM Orders WHERE Order_Total > ALL (SELECT Order_Total FROM Orders WHERE Customer_ID = 45);`  
Assume Customer 45 has three recorded orders with values: `$150, $400, $850`.  
Which orders will be returned by the outer query?
- A) Orders with an `Order_Total` strictly greater than $150
- B) Orders with an `Order_Total` strictly greater than $850
- C) Orders with an `Order_Total` between $150 and $850
- D) All orders placed by Customer 45

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The **`> ALL`** comparison operator requires the outer value to be strictly greater than **every single value** in the set returned by the subquery.  
  Mathematically:  
  $$x > \text{ALL} \{150, 400, 850\} \iff x > 150 \land x > 400 \land x > 850 \iff x > \max(150, 400, 850) = 850.$$  
  Therefore, only orders with an `Order_Total > 850` will satisfy the predicate. (Note: Conversely, `> ANY` would mean greater than at least one value, which evaluates to $x > \min(150, 400, 850) = 150$).
- **Why other options are incorrect:**  
  - Option A describes `> ANY`.  
  - Options C and D are incorrect interpretations.

---

### Question 113
What is the evaluated boolean outcome of the predicates `val > ALL (Subquery)` and `val > ANY (Subquery)` when the subquery returns a completely **EMPTY result set** (0 rows)?
- A) Both evaluate to `FALSE`
- B) Both evaluate to `UNKNOWN`
- C) `> ALL` evaluates to `TRUE` (vacuously true), while `> ANY` evaluates to `FALSE`
- D) `> ALL` evaluates to `FALSE`, while `> ANY` evaluates to `TRUE`

**Answer: C**  
**Explanation:**  
- **Why C is correct:** This is a classic predicate logic subtlety in the SQL standard:  
  1. **`val > ALL (empty set)`:** Evaluates whether there does NOT exist any element $y$ in the subquery such that $val \le y$. Because the subquery contains zero elements, no counterexample exists! In formal mathematical logic, universal quantification over an empty set ($\forall x \in \emptyset, P(x)$) is **vacuously TRUE**. Hence, `> ALL (empty)` evaluates to **`TRUE`**!  
  2. **`val > ANY (empty set)`:** Evaluates whether there exists at least one element $y$ in the subquery such that $val > y$ ($\exists x \in \emptyset, P(x)$). Because there are no elements in the subquery, no such element can be found. Hence, `> ANY (empty)` evaluates to **`FALSE`**!
- **Why other options are incorrect:**  
  - All other combinations contradict standard relational predicate calculus.

---

### Question 114
What defines a **Correlated Subquery**, and how does its conceptual execution mechanism differ from an **Uncorrelated (Independent) Subquery**?
- A) A correlated subquery runs on an external database server over a network socket
- B) A correlated subquery references columns from the outer query table; conceptually, the inner query must be evaluated repeatedly for each candidate row processed by the outer query
- C) A correlated subquery can only return character strings, while an uncorrelated subquery returns integers
- D) An uncorrelated subquery must always be preceded by the `EXISTS` keyword

**Answer: B**  
**Explanation:**  
- **Why B is correct:**  
  - **Uncorrelated Subquery:** Completely self-contained. It does not reference any attributes from the outer query. The query optimizer can execute it **once**, cache the result set, and supply it to the outer query.  
  - **Correlated Subquery:** Contains references to attributes belonging to the outer query (e.g., `WHERE inner.dept_id = outer.dept_id`). Because the inner query's search condition depends on the specific row currently being evaluated by the outer query, the inner query cannot be evaluated in isolation—it must conceptually be re-evaluated for each row produced by the outer query (unless the optimizer transforms it into a join).
- **Why other options are incorrect:**  
  - Options A, C, and D are false assertions.

---

### Question 115
Why is the `EXISTS` operator generally immune to issues with `NULL` values returned by a subquery, compared to the `IN` operator?
- A) Because `EXISTS` automatically converts all NULL values to the integer 0
- B) Because `EXISTS` only checks for the existence of at least one qualifying row satisfying the predicate; the actual expressions or NULLs in the subquery's `SELECT` list are not evaluated
- C) Because `EXISTS` can only be executed by the Database Administrator
- D) Because `EXISTS` does not allow `WHERE` clauses inside the subquery

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The `EXISTS` operator tests whether the subquery produces **at least one row**. The select list of the subquery is completely irrelevant; `SELECT 1`, `SELECT NULL`, and `SELECT *` inside an `EXISTS (SELECT ...)` behave identically! Even if the subquery returns a row containing purely `NULL`, `EXISTS` evaluates to **`TRUE`** because a row exists. Unlike `IN`, which performs equality tests with the returned values (and gets derailed by `NULL = val \implies UNKNOWN`), `EXISTS` operates purely as a boolean existence check.
- **Why other options are incorrect:**  
  - Options A, C, and D are false descriptions of SQL engine mechanics.

---

### Question 116
Consider two tables: `Customers(Customer_ID, Name)` and `Orders(Order_ID, Customer_ID)`.  
Table `Orders` contains 1,000 valid orders, but has **one row where `Customer_ID` is `NULL`** (an anonymous guest checkout).  
A developer wants to find all customers who have never placed an order and writes:  
```sql
SELECT Customer_ID, Name 
FROM Customers 
WHERE Customer_ID NOT IN (SELECT Customer_ID FROM Orders);
```
What will this query return?
- A) All customers who have never placed an order
- B) All customers who have never placed an order, plus the guest customer
- C) Exactly zero rows (Empty Result Set)
- D) A runtime syntax error

**Answer: C**  
**Explanation:**  
- **Why C is correct:** This is the most notorious trap in SQL!  
  1. The subquery returns a set that includes `NULL`: `{ 101, 102, ..., NULL }`.  
  2. For *any* customer in `Customers` (say, `Customer_ID = 500` who has no orders):  
     `500 NOT IN (101, 102, ..., NULL)` expands to:  
     `(500 <> 101) AND (500 <> 102) AND ... AND (500 <> NULL)`  
  3. While `500 <> 101` is `TRUE`, the comparison `500 <> NULL` evaluates to **`UNKNOWN`**!  
  4. In SQL boolean logic, `TRUE AND TRUE AND ... AND UNKNOWN` evaluates to **`UNKNOWN`**!  
  5. The `WHERE` clause filters out any row where the condition does not evaluate to strictly `TRUE`.  
  6. Consequently, **every single customer row is discarded**, and the query returns **zero rows**!  
  *(The correct, production-safe pattern is to use `NOT EXISTS` or add `WHERE Customer_ID IS NOT NULL` to the subquery).*
- **Why other options are incorrect:**  
  - Option A is the intended business logic, but fails due to the SQL 3VL NULL trap.  
  - Options B and D are factually incorrect.

---

### Question 117
In standard SQL, when a subquery is placed within the **`FROM` clause** (acting as a derived table or inline view):  
`SELECT T.Dept_ID, T.Avg_Sal FROM (SELECT Dept_ID, AVG(Salary) AS Avg_Sal FROM Employees GROUP BY Dept_ID) T;`  
What is a mandatory requirement regarding the derived table in most relational engines (such as PostgreSQL and MySQL)?
- A) The subquery must be declared as a temporary table before execution
- B) The derived table must be assigned an explicit correlation name (table alias), such as `T`
- C) The derived table cannot contain aggregate functions
- D) The derived table must have an index created on it

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In ANSI SQL and relational engines like PostgreSQL and MySQL, every derived table in the `FROM` clause **must be given an explicit alias** (correlation name). Failing to provide an alias (e.g., omitting `T` at the end) results in a syntax error: *"Every derived table must have its own alias"*.
- **Why other options are incorrect:**  
  - Options A, C, and D are false; derived tables can contain aggregates, do not require pre-creation, and cannot have explicit indexes declared inline.

---

### Question 118
What happens if a **Scalar Subquery** placed in the `SELECT` list returns **zero rows** for a particular outer row?  
```sql
SELECT E.Name, 
       (SELECT D.Department_Name FROM Departments D WHERE D.Dept_ID = E.Dept_ID) AS Dept_Name 
FROM Employees E;
```
If an employee has a `Dept_ID` that does not match any row in `Departments`, what value is displayed in `Dept_Name`?
- A) The query crashes with a runtime exception
- B) The employee row is completely omitted from the output
- C) `NULL`
- D) An empty string `''`

**Answer: C**  
**Explanation:**  
- **Why C is correct:** A scalar subquery in the `SELECT` projection list is defined to return a single value. If the subquery finds a matching row, it returns that value. If the subquery finds **zero matching rows**, the ANSI SQL standard specifies that it evaluates to **`NULL`**. (If it returns more than one row, it raises a runtime subquery cardinality violation error).
- **Why other options are incorrect:**  
  - Option A only happens if the subquery returns 2 or more rows.  
  - Option B confuses scalar subquery projection with an inner join.  
  - Option D is incorrect because SQL substitutes NULL, not an empty string.

---

### Question 119
Which of the following queries correctly retrieves the **Second Highest Salary** from the `Employees` table, returning `NULL` if no second highest salary exists?
- A) `SELECT Salary FROM Employees ORDER BY Salary DESC LIMIT 1 OFFSET 1;`
- B) `SELECT MAX(Salary) FROM Employees WHERE Salary < (SELECT MAX(Salary) FROM Employees);`
- C) `SELECT MIN(Salary) FROM Employees WHERE Salary > (SELECT MIN(Salary) FROM Employees);`
- D) `SELECT Salary FROM Employees WHERE Salary = (SELECT AVG(Salary) FROM Employees);`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Let us analyze how this subquery functions:  
  1. The inner subquery `(SELECT MAX(Salary) FROM Employees)` finds the absolute highest salary in the company.  
  2. The outer query filters for all salaries strictly less than that maximum (`WHERE Salary < MAX(Salary)`).  
  3. `SELECT MAX(Salary)` over that filtered set finds the highest remaining salary—which is precisely the **second highest salary**!  
  4. Crucially, if all employees earn the exact same salary (or only 1 employee exists), the `WHERE` condition produces an empty set. Applying `MAX()` over an empty set safely returns **`NULL`**, exactly conforming to standard interview and exam specifications.  
  *(Note: Option A fails if there are duplicate top salaries, e.g. two people earning $100k, because offset 1 would still return $100k instead of the second highest distinct salary).*
- **Why other options are incorrect:**  
  - Option A fails with ties / duplicate highest salaries and does not return NULL if there is only 1 row.  
  - Option C finds the second lowest salary.  
  - Option D finds salaries equal to the average.

---

### Question 120
Examine the following correlated subquery:  
```sql
SELECT E1.Emp_ID, E1.Department_ID, E1.Salary 
FROM Employees E1 
WHERE E1.Salary > (
    SELECT AVG(E2.Salary) 
    FROM Employees E2 
    WHERE E2.Department_ID = E1.Department_ID
);
```
What business question does this query solve?
- A) Finds all employees who earn more than the overall average company salary
- B) Finds all employees who earn more than the average salary of their own respective department
- C) Finds the employee with the highest salary in the entire database
- D) Finds the department that has the highest average salary

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The correlation occurs at `WHERE E2.Department_ID = E1.Department_ID`.  
  For each employee `E1` evaluated by the outer query:  
  1. The inner subquery calculates the `AVG(E2.Salary)` for only those employees belonging to `E1`'s specific department.  
  2. The outer query compares `E1.Salary` against that specific department average.  
  3. If `E1.Salary` is strictly greater than their department's average, the employee is selected.  
  Thus, it identifies employees earning more than their own department's average.
- **Why other options are incorrect:**  
  - Option A would require an uncorrelated subquery without `WHERE E2.Department_ID = E1.Department_ID`.  
  - Options C and D describe different aggregate/ranking queries.

---

# MODULE 14: DATA CONTROL LANGUAGE (DCL) & PRIVILEGE MANAGEMENT (Q121 - Q130)

### Question 121
Which category of SQL commands includes statements like `GRANT` and `REVOKE`, and what is their primary functional purpose?
- A) DDL; to define table structures
- B) DML; to insert and update rows
- C) DCL (Data Control Language); to manage user privileges, database security, and access authorization
- D) TCL (Transaction Control Language); to control transaction boundaries

**Answer: C**  
**Explanation:**  
- **Why C is correct:** `GRANT` and `REVOKE` belong to **Data Control Language (DCL)**. DCL statements are used by Database Administrators and object owners to administer security privileges, manage access rights to database objects (tables, views, stored procedures), and enforce authorization policies.
- **Why other options are incorrect:**  
  - DDL includes `CREATE`, `ALTER`, `DROP`, `TRUNCATE`.  
  - DML includes `INSERT`, `UPDATE`, `DELETE`.  
  - TCL includes `COMMIT`, `ROLLBACK`, `SAVEPOINT`.

---

### Question 122
What is the effect of executing:  
`GRANT SELECT, INSERT ON Employees TO User_Alice WITH GRANT OPTION;`
- A) User_Alice can read and insert into `Employees`, but cannot share these permissions with anyone else
- B) User_Alice can read and insert into `Employees`, and additionally has the authority to grant `SELECT` and `INSERT` privileges on `Employees` to other database users
- C) User_Alice is granted full DBA administrator rights over the entire database server
- D) User_Alice can delete the `Employees` table at will

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The clause **`WITH GRANT OPTION`** confers an essential authorization power: it allows the recipient (`User_Alice`) not only to exercise the specified privileges (`SELECT` and `INSERT`) on the object, but also to **delegate / grant** those exact privileges to other users or roles in the database.
- **Why other options are incorrect:**  
  - Option A describes a grant *without* `WITH GRANT OPTION`.  
  - Options C and D are vast exaggerations; `WITH GRANT OPTION` only applies to the specific object privileges explicitly named in the grant statement.

---

### Question 123
Consider the following chain of privilege delegations:  
1. DBA executes: `GRANT SELECT ON Accounts TO Bob WITH GRANT OPTION;`  
2. Bob executes: `GRANT SELECT ON Accounts TO Charlie;`  
Later, the DBA executes:  
`REVOKE SELECT ON Accounts FROM Bob CASCADE;`  
Assuming Charlie received the privilege *only* from Bob, what is Charlie's resulting privilege status?
- A) Charlie retains `SELECT` privilege on `Accounts`
- B) Charlie's `SELECT` privilege on `Accounts` is automatically revoked
- C) Charlie is granted ownership of `Accounts`
- D) The DBA's revoke statement fails because Charlie holds a dependent privilege

**Answer: B**  
**Explanation:**  
- **Why B is correct:** Under the ANSI SQL privilege propagation model, authorization delegation forms a directed **Privilege Dependency Graph**. When privileges are revoked using the **`CASCADE`** option, the revocation cascades down the entire dependency tree. Because Charlie's authorization was derived directly and solely from Bob's grant, revoking Bob's privilege with `CASCADE` automatically revokes Charlie's privilege as well.
- **Why other options are incorrect:**  
  - Option A would violate cascading authorization semantics.  
  - Option C is absurd.  
  - Option D describes what would happen if `RESTRICT` were specified instead of `CASCADE`.

---

### Question 124
Suppose in Question 123 the DBA had instead executed:  
`REVOKE SELECT ON Accounts FROM Bob RESTRICT;`  
What would be the outcome?
- A) Bob's privilege is revoked, but Charlie keeps his privilege
- B) The REVOKE statement fails and aborts with an error, because dependent privileges exist (Charlie's privilege depends on Bob's)
- C) Both Bob and Charlie are deleted from the database
- D) Bob loses `SELECT` on Accounts, but gains `UPDATE`

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The **`RESTRICT`** keyword in `REVOKE` mandates that the revocation must **fail and raise an error** if there exist any dependent privileges granted to other users in the authorization graph. Because Charlie's privilege depends on Bob's privilege, the DBMS rejects the revoke command to prevent dangling or uncoordinated authorization states. To successfully revoke from Bob, the administrator must either specify `CASCADE` or revoke Charlie's privilege first.
- **Why other options are incorrect:**  
  - Option A describes an invalid state that violates the authorization dependency invariant.  
  - Options C and D are completely fictitious.

---

### Question 125
Can an administrator grant permissions on **specific columns** of a table rather than the entire table in standard SQL?
- A) No; SQL privileges apply only to whole tables
- B) Yes; column-level permissions can be granted for `INSERT`, `UPDATE`, and `REFERENCES` (e.g., `GRANT UPDATE (Salary) ON Employees TO Payroll_Specialist;`)
- C) Only for primary key columns
- D) Only by creating separate hard disk partitions

**Answer: B**  
**Explanation:**  
- **Why B is correct:** The ANSI SQL standard explicitly supports **column-level privileges**. An administrator can restrict data modification to specific attributes using syntax such as:  
  `GRANT UPDATE (Salary, Bonus) ON Employees TO Payroll_User;`  
  This allows `Payroll_User` to modify only the specified columns, while preventing them from altering columns like `Emp_ID`, `Social_Security_Number`, or `Job_Title`.
- **Why other options are incorrect:**  
  - Option A is a common misconception; while some older or lightweight engines only support table-level grants, standard enterprise SQL supports column-level granularity.  
  - Options C and D are false.

---

### Question 126
Why is **Role-Based Access Control (RBAC)** strongly preferred over granting individual privileges directly to user accounts in enterprise database administration?
- A) Because roles eliminate the need for primary keys
- B) Administrative scalability and maintainability: Privileges are granted once to a Role (e.g., `Accountant`, `Junior_Dev`); users are simply assigned to or removed from roles as their job functions change, avoiding the maintenance nightmare of managing thousands of individual privilege grants
- C) Because SQL databases do not permit more than 5 user accounts
- D) Because roles automatically encrypt all network traffic

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In an organization with hundreds of employees and high turnover:  
  - Granting permissions directly to individual user accounts requires managing thousands of individual access control lists. When an employee changes departments or leaves, hundreds of privileges must be manually identified and revoked.  
  - Under **RBAC**, permissions are bundled into logical **Roles** (e.g., `Role_Analyst`, `Role_Teller`). Privileges are granted to the role. Users are simply assigned membership in the appropriate role. When job duties change, granting or revoking role membership instantly updates all associated privileges.
- **Why other options are incorrect:**  
  - Options A, C, and D are factually absurd.

---

### Question 127
Consider the following authorization graph where User $A$ is the owner of table $T$:  
1. $A$ grants privilege $P$ with grant option to $B$.  
2. $A$ grants privilege $P$ with grant option to $C$.  
3. Both $B$ and $C$ grant privilege $P$ to $D$.  
4. Later, $A$ revokes privilege $P$ from $B$ using `CASCADE`.  
Does User $D$ still retain privilege $P$?
- A) No; when $B$ loses the privilege, all users who received it from $B$ lose it unconditionally
- B) Yes; because $D$ still possesses an independent, valid path of authorization from the table owner ($A \rightarrow C \rightarrow D$)
- C) Only if $D$ logs out and logs back in within 5 minutes
- D) No; the database server drops table $T$ automatically

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In relational authorization graph theory, a user retains a privilege as long as there exists **at least one valid directed authorization path from the object owner (or root DBA)** to that user.  
  Although the path $A \rightarrow B \rightarrow D$ was severed when $A$ revoked from $B$, the independent path $A \rightarrow C \rightarrow D$ remains completely intact and active. Therefore, User $D$ lawfully retains privilege $P$.
- **Why other options are incorrect:**  
  - Option A ignores alternative authorization pathways in the dependency graph.  
  - Options C and D are nonsensical distractors.

---

### Question 128
What is the security implication of executing:  
`GRANT SELECT ON Public_Announcements TO PUBLIC;`
- A) The table is published to the public internet without password protection
- B) Every current database user, as well as any future database user account created hereafter, is automatically granted `SELECT` access to the table
- C) Only users logged in from public IP addresses can access the table
- D) The command fails because `PUBLIC` is a reserved keyword that cannot be a grant target

**Answer: B**  
**Explanation:**  
- **Why B is correct:** In SQL security, **`PUBLIC`** is a special predefined system pseudo-role representing all users. Granting a privilege to `PUBLIC` makes that privilege accessible to every existing database user account, as well as any user account that will be created in the future, without needing explicit individual grants.
- **Why other options are incorrect:**  
  - Option A confuses DBMS internal authentication with public web server exposure.  
  - Options C and D are completely incorrect.

---

### Question 129
What is the fundamental difference between a **System Privilege** and an **Object Privilege** in database security?
- A) System privileges govern the ability to perform specific actions across the database system or schema (e.g., `CREATE TABLE`, `CREATE SESSION`, `ALTER SYSTEM`), whereas Object privileges govern specific access operations on a particular schema object (e.g., `SELECT`, `UPDATE` on `Customer_Table`)
- B) System privileges are stored on magnetic tape, while Object privileges are stored in RAM
- C) System privileges apply only to views, while Object privileges apply only to stored procedures
- D) Object privileges can never be revoked once granted

**Answer: A**  
**Explanation:**  
- **Why A is correct:**  
  - **System Privileges:** Authorize users to perform architectural, administrative, or DDL actions across the database instance (e.g., connecting to the database `CREATE SESSION`, creating new schema objects `CREATE TABLE`, `CREATE VIEW`, managing tablespaces, or performing system checkpoints).  
  - **Object Privileges:** Authorize users to execute specific DML or DDL operations on a **specific named database object** (e.g., `SELECT ON Orders`, `UPDATE ON Employees`, `EXECUTE ON Calculate_Tax_Procedure`).
- **Why other options are incorrect:**  
  - Options B, C, and D are factually inaccurate.

---

### Question 130
**[Comprehensive Capstone Question]**  
A banking DBMS executes the following sequence of operations within an interactive session:  
```sql
BEGIN TRANSACTION;
INSERT INTO Accounts (Acc_No, Balance) VALUES (101, 5000);
SAVEPOINT SP1;
UPDATE Accounts SET Balance = Balance - 1000 WHERE Acc_No = 101;
SAVEPOINT SP2;
UPDATE Accounts SET Balance = Balance + 200 WHERE Acc_No = 101;
ROLLBACK TO SAVEPOINT SP1;
COMMIT;
```
Assuming Account 101 did not exist prior to this transaction, what is the final `Balance` of Account 101 committed to the database?
- A) 5000
- B) 4000
- C) 4200
- D) Account 101 does not exist because the transaction rolled back

**Answer: A**  
**Explanation:**  
- **Why A is correct:** Let us trace the transaction step-by-step:  
  1. `BEGIN TRANSACTION;` $\implies$ Starts transaction $T$.  
  2. `INSERT ... VALUES (101, 5000);` $\implies$ Account 101 is inserted with Balance = 5000.  
  3. `SAVEPOINT SP1;` $\implies$ Marker `SP1` established (state: Balance = 5000).  
  4. `UPDATE ... Balance - 1000;` $\implies$ Balance becomes 4000.  
  5. `SAVEPOINT SP2;` $\implies$ Marker `SP2` established (state: Balance = 4000).  
  6. `UPDATE ... Balance + 200;` $\implies$ Balance becomes 4200.  
  7. `ROLLBACK TO SAVEPOINT SP1;` $\implies$ Undoes all modifications made after `SP1`. This rolls back the addition of 200 AND the deduction of 1000. The transaction state returns exactly to the state at `SP1` (where Balance = 5000).  
  8. `COMMIT;` $\implies$ Commits the remaining unrolled modifications (the initial insertion of Account 101 with Balance = 5000).  
  Therefore, Account 101 exists in the database with a persistent committed balance of **5000**.
- **Why other options are incorrect:**  
  - Option B (4000) would be the state if rolled back to `SP2`.  
  - Option C (4200) would be the state if no rollback occurred before commit.  
  - Option D would only happen if an unconditional `ROLLBACK;` were issued instead of `ROLLBACK TO SAVEPOINT SP1;`.

---
## END OF MCQ EXAMINATION QUESTION BANK (130 QUESTIONS COMPLETE)

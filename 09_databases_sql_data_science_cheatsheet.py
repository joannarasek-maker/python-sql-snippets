"""
IBM: Databases and SQL for Data Science with Python — CHEAT SHEET

Zakres:
- SQL basics: SELECT, WHERE, ORDER BY, LIMIT
- Aggregations: COUNT, SUM, AVG, GROUP BY, HAVING
- JOINs
- Subqueries & Views
- CRUD operations
- DB2 connection (ibm_db)
- SQLAlchemy + pandas
"""

# =========================
# 1. BASIC SQL QUERIES
# =========================

"""
SELECT *
FROM employees
LIMIT 5;

SELECT first_name, last_name, salary
FROM employees
WHERE salary > 60000
ORDER BY salary DESC;
"""

# =========================
# 2. AGGREGATIONS
# =========================

"""
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department;

SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;
"""

# =========================
# 3. JOINS
# =========================

"""
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id;
"""

# =========================
# 4. SUBQUERIES
# =========================

"""
SELECT *
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
);
"""

# =========================
# 5. VIEWS
# =========================

"""
CREATE VIEW high_salary_employees AS
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 80000;

SELECT * FROM high_salary_employees;
"""

# =========================
# 6. CRUD OPERATIONS
# =========================

"""
INSERT INTO employees (first_name, last_name, salary)
VALUES ('Anna', 'Nowak', 75000);

UPDATE employees
SET salary = 80000
WHERE last_name = 'Nowak';

DELETE FROM employees
WHERE last_name = 'Nowak';
"""

# =========================
# 7. DB2 CONNECTION (ibm_db)
# =========================

import ibm_db

dsn = (
    "DATABASE=your_db;"
    "HOSTNAME=hostname;"
    "PORT=port;"
    "PROTOCOL=TCPIP;"
    "UID=username;"
    "PWD=password;"
    "SECURITY=SSL;"
)

conn = ibm_db.connect(dsn, "", "")

sql = "SELECT * FROM employees FETCH FIRST 5 ROWS ONLY"
stmt = ibm_db.exec_immediate(conn, sql)

result = []
row = ibm_db.fetch_assoc(stmt)
while row:
    result.append(row)
    row = ibm_db.fetch_assoc(stmt)

ibm_db.close(conn)

# =========================
# 8. SQLAlchemy CONNECTION
# =========================

from sqlalchemy import create_engine, text

engine = create_engine(
    "db2+ibm_db://username:password@hostname:port/database"
)

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM employees"))
    rows = result.fetchall()

# =========================
# 9. SQL + pandas
# =========================

import pandas as pd

query = """
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
"""

df = pd.read_sql(query, engine)
print(df)

# =========================
# 10. PARAMETERIZED QUERY (SAFE)
# =========================

query = text("""
SELECT *
FROM employees
WHERE salary > :min_salary
""")

df_filtered = pd.read_sql(query, engine, params={"min_salary": 70000})

# =========================
# 11. WRITE DATAFRAME TO DB
# =========================

df_filtered.to_sql(
    "high_salary_employees",
    engine,
    if_exists="replace",
    index=False
)

# =========================
# 12. QUICK SQL TEMPLATES
# =========================

"""
-- Top N rows
SELECT *
FROM table
FETCH FIRST 10 ROWS ONLY;

-- Distinct values
SELECT DISTINCT department
FROM employees;

-- Check table structure
DESCRIBE employees;
"""

# =========================
# END
# =========================

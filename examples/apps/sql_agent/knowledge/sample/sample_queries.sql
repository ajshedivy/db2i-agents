-- ============================================================================
-- DB2 for IBM i Sample Queries
-- ============================================================================

-- ----------------------------------------------------------------------------
-- BASIC QUERIES
-- ----------------------------------------------------------------------------

-- 1. Select all employees' information
SELECT EMPNO, FIRSTNME, LASTNAME
FROM SAMPLE2.EMPLOYEE;

-- 2. Select all departments with their department numbers
SELECT DEPTNO, DEPTNAME
FROM SAMPLE2.DEPARTMENT;

-- 3. Select employees hired after a specific date
SELECT EMPNO, FIRSTNME, LASTNAME, HIREDATE
FROM SAMPLE2.EMPLOYEE
WHERE HIREDATE > '2000-01-01';

-- 4. Select projects managed by a specific department
SELECT PROJNO, PROJNAME, DEPTNO
FROM SAMPLE2.PROJECT
WHERE DEPTNO = 'D11';

-- 5. Select employees by job title
SELECT EMPNO, FIRSTNME, LASTNAME, JOB
FROM SAMPLE2.EMPLOYEE
WHERE JOB = 'MANAGER';

-- ----------------------------------------------------------------------------
-- JOINS AND RELATIONSHIPS
-- ----------------------------------------------------------------------------

-- 6. Employees with their department names
-- Using the foreign key relationship: EMPLOYEE.WORKDEPT → DEPARTMENT.DEPTNO
SELECT E.EMPNO, E.FIRSTNME, E.LASTNAME, D.DEPTNAME
FROM SAMPLE2.EMPLOYEE E
JOIN SAMPLE2.DEPARTMENT D ON E.WORKDEPT = D.DEPTNO;

-- 7. Departments with their managers
-- Using the foreign key relationship: DEPARTMENT.MGRNO → EMPLOYEE.EMPNO
SELECT D.DEPTNO, D.DEPTNAME, E.FIRSTNME AS MANAGER_FIRST_NAME, E.LASTNAME AS MANAGER_LAST_NAME
FROM SAMPLE2.DEPARTMENT D
LEFT JOIN SAMPLE2.EMPLOYEE E ON D.MGRNO = E.EMPNO;

-- 8. Projects with responsible employees
-- Using the foreign key relationship: PROJECT.RESPEMP → EMPLOYEE.EMPNO
SELECT P.PROJNO, P.PROJNAME, E.FIRSTNME AS RESPONSIBLE_EMP_FIRST_NAME, E.LASTNAME AS RESPONSIBLE_EMP_LAST_NAME
FROM SAMPLE2.PROJECT P
JOIN SAMPLE2.EMPLOYEE E ON P.RESPEMP = E.EMPNO;

-- 9. Employees assigned to projects
-- Multiple table join with foreign keys:
-- EMPPROJACT.EMPNO → EMPLOYEE.EMPNO and EMPPROJACT.PROJNO → PROJECT.PROJNO
SELECT E.FIRSTNME, E.LASTNAME, P.PROJNAME
FROM SAMPLE2.EMPLOYEE E
JOIN SAMPLE2.EMPPROJACT EPA ON E.EMPNO = EPA.EMPNO
JOIN SAMPLE2.PROJECT P ON EPA.PROJNO = P.PROJNO
ORDER BY P.PROJNAME, E.LASTNAME, E.FIRSTNME;

-- ----------------------------------------------------------------------------
-- AGGREGATION QUERIES
-- ----------------------------------------------------------------------------

-- 10. Average salary by department
SELECT D.DEPTNAME, AVG(E.SALARY) AS AVERAGE_SALARY
FROM SAMPLE2.EMPLOYEE E
JOIN SAMPLE2.DEPARTMENT D ON E.WORKDEPT = D.DEPTNO
GROUP BY D.DEPTNAME
ORDER BY AVERAGE_SALARY DESC;

-- 11. Employee count by department
SELECT D.DEPTNO, D.DEPTNAME, COUNT(E.EMPNO) AS NUMBER_OF_EMPLOYEES
FROM SAMPLE2.DEPARTMENT D
LEFT JOIN SAMPLE2.EMPLOYEE E ON D.DEPTNO = E.WORKDEPT
GROUP BY D.DEPTNO, D.DEPTNAME
ORDER BY D.DEPTNO;

-- 12. Cross-department project assignments
SELECT DISTINCT E.EMPNO, E.FIRSTNME, E.LASTNAME, E.WORKDEPT, P.PROJNO, P.PROJNAME, P.DEPTNO AS PROJECT_DEPT
FROM SAMPLE2.EMPLOYEE E
JOIN SAMPLE2.EMPPROJACT EPA ON E.EMPNO = EPA.EMPNO
JOIN SAMPLE2.PROJECT P ON EPA.PROJNO = P.PROJNO
WHERE E.WORKDEPT <> P.DEPTNO;

-- 13. Total project time by project
SELECT P.PROJNO, P.PROJNAME, SUM(EPA.EMPTIME) AS TOTAL_EMP_TIME
FROM SAMPLE2.PROJECT P
JOIN SAMPLE2.EMPPROJACT EPA ON P.PROJNO = EPA.PROJNO
GROUP BY P.PROJNO, P.PROJNAME
ORDER BY TOTAL_EMP_TIME DESC;

-- ----------------------------------------------------------------------------
-- MULTI-TABLE COMPLEX QUERIES
-- ----------------------------------------------------------------------------

-- 14. Activities for each project
-- Three-table join with foreign keys
SELECT P.PROJNAME, PA.ACTNO, A.ACTDESC, PA.ACSTDATE, PA.ACENDATE
FROM SAMPLE2.PROJECT P
JOIN SAMPLE2.PROJACT PA ON P.PROJNO = PA.PROJNO
JOIN SAMPLE2.ACT A ON PA.ACTNO = A.ACTNO;

-- 15. Project timeline information
SELECT PROJNO, PROJNAME, PRSTDATE, PRENDATE
FROM SAMPLE2.PROJECT
ORDER BY PRSTDATE;

-- 16. Employee project assignments with detailed information
SELECT E.FIRSTNME, E.LASTNAME, P.PROJNAME, EPA.ACTNO, EPA.EMPTIME
FROM SAMPLE2.EMPLOYEE E
JOIN SAMPLE2.EMPPROJACT EPA ON E.EMPNO = EPA.EMPNO
JOIN SAMPLE2.PROJECT P ON EPA.PROJNO = P.PROJNO
ORDER BY P.PROJNAME, E.LASTNAME, E.FIRSTNME, EPA.ACTNO;

-- ----------------------------------------------------------------------------
-- SPECIALIZED QUERIES
-- ----------------------------------------------------------------------------

-- 17. Projects with staffing level exceeding threshold
SELECT PROJNO, PROJNAME, PRSTAFF
FROM SAMPLE2.PROJECT
WHERE PRSTAFF > 3.00;

-- 18. Sub-projects with employee assignments
SELECT DISTINCT P.PROJNO, P.PROJNAME, P.MAJPROJ
FROM SAMPLE2.PROJECT P
JOIN SAMPLE2.EMPPROJACT EPA ON P.PROJNO = EPA.PROJNO
WHERE P.MAJPROJ IS NOT NULL;

-- 19. Assignments after a specific date
SELECT EMPNO, PROJNO, ACTNO, EMSTDATE
FROM SAMPLE2.EMPPROJACT
WHERE EMSTDATE > '2002-06-01';

-- 20. Employees working on multiple project activities
-- Using string concatenation to create unique activity identifier
SELECT EMPNO, COUNT(DISTINCT PROJNO || CHAR(ACTNO)) AS ACTIVITY_COUNT
FROM SAMPLE2.EMPPROJACT
GROUP BY EMPNO
HAVING COUNT(DISTINCT PROJNO || CHAR(ACTNO)) > 1
ORDER BY ACTIVITY_COUNT DESC;

-- 21. Project hierarchy using self-join
-- Using the foreign key relationship: PROJECT.MAJPROJ → PROJECT.PROJNO
SELECT P1.PROJNO AS SUB_PROJ_NO, P1.PROJNAME AS SUB_PROJ_NAME,
       P1.MAJPROJ AS MAIN_PROJ_NO, P2.PROJNAME AS MAIN_PROJ_NAME
FROM SAMPLE2.PROJECT P1
LEFT JOIN SAMPLE2.PROJECT P2 ON P1.MAJPROJ = P2.PROJNO
WHERE P1.MAJPROJ IS NOT NULL;

-- 22. Early-completion assignments
-- Finding assignments that end before the project's planned end date
SELECT EPA.EMPNO, EPA.PROJNO, P.PROJNAME, EPA.ACTNO, EPA.EMENDATE, P.PRENDATE
FROM SAMPLE2.EMPPROJACT EPA
JOIN SAMPLE2.PROJECT P ON EPA.PROJNO = P.PROJNO
WHERE EPA.EMENDATE IS NOT NULL AND P.PRENDATE IS NOT NULL AND EPA.EMENDATE < P.PRENDATE;

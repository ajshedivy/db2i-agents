--  category:  Data Definition Language (DDL)
--  description:  (re)Attach a partition 

ALTER TABLE account 
ATTACH PARTITION p2011 FROM Archived_2011_Accounts;


--  category:  Data Definition Language (DDL)
--  description:  Add generated columns to a table

ALTER TABLE account
ADD COLUMN audit_type_change CHAR(1) GENERATED ALWAYS AS (DATA CHANGE OPERATION)
ADD COLUMN audit_user VARCHAR(128) GENERATED ALWAYS AS (SESSION_USER) 
ADD COLUMN audit_client_IP VARCHAR(128) GENERATED ALWAYS AS (SYSIBM.CLIENT_IPADDR) 
ADD COLUMN audit_job_name VARCHAR(28) GENERATED ALWAYS AS (QSYS2.JOB_NAME);



--  category:  Data Definition Language (DDL)
--  description:  Alter Sequence

ALTER SEQUENCE seq1 DATA TYPE BIGINT INCREMENT BY 10 MINVALUE 100 NO MAXVALUE CYCLE CACHE 5 ORDER;


--  category:  Data Definition Language (DDL)
--  description:  Alter Sequence to Restart

ALTER SEQUENCE seq1 RESTART;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to Add Column

ALTER TABLE table1 ADD COLUMN column3 INTEGER;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to Add Materialized Query

ALTER TABLE table1 ADD MATERIALIZED QUERY (select int_col, varchar_col from table3) DATA INITIALLY IMMEDIATE REFRESH DEFERRED MAINTAINED BY USER ENABLE QUERY OPTIMIZATION;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to Alter Column

ALTER TABLE table1 ALTER COLUMN column1 SET DATA TYPE DECIMAL(31, 0);


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to Drop Column

ALTER TABLE table1 DROP COLUMN column3;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to add Foreign Key Constraint

ALTER TABLE table1 ADD CONSTRAINT constraint3 FOREIGN KEY (column2) REFERENCES table2 ON DELETE RESTRICT ON UPDATE RESTRICT;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to add Hash Partition

ALTER TABLE employee ADD PARTITION BY HASH (empno, firstnme, midinit, lastname) INTO 20 PARTITIONS;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to add Primary Key Constraint

ALTER TABLE table1 ADD CONSTRAINT constraint1 PRIMARY KEY (column1);


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to add Range Partition

ALTER TABLE employee
  ADD PARTITION BY RANGE (lastname NULLS LAST) (
    PARTITION a_l STARTING FROM ('A') INCLUSIVE ENDING AT ('M') EXCLUSIVE ,
    PARTITION m_z STARTING FROM ('M') INCLUSIVE ENDING AT (MAXVALUE) INCLUSIVE
  );


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to add Unique Constraint

ALTER TABLE table1 ADD CONSTRAINT constraint2 UNIQUE (column2);


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to be located in memory

ALTER TABLE table1 ALTER KEEP IN MEMORY YES;


--  category:  Data Definition Language (DDL)
--  description:  Alter Table to be located on Solid State Drives

ALTER TABLE table1 ALTER UNIT SSD;


--  category:  Data Definition Language (DDL)
--  description:  Comment for Variable

COMMENT ON VARIABLE MYSCHEMA.MYJOB_PRINTER IS 'Comment for this variable';


--  category:  Data Definition Language (DDL)
--  description:  Comment on Alias

COMMENT ON ALIAS alias1 IS 'comment';


--  category:  Data Definition Language (DDL)
--  description:  Comment on Column

COMMENT ON COLUMN table1 (column2 IS 'comment', column3 IS 'comment');


--  category:  Data Definition Language (DDL)
--  description:  Create Alias for Table

CREATE ALIAS alias1 FOR table1;


--  category:  Data Definition Language (DDL)
--  description:  Create Distinct Type

CREATE DISTINCT TYPE type1 AS INTEGER WITH COMPARISONS;


--  category:  Data Definition Language (DDL)
--  description:  Create Schema

CREATE SCHEMA schema1;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Alias for Table

CREATE OR REPLACE ALIAS alias2 FOR table2(member1);


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Hash Table

CREATE OR REPLACE TABLE phashtable1 (
            empno CHAR(6) NOT NULL, firstnme VARCHAR(12) NOT NULL, lastname VARCHAR(15) CCSID 37 NOT NULL,
            workdept CHAR(3))
    PARTITION BY HASH (workdept) INTO 10 PARTITIONS ;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Range Table

CREATE OR REPLACE TABLE prangetable1 (
            empnum INTEGER, firstnme VARCHAR(12) NOT NULL, lastname VARCHAR(15) NOT NULL, workdept CHAR(3))
    PARTITION BY RANGE (empnum) (
            STARTING FROM (MINVALUE) INCLUSIVE ENDING AT (1000) INCLUSIVE,
            STARTING FROM (1001) INCLUSIVE ENDING AT (MAXVALUE) INCLUSIVE
        );


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Range Table 2

CREATE OR REPLACE TABLE prangetable2 (widget CHAR(100), price DECIMAL(6, 2), date_sold DATE)
    PARTITION BY RANGE (date_sold) (
            STARTING FROM ('2015-01-01') INCLUSIVE ENDING AT ('2021-01-01') EXCLUSIVE EVERY 3 MONTHS
        );


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Sequence

CREATE OR REPLACE SEQUENCE seq1 START WITH 10 INCREMENT BY 10;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Table

CREATE OR REPLACE TABLE table1 (column1 INTEGER NOT NULL, column2 VARCHAR(100) ALLOCATE(20));


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Table With Constraints

CREATE OR REPLACE TABLE table2 (column1 INTEGER NOT NULL CONSTRAINT constraint9 PRIMARY KEY, column2 DECIMAL(5, 2));


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Table With Data Deferred

CREATE OR REPLACE TABLE mqt1 AS
            (SELECT sys_tname, LABEL
                    FROM qsys2.systables
                    WHERE sys_dname = 'QGPL')
            DATA INITIALLY DEFERRED REFRESH DEFERRED MAINTAINED BY USER ENABLE QUERY OPTIMIZATION;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Trigger After Insert

CREATE OR REPLACE TRIGGER NEW_HIRE AFTER INSERT ON EMPLOYEE FOR EACH ROW MODE DB2SQL UPDATE COMPANY_STATS SET NBEMP = NBEMP + 1;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Trigger After Update

CREATE OR REPLACE TRIGGER SAL_ADJ
        AFTER UPDATE OF SALARY ON EMPLOYEE
        REFERENCING OLD AS OLD_EMP NEW AS NEW_EMP FOR EACH ROW MODE DB2SQL
    WHEN (NEW_EMP.SALARY > (OLD_EMP.SALARY * 1.20))
    BEGIN ATOMIC
        SIGNAL SQLSTATE '75001' ('Invalid Salary Increase - Exceeds 20%');
    END;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Trigger Instead of Insert

CREATE OR REPLACE TRIGGER trig2
        INSTEAD OF INSERT ON view1
        REFERENCING NEW newrow FOR EACH ROW
    INSERT INTO table1 (
                column1, column2)
        VALUES (newrow.column1, ENCRYPT_RC2(newrow.column2, 'pwd456'));


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace Variable

CREATE OR REPLACE VARIABLE MYSCHEMA.MYJOB_PRINTER VARCHAR(30)DEFAULT 'Default printer';


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace View

CREATE OR REPLACE VIEW view1 AS SELECT column1, column2, column3 FROM table2 WHERE column1 > 5;


--  category:  Data Definition Language (DDL)
--  description:  Create or Replace View With Check Options

CREATE OR REPLACE VIEW view1 AS SELECT * FROM table2 WHERE column1 > 5 WITH CHECK OPTION;


--  category:  Data Definition Language (DDL)
--  description:  Detach a partition

ALTER TABLE account 
DETACH PARTITION p2011 INTO Archived_2011_Accounts;


--  category:  Data Definition Language (DDL)
--  description:  Drop Alias

DROP ALIAS alias1;


--  category:  Data Definition Language (DDL)
--  description:  Drop Distinct Type Cascade

DROP DISTINCT TYPE type1 CASCADE;


--  category:  Data Definition Language (DDL)
--  description:  Drop Schema

DROP SCHEMA schema1;


--  category:  Data Definition Language (DDL)
--  description:  Drop Table and Restrict

DROP TABLE table3 RESTRICT;


--  category:  Data Definition Language (DDL)
--  description:  Drop View Cascade

DROP VIEW view3 CASCADE;


--  category:  Data Definition Language (DDL)
--  description:  Dynamically built CREATE VIEW statement

--  create a sample database
CALL QSYS.CREATE_SQL_SAMPLE('BIERHAUS');

--
-- Generate the column list for a table or view
--
SELECT LISTAGG(CAST(QSYS2.DELIMIT_NAME(COLUMN_NAME) AS CLOB(1M)), 
                   ', ') 
                   WITHIN GROUP ( ORDER BY ORDINAL_POSITION ) AS COLUMN_LIST
      FROM QSYS2.SYSCOLUMNS2 C
        WHERE TABLE_NAME   = 'EMPLOYEE' AND
              TABLE_SCHEMA = 'BIERHAUS'
              AND HIDDEN = 'N'; -- Don't include hidden columns

--
-- Generate a valid CREATE VIEW statement
--

begin
  declare create_view_statement clob(1M) ccsid 37;

  WITH Gen(Column_list) as (
    SELECT LISTAGG(CAST(QSYS2.DELIMIT_NAME(COLUMN_NAME) AS CLOB(1M)), 
                   ', ') 
                   WITHIN GROUP ( ORDER BY ORDINAL_POSITION ) AS COLUMN_LIST
      FROM QSYS2.SYSCOLUMNS2 C
        WHERE TABLE_NAME   = 'EMPLOYEE' AND
              TABLE_SCHEMA = 'BIERHAUS'
              AND HIDDEN = 'N' -- Don't include hidden columns
  )
  select 'create or replace view BIERHAUS.employee_view( '   concat Column_list concat ' )
        as (SELECT ' concat Column_list concat ' from BIERHAUS.employee)'
    into create_view_statement
    from Gen;
  execute immediate create_view_statement;
end;

-- Results in this view being created:
-- create or replace view BIERHAUS.employee_view( EMPNO, FIRSTNME, MIDINIT, LASTNAME, 
--                                                WORKDEPT, PHONENO, HIREDATE, JOB, 
--                                                EDLEVEL, SEX, BIRTHDATE, SALARY, 
--                                                BONUS, COMM )
--   as (SELECT EMPNO, FIRSTNME, MIDINIT, LASTNAME, WORKDEPT, 
--              PHONENO, HIREDATE, JOB, EDLEVEL, SEX, BIRTHDATE, 
--              SALARY, BONUS, COMM from BIERHAUS.employee)
        
        
;

--  category:  Data Definition Language (DDL)
--  description:  Establish a Temporal table
--  minvrm:  v7r3m0

ALTER TABLE account
 ADD COLUMN row_birth TIMESTAMP(12) NOT NULL IMPLICITLY HIDDEN GENERATED ALWAYS AS ROW BEGIN
 ADD COLUMN row_death  TIMESTAMP(12) NOT NULL IMPLICITLY HIDDEN 
   GENERATED ALWAYS AS ROW END    
 ADD COLUMN transaction_time 
   TIMESTAMP(12) IMPLICITLY HIDDEN GENERATED ALWAYS AS TRANSACTION START ID
 ADD PERIOD SYSTEM_TIME (row_birth, row_death);

CREATE TABLE account_hist LIKE account;

ALTER TABLE account 
   ADD VERSIONING USE HISTORY TABLE account_hist;


--  category:  Data Definition Language (DDL)
--  description:  Establish a Temporal table using a partitioned history table
--  minvrm:  v7r3m0

--
--  Note: Partitioning support is enabled via 5770SS1 Option 27 - DB2 Multisystem 
--        Email Scott Forstie (forstie@us.ibm.com) to get a free trial version of this priced option

ALTER TABLE account
 ADD COLUMN row_birth TIMESTAMP(12) NOT NULL IMPLICITLY HIDDEN GENERATED ALWAYS AS ROW BEGIN
 ADD COLUMN row_death  TIMESTAMP(12) NOT NULL IMPLICITLY HIDDEN GENERATED ALWAYS AS ROW END    
 ADD COLUMN transaction_time TIMESTAMP(12) IMPLICITLY HIDDEN GENERATED ALWAYS AS TRANSACTION START ID
 ADD PERIOD SYSTEM_TIME (row_birth, row_death);

CREATE TABLE account_hist LIKE account
PARTITION BY RANGE (row_death)
(PARTITION  p2016 STARTING ('01/01/2016') INCLUSIVE ENDING ('01/01/2017') EXCLUSIVE, 
 PARTITION  p2017 STARTING ('01/01/2017') INCLUSIVE ENDING ('01/01/2018') EXCLUSIVE, 
 PARTITION  p2018 STARTING ('01/01/2018') INCLUSIVE ENDING ('01/01/2019') EXCLUSIVE, 
 PARTITION  p2019 STARTING ('01/01/2019') INCLUSIVE ENDING ('01/01/2020') EXCLUSIVE );

ALTER TABLE account 
   ADD VERSIONING USE HISTORY TABLE account_hist;


--  category:  Data Definition Language (DDL)
--  description:  Label for Variable

LABEL ON VARIABLE MYSCHEMA.MYJOB_PRINTER IS 'Label for this variable';


--  category:  Data Definition Language (DDL)
--  description:  Label on Alias

LABEL ON ALIAS alias1 IS 'label';


--  category:  Data Definition Language (DDL)
--  description:  Label on Column

LABEL ON COLUMN table1 (column2 IS 'label', column3 IS 'label');


--  category:  Data Definition Language (DDL)
--  description:  Refresh Table

REFRESH TABLE mqt1;


--  category:  Data Definition Language (DDL)
--  description:  Rename Table

RENAME TABLE table1 TO table3;


--  category:  Data Definition Language (DDL)
--  description:  Start or stop history tracking for a Temporal table
--  minvrm:  v7r3m0

ALTER TABLE account ADD PERIOD SYSTEM_TIME (row_birth, row_death);
ALTER TABLE account ADD VERSIONING USE HISTORY TABLE account_history;


ALTER TABLE account DROP VERSIONING;
ALTER TABLE account DROP PERIOD SYSTEM_TIME;




--  category:  Data Manipulation Language (DML)
--  description:  Delete From Table

DELETE FROM table1 WHERE column1 = 0;


--  category:  Data Manipulation Language (DML)
--  description:  INSERT with FINAL TABLE
--  minvrm: V7R2M0

--
-- Setup
--
CALL qsys.create_sql_sample('TOYSTORE');
ALTER TABLE toystore.sales
  ADD COLUMN sales_id BIGINT AS IDENTITY (START WITH 1 NO CYCLE);
  
--
-- INSERT with FINAL TABLE 
--
SELECT sales_id, current timestamp as insert_time
  FROM FINAL TABLE (
      INSERT INTO toystore.sales (
            sales_date, sales_person, region, sales)
        VALUES (CURRENT DATE, 'ROWE', 'Eyota', 1)
    );
stop;


--  category:  Data Manipulation Language (DML)
--  description:  Insert into Column in Table

INSERT INTO table1 (column1) VALUES(0);


--  category:  Data Manipulation Language (DML)
--  description:  Insert into Column in Table From Another Column

INSERT INTO table1 (column1) SELECT column1 FROM table2 WHERE column1 > 5;


--  category:  Data Manipulation Language (DML)
--  description:  Insert into Table

INSERT INTO table1 VALUES(0, 'AAA', 1);


--  category:  Data Manipulation Language (DML)
--  description:  MERGE - working example

-- =================================================
-- Title: iSee how to track journal sizes over time
-- =================================================
cl: crtlib coolstuff; 

delete from  coolstuff.journal_size_tracker;
delete from  coolstuff.journal_size_tracker_hist;
-- ===================================================
--
-- The journal size tracker will use temporal support and MERGE
-- to answer questions about journal receiver size
-- growth over time.
--
-- =================================================== 
create table coolstuff.journal_size_tracker as
      (select JOURNAL_LIBRARY, JOURNAL_NAME, TOTAL_SIZE_JOURNAL_RECEIVERS, current date as Last_update
          from qsys2.journal_info)
      with data;

alter table coolstuff.journal_size_tracker
  add column row_birth timestamp(12) not null implicitly hidden generated always as row begin
  add column row_death timestamp(12) not null implicitly hidden generated always as row end
  add column transaction_time timestamp(12) implicitly hidden generated always as transaction start id
  add period system_time (row_birth, row_death);

create table coolstuff.journal_size_tracker_hist like coolstuff.journal_size_tracker;

alter table coolstuff.journal_size_tracker
  add versioning use history table coolstuff.journal_size_tracker_hist;


-- =========================================================================
--
-- Package the DML into an SQL procedure for ease of use, maintenance, and more
--
-- =========================================================================
create or replace procedure coolstuff.maintain_journal_size_tracker ()
    set option usrprf = *user
begin
  merge into coolstuff.journal_size_tracker tt using (
      select JOURNAL_LIBRARY, JOURNAL_NAME, TOTAL_SIZE_JOURNAL_RECEIVERS
        from qsys2.journal_info
    ) live
    on tt.JOURNAL_LIBRARY = live.JOURNAL_LIBRARY and
    tt.JOURNAL_NAME = live.JOURNAL_NAME
    when not matched then insert values (live.JOURNAL_LIBRARY, live.JOURNAL_NAME,
        live.TOTAL_SIZE_JOURNAL_RECEIVERS, current date)
    when matched then update set (TOTAL_SIZE_JOURNAL_RECEIVERS, last_update) = 
                                 (live.TOTAL_SIZE_JOURNAL_RECEIVERS, current date);
end;

stop;
-- The work process can be called via:
-- 1) Directly using the SQL CALL statement
-- 2) Directly using the RUNSQL CL command
-- 3) Scheduled, using a scheduled job and RUNSQL
call coolstuff.maintain_journal_size_tracker();
-- Or
cl: RUNSQL SQL('call coolstuff.maintain_journal_size_tracker()') COMMIT(*NONE) NAMING(*SQL); 
-- Or
cl: ADDJOBSCDE JOB(COOLALLOBJ) CMD(RUNSQL SQL('call coolstuff.maintain_journal_size_tracker()') COMMIT(*NONE) NAMING(*SQL)) FRQ(*WEEKLY) SCDDATE(*NONE) SCDDAY(*ALL) SCDTIME(235500)   ;
stop;

 
-- =========================================================================
--
-- Review journal receivers side, with a perspective over time
--
-- =========================================================================
select JOURNAL_LIBRARY, JOURNAL_NAME, TOTAL_SIZE_JOURNAL_RECEIVERS, last_update, 
       row_number() over (
         partition by JOURNAL_LIBRARY, JOURNAL_NAME
         order by     JOURNAL_LIBRARY, JOURNAL_NAME, last_update desc nulls last
       ) as Row_number
  from coolstuff.journal_size_tracker for
    system_time from '0001-01-01 00:00:00.000000000000' to '9999-12-30 00:00:00.000000000000';





--  category:  Data Manipulation Language (DML)
--  description: MERGE multiple rows and diagnostics area

create table mergeit.merge_result_conds (
      @DB2_PARTITION_NUMBER integer, 
      @db2_row_number integer, 
      @sqlstate char(5) for sbcs data);
      
create or replace procedure mergeit.merge_item_factp_multiple ( )
    modifies sql data
    set option output=*print
begin
  declare lc integer default 0;
  declare @number integer;
  declare @db2_row_number integer;
  declare @sqlstate char(5) for sbcs data;
  declare @cOMMAND_FUNCTION varchar(128);
  declare @COMMAND_FUNCTION_CODE integer;
  declare @DB2_DIAGNOSTIC_CONVERSION_ERROR integer;
  declare @DB2_LAST_ROW integer;
  declare @DB2_NUMBER_ROWS decimal(31, 0);
  declare @DB2_NUMBER_SUCCESSFUL_SUBSTMTS integer;
  declare @DB2_RETURN_STATUS integer;
  declare @DB2_ROW_COUNT_SECONDARY decimal(31, 0);
  declare @DB2_SQL_NESTING_LEVEL integer;
  declare @ROW_COUNT decimal(31, 0);
  declare @DB2_PARTITION_NUMBER integer;
  declare @DB2_NUMBER_CONNECTIONS integer;
  declare @DB2_NUMBER_PARAMETER_MARKERS integer;
  declare @DB2_NUMBER_RESULT_SETS integer;
  declare @DB2_RELATIVE_COST_ESTIMATE integer;
  declare @DB2_ROW_LENGTH integer;
  declare @DYNAMIC_FUNCTION varchar(128);
  declare @DYNAMIC_FUNCTION_CODE integer;
  declare @TRANSACTION_ACTIVE integer;
  declare @TRANSACTIONS_COMMITTED integer;
  declare @TRANSACTIONS_ROLLED_BACK integer;
  declare @MORE char(1);
  
  declare @db2_row_number1       integer;
  declare @sqlstate1             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER1 integer;  
  declare @db2_row_number2       integer;
  declare @sqlstate2             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER2 integer;
  declare @db2_row_number3       integer;
  declare @sqlstate3             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER3 integer;  
  declare @db2_row_number4       integer;
  declare @sqlstate4             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER4 integer;
  declare @db2_row_number5       integer;
  declare @sqlstate5             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER5 integer;  
  declare @db2_row_number6       integer;
  declare @sqlstate6             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER6 integer;
  declare @db2_row_number7       integer;
  declare @sqlstate7             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER7 integer;  
  declare @db2_row_number8       integer;
  declare @sqlstate8             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER8 integer;
  declare @db2_row_number9       integer;
  declare @sqlstate9             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER9 integer;  
  declare @db2_row_number10       integer;
  declare @sqlstate10             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER10 integer;
  declare @db2_row_number11       integer;
  declare @sqlstate11             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER11 integer;  
  declare @db2_row_number12       integer;
  declare @sqlstate12             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER12 integer;
  declare @db2_row_number13       integer;
  declare @sqlstate13             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER13 integer;  
  declare @db2_row_number14       integer;
  declare @sqlstate14             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER14 integer;
  declare @db2_row_number15       integer;
  declare @sqlstate15             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER15 integer;  
  declare @db2_row_number16       integer;
  declare @sqlstate16             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER16 integer;
  declare @db2_row_number17       integer;
  declare @sqlstate17             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER17 integer;  
  declare @db2_row_number18       integer;
  declare @sqlstate18             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER18 integer;
  declare @db2_row_number19       integer;
  declare @sqlstate19             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER19 integer;  
  declare @db2_row_number20       integer;
  declare @sqlstate20             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER20 integer;  
  declare @db2_row_number21       integer;
  declare @sqlstate21             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER21 integer;  
  declare @db2_row_number22       integer;
  declare @sqlstate22             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER22 integer;
  declare @db2_row_number23       integer;
  declare @sqlstate23             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER23 integer;  
  declare @db2_row_number24       integer;
  declare @sqlstate24             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER24 integer;
  declare @db2_row_number25       integer;
  declare @sqlstate25             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER25 integer;  
  declare @db2_row_number26       integer;
  declare @sqlstate26             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER26 integer;
  declare @db2_row_number27       integer;
  declare @sqlstate27             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER27 integer;  
  declare @db2_row_number28       integer;
  declare @sqlstate28             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER28 integer;
  declare @db2_row_number29       integer;
  declare @sqlstate29             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER29 integer;  
  declare @db2_row_number30       integer;
  declare @sqlstate30             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER30 integer;  
  declare @db2_row_number31       integer;
  declare @sqlstate31             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER31 integer;  
  declare @db2_row_number32       integer;
  declare @sqlstate32             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER32 integer;
  declare @db2_row_number33       integer;
  declare @sqlstate33             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER33 integer;  
  declare @db2_row_number34       integer;
  declare @sqlstate34             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER34 integer;
  declare @db2_row_number35       integer;
  declare @sqlstate35             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER35 integer;  
  declare @db2_row_number36       integer;
  declare @sqlstate36             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER36 integer;
  declare @db2_row_number37       integer;
  declare @sqlstate37             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER37 integer;  
  declare @db2_row_number38       integer;
  declare @sqlstate38             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER38 integer;
  declare @db2_row_number39       integer;
  declare @sqlstate39             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER39 integer;  
  declare @db2_row_number40       integer;
  declare @sqlstate40             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER40 integer;  
  declare @db2_row_number41       integer;
  declare @sqlstate41             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER41 integer;  
  declare @db2_row_number42       integer;
  declare @sqlstate42             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER42 integer;
  declare @db2_row_number43       integer;
  declare @sqlstate43             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER43 integer;  
  declare @db2_row_number44       integer;
  declare @sqlstate44             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER44 integer;
  declare @db2_row_number45       integer;
  declare @sqlstate45             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER45 integer;  
  declare @db2_row_number46       integer;
  declare @sqlstate46             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER46 integer;
  declare @db2_row_number47       integer;
  declare @sqlstate47             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER47 integer;  
  declare @db2_row_number48       integer;
  declare @sqlstate48             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER48 integer;
  declare @db2_row_number49       integer;
  declare @sqlstate49             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER49 integer;  
  declare @db2_row_number50       integer;
  declare @sqlstate50             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER50 integer;  
  declare @db2_row_number51       integer;
  declare @sqlstate51             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER51 integer;  
  declare @db2_row_number52       integer;
  declare @sqlstate52             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER52 integer;
  declare @db2_row_number53       integer;
  declare @sqlstate53             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER53 integer;  
  declare @db2_row_number54       integer;
  declare @sqlstate54             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER54 integer;
  declare @db2_row_number55       integer;
  declare @sqlstate55             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER55 integer;  
  declare @db2_row_number56       integer;
  declare @sqlstate56             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER56 integer;
  declare @db2_row_number57       integer;
  declare @sqlstate57             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER57 integer;  
  declare @db2_row_number58       integer;
  declare @sqlstate58             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER58 integer;
  declare @db2_row_number59       integer;
  declare @sqlstate59             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER59 integer;  
  declare @db2_row_number60       integer;
  declare @sqlstate60             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER60 integer;  
  declare @db2_row_number61       integer;
  declare @sqlstate61             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER61 integer;  
  declare @db2_row_number62       integer;
  declare @sqlstate62             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER62 integer;
  declare @db2_row_number63       integer;
  declare @sqlstate63             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER63 integer;  
  declare @db2_row_number64       integer;
  declare @sqlstate64             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER64 integer;
  declare @db2_row_number65       integer;
  declare @sqlstate65             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER65 integer;  
  declare @db2_row_number66       integer;
  declare @sqlstate66             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER66 integer;
  declare @db2_row_number67       integer;
  declare @sqlstate67             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER67 integer;  
  declare @db2_row_number68       integer;
  declare @sqlstate68             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER68 integer;
  declare @db2_row_number69       integer;
  declare @sqlstate69             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER69 integer;  
  declare @db2_row_number70       integer;
  declare @sqlstate70             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER70 integer;  
  declare @db2_row_number71       integer;
  declare @sqlstate71             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER71 integer;  
  declare @db2_row_number72       integer;
  declare @sqlstate72             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER72 integer;
  declare @db2_row_number73       integer;
  declare @sqlstate73             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER73 integer;  
  declare @db2_row_number74       integer;
  declare @sqlstate74             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER74 integer;
  declare @db2_row_number75       integer;
  declare @sqlstate75             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER75 integer;  
  declare @db2_row_number76       integer;
  declare @sqlstate76             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER76 integer;
  declare @db2_row_number77       integer;
  declare @sqlstate77             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER77 integer;  
  declare @db2_row_number78       integer;
  declare @sqlstate78             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER78 integer;
  declare @db2_row_number79       integer;
  declare @sqlstate79             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER79 integer;  
  declare @db2_row_number80       integer;
  declare @sqlstate80             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER80 integer;  
  declare @db2_row_number81       integer;
  declare @sqlstate81             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER81 integer;  
  declare @db2_row_number82       integer;
  declare @sqlstate82             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER82 integer;
  declare @db2_row_number83       integer;
  declare @sqlstate83             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER83 integer;  
  declare @db2_row_number84       integer;
  declare @sqlstate84             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER84 integer;
  declare @db2_row_number85       integer;
  declare @sqlstate85             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER85 integer;  
  declare @db2_row_number86       integer;
  declare @sqlstate86             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER86 integer;
  declare @db2_row_number87       integer;
  declare @sqlstate87             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER87 integer;  
  declare @db2_row_number88       integer;
  declare @sqlstate88             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER88 integer;
  declare @db2_row_number89       integer;
  declare @sqlstate89             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER89 integer;  
  declare @db2_row_number90       integer;
  declare @sqlstate90             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER90 integer;  
  declare @db2_row_number91       integer;
  declare @sqlstate91             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER91 integer;  
  declare @db2_row_number92       integer;
  declare @sqlstate92             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER92 integer;
  declare @db2_row_number93       integer;
  declare @sqlstate93             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER93 integer;  
  declare @db2_row_number94       integer;
  declare @sqlstate94             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER94 integer;
  declare @db2_row_number95       integer;
  declare @sqlstate95             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER95 integer;  
  declare @db2_row_number96       integer;
  declare @sqlstate96             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER96 integer;
  declare @db2_row_number97       integer;
  declare @sqlstate97             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER97 integer;  
  declare @db2_row_number98       integer;
  declare @sqlstate98             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER98 integer;
  declare @db2_row_number99       integer;
  declare @sqlstate99             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER99 integer;  
  declare @db2_row_number100      integer;
  declare @sqlstate100             char(5) for sbcs data;
  declare @DB2_PARTITION_NUMBER100 integer;    
  merge into mergeit.item_factp ar using (
      select ORDERKEY, PARTKEY, SUPPKEY, LINENUMBER, QUANTITY, EXTENDEDPRICE, DISCOUNT, TAX,
             RETURNFLAG, LINESTATUS, SHIPDATE, COMMITDATE, RECEIPTDATE, SHIPMODE, SUPPLYCOST,
             CUSTKEY, ORDERDATE, ORDERPRIORITY, SHIPPRIORITY, REVENUE_WO_TAX, REVENUE_W_TAX,
             PROFIT_WO_TAX, PROFIT_W_TAX, DAYS_ORDER_TO_SHIP, DAYS_ORDER_TO_RECEIPT,
             DAYS_SHIP_TO_RECEIPT, DAYS_COMMIT_TO_RECEIPT, "YEAR", "MONTH", QUARTER, DUMMYKEY,
             EXPANDER
        from KRAKorg1.item_factp_alias
    ) ac
    on (ar.ORDERKEY = ac.ORDERKEY) and
    (ar.PARTKEY = ac.PARTKEY) and
    (ar.SUPPKEY = ac.SUPPKEY) and
    (ar.LINENUMBER = ac.LINENUMBER) and
    (ar.RECEIPTDATE = ac.RECEIPTDATE)
    when matched and ac.quantity = 77 then signal sqlstate '02YY1'
      set message_text = 'quantity is 77   ' 
    when matched and ac.quantity = 88 then signal sqlstate '02YY2'
      set message_text = 'quantity is 88   ' 
    when matched and ac.quantity = 99 then signal sqlstate '02YY3'
      set message_text = 'quantity is 99   ' 
    when matched 
    then update set (QUANTITY, EXTENDEDPRICE, DISCOUNT, TAX, RETURNFLAG, LINESTATUS,
      SHIPDATE, COMMITDATE, SHIPMODE, SUPPLYCOST, CUSTKEY, ORDERDATE, ORDERPRIORITY, SHIPPRIORITY,
      REVENUE_WO_TAX, REVENUE_W_TAX, PROFIT_WO_TAX, PROFIT_W_TAX, DAYS_ORDER_TO_SHIP,
      DAYS_ORDER_TO_RECEIPT, DAYS_SHIP_TO_RECEIPT, DAYS_COMMIT_TO_RECEIPT, "YEAR", "MONTH", QUARTER,
      DUMMYKEY, EXPANDER) =
      (ac.QUANTITY, ac.EXTENDEDPRICE, ac.DISCOUNT, ac.TAX, ac.RETURNFLAG, ac.LINESTATUS,
      ac.SHIPDATE, ac.COMMITDATE, ac.SHIPMODE, ac.SUPPLYCOST, ac.CUSTKEY, ac.ORDERDATE,
      ac.ORDERPRIORITY, ac.SHIPPRIORITY, ac.REVENUE_WO_TAX, ac.REVENUE_W_TAX, ac.PROFIT_WO_TAX,
      ac.PROFIT_W_TAX, ac.DAYS_ORDER_TO_SHIP, ac.DAYS_ORDER_TO_RECEIPT, ac.DAYS_SHIP_TO_RECEIPT,
      ac.DAYS_COMMIT_TO_RECEIPT, ac."YEAR", ac."MONTH", ac.QUARTER, ac.DUMMYKEY, ac.EXPANDER)
    when not matched 
    then insert (ORDERKEY, PARTKEY, SUPPKEY,
      LINENUMBER, QUANTITY, EXTENDEDPRICE, DISCOUNT, TAX, RETURNFLAG, LINESTATUS, SHIPDATE,
      COMMITDATE, RECEIPTDATE, SHIPMODE, SUPPLYCOST, CUSTKEY, ORDERDATE, ORDERPRIORITY,
      SHIPPRIORITY, REVENUE_WO_TAX, REVENUE_W_TAX, PROFIT_WO_TAX, PROFIT_W_TAX, DAYS_ORDER_TO_SHIP,
      DAYS_ORDER_TO_RECEIPT, DAYS_SHIP_TO_RECEIPT, DAYS_COMMIT_TO_RECEIPT, "YEAR", "MONTH", QUARTER,
      DUMMYKEY, EXPANDER) values (ac.ORDERKEY, ac.PARTKEY, ac.SUPPKEY, ac.LINENUMBER, ac.QUANTITY,
        ac.EXTENDEDPRICE, ac.DISCOUNT, ac.TAX, ac.RETURNFLAG, ac.LINESTATUS, ac.SHIPDATE,
        ac.COMMITDATE, ac.RECEIPTDATE, ac.SHIPMODE, ac.SUPPLYCOST, ac.CUSTKEY, ac.ORDERDATE,
        ac.ORDERPRIORITY, ac.SHIPPRIORITY, ac.REVENUE_WO_TAX, ac.REVENUE_W_TAX, ac.PROFIT_WO_TAX,
        ac.PROFIT_W_TAX, ac.DAYS_ORDER_TO_SHIP, ac.DAYS_ORDER_TO_RECEIPT, ac.DAYS_SHIP_TO_RECEIPT,
        ac.DAYS_COMMIT_TO_RECEIPT, ac."YEAR", ac."MONTH", ac.QUARTER, ac.DUMMYKEY, ac.EXPANDER)
    else ignore;
    
  get diagnostics @number = NUMBER, @cOMMAND_FUNCTION = cOMMAND_FUNCTION,
      @COMMAND_FUNCTION_CODE = COMMAND_FUNCTION_CODE,
      @DB2_DIAGNOSTIC_CONVERSION_ERROR = DB2_DIAGNOSTIC_CONVERSION_ERROR,
      @DB2_LAST_ROW = DB2_LAST_ROW,  @DB2_NUMBER_ROWS = DB2_NUMBER_ROWS,
      @DB2_NUMBER_SUCCESSFUL_SUBSTMTS = DB2_NUMBER_SUCCESSFUL_SUBSTMTS,
      @DB2_RETURN_STATUS = DB2_RETURN_STATUS, @DB2_ROW_COUNT_SECONDARY = DB2_ROW_COUNT_SECONDARY,
      @DB2_SQL_NESTING_LEVEL = DB2_SQL_NESTING_LEVEL, @ROW_COUNT = ROW_COUNT,
      @DB2_NUMBER_CONNECTIONS = DB2_NUMBER_CONNECTIONS, @DB2_NUMBER_PARAMETER_MARKERS = DB2_NUMBER_PARAMETER_MARKERS,
      @DB2_NUMBER_RESULT_SETS = DB2_NUMBER_RESULT_SETS, @DB2_RELATIVE_COST_ESTIMATE = DB2_RELATIVE_COST_ESTIMATE,
      @DB2_ROW_LENGTH = DB2_ROW_LENGTH, @DYNAMIC_FUNCTION = DYNAMIC_FUNCTION, @DYNAMIC_FUNCTION_CODE = DYNAMIC_FUNCTION_CODE,
      @TRANSACTION_ACTIVE = TRANSACTION_ACTIVE, @TRANSACTIONS_COMMITTED = TRANSACTIONS_COMMITTED, @TRANSACTIONS_ROLLED_BACK = TRANSACTIONS_ROLLED_BACK,
      @MORE = MORE;
 

    get diagnostics condition 1 @db2_row_number1 = db2_row_number, @sqlstate1 = returned_sqlstate, @DB2_PARTITION_NUMBER1 = DB2_PARTITION_NUMBER;
    get diagnostics condition 2 @db2_row_number2 = db2_row_number, @sqlstate2 = returned_sqlstate, @DB2_PARTITION_NUMBER2 = DB2_PARTITION_NUMBER;
    get diagnostics condition 3 @db2_row_number3 = db2_row_number, @sqlstate3 = returned_sqlstate, @DB2_PARTITION_NUMBER3 = DB2_PARTITION_NUMBER;
    get diagnostics condition 4 @db2_row_number4 = db2_row_number, @sqlstate4 = returned_sqlstate, @DB2_PARTITION_NUMBER4 = DB2_PARTITION_NUMBER;
    get diagnostics condition 5 @db2_row_number5 = db2_row_number, @sqlstate5 = returned_sqlstate, @DB2_PARTITION_NUMBER5 = DB2_PARTITION_NUMBER;
    get diagnostics condition 6 @db2_row_number6 = db2_row_number, @sqlstate6 = returned_sqlstate, @DB2_PARTITION_NUMBER6 = DB2_PARTITION_NUMBER;
    get diagnostics condition 7 @db2_row_number7 = db2_row_number, @sqlstate7 = returned_sqlstate, @DB2_PARTITION_NUMBER7 = DB2_PARTITION_NUMBER;
    get diagnostics condition 8 @db2_row_number8 = db2_row_number, @sqlstate8 = returned_sqlstate, @DB2_PARTITION_NUMBER8 = DB2_PARTITION_NUMBER;
    get diagnostics condition 9 @db2_row_number9 = db2_row_number, @sqlstate9 = returned_sqlstate, @DB2_PARTITION_NUMBER9 = DB2_PARTITION_NUMBER;
    get diagnostics condition 10 @db2_row_number10 = db2_row_number, @sqlstate10 = returned_sqlstate, @DB2_PARTITION_NUMBER10 = DB2_PARTITION_NUMBER;
    get diagnostics condition 11 @db2_row_number11 = db2_row_number, @sqlstate11 = returned_sqlstate, @DB2_PARTITION_NUMBER11 = DB2_PARTITION_NUMBER;
    get diagnostics condition 12 @db2_row_number12 = db2_row_number, @sqlstate12 = returned_sqlstate, @DB2_PARTITION_NUMBER12 = DB2_PARTITION_NUMBER;
    get diagnostics condition 13 @db2_row_number13 = db2_row_number, @sqlstate13 = returned_sqlstate, @DB2_PARTITION_NUMBER13 = DB2_PARTITION_NUMBER;
    get diagnostics condition 14 @db2_row_number14 = db2_row_number, @sqlstate14 = returned_sqlstate, @DB2_PARTITION_NUMBER14 = DB2_PARTITION_NUMBER;
    get diagnostics condition 15 @db2_row_number15 = db2_row_number, @sqlstate15 = returned_sqlstate, @DB2_PARTITION_NUMBER15 = DB2_PARTITION_NUMBER;
    get diagnostics condition 16 @db2_row_number16 = db2_row_number, @sqlstate16 = returned_sqlstate, @DB2_PARTITION_NUMBER16 = DB2_PARTITION_NUMBER;
    get diagnostics condition 17 @db2_row_number17 = db2_row_number, @sqlstate17 = returned_sqlstate, @DB2_PARTITION_NUMBER17 = DB2_PARTITION_NUMBER;
    get diagnostics condition 18 @db2_row_number18 = db2_row_number, @sqlstate18 = returned_sqlstate, @DB2_PARTITION_NUMBER18 = DB2_PARTITION_NUMBER;
    get diagnostics condition 19 @db2_row_number19 = db2_row_number, @sqlstate19 = returned_sqlstate, @DB2_PARTITION_NUMBER19 = DB2_PARTITION_NUMBER;
    get diagnostics condition 20 @db2_row_number20 = db2_row_number, @sqlstate20 = returned_sqlstate, @DB2_PARTITION_NUMBER20 = DB2_PARTITION_NUMBER;
    get diagnostics condition 21 @db2_row_number21 = db2_row_number, @sqlstate21 = returned_sqlstate, @DB2_PARTITION_NUMBER21 = DB2_PARTITION_NUMBER;
    get diagnostics condition 22 @db2_row_number22 = db2_row_number, @sqlstate22 = returned_sqlstate, @DB2_PARTITION_NUMBER22 = DB2_PARTITION_NUMBER;
    get diagnostics condition 23 @db2_row_number23 = db2_row_number, @sqlstate23 = returned_sqlstate, @DB2_PARTITION_NUMBER23 = DB2_PARTITION_NUMBER;
    get diagnostics condition 24 @db2_row_number24 = db2_row_number, @sqlstate24 = returned_sqlstate, @DB2_PARTITION_NUMBER24 = DB2_PARTITION_NUMBER;
    get diagnostics condition 25 @db2_row_number25 = db2_row_number, @sqlstate25 = returned_sqlstate, @DB2_PARTITION_NUMBER25 = DB2_PARTITION_NUMBER;
    get diagnostics condition 26 @db2_row_number26 = db2_row_number, @sqlstate26 = returned_sqlstate, @DB2_PARTITION_NUMBER26 = DB2_PARTITION_NUMBER;
    get diagnostics condition 27 @db2_row_number27 = db2_row_number, @sqlstate27 = returned_sqlstate, @DB2_PARTITION_NUMBER27 = DB2_PARTITION_NUMBER;
    get diagnostics condition 28 @db2_row_number28 = db2_row_number, @sqlstate28 = returned_sqlstate, @DB2_PARTITION_NUMBER28 = DB2_PARTITION_NUMBER;
    get diagnostics condition 29 @db2_row_number29 = db2_row_number, @sqlstate29 = returned_sqlstate, @DB2_PARTITION_NUMBER29 = DB2_PARTITION_NUMBER;
    get diagnostics condition 30 @db2_row_number30 = db2_row_number, @sqlstate30 = returned_sqlstate, @DB2_PARTITION_NUMBER30 = DB2_PARTITION_NUMBER;
    get diagnostics condition 31 @db2_row_number31 = db2_row_number, @sqlstate31 = returned_sqlstate, @DB2_PARTITION_NUMBER31 = DB2_PARTITION_NUMBER;
    get diagnostics condition 32 @db2_row_number32 = db2_row_number, @sqlstate32 = returned_sqlstate, @DB2_PARTITION_NUMBER32 = DB2_PARTITION_NUMBER;
    get diagnostics condition 33 @db2_row_number33 = db2_row_number, @sqlstate33 = returned_sqlstate, @DB2_PARTITION_NUMBER33 = DB2_PARTITION_NUMBER;
    get diagnostics condition 34 @db2_row_number34 = db2_row_number, @sqlstate34 = returned_sqlstate, @DB2_PARTITION_NUMBER34 = DB2_PARTITION_NUMBER;
    get diagnostics condition 35 @db2_row_number35 = db2_row_number, @sqlstate35 = returned_sqlstate, @DB2_PARTITION_NUMBER35 = DB2_PARTITION_NUMBER;
    get diagnostics condition 36 @db2_row_number36 = db2_row_number, @sqlstate36 = returned_sqlstate, @DB2_PARTITION_NUMBER36 = DB2_PARTITION_NUMBER;
    get diagnostics condition 37 @db2_row_number37 = db2_row_number, @sqlstate37 = returned_sqlstate, @DB2_PARTITION_NUMBER37 = DB2_PARTITION_NUMBER;
    get diagnostics condition 38 @db2_row_number38 = db2_row_number, @sqlstate38 = returned_sqlstate, @DB2_PARTITION_NUMBER38 = DB2_PARTITION_NUMBER;
    get diagnostics condition 39 @db2_row_number39 = db2_row_number, @sqlstate39 = returned_sqlstate, @DB2_PARTITION_NUMBER39 = DB2_PARTITION_NUMBER;
    get diagnostics condition 40 @db2_row_number40 = db2_row_number, @sqlstate40 = returned_sqlstate, @DB2_PARTITION_NUMBER40 = DB2_PARTITION_NUMBER;
    get diagnostics condition 41 @db2_row_number41 = db2_row_number, @sqlstate41 = returned_sqlstate, @DB2_PARTITION_NUMBER41 = DB2_PARTITION_NUMBER;
    get diagnostics condition 42 @db2_row_number42 = db2_row_number, @sqlstate42 = returned_sqlstate, @DB2_PARTITION_NUMBER42 = DB2_PARTITION_NUMBER;
    get diagnostics condition 43 @db2_row_number43 = db2_row_number, @sqlstate43 = returned_sqlstate, @DB2_PARTITION_NUMBER43 = DB2_PARTITION_NUMBER;
    get diagnostics condition 44 @db2_row_number44 = db2_row_number, @sqlstate44 = returned_sqlstate, @DB2_PARTITION_NUMBER44 = DB2_PARTITION_NUMBER;
    get diagnostics condition 45 @db2_row_number45 = db2_row_number, @sqlstate45 = returned_sqlstate, @DB2_PARTITION_NUMBER45 = DB2_PARTITION_NUMBER;
    get diagnostics condition 46 @db2_row_number46 = db2_row_number, @sqlstate46 = returned_sqlstate, @DB2_PARTITION_NUMBER46 = DB2_PARTITION_NUMBER;
    get diagnostics condition 47 @db2_row_number47 = db2_row_number, @sqlstate47 = returned_sqlstate, @DB2_PARTITION_NUMBER47 = DB2_PARTITION_NUMBER;
    get diagnostics condition 48 @db2_row_number48 = db2_row_number, @sqlstate48 = returned_sqlstate, @DB2_PARTITION_NUMBER48 = DB2_PARTITION_NUMBER;
    get diagnostics condition 49 @db2_row_number49 = db2_row_number, @sqlstate49 = returned_sqlstate, @DB2_PARTITION_NUMBER49 = DB2_PARTITION_NUMBER;
    get diagnostics condition 50 @db2_row_number50 = db2_row_number, @sqlstate50 = returned_sqlstate, @DB2_PARTITION_NUMBER50 = DB2_PARTITION_NUMBER;
    get diagnostics condition 51 @db2_row_number51 = db2_row_number, @sqlstate51 = returned_sqlstate, @DB2_PARTITION_NUMBER51 = DB2_PARTITION_NUMBER;
    get diagnostics condition 52 @db2_row_number52 = db2_row_number, @sqlstate52 = returned_sqlstate, @DB2_PARTITION_NUMBER52 = DB2_PARTITION_NUMBER;
    get diagnostics condition 53 @db2_row_number53 = db2_row_number, @sqlstate53 = returned_sqlstate, @DB2_PARTITION_NUMBER53 = DB2_PARTITION_NUMBER;
    get diagnostics condition 54 @db2_row_number54 = db2_row_number, @sqlstate54 = returned_sqlstate, @DB2_PARTITION_NUMBER54 = DB2_PARTITION_NUMBER;
    get diagnostics condition 55 @db2_row_number55 = db2_row_number, @sqlstate55 = returned_sqlstate, @DB2_PARTITION_NUMBER55 = DB2_PARTITION_NUMBER;
    get diagnostics condition 56 @db2_row_number56 = db2_row_number, @sqlstate56 = returned_sqlstate, @DB2_PARTITION_NUMBER56 = DB2_PARTITION_NUMBER;
    get diagnostics condition 57 @db2_row_number57 = db2_row_number, @sqlstate57 = returned_sqlstate, @DB2_PARTITION_NUMBER57 = DB2_PARTITION_NUMBER;
    get diagnostics condition 58 @db2_row_number58 = db2_row_number, @sqlstate58 = returned_sqlstate, @DB2_PARTITION_NUMBER58 = DB2_PARTITION_NUMBER;
    get diagnostics condition 59 @db2_row_number59 = db2_row_number, @sqlstate59 = returned_sqlstate, @DB2_PARTITION_NUMBER59 = DB2_PARTITION_NUMBER;
    get diagnostics condition 60 @db2_row_number60 = db2_row_number, @sqlstate60 = returned_sqlstate, @DB2_PARTITION_NUMBER60 = DB2_PARTITION_NUMBER;
    get diagnostics condition 61 @db2_row_number61 = db2_row_number, @sqlstate61 = returned_sqlstate, @DB2_PARTITION_NUMBER61 = DB2_PARTITION_NUMBER;
    get diagnostics condition 62 @db2_row_number62 = db2_row_number, @sqlstate62 = returned_sqlstate, @DB2_PARTITION_NUMBER62 = DB2_PARTITION_NUMBER;
    get diagnostics condition 63 @db2_row_number63 = db2_row_number, @sqlstate63 = returned_sqlstate, @DB2_PARTITION_NUMBER63 = DB2_PARTITION_NUMBER;
    get diagnostics condition 64 @db2_row_number64 = db2_row_number, @sqlstate64 = returned_sqlstate, @DB2_PARTITION_NUMBER64 = DB2_PARTITION_NUMBER;
    get diagnostics condition 65 @db2_row_number65 = db2_row_number, @sqlstate65 = returned_sqlstate, @DB2_PARTITION_NUMBER65 = DB2_PARTITION_NUMBER;
    get diagnostics condition 66 @db2_row_number66 = db2_row_number, @sqlstate66 = returned_sqlstate, @DB2_PARTITION_NUMBER66 = DB2_PARTITION_NUMBER;
    get diagnostics condition 67 @db2_row_number67 = db2_row_number, @sqlstate67 = returned_sqlstate, @DB2_PARTITION_NUMBER67 = DB2_PARTITION_NUMBER;
    get diagnostics condition 68 @db2_row_number68 = db2_row_number, @sqlstate68 = returned_sqlstate, @DB2_PARTITION_NUMBER68 = DB2_PARTITION_NUMBER;
    get diagnostics condition 69 @db2_row_number69 = db2_row_number, @sqlstate69 = returned_sqlstate, @DB2_PARTITION_NUMBER69 = DB2_PARTITION_NUMBER;
    get diagnostics condition 70 @db2_row_number70 = db2_row_number, @sqlstate70 = returned_sqlstate, @DB2_PARTITION_NUMBER70 = DB2_PARTITION_NUMBER;
    get diagnostics condition 71 @db2_row_number71 = db2_row_number, @sqlstate71 = returned_sqlstate, @DB2_PARTITION_NUMBER71 = DB2_PARTITION_NUMBER;
    get diagnostics condition 72 @db2_row_number72 = db2_row_number, @sqlstate72 = returned_sqlstate, @DB2_PARTITION_NUMBER72 = DB2_PARTITION_NUMBER;
    get diagnostics condition 73 @db2_row_number73 = db2_row_number, @sqlstate73 = returned_sqlstate, @DB2_PARTITION_NUMBER73 = DB2_PARTITION_NUMBER;
    get diagnostics condition 74 @db2_row_number74 = db2_row_number, @sqlstate74 = returned_sqlstate, @DB2_PARTITION_NUMBER74 = DB2_PARTITION_NUMBER;
    get diagnostics condition 75 @db2_row_number75 = db2_row_number, @sqlstate75 = returned_sqlstate, @DB2_PARTITION_NUMBER75 = DB2_PARTITION_NUMBER;
    get diagnostics condition 76 @db2_row_number76 = db2_row_number, @sqlstate76 = returned_sqlstate, @DB2_PARTITION_NUMBER76 = DB2_PARTITION_NUMBER;
    get diagnostics condition 77 @db2_row_number77 = db2_row_number, @sqlstate77 = returned_sqlstate, @DB2_PARTITION_NUMBER77 = DB2_PARTITION_NUMBER;
    get diagnostics condition 78 @db2_row_number78 = db2_row_number, @sqlstate78 = returned_sqlstate, @DB2_PARTITION_NUMBER78 = DB2_PARTITION_NUMBER;
    get diagnostics condition 79 @db2_row_number79 = db2_row_number, @sqlstate79 = returned_sqlstate, @DB2_PARTITION_NUMBER79 = DB2_PARTITION_NUMBER;
    get diagnostics condition 80 @db2_row_number80 = db2_row_number, @sqlstate80 = returned_sqlstate, @DB2_PARTITION_NUMBER80 = DB2_PARTITION_NUMBER;
    get diagnostics condition 81 @db2_row_number81 = db2_row_number, @sqlstate81 = returned_sqlstate, @DB2_PARTITION_NUMBER81 = DB2_PARTITION_NUMBER;
    get diagnostics condition 82 @db2_row_number82 = db2_row_number, @sqlstate82 = returned_sqlstate, @DB2_PARTITION_NUMBER82 = DB2_PARTITION_NUMBER;
    get diagnostics condition 83 @db2_row_number83 = db2_row_number, @sqlstate83 = returned_sqlstate, @DB2_PARTITION_NUMBER83 = DB2_PARTITION_NUMBER;
    get diagnostics condition 84 @db2_row_number84 = db2_row_number, @sqlstate84 = returned_sqlstate, @DB2_PARTITION_NUMBER84 = DB2_PARTITION_NUMBER;
    get diagnostics condition 85 @db2_row_number85 = db2_row_number, @sqlstate85 = returned_sqlstate, @DB2_PARTITION_NUMBER85 = DB2_PARTITION_NUMBER;
    get diagnostics condition 86 @db2_row_number86 = db2_row_number, @sqlstate86 = returned_sqlstate, @DB2_PARTITION_NUMBER86 = DB2_PARTITION_NUMBER;
    get diagnostics condition 87 @db2_row_number87 = db2_row_number, @sqlstate87 = returned_sqlstate, @DB2_PARTITION_NUMBER87 = DB2_PARTITION_NUMBER;
    get diagnostics condition 88 @db2_row_number88 = db2_row_number, @sqlstate88 = returned_sqlstate, @DB2_PARTITION_NUMBER88 = DB2_PARTITION_NUMBER;
    get diagnostics condition 89 @db2_row_number89 = db2_row_number, @sqlstate89 = returned_sqlstate, @DB2_PARTITION_NUMBER89 = DB2_PARTITION_NUMBER;
    get diagnostics condition 90 @db2_row_number90 = db2_row_number, @sqlstate90 = returned_sqlstate, @DB2_PARTITION_NUMBER90 = DB2_PARTITION_NUMBER;
    get diagnostics condition 91 @db2_row_number91 = db2_row_number, @sqlstate91 = returned_sqlstate, @DB2_PARTITION_NUMBER91 = DB2_PARTITION_NUMBER;
    get diagnostics condition 92 @db2_row_number92 = db2_row_number, @sqlstate92 = returned_sqlstate, @DB2_PARTITION_NUMBER92 = DB2_PARTITION_NUMBER;
    get diagnostics condition 93 @db2_row_number93 = db2_row_number, @sqlstate93 = returned_sqlstate, @DB2_PARTITION_NUMBER93 = DB2_PARTITION_NUMBER;
    get diagnostics condition 94 @db2_row_number94 = db2_row_number, @sqlstate94 = returned_sqlstate, @DB2_PARTITION_NUMBER94 = DB2_PARTITION_NUMBER;
    get diagnostics condition 95 @db2_row_number95 = db2_row_number, @sqlstate95 = returned_sqlstate, @DB2_PARTITION_NUMBER95 = DB2_PARTITION_NUMBER;
    get diagnostics condition 96 @db2_row_number96 = db2_row_number, @sqlstate96 = returned_sqlstate, @DB2_PARTITION_NUMBER96 = DB2_PARTITION_NUMBER;
    get diagnostics condition 97 @db2_row_number97 = db2_row_number, @sqlstate97 = returned_sqlstate, @DB2_PARTITION_NUMBER97 = DB2_PARTITION_NUMBER;
    get diagnostics condition 98 @db2_row_number98 = db2_row_number, @sqlstate98 = returned_sqlstate, @DB2_PARTITION_NUMBER98 = DB2_PARTITION_NUMBER;
    get diagnostics condition 99 @db2_row_number99 = db2_row_number, @sqlstate99 = returned_sqlstate, @DB2_PARTITION_NUMBER99 = DB2_PARTITION_NUMBER;
    get diagnostics condition 100 @db2_row_number100 = db2_row_number, @sqlstate100 = returned_sqlstate, @DB2_PARTITION_NUMBER100 = DB2_PARTITION_NUMBER;
  
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number1 , @sqlstate1 , @DB2_PARTITION_NUMBER1 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number2 , @sqlstate2 , @DB2_PARTITION_NUMBER2 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number3 , @sqlstate3 , @DB2_PARTITION_NUMBER3 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number4 , @sqlstate4 , @DB2_PARTITION_NUMBER4 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number5 , @sqlstate5 , @DB2_PARTITION_NUMBER5 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number6 , @sqlstate6 , @DB2_PARTITION_NUMBER6 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number7 , @sqlstate7 , @DB2_PARTITION_NUMBER7 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number8 , @sqlstate8 , @DB2_PARTITION_NUMBER8 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number9 , @sqlstate9 , @DB2_PARTITION_NUMBER9 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number10 , @sqlstate10 , @DB2_PARTITION_NUMBER10 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number11 , @sqlstate11 , @DB2_PARTITION_NUMBER11 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number12 , @sqlstate12 , @DB2_PARTITION_NUMBER12 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number13 , @sqlstate13 , @DB2_PARTITION_NUMBER13 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number14 , @sqlstate14 , @DB2_PARTITION_NUMBER14 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number15 , @sqlstate15 , @DB2_PARTITION_NUMBER15 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number16 , @sqlstate16 , @DB2_PARTITION_NUMBER16 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number17 , @sqlstate17 , @DB2_PARTITION_NUMBER17 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number18 , @sqlstate18 , @DB2_PARTITION_NUMBER18 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number19 , @sqlstate19 , @DB2_PARTITION_NUMBER19 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number20 , @sqlstate20 , @DB2_PARTITION_NUMBER20 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number21 , @sqlstate21 , @DB2_PARTITION_NUMBER21 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number22 , @sqlstate22 , @DB2_PARTITION_NUMBER22 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number23 , @sqlstate23 , @DB2_PARTITION_NUMBER23 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number24 , @sqlstate24 , @DB2_PARTITION_NUMBER24 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number25 , @sqlstate25 , @DB2_PARTITION_NUMBER25 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number26 , @sqlstate26 , @DB2_PARTITION_NUMBER26 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number27 , @sqlstate27 , @DB2_PARTITION_NUMBER27 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number28 , @sqlstate28 , @DB2_PARTITION_NUMBER28 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number29 , @sqlstate29 , @DB2_PARTITION_NUMBER29 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number30 , @sqlstate30 , @DB2_PARTITION_NUMBER30 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number31 , @sqlstate31 , @DB2_PARTITION_NUMBER31 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number32 , @sqlstate32 , @DB2_PARTITION_NUMBER32 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number33 , @sqlstate33 , @DB2_PARTITION_NUMBER33 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number34 , @sqlstate34 , @DB2_PARTITION_NUMBER34 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number35 , @sqlstate35 , @DB2_PARTITION_NUMBER35 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number36 , @sqlstate36 , @DB2_PARTITION_NUMBER36 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number37 , @sqlstate37 , @DB2_PARTITION_NUMBER37 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number38 , @sqlstate38 , @DB2_PARTITION_NUMBER38 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number39 , @sqlstate39 , @DB2_PARTITION_NUMBER39 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number40 , @sqlstate40 , @DB2_PARTITION_NUMBER40 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number41 , @sqlstate41 , @DB2_PARTITION_NUMBER41 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number42 , @sqlstate42 , @DB2_PARTITION_NUMBER42 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number43 , @sqlstate43 , @DB2_PARTITION_NUMBER43 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number44 , @sqlstate44 , @DB2_PARTITION_NUMBER44 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number45 , @sqlstate45 , @DB2_PARTITION_NUMBER45 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number46 , @sqlstate46 , @DB2_PARTITION_NUMBER46 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number47 , @sqlstate47 , @DB2_PARTITION_NUMBER47 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number48 , @sqlstate48 , @DB2_PARTITION_NUMBER48 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number49 , @sqlstate49 , @DB2_PARTITION_NUMBER49 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number50 , @sqlstate50 , @DB2_PARTITION_NUMBER50 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number51 , @sqlstate51 , @DB2_PARTITION_NUMBER51 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number52 , @sqlstate52 , @DB2_PARTITION_NUMBER52 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number53 , @sqlstate53 , @DB2_PARTITION_NUMBER53 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number54 , @sqlstate54 , @DB2_PARTITION_NUMBER54 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number55 , @sqlstate55 , @DB2_PARTITION_NUMBER55 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number56 , @sqlstate56 , @DB2_PARTITION_NUMBER56 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number57 , @sqlstate57 , @DB2_PARTITION_NUMBER57 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number58 , @sqlstate58 , @DB2_PARTITION_NUMBER58 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number59 , @sqlstate59 , @DB2_PARTITION_NUMBER59 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number60 , @sqlstate60 , @DB2_PARTITION_NUMBER60 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number61 , @sqlstate61 , @DB2_PARTITION_NUMBER61 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number62 , @sqlstate62 , @DB2_PARTITION_NUMBER62 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number63 , @sqlstate63 , @DB2_PARTITION_NUMBER63 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number64 , @sqlstate64 , @DB2_PARTITION_NUMBER64 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number65 , @sqlstate65 , @DB2_PARTITION_NUMBER65 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number66 , @sqlstate66 , @DB2_PARTITION_NUMBER66 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number67 , @sqlstate67 , @DB2_PARTITION_NUMBER67 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number68 , @sqlstate68 , @DB2_PARTITION_NUMBER68 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number69 , @sqlstate69 , @DB2_PARTITION_NUMBER69 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number70 , @sqlstate70 , @DB2_PARTITION_NUMBER70 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number71 , @sqlstate71 , @DB2_PARTITION_NUMBER71 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number72 , @sqlstate72 , @DB2_PARTITION_NUMBER72 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number73 , @sqlstate73 , @DB2_PARTITION_NUMBER73 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number74 , @sqlstate74 , @DB2_PARTITION_NUMBER74 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number75 , @sqlstate75 , @DB2_PARTITION_NUMBER75 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number76 , @sqlstate76 , @DB2_PARTITION_NUMBER76 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number77 , @sqlstate77 , @DB2_PARTITION_NUMBER77 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number78 , @sqlstate78 , @DB2_PARTITION_NUMBER78 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number79 , @sqlstate79 , @DB2_PARTITION_NUMBER79 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number80 , @sqlstate80 , @DB2_PARTITION_NUMBER80 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number81 , @sqlstate81 , @DB2_PARTITION_NUMBER81 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number82 , @sqlstate82 , @DB2_PARTITION_NUMBER82 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number83 , @sqlstate83 , @DB2_PARTITION_NUMBER83 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number84 , @sqlstate84 , @DB2_PARTITION_NUMBER84 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number85 , @sqlstate85 , @DB2_PARTITION_NUMBER85 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number86 , @sqlstate86 , @DB2_PARTITION_NUMBER86 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number87 , @sqlstate87 , @DB2_PARTITION_NUMBER87 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number88 , @sqlstate88 , @DB2_PARTITION_NUMBER88 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number89 , @sqlstate89 , @DB2_PARTITION_NUMBER89 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number90 , @sqlstate90 , @DB2_PARTITION_NUMBER90 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number91 , @sqlstate91 , @DB2_PARTITION_NUMBER91 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number92 , @sqlstate92 , @DB2_PARTITION_NUMBER92 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number93 , @sqlstate93 , @DB2_PARTITION_NUMBER93 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number94 , @sqlstate94 , @DB2_PARTITION_NUMBER94 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number95 , @sqlstate95 , @DB2_PARTITION_NUMBER95 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number96 , @sqlstate96 , @DB2_PARTITION_NUMBER96 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number97 , @sqlstate97 , @DB2_PARTITION_NUMBER97 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number98 , @sqlstate98 , @DB2_PARTITION_NUMBER98 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number99 , @sqlstate99 , @DB2_PARTITION_NUMBER99 );
    insert into mergeit.merge_result_conds(  @db2_row_number, @sqlstate,@DB2_PARTITION_NUMBER )  values (@db2_row_number100 , @sqlstate100 , @DB2_PARTITION_NUMBER100 );
 
end;




--  category:  Data Manipulation Language (DML)
--  description:  Merge into Table

MERGE INTO t1 USING 
  (SELECT id, c2 FROM t2) x ON 
     t1.id = x.id 
  WHEN NOT MATCHED THEN INSERT VALUES (id, c2) 
  WHEN MATCHED THEN UPDATE SET c2 = x.c2;


--  category:  Data Manipulation Language (DML)
--  description:  Select All From Table

SELECT * FROM QSYS2.SYSTABLES;


--  category:  Data Manipulation Language (DML)
--  description:  Select All from Table with Where Clause

SELECT * FROM QSYS2.SYSTABLES WHERE TABLE_NAME LIKE 'FILE%';


--  category:  Data Manipulation Language (DML)
--  description:  Select Table Schema and Group By

SELECT TABLE_SCHEMA, COUNT(*) AS "COUNT" FROM QSYS2.SYSTABLES GROUP BY TABLE_SCHEMA ORDER BY "COUNT" DESC;


--  category:  Data Manipulation Language (DML)
--  description:  Truncate Table Continue Identity

TRUNCATE table1 CONTINUE IDENTITY;


--  category:  Data Manipulation Language (DML)
--  description:  Truncate Table Ignoring Delete Triggers

TRUNCATE table1 IGNORE DELETE TRIGGERS;


--  category:  Data Manipulation Language (DML)
--  description:  Truncate Table Restart Identity Immediate

TRUNCATE table1 RESTART IDENTITY IMMEDIATE;


--  category:  Data Manipulation Language (DML)
--  description:  Update Column in Table

UPDATE table1 SET column1 = 0 WHERE column1 < 0;


--  category:  Data Manipulation Language (DML)
--  description:  Update Columns in Table with Columns from another Table

UPDATE table1 SET (column1, column2) = (SELECT column1, column2 FROM table2 WHERE table1.column3 = column3);


--  category:  Data Manipulation Language (DML)
--  description:  Update Row in Table

UPDATE table1 SET ROW = (column1, ' ', column3);


--  category:  Data Manipulation Language (DML)
--  description:  Use FOR UPDATE to launch Edit Table

CALL qsys.create_sql_sample('BUSINESS_NAME');

-- Normal query - read only
SELECT *
   FROM business_name.sales;

-- Edit Table mode in ACS
SELECT *
   FROM business_name.sales
   FOR UPDATE;




--  category:  Data Control Language (DCL)
--  description:  Alter Mask Disable
--  minvrm:  v7r2m0

ALTER MASK SSN_MASK DISABLE;


--  category:  Data Control Language (DCL)
--  description:  Alter Mask Enable
--  minvrm:  v7r2m0

ALTER MASK SSN_MASK ENABLE;


--  category:  Data Control Language (DCL)
--  description:  Alter Mask Regenerate
--  minvrm:  v7r2m0

ALTER MASK SSN_MASK REGENERATE;


--  category:  Data Control Language (DCL)
--  description:  Alter Permission Row Access Disable
--  minvrm:  v7r2m0

ALTER PERMISSION NETHMO.ROW_ACCESS DISABLE;


--  category:  Data Control Language (DCL)
--  description:  Alter Permission Row Access Enable
--  minvrm:  v7r2m0

ALTER PERMISSION NETHMO.ROW_ACCESS ENABLE;


--  category:  Data Control Language (DCL)
--  description:  Alter Permission Row Access Regenerate
--  minvrm:  v7r2m0

ALTER PERMISSION NETHMO.ROW_ACCESS REGENERATE;


--  category:  Data Control Language (DCL)
--  description:  Alter Table Activate Column Access Control
--  minvrm:  v7r2m0

ALTER TABLE EMPLOYEE ACTIVATE COLUMN ACCESS CONTROL;


--  category:  Data Control Language (DCL)
--  description:  Alter Table Activate Row Access Control
--  minvrm:  v7r2m0

ALTER TABLE HOSPITAL.PATIENT ACTIVATE ROW ACCESS CONTROL;


--  category:  Data Control Language (DCL)
--  description:  Create or Replace Mask
--  minvrm:  v7r2m0

CREATE OR REPLACE MASK SSN_MASK ON EMPLOYEE FOR COLUMN SSN RETURN
CASE
    WHEN (VERIFY_GROUP_FOR_USER(SESSION_USER, 'PAYROLL') = 1) THEN SSN
    WHEN (VERIFY_GROUP_FOR_USER(SESSION_USER, 'MGR') = 1) THEN 'XXX-XX-' CONCAT SUBSTR(SSN, 8, 4)
    ELSE NULL
END ENABLE;


--  category:  Data Control Language (DCL)
--  description:  Create or Replace Permission
--  minvrm:  v7r2m0

CREATE OR REPLACE PERMISSION NETHMO.ROW_ACCESS ON HOSPITAL.PATIENT FOR ROWS WHERE (VERIFY_GROUP_FOR_USER(
        SESSION_USER, 'PATIENT') = 1 AND HOSPITAL.PATIENT.USERID = SESSION_USER) OR (VERIFY_GROUP_FOR_USER(
        SESSION_USER, 'PCP') = 1 AND HOSPITAL.PATIENT.PCP_ID = SESSION_USER) OR (VERIFY_GROUP_FOR_USER(
        SESSION_USER, 'MEMBERSHIP') = 1 OR VERIFY_GROUP_FOR_USER(SESSION_USER, 'ACCOUNTING') = 1 OR
    VERIFY_GROUP_FOR_USER(SESSION_USER, 'DRUG_RESEARCH') = 1) ENFORCED FOR ALL ACCESS ENABLE;


--  category:  Data Control Language (DCL)
--  description:  Grant Alter, Index on Table to Public

GRANT ALTER, INDEX ON table3 TO PUBLIC;


--  category:  Data Control Language (DCL)
--  description:  Grant Select, Delete, Insert, Update on Table to Public with Grant Option

GRANT SELECT, DELETE, INSERT, UPDATE ON TABLE table3 TO PUBLIC WITH GRANT OPTION;


--  category:  Data Control Language (DCL)
--  description:  Grant Update Column to Public

GRANT UPDATE (column1) ON table2 TO PUBLIC;


--  category:  Data Control Language (DCL)
--  description:  Grant all Privileges to Public

GRANT ALL PRIVILEGES ON table3 TO PUBLIC;


--  category:  Data Control Language (DCL)
--  description:  Revoke Alter, Index on Table From Public

REVOKE ALTER, INDEX on table3 FROM PUBLIC;


--  category:  Data Control Language (DCL)
--  description:  Revoke Select, Delete, Insert, Update On Table From Public

REVOKE SELECT, DELETE, INSERT, UPDATE ON TABLE table3 FROM PUBLIC;


--  category:  Data Control Language (DCL)
--  description:  Revoke Update Column from Public

REVOKE UPDATE (column1) ON table2 FROM PUBLIC;


--  category:  Data Control Language (DCL)
--  description:  Revoke all Privileges from Public

REVOKE ALL PRIVILEGES ON table3 FROM PUBLIC;




--  category:  Routine (Function or Procedure) Statements
--  description:  Alter Procedure

ALTER PROCEDURE procedure2 (INTEGER) REPLACE (INOUT parameter1 INTEGER, IN parameter2 INTEGER) MODIFIES SQL DATA
BEGIN
    DECLARE variable1 DECIMAL(5, 2);
    SELECT column1
        INTO variable1
        FROM table1
        WHERE column1 = parameter1;
    IF variable1 > parameter2 THEN
        INSERT INTO table2
            VALUES (100);
    END IF;
END;


--  category:  Routine (Function or Procedure) Statements
--  description:  Comment on Parameter for Procedure

COMMENT ON PARAMETER procedure1 (parameter1  IS 'comment', parameter2 IS 'comment');


--  category:  Routine (Function or Procedure) Statements
--  description:  Comment on Procedure

COMMENT ON PROCEDURE procedure1 IS 'comment';


--  category:  Routine (Function or Procedure) Statements
--  description:  Create Procedure Language C Modifies SQL

CREATE PROCEDURE xmlp1 (IN p1 XML AS CLOB(100) CCSID 1208, OUT p2 XML AS CLOB(100) CCSID 1208)
        LANGUAGE C
        EXTERNAL NAME lib.xmlp1
        MODIFIES SQL DATA
        SIMPLE CALL WITH NULLS;


--  category:  Routine (Function or Procedure) Statements
--  description:  Create XML Variable

CREATE VARIABLE gxml1 XML;


--  category:  Routine (Function or Procedure) Statements
--  description:  Create or Replace Function Language C

CREATE OR REPLACE FUNCTION function1 (parameter1 INTEGER) RETURNS INTEGER LANGUAGE C EXTERNAL NAME 'lib1/pgm1(entryname)' PARAMETER STYLE GENERAL;


--  category:  Routine (Function or Procedure) Statements
--  description:  Create or Replace Function Language SQL

CREATE OR REPLACE FUNCTION function2 (
            parameter1 INTEGER
    )
    RETURNS INTEGER
    LANGUAGE SQL
    BEGIN
        DECLARE variable1 DECIMAL(5, 2);
        SELECT c1
            INTO variable1
            FROM table1
            WHERE column1 = parameter1;
        RETURN variable1;
    END;


--  category:  Routine (Function or Procedure) Statements
--  description:  Create or Replace Procedure Language C

CREATE OR REPLACE PROCEDURE procedure1 (INOUT parameter1 INTEGER) LANGUAGE C EXTERNAL PARAMETER STYLE GENERAL;


--  category:  Routine (Function or Procedure) Statements
--  description:  Create or Replace Procedure Language C External Name

CREATE OR REPLACE PROCEDURE procedure2 (INOUT parameter1 INTEGER) LANGUAGE C EXTERNAL NAME 'lib1/srvpgm1(entryname)' PARAMETER STYLE GENERAL;


--  category:  Routine (Function or Procedure) Statements
--  description:  Create or Replace Procedure Language SQL

CREATE OR REPLACE PROCEDURE procedure2 (INOUT parameter1 INTEGER)
        LANGUAGE SQL
BEGIN
    DECLARE variable1 DECIMAL(5, 2);
    SELECT column1
        INTO variable1
        FROM table1
        WHERE column1 = parameter1;
    IF variable1 > 5 THEN
        INSERT INTO table2
            VALUES (100);
    END IF;
END;


--  category:  Routine (Function or Procedure) Statements
--  description:  Drop Function

DROP FUNCTION function1;


--  category:  Routine (Function or Procedure) Statements
--  description:  Drop Procedure

DROP PROCEDURE procedure1;


--  category:  Routine (Function or Procedure) Statements
--  description:  Dynamic Compound statement

BEGIN
   DECLARE already_exists SMALLINT DEFAULT 0;
   DECLARE dup_object_hdlr CONDITION FOR SQLSTATE '42710';
   DECLARE CONTINUE HANDLER FOR dup_object_hdlr
      SET already_exists = 1;
   CREATE TABLE table1(col1 INT);
   IF already_exists > 0
   THEN
      DELETE FROM table1;
   END IF;
END;


--  category:  Routine (Function or Procedure) Statements
--  description:  Grant Execute on Procedure

GRANT EXECUTE ON PROCEDURE procedure1 TO PUBLIC;


--  category:  Routine (Function or Procedure) Statements
--  description:  Revoke Execute on Procedure

REVOKE EXECUTE ON SPECIFIC PROCEDURE specific1 FROM PUBLIC;


--  category:  Routine (Function or Procedure) Statements
--  description:  Set Variable to Parse XML

SET gxml1 = XMLPARSE(DOCUMENT '<run/>');



--  category:  Special Registers
--  description:  Select  Decimal Float Rounding Mode

SELECT CURRENT DECFLOAT ROUNDING MODE FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select  Decimal Float Rounding Mode

SELECT CURRENT DECFLOAT ROUNDING MODE FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select  Implicit XML Parse option

VALUES( CURRENT IMPLICIT XMLPARSE OPTION );


--  category:  Special Registers
--  description:  Select Client Special Registers

SELECT CLIENT APPLNAME   , 
       CLIENT ACCTNG     ,
       CLIENT PROGRAMID  , 
       CLIENT USERID     , 
       CLIENT WRKSTNNAME   
FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Date

SELECT CURRENT_DATE FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Debug Mode

SELECT CURRENT DEBUG MODE FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Degree

SELECT CURRENT DEGREE FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Path

SELECT CURRENT_PATH FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Schema

SELECT CURRENT SCHEMA FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Server

SELECT CURRENT SERVER FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Time

SELECT CURRENT_TIME FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Time Zone

SELECT CURRENT TIMEZONE FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current Timestamp

SELECT CURRENT_TIMESTAMP FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select Current User

VALUES(CURRENT USER);


--  category:  Special Registers
--  description:  Select Session User

SELECT SESSION_USER FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select System User

SELECT SYSTEM_USER FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select User

SELECT USER FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Select maximum precision Current Timestamp
--  minvrm:  v7r2m0

SELECT CURRENT_TIMESTAMP(12) FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Set Decfloat Rounding to Round Half Even

SET CURRENT DECFLOAT ROUNDING MODE = ROUND_HALF_EVEN;


--  category:  Special Registers
--  description:  Set Degree to 5

SET CURRENT DEGREE = '5';


--  category:  Special Registers
--  description:  Set Degree to Any

SET CURRENT DEGREE = 'ANY';


--  category:  Special Registers
--  description:  Set Degree to Default

SET CURRENT DEGREE = DEFAULT;


--  category:  Special Registers
--  description:  Set Path

SET PATH = MYSCHEMA, SYSTEM PATH;


--  category:  Special Registers
--  description:  Set Session Authorization to JOEUSER

SET SESSION AUTHORIZATION ='JOEUSER';


--  category:  Special Registers
--  description:  Set client special registers

CALL SYSPROC.WLM_SET_CLIENT_INFO(
    'db2user', 
    'machine.rchland.ibm.com', 
    'Auditor', 
    'Accounting department', 
    'AUTOMATIC' );

SELECT 
UPPER(CURRENT CLIENT_USERID) , 
CURRENT CLIENT_WRKSTNNAME , 
CURRENT CLIENT_APPLNAME , 
CURRENT CLIENT_ACCTNG , 
CURRENT CLIENT_PROGRAMID 
FROM SYSIBM.SYSDUMMY1;

-- Selectively change a subset of registers
CALL SYSPROC.WLM_SET_CLIENT_INFO(
    CLIENT_PROGRAMID => 'Warehouse Extraction Process - V2.4' 
 );

SELECT 
UPPER(CURRENT CLIENT_USERID) , 
CURRENT CLIENT_WRKSTNNAME , 
CURRENT CLIENT_APPLNAME , 
CURRENT CLIENT_ACCTNG , 
CURRENT CLIENT_PROGRAMID 
FROM SYSIBM.SYSDUMMY1;


--  category:  Special Registers
--  description:  Set current schema

SET SCHEMA = MYSCHEMA;


--  category:  Special Registers
--  description:  Set the system time to one hour in the past
--  minvrm:  v7r3m0

SET CURRENT TEMPORAL SYSTEM_TIME = current timestamp - 1 hour;




--  category:  Built-in Global Variables
--  description:  Client Host
--  minvrm:  v7r2m0

VALUES(SYSIBM.CLIENT_HOST);


--  category:  Built-in Global Variables
--  description:  Client IP Address
--  minvrm:  v7r2m0

VALUES(SYSIBM.CLIENT_IPADDR);


--  category:  Built-in Global Variables
--  description:  Client Port
--  minvrm:  v7r2m0

VALUES(SYSIBM.CLIENT_PORT);


--  category:  Built-in Global Variables
--  description:  Job Name
--  minvrm:  v7r2m0

VALUES(QSYS2.JOB_NAME);


--  category:  Built-in Global Variables
--  description:  Package Name
--  minvrm:  v7r2m0

VALUES(SYSIBM.PACKAGE_NAME);


--  category:  Built-in Global Variables
--  description:  Package Schema
--  minvrm:  v7r2m0

VALUES(SYSIBM.PACKAGE_SCHEMA);


--  category:  Built-in Global Variables
--  description:  Package Version
--  minvrm:  v7r2m0

VALUES(SYSIBM.PACKAGE_VERSION);


--  category:  Built-in Global Variables
--  description:  Process Identifier
--  minvrm:  v7r2m0

VALUES(QSYS2.PROCESS_ID);


--  category:  Built-in Global Variables
--  description:  Routine Schema
--  minvrm:  v7r2m0

VALUES(SYSIBM.ROUTINE_SCHEMA);


--  category:  Built-in Global Variables
--  description:  Routine Specific Name
--  minvrm:  v7r2m0

VALUES(SYSIBM.ROUTINE_SPECIFIC_NAME);


--  category:  Built-in Global Variables
--  description:  Routine Type
--  minvrm:  v7r2m0

VALUES(SYSIBM.ROUTINE_TYPE);


--  category:  Built-in Global Variables
--  description:  Server Mode Job Name
--  minvrm:  v7r2m0

VALUES(QSYS2.SERVER_MODE_JOB_NAME);


--  category:  Built-in Global Variables
--  description:  Thread Identifier

VALUES(QSYS2.THREAD_ID);




--  category:  Miscellaneous
--  description:  CL ADDRPYLE 

CL: ADDRPYLE SEQNBR(3333) MSGID(CPA32B2) RPY(I);


--  category:  Miscellaneous
--  description:  CL ADDRPYLE CMPDTA(table)

CL: ADDRPYLE SEQNBR(3333) MSGID(CPA32B2) CMPDTA(table1 1) RPY(I);


--  category:  Miscellaneous
--  description:  CL: CHGJOB INQMSGRPY(*DFT)

CL: CHGJOB INQMSGRPY(*DFT);


--  category:  Miscellaneous
--  description:  CL: CHGJOB INQMSGRPY(*SYSRPYL)

CL: CHGJOB INQMSGRPY(*SYSRPYL);


--  category:  Miscellaneous
--  description:  CL: RMVRPYLE SEQNBR(3333)

CL: RMVRPYLE SEQNBR(3333);


--  category:  Miscellaneous
--  description:  Call Create SQL Sample with Schema

CALL QSYS.CREATE_SQL_SAMPLE('SCHEMA-NAME');


--  category:  Miscellaneous
--  description:  Call QCMDEXC with schema

CALL QSYS2.QCMDEXC('addlible schema1');


--  category:  Miscellaneous
--  description:  Declare Global Temporary Table

DECLARE GLOBAL TEMPORARY TABLE TEMPTAB1 LIKE USER1.EMPTAB INCLUDING IDENTITY ON COMMIT PRESERVE ROWS;


--  category:  Miscellaneous
--  description:  Declare Global Temporary Table Session

DECLARE GLOBAL TEMPORARY TABLE SESSION.TEMP_EMP (EMPNO CHAR(6) NOT NULL, SALARY DECIMAL(9, 2), BONUS DECIMAL(9, 2), COMM DECIMAL(9, 2)) ON COMMIT PRESERVE ROWS;


--  category:  Miscellaneous
--  description:  Drop a schema without the CPA7025 inquiry messages
--  minvrm:  v7r3m0

DROP SCHEMA TOYSTORE CASCADE;


--  category:  Miscellaneous
--  description:  Lock Table in Exclusive Mode

LOCK TABLE table1 IN EXCLUSIVE MODE;


--  category:  Miscellaneous
--  description:  Lock Table in Exclusive Mode Allow Read

LOCK TABLE table1 IN EXCLUSIVE MODE ALLOW READ;


--  category:  Miscellaneous
--  description:  Lock Table in Share Mode

LOCK TABLE table1 IN SHARE MODE;


--  category:  Miscellaneous
--  description:  Review ACS function usage configuration

-- 
--  Note: Here is the default configuration
--
--  Function ID              Default Usage
--  -----------              -------------
--  QIBM_DB_SQLADM           DENIED
--  QIBM_DB_SYSMON           DENIED
--  QIBM_DB_SECADM           DENIED
--  QIBM_DB_DDMDRDA          ALLOWED
--  QIBM_DB_ZDA              ALLOWED
--  QIBM_XE1_OPNAV_DBNAV     ALLOWED
--  QIBM_XE1_OPNAV_DBSQLPM   ALLOWED
--  QIBM_XE1_OPNAV_DBSQLPCS  ALLOWED
--  QIBM_XE1_OPNAV_DBXACT    ALLOWED
SELECT function_id,
       default_usage,
       f.*
   FROM qsys2.function_info f
   WHERE function_id LIKE 'QIBM_DB_%' OR
         function_id LIKE 'QIBM_XE1_OPNAV_DB_%';


--  category:  Miscellaneous
--  description:  Set Path to *LIBL

SET PATH = *LIBL;


--  category:  Miscellaneous
--  description:  Set Path to schemas

SET PATH = schema1, schema2;




--  category:  IBM i Services
--  description:  Application - Bound Module - Optimization level detail

--
--  Are we taking advantage of ILE optimization?
--
select optimization_level, count(*) as optimization_level_count
  from qsys2.bound_module_info
  where program_library = 'APPLIB'
  group by optimization_level
  order by 2 desc;


--  category:  IBM i Services
--  description:  Application - Bound Module - What's not built from IFS source?

--
--  Which modules are not being built with source residing in the IFS?
--
select *
  from qsys2.bound_module_info
  where program_library = 'QGPL'
        and source_file_library not in ('QTEMP')
        and source_stream_file_path is null
  order by source_file_library, source_file, source_file_member desc;


--  category:  IBM i Services
--  description:  Application - Bound SRVPGM - Deferred Activation

--
--  Are we using deferred service program activation?
--
select bound_service_program_activation, count(*) as bound_service_program_activation_count
  from qsys2.BOUND_SRVPGM_INFO
  where program_library = 'APPLIB'
  group by bound_service_program_activation
  order by 2 desc;


--  category:  IBM i Services
--  description:  Application - Command Information
--  minvrm: V7R4M0

--
-- Which commands are available to limited capabilities users?
--
select *
  from qsys2.command_info
  where allow_limited_user = 'YES';
stop;


--
-- Who are these users with limited capabilties?
--
select *
  from qsys2.user_info
  where LIMIT_CAPABILITIES = '*YES';
stop;
  


--  category:  IBM i Services
--  description:  Application - Data Queue Entries
--

--
-- Data queue example
--
create schema TheQueen;
cl:CRTDTAQ DTAQ(TheQueen/OrderDQ) MAXLEN(100) SEQ(*KEYED) KEYLEN(3);
call qsys2.send_data_queue(message_data       => 'Sue - Dilly Bar',
                           data_queue         => 'ORDERDQ', 
                           data_queue_library => 'THEQUEEN',
                           key_data           => '010');
call qsys2.send_data_queue(message_data       => 'Sarah - Ice cream cake!',
                           data_queue         => 'ORDERDQ', 
                           data_queue_library => 'THEQUEEN',
                           key_data           => '020');
call qsys2.send_data_queue(message_data       => 'Scott - Strawberry Sundae',
                           data_queue         => 'ORDERDQ', 
                           data_queue_library => 'THEQUEEN',
                           key_data           => '030');
call qsys2.send_data_queue(message_data       => 'Scott - Pineapple Shake',
                           data_queue         => 'ORDERDQ', 
                           data_queue_library => 'THEQUEEN',
                           key_data           => '030');
stop;

-- Search what's on the DQ
select message_data, key_data from table
     (qsys2.data_queue_entries('ORDERDQ', 'THEQUEEN', 
                               selection_type => 'KEY',
                               key_data       => '030',
                               key_order      => 'EQ'));
stop;

-- Order fulfilled!
select message_data, message_data_utf8, message_data_binary, key_data, sender_job_name, sender_current_user
  from table (
      qsys2.receive_data_queue(
        data_queue => 'ORDERDQ', data_queue_library => 'THEQUEEN', 
        remove => 'YES',
        wait_time => 0, 
        key_data => '030', 
        key_order => 'EQ')
    );
stop;

-- What remains on the queue?
select * from table
     (qsys2.data_queue_entries('ORDERDQ', 'THEQUEEN', 
                               selection_type => 'KEY',
                               key_data       => '030',
                               key_order      => 'LE'));          


--  category:  IBM i Services
--  description:  Application - Data Queues - Info and detail
--

--
-- Review data queues, by percentage filled up
--
select data_queue_library, data_queue_name, data_queue_type, 
       current_messages, maximum_messages, 
       DEC(DEC(current_messages,19,2) / DEC(maximum_messages,19,2) * 100,19,2) AS percentage_used,
       maximum_message_length, 
       "SEQUENCE", key_length,
       include_sender_id, specified_maximum_messages, initial_message_allocation,
       current_message_allocation, force, automatic_reclaim, last_reclaim_timestamp,
       enforce_data_queue_locks, text_description, remote_data_queue_library,
       remote_data_queue, remote_location, relational_database_name,
       appc_device_description, local_location, "MODE", remote_network_id
  from qsys2.data_queue_info
  order by 6 desc;



--  category:  IBM i Services
--  description:  Application - Data Queues - Keyed
--

cl:CRTDTAQ DTAQ(COOLSTUFF/KEYEDDQ) MAXLEN(64000) SEQ(*KEYED) KEYLEN(8) SENDERID(*YES) SIZE(*MAX2GB) TEXT('DQueue Time');

select *
  from qsys2.data_queue_info
  where data_queue_library = 'COOLSTUFF';
  
stop;
-- Example of how to produce a key value
values lpad(3, 8, 0);
stop;

call qsys2.send_data_queue(data_queue_library => 'COOLSTUFF',
                           data_queue => 'KEYEDDQ',
                           message_data => 'Keyed message 1',
                           key_data => lpad(1, 8, 0) );  
                           
call qsys2.send_data_queue(data_queue_library => 'COOLSTUFF',
                           data_queue => 'KEYEDDQ',
                           message_data => 'Keyed message 2',
                           key_data => lpad(2, 8, 0) );  
                           
call qsys2.send_data_queue(data_queue_library => 'COOLSTUFF',
                           data_queue => 'KEYEDDQ',
                           message_data => 'Keyed message 3',
                           key_data => lpad(3, 8, 0) );

stop;

select *
  from qsys2.data_queue_info
  where data_queue_library = 'COOLSTUFF';
                            
stop;

select *
  from table(qsys2.receive_data_queue(
               data_queue_library => 'COOLSTUFF',
               data_queue => 'KEYEDDQ',
               key_data => lpad(3, 8, 0),
               key_order => 'EQ'));


select *
  from table(qsys2.receive_data_queue(
               data_queue_library => 'COOLSTUFF',
               data_queue => 'KEYEDDQ',
               key_data => lpad(99, 8, 0),
               key_order => 'LT')); 


select *
  from table(qsys2.receive_data_queue(
               data_queue_library => 'COOLSTUFF',
               data_queue => 'KEYEDDQ',
               key_data => lpad(0, 8, 0),
               key_order => 'GT')); 
               
                  


--  category:  IBM i Services
--  description:  Application - Data Queues - Send and Receive
--

-- create a data queue
cl: crtlib coolstuff;
cl:CRTDTAQ DTAQ(COOLSTUFF/SQLCANDOIT) MAXLEN(32000) SENDERID(*YES);
stop;

-- review the state and status of the data queue
select *
  from qsys2.data_queue_info
  where data_queue_library = 'COOLSTUFF';
stop;

-- Send a (character) message to the data queue
call qsys2.send_data_queue(
  message_data       => 'Hello World... today is ' concat current date, 
  data_queue         => 'SQLCANDOIT',
  data_queue_library => 'COOLSTUFF');

stop;

-- Retrieve the message from the data queue
select *
  from table (
      qsys2.receive_data_queue(
        data_queue => 'SQLCANDOIT', data_queue_library => 'COOLSTUFF')
    );


--  category:  IBM i Services
--  description:  Application - Data Queues - UTF8 data
--

--
-- Send unicode data to the data queue
--
call qsys2.send_data_queue_utf8(
  message_data       => 'Hello World... today is ' concat current date, 
  data_queue         => 'SQLCANDOIT',
  data_queue_library => 'COOLSTUFF');

stop;

-- Retrieve the message from the data queue
select message_data_utf8
  from table (
      qsys2.receive_data_queue(
        data_queue => 'SQLCANDOIT', data_queue_library => 'COOLSTUFF')
    );


--  category:  IBM i Services
--  description:  Application - Environment variable information

--
-- Retrieve the environment variables for the
-- current connection
--
SELECT * FROM QSYS2.ENVIRONMENT_VARIABLE_INFO;


--  category:  IBM i Services
--  description:  Application - Examine my stack 

--
-- Look at my thread's stack
-- 
SELECT * FROM TABLE(QSYS2.STACK_INFO('*')) AS x
  WHERE LIC_PROCEDURE_NAME IS NULL
     ORDINAL_POSITION;

--
-- Look at all threads in my job
-- 
SELECT * FROM TABLE(QSYS2.STACK_INFO('*', 'ALL')) AS x
  WHERE LIC_PROCEDURE_NAME IS NULL
     ORDER BY THREAD_ID, ORDINAL_POSITION;



--  category:  IBM i Services
--  description:  Application - Exit Point information
--

--
-- What are the CL command exit programs?
--
select *
  from qsys2.exit_point_info
  where exit_point_name like 'QIBM_QCA_%_COMMAND%';


--  category:  IBM i Services
--  description:  Application - Exit Program information
--

--
-- What are the CL command exit programs?
--
select a.*, b.*
  from qsys2.exit_program_info a, lateral 
  (select * from table(qsys2.object_statistics(exit_program_library, '*PGM', exit_program))) b
  where exit_point_name like 'QIBM_QCA_%_COMMAND%'
  order by exit_point_name, exit_program_number;


--  category:  IBM i Services
--  description:  Application - Messages being Watched
--

--
-- What messages are being watched?
--
select a.session_id, a.status, b.message_id, b.message_type,
       b.message_queue_library, b.message_queue, b.message_job_name, b.message_job_user,
       b.message_job_number, b.message_severity, b.message_relational_operator,
       b.message_comparison_data, b.message_compare_against, b.comparison_data_ccsid
  from qsys2.watch_info a, lateral (
         select *
           from table (
               qsys2.watch_detail(session_id => a.session_id)
             )
       ) b
  where watched_message_count > 0
  order by session_id;


--  category:  IBM i Services
--  description:  Application - PASE Shell 

--
-- Set the current user's shell to BASH shipped by 5733-OPS.
--
CALL QSYS2.SET_PASE_SHELL_INFO('*CURRENT', 
                               '/QOpenSys/QIBM/ProdData/OPS/tools/bin/bash');

--
-- Set the default shell to be ksh for any users that do not have an explicit shell set.
--
CALL QSYS2.SET_PASE_SHELL_INFO('*DEFAULT', '/QOpenSys/usr/bin/ksh');

--
-- Review shell configuration
--
select authorization_name, pase_shell_path 
  from qsys2.user_info where pase_shell_path is not null;


--  category:  IBM i Services
--  description:  Application - Pending database transactions
--

select job_name, state_timestamp, user_name, t.*
  from qsys2.db_transaction_info t
  where local_changes_pending = 'YES'
  order by t.state_timestamp;


--  category:  IBM i Services
--  description:  Application - Program Export/Import
--
--
--   Alternative to: DSPSRVPGM SRVPGM(QSYS/QP0ZCPA) DETAIL(*PROCEXP) 
--
select *
  from qsys2.PROGRAM_EXPORT_IMPORT_INFO 
  where program_library = 'QSYS'    and 
        program_name    = 'QP0ZCPA' and
        object_type     = '*SRVPGM' and
        symbol_usage    = '*PROCEXP';



--  category:  IBM i Services
--  description:  Application - Program info - Activation Group analysis
--
--
--  Summarize the activation group usage
--
select activation_group, count(*) as activation_group_name_count
  from qsys2.program_info
  where program_library = 'APPLIB'
        and program_type = 'ILE'
  group by activation_group
  order by 2 desc;



--  category:  IBM i Services
--  description:  Application - Program info - Ownership Summary
--
--
--  Review adopted ownership (summary)
--
select program_owner, object_type, count(*) as application_owner_count
  from qsys2.program_info
  where program_library = 'APPLIB' and 
        user_profile = '*OWNER'
  group by program_owner, object_type
  order by 2, 3 desc;
  



--  category:  IBM i Services
--  description:  Application - QCMDEXC scalar function
--

--
-- Hold any jobs that started running an SQL statement more than 2 hours ago.
--
select JOB_NAME,
       case
         when QSYS2.QCMDEXC('HLDJOB ' concat JOB_NAME) = 1 then 'Job Held'
         else 'Job not held'
       end as HLDJOB_RESULT
  from table (
      QSYS2.ACTIVE_JOB_INFO(DETAILED_INFO => 'ALL')
    )
  where SQL_STATEMENT_START_TIMESTAMP < current timestamp - 2 hours;


--  category:  IBM i Services
--  description:  Application - Service tracker

--
-- Review all the Security related IBM i Services 
--
SELECT * FROM QSYS2.SERVICES_INFO 
   WHERE SERVICE_CATEGORY = 'SECURITY';

--
-- Find the example for top storage consumers 
--
SELECT EXAMPLE
   FROM QSYS2.SERVICES_INFO
   WHERE EXAMPLE LIKE '%top 10 storage%';


--  category:  IBM i Services
--  description:  Application - Special case Data Areas

--
-- SQL alternative to RTVDTAARA
--
-- *GDA - Group data area.
-- *LDA - Local data area.
-- *PDA - Program initialization parameter data area.
--

select data_area_value from 
  table(qsys2.data_area_info(DATA_AREA_LIBRARY => '*LIBL',
                             DATA_AREA_NAME    => '*GDA'));
                             
select data_area_value from 
  table(qsys2.data_area_info(DATA_AREA_LIBRARY => '*LIBL',
                             DATA_AREA_NAME    => '*LDA'));
                             
select data_area_value from 
  table(qsys2.data_area_info(DATA_AREA_LIBRARY => '*LIBL',
                             DATA_AREA_NAME    => '*PDA'));
                             

                             


--  category:  IBM i Services
--  description:  Application - Split an aggregated list

-- Do the opposite of LISTAGG(), break apart a list of values
SELECT ordinal_position,
       LTRIM(element) AS special_authority
   FROM qsys2.user_info u,
        TABLE (
           systools.split(input_list => special_authorities, 
                          delimiter  => '   ')
        ) b
   WHERE u.authorization_name = 'SCOTTF';
   


--  category:  IBM i Services
--  description:  Application - User Indexes (*USRIDX)
--  minvrm: V7R3M0
--
   
--
--  Review user index attributes
--
select USER_INDEX_LIBRARY, USER_INDEX, ENTRY_TYPE, ENTRY_LENGTH, MAXIMUM_ENTRY_LENGTH, INDEX_SIZE,
       IMMEDIATE_UPDATE, OPTIMIZATION, KEY_INSERTION, KEY_LENGTH, ENTRY_TOTAL, ENTRIES_ADDED,
       ENTRIES_REMOVED, TEXT_DESCRIPTION
  from qsys2.user_index_info
  order by ENTRY_TOTAL * ENTRY_LENGTH desc;


--  category:  IBM i Services
--  description:  Application - User Indexes (*USRIDX)
--  minvrm: V7R3M0

--
--  Examine the user index entries
--
select *
  from table (
      QSYS2.USER_INDEX_ENTRIES(USER_INDEX         => 'USRINDEX1', 
                               USER_INDEX_LIBRARY => 'STORE42')
    );


--  category:  IBM i Services
--  description:  Application - User Spaces (*USRSPC)
--  minvrm: V7R3M0
--
--
--  Review user space attributes
--
select USER_SPACE_LIBRARY, USER_SPACE, SIZE, EXTENDABLE, INITIAL_VALUE
  from qsys2.user_space_info
  order by size desc;
  


--  category:  IBM i Services
--  description:  Application - User Spaces (*USRSPC)
--  minvrm: V7R3M0

--
--  Examine the data within a user space
-- 
select *
  from table (
      QSYS2.USER_SPACE(USER_SPACE         => 'USRSPACE1', 
                       USER_SPACE_LIBRARY => 'STORE42')
    );
  


--  category:  IBM i Services
--  description:  Application - Watches
--

--
-- What system watches exist?
--
select session_id, origin, origin_job, start_timestamp, user_id, status,
       watch_session_type, job_run_priority, watched_message_count, watched_lic_log_count,
       watched_pal_count, watch_program_library, watch_program, watch_program_call_start,
       watch_program_call_end, time_limit, time_interval
  from qsys2.watch_info order by session_id;


--  category:  IBM i Services
--  description:  Application - Work with Data areas in QTEMP

--
-- Use SQL to work with a data area
-- 
cl:qsys/CRTDTAARA DTAARA(QTEMP/SECRET) TYPE(*CHAR) LEN(50) VALUE(SAUCE);

select * from 
  table(qsys2.data_area_info(DATA_AREA_LIBRARY => 'QTEMP',
                             DATA_AREA_NAME    => 'SECRET'));

call qsys2.qcmdexc('qsys/CHGDTAARA DTAARA(QTEMP/SECRET) VALUE(''SQL is the secret sauce'')');


select * from 
  table(qsys2.data_area_info(DATA_AREA_LIBRARY => 'QTEMP',
                             DATA_AREA_NAME    => 'SECRET'));



--  category:  IBM i Services
--  description:  Application - Work with numeric Data areas

--
-- Use SQL to extract and manipulate a numeric type data area
-- 

call qsys.create_sql_sample('TOYSTORE');

call qsys2.qcmdexc('QSYS/CRTDTAARA DTAARA(TOYSTORE/SALESLEAD) TYPE(*DEC) LEN(20 2) VALUE(0.00) TEXT(''top dog'')');

select * from qsys2.data_area_info
  where data_area_library = 'TOYSTORE';

begin
declare temp_top_dog varchar(100);

select sales into temp_top_dog from toystore.sales 
  where sales is not null 
  order by sales desc limit 1;

call qsys2.qcmdexc('qsys/CHGDTAARA DTAARA(TOYSTORE/SALESLEAD) VALUE(' concat temp_top_dog concat ')');
end;

select * from qsys2.data_area_info
  where data_area_library = 'TOYSTORE';


--  category:  IBM i Services
--  description:  Communications - Active Database Connections

-- List the active database connections for my job
select * from table(qsys2.active_db_connections(qsys2.job_name));


--  category:  IBM i Services
--  description:  Communications - Active Database Connections

-- Extract the database application server job name
select c.remote_job_name, c.connection_type, c.*
  from table (
      qsys2.active_db_connections('*')
    ) c;


--  category:  IBM i Services
--  description:  Communications - Apache Real Time Server Statistics

-- Review the HTTP Servers thread usage detail
select server_active_threads, server_idle_threads, h.*
  from qsys2.http_server_info h
  where server_name = 'ADMIN'
  order by 1 desc, 2 desc;


--  category:  IBM i Services
--  description:  Communications - Network Statistics Info (NETSTAT)

--  
-- Description: Review the connections that are transferring the most data
--
SELECT * FROM QSYS2.NETSTAT_INFO
  ORDER BY BYTES_SENT_REMOTELY + BYTES_RECEIVED_LOCALLY DESC
  LIMIT 10;



--  category:  IBM i Services
--  description:  Communications - Network Statistics Interface (NETSTAT)

--
-- The following procedure was created to help clients prepare for improved enforcement of TCP/IP configuration problems.
-- Reference: https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_73/rzaq9/rzaq9osCLtcpifc.htm

--  
-- Analyze NETSTAT Interface detail, looking for problems. 
-- The example shows how TCP/IP would be incorrectly configured and the SQL below shows how to detect that this condition exists
--

-- Example:
CL: ADDTCPIFC INTNETADR('10.1.1.1') LIND(*VIRTUALIP) SUBNETMASK('255.255.252.0');
CL: ADDTCPIFC INTNETADR('10.1.1.2') LIND(*VIRTUALIP) SUBNETMASK('255.255.252.0');
CL: ADDTCPIFC INTNETADR('10.1.1.3') LIND(ETHLINE) SUBNETMASK('255.255.255.255') PREFIFC('10.1.1.1' '10.1.1.2');

CREATE OR REPLACE PROCEDURE FIND_INTERFACE_CONFIG_PROBLEMS()
LANGUAGE SQL
DYNAMIC RESULT SETS 1
SET OPTION DBGVIEW = *SOURCE, OUTPUT = *PRINT
BEGIN
  DECLARE Pref_IP, Int_Addr, Net_Addr VARCHAR(15);
  DECLARE Pref_IP_List VARCHAR(159);
  DECLARE at_end integer default 0;
  DECLARE not_found CONDITION FOR '02000';
  DECLARE Pref_Interface_Result_Cursor CURSOR FOR
    SELECT A.* FROM SESSION.CONFIG_ISSUES A
    INNER JOIN QSYS2.NETSTAT_INTERFACE_INFO B
    ON A.PREFERRED_IP_REFERENCED_AS_A_NON_ETHERNET_INTERFACE = B.INTERNET_ADDRESS
    WHERE B.INTERFACE_LINE_TYPE <> 'ELAN' AND B.INTERFACE_LINE_TYPE <> 'VETH';
  DECLARE PreferredIP_Cursor CURSOR FOR SELECT INTERNET_ADDRESS, NETWORK_ADDRESS, PREFERRED_INTERFACE_LIST
    FROM QSYS2.NETSTAT_INTERFACE_INFO WHERE PREFERRED_INTERFACE_LIST IS NOT NULL;
  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET at_end  = 1;
  DECLARE CONTINUE HANDLER FOR not_found    SET at_end  = 1;

  DECLARE GLOBAL TEMPORARY TABLE CONFIG_ISSUES(INTERNET_ADDRESS, NETWORK_ADDRESS, PREFERRED_IP_REFERENCED_AS_A_NON_ETHERNET_INTERFACE) AS (
  SELECT INTERNET_ADDRESS, NETWORK_ADDRESS, CAST(NULL AS VARCHAR(15)) FROM QSYS2.NETSTAT_INTERFACE_INFO)
  WITH NO DATA WITH REPLACE;

  OPEN PreferredIP_Cursor;
  FETCH FROM PreferredIP_Cursor INTO Int_Addr, Net_Addr, Pref_IP_List;
  WHILE (at_end = 0) DO
    BEGIN
      DECLARE v_loc integer;
      DECLARE v_start integer default 1;

      Pref_IP_loop: LOOP
        SET v_loc = LOCATE_IN_STRING(Pref_IP_List, ' ', v_start, 1);
        IF (v_loc = 0) THEN
          SET Pref_IP = SUBSTR(Pref_IP_List, v_start);
        ELSE
          SET Pref_IP = SUBSTR(Pref_IP_List, v_start, v_loc - v_start);
        END IF;

        INSERT INTO SESSION.CONFIG_ISSUES VALUES(Int_Addr, Net_Addr, Pref_IP);

        IF (v_loc = 0) THEN
          LEAVE Pref_IP_loop;
        END IF;
        SET v_start = v_loc + 1;
      END LOOP;
    END;
  FETCH FROM PreferredIP_Cursor INTO Int_Addr, Net_Addr, Pref_IP_List;
  END WHILE;
  CLOSE PreferredIP_Cursor;
  OPEN Pref_Interface_Result_Cursor;
END;

--
-- Look for NETSTAT interface problems. Any rows returned should be analyzed.
--
CALL FIND_INTERFACE_CONFIG_PROBLEMS();


--  category:  IBM i Services
--  description:  Communications - Network Statistics Interface (NETSTAT)

--  
-- Analyze NETSTAT Interface detail, looking for problems. 
-- The examples show how TCP/IP would be incorrectly configured and the SQL below shows how to detect that this condition exists
--

-- Example 1
CL: CRTLINETH LIND(MYETH) RSRCNAME(NOEXIST);
CL: ADDTCPIFC INTNETADR('10.1.1.1') LIND(*VIRTUALIP) SUBNETMASK('255.255.252.0');
CL: ADDTCPIFC INTNETADR('10.1.1.2') LIND(MYETH) SUBNETMASK('255.255.255.255') LCLIFC('10.1.1.1');

-- Description: Find instances where a TCP/IP interface contains an associated local interface
-- and the line description type of the interface is not set to *VIRTUALIP
SELECT * FROM QSYS2.NETSTAT_INTERFACE_INFO
WHERE ASSOCIATED_LOCAL_INTERFACE IS NOT NULL AND
      LINE_DESCRIPTION <> '*VIRTUALIP' AND
      INTERFACE_LINE_TYPE = 'ELAN';

-- Example 2
CL: ADDTCPIFC INTNETADR('10.1.1.1') LIND(ETHLINE) SUBNETMASK('255.255.255.255') PREFIFC(*AUTO);

-- Description: Find instances where a TCP/IP interface contains a preferred interface list
-- and the line description type of the interface is not set to *VIRTUALIP
-- and interface selection is performed automatically by the system
SELECT * FROM QSYS2.NETSTAT_INTERFACE_INFO
WHERE PREFERRED_INTERFACE_LIST IS NULL AND
      LINE_DESCRIPTION <> '*VIRTUALIP' AND
      PREFERRED_INTERFACE_DEFAULT_ROUTE = 'NO' AND
      PROXY_ARP_ALLOWED = 'YES' AND
      PROXY_ARP_ENABLED = 'YES';

-- Example 3
CL: CRTLINETH LIND(MYETH) RSRCNAME(NOEXIST);
CL: ADDTCPIFC INTNETADR('10.1.1.1') LIND(*VIRTUALIP) SUBNETMASK('255.255.252.0');
CL: ADDTCPIFC INTNETADR('10.1.1.2') LIND(MYETH) SUBNETMASK('255.255.255.255') PREFIFC('10.1.1.1');

-- Description: Find instances where a TCP/IP interface contains a preferred interface list
-- and the line description type of the interface is not set to *VIRTUALIP
-- and the line type of the interface is not set to Virtual Ethernet
SELECT * FROM QSYS2.NETSTAT_INTERFACE_INFO
WHERE PREFERRED_INTERFACE_LIST IS NOT NULL AND
      LINE_DESCRIPTION <> '*VIRTUALIP' AND
      INTERFACE_LINE_TYPE <> 'VETH';

-- Example 4
CL: ADDTCPIFC INTNETADR('10.1.1.1') LIND(*VIRTUALIP) SUBNETMASK('255.255.252.0');
CL: ADDTCPIFC INTNETADR('10.1.1.2') LIND(ETHLINE) SUBNETMASK('255.255.255.255') LCLIFC('10.1.1.1') PREFIFC('10.1.1.1');

-- Description: Find instances where a TCP/IP interface contains a preferred interface list
-- and an associated local interface list
SELECT * FROM QSYS2.NETSTAT_INTERFACE_INFO
WHERE PREFERRED_INTERFACE_LIST IS NOT NULL AND
      ASSOCIATED_LOCAL_INTERFACE IS NOT NULL;


--  category:  IBM i Services
--  description:  Communications - Network Statistics Job Info (NETSTAT)

--  
-- Analyze remote IP address detail for password failures
--
WITH ip_addrs(rmt_addr, rmt_count)
   AS (SELECT remote_address, COUNT(*)
          FROM TABLE(qsys2.display_journal('QSYS', 'QAUDJRN',
             journal_entry_types => 'PW', starting_timestamp => CURRENT
             TIMESTAMP - 24 HOURS)) AS x
          GROUP BY remote_address)
   SELECT i.rmt_addr, i.rmt_count, user_name, rmt_port
      FROM ip_addrs i LEFT OUTER JOIN 
      qsys2.netstat_job_info n ON i.rmt_addr = remote_address
      ORDER BY rmt_count DESC;


--  category:  IBM i Services
--  description:  Communications - Network Statistics Route Info (NETSTAT)

--  
-- Review the details of all TCP/IP routes
--
SELECT * FROM QSYS2.NETSTAT_ROUTE_INFO;


--  category:  IBM i Services
--  description:  Communications - TCP/IP Information

--
-- description: Who am I?
--
select * from qsys2.tcpip_info;

--
-- Using the well defined port #'s
-- Reference:
-- https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_73/rzaku/rzakuservertable.htm
--
CREATE OR REPLACE TRIGGER SHOESTORE.INSERT_EMPLOYEE
  BEFORE INSERT ON SHOESTORE.EMPLOYEE 
  REFERENCING NEW AS N 
  FOR EACH ROW 
  MODE DB2ROW  
  SET OPTION DBGVIEW = *SOURCE
IE : BEGIN ATOMIC 
    DECLARE V_SERVER_PORT_NUMBER INTEGER;
    --
    -- Perform extra validation for ODBC users
    --
    SET V_SERVER_PORT_NUMBER = 
      (select server_port_number from qsys2.tcpip_info);
    IF (V_SERVER_PORT_NUMBER = 8471) THEN
       SIGNAL SQLSTATE '80001' 
	 SET MESSAGE_TEXT = 'Employees cannot be added via this interface'; 
    END IF;
END IE  ; 


--  category:  IBM i Services
--  description:  Communications - Time server

-- Define a time server as the preferred time server
--
call qsys2.add_time_server(TIME_SERVER         => 'TICK.RCHLAND.IBM.COM',
                           PREFERRED_INDICATOR => 'YES');
--
-- Define a second time server in case the preferred time server is not reachable
--
call qsys2.add_time_server(TIME_SERVER         => 'TOCK.RCHLAND.IBM.COM',
                           PREFERRED_INDICATOR => 'NO');
--
-- List the time servers that have been defined
--
select * from qsys2.time_protocol_info;


--  category:  IBM i Services
--  description:  Find objects in a library, not included in an authorization list

SELECT a.objname, objdefiner, objtype, sql_object_type
 FROM TABLE(qsys2.object_statistics('TOYSTORE', 'ALL')) a
LEFT EXCEPTION JOIN LATERAL
 (SELECT system_object_name 
    FROM qsys2.authorization_list_info x 
      WHERE AUTHORIZATION_LIST = 'TOYSTOREAL') b
        ON a.objname = b.system_object_name;


--  category:  IBM i Services
--  description:  History Log - Study job longevity 

   WITH JOB_START(start_time, from_user, sbs, from_job) AS (
     SELECT message_timestamp as time, 
          from_user, 
          substr(message_tokens, 59, 10) as subsystem,
          from_job
     FROM TABLE(qsys2.history_log_info(START_TIME => CURRENT DATE,
                                       END_TIME   => CURRENT TIMESTAMP)) x           
     WHERE message_id = 'CPF1124'
     ORDER BY ORDINAL_POSITION DESC
   ) SELECT TIMESTAMPDIFF(4, CAST(b.message_timestamp - a.start_time AS CHAR(22)))
              AS execution_minutes, DAYNAME(b.message_timestamp) AS JOB_END_DAY, 
            a.from_user, a.from_job, a.sbs
     FROM JOB_START A  INNER JOIN
          TABLE(qsys2.history_log_info(START_TIME => CURRENT DATE,
                                       END_TIME   => CURRENT TIMESTAMP)) b
          ON b.from_job = a.from_job 
     WHERE b.message_id = 'CPF1164'
     ORDER BY execution_minutes desc limit 20;


--  category:  IBM i Services
--  description:  IBM PowerHA SystemMirror for i - CRG and Session Switch Readiness
--  minvrm: V7R2M0

--
-- Indicates if a device cluster resource group (CRG) is ready to switch with the READY_TO_SWITCH column. 
-- Contains YES if ready to switch, or NO if not ready to switch.
-- This also provides supporting data for why the CRG is or is not ready to switch. 
-- For example, the CRG status, PowerHA Session Status, or CRG recovery domain node status
--
select crg.cluster_resource_group, crg.crg_status, ssn_info.session_name,
       ssn_info.copy_status, rcydmn_nodes.*, (
       case
         when ((crg.crg_status = 'ACTIVE' or
               crg.crg_status = 'EXIT POINT OPERATION PENDING') and
             ssn_info.copy_status = 'ACTIVE' and
             rcydmn_nodes.number_of_crg_inactive_backup_nodes = 0 and
             rcydmn_nodes.number_of_crg_ineligible_backup_nodes = 0 and
             rcydmn_nodes.number_of_crg_partitioned_backup_nodes = 0) then 'YES'
         else 'NO'
       end) as ready_to_switch
  from qhasm.crg_list crg, (
         select coalesce(sum(
                    case node_status
                      when 'INACTIVE' then 1
                      else 0
                    end), 0) number_of_crg_inactive_backup_nodes, coalesce(sum(
                    case node_status
                      when 'INELIGIBLE' then 1
                      else 0
                    end), 0) number_of_crg_ineligible_backup_nodes, coalesce(sum(
                    case node_status
                      when 'PARTITIONED' then 1
                      else 0
                    end), 0) number_of_crg_partitioned_backup_nodes
           from qhasm.crg_list crg, table (
                  qhasm.crg_recovery_domain(
                    cluster_resource_group => crg.cluster_resource_group)
                ) rcydmn
           where rcydmn.node_status != 'ACTIVE' and
                 rcydmn.current_node_role > 0
       ) as rcydmn_nodes, qhasm.session_list ssn_list, table (
         qhasm.session_info(session => ssn_list.session_name)
       ) ssn_info
  where crg.crg_type = '*DEV' and
        crg.cluster_resource_group = ssn_list.cluster_resource_group; 


--  category:  IBM i Services
--  description:  IBM PowerHA SystemMirror for i - Monitored Resources Requiring Attention
--  minvrm: V7R2M0

--
-- A list of monitored resources that are either failed or inconsistent along with additional node level information
--
select details.monitored_resource, details.resource_type, details.library,
       details.global_status, details.node, details.local_status, details.message_id,
       details.message_text
  from table (
         qhasm.admin_domain_mre_list()
       ) list, table (
         qhasm.admin_domain_mre_details(
           monitored_resource => list.monitored_resource,
           resource_type => list.resource_type, library => list.library)
       ) details
  where (list.global_status = '*INCONSISTENT' or
          list.global_status = '*FAILED') and
        details.local_status != 'CURRENT';


--  category:  IBM i Services
--  description:  IBM PowerHA SystemMirror for i - Unmonitored Resources
--  minvrm: V7R2M0

--
-- Find the list of unmonitored resources in the administrative domain
--
select jobd.objname as "Unmonitored Resource", '*JOBD' as "Resource Type",
       jobd.objlongschema as "Resource Library"
  from table (
      qsys2.object_statistics('*ALL', '*JOBD', '*ALLSIMPLE')
    ) jobd
  where jobd.objlongschema != 'QSYS' and
        jobd.objlongschema != 'QINSYS' and
        jobd.objlongschema != 'QINPRIOR' and
        jobd.objlongschema != 'QINMEDIA' and
        not exists (
            select monitored_resource
              from table (
                  qhasm.admin_domain_mre_list(resource_type => '*JOBD')
                ) mre
              where mre.monitored_resource = jobd.objname)
union
select sbsd.objname as "Unmonitored Resource", '*SBSD' as "Resource Type",
       sbsd.objlongschema as "Resource Library"
  from table (
      qsys2.object_statistics('*ALL', '*SBSD', '*ALLSIMPLE')
    ) sbsd
  where sbsd.objlongschema != 'QSYS' and
        sbsd.objlongschema != 'QINSYS' and
        sbsd.objlongschema != 'QINPRIOR' and
        sbsd.objlongschema != 'QINMEDIA' and
        not exists (
            select monitored_resource
              from table (
                  qhasm.admin_domain_mre_list(resource_type => '*SBSD')
                ) mre
              where mre.monitored_resource = sbsd.objname)
union
select usrprf.objname as "Unmonitored Resource", '*USRPRF' as "Resource Type",
       usrprf.objlongschema as "Resource Library"
  from table (
      qsys2.object_statistics('QSYS', '*USRPRF', '*ALLSIMPLE')
    ) usrprf
  where not exists (
        select monitored_resource
          from table (
              qhasm.admin_domain_mre_list(resource_type => '*USRPRF')
            ) mre
          where mre.monitored_resource = usrprf.objname)
union
select autl.objname as "Unmonitored Resource", '*AUTL' as "Resource Type",
       autl.objlongschema as "Resource Library"
  from table (
      qsys2.object_statistics('QSYS', '*AUTL', '*ALLSIMPLE')
    ) autl
  where not exists (
        select monitored_resource
          from table (
              qhasm.admin_domain_mre_list(resource_type => '*AUTL')
            ) mre
          where mre.monitored_resource = autl.objname)
union
select cls.objname as "Unmonitored Resource", '*CLS' as "Resource Type",
       cls.objlongschema as "Resource Library"
  from table (
      qsys2.object_statistics('*ALL', '*CLS', '*ALLSIMPLE')
    ) cls
  where cls.objlongschema != 'QSYS' and
        cls.objlongschema != 'QINSYS' and
        cls.objlongschema != 'QINPRIOR' and
        cls.objlongschema != 'QINMEDIA' and
        not exists (
            select monitored_resource
              from table (
                  qhasm.admin_domain_mre_list(resource_type => '*CLS')
                ) mre
              where mre.monitored_resource = cls.objname);


--  category:  IBM i Services
--  description:  IFS -  10 largest files under a subdir and tree
--  minvrm: V7R3M0
--
select path_name, object_type, data_size, object_owner
  from table(qsys2.IFS_OBJECT_STATISTICS( 
                   start_path_name => '/usr',
                   subtree_directories => 'YES'))
   order by 3 desc
   limit 10;


--  category:  IBM i Services
--  description:  IFS -  IFS storage consumed for a specific user
--  minvrm: V7R3M0
--
with ifsobjs (path, type) as (
  select path_name, object_type
    from table(qsys2.object_ownership('SCOTTF')) a
      where path_name is not null
)
select i.*, data_size, z.*
  from ifsobjs i, lateral (
    select * from 
      table(qsys2.ifs_object_statistics(
              start_path_name => path, 
              subtree_directories => 'NO'))) z
order by data_size desc;


--  category:  IBM i Services
--  description:  IFS -  Non-QSYS, IFS directory data size probe
--  minvrm: V7R3M0
--

-- Note... if not already enrolled, add this...
cl:ADDDIRE USRID(<user-profile> RST) USRD('Your name') USER(<user-profile>);
 
stop;
select path_name, object_type, data_size, object_owner, create_timestamp, access_timestamp,
       data_change_timestamp, object_change_timestamp
  from table (
      qsys2.ifs_object_statistics(
        start_path_name => '/', 
        subtree_directories => 'YES', 
        object_type_list => '*ALLDIR *NOQSYS'))
   where  data_size is not null and object_owner not in ('QSYS')                    
   order by 3 desc
   limit 10;


--  category:  IBM i Services
--  description:  IFS -  What IFS files are in use by a specific job?
--  minvrm: V7R3M0
--
select j.*
  from table (
      qsys2.ifs_job_info(
        '432732/SCOTTF/QPADEV000F')
    ) j;


--  category:  IBM i Services
--  description:  IFS -  Which jobs hold a lock on a specific IFS stream file?
--  minvrm: V7R3M0
--
-- 
select i.*
  from table (
      qsys2.ifs_object_lock_info(
        path_name => '/usr/local/guardium/guard_tap.ini')
    ) i;
    


--  category:  IBM i Services
--  description:  IFS - Capture the meta-data for an IFS tree
--  minvrm: V7R3M0
--
--
-- Note: Change '/tmp' to be the starting location in the IFS

--
-- Which IFS objects were created or changed after a specific point in time (names only)
--
CREATE OR REPLACE TABLE coolstuff.ifschgs (path_name) AS
            (SELECT VARCHAR(path_name, 5000)
                    FROM TABLE (
                            qsys2.ifs_object_statistics(
                                start_path_name => '/tmp', subtree_directories => 'YES', ignore_errors => 'YES',
                                object_type_list => '*NOQSYS *NOQDLS *NOQOPT')
                        )
                    WHERE object_change_timestamp > current_timestamp - 14 DAYS)
            WITH DATA
    ON REPLACE DELETE ROWS;
stop;

--
-- Which IFS objects were created or changed after a specific point in time (full detail)
--
CREATE OR REPLACE TABLE coolstuff.ifschgs as
      (SELECT VARCHAR(path_name, 5000) as path_name, object_type, symbolic_link, asp_number,
              text_description, file_identifier_number, generation_identifier,
              file_system_identifier, file_identifier, file_access, create_timestamp,
              access_timestamp, data_change_timestamp, object_change_timestamp, last_used_timestamp,
              days_used_count, last_reset_timestamp, allocated_size, data_size, "CCSID", code_page,
              extended_attribute_count, critical_extended_attribute_count, extended_attribute_size,
              hard_link_count, object_read_only, object_hidden, temporary_object, system_file,
              system_usage, device_special_file, object_owner, user_id_number, primary_group,
              group_id_number, authorization_list, set_effective_user_id, set_effective_group_id,
              authority_collection_value, object_audit, object_audit_create, journaled,
              journal_library, journal_name, journal_before_image, journal_after_image,
              journal_identifier, journal_start_timestamp, journal_optional_entries,
              journal_subtree, partial_transaction, apply_starting_receiver_library,
              apply_starting_receiver, apply_starting_receiver_asp, object_signed,
              system_trusted_source, multiple_signatures, object_domain, block_size,
              aux_storage_allocation, aux_storage_overflow, main_storage_allocation, storage_freed,
              stored_local, virtual_disk_storage, directory_format, stream_file_format,
              udfs_file_format, udfs_preferred_storage, udfs_temporary_object,
              case_sensitive_file_system, restrict_rename_and_unlink, pc_archive, system_archive,
              allow_save, system_restrict_save, inherit_allow_checkpoint_writer,
              allow_write_during_save, exit_program_scan, exit_program_scan_directory, scan_status,
              ccsid_scan, ccsid_scan_success, scan_signatures_different, binary_scan, checked_out,
              checked_out_timestamp, checked_out_user
          FROM TABLE (
              qsys2.ifs_object_statistics(
                start_path_name => '/tmp', subtree_directories => 'YES', ignore_errors => 'YES',
                object_type_list => '*NOQSYS *NOQDLS *NOQOPT')
            )
          WHERE object_change_timestamp > current_timestamp - 14 DAYS)
      WITH DATA
  ON REPLACE delete ROWS;
stop;
    
--
-- Review the results
--
select * from coolstuff.ifschgs;
stop;


--  category:  IBM i Services
--  description:  IFS - Compare files or trees
--  minvrm: V7R4M0

--
-- Compare two (2) IFS trees
--
select *
  from table (
      qsys2.COMPARE_IFS(
        START_PATH_NAME1   => '/home/scottf/.vscode', 
        START_PATH_NAME2   => '/home/timmr/.vscode',
        COMPARE_ATTRIBUTES => 'YES', 
        OBJECT_TYPE_LIST   => '*ALL')
    );


--  category:  IBM i Services
--  description:  IFS - For the SQL programmers
--  minvrm: V7R4M0
--
-- Resources:
-- https://www.ibm.com/docs/en/i/7.5?topic=services-ifs

--
-- Does /home/scottf/ifs_demo.stmf exist?
--
select path_name, object_type, data_size, object_owner
  from table(qsys2.ifs_object_statistics( 
                   start_path_name => '/home/scottf/ifs_demo.stmf',
                   subtree_directories => 'NO'));
stop;

--
-- Does anyone have a lock on /home/scottf/ifs_demo.stmf?
--
select *
  from table(qsys2.ifs_object_lock_info( 
                   path_name => '/home/scottf/ifs_demo.stmf'));
stop;

--
-- Create /home/scottf/ifs_demo.stmf
--
call qsys2.ifs_write(
  path_name => '/home/scottf/ifs_demo.stmf', 
  line => 'iSee IFS demo');
stop;

--
-- Read /home/scottf/ifs_demo.stmf
--
select line_number, line
  from table (
      qsys2.ifs_read(
        path_name => '/home/scottf/ifs_demo.stmf')
    );  
stop;

--
-- Rename /home/scottf/ifs_demo.stmf
--
values systools.ifs_rename(
                           from_object => '/home/scottf/ifs_demo.stmf', 
                           to_object   => '/home/scottf/ifs_demo_new_name.stmf',
                           replace     => 'NO'
                           );
stop;

--
-- Do I have RWX to that IFS file?
--
values systools.ifs_access(path_name => '/home/scottf/ifs_demo_new_name.stmf', 
                           read      => 'YES',
                           write     => 'YES',
                           execute   => 'YES');
           
--
-- Does JOEUSER have RWX to that IFS file?
--
set session authorization joeuser; 
values systools.ifs_access(path_name => '/home/scottf/ifs_demo_new_name.stmf', 
                           read      => 'YES',
                           write     => 'YES',
                           execute   => 'YES');               
stop;

--
-- Does JOEUSER have RWX to that IFS file?
--
values systools.errno_info(systools.ifs_access(path_name => '/home/scottf/ifs_demo_new_name.stmf', 
                           read      => 'YES',
                           write     => 'YES',
                           execute   => 'YES'));               
stop;

--
-- Delete /home/scottf/ifs_demo_new_name.stmf
--
values systools.ifs_unlink(path_name => '/home/scottf/ifs_demo_new_name.stmf');
stop;

set session authorization system_user; 
values user;

--
-- Delete /home/scottf/ifs_demo_new_name.stmf
--
values systools.ifs_unlink(path_name => '/home/scottf/ifs_demo_new_name.stmf');
stop;




--  category:  IBM i Services
--  description:  IFS - How *PUBLIC is configured for IFS objects I own
--  minvrm: V7R3M0
--
with ifsobjs (path) as (
    select path_name
      from table (
          qsys2.object_ownership(session_user)
        )
      where path_name is not null
  )
  select z.*
    from ifsobjs i, lateral (
           select *
             from table (
                 qsys2.ifs_object_privileges(path_name => path)
               )
         ) z
    where authorization_name = '*PUBLIC'
    order by data_authority;


--  category:  IBM i Services
--  description:  IFS - Reading a stream file
--  minvrm: V7R3M0

-- Read an IFS stream using character data 
--
select line_number, line
  from table (
      qsys2.ifs_read(
        path_name => '/usr/local/install.log', 
        end_of_line => 'ANY',
        maximum_line_length => default, 
        ignore_errors => 'NO')
    );  


--  category:  IBM i Services
--  description:  IFS - Server share info
--  minvrm: V7R3M0

--
-- IBM� i NetServer shares - IFS stream files being shared
--
select server_share_name, path_name, permissions 
  from qsys2.server_share_info
  where share_type = 'FILE';


--  category:  IBM i Services
--  description:  IFS - Server share info with security details
--  minvrm: V7R3M0

--
-- IBM� i NetServer shares - IFS stream files security
--
with shares (name, pn, perm) as (
    select server_share_name, path_name, permissions
      from qsys2.server_share_info
      where share_type = 'FILE'
  )
  select name, pn, perm, authorization_name as username,
         data_authority as actual_data_authority
    from shares, lateral (
           select *
             from table (
                 qsys2.ifs_object_privileges(path_name => pn)
               )
         );


--  category:  IBM i Services
--  description:  IFS - Summarize the current usage for an IFS stream file
--  minvrm: V7R3M0
--
-- 
select r.*
  from table (
      qsys2.ifs_object_references_info(
        path_name => '/usr/local/guardium/guard_tap.ini')
    ) r;
    


--  category:  IBM i Services
--  description:  IFS - Writing to a stream file
--  minvrm: V7R3M0

-- 
-- Find all the library names and write them to an IFS file
--
begin
  -- Make sure output file is empty to start
  call qsys2.ifs_write(
    path_name => '/tmp/library_names',
    line => '',
    overwrite => 'REPLACE',
    end_of_line => 'NONE'
  );
  -- Add lines to the output file
  for select objname as libname
    from table (
        qsys2.object_statistics('*ALLSIMPLE', 'LIB')
      )
    do
      call qsys2.ifs_write(
        path_name => '/tmp/library_names',
        line => libname
      );
  end for;
end;

select *
  from table (
      qsys2.ifs_read('/tmp/library_names')
    );
stop;



--  category:  IBM i Services
--  description:  Java - Find instances of old Java versions being used

select * from qsys2.jvm_info
 where JAVA_HOME not like '%/jdk7%' and 
       JAVA_HOME not like '%/jdk8%';
       


--  category:  IBM i Services
--  description:  Java - JVM Health

--
-- Find the top 10 JVM jobs by amount of time spent in Garbage Collection
--
SELECT TOTAL_GC_TIME, GC_CYCLE_NUMBER,JAVA_THREAD_COUNT, A.* FROM QSYS2.JVM_INFO A
 ORDER BY TOTAL_GC_TIME DESC
 FETCH FIRST 10 ROWS ONLY;

--
-- Change a specific web admin JVM to provide verbose garbage collection details:
--
CALL QSYS2.SET_JVM('121376/QWEBADMIN/ADMIN4','GC_ENABLE_VERBOSE') ;


--  category:  IBM i Services
--  description:  Journal - Journal Info
--  minvrm: V7R3M0

--
-- description: Which journal receivers are detached?
-- (replace SHOESTORE with your library name and QSQJRN with your journal name)
--
with attached(jl, jn, jrcv) as (
select attached_journal_receiver_library, 'QSQJRN', attached_journal_receiver_name
  from qsys2.journal_info
  where journal_library = 'SHOESTORE' and journal_name = 'QSQJRN'
)
select objname as detached_jrnrcv, a.*
  from attached, table (
      qsys2.object_statistics(jl, '*JRNRCV')
    ) as a
    where 
    a.journal_library = jl and a.journal_name = jn and
    objname not in (select jrcv from attached);


--  category:  IBM i Services
--  description:  Journal - Journaled Objects
--  minvrm: V7R3M0

--
-- Which objects are journaled to this journal?
--
select *
  from qsys2.journaled_objects
  where journal_library = 'TOYSTORE' and
        journal_name = 'QSQJRN';
        


--  category:  IBM i Services
--  description:  Journal - Systools Audit Journal AF
--  minvrm: V7R3M0

--
-- Is this IBM i configured to generated AF entries?
-- Note: auditing_control         == QAUDCTL 
--       auditing_level           == QAUDLVL and
--       auditing_level_extension == QAUDLVL2
--
select count(*) as "AF_enabled?"
  from qsys2.security_info
  where (auditing_control like '%*AUDLVL%') and
        ((auditing_level like '%*AUTFAIL%') or
         (auditing_level like '%*AUDLVL2%' and
          auditing_level_extension like '%*AUTFAIL%'));

--
-- Review the authorization violations, which occurred in the last 24 hours
-- 
select ENTRY_TIMESTAMP, VIOLATION_TYPE_DETAIL, USER_NAME, coalesce(
         path_name, object_library concat '/' concat object_name concat ' ' concat object_type) as object
  from table (
      SYSTOOLS.AUDIT_JOURNAL_AF(STARTING_TIMESTAMP => current timestamp - 24 hours)
    );

--
-- Review the authorization violations, which occurred in the last 24 hours (include all columns)
-- 
select ENTRY_TIMESTAMP, VIOLATION_TYPE_DETAIL, USER_NAME, coalesce(
         path_name, object_library concat '/' concat object_name concat ' ' concat object_type) as object, af.*
  from table (
      SYSTOOLS.AUDIT_JOURNAL_AF(STARTING_TIMESTAMP => current timestamp - 24 hours)
    ) af;
 


--  category:  IBM i Services
--  description:  Journal - Systools Audit Journal CA
--  minvrm: V7R3M0

--
-- Is this IBM i configured to generated CA entries?
-- Note: auditing_control         == QAUDCTL
--       auditing_level           == QAUDLVL and
--       auditing_level_extension == QAUDLVL2
--
select count(*) as "CA_enabled?"
  from qsys2.security_info
  where (auditing_control like '%*AUDLVL%') and
        ((auditing_level like '%*SECURITY%') or (auditing_level like '%*SECRUN%') or
         (auditing_level like '%*AUDLVL2%' and
           (auditing_level_extension like '%*SECURITY%') or (auditing_level_extension like '%*SECRUN%')));

--
-- Review the authorization changes, which occurred in the last 24 hours (include all columns)
-- 
select ENTRY_TIMESTAMP, USER_NAME, COMMAND_TYPE, USER_PROFILE_NAME,
coalesce(
         path_name, object_library concat '/' concat object_name concat ' ' concat object_type) as object, ca.*
  from table (
      SYSTOOLS.AUDIT_JOURNAL_CA(STARTING_TIMESTAMP => current timestamp - 24 hours)
    ) ca
    order by entry_timestamp desc;



--  category:  IBM i Services
--  description:  Journal - Systools Audit Journal OW
--  minvrm: V7R3M0

--
-- Is this IBM i configured to generated OW entries?
-- Note: auditing_control         == QAUDCTL 
--       auditing_level           == QAUDLVL and
--       auditing_level_extension == QAUDLVL2
--
select count(*) as "OW_enabled?"
  from qsys2.security_info
  where (auditing_control like '%*AUDLVL%') and
        ((auditing_level like '%*SECURITY%') or (auditing_level like '%*SECRUN%') or
         (auditing_level like '%*AUDLVL2%' and
           (auditing_level_extension like '%*SECURITY%') or (auditing_level_extension like '%*SECRUN%')));

--
-- Review the ownership changes, which occurred in the last 24 hours (include all columns)
-- 
select ENTRY_TIMESTAMP, USER_NAME, PREVIOUS_OWNER, NEW_OWNER,  
coalesce(
         path_name, object_library concat '/' concat object_name concat ' ' concat object_type) as object, ow.*
  from table (
      SYSTOOLS.AUDIT_JOURNAL_OW(STARTING_TIMESTAMP => current timestamp - 24 hours)
    ) ow
    order by entry_timestamp desc;


--  category:  IBM i Services
--  description:  Journal - Systools Audit Journal PW
--  minvrm: V7R3M0

--
-- Is this IBM i configured to generated PW entries?
-- Note: auditing_control         == QAUDCTL 
--       auditing_level           == QAUDLVL and
--       auditing_level_extension == QAUDLVL2
--
select count(*) as "PW_enabled?"
  from qsys2.security_info
  where (auditing_control like '%*AUDLVL%') and
        ((auditing_level like '%*AUTFAIL%') or
         (auditing_level like '%*AUDLVL2%' and
          auditing_level_extension like '%*AUTFAIL%'));

--
-- Review the password failures, which occurred in the last 24 hours (include all columns)
-- 
select ENTRY_TIMESTAMP, VIOLATION_TYPE_DETAIL, AUDIT_USER_NAME, DEVICE_NAME, pw.*
  from table (
      SYSTOOLS.AUDIT_JOURNAL_PW(STARTING_TIMESTAMP => current timestamp - 24 hours)
    ) pw
    order by entry_timestamp desc;


--  category:  IBM i Services
--  description:  Journal - Systools change user profile (CHGUSRPRF)
--  minvrm: V7R3M0

--
-- Find user profiles using a default password, generate the commands needed to disable them
--
select AUTHORIZATION_NAME, TEXT_DESCRIPTION, CHGUSRPRF_COMMAND
  from QSYS2.USER_INFO,
       table (
         SYSTOOLS.CHANGE_USER_PROFILE(
           P_USER_NAME => AUTHORIZATION_NAME, P_STATUS => '*DISABLED', PREVIEW => 'YES'
         ))
  where STATUS = '*ENABLED' and
        user_creator <> '*IBM' and
        USER_DEFAULT_PASSWORD = 'YES';
stop;
--
-- Take the action!
--
select cp.* from QSYS2.USER_INFO,
       table (
         SYSTOOLS.CHANGE_USER_PROFILE(
           P_USER_NAME => AUTHORIZATION_NAME, P_STATUS => '*DISABLED', PREVIEW => 'NO'
         )
       ) cp
  where STATUS = '*ENABLED' and
        user_creator <> '*IBM' and
        USER_DEFAULT_PASSWORD = 'YES';
stop;


--  category:  IBM i Services
--  description:  Librarian -  Library Info 
--  minvrm: V7R3M0
--

create or replace variable coolstuff.library_report_stmt varchar(10000) for sbcs data default
'create or replace table coolstuff.library_sizes
      (library_name, schema_name, 
      
       -- qsys2.library_info() columns
       library_size, library_size_formatted, 
       object_count, library_size_complete, library_type, text_description,
       iasp_name, iasp_number, create_authority, object_audit_create, journaled,
       journal_library, journal_name, inherit_journaling, journal_start_timestamp,
       apply_starting_receiver_library, apply_starting_receiver,
       apply_starting_receiver_asp,
       
       -- qsys2.object_statistics() columns
       objowner, objdefiner, objcreated, objsize, objtext, objlongname,
       change_timestamp, last_used_timestamp, last_used_object, days_used_count, last_reset_timestamp,
       save_timestamp, restore_timestamp, save_while_active_timestamp, 
       user_changed, source_file, source_library, source_member,
       source_timestamp, created_system, created_system_version, licensed_program,
       licensed_program_version, compiler, compiler_version, object_control_level,
       ptf_number, apar_id, user_defined_attribute, allow_change_by_program,
       changed_by_program, compressed, primary_group, storage_freed,
       associated_space_size, optimum_space_alignment, overflow_storage, object_domain,
       object_audit, object_signed, system_trusted_source, multiple_signatures,
       save_command, save_device, save_file_name, save_file_library, save_volume, save_label,
       save_sequence_number, last_save_size, journal_images, omit_journal_entry, remote_journal_filter, 
       authority_collection_value
       )
  as
      (select objname as lib, objlongname as schema, library_size,
              varchar_format(library_size, ''999G999G999G999G999G999G999G999G999G999'')
                as formatted_size, object_count, library_size_complete, library_type, text_description,
       b.iasp_name, b.iasp_number, create_authority, object_audit_create, a.journaled,
       b.journal_library, b.journal_name, inherit_journaling, b.journal_start_timestamp,
       b.apply_starting_receiver_library, b.apply_starting_receiver,
       b.apply_starting_receiver_asp,
              objowner, objdefiner, objcreated, objsize, objtext, objlongname,
       change_timestamp, last_used_timestamp, last_used_object, days_used_count, last_reset_timestamp,
       save_timestamp, restore_timestamp, save_while_active_timestamp, 
       user_changed, source_file, source_library, source_member,
       source_timestamp, created_system, created_system_version, licensed_program,
       licensed_program_version, compiler, compiler_version, object_control_level,
       ptf_number, apar_id, user_defined_attribute, allow_change_by_program,
       changed_by_program, compressed, primary_group, storage_freed,
       associated_space_size, optimum_space_alignment, overflow_storage, object_domain,
       object_audit, object_signed, system_trusted_source, multiple_signatures,
       save_command, save_device, save_file_name, save_file_library, save_volume, save_label,
       save_sequence_number, last_save_size, journal_images, omit_journal_entry, remote_journal_filter, 
       authority_collection_value
          from table (
                 qsys2.object_statistics(''*ALLUSR'', ''*LIB'')
               ) as a, lateral (
                 select *
                   from table (
                       qsys2.library_info(library_name => a.objname,
                                          ignore_errors => ''YES'',
                                          detailed_info => ''LIBRARY_SIZE'')
                     )
               ) b)
      with data   on replace delete rows';
stop;
  
cl:SBMJOB CMD(RUNSQL SQL('begin execute immediate coolstuff.library_report_stmt; end') commit(*NONE)) JOB(LIBSIZES);
stop;

--
-- jobs submitted from this job
--
select *
  from table (
      qsys2.job_info(job_submitter_filter => '*JOB', job_user_filter => '*ALL')
    );

-- once the job ends, it won't be returned by job_info... then you can query the results
select * from coolstuff.library_sizes ls order by library_size desc;
 


--  category:  IBM i Services
--  description:  Librarian -  Which IBM commands have had their command parameter defaults changed using CHGCMDDFT
--  minvrm: V7R3M0
--
select * from table(qsys2.object_statistics('QSYS', '*CMD'))
  where APAR_ID = 'CHGDFT';


--  category:  IBM i Services
--  description:  Librarian - Examine least and most popular routines

--
-- Note: Replace library-name with the target library name
-- Find unused procedures and functions
--
select OBJNAME,OBJTEXT,OBJCREATED,DAYS_USED_COUNT, x.* from table(qsys2.object_statistics('library-name', 'PGM SRVPGM')) x
WHERE SQL_OBJECT_TYPE IN ('PROCEDURE','FUNCTION')
AND LAST_USED_TIMESTAMP IS NULL OR DAYS_USED_COUNT = 0
ORDER BY OBJLONGNAME ASC;

-- Find the most frequently used procedures and functions
--
select LAST_USED_TIMESTAMP, DAYS_USED_COUNT, LAST_RESET_TIMESTAMP, x.* from table(qsys2.object_statistics('library-name', 'PGM SRVPGM')) x
WHERE SQL_OBJECT_TYPE IN ('PROCEDURE','FUNCTION')
AND LAST_USED_TIMESTAMP IS NOT NULL
ORDER BY DAYS_USED_COUNT DESC;


--  category:  IBM i Services
--  description:  Librarian - Find objects

--
-- Find user libraries that are available, return full details about the libraries
--
SELECT * FROM TABLE (QSYS2.OBJECT_STATISTICS('*ALLUSRAVL ', '*LIB') ) as a;

--
-- Super Fast retrieval of library and schema name
--
SELECT OBJNAME AS LIBRARY_NAME, OBJLONGNAME AS SCHEMA_NAME
   FROM TABLE(QSYS2.OBJECT_STATISTICS('*ALLSIMPLE', 'LIB')) Z
     ORDER BY 1 ASC;

--
-- Super Fast retrieval names of an object type within a library
--
SELECT objname
   FROM TABLE(qsys2.object_statistics('TOYSTORE', '*FILE', '*ALLSIMPLE')) AS x;

--
-- Find Program and Service programs within a library
-- Note: Replace library-name with the target library name
--
SELECT * FROM TABLE (QSYS2.OBJECT_STATISTICS('library-name', '*PGM *SRVPGM') ) as a;



--  category:  IBM i Services
--  description:  Librarian - Journal Inherit Rules
--  minvrm: V7R3M0

--
-- Review library specific journal inheritance rules
--
select library_name, 
       ordinal_position,  
       object_type, 
       operation, 
       rule_action,  
       name_filter, 
       journal_images,  
       omit_journal_entry, 
       remote_journal_filter 
  from qsys2.journal_inherit_rules
  where journaled = 'YES'
  order by library_name, ordinal_position;


--  category:  IBM i Services
--  description:  Librarian - Library list

--
-- Description: Ensure that the TOYSTORE library is the first library 
--              in the user portion of the library list 
 BEGIN 
 DECLARE V_ROW_NUM INTEGER; 
 WITH CTE1(SCHEMA_NAME, ROW_NUM) AS ( 
   SELECT SCHEMA_NAME, ROW_NUMBER() OVER (ORDER BY ORDINAL_POSITION) AS ROW_NUM 
     FROM QSYS2.LIBRARY_LIST_INFO WHERE TYPE = 'USER' 
 ) SELECT ROW_NUM INTO V_ROW_NUM FROM CTE1 WHERE SCHEMA_NAME = 'TOYSTORE'; 
 IF (V_ROW_NUM IS NULL) THEN 
   CALL QSYS2.QCMDEXC('ADDLIBLE TOYSTORE'); 
 ELSEIF (V_ROW_NUM > 1) THEN 
   BEGIN 
     CALL QSYS2.QCMDEXC('RMVLIBLE TOYSTORE'); 
     CALL QSYS2.QCMDEXC('ADDLIBLE TOYSTORE'); 
   END; 
 END IF; 
 END;


--  category:  IBM i Services
--  description:  License Management - Expiration processing
--  minvrm:  v7r2m0

--
-- Detect if any license is expired or will expire soon (within the next 45 days)
--         
CALL systools.license_expiration_check(45);         

--
-- Review messages sent to the system operator message queue with license expiration details
--
SELECT MESSAGE_TEXT, m.*
   FROM qsys2.message_queue_info m
   WHERE message_queue_name = 'QSYSOPR' AND
         MESSAGE_TEXT LIKE '%EXPIRE%';

--
-- Review license usage violations
--
SELECT a.*
   FROM qsys2.license_info a
   WHERE log_violation = 'YES'
   ORDER BY peak_usage DESC;


--  category:  IBM i Services
--  description:  Message Handling  - Query a message file

SELECT
  MESSAGE_FILE_LIBRARY,               -- MSGF_LIB    VARCHAR(10)       
  MESSAGE_FILE,                       -- MSGF        VARCHAR(10)       
  MESSAGE_ID,                         -- MSGID       CHARACTER(7)      
  MESSAGE_TEXT,                       -- MSG_TEXT    VARGRAPHIC(132)   
  MESSAGE_SECOND_LEVEL_TEXT,          -- SECLVL      VARGRAPHIC(3000)  
  SEVERITY,                           -- SEVERITY    INTEGER           
  MESSAGE_DATA_COUNT,                 -- MSGDATACNT  INTEGER           
  MESSAGE_DATA,                       -- MSGDATA     VARCHAR(2078)     
  LOG_PROBLEM,                        -- LOGPRB      VARCHAR(4)        
  CREATION_DATE,                      -- CRT_DATE    DATE              
  CREATION_LEVEL,                     -- CRT_LEVEL   INTEGER           
  MODIFICATION_DATE,                  -- MOD_DATE    DATE              
  MODIFICATION_LEVEL,                 -- MOD_LEVEL   INTEGER           
  CCSID,                              -- CCSID       INTEGER           
  DEFAULT_PROGRAM_LIBRARY,            -- DFT_PGMLIB  VARCHAR(10)       
  DEFAULT_PROGRAM,                    -- DFT_PGM     VARCHAR(10)       
  REPLY_TYPE,                         -- REPLY_TYPE  VARCHAR(6)        
  REPLY_LENGTH,                       -- REPLY_LEN   INTEGER           
  REPLY_DECIMAL_POSITIONS,            -- REPLY_DEC   INTEGER           
  DEFAULT_REPLY,                      -- DFT_REPLY   VARCHAR(132)      
  VALID_REPLY_VALUES_COUNT,           -- REPLY_CNT   INTEGER           
  VALID_REPLY_VALUES,                 -- REPLY_VALS  VARCHAR(659)      
  VALID_REPLY_LOWER_LIMIT,            -- LOWERLIMIT  VARCHAR(32)       
  VALID_REPLY_UPPER_LIMIT,            -- UPPERLIMIT  VARCHAR(32)       
  VALID_REPLY_RELATIONSHIP_OPERATOR,  -- REL_OP      CHARACTER(3)      
  VALID_REPLY_RELATIONSHIP_VALUE,     -- REL_VALUE   VARCHAR(32)       
  SPECIAL_REPLY_VALUES_COUNT,         -- SPECIALCNT  INTEGER           
  SPECIAL_REPLY_VALUES,               -- SPECIALVAL  VARCHAR(1319)     
  DUMP_LIST_COUNT,                    -- DUMP_COUNT  INTEGER           
  DUMP_LIST,                          -- DUMP_LIST   VARCHAR(815)      
  ALERT_OPTION,                       -- ALERTOPT    VARCHAR(9)        
  ALERT_INDEX                         -- ALERTINDEX  INTEGER           
FROM QSYS2.MESSAGE_FILE_DATA 
where MESSAGE_FILE_LIBRARY = 'QSYS' and MESSAGE_FILE = 'QSQLMSG';



--  category:  IBM i Services
--  description:  Message Handling - Abnormal IPL Predictor 
--  minvrm:  v7r2m0

--
-- Examine history log messages since the previous IPL and
-- determine whether the next IPL will be abnormal or normal
--
WITH last_ipl(ipl_time)
   AS (SELECT job_entered_system_time
          FROM TABLE(qsys2.job_info(job_status_filter => '*ACTIVE',
             job_user_filter => 'QSYS')) x
          WHERE job_name = '000000/QSYS/SCPF'), 
   abnormal(abnormal_count) 
   AS (SELECT COUNT(*)
          FROM last_ipl, 
          TABLE(qsys2.history_log_info(ipl_time, CURRENT TIMESTAMP)) x
          WHERE message_id IN ('CPC1225'))
   SELECT
      CASE
         WHEN abnormal_count = 0
            THEN 'NEXT IPL WILL BE NORMAL'
            ELSE 'NEXT IPL WILL BE ABNORMAL - ABNORMAL END COUNT: ' 
               concat abnormal_count
      END AS next_ipl_indicator FROM abnormal ; 


--  category:  IBM i Services
--  description:  Message Handling - Reply List

-- Review reply list detail for all messages which begin with CPA 
SELECT * FROM QSYS2.REPLY_LIST_INFO WHERE message_ID LIKE 'CPA%';


--  category:  IBM i Services
--  description:  Message Handling - Review system operator inquiry messages

--
-- Examine all system operator inquiry messages that have a reply
--
SELECT a.message_text AS "INQUIRY", b.message_text AS "REPLY", B.FROM_USER, B.*, A.*
 FROM qsys2.message_queue_info a INNER JOIN   
      qsys2.message_queue_info b
ON a.message_key = b.associated_message_key
WHERE A.MESSAGE_QUEUE_NAME = 'QSYSOPR' AND
      A.MESSAGE_QUEUE_LIBRARY = 'QSYS' AND
      B.MESSAGE_QUEUE_NAME = 'QSYSOPR' AND
      B.MESSAGE_QUEUE_LIBRARY = 'QSYS'
ORDER BY b.message_timestamp DESC; 


--  category:  IBM i Services
--  description:  Message Handling - Review system operator unanswered inquiry messages

--
-- Examine all system operator inquiry messages that have no reply
--
WITH REPLIED_MSGS(KEY) AS (
SELECT a.message_key
 FROM qsys2.message_queue_info a INNER JOIN   
      qsys2.message_queue_info b
ON a.message_key = b.associated_message_key
WHERE A.MESSAGE_QUEUE_NAME = 'QSYSOPR' AND
      A.MESSAGE_QUEUE_LIBRARY = 'QSYS' AND
      B.MESSAGE_QUEUE_NAME = 'QSYSOPR' AND
      B.MESSAGE_QUEUE_LIBRARY = 'QSYS'
ORDER BY b.message_timestamp DESC
)
SELECT a.message_text AS "INQUIRY", A.*
 FROM qsys2.message_queue_info a 
      LEFT EXCEPTION JOIN REPLIED_MSGS b
ON a.message_key = b.key
WHERE MESSAGE_QUEUE_NAME = 'QSYSOPR' AND
      MESSAGE_QUEUE_LIBRARY = 'QSYS' AND
      message_type = 'INQUIRY'  
ORDER BY message_timestamp DESC; 



--  category:  IBM i Services
--  description:  Message Handling - Send Alert messages to QSYSOPR
--  minvrm:  v7r3m0

--
-- Send the SQL7064 message to the QSYSOPR message queue
--
values length('Query Supervisor - terminated a query for ' concat qsys2.job_name);

call QSYS2.SEND_MESSAGE('SQL7064', 65, 'Query Supervisor - terminated a query for ' concat
      qsys2.job_name);

--
-- Review the most recent messages on the QSYSOPR message queue
--
select *
  from table (
      QSYS2.MESSAGE_QUEUE_INFO(MESSAGE_FILTER => 'ALL')
    )
  order by MESSAGE_TIMESTAMP desc; 


--  category:  IBM i Services
--  description: PTF - Defective PTF Currency
--  minvrm:  v7r4m0

--
-- Do we have a defective PTF installed, where the corrective PTF is not applied?
--
select *
  from systools.defective_ptf_currency;


--  category:  IBM i Services
--  description:  PTF - Firmware Currency 

--
-- Compare the current Firmware against IBM's 
-- Fix Level Request Tool (FLRT) to determine if the 
-- firmware level is current or upgrades are available
--   
SELECT * 
  FROM SYSTOOLS.FIRMWARE_CURRENCY;


--  category:  IBM i Services
--  description:  PTF - Group PTF Currency 

--
-- Derive the IBM i operating system level and then 
-- determine the level of currency of PTF Groups
--   
With iLevel(iVersion, iRelease) AS
(
select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info
)
  SELECT P.*
     FROM iLevel, systools.group_ptf_currency P
     WHERE ptf_group_release = 
           'R' CONCAT iVersion CONCAT iRelease concat '0'
     ORDER BY ptf_group_level_available -
        ptf_group_level_installed DESC;
        
--
-- For those that need to use STRSQL ;-(
-- 
With iLevel(iVersion, iRelease) AS
(
select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info
)
SELECT VARCHAR(GRP_CRNCY,26) AS "GRPCUR",
       GRP_ID,  VARCHAR(GRP_TITLE, 20) AS "NAME",
       GRP_LVL, GRP_IBMLVL, GRP_LSTUPD,
       GRP_RLS, GRP_SYSSTS
FROM iLevel, systools.group_ptf_currency P
WHERE ptf_group_release =
'R' CONCAT iVersion CONCAT iRelease concat '0'
ORDER BY ptf_group_level_available -
ptf_group_level_installed DESC;


--  category:  IBM i Services
--  description:  PTF - Group PTF Currency 

--
-- Derive the IBM i operating system level and then 
-- determine the level of currency of PTF Groups
--   
With iLevel(iVersion, iRelease) AS
(
select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info
)
  SELECT P.*
     FROM iLevel, systools.group_ptf_currency P
     WHERE ptf_group_release = 
           'R' CONCAT iVersion CONCAT iRelease concat '0'
     ORDER BY ptf_group_level_available -
        ptf_group_level_installed DESC;
        

-- 
-- For those that like STRSQL ;-(
--
With iLevel(iVersion, iRelease) AS
(
select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info
)
SELECT VARCHAR(GRP_CRNCY,26) AS "GRPCUR",
       GRP_ID,  VARCHAR(GRP_TITLE, 20) AS "NAME",
       GRP_LVL, GRP_IBMLVL, GRP_LSTUPD,
       GRP_RLS, GRP_SYSSTS
FROM iLevel, systools.group_ptf_currency P
WHERE ptf_group_release =
'R' CONCAT iVersion CONCAT iRelease concat '0'
ORDER BY ptf_group_level_available -
ptf_group_level_installed DESC;


--  category:  IBM i Services
--  description:  PTF - Group PTF Details 

--
-- Review all unapplied PTFs contained within PTF Groups installed on the partition 
-- against the live PTF detail available from IBM
--
SELECT * FROM SYSTOOLS.GROUP_PTF_DETAILS
  WHERE PTF_STATUS <> 'PTF APPLIED'
  ORDER BY PTF_GROUP_NAME;


--  category:  IBM i Services
--  description:  PTF - Group PTF Details 

--
-- Determine if this IBM i is missing any IBM i Open Source PTFs
-- 
SELECT *
   FROM TABLE(systools.group_ptf_details('SF99225')) a
     WHERE PTF_STATUS = 'PTF MISSING'; /* SF99225 == 5733OPS */
;

--  category:  IBM i Services
--  description:  PTF - PTF information 

--
-- Find which PTFs will be impacted by the next IPL.
--
SELECT PTF_IDENTIFIER, PTF_IPL_ACTION, A.*
  FROM QSYS2.PTF_INFO A
  WHERE PTF_IPL_ACTION <> 'NONE';

--
-- Find which PTFs are loaded but not applied
--
SELECT PTF_IDENTIFIER, PTF_IPL_REQUIRED, A.*
  FROM QSYS2.PTF_INFO A
  WHERE PTF_LOADED_STATUS = 'LOADED'
  ORDER BY PTF_PRODUCT_ID;


--  category:  IBM i Services
--  description:  Password failures over the last 24 hours

CREATE OR REPLACE VIEW coolstuff.Password_Failures_24hrs  FOR SYSTEM NAME PW_LAST24
  (TIME, JOBNAME, USERNAME, IPADDR)
   AS
SELECT ENTRY_TIMESTAMP, 
       JOB_NUMBER CONCAT '/' CONCAT RTRIM(JOB_USER) CONCAT '/' CONCAT RTRIM(JOB_NAME) AS JOB_NAME, 
       RTRIM(CAST(SUBSTR(entry_data, 2, 10) AS VARCHAR(10))), REMOTE_ADDRESS
  FROM TABLE(qsys2.display_journal(
            'QSYS', 'QAUDJRN',              -- Journal library and name
            STARTING_RECEIVER_NAME => '*CURAVLCHN',
            journal_entry_types => 'PW',    -- Journal entry types
            starting_timestamp => CURRENT TIMESTAMP - 24 HOURS -- Time period
)) X;

--
-- description: Review the password failure detail
--
SELECT * FROM coolstuff.PW_LAST24
  order by TIME asc;        


--  category:  IBM i Services
--  description:  Performance - Collection Services 
--  minvrm: V7R3M0
--

  
--
-- Review the Collection Services (CS) configuration
--
select *
  from QSYS2.COLLECTION_SERVICES_INFO;

--
-- Shred the CS categories and interval settings
--
select a.*
  from QSYS2.COLLECTION_SERVICES_INFO, lateral (select * from JSON_TABLE(CATEGORY_LIST, 'lax $.category_list[*]' 
  columns(cs_category clob(1k) ccsid 1208 path 'lax $."category"', 
          cs_interval clob(1k) ccsid 1208 path 'lax $."interval"'))) a;
  
  


--  category:  IBM i Services
--  description:  Product - Expiring license info

--
-- Return information about all licensed products and features 
-- that will expire within the next 2 weeks.
--
SELECT * FROM QSYS2.LICENSE_INFO
WHERE LICENSE_EXPIRATION <= CURRENT DATE + 50 DAYS;

-- Return information about all licensed products and features 
-- that will expire within the next 2 weeks, for installed products only
--
SELECT * FROM QSYS2.LICENSE_INFO
WHERE INSTALLED = 'YES' AND
LICENSE_EXPIRATION <= CURRENT DATE + 50 DAYS;


--  category:  IBM i Services
--  description:  Product - Software Product Info 
--  minvrm:  v7r3m0

-- Is QSYSINC installed? (DSPSFWRSC alternative)
--
select count(*) as gtg_count
  from qsys2.software_product_info
  where upper(text_description) like '%SYSTEM OPENNESS%'
        and load_error = 'NO'
        and load_state = 90
        and symbolic_load_state = 'INSTALLED';


--  category:  IBM i Services
--  description:  Review public authority to files in library TOYSTORE

SELECT OBJECT_AUTHORITY AS PUBLIC_AUTHORITY,  
       COUNT(*) AS COUNT FROM TABLE(QSYS2.OBJECT_STATISTICS('TOYSTORE', 'FILE')) F, 
LATERAL 
(SELECT OBJECT_AUTHORITY FROM QSYS2.OBJECT_PRIVILEGES 
    WHERE SYSTEM_OBJECT_NAME   = F.OBJNAME 
      AND USER_NAME            = '*PUBLIC'
      AND SYSTEM_OBJECT_SCHEMA = 'TOYSTORE'
      AND OBJECT_TYPE          = '*FILE') P 
GROUP BY OBJECT_AUTHORITY ORDER BY 2 DESC;


--  category:  IBM i Services
--  description:  Review the object ownership summary for objects in a library

SELECT OBJOWNER, COUNT(*) AS OWN_COUNT
  FROM TABLE(QSYS2.OBJECT_STATISTICS('TOYSTORE', 'ALL')) X
  GROUP BY OBJOWNER
  ORDER BY 2 DESC;


--  category:  IBM i Services
--  description:  Security - Audit Journal CD review
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Review the audited commands from today and yesterday
--
SELECT entry_timestamp, user_name, object_library, object_name, object_type, command_string
  FROM TABLE (
      systools.audit_journal_cd()
    )
  WHERE object_name IN ('ADDPFTRG', 'CRTPGM', 'CRTSRVPGM', 'SAVOBJ', 
                    'SAVLIB', 'CRTDUPOBJ', 'CPYF')
  ORDER BY entry_timestamp DESC;


--  category:  IBM i Services
--  description:  Security - Auditing configuration for commands 
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Enable object auditing of a command
--
cl: QSYS/CHGOBJAUD OBJ(QSYS/ADDPFTRG) OBJTYPE(*CMD) OBJAUD(*ALL); 
stop;

--
-- What is the Object Audit setting for attack vector commands?
--
SELECT objname, object_audit
  FROM TABLE (
      qsys2.object_statistics('QSYS', '*CMD')
    )
  WHERE objname IN ('ADDPFTRG', 'CRTPGM', 'CRTSRVPGM', 'SAVOBJ', 
                    'SAVLIB', 'CRTDUPOBJ', 'CPYF');


--  category:  IBM i Services
--  description:  Security - Authority Collection
--  minvrm:  v7r3m0

--
-- Use authority collection to capture and study the enforcement of security.
-- In this example, JOEUSER needs to be given read data privileges to 
-- the TOYSTORE/SALES file. Authority collection can be used to iterate through
-- the process of identifying and granting granular authorities.
--
CL: STRAUTCOL USRPRF(JOEUSER) LIBINF((TOYSTORE));
stop; -- Ask JOEUSER to attempt the data access on the TOYSTORE/SALES table
CL: ENDAUTCOL USRPRF(JOEUSER);

-- Review the authorization failures
SELECT SYSTEM_OBJECT_NAME, DETAILED_REQUIRED_AUTHORITY FROM QSYS2.AUTHORITY_COLLECTION
 WHERE AUTHORIZATION_NAME = 'JOEUSER'
  AND  AUTHORITY_CHECK_SUCCESSFUL = '0';

CL: DLTAUTCOL USRPRF(JOEUSER);

CL: GRTOBJAUT OBJ(TOYSTORE) OBJTYPE(*LIB) USER(JOEUSER) AUT(*EXECUTE);
CL: GRTOBJAUT OBJ(TOYSTORE/SALES) OBJTYPE(*FILE) USER(JOEUSER) AUT(*OBJOPR);
CL: GRTOBJAUT OBJ(TOYSTORE/SALES) OBJTYPE(*FILE) USER(JOEUSER) AUT(*READ);


--  category:  IBM i Services
--  description:  Security - Authority Collection 
--  minvrm:  v7r4m0

-- Enable authority collection by object for the TOYSTORE/EMPLOYEE *FILE 
-- and include all dependent objects
cl: CHGAUTCOL  OBJ('/QSYS.LIB/TOYSTORE.LIB/EMPLOYEE.FILE')
           AUTCOLVAL(*OBJINF) INCDEPOBJ(*LF);


-- Start capturing authority collection by object detail
cl: STRAUTCOL TYPE(*OBJAUTCOL) DLTCOL(*ALL);

-- Review which objects are enabled for authority collection
SELECT authority_collection_value,
       a.*
   FROM TABLE (
         qsys2.object_statistics('TOYSTORE', '*ALL')
      ) a
   ORDER BY 1 DESC; 

stop;
-- Stop capturing data
cl: ENDAUTCOL TYPE(*OBJAUTCOL);

-- Delete the authority collection data
cl: DLTAUTCOL TYPE(*OBJ) OBJ('/QSYS.LIB/TOYSTORE.LIB/EMPLOYEE.FILE') INCDEPOBJ(*LF);





--  category:  IBM i Services
--  description:  Security - Authority Collection 
--  minvrm:  v7r4m0

--
-- Show me activity over TOYSTORE/EMPLOYEE
--
with emp_activity (
    username, cur_auth, req_auth
  ) as (
    select "CURRENT_USER", detailed_current_authority, detailed_required_authority
      from qsys2.authority_collection_object aco
      where system_object_schema = 'TOYSTORE' and system_object_name = 'EMPLOYEE' and adopting_program_owner is null
  )
  select * from emp_activity;

--
-- Show me just the data changers
--
with emp_activity (
    username, cur_auth, req_auth
  ) as (
    select "CURRENT_USER", detailed_current_authority, detailed_required_authority
      from qsys2.authority_collection_object aco
      where system_object_schema = 'TOYSTORE' and system_object_name = 'EMPLOYEE' and adopting_program_owner is null
  )
  select * from emp_activity
    where  req_auth like '%UPD%' or
           req_auth like '%DLT%' or
           req_auth like '%ADD%';
     
stop;
--
-- Refine the data changers query to include more data
--
with emp_activity (
    authorization_name,
    check_timestamp,
    system_object_name,
    system_object_schema,
    system_object_type,
    asp_name,
    asp_number,
    object_name,
    object_schema,
    object_type,
    authorization_list,
    authority_check_successful,
    check_any_authority,
    cached_authority,
    required_authority,
    detailed_required_authority,
    current_authority,
    detailed_current_authority,
    authority_source,
    group_name,
    multiple_groups_used,
    adopt_authority_used,
    multiple_adopting_programs_used,
    adopting_program_name,
    adopting_program_schema,
    adopting_procedure_name,
    adopting_program_type,
    adopting_program_asp_name,
    adopting_program_asp_number,
    adopting_program_statement_number,
    adopting_program_owner,
    current_adopted_authority,
    detailed_current_adopted_authority,
    adopted_authority_source,
    most_recent_program_invoked,
    most_recent_program_schema,
    most_recent_module,
    most_recent_program_procedure,
    most_recent_program_type,
    most_recent_program_asp_name,
    most_recent_program_asp_number,
    most_recent_program_statement_number,
    most_recent_user_state_program_invoked,
    most_recent_user_state_program_schema,
    most_recent_user_state_module,
    most_recent_user_state_program_procedure,
    most_recent_user_state_program_type,
    most_recent_user_state_program_asp_name,
    most_recent_user_state_program_asp_number,
    most_recent_user_state_program_statement_number,
    job_name,
    job_user,
    job_number,
    thread_id,
    "CURRENT_USER",
    object_file_id,
    object_asp_name,
    object_asp_number,
    path_name,
    path_region,
    path_language,
    absolute_path_indicator,
    relative_directory_file_id
  )
  as (
    select authorization_name,
           check_timestamp,
           system_object_name,
           system_object_schema,
           system_object_type,
           asp_name,
           asp_number,
           object_name,
           object_schema,
           object_type,
           authorization_list,
           authority_check_successful,
           check_any_authority,
           cached_authority,
           required_authority,
           detailed_required_authority,
           current_authority,
           detailed_current_authority,
           authority_source,
           group_name,
           multiple_groups_used,
           adopt_authority_used,
           multiple_adopting_programs_used,
           adopting_program_name,
           adopting_program_schema,
           adopting_procedure_name,
           adopting_program_type,
           adopting_program_asp_name,
           adopting_program_asp_number,
           adopting_program_statement_number,
           adopting_program_owner,
           current_adopted_authority,
           detailed_current_adopted_authority,
           adopted_authority_source,
           most_recent_program_invoked,
           most_recent_program_schema,
           most_recent_module,
           most_recent_program_procedure,
           most_recent_program_type,
           most_recent_program_asp_name,
           most_recent_program_asp_number,
           most_recent_program_statement_number,
           most_recent_user_state_program_invoked,
           most_recent_user_state_program_schema,
           most_recent_user_state_module,
           most_recent_user_state_program_procedure,
           most_recent_user_state_program_type,
           most_recent_user_state_program_asp_name,
           most_recent_user_state_program_asp_number,
           most_recent_user_state_program_statement_number,
           job_name,
           job_user,
           job_number,
           thread_id,
           "CURRENT_USER",
           object_file_id,
           object_asp_name,
           object_asp_number,
           path_name,
           path_region,
           path_language,
           absolute_path_indicator,
           relative_directory_file_id
      from qsys2.authority_collection_object aco
      where system_object_schema = 'TOYSTORE' and system_object_name = 'EMPLOYEE' and
            adopting_program_owner is null
  )
  select *
    from emp_activity
    where detailed_required_authority like '%UPD%' or detailed_required_authority like
            '%DLT%' or detailed_required_authority like '%ADD%';
     


--  category:  IBM i Services
--  description:  Security - Authority Collection (analyze)

-- Review the authorization failures
SELECT system_object_schema concat '/' concat system_object_name as Object, 
       system_object_type, authority_source, 
       detailed_current_authority,
       detailed_required_authority, ac.*
     FROM qsys2.authority_collection ac
     WHERE authorization_name = 'JOEUSER' and authority_check_successful = '0';
           

-- Review the successes
SELECT system_object_schema concat '/' concat system_object_name as Object, 
       system_object_type, authority_source, 
       detailed_current_authority,
       detailed_required_authority, ac.*
     FROM qsys2.authority_collection ac
     WHERE authorization_name = 'JOEUSER' and
      (system_object_schema concat '/' concat system_object_name like '%SQL123%' or system_object_schema concat '/' concat system_object_name like '%TOYSTORE%') and
           authority_check_successful = '1';

-- Review use of adopted authority 
SELECT adopting_program_schema concat '/' concat adopting_program_name as Object, 
       adopting_program_type,    current_adopted_authority, 
       adopted_authority_source, detailed_required_authority, 
       multiple_adopting_programs_used, ac.*
     FROM qsys2.authority_collection ac
     WHERE authorization_name = 'JOEUSER' and
           adopt_authority_used = '1';
           
-- Which commands and programs are being used?           
SELECT SYSTEM_OBJECT_SCHEMA concat '/' concat SYSTEM_OBJECT_NAME as Object, COUNT(*) as COUNT
 FROM QSYS2.AUTHORITY_COLLECTION A
 WHERE SYSTEM_OBJECT_TYPE IN ('*PGM', '*CMD') and authorization_name = 'JOEUSER' 
 GROUP BY SYSTEM_OBJECT_SCHEMA concat '/' concat SYSTEM_OBJECT_NAME   
 ORDER BY 2 DESC;


--  category:  IBM i Services
--  description:  Security - Authority Collection (capture)

--
-- Capture and save authority collection detail for JOEUSER
--
CL:STRAUTCOL USRPRF(JOEUSER) LIBINF((TOYSTORE));
stop; -- Ask JOEUSER to attempt the data access on the TOYSTORE/SALES table
CL: ENDAUTCOL USRPRF(JOEUSER);

--
-- Save JOEUSER's authority collection detail
--
CL: CRTLIB AUTCOLDATA;

CREATE TABLE AUTCOLDATA.JOEUSER AS (
  SELECT * FROM qsys2.authority_collection 
    WHERE AUTHORIZATION_NAME = 'JOEUSER'
) WITH DATA;

-- delete the authority collection detail 
CL: DLTAUTCOL USRPRF(JOEUSER);


--  category:  IBM i Services
--  description:  Security - Authority Collection (review)

--
-- Use authority collection to capture and study the enforcement of security.
-- In this example, JOEUSER needs to be given read data privileges to 
-- the TOYSTORE/SALES file. Authority collection can be used to iterate through
-- the process of identifying and granting granular authorities.
--
-- Which users have ACTIVE authority collection on-going?
--                  ======
--
SELECT AUTHORIZATION_NAME, AUTHORITY_COLLECTION_REPOSITORY_EXISTS 
  FROM QSYS2.USER_INFO 
    WHERE AUTHORITY_COLLECTION_ACTIVE = 'YES';

--
-- Which users have authority collection detail?
--
SELECT AUTHORIZATION_NAME, AUTHORITY_COLLECTION_ACTIVE 
  FROM QSYS2.USER_INFO 
    WHERE AUTHORITY_COLLECTION_REPOSITORY_EXISTS = 'YES';

--
-- How much Authority Collection detail was captured?
--
SELECT AUTHORIZATION_NAME, count(*) as AC_COUNT
  FROM qsys2.authority_collection 
  GROUP BY AUTHORIZATION_NAME
  ORDER BY 2 DESC;


--  category:  IBM i Services
--  description:  Security - Authorization List detail

--
-- List the public security settings for all authorization lists.
--
SELECT *
FROM QSYS2.AUTHORIZATION_LIST_USER_INFO
WHERE AUTHORIZATION_NAME = '*PUBLIC';


--  category:  IBM i Services
--  description:  Security - Certificate attribute analysis
--  minvrm:  v7r3m0

-- Use a global variable to avoid having source code include password values
create or replace variable coolstuff.system_cert_pw varchar(30);
set coolstuff.system_cert_pw = 'PWDVALUE1234567';

select *
  from table (
      qsys2.certificate_info(certificate_store_password => coolstuff.system_cert_pw)
    )
  where validity_end < current date + 1 month;


--  category:  IBM i Services
--  description:  Security - Certificate attribute analysis
--  minvrm:  v7r3m0

--
--  Review the certificate store detail using the stashed password file
--  Find the certificates that are no longer valid, or that become invalid within a month
--
select *
  from table (
      qsys2.certificate_info(certificate_store_password => '*NOPWD')
    )
  where validity_end < current date + 1 month
  order by validity_end;


--  category:  IBM i Services
--  description:  Security - Check authority to query

--
-- Description: Does this user have authority to query this file 
--
VALUES ( 
   CASE WHEN QSYS2.SQL_CHECK_AUTHORITY('QSYS2','SYSLIMITS') = 1 
        THEN 'I can query QSYS2/SYSLIMITS' 
        ELSE 'No query access for me' END 
);


--  category:  IBM i Services
--  description:  Security - Commands that Limited Capabilities can use
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Which commands can be executed by users with "Limited Capabilities"?
--
SELECT *
  FROM qsys2.command_info
  WHERE allow_limited_user = 'YES';


--  category:  IBM i Services
--  description:  Security - DISPLAY_JOURNAL() of the audit journal
--  minvrm:  v7r2m0
--  Note: this is available at IBM i 7.2 and higher, because it relies upon UDTF default & named parameter support 

--
--  Use Display_Journal() to examine the Change Profile (CP) entries that have occurred over the last 24 hours.
--
SELECT journal_code, journal_entry_type, object, object_type, X.* 
FROM TABLE (
QSYS2.Display_Journal(
  'QSYS', 'QAUDJRN',                       -- Journal library and name
  JOURNAL_ENTRY_TYPES => 'CP' ,            -- Journal entry types
  STARTING_TIMESTAMP => CURRENT TIMESTAMP - 24 HOURS  -- Time period
) ) AS x
;

--  category:  IBM i Services
--  description:  Security - DRDA Authentication Entry info

--
-- Review the DRDA & DDM Server authentication entry configuration
--
SELECT * FROM QSYS2.DRDA_AUTHENTICATION_ENTRY_INFO
  ORDER BY AUTHORIZATION_NAME, SERVER_NAME;


--  category:  IBM i Services
--  description:  Security - Dashboard 
--  minvrm:  v7r3m0

--
-- How is my IBM i Security configured?
--
select *
  from qsys2.security_info;


--  category:  IBM i Services
--  description:  Security - Db2 for i - Delete attack vector
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Files where ANY user can delete rows
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND user_name = '*PUBLIC' AND
            data_execute = 'YES'
  )
  SELECT *
    FROM libs, qsys2.object_privileges
    WHERE system_object_schema = lib_name AND object_type = '*FILE' AND user_name = '*PUBLIC' AND
          data_delete = 'YES' AND ('PF' = (SELECT objattribute
                FROM TABLE (
                    qsys2.object_statistics(lib_name, '*FILE', object_name)
                  )));


--  category:  IBM i Services
--  description:  Security - Db2 for i - Insert attack vector
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Files where ANY user can insert rows
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND user_name = '*PUBLIC' AND
            data_execute = 'YES'
  )
  SELECT *
    FROM libs, qsys2.object_privileges
    WHERE system_object_schema = lib_name AND object_type = '*FILE' AND user_name = '*PUBLIC' AND
          data_add = 'YES' AND ('PF' = (SELECT objattribute
                FROM TABLE (
                    qsys2.object_statistics(lib_name, '*FILE', object_name)
                  ))); 


--  category:  IBM i Services
--  description:  Security - Db2 for i - Query attack vector
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Database physical files that ANY user can read
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND user_name = '*PUBLIC' AND
            data_execute = 'YES'
  )
  SELECT *
    FROM libs, qsys2.object_privileges
    WHERE system_object_schema = lib_name AND object_type = '*FILE' AND user_name = '*PUBLIC' AND
          data_read = 'YES' AND object_operational = 'YES' AND ('PF' = (SELECT objattribute
                FROM TABLE (
                    qsys2.object_statistics(lib_name, '*FILE', object_name)
                  )));


--  category:  IBM i Services
--  description:  Security - Db2 for i - RENAME attack
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Database files exposed to a RENAME attack
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND authorization_name =
            '*PUBLIC' AND data_execute = 'YES' AND data_update = 'YES'
  )
  SELECT priv.*
    FROM libs,
         LATERAL (
           SELECT *
             FROM qsys2.object_privileges
             WHERE system_object_schema = lib_name AND object_type = '*FILE' AND authorization_name
                   = '*PUBLIC' AND object_management = 'YES' AND object_operational = 'YES' AND (
                     'PF' = (SELECT objattribute
                         FROM TABLE (
                             qsys2.object_statistics(lib_name, '*FILE', object_name)
                           )))
         ) priv;


--  category:  IBM i Services
--  description:  Security - Db2 for i - Trigger attack vector
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Files exposed to a trigger attack
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND user_name = '*PUBLIC' AND
            data_execute = 'YES'
  )
  SELECT *
    FROM libs, qsys2.object_privileges
    WHERE system_object_schema = lib_name AND object_type = '*FILE' AND user_name = '*PUBLIC' AND
          data_read = 'YES' AND object_operational = 'YES' AND (object_alter = 'YES' OR
            object_management = 'YES') AND ('PF' = (SELECT objattribute
                FROM TABLE (
                    qsys2.object_statistics(lib_name, '*FILE', object_name)
                  ))); 


--  category:  IBM i Services
--  description:  Security - Db2 for i - Update attack vector
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Files where ANY user can update rows
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND user_name = '*PUBLIC' AND
            data_execute = 'YES'
  )
  SELECT *
    FROM libs, qsys2.object_privileges
    WHERE system_object_schema = lib_name AND object_type = '*FILE' AND user_name = '*PUBLIC' AND
          data_update = 'YES' AND ('PF' = (SELECT objattribute
                FROM TABLE (
                    qsys2.object_statistics(lib_name, '*FILE', object_name)
                  )));


--  category:  IBM i Services
--  description:  Security - Function Usage

--
-- Compare Security Function Usage details between production and backup 
--

DECLARE GLOBAL TEMPORARY TABLE SESSION . Remote_function_usage 
( function_id, user_name, usage, user_type )
AS (SELECT * FROM gt73p2.qsys2.function_usage) WITH DATA
WITH REPLACE;

SELECT 'GT73P1' AS "Source Partition",
   a.function_id, a.user_name, a.usage, a.user_type
   FROM qsys2.function_usage a LEFT EXCEPTION JOIN 
        session.remote_function_usage b ON 
   a.function_id = b.function_id AND a.user_name   = b.user_name AND
   a.usage   = b.usage           AND a.user_type   = b.user_type
UNION ALL
SELECT 'GT73P2' AS "Target Partition",
   b.function_id, b.user_name, b.usage, b.user_type
   FROM qsys2.function_usage a RIGHT EXCEPTION JOIN 
        session.remote_function_usage b ON 
   a.function_id = b.function_id AND a.user_name   = b.user_name AND
   a.usage   = b.usage           AND a.user_type   = b.user_type
ORDER BY 2, 3;



--  category:  IBM i Services
--  description:  Security - Group profile detail

--
-- Review Group and Supplemental Group settings
--
SELECT group_profile_name,
       supplemental_group_count,
       supplemental_group_list,
       u.*
   FROM qsys2.user_info u
   WHERE supplemental_group_count > 0
   ORDER BY 2 DESC;


--  category:  IBM i Services
--  description:  Security - IFS Authority Collection 
--  minvrm:  v7r4m0

-- 
-- Who is using, or attempting to use, Scott's IFS home?
--
cl:CHGAUTCOL OBJ('/home/SCOTTF/') AUTCOLVAL(*OBJINF) SUBTREE(*ALL) DLTCOL(*YES);

--
-- Is Authority Collection by Object enabled system wide?
--
select object_authority_collection_active
  from qsys2.security_info;
stop; 
  
--
-- Are the objects under Scott's IFS home configured for 
-- Authority Collection by Object?
--
select path_name, object_type, authority_collection_value
  from table(qsys2.ifs_object_statistics('/home/SCOTTF/')); 
stop; 

--
-- Start capturing authority collection by object detail
--
cl: STRAUTCOL TYPE(*OBJAUTCOL) DLTCOL(*ALL);
stop;

--
-- Who is using (or attempting to use) my IFS home?
--
SELECT user_name, COUNT(*) AS count
  FROM qsys2.authority_collection_ifs
  WHERE LEFT(path_name, 12) LIKE '/home/SCOTTF' AND user_name NOT IN ('SCOTTF')
  GROUP BY user_name
  ORDER BY count desc;
stop;

--
-- Who is attempting to use my IFS home, but seeing a failure
--
SELECT user_name, check_timestamp, path_name, system_object_type, detailed_required_authority,
       detailed_current_authority, authority_source
  FROM qsys2.authority_collection_ifs
  WHERE LEFT(path_name, 12) LIKE '/home/SCOTTF' AND chksuccess = '0';
stop;

--
-- Shut down and cleanup
--
stop;
-- Stop capturing data
cl: ENDAUTCOL TYPE(*OBJAUTCOL);

-- Delete the authority collection data
cl:DLTAUTCOL TYPE(*OBJ) OBJ('/home/SCOTTF/') SUBTREE(*ALL);
stop;



--  category:  IBM i Services
--  description:  Security - IFS home directories (detail)
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Where *PUBLIC authorization is NOT set to DTAAUT(*EXCLUDE) OBJAUT(*NONE)
--  
SELECT ios.path_name, object_owner, data_authority, object_operational, 
       object_management, object_existence, object_alter, object_reference
  FROM TABLE(qsys2.ifs_object_statistics(
        start_path_name     => '/home/', 
        subtree_directories => 'NO', 
        object_type_list    => '*ALLDIR')
    ) ios, lateral (
           select *
             from table (
                 qsys2.ifs_object_privileges(path_name => ios.path_name)
               )
         ) z where ios.path_name not in ('/home/') and 
                   data_authority <> '*EXCLUDE' 
                   or 
                   (object_operational = 'YES' or 
                    object_management  = 'YES' or   
                    object_existence   = 'YES' or  
                    object_alter       = 'YES' or  
                    object_reference   = 'YES') 
  order by data_authority;


--  category:  IBM i Services
--  description:  Security - IFS home directories (summary)
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Where *PUBLIC authorization is NOT set to DTAAUT(*EXCLUDE) OBJAUT(*NONE)
--  
SELECT data_authority, count(*) as dir_count
  FROM TABLE(qsys2.ifs_object_statistics(
        start_path_name     => '/home/', 
        subtree_directories => 'NO', 
        object_type_list    => '*ALLDIR')
    ) ios, lateral (
           select *
             from table (
                 qsys2.ifs_object_privileges(path_name => ios.path_name)
               )
         ) z where ios.path_name not in ('/home/') and 
                   data_authority <> '*EXCLUDE' 
                   or 
                   (object_operational = 'YES' or 
                    object_management  = 'YES' or   
                    object_existence   = 'YES' or  
                    object_alter       = 'YES' or  
                    object_reference   = 'YES')
         group by data_authority
  order by data_authority;


--  category:  IBM i Services
--  description:  Security - Library List security review
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Review the library list and return any library where *PUBLIC is configured to something other than *USE
--
SELECT libl.system_schema_name AS lib_name, priv.authorization_user AS user_name,
       priv.object_authority
  FROM qsys2.library_list_info libl, LATERAL (
         SELECT *
           FROM TABLE (
               qsys2.object_privileges(
                 system_object_schema => 'QSYS', system_object_name => system_schema_name,
                 object_type => '*LIB')
             )
       ) priv
  WHERE priv.authorization_user = '*PUBLIC' AND 
        priv.object_authority   <> '*USE'   AND
        libl.system_schema_name not in ('QTEMP'); 


--  category:  IBM i Services
--  description:  Security - Object Ownership
--  minvrm:  v7r3m0

with qsysobjs (lib, obj, type) as (
    select object_library, object_name, object_type
      from table (qsys2.object_ownership('SCOTTF'))
      where path_name is null
  )
  select q.*, z.*
    from qsysobjs q, lateral (
           select objcreated, last_used_timestamp, objsize
             from table (qsys2.object_statistics(lib, type, obj))
         ) z
  order by OBJSIZE DESC;


--  category:  IBM i Services
--  description:  Security - Powerful commands 
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- What is *PUBLIC set to for the most productive attack vector commands?
--
SELECT object_name, object_type, object_authority
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*CMD' AND 
        object_name IN ('ADDPFTRG', 'CRTPGM', 'CRTSRVPGM', 'SAVOBJ', 
                        'SAVLIB', 'CRTDUPOBJ', 'CPYF') AND 
        user_name = '*PUBLIC';


--  category:  IBM i Services
--  description:  Security - QSYS objects owned by the #1 storage consumer
--  minvrm:  v7r3m0

with top_dog (username, storage) as (
       select authorization_name, sum(storage_used)
         from qsys2.user_storage
         where authorization_name not like 'Q%'
         group by authorization_name
         order by 2 desc
         limit 1),
     qsysobjs (lib, obj, type) as (
       select object_library, object_name, object_type
         from top_dog, table (
                qsys2.object_ownership(username)
              )
         where path_name is null
     )
  select username, q.*, z.*
    from top_dog, qsysobjs q, lateral (
           select objcreated, last_used_timestamp, objsize
             from table (
                 qsys2.object_statistics(lib, type, obj)
               )
         ) z
    order by objsize desc;
  


--  category:  IBM i Services
--  description:  Security - Review *ALLOBJ users

--
-- Which users have *ALLOBJ authority either directly
-- or via a Group or Supplemental profile?
--
SELECT AUTHORIZATION_NAME, STATUS, NO_PASSWORD_INDICATOR, PREVIOUS_SIGNON,
TEXT_DESCRIPTION
FROM QSYS2.USER_INFO
WHERE SPECIAL_AUTHORITIES LIKE '%*ALLOBJ%'
OR AUTHORIZATION_NAME IN (
SELECT USER_PROFILE_NAME
FROM QSYS2.GROUP_PROFILE_ENTRIES
WHERE GROUP_PROFILE_NAME IN (
SELECT AUTHORIZATION_NAME
FROM QSYS2.USER_INFO
WHERE SPECIAL_AUTHORITIES like '%*ALLOBJ%'
)
)
ORDER BY AUTHORIZATION_NAME;


--  category:  IBM i Services
--  description:  Security - Review *JOBCTL users

--
-- Which users have *JOBCTL authority either directly
-- or via a Group or Supplemental profile?
--
SELECT AUTHORIZATION_NAME, STATUS, NO_PASSWORD_INDICATOR, PREVIOUS_SIGNON,
TEXT_DESCRIPTION
FROM QSYS2.USER_INFO
WHERE SPECIAL_AUTHORITIES LIKE '%*JOBCTL%'
OR AUTHORIZATION_NAME IN (
SELECT USER_PROFILE_NAME
FROM QSYS2.GROUP_PROFILE_ENTRIES
WHERE GROUP_PROFILE_NAME IN (
SELECT AUTHORIZATION_NAME
FROM QSYS2.USER_INFO
WHERE SPECIAL_AUTHORITIES like '%*JOBCTL%'
)
)
ORDER BY AUTHORIZATION_NAME;


--  category:  IBM i Services
--  description:  Security - Secure column values within SQL tooling

--
-- Secure salary column values in the SQL Performance Center  
--
CALL SYSPROC.SET_COLUMN_ATTRIBUTE('TOYSTORE',
                                  'EMPLOYEE',
                                  'SALARY', 
                                  'SECURE YES'); 

--
-- Review configuration of SECURE column values for the tools 
-- used by DBEs & Database Performance analysts 
--
 SELECT COLUMN_NAME,SECURE 
    FROM QSYS2.SYSCOLUMNS2 
    WHERE SYSTEM_TABLE_SCHEMA = 'TOYSTORE' AND
          SYSTEM_TABLE_NAME   = 'EMPLOYEE';


--  category:  IBM i Services
--  description:  Security - Special Authority Data Mart
--  minvrm:  v7r4m0

--
-- Determine when the table was last refreshed.
--
SELECT REFRESH_TIME FROM QSYS2.SYSTABLES
  WHERE TABLE_SCHEMA = 'SYSTOOLS' AND
        TABLE_NAME = 'SPECIAL_AUTHORITY_DATA_MART';xs

--
-- Update the table to contain the current 
-- special authority values for all user profiles on the system
--
REFRESH TABLE SYSTOOLS.SPECIAL_AUTHORITY_DATA_MART;
stop;

--
-- List all the users who have *ALLOBJ special authority, 
-- either directly from their user profile or as part of a group profile.
--
SELECT DISTINCT USER_NAME FROM SYSTOOLS.SPECIAL_AUTHORITY_DATA_MART
  WHERE SPECIAL_AUTHORITY = '*ALLOBJ';



--  category:  IBM i Services
--  description:  Security - Special Authority Data Mart
--  minvrm:  v7r4m0

--
-- This example shows how to establish and use the data mart in a library of your choosing
--

--
-- Generate the SQL source for the data mart into the IFS, without the SYSTOOLS qualification
--
call qsys2.generate_sql(DATABASE_OBJECT_NAME         => 'SPECIAL_AUTHORITY_DATA_MART', 
                        DATABASE_OBJECT_LIBRARY_NAME => 'SYSTOOLS', 
                        DATABASE_OBJECT_TYPE         => 'TABLE', 
                        QUALIFIED_NAME_OPTION        => '1', 
                        DATABASE_SOURCE_FILE_NAME    => '*STMF',
                        SOURCE_STREAM_FILE_CCSID     => 37,
                        SOURCE_STREAM_FILE           => '/home/SCOTTF/sadm_source.sql'
                        );
stop;

--
-- Review the generate SQL source
--
select * from table(qsys2.ifs_read('/home/SCOTTF/sadm_source.sql'));                        
stop;

--
-- Create a library for the data mart
--
cl: crtlib special;
    
--
-- Create the data mart
--
begin 
  set schema special;
  call qsys2.qcmdexc('QSYS/RUNSQLSTM SRCSTMF(''/home/SCOTTF/sadm_source.sql'') COMMIT(*NONE) NAMING(*SQL)');
end;
stop;

--
-- Add the data to the MQT (data mart)
--
REFRESH TABLE special.SPECIAL_AUTHORITY_DATA_MART;
stop;

--
-- Work with the MQT (data mart)
--
select AUTHORIZATION_NAME, SPECIAL_AUTHORITY, AUTHORITY_SOURCE, GROUP_PROFILE_NAME, STATUS,
       TEXT_DESCRIPTION, LAST_USED_DATE
  from special.SPECIAL_AUTHORITY_DATA_MART
  order by USER_NAME;
stop;


--  category:  IBM i Services
--  description:  Security - Special Authority and Db2 data
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Repopulate the special authority detail in the SYSTOOLS MQT
--  
refresh table systools.special_authority_data_mart;

--
-- Which users can see ANY Db2 for i data
--                     ===
--
SELECT *
  FROM systools.special_authority_data_mart
  WHERE special_authority IN ('*ALLOBJ', '*SAVSYS')
  ORDER BY user_name;
   


--  category:  IBM i Services
--  description:  Security - User Info Basic (faster than User Info)
--  minvrm:  v7r3m0

--
-- Review all user profiles that have an expired password
--
select *
  from QSYS2.USER_INFO_BASIC
  where DAYS_UNTIL_PASSWORD_EXPIRES = 0
  order by coalesce(PREVIOUS_SIGNON, current timestamp - 100 years) asc;


--  category:  IBM i Services
--  description:  Security - User Info Sign On Failures

--
-- Which users are having trouble signing on?
--
SELECT * FROM QSYS2.USER_INFO 
 WHERE SIGN_ON_ATTEMPTS_NOT_VALID > 0;


--  category:  IBM i Services
--  description:  Security - User Info close to disabled

--
-- Which users are at risk of becoming disabled due to lack of use? 
--
SELECT * FROM QSYS2.USER_INFO 
 WHERE STATUS = '*ENABLED' AND LAST_USED_TIMESTAMP IS NOT NULL
 ORDER BY LAST_USED_TIMESTAMP ASC
 FETCH FIRST 20 ROWS ONLY;


--  category:  IBM i Services
--  description:  Security - User profile attack vector 
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Which *USRPRF's do not have *PUBLIC set to *EXCLUDE?
--
SELECT object_name AS user_name, object_authority, owner
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
          'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
        '*EXCLUDE';


--  category:  IBM i Services
--  description:  Security - Users with Limited Capabilities 
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- Which users are configured with "Limited Capabilities"?
--
SELECT *
  FROM qsys2.user_info_basic
  WHERE limit_capabilities = '*YES';


--  category:  IBM i Services
--  description:  Security - Which users are changing data via a remote connection?
--  minvrm:  v7r2m0
--  Note: this is available at IBM i 7.2 and higher because this example uses the named and default parameters on a function invocation

SELECT OBJECT,"CURRENT_USER",remote_address,
COUNT(*) AS change_count
   FROM TABLE(qsys2.display_journal('QSYS', 'QAUDJRN', -- Journal library and name
journal_entry_types => 'ZC', -- Journal entry types
starting_timestamp => CURRENT TIMESTAMP - 24 HOURS -- Time period
)) AS x
   WHERE remote_address IS NOT NULL
   GROUP BY OBJECT, "CURRENT_USER", remote_address;


--  category:  IBM i Services
--  description:  Spool - Consume my most recent spooled file

--
-- Query my most recent spooled file
--
WITH my_spooled_files (
      job,
      FILE,
      file_number,
      user_data,
      create_timestamp
   )
      AS (SELECT job_name,
                 spooled_file_name,
                 file_number,
                 user_data,
                 create_timestamp
            FROM qsys2.output_queue_entries_basic
            WHERE user_name = USER
            ORDER BY create_timestamp DESC
            LIMIT 1)
   SELECT job,
          FILE,
          file_number,
          spooled_data
      FROM my_spooled_files,
           TABLE (
              systools.spooled_file_data(
                 job_name => job, spooled_file_name => FILE,
                 spooled_file_number => file_number)
           );
           




--  category:  IBM i Services
--  description:  Spool - Generate PDF into the IFS
--  minvrm: V7R3M0

--
-- What spooled files exist for a user?
--
select *
  from qsys2.output_queue_entries_basic
  where status = 'READY' and
        user_name = 'JOEUSER';

cl: mkdir '/usr/timmr';

--
-- What files exist under this path?
--
select *
  from table (
      qsys2.ifs_object_statistics(START_PATH_NAME => '/usr/JOEUSER', SUBTREE_DIRECTORIES => 'YES')
    );

--
-- Take the spooled files and generate pdfs into IFS path
-- Note: prerequisite software: 5770TS1 - Option 1 - Transform Services - AFP to PDF Transform 
--
select job_name, spooled_file_name, file_number, 
  SYSTOOLS.Generate_PDF( 
   job_name            => job_name, 
   spooled_file_name   => spooled_file_name, 
   spooled_file_number => file_number, 
   path_name   => '/usr/timmr/' concat regexp_replace(job_name, '/', '_') 
      concat '_' concat spooled_file_name concat '_' concat file_number) 
      as "pdf_created?",
   '/usr/timmr/' concat regexp_replace(job_name, '/', '_') 
      concat '_' concat spooled_file_name concat '_' concat file_number
      as pdf_path from qsys2.output_queue_entries_basic 
      where status = 'READY' and user_name = 'TIMMR';

--
-- What files exist under this path?
--
select *
  from table (
      qsys2.ifs_object_statistics(START_PATH_NAME => '/usr/timmr/', SUBTREE_DIRECTORIES => 'YES')
    );

--
-- and the data is there
--
select path_name, line_number, line
  from table (
         qsys2.ifs_object_statistics(START_PATH_NAME => '/usr/timmr/', SUBTREE_DIRECTORIES => 'YES')
       ), lateral (
         select *
           from table (
               qsys2.ifs_read_binary(
                 path_name => path_name,   maximum_line_length => default,
                 ignore_errors => 'NO')
             )
       ) where object_type = '*STMF';

 


--  category:  IBM i Services
--  description:  Spool - Output queue basic detail

--
-- Find the 100 largest spool files in the QEZJOBLOG output queue.
--
SELECT * FROM QSYS2.OUTPUT_QUEUE_ENTRIES_BASIC
  WHERE OUTPUT_QUEUE_NAME = 'QEZJOBLOG'
  ORDER BY SIZE DESC
  FETCH FIRST 100 ROWS ONLY;

--
-- Find the top 10 consumers of SPOOL storage.
--
SELECT USER_NAME, SUM(SIZE) AS TOTAL_SPOOL_SPACE
  FROM QSYS2.OUTPUT_QUEUE_ENTRIES_BASIC
  WHERE USER_NAME NOT LIKE 'Q%'
  GROUP BY USER_NAME
  ORDER BY TOTAL_SPOOL_SPACE DESC LIMIT 10;


--  category:  IBM i Services
--  description:  Spool - Output queue exploration

--
-- Find the output queue with the most files & see the details
WITH BIGGEST_OUTQ(LIBNAME, QUEUENAME, FILECOUNT)
   AS (SELECT OUTPUT_QUEUE_LIBRARY_NAME, OUTPUT_QUEUE_NAME, NUMBER_OF_FILES
          FROM QSYS2.OUTPUT_QUEUE_INFO
          ORDER BY NUMBER_OF_FILES DESC
          FETCH FIRST 1 ROWS ONLY)
   SELECT LIBNAME, QUEUENAME, X.*  FROM BIGGEST_OUTQ,   
          TABLE(QSYS2.OUTPUT_QUEUE_ENTRIES(LIBNAME, QUEUENAME, '*NO')) X
 ORDER BY TOTAL_PAGES DESC;


-- Review the files on the top 5 output queues with the most files
WITH outqs_manyfiles ( libname, queuename )
   AS (SELECT OUTPUT_QUEUE_LIBRARY_NAME, OUTPUT_QUEUE_NAME
          FROM QSYS2.OUTPUT_QUEUE_INFO
          ORDER BY NUMBER_OF_FILES DESC
          FETCH FIRST 5 ROWS ONLY)
   SELECT libname, queuename, create_timestamp, spooled_file_name, user_name, total_pages, size 
	FROM outqs_manyfiles INNER JOIN QSYS2.OUTPUT_QUEUE_ENTRIES 
	ON queuename=OUTPUT_QUEUE_NAME AND libname=OUTPUT_QUEUE_LIBRARY_NAME 
 	ORDER BY TOTAL_PAGES DESC;


--  category:  IBM i Services
--  description:  Spool - Search all QZDASOINIT spooled files

--
-- Find QZDASONIT joblogs related to a specific TCP/IP address
--
with my_spooled_files (
        job,
        file,
        file_number,
        user_data,
        create_timestamp
     )
        as (select job_name,
                   spooled_file_name,
                   file_number,
                   user_data,
                   create_timestamp
              from qsys2.output_queue_entries_basic
              where user_data = 'QZDASOINIT' and spooled_file_name = 'QPJOBLOG'
                 and CREATE_TIMESTAMP > CURRENT TIMESTAMP - 24 hours
              order by create_timestamp desc),
     all_my_spooled_file_data (
        job,
        file,
        file_number,
        spool_data
     )
     as (
        select job,
               file,
               file_number,
               spooled_data
           from my_spooled_files,
                table (
                   systools.spooled_file_data(
                      job_name => job, spooled_file_name => file,
                      spooled_file_number => file_number)
                )
     )
   select *
      from all_my_spooled_file_data
      where upper(spool_data) like upper('%client 9.85.200.78 connected to server%') ;     




--  category:  IBM i Services
--  description:  Spool - Top 10 consumers of spool storage

--
-- Find the top 10 consumers of SPOOL storage 
-- Note: Replace library-name with the target library name
--
SELECT USER_NAME, SUM(SIZE) AS TOTAL_SPOOL_SPACE FROM 
   TABLE (QSYS2.OBJECT_STATISTICS('QSYS      ', '*LIB') ) as a, 
   TABLE (QSYS2.OBJECT_STATISTICS(a.objname, 'OUTQ')  ) AS b, 
   TABLE (QSYS2.OUTPUT_QUEUE_ENTRIES(a.objname, b.objname, '*NO')) AS c
WHERE USER_NAME NOT LIKE 'Q%'
GROUP BY USER_NAME
ORDER BY TOTAL_SPOOL_SPACE DESC
LIMIT 10;


--  category:  IBM i Services
--  description:  Spool - managing spool

--
-- Preview spooled files to remove
--
call systools.delete_old_spooled_files(delete_older_than => current timestamp - 30 days, 
-- p_output_queue_library_name => , 
-- p_output_queue_name => , 
-- p_user_name => , 
                                       preview => 'YES');

--
-- Remove the spooled files
--
call systools.delete_old_spooled_files(delete_older_than => current timestamp - 30 days, 
                                       preview => 'NO');


--  category:  IBM i Services
--  description:  Storage - ASP management

--
-- description: Review ASP and IASP definition and status
--
select * from qsys2.asp_info
  order by ASP_NUMBER;

--
-- description: Review ASP and IASP storage status
--
select ASP_NUMBER, DEVD_NAME, DISK_UNITS, PRESENT, 
       TOTAL_CAPACITY_AVAILABLE, TOTAL_CAPACITY, 
       DEC(DEC(TOTAL_CAPACITY_AVAILABLE, 19, 2) /
       DEC(TOTAL_CAPACITY, 19, 2) * 100, 19, 2) AS
       AVAILABLE_SPACE
       from qsys2.asp_info ORDER BY 7 ASC;


--  category:  IBM i Services
--  description:  Storage - ASP management

--
-- description: SQL alternative to WRKASPJOB
--
SELECT iasp_name AS iasp,
       iasp_number AS iasp#,
       job_name,
       job_status AS status,
       job_type AS TYPE,
       user_name AS "User",
       subsystem_name AS sbs,
       sql_status,
       sql_stmt,
       sql_time,
       asp_type,
       rdb_name
   FROM qsys2.asp_job_info;


--  category:  IBM i Services
--  description:  Storage - IASP Vary ON and OFF steps

--
-- description: Review the most expensive steps in recent vary ONs
--
SELECT v.* FROM qsys2.asp_vary_info v 
WHERE OPERATION_TYPE = 'VARY ON'
AND END_TIMESTAMP > CURRENT TIMESTAMP - 21 DAYS 
ORDER BY duration DESC; 

--
-- description: Review the most expensive steps in recent vary ONs
--
SELECT iasp_name,       operation_type,
       operation_number,MAX(start_timestamp) AS WHEN,
       BIGINT(SUM(duration)) AS total_seconds
   FROM qsys2.asp_vary_info WHERE DURATION IS NOT NULL
   AND END_TIMESTAMP > CURRENT TIMESTAMP - 21 DAYS
   GROUP BY iasp_name, operation_type, operation_number
   ORDER BY total_seconds DESC;


--  category:  IBM i Services
--  description:  Storage - Media Library

-- Check for unavailable tape drives 
SELECT * FROM QSYS2.MEDIA_LIBRARY_INFO 
  WHERE DEVICE_STATUS = 'VARIED OFF';


--  category:  IBM i Services
--  description:  Storage - NVMe Fuel Gauge

--
-- NVMe health detail
--      
select CAP_MET, LIFE, DEGRADED, TEMP_WARN, TEMP_CRIT, 
       DEVICE_TYPE, RESOURCE_NAME, DEVICE_MODEL,
       SERIAL_NUMBER
  from QSYS2.NVME_INFO;


--  category:  IBM i Services
--  description:  Storage - Review status of all storage H/W

--
-- Query information for all DISKs, order by percentage used
--
SELECT PERCENT_USED, 
       CASE WHEN UNIT_TYPE = 1 
          THEN 'SSD' 
          ELSE 'DISK' END as STORAGE_TYPE, 
       A.* 
FROM QSYS2.SYSDISKSTAT A 
ORDER BY PERCENT_USED DESC;


--  category:  IBM i Services
--  description:  Storage - Storage details for a specific user 

--
-- Retrieve the details of objects owned by a specific user
-- Note: replace user-name with the user profile name of interest
--
SELECT b.objlongschema, b.objname, b.objtype, b.objattribute, b.objcreated, b.objsize, b.objtext, b.days_used_count, b.last_used_timestamp,b.* FROM 
   TABLE (QSYS2.OBJECT_STATISTICS('*ALLUSRAVL ', '*LIB') ) as a, 
   TABLE (QSYS2.OBJECT_STATISTICS(a.objname, 'ALL')  ) AS b
WHERE b.OBJOWNER = 'user-name'
ORDER BY b.OBJSIZE DESC
FETCH FIRST 100 ROWS ONLY;


--  category:  IBM i Services
--  description:  Storage - Temporary storage consumption, by DB workload

--
-- Which active database server connections 
-- are consuming the most temporary storage
--
WITH TOP_TMP_STG (bucket_current_size, q_job_name) AS (
SELECT bucket_current_size, rtrim(job_number) concat '/' concat rtrim(job_user_name) concat '/' concat rtrim(job_name) as q_job_name 
FROM QSYS2.SYSTMPSTG 
WHERE job_status = '*ACTIVE' AND JOB_NAME IN ('QZDASOINIT', 'QZDASSINIT', 'QRWTSRVR', 'QSQSRVR')
ORDER BY bucket_current_size desc fetch first 10 rows only
) SELECT bucket_current_size, q_job_name, V_SQL_STATEMENT_TEXT, B.* FROM TOP_TMP_STG, TABLE(QSYS2.GET_JOB_INFO(q_job_name)) B;


--  category:  IBM i Services
--  description:  Storage - Temporary storage consumption, by active jobs

--
-- Which active jobs are the top consumers of temporary storage?
--
SELECT bucket_current_size, bucket_peak_size, 
  rtrim(job_number) concat '/' 
  concat rtrim(job_user_name) 
  concat '/' 
  concat rtrim(job_name) as q_job_name 
FROM QSYS2.SYSTMPSTG 
WHERE job_status = '*ACTIVE' 
ORDER BY bucket_current_size desc;


--  category:  IBM i Services
--  description:  Storage - Top 10 Spool consumers, by user 

--
-- Find the top 10 consumers of SPOOL storage 
--
SELECT USER_NAME, SUM(SIZE) AS TOTAL_SPOOL_SPACE FROM 
   TABLE (QSYS2.OBJECT_STATISTICS('QSYS      ', '*LIB') ) as a, 
   TABLE (QSYS2.OBJECT_STATISTICS(a.objname, 'OUTQ')  ) AS b, 
   TABLE (QSYS2.OUTPUT_QUEUE_ENTRIES(a.objname, b.objname, '*NO')) AS c
WHERE USER_NAME NOT LIKE 'Q%' 
GROUP BY USER_NAME
ORDER BY TOTAL_SPOOL_SPACE DESC
FETCH FIRST 10 ROWS ONLY;


--  category:  IBM i Services
--  description:  Storage - Top 10 consumers, by user 

--
-- Review the top 10 storage consumers
SELECT A.AUTHORIZATION_NAME, SUM(A.STORAGE_USED) AS TOTAL_STORAGE_USED, B.TEXT_DESCRIPTION, B.ACCOUNTING_CODE, B.MAXIMUM_ALLOWED_STORAGE
  FROM QSYS2.USER_STORAGE A 
  INNER JOIN QSYS2.USER_INFO B ON B.USER_NAME = A.AUTHORIZATION_NAME WHERE B.USER_NAME NOT LIKE 'Q%' 
  GROUP BY A.AUTHORIZATION_NAME, B.TEXT_DESCRIPTION, B.ACCOUNTING_CODE, B.MAXIMUM_ALLOWED_STORAGE
  ORDER BY TOTAL_STORAGE_USED DESC FETCH FIRST 10 ROWS ONLY;


--  category:  IBM i Services
--  description:  Storage - iASP storage consumption

--
--  Format output and break down by iASP
--
SELECT USER_NAME, ASPGRP,
       VARCHAR_FORMAT(MAXSTG, '999,999,999,999,999,999,999,999') AS MAXIMUM_STORAGE_KB,
       VARCHAR_FORMAT(STGUSED,'999,999,999,999,999,999,999,999') AS STORAGE_KB
       FROM QSYS2.USER_STORAGE 
  ORDER BY 4 DESC;


--  category:  IBM i Services
--  description:  System Health - Fastest query of System Limits detail
--  minvrm: V7R3M0

--
-- Show me the historical percentage used for Maximum # of Jobs
--
-- https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/rzajq/rzajqserviceshealth.htm
--
with tt (job_maximum) as (
    select current_numeric_value
      from qsys2.system_value_info
      where system_value_name = 'QMAXJOB'
  )
  select last_change_timestamp as increment_time, current_value as job_count,
         tt.job_maximum,
         dec(dec(current_value, 19, 2) / dec(tt.job_maximum, 19, 2) * 100, 19, 2)
           as percent_consumed
    from qsys2.syslimits_basic, tt
    where limit_id = 19000
    order by Increment_time desc;


--  category:  IBM i Services
--  description:  System Health - System Limits tracking

--
-- Description: Enable alerts for files which are growing near the maximum
--
CL: ALCOBJ OBJ((QSYS2/SYSLIMTBL *FILE *EXCL)) CONFLICT(*RQSRLS) ;
CL: DLCOBJ OBJ((QSYS2/SYSLIMTBL *FILE *EXCL));

CREATE OR REPLACE TRIGGER QSYS2.SYSTEM_LIMITS_LARGE_FILE
	AFTER INSERT ON QSYS2.SYSLIMTBL 
	REFERENCING NEW AS N FOR EACH ROW MODE DB2ROW 
SET OPTION USRPRF=*OWNER, DYNUSRPRF=*OWNER
BEGIN ATOMIC 
DECLARE V_CMDSTMT VARCHAR(200) ;
DECLARE V_ERROR INTEGER;

DECLARE EXIT HANDLER FOR SQLEXCEPTION 
   SET V_ERROR = 1;

/* ------------------------------------------------------------------ */
/* If a table has exceeded 80% of this limit, alert the operator     */
/* ------------------------------------------------------------------ */
/* 15000 == MAXIMUM NUMBER OF ALL ROWS IN A PARTITION                 */
/*          (max size = 4,294,967,288)                                */
/* ------------------------------------------------------------------ */
IF (N.LIMIT_ID = 15000 AND
    N.CURRENT_VALUE > ((select supported_value from qsys2.sql_sizing where sizing_id = 15000) * 0.8)) THEN 

SET V_CMDSTMT = 'SNDMSG MSG(''Table: ' 
     CONCAT N.SYSTEM_SCHEMA_NAME CONCAT '/' CONCAT N.SYSTEM_OBJECT_NAME
     CONCAT ' (' CONCAT N.SYSTEM_TABLE_MEMBER CONCAT 
     ') IS GETTING VERY LARGE - ROW COUNT =  '
     CONCAT CURRENT_VALUE CONCAT ' '') TOUSR(*SYSOPR) MSGTYPE(*INFO) ';
 CALL QSYS2.QCMDEXC( V_CMDSTMT );
END IF;
END;

commit;
--
-- Description: Determine if any user triggers have been created over the System Limits table
--
SELECT * FROM QSYS2.SYSTRIGGERS 
  WHERE EVENT_OBJECT_SCHEMA = 'QSYS2' AND EVENT_OBJECT_TABLE = 'SYSLIMTBL';


--  category:  IBM i Services
--  description:  System Health - Tracking the largest database tables

--
-- Review the largest tables in System Limits 
-- 
 WITH X AS (SELECT ROW_NUMBER() 
            OVER(PARTITION BY SYSTEM_SCHEMA_NAME, 
                 SYSTEM_OBJECT_NAME, SYSTEM_TABLE_MEMBER ORDER BY 
                CURRENT_VALUE DESC NULLS LAST) AS R, U.* 
            FROM QSYS2.SYSLIMITS U 
            WHERE LIMIT_ID = 15000) 
        SELECT LAST_CHANGE_TIMESTAMP, SYSTEM_SCHEMA_NAME, 
          SYSTEM_OBJECT_NAME, SYSTEM_TABLE_MEMBER, 
        CURRENT_VALUE 
        FROM X WHERE R = 1 
        ORDER BY CURRENT_VALUE DESC;


--  category:  IBM i Services
--  description:  What is our journaling setup, by object type
  
SELECT JOURNAL_LIBRARY, JOURNAL_NAME, OBJTYPE, COUNT(*) 
  FROM TABLE(QSYS2.OBJECT_STATISTICS('TOYSTORE', '*ALL')) X
  GROUP BY JOURNAL_LIBRARY, JOURNAL_NAME, OBJTYPE
  ORDER BY 1, 2, 3, 4 DESC;
  

--
-- Which files in a library, are not being journaled?
--  
SELECT * 
  FROM TABLE(QSYS2.OBJECT_STATISTICS('TOYSTORE', '*ALL')) X
  WHERE JOURNAL_LIBRARY IS NULL AND OBJTYPE = '*FILE'
  ORDER BY OBJNAME ASC;


--  category:  IBM i Services
--  description:  What unofficial IBM i code exists in QSYS?

SELECT * FROM TABLE(QSYS2.OBJECT_STATISTICS('QSYS', '*PGM *SRVPGM')) X
  WHERE OBJECT_DOMAIN = '*SYSTEM' and OBJECT_SIGNED = 'NO'
  ORDER BY LAST_USED_TIMESTAMP DESC;


--  category:  IBM i Services
--  description:  Work Management - Active Job Info - Largest Query

--
-- description: Find the 10 QZDASOINIT jobs that have executed the most expensive (by storage) queries
--
SELECT JOB_NAME, LARGEST_QUERY_SIZE, J.*
FROM TABLE(QSYS2.ACTIVE_JOB_INFO(
  subsystem_list_filter => 'QUSRWRK', 
  job_name_filter       => 'QZDASOINIT', 
  detailed_info         => 'ALL')) J
ORDER BY LARGEST_QUERY_SIZE DESC
LIMIT 10;




--  category:  IBM i Services
--  description:  Work Management - Active Job Info - Lock contention

--
-- description: Find the jobs that are encountering the most lock contention
--
SELECT JOB_NAME, DATABASE_LOCK_WAITS, NON_DATABASE_LOCK_WAITS, 
       DATABASE_LOCK_WAITS + NON_DATABASE_LOCK_WAITS as Total_Lock_Waits, J.*
FROM TABLE (QSYS2.ACTIVE_JOB_INFO(DETAILED_INFO => 'ALL')) J
ORDER BY 4 DESC
LIMIT 20;


--  category:  IBM i Services
--  description:  Work Management - Active Job Info - Long running SQL statements

--
-- description: Look for long-running SQL statements for a subset of users
--
SELECT JOB_NAME, authorization_name as "User", 
  TIMESTAMPDIFF(2, CAST(CURRENT TIMESTAMP - SQL_STATEMENT_START_TIMESTAMP AS CHAR(22))) AS execution_seconds,
  TIMESTAMPDIFF(4, CAST(CURRENT TIMESTAMP - SQL_STATEMENT_START_TIMESTAMP AS CHAR(22))) AS execution_minutes,
  TIMESTAMPDIFF(8, CAST(CURRENT TIMESTAMP - SQL_STATEMENT_START_TIMESTAMP AS CHAR(22))) AS execution_hours,
  SQL_STATEMENT_TEXT, J.*      
FROM TABLE(QSYS2.ACTIVE_JOB_INFO(
             CURRENT_USER_LIST_FILTER => 'SCOTTF,SLROMANO,JELSBURY',
             DETAILED_INFO            => 'ALL')) J
WHERE SQL_STATEMENT_STATUS = 'ACTIVE'  
ORDER BY 2 DESC
LIMIT 30;
 


--  category:  IBM i Services
--  description:  Work Management - Active Job Info - QTEMP consumption
 
--
-- description: Identify Host Server jobs currently using >10 Meg of QTEMP
--
SELECT qtemp_size, job_name,
   internal_job_id, subsystem, subsystem_library_name, authorization_name, job_type,
   function_type, "FUNCTION", job_status, memory_pool, run_priority, thread_count,
   temporary_storage, cpu_time, total_disk_io_count, elapsed_interaction_count,
   elapsed_total_response_time, elapsed_total_disk_io_count,
   elapsed_async_disk_io_count, elapsed_sync_disk_io_count, elapsed_cpu_percentage,
   elapsed_cpu_time, elapsed_page_fault_count, job_end_reason, server_type, elapsed_time
FROM TABLE(qsys2.active_job_info(
  subsystem_list_filter => 'QUSRWRK', 
  job_name_filter       => 'QZDASOINIT', 
  detailed_info         => 'QTEMP'))
WHERE qtemp_size > 10; 


--  category:  IBM i Services
--  description:  Work Management - Active Job Info - Temp storage top consumers
 
--
-- description: Find active jobs using the most temporary storage. 
--
SELECT JOB_NAME, AUTHORIZATION_NAME, TEMPORARY_STORAGE, SQL_STATEMENT_TEXT, J.*
  FROM TABLE (QSYS2.ACTIVE_JOB_INFO(DETAILED_INFO => 'ALL')) J
   WHERE JOB_TYPE <> 'SYS' ORDER BY TEMPORARY_STORAGE DESC ;


--  category:  IBM i Services
--  description:  Work Management - Active Job info - Longest active DRDA connections

--
-- Find the active DRDA jobs and compute the connection duration
--
WITH ACTIVE_USER_JOBS (Q_JOB_NAME,  CPU_TIME, RUN_PRIORITY) AS ( 
SELECT JOB_NAME, CPU_TIME, RUN_PRIORITY FROM TABLE (ACTIVE_JOB_INFO('NO','','QRWTSRVR','')) x 
WHERE JOB_STATUS <> 'PSRW'
) SELECT Q_JOB_NAME, 
ABS( CURRENT TIMESTAMP - MESSAGE_TIMESTAMP ) AS CONNECTION_DURATION, CPU_TIME, RUN_PRIORITY, B.* 
FROM ACTIVE_USER_JOBS, TABLE(QSYS2.JOBLOG_INFO(Q_JOB_NAME)) B 
WHERE MESSAGE_ID = 'CPI3E01'   
ORDER BY CONNECTION_DURATION DESC ; 


--  category:  IBM i Services
--  description:  Work Management - Active Job info - Longest running SQL statements

--
-- Find the jobs with SQL statements executing and order the results by duration of SQL statement execution
--
WITH ACTIVE_USER_JOBS (Q_JOB_NAME, AUTHORIZATION_NAME, CPU_TIME, RUN_PRIORITY) AS ( 
SELECT JOB_NAME, AUTHORIZATION_NAME, CPU_TIME, RUN_PRIORITY FROM TABLE (ACTIVE_JOB_INFO('NO','','','')) x 
WHERE JOB_TYPE <> 'SYS' 
) SELECT Q_JOB_NAME, AUTHORIZATION_NAME, CPU_TIME, RUN_PRIORITY, V_SQL_STATEMENT_TEXT, 
ABS( CURRENT TIMESTAMP - V_SQL_STMT_START_TIMESTAMP )  AS SQL_STMT_DURATION, B.* 
FROM ACTIVE_USER_JOBS, TABLE(QSYS2.GET_JOB_INFO(Q_JOB_NAME)) B 
WHERE V_SQL_STMT_STATUS = 'ACTIVE'   
ORDER BY SQL_STMT_DURATION DESC ; 


--  category:  IBM i Services
--  description:  Work Management - Active Job info - SQL Server Mode study

--
-- Find active QSQSRVR jobs and the owning application job
--
WITH tt (authorization_name, job_name, cpu_time, total_disk_io_count)
AS (
select authorization_name, job_name, cpu_time, total_disk_io_count from
table(qsys2.active_job_info(
SUBSYSTEM_LIST_FILTER=>'QSYSWRK',
JOB_NAME_FILTER=>'QSQSRVR')) x
)
select authorization_name, ss.message_text, job_name, cpu_time,
total_disk_io_count
from tt, table(qsys2.joblog_info(job_name)) ss where message_id = 'CPF9898' and
from_program = 'QSQSRVR'
ORDER BY CPU_TIME DESC;


--  category:  IBM i Services
--  description:  Work Management - Active Job info - Temp storage consumers, by memory pool

--
-- Find the top 4 consumers of temporary storage, by memory pool
--
WITH TOP_CONSUMERS (JOB_NAME, MEMORY_POOL, AUTHORIZATION_NAME, FUNCTION_TYPE, FUNCTION, TEMPORARY_STORAGE, RANK) AS (
        SELECT JOB_NAME, MEMORY_POOL, AUTHORIZATION_NAME, FUNCTION_TYPE, FUNCTION, TEMPORARY_STORAGE, RANK() OVER (
                   PARTITION BY MEMORY_POOL
                   ORDER BY TEMPORARY_STORAGE DESC
               )
            FROM TABLE (
                    ACTIVE_JOB_INFO()
                ) x
            WHERE JOB_TYPE <> 'SYS'
    )
    SELECT JOB_NAME, MEMORY_POOL, AUTHORIZATION_NAME, FUNCTION_TYPE CONCAT '-' CONCAT FUNCTION AS FUNCTION,
           TEMPORARY_STORAGE
        FROM TOP_CONSUMERS
        WHERE RANK IN (1, 2, 3, 4)
        ORDER BY MEMORY_POOL DESC;


--  category:  IBM i Services
--  description:  Work Management - Active Job info - Top ZDA CPU consumers
--  minvrm:  v7r2m0
--  Note: this is available at IBM i 7.2 and higher, because it uses named parameter syntax... <parameter name> => <parameter value>


-- Examine active Host Server jobs and find the top consumers
SELECT JOB_NAME, AUTHORIZATION_NAME,  ELAPSED_CPU_PERCENTAGE,ELAPSED_TOTAL_DISK_IO_COUNT, ELAPSED_PAGE_FAULT_COUNT, X.*
	FROM TABLE(ACTIVE_JOB_INFO(
		   JOB_NAME_FILTER => 'QZDASOINIT',
		   SUBSYSTEM_LIST_FILTER => 'QUSRWRK')) x
ORDER BY ELAPSED_CPU_PERCENTAGE DESC
FETCH FIRST 10 ROWS ONLY;


--  category:  IBM i Services
--  description:  Work Management - Active Subsystem detail

select subsystem_description_library, subsystem_description, maximum_active_jobs,
       current_active_jobs, subsystem_monitor_job, text_description,
       controlling_subsystem, workload_group, signon_device_file_library,
       signon_device_file, secondary_language_library, iasp_name
  from qsys2.subsystem_info
  where status = 'ACTIVE'
  order by current_active_jobs desc;


--  category:  IBM i Services
--  description:  Work Management - Communications Entry Info
--  minvrm: V7R3M0
--

-- List all the communications entries defined for the QCMN subsystem
select *
  from qsys2.communications_entry_info
  where subsystem_description_library = 'QSYS' and
        subsystem_description = 'QCMN';


--  category:  IBM i Services
--  description:  Work Management - Interactive jobs

--
-- Find all interactive jobs 
--
SELECT * FROM TABLE(QSYS2.JOB_INFO(JOB_TYPE_FILTER => '*INTERACT')) X;


--  category:  IBM i Services
--  description:  Work Management - Job Description Initial Library List

--
-- If we plan to delete a library, use SQL to determine whether any job descriptions 
-- include that library name in its INLLIBL.

-- Examine the library lists for every job description.
-- Since the library list column returns a character string containing a list of libraries,
-- to see the individual library names it needs to be broken apart. 
-- To do this, you can create a table function that takes the library list string and returns a list of library names.

CREATE OR REPLACE FUNCTION systools.get_lib_names (
         jobd_libl VARCHAR(2750),
         jobd_libl_cnt INT
      )
   RETURNS TABLE (
      libl_position INT, library_name VARCHAR(10)
   )
   BEGIN
      DECLARE in_pos INT;
      DECLARE lib_cnt INT;
      SET in_pos = 1;
      SET lib_cnt = 1;
      WHILE lib_cnt <= jobd_libl_cnt DO
         PIPE (
            lib_cnt,
            RTRIM((SUBSTR(jobd_libl, in_pos, 10)))
         );
         SET in_pos = in_pos + 11;
         SET lib_cnt = lib_cnt + 1;
      END WHILE;
      RETURN;
   END;
 
--
-- Use the function to interrogate the use of libraries in jobd's libl
--
SELECT job_description,
       job_description_library,
       libl_position,
       library_name
   FROM qsys2.job_description_info,
        TABLE (
           systools.get_lib_names(library_list, library_list_count)
        ) x
   WHERE library_name = 'QGPL';
                             


--  category:  IBM i Services
--  description:  Work Management - Job Descriptions

--
-- description: compare job descriptions between production and DR or HA
-- (note change xxxxxxx to be the RDB name of the target for comparison)
--           
DECLARE GLOBAL TEMPORARY TABLE SESSION . remote_job_descriptions
   (job_description_library, job_description, authorization_name, job_date,
      accounting_code, routing_data, request_data, library_list_count, library_list,
      job_switches, text_description, job_queue_library, job_queue, job_queue_priority,
      hold_on_job_queue, output_queue_library, output_queue, output_queue_priority,
      spooled_file_action, printer_device, print_text, job_message_queue_maximum_size,
      job_message_queue_full_action, syntax_check_severity, job_end_severity,
      joblog_output, inquiry_message_reply, message_logging_level,
      message_logging_severity, message_logging_text, log_cl_program_commands,
      device_recovery_action, time_slice_end_pool, allow_multiple_threads,
      workload_group, aspgrp, ddm_conversation)
   AS (SELECT *
          FROM xxxxxxx.qsys2.job_description_info jd)
   WITH DATA WITH REPLACE;

-- 
-- Any rows returned represent a difference
--
SELECT 'Production' AS "System Name",
  A.JOB_DESCRIPTION_LIBRARY, A.JOB_DESCRIPTION, A.AUTHORIZATION_NAME, A.JOB_DATE, A.ACCOUNTING_CODE, A.ROUTING_DATA, A.REQUEST_DATA, A.LIBRARY_LIST_COUNT,
  A.LIBRARY_LIST, A.JOB_SWITCHES, A.TEXT_DESCRIPTION, A.JOB_QUEUE_LIBRARY, A.JOB_QUEUE, A.JOB_QUEUE_PRIORITY, A.HOLD_ON_JOB_QUEUE, A.OUTPUT_QUEUE_LIBRARY,
  A.OUTPUT_QUEUE, A.OUTPUT_QUEUE_PRIORITY, A.SPOOLED_FILE_ACTION, A.PRINTER_DEVICE, A.PRINT_TEXT, A.JOB_MESSAGE_QUEUE_MAXIMUM_SIZE,
  A.JOB_MESSAGE_QUEUE_FULL_ACTION, A.SYNTAX_CHECK_SEVERITY, A.JOB_END_SEVERITY, A.JOBLOG_OUTPUT, A.INQUIRY_MESSAGE_REPLY, A.MESSAGE_LOGGING_LEVEL,
  A.MESSAGE_LOGGING_SEVERITY, A.MESSAGE_LOGGING_TEXT, A.LOG_CL_PROGRAM_COMMANDS, A.DEVICE_RECOVERY_ACTION, A.TIME_SLICE_END_POOL, A.ALLOW_MULTIPLE_THREADS,
  A.ASPGRP, A.DDM_CONVERSATION
	FROM qsys2.job_description_info A LEFT EXCEPTION JOIN SESSION.remote_job_descriptions B 
    ON  A.JOB_DESCRIPTION_LIBRARY IS NOT DISTINCT FROM b.JOB_DESCRIPTION_LIBRARY
	AND A.JOB_DESCRIPTION IS NOT DISTINCT FROM b.JOB_DESCRIPTION
	AND A.AUTHORIZATION_NAME IS NOT DISTINCT FROM b.AUTHORIZATION_NAME
	AND A.JOB_DATE IS NOT DISTINCT FROM b.JOB_DATE
	AND A.ACCOUNTING_CODE IS NOT DISTINCT FROM b.ACCOUNTING_CODE
	AND A.ROUTING_DATA IS NOT DISTINCT FROM b.ROUTING_DATA
	AND A.REQUEST_DATA IS NOT DISTINCT FROM b.REQUEST_DATA
	AND A.LIBRARY_LIST_COUNT IS NOT DISTINCT FROM b.LIBRARY_LIST_COUNT
	AND A.LIBRARY_LIST IS NOT DISTINCT FROM b.LIBRARY_LIST
	AND A.JOB_SWITCHES IS NOT DISTINCT FROM b.JOB_SWITCHES
	AND A.TEXT_DESCRIPTION IS NOT DISTINCT FROM b.TEXT_DESCRIPTION
	AND A.JOB_QUEUE_LIBRARY IS NOT DISTINCT FROM b.JOB_QUEUE_LIBRARY
	AND A.JOB_QUEUE IS NOT DISTINCT FROM b.JOB_QUEUE
	AND A.JOB_QUEUE_PRIORITY IS NOT DISTINCT FROM b.JOB_QUEUE_PRIORITY
	AND A.HOLD_ON_JOB_QUEUE IS NOT DISTINCT FROM b.HOLD_ON_JOB_QUEUE
	AND A.OUTPUT_QUEUE_LIBRARY IS NOT DISTINCT FROM b.OUTPUT_QUEUE_LIBRARY
	AND A.OUTPUT_QUEUE IS NOT DISTINCT FROM b.OUTPUT_QUEUE
	AND A.OUTPUT_QUEUE_PRIORITY IS NOT DISTINCT FROM b.OUTPUT_QUEUE_PRIORITY
	AND A.SPOOLED_FILE_ACTION IS NOT DISTINCT FROM b.SPOOLED_FILE_ACTION
	AND A.PRINTER_DEVICE IS NOT DISTINCT FROM b.PRINTER_DEVICE
	AND A.PRINT_TEXT IS NOT DISTINCT FROM b.PRINT_TEXT
	AND A.JOB_MESSAGE_QUEUE_MAXIMUM_SIZE IS NOT DISTINCT FROM b.JOB_MESSAGE_QUEUE_MAXIMUM_SIZE
	AND A.JOB_MESSAGE_QUEUE_FULL_ACTION IS NOT DISTINCT FROM b.JOB_MESSAGE_QUEUE_FULL_ACTION
	AND A.SYNTAX_CHECK_SEVERITY IS NOT DISTINCT FROM b.SYNTAX_CHECK_SEVERITY
	AND A.JOB_END_SEVERITY IS NOT DISTINCT FROM b.JOB_END_SEVERITY
	AND A.JOBLOG_OUTPUT IS NOT DISTINCT FROM b.JOBLOG_OUTPUT
	AND A.INQUIRY_MESSAGE_REPLY IS NOT DISTINCT FROM b.INQUIRY_MESSAGE_REPLY
	AND A.MESSAGE_LOGGING_LEVEL IS NOT DISTINCT FROM b.MESSAGE_LOGGING_LEVEL
	AND A.MESSAGE_LOGGING_SEVERITY IS NOT DISTINCT FROM b.MESSAGE_LOGGING_SEVERITY
	AND A.MESSAGE_LOGGING_TEXT IS NOT DISTINCT FROM b.MESSAGE_LOGGING_TEXT
	AND A.LOG_CL_PROGRAM_COMMANDS IS NOT DISTINCT FROM b.LOG_CL_PROGRAM_COMMANDS
	AND A.DEVICE_RECOVERY_ACTION IS NOT DISTINCT FROM b.DEVICE_RECOVERY_ACTION
	AND A.TIME_SLICE_END_POOL IS NOT DISTINCT FROM b.TIME_SLICE_END_POOL
	AND A.ALLOW_MULTIPLE_THREADS IS NOT DISTINCT FROM b.ALLOW_MULTIPLE_THREADS
	AND A.ASPGRP IS NOT DISTINCT FROM b.ASPGRP
	AND A.DDM_CONVERSATION IS NOT DISTINCT FROM b.DDM_CONVERSATION
union all
SELECT 'Failover' AS "System Name",
  B.JOB_DESCRIPTION_LIBRARY, B.JOB_DESCRIPTION, B.AUTHORIZATION_NAME, B.JOB_DATE, B.ACCOUNTING_CODE, B.ROUTING_DATA,
  B.REQUEST_DATA, B.LIBRARY_LIST_COUNT, B.LIBRARY_LIST, B.JOB_SWITCHES, B.TEXT_DESCRIPTION, B.JOB_QUEUE_LIBRARY,
  B.JOB_QUEUE, B.JOB_QUEUE_PRIORITY, B.HOLD_ON_JOB_QUEUE, B.OUTPUT_QUEUE_LIBRARY, B.OUTPUT_QUEUE, B.OUTPUT_QUEUE_PRIORITY, B.SPOOLED_FILE_ACTION,
  B.PRINTER_DEVICE, B.PRINT_TEXT, B.JOB_MESSAGE_QUEUE_MAXIMUM_SIZE, B.JOB_MESSAGE_QUEUE_FULL_ACTION, B.SYNTAX_CHECK_SEVERITY, B.JOB_END_SEVERITY,
  B.JOBLOG_OUTPUT, B.INQUIRY_MESSAGE_REPLY, B.MESSAGE_LOGGING_LEVEL, B.MESSAGE_LOGGING_SEVERITY, B.MESSAGE_LOGGING_TEXT, B.LOG_CL_PROGRAM_COMMANDS,
  B.DEVICE_RECOVERY_ACTION, B.TIME_SLICE_END_POOL, B.ALLOW_MULTIPLE_THREADS, B.ASPGRP, B.DDM_CONVERSATION
	FROM qsys2.job_description_info A RIGHT EXCEPTION JOIN SESSION.remote_job_descriptions B 
    ON  A.JOB_DESCRIPTION_LIBRARY IS NOT DISTINCT FROM b.JOB_DESCRIPTION_LIBRARY
	AND A.JOB_DESCRIPTION IS NOT DISTINCT FROM b.JOB_DESCRIPTION
	AND A.AUTHORIZATION_NAME IS NOT DISTINCT FROM b.AUTHORIZATION_NAME
	AND A.JOB_DATE IS NOT DISTINCT FROM b.JOB_DATE
	AND A.ACCOUNTING_CODE IS NOT DISTINCT FROM b.ACCOUNTING_CODE
	AND A.ROUTING_DATA IS NOT DISTINCT FROM b.ROUTING_DATA
	AND A.REQUEST_DATA IS NOT DISTINCT FROM b.REQUEST_DATA
	AND A.LIBRARY_LIST_COUNT IS NOT DISTINCT FROM b.LIBRARY_LIST_COUNT
	AND A.LIBRARY_LIST IS NOT DISTINCT FROM b.LIBRARY_LIST
	AND A.JOB_SWITCHES IS NOT DISTINCT FROM b.JOB_SWITCHES
	AND A.TEXT_DESCRIPTION IS NOT DISTINCT FROM b.TEXT_DESCRIPTION
	AND A.JOB_QUEUE_LIBRARY IS NOT DISTINCT FROM b.JOB_QUEUE_LIBRARY
	AND A.JOB_QUEUE IS NOT DISTINCT FROM b.JOB_QUEUE
	AND A.JOB_QUEUE_PRIORITY IS NOT DISTINCT FROM b.JOB_QUEUE_PRIORITY
	AND A.HOLD_ON_JOB_QUEUE IS NOT DISTINCT FROM b.HOLD_ON_JOB_QUEUE
	AND A.OUTPUT_QUEUE_LIBRARY IS NOT DISTINCT FROM b.OUTPUT_QUEUE_LIBRARY
	AND A.OUTPUT_QUEUE IS NOT DISTINCT FROM b.OUTPUT_QUEUE
	AND A.OUTPUT_QUEUE_PRIORITY IS NOT DISTINCT FROM b.OUTPUT_QUEUE_PRIORITY
	AND A.SPOOLED_FILE_ACTION IS NOT DISTINCT FROM b.SPOOLED_FILE_ACTION
	AND A.PRINTER_DEVICE IS NOT DISTINCT FROM b.PRINTER_DEVICE
	AND A.PRINT_TEXT IS NOT DISTINCT FROM b.PRINT_TEXT
	AND A.JOB_MESSAGE_QUEUE_MAXIMUM_SIZE IS NOT DISTINCT FROM b.JOB_MESSAGE_QUEUE_MAXIMUM_SIZE
	AND A.JOB_MESSAGE_QUEUE_FULL_ACTION IS NOT DISTINCT FROM b.JOB_MESSAGE_QUEUE_FULL_ACTION
	AND A.SYNTAX_CHECK_SEVERITY IS NOT DISTINCT FROM b.SYNTAX_CHECK_SEVERITY
	AND A.JOB_END_SEVERITY IS NOT DISTINCT FROM b.JOB_END_SEVERITY
	AND A.JOBLOG_OUTPUT IS NOT DISTINCT FROM b.JOBLOG_OUTPUT
	AND A.INQUIRY_MESSAGE_REPLY IS NOT DISTINCT FROM b.INQUIRY_MESSAGE_REPLY
	AND A.MESSAGE_LOGGING_LEVEL IS NOT DISTINCT FROM b.MESSAGE_LOGGING_LEVEL
	AND A.MESSAGE_LOGGING_SEVERITY IS NOT DISTINCT FROM b.MESSAGE_LOGGING_SEVERITY
	AND A.MESSAGE_LOGGING_TEXT IS NOT DISTINCT FROM b.MESSAGE_LOGGING_TEXT
	AND A.LOG_CL_PROGRAM_COMMANDS IS NOT DISTINCT FROM b.LOG_CL_PROGRAM_COMMANDS
	AND A.DEVICE_RECOVERY_ACTION IS NOT DISTINCT FROM b.DEVICE_RECOVERY_ACTION
	AND A.TIME_SLICE_END_POOL IS NOT DISTINCT FROM b.TIME_SLICE_END_POOL
	AND A.ALLOW_MULTIPLE_THREADS IS NOT DISTINCT FROM b.ALLOW_MULTIPLE_THREADS
	AND A.ASPGRP IS NOT DISTINCT FROM b.ASPGRP
	AND A.DDM_CONVERSATION IS NOT DISTINCT FROM b.DDM_CONVERSATION 
ORDER BY JOB_DESCRIPTION_LIBRARY, JOB_DESCRIPTION;


--  category:  IBM i Services
--  description:  Work Management - Job Queues

--
-- Review the job queues with the most pending jobs
--
SELECT * FROM qsys2.job_queue_info
 ORDER BY NUMBER_OF_JOBS DESC
 LIMIT 10;


--  category:  IBM i Services
--  description:  Work Management - Jobs that are waiting to run

--
-- Find jobs sitting on a job queue, waiting to run
--
SELECT * FROM TABLE(QSYS2.JOB_INFO(JOB_STATUS_FILTER    => '*JOBQ')) X;


--  category:  IBM i Services
--  description:  Work Management - Locks held by the current job

select *
  from table (
      qsys2.job_lock_info(job_name => '*')
    )
  order by object_library, object_name, object_type;
                             


--  category:  IBM i Services
--  description:  Work Management - Object lock info

--
-- Review detail about all object lock holders over TOYSTORE/EMPLOYEE *FILE
--
WITH LOCK_CONFLICT_TABLE (object_name, lock_state, q_job_name) AS (
SELECT object_name, lock_state, job_name
FROM QSYS2.OBJECT_LOCK_INFO where 
 object_schema = 'TOYSTORE' and 
 object_name = 'EMPLOYEE'
) SELECT object_name, lock_state, q_job_name, V_SQL_STATEMENT_TEXT, V_CLIENT_IP_ADDRESS, 
   B.* FROM LOCK_CONFLICT_TABLE, 
TABLE(QSYS2.GET_JOB_INFO(q_job_name)) B;


--  category:  IBM i Services
--  description:  Work Management - Object lock info

--  Example showing how to use IBM i Services to capture point of failure
--  detail within an SQL procedure, function or trigger

--  One time setup steps
CL: CRTLIB APPLIB;
CREATE OR REPLACE TABLE APPLIB.HARD_TO_DEBUG_PROBLEMS AS 
   (SELECT * FROM TABLE(QSYS2.JOBLOG_INFO('*')) X) WITH NO DATA ON REPLACE PRESERVE ROWS;
CREATE OR REPLACE TABLE APPLIB.HARD_TO_DEBUG_LOCK_PROBLEMS LIKE 
   QSYS2.OBJECT_LOCK_INFO ON REPLACE PRESERVE ROWS;

create or replace procedure toystore.update_sales(IN P_PERSON VARCHAR(50),
IN P_SALES INTEGER, IN P_DATE DATE)
LANGUAGE SQL
BEGIN
-- Handler code
DECLARE EXIT HANDLER FOR SQLSTATE '57033' 
  BEGIN  /* Message: [SQL0913] Object in use. */
  DECLARE SCHEMA_NAME VARCHAR(128);
  DECLARE TABLE_NAME VARCHAR(128);
  DECLARE DOT_LOCATION INTEGER;
  DECLARE MSG_TOKEN CLOB(1K);

  GET DIAGNOSTICS condition 1 MSG_TOKEN = db2_ordinal_token_1;
  SET DOT_LOCATION = LOCATE_IN_STRING(MSG_TOKEN, '.');

  SET SCHEMA_NAME = RTRIM(SUBSTR(MSG_TOKEN, 1, DOT_LOCATION - 1));
  SET TABLE_NAME = RTRIM(SUBSTR(MSG_TOKEN, DOT_LOCATION + 1, LENGTH(MSG_TOKEN) - DOT_LOCATION));
  INSERT INTO APPLIB.HARD_TO_DEBUG_PROBLEMS
    SELECT * FROM TABLE(QSYS2.JOBLOG_INFO('*')) A
    ORDER BY A.ORDINAL_POSITION DESC
    FETCH FIRST 5 ROWS ONLY;

  INSERT INTO APPLIB.HARD_TO_DEBUG_LOCK_PROBLEMS
    SELECT * FROM QSYS2.OBJECT_LOCK_INFO
     WHERE OBJECT_SCHEMA = SCHEMA_NAME AND OBJECT_NAME = TABLE_NAME;
  SET MSG_TOKEN =
	 SCHEMA_NAME CONCAT '.' CONCAT TABLE_NAME CONCAT ' LOCK FAILURE. See APPLIB.HARD_TO_DEBUG_LOCK_PROBLEMS';  
  RESIGNAL SQLSTATE '57033' SET MESSAGE_TEXT = MSG_TOKEN;
  END;

-- Mainline procedure code
update toystore.sales set sales = sales + p_sales
where sales_person = p_person and sales_date = p_date;

end;

--
-- From a different job:
CL:ALCOBJ OBJ((TOYSTORE/SALES *FILE *EXCLRD)) CONFLICT(*RQSRLS);

--
-- Try to update the sales
CALL toystore.update_sales('LUCCHESSI', 14, '1995-12-31');
-- SQL State: 57033 
-- Vendor Code: -438 
-- Message: [SQL0438] TOYSTORE.SALES LOCK FAILURE. See APPLIB.HARD_TO_DEBUG_LOCK_PROBLEMS
 
SELECT * FROM APPLIB.HARD_TO_DEBUG_PROBLEMS;
SELECT * FROM APPLIB.HARD_TO_DEBUG_LOCK_PROBLEMS;



--  category:  IBM i Services
--  description:  Work Management - Open Files
--  minvrm: V7R3M0
--

--
-- Examine the open files in jobs that have pending database changes
--
select job_name, commitment_definition, state_timestamp,o.*
  from qsys2.db_transaction_info d, lateral (
         select *
           from table (
               qsys2.open_files(d.job_name)
             )
       ) o
  where (local_record_changes_pending = 'YES' or
         local_object_changes_pending = 'YES') and
        o.library_name not in ('QSYS', 'QSYS2', 'SYSIBM'); 
        


--  category:  IBM i Services
--  description:  Work Management - Prestart job statistical review

-- Review the prestart job statistics for all active prestart jobs
with pjs (sbslib, sbs, pgmlib, pgm, pj) as (
       -- active subsystems that have prestart jobs
       select subsystem_description_library, subsystem_description,
              prestart_job_program_library, prestart_job_program, prestart_job_name
         from qsys2.prestart_job_info
         where subsystem_active = 'YES'
     ),
     active_pjs (sbslib, sbs, pgmlib, pgm, pj) as (
       -- active pjs
       select distinct sbslib, sbs, pgmlib, pgm, pj
         from pjs,
              lateral (
                select *
                  from table (
                      qsys2.job_info(
                        job_status_filter => '*ACTIVE', job_subsystem_filter => sbs,
                        job_user_filter => '*ALL')
                    )
                  where job_type_enhanced = 'PRESTART_BATCH'
                        and trim(
                          substr(job_name, locate_in_string(job_name, '/', 1, 2) + 1, 10))
                        = pj
              ) xpj
     )
  -- active pjs and statistics
  select sbslib, sbs, pgmlib, pgm, pj, stat.*
    from active_pjs, lateral (
           select *
             from table (
                 qsys2.prestart_job_statistics(sbs, pgmlib, pgm)
               )
         ) as stat
    order by 1, 2, 3;
         
;
     


--  category:  IBM i Services
--  description:  Work Management - QBATCH routing entries

select sequence_number, program_library, program_name, class_library, class_name,
       comparison_data, comparison_start
  from qsys2.routing_entry_info
  where subsystem_description_library = 'QSYS'
        and subsystem_description = 'QBATCH'
  order by sequence_number;


--  category:  IBM i Services
--  description:  Work Management - QSYSWRK subsystem autostart jobs

select autostart_job_name, job_description_library, job_description
  from qsys2.autostart_job_info
  where subsystem_description_library = 'QSYS'
        and subsystem_description = 'QSYSWRK'
  order by 1, 2, 3;


--  category:  IBM i Services
--  description:  Work Management - QUSRWRK prestart jobs configured with limited reuse

select maximum_uses, pj.*
  from qsys2.prestart_job_info pj
  where subsystem_description_library = 'QSYS'
        and subsystem_description = 'QUSRWRK'
        and pj.maximum_uses <> -1
  order by 1;
                             


--  category:  IBM i Services
--  description:  Work Management - Record lock info

--
-- Review detail about all record locks held over TOYSTORE/EMPLOYEE *FILE
--
WITH LOCK_CONFLICT_TABLE (
  table_name, lock_state, rrn, q_job_name) AS (
SELECT table_name, lock_state, rrn, job_name
FROM QSYS2.RECORD_LOCK_INFO where 
  table_schema = 'TOYSTORE' and 
  table_name = 'EMPLOYEE'
) SELECT table_name, lock_state, rrn, 
         q_job_name, V_SQL_STATEMENT_TEXT, 
         V_CLIENT_IP_ADDRESS, 
         B.* FROM LOCK_CONFLICT_TABLE, 
TABLE(QSYS2.GET_JOB_INFO(q_job_name)) B;



--  category:  IBM i Services
--  description:  Work Management - SET_SERVER_SBS_ROUTING and ad hoc users

--
-- Construct a subsystem that will constrain the amount of system resources
-- available to users who are known to execute ad hoc queries.
--
CL: CRTSBSD SBSD(QGPL/ADHOCSBS) POOLS((1 *BASE)) TEXT('Ad hoc users SBS');
CL: CRTJOBQ QGPL/ADHOCJOBQ TEXT('Ad hoc users job queue');
CL: ADDJOBQE SBSD(QGPL/ADHOCSBS) JOBQ(QGPL/ADHOCJOBQ) MAXACT(100) SEQNBR(40);
CL: CRTCLS CLS(QGPL/ADHOCCLS) RUNPTY(55) TIMESLICE(100) TEXT('Ad hoc class');
CL: ADDPJE SBSD(QGPL/ADHOCSBS) PGM(QSYS/QRWTSRVR) JOBD(QGPL/QDFTSVR) 	CLS(QGPL/ADHOCCLS);
CL: ADDPJE SBSD(QGPL/ADHOCSBS) PGM(QSYS/QZDASOINIT) JOBD(QGPL/QDFTSVR) 	CLS(QGPL/ADHOCCLS);
CL: STRSBS SBSD(QGPL/ADHOCSBS);
--
-- Relocate SCOTT's server jobs to the ADHOCSBS
--
CALL QSYS2.SET_SERVER_SBS_ROUTING('SCOTT','*ALL','ADHOCSBS');

--
-- Review existing configurations for users and groups
--
SELECT * FROM QSYS2.SERVER_SBS_ROUTING;


--  category:  IBM i Services
--  description:  Work Management - Scheduled Job Info

--
-- Example: Review the job scheduled entries which are no longer in effect, either because they 
-- were explicitly held or because they were scheduled to run a single time and the date has 
-- passed.
--
SELECT * FROM QSYS2.SCHEDULED_JOB_INFO  WHERE STATUS IN ('HELD', 'SAVED') ORDER BY SCHEDULED_BY;


--  category:  IBM i Services
--  description:  Work Management - Subsystem pool detail

select subsystem_description_library, subsystem_description, pool_id, pool_name,
       maximum_active_jobs, pool_size
  from qsys2.subsystem_pool_info
  order by pool_id, pool_size desc;


--  category:  IBM i Services
--  description:  Work Management - Subsystem workstation configuration

select subsystem_description_library, subsystem_description, workstation_name,
       workstation_type, job_description_library, job_description, allocation,
       maximum_active_jobs, subsystem_description, workstation_type,
       job_description_library, job_description, allocation, maximum_active_jobs
  from qsys2.workstation_info
  order by subsystem_description_library, subsystem_description;


--  category:  IBM i Services
--  description:  Work Management - System Status

--
-- Return storage and CPU status for the partition. 
-- Specify to reset all the elapsed values to 0.
--
SELECT * FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES')) X;

-- deleay 60 seconds
cl: dllyjob dly(60);

--
-- Repeat the query, observing the elapsed detail
-- 
SELECT elapsed_time, elapsed_cpu_used, elapsed_cpu_shared,
   elapsed_cpu_uncapped_capacity, total_jobs_in_system, maximum_jobs_in_system,
   active_jobs_in_system, interactive_jobs_in_system, configured_cpus,
   cpu_sharing_attribute, current_cpu_capacity, average_cpu_rate,
   average_cpu_utilization, minimum_cpu_utilization, maximum_cpu_utilization,
   sql_cpu_utilization, main_storage_size, system_asp_storage, total_auxiliary_storage,
   system_asp_used, current_temporary_storage, maximum_temporary_storage_used,
   permanent_address_rate, temporary_address_rate, temporary_256mb_segments,
   temporary_4gb_segments, permanent_256mb_segments, permanent_4gb_segments, host_name
   FROM TABLE(qsys2.system_status()) x;


--  category:  IBM i Services
--  description:  Work Management - System Status

--
-- Review the ASP consumption vs limit
--
with sysval(low_limit) as (
select current_numeric_value/10000.0 as QSTGLOWLMT
  from qsys2.system_value_info
  where system_value_name = 'QSTGLOWLMT'
)
select SYSTEM_ASP_USED, 
       DEC((100.00 - low_limit),4,2) as SYSTEM_ASP_LIMIT 
from sysval, qsys2.SYSTEM_STATUS_INFO ;
   


--  category:  IBM i Services
--  description:  Work Management - System Status Info Basic
--  minvrm: V7R3M0
--

--
-- Review the ASP consumption vs limit
--
with sysval (low_limit) as (
       select current_numeric_value / 10000.0
         from qsys2.system_value_info
         where system_value_name = 'QSTGLOWLMT'
     ),
     sysval2 (low_limit_action) as (
       select current_character_value
         from qsys2.system_value_info
         where system_value_name = 'QSTGLOWACN'
     )
  select system_asp_used, 
         dec((100.00 - low_limit), 4, 2) as system_asp_limit, 
         low_limit,
         low_limit_action
    from sysval, sysval2, qsys2.system_status_info_basic;


--  category:  IBM i Services
--  description:  Work Management - System Values

-- Note: replace REMOTEPART with the name of the remote partition
--       (WRKRDBDIRE or QSYS2.SYSCATALOGS)

-- Compare System Values across two partitions 
 DECLARE GLOBAL TEMPORARY TABLE SESSION.Remote_System_Values 
 ( SYSTEM_VALUE_NAME,CURRENT_NUMERIC_VALUE,CURRENT_CHARACTER_VALUE ) 
 AS (SELECT * FROM REMOTEPART.QSYS2.SYSTEM_VALUE_INFO) WITH DATA 
 WITH REPLACE; 

-- Use exception join to reveal any differences 
  SELECT 'REMOTEPART' AS "System Name", A.SYSTEM_VALUE_NAME, 
  A.CURRENT_NUMERIC_VALUE,A.CURRENT_CHARACTER_VALUE FROM QSYS2.SYSTEM_VALUE_INFO A 
 LEFT EXCEPTION JOIN SESSION.Remote_System_Values B 
 ON A.SYSTEM_VALUE_NAME = B.SYSTEM_VALUE_NAME AND 
    A.CURRENT_NUMERIC_VALUE IS NOT DISTINCT FROM B.CURRENT_NUMERIC_VALUE AND 
    A.CURRENT_CHARACTER_VALUE IS NOT DISTINCT FROM B.CURRENT_CHARACTER_VALUE 
 UNION ALL 
  SELECT 'LOCALPART' AS "System Name", B.SYSTEM_VALUE_NAME, 
  B.CURRENT_NUMERIC_VALUE, 
  B.CURRENT_CHARACTER_VALUE FROM QSYS2.SYSTEM_VALUE_INFO A 
 RIGHT EXCEPTION JOIN SESSION.Remote_System_Values B 
 ON A.SYSTEM_VALUE_NAME = B.SYSTEM_VALUE_NAME AND 
    A.CURRENT_NUMERIC_VALUE IS NOT DISTINCT FROM B.CURRENT_NUMERIC_VALUE AND 
    A.CURRENT_CHARACTER_VALUE IS NOT DISTINCT FROM B.CURRENT_CHARACTER_VALUE 
 ORDER BY SYSTEM_VALUE_NAME;


--  category:  IBM i Services
--  description:  Work Management - Workload Group Info
--  minvrm: V7R3M0
--

--
-- Review the configured workload groups
--
select *
  from QSYS2.WORKLOAD_GROUP_INFO;

--
-- Review active jobs, that utilize a workload group
--
select w.*, b.*
  from QSYS2.WORKLOAD_GROUP_INFO w, lateral (
         select a.*
           from table (
               qsys2.active_job_info(DETAILED_INFO => 'ALL')
             ) a
           where WORKLOAD_GROUP = w.workload_group
       ) b;


--  category:  IBM i Services
--  description:  __ Where to find more detail __

--  Documentation can be found here:
--  --------------------------------
--  https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_73/rzajq/rzajqservicessys.htm
-- 
--  Enabling DB2 PTF Group level and enhancement details can be found here:
--  -----------------------------------------------------------------------
--  https://ibm.biz/DB2foriServices
--
;



--  category:  SYSTOOLS
--  description:  Analyze IFS storage consumption

-- first time only
cl: crtlib ifsinfo;

-- On subsequent executions, delete these files before calling RTVDIRINF
drop table IFSINFO.IFSINFO2O;
drop table IFSINFO.IFSINFO2D;

-- indicate the root location for study
cl:RTVDIRINF DIR('/') INFFILEPFX(IFSINFO2) INFLIB(IFSINFO) OMIT('/QSYS.LIB');
stop;


--
-- description: List all objects and directories, in order with their sizes
--
SELECT QEZDIRNAM1 as IFS_DIRECTORY, 
       QEZOBJNAM as IFS_OBJECT_NAME, 
       VARCHAR_FORMAT(QEZDTASIZE, '999G999G999G999G999G999') as IFS_OBJECT_SIZE, 
       QEZOBJTYPE AS IFS_OBJECT_TYPE
FROM IFSINFO.IFSINFO2O O
INNER JOIN 
     IFSINFO.IFSINFO2D D
ON O.QEZDIRIDX = D.QEZDIRIDX
ORDER BY 3 desc;
 
--
-- description: Summarize the size count at the directory levels
--
WITH IFS_SIZE_INFO(IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX, IFS_OBJECT_NAME, IFS_OBJECT_SIZE, IFS_OBJECT_TYPE) AS (
  SELECT QEZDIRNAM1 as IFS_DIRECTORY, D.QEZDIRIDX AS IFS_DIRECTORY_INDEX, 
         QEZPARDIR AS IFS_PARENT_DIRECTORY_INDEX, QEZOBJNAM as IFS_OBJECT_NAME, 
         QEZDTASIZE as IFS_OBJECT_SIZE, QEZOBJTYPE AS IFS_OBJECT_TYPE
  FROM IFSINFO.IFSINFO2O O
    INNER JOIN 
      IFSINFO.IFSINFO2D D
    ON O.QEZDIRIDX = D.QEZDIRIDX
    ORDER BY 1,2,4
)
  SELECT IFS_DIRECTORY,
         VARCHAR_FORMAT(SUM(IFS_OBJECT_SIZE), '999G999G999G999G999G999') as TOTAL_SUBDIR_SIZE
    FROM IFS_SIZE_INFO
    GROUP BY IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX
    ORDER BY TOTAL_SUBDIR_SIZE DESC;

--
-- description: Summarize the size of directories including any subdirectory trees
--
WITH IFS_SIZE_INFO(IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX, IFS_OBJECT_NAME, IFS_OBJECT_SIZE, IFS_OBJECT_TYPE) AS (
  SELECT QEZDIRNAM1 as IFS_DIRECTORY, D.QEZDIRIDX AS IFS_DIRECTORY_INDEX, 
         QEZPARDIR AS IFS_PARENT_DIRECTORY_INDEX, QEZOBJNAM as IFS_OBJECT_NAME, 
         QEZDTASIZE as IFS_OBJECT_SIZE, QEZOBJTYPE AS IFS_OBJECT_TYPE
  FROM IFSINFO.IFSINFO2O O
    INNER JOIN 
      IFSINFO.IFSINFO2D D
    ON O.QEZDIRIDX = D.QEZDIRIDX
    ORDER BY 1,2,4
),   IFS_DIRECTORY_ROLLUP(IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX, TOTAL_SUBDIR_SIZE) AS (
  SELECT IFS_DIRECTORY, 
         CASE WHEN IFS_DIRECTORY_INDEX = 1 THEN 0 ELSE IFS_DIRECTORY_INDEX END AS IFS_DIRECTORY_INDEX, 
         IFS_PARENT_DIRECTORY_INDEX, SUM(IFS_OBJECT_SIZE) AS TOTAL_SUBDIR_SIZE
    FROM IFS_SIZE_INFO
    GROUP BY IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX
    ORDER BY TOTAL_SUBDIR_SIZE DESC
),   IFS_DIRECTORY_RCTE(LEVEL, IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX, TOTAL_SUBDIR_SIZE) AS (
  SELECT 1, IFS_DIRECTORY, IFS_DIRECTORY_INDEX, IFS_PARENT_DIRECTORY_INDEX, TOTAL_SUBDIR_SIZE
    FROM IFS_DIRECTORY_ROLLUP ROOT
    UNION ALL
  SELECT PARENT.LEVEL+1, PARENT.IFS_DIRECTORY, CHILD.IFS_DIRECTORY_INDEX, CHILD.IFS_PARENT_DIRECTORY_INDEX, CHILD.TOTAL_SUBDIR_SIZE
    FROM IFS_DIRECTORY_RCTE PARENT, IFS_DIRECTORY_ROLLUP CHILD
      WHERE PARENT.IFS_DIRECTORY_INDEX = CHILD.IFS_PARENT_DIRECTORY_INDEX
)
select IFS_DIRECTORY, 
       VARCHAR_FORMAT(SUM(TOTAL_SUBDIR_SIZE), '999G999G999G999G999G999') AS TOTAL_SIZE 
 from IFS_DIRECTORY_RCTE
 where IFS_DIRECTORY_INDEX > 1
 GROUP BY IFS_DIRECTORY
 ORDER BY TOTAL_SIZE DESC;
 
 

--
-- description: Summarize the object counts at each directory level
-- 
SELECT QEZDIRNAM1 as IFS_DIRECTORY, 
       COUNT(*)   as IFS_OBJECT_COUNT
FROM IFSINFO.IFSINFO2O O
INNER JOIN 
     IFSINFO.IFSINFO2D D
ON O.QEZDIRIDX = D.QEZDIRIDX
GROUP BY QEZDIRNAM1
ORDER BY 2 desc;


--
--  category:  SYSTOOLS
--  description: Audit Journal Data Mart - Deleted Objects
--  minvrm: v7r4m0
--  

--
-- Create a library for the data mart
--
cl: crtlib aud_dmart;

-- 
-- Set up the data mart for DO audit entries
--
call QSYS2.MANAGE_AUDIT_JOURNAL_DATA_MART(JOURNAL_ENTRY_TYPE => 'DO',
                                          DATA_MART_LIBRARY  => 'AUD_DMART', 
                                          STARTING_TIMESTAMP => '*FIRST', 
                                          DATA_MART_ACTION   => 'CREATE');
stop;

--
-- Confirm that the audit journal data mart has been established
--
select * from 
  qsys2.audit_journal_data_mart_info
    where data_mart_library = 'AUD_DMART';
stop;

--
-- Review the DO detail
--
select * from aud_dmart.aj_do;
stop;

--
-- Review the DO detail
--
select * from aud_dmart.aj_do;
stop;

--
-- Yesterday's DOs for library based objects
--
with DOers (doer) as (
    select
      user_name concat ' deleted ' concat count(*) concat ' objects in ' concat OBJECT_LIBRARY
        concat ' of type ' OBJECT_TYPE
      from aud_dmart.aj_do
      where entry_timestamp > current date - 1 day and
            object_library is not null and
            user_name not like 'Q%'
      group by user_name, OBJECT_LIBRARY, OBJECT_TYPE
      order by user_name, OBJECT_LIBRARY, OBJECT_TYPE)
  select *
    from doers;
stop;    

-- 
-- description: List yesterday's DOs for library based objects
--
with DOers (doer) as (
    select
      rtrim(user_name) concat ' deleted ' concat count(*) concat ' objects in ' concat OBJECT_LIBRARY
        concat ' of type ' concat OBJECT_TYPE
      from aud_dmart.aj_do
      where entry_timestamp > current date - 1 day and
            object_library is not null and
            user_name not like 'Q%'
      group by user_name, OBJECT_LIBRARY, OBJECT_TYPE
      order by user_name, OBJECT_LIBRARY, OBJECT_TYPE)
  select listagg(cast(doer as clob(1m)), ', ')  
    from doers;
stop;

--
-- description: Email yesterday's DOs for library based objects
--
with DOers (doer) as (
       select rtrim(user_name) concat ' deleted ' concat count(*) concat ' objects in ' concat
           OBJECT_LIBRARY concat ' of type ' concat OBJECT_TYPE
         from aud_dmart.aj_do
         where entry_timestamp > current date - 1 day and
               object_library is not null and
               user_name not like 'Q%'
         group by user_name, OBJECT_LIBRARY, OBJECT_TYPE
         order by user_name, OBJECT_LIBRARY, OBJECT_TYPE),
     email_body (body) as (
       select listagg(cast(doer as clob(1m)), ', ')
         from doers
     )
  select SYSTOOLS.SEND_EMAIL(
      TO_EMAIL => 'forstie@us.ibm.com', 
      SUBJECT => 'DOers from ' concat char(current date - 1 day),
      BODY => body)
    from email_body;
stop;


--
--  category:  SYSTOOLS
--  description: Check Software Product Options 
--  minvrm: v7r4m0
--

--
-- SQL alternative to Check Product Option (CHKPRDOPT) CL command
-- Examine those products that fail the check.
--
select *
  from table (
      SYSTOOLS.CHECK_PRODUCT_OPTIONS()
    ) where failure_message_id is not null;




--
--  category:  SYSTOOLS
--  description: Check licences, generate spreadsheets, and send emails
--  minvrm: v7r4m0
--
--  https://www.ibm.com/docs/en/i/7.5?topic=services-send-email-scalar-function
-- 

--
-- Proceduralize the license check, spreadsheet generation, and email
--
create or replace procedure coolstuff.license_check ()
set option commit = *none, usrprf = *user, dynusrprf = *user
begin
  declare expired_license_count integer;
  declare spreadsheet_gen_rv integer;
  declare send_email_rv integer;
  
  call qsys2.qcmdexc('QSYS/CHGJOB CCSID(37)');
  
--
-- How many installed LPPs have an expired license (full deetz)
--
  create or replace table coolstuff.expiredlic as
        (select current date as today, LICENSE_EXPIRATION, PRODUCT_ID, LICENSE_TERM, RELEASE_LEVEL,
                FEATURE_ID, PROCESSOR_GROUP, USAGE_TYPE, LOG_VIOLATION, PRODUCT_TEXT
            from QSYS2.LICENSE_INFO
            where INSTALLED = 'YES' and
                  product_id not like '%WQX' and
                  license_expiration <= current date)
        with data
    on replace delete rows;
  select count(*)
    into expired_license_count
    from coolstuff.expiredlic;
  if (expired_license_count > 0) then
    --
-- Generate the spreadsheet via a Db2 File
--
    values SYSTOOLS.GENERATE_SPREADSHEET(
        PATH_NAME => '/tmp/expired_licenses', LIBRARY_NAME => 'COOLSTUFF',
        FILE_NAME => 'EXPIREDLIC', SPREADSHEET_TYPE => 'xlsx', COLUMN_HEADINGS => 'COLUMN')
      into spreadsheet_gen_rv;
--
-- Send an email with the deetz!
--
    values SYSTOOLS.SEND_EMAIL(
        TO_EMAIL => 'timmr@us.ibm.com', SUBJECT => 'Expired licences on IBM i: ' concat
          (select host_name
              from sysibmadm.env_sys_info), BODY => 'There are ' concat (select count(*)
              from coolstuff.expiredlic) concat ' expired licenses!',
        ATTACHMENT => '/tmp/expired_licenses.xlsx')
              into send_email_rv;
  end if;
end;
stop;


--
-- Automate the report
--
cl: ADDJOBSCDE JOB(LICCHECK) CMD(RUNSQL SQL('call coolstuff.license_check()') COMMIT(*NONE) NAMING(*SQL)) FRQ(*WEEKLY) SCDDATE(*NONE) SCDDAY(*ALL) SCDTIME(235500);
stop;


--
--  category:  SYSTOOLS
--  description:  Data driven emails
--  minvrm: v7r4m0
--
--  https://www.ibm.com/docs/en/i/7.5?topic=services-send-email-scalar-function
-- 
--
-- Now that it's simple to generate spreadsheets and send emails from the IBM i, the request was to 
-- send emails and NOT have the recipient(s) of the email hard-coded.
--
-- One solution is found below. Store the email recipients within a Db2 for i table and 
-- use the LISTAGG built-in function to build the email TO, CC, and BCC lists.
--

--
-- Create an SQL table that contains who should be emailed, by team name
--
create table coolstuff.email 
(team varchar(50), email_address for column emailaddr varchar(100));

--
-- The following table could contain more designations for email delivery.
-- You choose how complex and elaborate the data model becomes.
--
insert into coolstuff.email values('Sec_team', 'forstie@us.ibm.com');
insert into coolstuff.email values('Sec_team', 'timmr@us.ibm.com');
select * from coolstuff.email;
stop;

--
-- Test how LISTAGG can transform multiple column values into a single, comma separated list
--
select
  listagg(
    cast(email_address as clob(1m)), ', ') within group (order by email_address)
    as EMAIL_LIST
  from coolstuff.email
  where team = 'Sec_team';
stop;  

--
-- IBM Security configuration (for purposes of demonstration)
--
select * from qsys2.security_info;
stop;

-- One time setup
-- call qsys2.qcmdexc('QSYS/ADDUSRSMTP  USRPRF(' concat user concat ')');
-- 

--
-- Built a Spreadsheet that resides within Scott's home in the IFS
--
VALUES SYSTOOLS.GENERATE_SPREADSHEET(
  PATH_NAME         => '/home/scottf/sec_info',        
  SPREADSHEET_QUERY => 'select * from qsys2.security_info',    
  SPREADSHEET_TYPE  => 'xlsx',    
  COLUMN_HEADINGS   => 'NONE'   
);
stop;

--
-- Is the spreadsheet created?
--
select PATH_NAME, OBJECT_TYPE, OBJECT_CHANGE_TIMESTAMP
  from table (
      qsys2.ifs_object_statistics('/home/scottf/', SUBTREE_DIRECTORIES => 'YES')
    ) order by object_change_timestamp desc limit 10;
stop;

--
-- What is the name of the current IBM i?
--
select host_name, OS_NAME, OS_VERSION, OS_RELEASE, TOTAL_MEMORY
          from sysibmadm.env_sys_info;
stop;
          
--
-- Send the email, with an attachment, 
-- but use a Db2 file (coolstuff.email) for the email addresses
--
values SYSTOOLS.SEND_EMAIL(
  TO_EMAIL => (select
        listagg(cast(email_address as clob(1m)), ', ') 
        within group (order by email_address)
          as EMAIL_LIST
        from coolstuff.email
        where team = 'Sec_team'), 
  SUBJECT => 'Security config on IBM i: ' concat (select host_name
          from sysibmadm.env_sys_info), 
  BODY => 'Security config captured on ' concat
      current timestamp, 
  ATTACHMENT => '/home/scottf/sec_info.xlsx');
stop;


--
--  category:  SYSTOOLS
--  description:  Generate a spreadsheet, from a Db2 file
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-generate-spreadsheet-scalar-function
--
create table coolstuff.seccfg as
      (select * from qsys2.security_info)
      with data;

VALUES SYSTOOLS.GENERATE_SPREADSHEET(
  PATH_NAME         => '/home/scottf/ss1',
  LIBRARY_NAME      => 'COOLSTUFF', 
  FILE_NAME         => 'SECCFG',     
  SPREADSHEET_TYPE  => 'csv',    
  COLUMN_HEADINGS   => 'NONE'   
);


--
--  category:  SYSTOOLS
--  description:  Generate a spreadsheet, from an SQL query
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-generate-spreadsheet-scalar-function
-- 

VALUES SYSTOOLS.GENERATE_SPREADSHEET(
  PATH_NAME         => '/home/scottf/ss1',        
  SPREADSHEET_QUERY => 'select * from qsys2.security_info',    
  SPREADSHEET_TYPE  => 'csv',    
  COLUMN_HEADINGS   => 'NONE'   
);


--   
--  category:  SYSTOOLS
--  description:  Manage jobs sitting on job queues
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-job-queue-entries-view
--   

--
-- Find jobs on a job queue
--
select *
  from systools.job_queue_entries;


--   
--  category:  SYSTOOLS
--  description:  PING to verify a TCP/IP connection
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-ping-table-function

--   
-- Ping IBM
--  
select *
  from table (
      SYSTOOLS.PING(REMOTE_SYSTEM => 'IBM.COM', /* VARCHAR(255)  Default: *INTNETADR   */
        REMOTE_IP_ADDRESS => NULL,              /* VARCHAR(45) - Default: NULL                      */
        ADDRESS_VERSION_FORMAT => '*CALC',      /* VARCHAR(5)  - *CALC, *IP4, *IP6 - Default: *CALC */
        NUMBER_PACKETS_TO_SEND => 5,            /* INTEGER     - Default: 5                         */
        PACKET_LENGTH_TO_SEND => 256,           /* INTEGER     - Default: 256                       */
        WAIT_TIME => 1,                         /* INTEGER     - Default: 1                         */
        LOCAL_IP_ADDRESS => '*ANY'              /* VARCHAR(45) - *ANY - Default: *ANY               */
      )
    );


--   
--  category:  SYSTOOLS
--  description:  Read PTF cover letters
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-ptf-cover-letter-table-function
--

--
-- Read PTF cover letters for PTFs that are loaded, but not applied
--
with PTFS (PTF_ID) as (
    select PTFID
      from QSYS2.PTF_INFO
      where PTF_COVER_LETTER = 'YES' and
            PTF_LOADED_STATUS = 'LOADED'
  )
  select PTF_ID, C.*
    from PTFS, table (
           SYSTOOLS.PTF_COVER_LETTER(PTF_ID)
         ) C;


--   
--  category:  SYSTOOLS
--  description:  Rename an IFS stream file
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-ifs-rename-scalar-function
--

-- Create an IFS file
call qsys2.ifs_write(
    path_name => '/tmp/library_names',
    line => (select LISTAGG(CAST(objname AS CLOB(1M)), ', ') 
                   WITHIN GROUP(ORDER BY objname) AS LIBRARY_LIST 
               from table(qsys2.object_statistics('QSYS', '*LIB', '*ALLSIMPLE'))),
    overwrite => 'REPLACE'
  );
stop;

-- Read the IFS file
select *
  from table (
      qsys2.ifs_read('/tmp/library_names')
    );
stop;

-- Rename the IFS file
VALUES SYSTOOLS.IFS_RENAME(
                           FROM_OBJECT => '/tmp/library_names', 
                           TO_OBJECT   => '/tmp/library_names' concat 
                                          varchar_format(current date, 'YYMMDD') concat 
                                          '.txt',
                           REPLACE     => 'YES'
                           );    
stop;

-- Read the IFS file
select *
  from table (
      qsys2.ifs_read('/tmp/library_names231111.txt')
    );
stop;


--
--  category:  SYSTOOLS
--  description:  Reply to QSYSOPR inquiry messages 
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-reply-inquiry-messages-scalar-function
-- 
-- Which jobs were the top 5 CPU consumers, by day, over the last week?
--

cl: sndmsg msg('Ipl now?') tousr(*sysopr) msgtype(*inq) rpymsgq(qsysopr);

--
-- Examine all system operator inquiry messages that have no reply
--
with REPLIED_MSGS (KEY) as (
    select a.message_key
      from qsys2.message_queue_info a
           inner join qsys2.message_queue_info b
             on a.message_key = b.associated_message_key
      where A.MESSAGE_QUEUE_NAME = 'QSYSOPR' and
            A.MESSAGE_QUEUE_LIBRARY = 'QSYS' and
            B.MESSAGE_QUEUE_NAME = 'QSYSOPR' and
            B.MESSAGE_QUEUE_LIBRARY = 'QSYS'
      order by b.message_timestamp desc)
  select a.message_text as "INQUIRY", A.*
    from qsys2.message_queue_info a
         left exception join REPLIED_MSGS b
           on a.message_key = b.key
    where MESSAGE_QUEUE_NAME = 'QSYSOPR' and
          MESSAGE_QUEUE_LIBRARY = 'QSYS' and
          message_type = 'INQUIRY'
    order by message_timestamp desc; 
stop;

--
-- Respond...
--
values SYSTOOLS.REPLY_INQUIRY_MESSAGES( 
    MESSAGE_ID          => '*IMMED',
    SEARCH_MESSAGE_TEXT => 'ipl',  
    RESPONSE            => 'Sure',  
    REMOVE_MESSAGE      => 'NO'  
  );


--  category:  SYSTOOLS
--  description:  Return Work Management Class info

call qsys2.override_qaqqini(1, '', '');
call qsys2.override_qaqqini(2,  
                            'SQL_GVAR_BUILD_RULE', 
                            '*EXIST');
--
CREATE OR REPLACE FUNCTION systools.class_info (
         p_library_name VARCHAR(10)
      )
   RETURNS TABLE (
      library VARCHAR(10) CCSID 1208, class VARCHAR(10) CCSID 1208, class_text VARCHAR(
      100) CCSID 1208, last_use TIMESTAMP, use_count INTEGER, run_priority INTEGER,
      timeslice_seconds INTEGER, default_wait_time_seconds INTEGER
   )
   NOT DETERMINISTIC
   EXTERNAL ACTION
   MODIFIES SQL DATA
   NOT FENCED
   SET OPTION COMMIT = *NONE
BEGIN
   DECLARE v_print_line CHAR(133);
   DECLARE local_sqlcode INTEGER;
   DECLARE local_sqlstate CHAR(5);
   DECLARE v_message_text VARCHAR(70);
   DECLARE v_dspcls VARCHAR(300);
   --
   -- DSPCLS detail
   --
   DECLARE v_class CHAR(10);
   DECLARE v_class_library CHAR(10);
   DECLARE v_run_priority INTEGER;
   DECLARE v_timeslice_seconds INTEGER;
   DECLARE v_default_wait_time_seconds INTEGER;
   --
   -- OBJECT_STATISTICS detail
   --
   DECLARE find_classes_query_text VARCHAR(500);
   DECLARE v_class_text CHAR(100);
   DECLARE v_job_name VARCHAR(28);
   DECLARE v_last_use TIMESTAMP;
   DECLARE v_use_count INTEGER;
   DECLARE c_find_classes CURSOR FOR find_classes_query;
   DECLARE c_find_dspcls_output CURSOR FOR SELECT job_name
      FROM qsys2.output_queue_entries_basic
      WHERE user_name = SESSION_USER AND
            spooled_file_name = 'QPDSPCLS' AND
            user_data = 'DSPCLS'
      ORDER BY create_timestamp DESC
      LIMIT 1;
   DECLARE c_dspcls_output CURSOR FOR SELECT c1
      FROM SESSION.splf x
      WHERE RRN(x) > 4
      ORDER BY RRN(x);
   DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
   BEGIN
      GET DIAGNOSTICS CONDITION 1
            local_sqlcode = db2_returned_sqlcode, local_sqlstate = returned_sqlstate;
      SET v_message_text = 'systools.class_info() failed with: ' CONCAT local_sqlcode
               CONCAT '  AND ' CONCAT local_sqlstate;
      SIGNAL SQLSTATE 'QPC01' SET MESSAGE_TEXT = v_message_text;
   END;
   DECLARE GLOBAL TEMPORARY TABLE splf (c1 CHAR(133))
      WITH REPLACE;
   SET find_classes_query_text =
   'select OBJNAME  , rtrim(OBJTEXT)  , LAST_USED_TIMESTAMP  , DAYS_USED_COUNT  FROM TABLE (OBJECT_STATISTICS('''
            CONCAT p_library_name CONCAT ''',''CLS    '')) AS a ';
   PREPARE find_classes_query FROM find_classes_query_text;
   OPEN c_find_classes;
   l1: LOOP
      FETCH FROM c_find_classes INTO v_class, v_class_text, v_last_use, v_use_count;
      GET DIAGNOSTICS CONDITION 1 local_sqlcode = db2_returned_sqlcode,
                  local_sqlstate = returned_sqlstate;
      IF (local_sqlstate = '02000') THEN
         CLOSE c_find_classes;
         RETURN;
      END IF;
      SET v_dspcls = 'DSPCLS CLS(' CONCAT RTRIM(p_library_name) CONCAT '/' CONCAT
               RTRIM(v_class) CONCAT ') OUTPUT(*PRINT)';
      CALL qsys2.qcmdexc(v_dspcls);
      OPEN c_find_dspcls_output;
      FETCH FROM c_find_dspcls_output INTO v_job_name;
      CLOSE c_find_dspcls_output;
      CALL qsys2.qcmdexc('CPYSPLF FILE(QPDSPCLS) TOFILE(QTEMP/SPLF) SPLNBR(*LAST) JOB('
            CONCAT v_job_name CONCAT ') ');
      OPEN c_dspcls_output;
      FETCH FROM c_dspcls_output INTO v_print_line;
      SET v_run_priority = INT(SUBSTR(v_print_line, 56, 10));
      FETCH FROM c_dspcls_output INTO v_print_line;
      SET v_timeslice_seconds = INT(SUBSTR(v_print_line, 56, 10)) / 1000;
      FETCH FROM c_dspcls_output INTO v_print_line; /* skip eligible for purge */
      FETCH FROM c_dspcls_output INTO v_print_line;
      IF SUBSTR(v_print_line, 56, 6) = '*NOMAX' THEN
         SET v_default_wait_time_seconds = NULL;
      ELSE SET v_default_wait_time_seconds = INT(SUBSTR(v_print_line, 56, 10));
      END IF;
      CLOSE c_dspcls_output;
      CALL qsys2.qcmdexc('DLTSPLF FILE(QPDSPCLS)  SPLNBR(*LAST) JOB(' CONCAT v_job_name
            CONCAT ') ');
      PIPE (
         p_library_name,
         v_class, v_class_text, v_last_use, v_use_count, v_run_priority,
         v_timeslice_seconds, v_default_wait_time_seconds);
   END LOOP; /* L1 */
   CLOSE c_find_classes;
END;


create or replace table classtoday.cdetail as (
SELECT *
   FROM TABLE (
         systools.class_info('QSYS')
      )) with data on replace delete rows;
      
select * from classtoday.cdetail;


--
--  category:  SYSTOOLS
--  description:  Send an email
--  minvrm: v7r4m0
--
--  https://www.ibm.com/docs/en/i/7.5?topic=services-send-email-scalar-function
-- 

--
-- One time setup
call qsys2.qcmdexc('QSYS/ADDUSRSMTP  USRPRF(' concat user concat ')');
stop;

VALUES SYSTOOLS.SEND_EMAIL(
  TO_EMAIL   => 'somebody@your.com',    
  SUBJECT    => 'Security config on IBM i: ' concat (select host_name from sysibmadm.env_sys_info),
  BODY       => 'Security config captured on ' concat current timestamp,       
  ATTACHMENT => '/home/scottf/ss1.csv'   
);
stop;


--
--  category:  SYSTOOLS
--  description:  Study job history, CPU top consumers
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-ended-job-info-table-function
--

-- 
-- Which jobs were the top 5 CPU consumers, by day, over the last week?
--
with x as (
    select row_number() over (
             partition by date(message_timestamp)
             order by cpu_time desc nulls last
           ) as r, date(MESSAGE_TIMESTAMP) as job_end_date, CPU_TIME,
           MESSAGE_TIMESTAMP as job_ended, FROM_USER, FROM_JOB, JOB_END_CODE, JOB_END_DETAIL,
           SYNC_AUX_IO_COUNT, JOB_TYPE, PEAK_TEMPORARY_STORAGE
      from table (
          SYSTOOLS.ENDED_JOB_INFO(START_TIME => (CURRENT_DATE - 7 days))
        )
  )
  select *
    from x
    where r <= 5
    order by job_end_date, CPU_TIME desc; 


--
--  category:  SYSTOOLS
--  description:  Study job history, temporary storage
--  minvrm: v7r4m0
--
-- https://www.ibm.com/docs/en/i/7.5?topic=services-ended-job-info-table-function
-- 

--
-- Which job used the most temporary storage? (today or yesterday)
--
select PEAK_TEMPORARY_STORAGE, MESSAGE_TIMESTAMP as job_end_time, FROM_USER, FROM_JOB, FROM_JOB_NAME, FROM_JOB_USER, FROM_JOB_NUMBER,
       JOB_INTERFACE, FROM_PROGRAM, CPU_TIME, NUMBER_OF_STEPS, JOB_END_CODE, JOB_END_DETAIL,
       SECONDARY_ENDING_CODE, SECONDARY_ENDING_CODE_DETAIL, JOB_ENTERED_SYSTEM_TIME,
       JOB_ACTIVE_TIME, TOTAL_RESPONSE_TIME, SUBSYSTEM, INTERACTIVE_TRANSACTIONS, SYNC_AUX_IO_COUNT,
       JOB_TYPE
  from table (
      SYSTOOLS.ENDED_JOB_INFO()
    )
  order by PEAK_TEMPORARY_STORAGE desc;




--  category:  Db2 for i Services
--  description:  Automated index advice processor

-- Purpose: This procedure using the index advice and find those indexes that have 
--          been used by an MTI 500 times, and creates a permanent index.
--          Also, the existing indexes that are at least 7 Days old are examined
--          to determine if any of them should be removed due to lack of sufficient use.

CL: CRTLIB DBESTUDY;

CREATE OR REPLACE PROCEDURE DBESTUDY.WEEKLY_INDEX_MANAGEMENT()
LANGUAGE SQL
BEGIN

CALL SYSTOOLS.ACT_ON_INDEX_ADVICE('TOYSTORE', NULL, NULL, 500, NULL);
CALL SYSTOOLS.REMOVE_INDEXES('TOYSTORE', 500, ' 7 DAYS ');
END;


--
-- Add this call to a scheduled job that runs once per day
--
Call DBESTUDY.WEEKLY_INDEX_MANAGEMENT();


--  category:  Db2 for i Services
--  description:  Collect and study database statistics

CL: CRTLIB dbestudy;
--
-- Capture point-in-time database file detail 
-- for all files in the TOYSTORE library
--
CREATE OR REPLACE TABLE dbestudy.toystore_tables_runtime_details (table_schema,TABLE_NAME,
   table_partition, partition_type, number_deleted_rows, number_rows, data_size, overflow,
   variable_length_size, maintained_temporary_index_size, open_operations, close_operations,
   insert_operations, update_operations, delete_operations, physical_reads, sequential_reads,
   random_reads, keep_in_memory, media_preference, capture_time)
     as (select table_schema, table_name, table_partition, partition_type, number_deleted_rows,
           number_rows, data_size, overflow, variable_length_size,
           maintained_temporary_index_size, open_operations, close_operations, insert_operations,
           update_operations, delete_operations, physical_reads, sequential_reads, random_reads,
           varchar(case keep_in_memory when '1' then 'yes' else 'no' end, default, 37),
           varchar(case media_preference when 255 then 'ssd' else 'any' end, default, 37),
           CURRENT TIMESTAMP
          FROM qsys2.syspartitionstat
          WHERE table_schema = 'TOYSTORE') WITH DATA ON REPLACE DELETE ROWS;
  
--        
-- Identify candidates for physical file reorganization
-- Only examine those files with more than a million rows deleted
--
SELECT TABLE_SCHEMA,
       TABLE_NAME,
       NUMBER_ROWS AS VALID_ROWS,
       NUMBER_DELETED_ROWS AS DELETED_ROWS,
       DATA_SIZE AS DATA_SPACE_SIZE_IN_BYTES,
       DEC(DEC(NUMBER_DELETED_ROWS,19,2) / DEC(NUMBER_ROWS + NUMBER_DELETED_ROWS,19,2) *
          100,19,2) AS DELETED_ROW_PERCENTAGE
   FROM dbestudy.toystore_tables_runtime_details A
   WHERE NUMBER_DELETED_ROWS > 1000000
   ORDER BY DELETED_ROW_PERCENTAGE DESC;


--  category:  Db2 for i Services
--  description:  Compare IFS details across 2 partitions
--                (existence, not contents or attributes)

-- Note: Replace <remote-rdb> with the remote RDB name of the target IBM i

call              qsys2.qcmdexc('crtlib ifsinfo');
call <remote-rdb>.qsys2.qcmdexc('crtlib ifsinfo');

--
-- Generate the IFS object detail
--
call              qsys2.qcmdexc('RTVDIRINF DIR(''/'') INFFILEPFX(IFSINFO2) INFLIB(IFSINFO)');
call <remote-rdb>.qsys2.qcmdexc('RTVDIRINF DIR(''/'') INFFILEPFX(IFSINFO2) INFLIB(IFSINFO)');

stop;

--
-- List all objects and directories
--
SELECT QEZDIRNAM1 as IFS_DIRECTORY, QEZOBJNAM as IFS_OBJECT_NAME, QEZOBJTYPE AS IFS_OBJECT_TYPE
FROM IFSINFO.IFSINFO2O O
     INNER JOIN  IFSINFO.IFSINFO2D D ON O.QEZDIRIDX = D.QEZDIRIDX
ORDER BY 1,3,2 desc;

--
-- Formalize the IFS detail from the local partition
--
CREATE TABLE IFSINFO.local_IFS_objects
   (IFS_DIRECTORY, IFS_OBJECT_NAME, IFS_OBJECT_TYPE)
   AS (SELECT QEZDIRNAM1 as IFS_DIRECTORY, 
              QEZOBJNAM  as IFS_OBJECT_NAME, 
              QEZOBJTYPE AS IFS_OBJECT_TYPE
          FROM IFSINFO.IFSINFO2O O
               INNER JOIN  
               IFSINFO.IFSINFO2D D 
               ON O.QEZDIRIDX = D.QEZDIRIDX)
WITH DATA;


--
-- Bring over the IFS detail from the remote partition
--
CREATE TABLE IFSINFO.remote_IFS_objects
   (IFS_DIRECTORY, IFS_OBJECT_NAME, IFS_OBJECT_TYPE)
   AS (SELECT QEZDIRNAM1 as IFS_DIRECTORY, 
              QEZOBJNAM  as IFS_OBJECT_NAME, 
              QEZOBJTYPE AS IFS_OBJECT_TYPE
          FROM <remote-rdb>.IFSINFO.IFSINFO2O O
               INNER JOIN  
               <remote-rdb>.IFSINFO.IFSINFO2D D 
               ON O.QEZDIRIDX = D.QEZDIRIDX)
WITH DATA;

-- Raw count of objects
select count(*) from IFSINFO.local_IFS_objects;
select count(*) from IFSINFO.remote_IFS_objects;

--
-- Compare and contrast the two partitions. 
-- Any rows returned represent an IFS difference
--
SELECT 'Production' AS "System Name", 
     a.IFS_DIRECTORY, a.IFS_OBJECT_NAME, a.IFS_OBJECT_TYPE
     FROM IFSINFO.local_IFS_objects a LEFT EXCEPTION JOIN 
          IFSINFO.remote_IFS_objects b 
          ON a.IFS_DIRECTORY   IS NOT DISTINCT FROM b.IFS_DIRECTORY   AND
             a.IFS_OBJECT_NAME IS NOT DISTINCT FROM b.IFS_OBJECT_NAME AND
             a.IFS_OBJECT_TYPE IS NOT DISTINCT FROM b.IFS_OBJECT_TYPE  
UNION ALL
SELECT 'Failover' AS "System Name", 
     b.IFS_DIRECTORY, b.IFS_OBJECT_NAME, b.IFS_OBJECT_TYPE
     FROM IFSINFO.local_IFS_objects a RIGHT EXCEPTION JOIN 
          IFSINFO.remote_IFS_objects b 
          ON b.IFS_DIRECTORY   IS NOT DISTINCT FROM a.IFS_DIRECTORY   AND
             b.IFS_OBJECT_NAME IS NOT DISTINCT FROM a.IFS_OBJECT_NAME AND
             b.IFS_OBJECT_TYPE IS NOT DISTINCT FROM a.IFS_OBJECT_TYPE
  ORDER BY IFS_DIRECTORY, IFS_OBJECT_NAME,IFS_OBJECT_TYPE;


--  category:  Db2 for i Services
--  description:  Compare SYSROUTINE across two IBM i partitions

-- Given a remote IBM i partition name and a library name
-- Search for procedure and function differences 
-- Receive a result set with any differences
CALL SYSTOOLS.CHECK_SYSROUTINE('MYREMOTE', 'TOYSTORE', default);

-- Search for procedure and function differences 
-- Query SESSION.SYSRTNDIFF to see the differences
CALL SYSTOOLS.CHECK_SYSROUTINE('MYREMOTE', 'TOYSTORE', 1);
SELECT * FROM SESSION.SYSRTNDIFF;


--  category:  Db2 for i Services
--  description:  Compare database constraints across two IBM i partitions

-- Given a remote IBM i partition name and a library name
-- Search for constraint differences 
-- Receive a result set with any differences
CALL SYSTOOLS.CHECK_SYSCST('MYREMOTE', 'TOYSTORE', default);

-- Search for constraint differences 
-- Query SESSION.SYSCSTDIFF to see the differences
CALL SYSTOOLS.CHECK_SYSCST('MYREMOTE', 'TOYSTORE', 1);
SELECT * FROM SESSION.SYSCSTDIFF;


--  category:  Db2 for i Services
--  description:  Daily SQL Plan Cache management

CL: CRTLIB SNAPSHOTS;
CL: CRTLIB EVENTMONS;
-- Purpose: This procedure captures detail on SQL queries.
--          1) The 100 most expensive SQL queries are captured into a SQL Plan Cache Snapshot named SNAPSHOTS/SNP<julian-date>
--          2) An SQL Plan Cache Event Monitor is started using a name SNAPSHOTS/EVT<julian-date>. The previous event monitor is ended.
--          3) For both 1 & 2, only the 14 most recent days are kept online. 
--          4) For both 1 & 2, the new monitor and snap shot are imported into System i Navigator / ACS SQL Performance Monitor
CREATE OR REPLACE PROCEDURE SNAPSHOTS.DAILY_PC_MANAGEMENT()
LANGUAGE SQL
BEGIN
DECLARE not_found CONDITION FOR '02000';
DECLARE SNAP_NAME CHAR(10);
DECLARE OLDEST_SNAP_NAME CHAR(10);
DECLARE SNAP_COMMENT VARCHAR(100);
DECLARE EVENT_MONITOR_NAME CHAR(10);
DECLARE YESTERDAY_EVENT_MONITOR_NAME CHAR(10);
DECLARE OLDEST_EVENT_MONITOR_NAME CHAR(10);
DECLARE v_not_found BIGINT DEFAULT 0;

-- A Julian date is the integer value representing a number of days
-- from January 1, 4713 B.C. (the start of the Julian calendar) to 
-- the date specified in the argument.
SET SNAP_NAME = 'SNP' CONCAT JULIAN_DAY(current date);
SET OLDEST_SNAP_NAME = 'SNP' CONCAT JULIAN_DAY(current date - 14 days);
SET EVENT_MONITOR_NAME = 'EVT' CONCAT JULIAN_DAY(current date);
SET OLDEST_EVENT_MONITOR_NAME = 'EVT' CONCAT JULIAN_DAY(current date - 14 days);
SET YESTERDAY_EVENT_MONITOR_NAME = 'EVT' CONCAT JULIAN_DAY(current date - 1 day);
---------------------------------------------------------------------------------------------------------
-- Process the Top 100 most expensive queries
---------------------------------------------------------------------------------------------------------
-- Capture the topN queries and import the snapshot
CALL QSYS2.DUMP_PLAN_CACHE_topN('SNAPSHOTS', SNAP_NAME, 100);

-- Remove the oldest TOPN snapshot
BEGIN
  DECLARE CONTINUE HANDLER FOR not_found 
     SET v_not_found = 1; 
  CALL QSYS2.REMOVE_PC_SNAPSHOT('SNAPSHOTS', OLDEST_SNAP_NAME);
END;

---------------------------------------------------------------------------------------------------------
-- Process prune plans using the SQL Plan Cache Event Monitor
---------------------------------------------------------------------------------------------------------
-- If we found yesterdays event monitor, end it 
BEGIN
  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
     SET v_not_found = 1; 
  CALL QSYS2.END_PLAN_CACHE_EVENT_MONITOR(YESTERDAY_EVENT_MONITOR_NAME);
END;

-- Start today's event monitor
CALL QSYS2.START_PLAN_CACHE_EVENT_MONITOR('EVENTMONS', EVENT_MONITOR_NAME);

-- Remove the oldest event monitor
BEGIN
  DECLARE CONTINUE HANDLER FOR not_found 
     SET v_not_found = 1; 
  CALL QSYS2.REMOVE_PC_EVENT_MONITOR('EVENTMONS', OLDEST_EVENT_MONITOR_NAME);
END;
END;


--
-- Add this call to a scheduled job that runs once per day
--
Call SNAPSHOTS.DAILY_PC_MANAGEMENT();


--  category:  Db2 for i Services
--  description:  Enable alerts for files which are growing near the maximum

CL: ALCOBJ OBJ((QSYS2/SYSLIMTBL *FILE *EXCL)) CONFLICT(*RQSRLS) ;
CL: DLCOBJ OBJ((QSYS2/SYSLIMTBL *FILE *EXCL));

CREATE OR REPLACE TRIGGER SCOTTF.SYSTEM_LIMITS_LARGE_FILE
	AFTER INSERT ON QSYS2.SYSLIMTBL 
	REFERENCING NEW AS N FOR EACH ROW MODE DB2ROW 
SET OPTION USRPRF=*OWNER, DYNUSRPRF=*OWNER
BEGIN ATOMIC 
DECLARE V_CMDSTMT VARCHAR(200) ;
DECLARE V_ERROR INTEGER;

DECLARE EXIT HANDLER FOR SQLEXCEPTION 
   SET V_ERROR = 1;

/* ------------------------------------------------------------------ */
/* If a table has exceeded 80% of this limit, alert the operator     */
/* ------------------------------------------------------------------ */
/* 15000 == MAXIMUM NUMBER OF ALL ROWS IN A PARTITION                 */
/*          (max size = 4,294,967,288)                                */
/* ------------------------------------------------------------------ */
IF (N.LIMIT_ID = 15000 AND
    N.CURRENT_VALUE > ((select supported_value from qsys2.sql_sizing where sizing_id = 15000) * 0.8)) THEN 

SET V_CMDSTMT = 'SNDMSG MSG(''Table: ' 
     CONCAT N.SYSTEM_SCHEMA_NAME CONCAT '/' CONCAT N.SYSTEM_OBJECT_NAME
     CONCAT ' (' CONCAT N.SYSTEM_TABLE_MEMBER CONCAT 
     ') IS GETTING VERY LARGE - ROW COUNT =  '
     CONCAT CURRENT_VALUE CONCAT ' '') TOUSR(*SYSOPR) MSGTYPE(*INFO) ';
 CALL QSYS2.QCMDEXC( V_CMDSTMT );
END IF;
END;

commit;

-- Description: Determine if any user triggers have been created over the System Limits table
SELECT * FROM QSYS2.SYSTRIGGERS 
  WHERE EVENT_OBJECT_SCHEMA = 'QSYS2' AND EVENT_OBJECT_TABLE = 'SYSLIMTBL';


--  category:  Db2 for i Services
--  description:  Find and fix SQL DYNUSRPRF setting
--  minvrm: V7R3M0
--
-- Which SQL programs or services have a mismatch between user profile and dynamic user profile (full)
--
select user_profile, dynamic_user_profile, program_schema, program_name, program_type,
       module_name, program_owner, program_creator, creation_timestamp, default_schema,
       "ISOLATION", concurrentaccessresolution, number_statements, program_used_size,
       number_compressions, statement_contention_count, original_source_file,
       original_source_file_ccsid, routine_type, routine_body, function_origin,
       function_type, number_external_routines, extended_indicator, c_nul_required,
       naming, target_release, earliest_possible_release, rdb, consistency_token,
       allow_copy_data, close_sql_cursor, lob_fetch_optimization, decimal_point,
       sql_string_delimiter, date_format, date_separator, time_format, time_separator,
       dynamic_default_schema, current_rules, allow_block, delay_prepare, user_profile,
       dynamic_user_profile, sort_sequence, language_identifier, sort_sequence_schema,
       sort_sequence_name, rdb_connection_method, decresult_maximum_precision,
       decresult_maximum_scale, decresult_minimum_divide_scale, decfloat_rounding_mode,
       decfloat_warning, sqlpath, dbgview, dbgkey, last_used_timestamp, days_used_count,
       last_reset_timestamp, system_program_name, system_program_schema, iasp_number,
       system_time_sensitive
  from qsys2.sysprogramstat
  where system_program_schema = 'SCOTTF'
        and dynamic_user_profile = '*USER' and program_type in ('*PGM', '*SRVPGM')
        and ((user_profile = '*OWNER')
          or (user_profile = '*NAMING'
            and naming = '*SQL'))
  order by program_name;
stop;

--
-- Which SQL programs or services have a mismatch between user profile and dynamic user profile (full)
--
select qsys2.delimit_name(system_program_schema) as lib, 
       qsys2.delimit_name(system_program_name) as pgm, 
       program_type as type
  from qsys2.sysprogramstat
  where system_program_schema = 'SCOTTF'
        and dynamic_user_profile = '*USER' 
        and program_type in ('*PGM', '*SRVPGM')
        and ((user_profile = '*OWNER')
          or (user_profile = '*NAMING'
            and naming = '*SQL'))
  order by program_name;

stop;  

  

--
-- Find misaligned use of SQL's Dynamic User Profile and swap the setting
--
CREATE OR REPLACE PROCEDURE coolstuff.swap_dynusrprf(target_library varchar(10))
   BEGIN
      DECLARE v_eof INTEGER DEFAULT 0;
      DECLARE Prepare_Attributes VARCHAR(100) default ' ';
      declare sql_statement_text clob(10K) ccsid 37;
      declare v_lib varchar(10) ccsid 37;
      declare v_pgm varchar(10) ccsid 37;
      declare v_type varchar(7) ccsid 37;
      DECLARE obj_cursor CURSOR FOR 
select qsys2.delimit_name(system_program_schema) as lib, 
       qsys2.delimit_name(system_program_name) as pgm, 
       program_type as type
  from qsys2.sysprogramstat
  where program_schema = target_library
        and dynamic_user_profile = '*USER'
        and program_type in ('*PGM', '*SRVPGM')
        and ((user_profile = '*OWNER')
          or (user_profile = '*NAMING'
            and naming = '*SQL'))
  order by program_name;
 
      OPEN obj_cursor;
      loop_through_data: BEGIN
                            DECLARE CONTINUE HANDLER FOR SQLSTATE '02000'
                               BEGIN
                               SET v_eof = 1;
                         END;                                                       
       l3 : LOOP
           FETCH obj_cursor INTO v_lib, v_pgm, v_type;
           IF (v_eof = 1)
           THEN
              LEAVE l3;
           END IF;
           
           -- Swap the SQL DYNUSRPRF setting
           CALL QSYS2.SWAP_DYNUSRPRF(v_lib, v_pgm, v_type);
           call systools.lprintf('DYNUSRPRF swapped for: ' concat v_lib concat '/' concat v_pgm concat ' ' concat v_type);

        END LOOP; /* L3 */
      CLOSE obj_cursor;
   END loop_through_data;
END;

stop;

-- Process all the misaligned SQL DynUsrPrf settings for a specific library
call coolstuff.swap_dynusrprf('SCOTTF');

  


--  category:  Db2 for i Services
--  description:  Index Advice - Analyzing advice since last IPL 

-- Examine the condensed index advice where the index advice has occurred since the last IPL
WITH last_ipl(ipl_time)
   AS (SELECT job_entered_system_time
          FROM TABLE(qsys2.job_info(job_status_filter => '*ACTIVE', 
                                    job_user_filter   => 'QSYS')) x
            WHERE job_name = '000000/QSYS/SCPF')
   SELECT
      * from  last_ipl, qsys2.condidxa where last_advised > ipl_time;
      
--
-- Examine the condensed index advice where Maintained Temporary Indexes (MTI)
-- have been used since the last IPL
--      
WITH last_ipl(ipl_time)
   AS (SELECT job_entered_system_time
          FROM TABLE(qsys2.job_info(job_status_filter => '*ACTIVE', 
                                    job_user_filter   => 'QSYS')) x
            WHERE job_name = '000000/QSYS/SCPF')
   SELECT
      * from  last_ipl, qsys2.condidxa 
        where last_mti_used > ipl_time or last_mti_used_for_stats > ipl_time;
      


--  category:  Db2 for i Services
--  description:  Interrogate interactive jobs

WITH INTERACTIVE_JOBS(JOBNAME, STATUS, CPU, IO) AS (
  SELECT job_name, job_status, cpu_time, total_disk_io_count 
    FROM TABLE(qsys2.active_job_info('YES', 'QINTER', '*ALL')) AS a
    WHERE JOB_STATUS IN ('LCKW', 'RUN') 
)
  SELECT JOBNAME, STATUS, CPU, IO, 
         PROGRAM_LIBRARY_NAME,  PROGRAM_NAME,                       
         MODULE_LIBRARY_NAME,   MODULE_NAME,                        
         HEX(BIGINT(STATEMENT_IDENTIFIERS)) AS STMT,
         PROCEDURE_NAME,        ACTIVATION_GROUP_NAME,
         OBJTEXT,               v_client_ip_address
     FROM INTERACTIVE_JOBS I,
     LATERAL  
     (SELECT * FROM TABLE(qsys2.stack_info(JOBNAME)) j
       WHERE program_library_name not like 'Q%'
         order by ordinal_position desc
           LIMIT 1) x,
     LATERAL 
     (SELECT OBJTEXT from table(qsys2.object_statistics(x.PROGRAM_LIBRARY_NAME, 
                                                        '*PGM *SRVPGM',
                                                        x.PROGRAM_NAME)) AS c) AS Y, 
     LATERAL 
     (SELECT v_client_ip_address from table(qsys2.get_job_info(JOBNAME)) AS d) AS z
  ORDER BY CPU DESC;


--  category:  Db2 for i Services
--  description:  Reset indexes statistics while in production

-- This procedure resets QUERY_USE_COUNT and QUERY_STATISTICS_COUNT.
-- The LAST_QUERY_USE, LAST_STATISTICS_USE, LAST_USE_DATE and 
-- NUMBER_DAYS_USED are not affected.
-- 
-- Reset Query statistics over TOYSTORE/EMPLOYEE
--
CALL QSYS2.RESET_TABLE_INDEX_STATISTICS('TOYSTORE', 'EMPLOYEE');

--
-- Reset Query statistics over all tables in the TOYSTORE library
--
CALL QSYS2.RESET_TABLE_INDEX_STATISTICS('TOYSTORE','%');


--  category:  Db2 for i Services
--  description:  Review the distribution of deleted records

SELECT 1000000 - COUNT(*) AS DELETEDCNT
   FROM star100g.item_fact A
   GROUP BY BIGINT(RRN(A) / 1000000)
   ORDER BY BIGINT(RRN(A) / 1000000);
   


--  category:  Db2 for i Services
--  description:  SQE - Query Supervisor - Add a threshold
--  minvrm: V7R3M0
--

--
-- Add a threshold for elapsed time of queries coming in over QZDA jobs
--
CALL QSYS2.ADD_QUERY_THRESHOLD(THRESHOLD_NAME  => 'ZDA QUERY TIME > 30',
                               THRESHOLD_TYPE  => 'ELAPSED TIME',
                               THRESHOLD_VALUE => 30,
                               SUBSYSTEMS      => 'QUSRWRK',
                               JOB_NAMES       =>  'QZDA*', 
                               LONG_COMMENT    => 'ZDA Queries running longer than 30 seconds');

--
-- Review configured Query Supervisor thresholds
--
select *
  from qsys2.query_supervisor;


--  category:  Db2 for i Services
--  description:  SQE - Query Supervisor - Exit programs
--  minvrm: V7R3M0
--

--
-- Review the Query Supervisor exit programs
--  
select *
  from QSYS2.EXIT_PROGRAM_INFO where EXIT_POINT_NAME = 'QIBM_QQQ_QRY_SUPER';


--  category:  Db2 for i Services
--  description:  SQE - Query Supervisor - Remove a threshold
--  minvrm: V7R3M0
--

--
-- Remove a Query Supervisor threshold 
--
CALL QSYS2.REMOVE_QUERY_THRESHOLD(THRESHOLD_NAME  => 'ZDA QUERY TIME > 30');

--
-- Review configured Query Supervisor thresholds
--
select *
  from qsys2.query_supervisor;


--  category:  Db2 for i Services
--  description:  SQE - Query Supervisor - Working example
--  minvrm: V7R3M0
--

--
-- This example shows how to establish a Query Supervisor threshold
-- that is looking at job name of QZDA* and supervising queries that
-- are taking longer than 30 seconds of elapsed time to complete.
-- 
-- When such a query is encountered, the exit program sends an
-- SQL7064 message to QSYSOPR and then directs SQE to 
-- terminate the query.
--
stop;

call qsys2.qcmdexc('CRTSRCPF FILE(QTEMP/ZDA_ELAP1) RCDLEN(140)');
call qsys2.qcmdexc('addpfm file(qtemp/ZDA_ELAP1) mbr(ZDA_ELAP1)');
insert into qtemp.ZDA_ELAP1
  values
 (1, 010101, '#include <stdlib.h>'),
 (2, 010101, '#include <string.h>'),
 (3, 010101, '#include <stddef.h> '),
 (4, 010101, '#include <iconv.h>'),
 (5, 010101, '#include <stdio.h>'),
 (6, 010101, '#include <except.h>'), 
 (7, 010101, '#include <eqqqrysv.h>'),
 (8, 010101, 'static void convertThresholdNameToJobCCSID(const char* input, char* output)'),
 (9, 010101, '{'),
 (10,010101, '  iconv_t converter;'),
 (11,010101, '  char from_code[32], to_code[32];'),
 (12,010101, '  size_t input_bytes, output_bytes;'),
 (13,010101, '  int iconv_rc;'),
 (14,010101, '  memset(from_code, 0, sizeof(from_code));'),
 (15,010101, '  memset(to_code, 0, sizeof(to_code));'),
 (16,010101, '  memcpy(from_code, "IBMCCSID012000000000", 20);'),
 (17,010101, '  memcpy(to_code, "IBMCCSID00000", 13);'),
 (18,010101, '  converter = iconv_open(to_code, from_code);'),
 (19,010101, '  if (converter.return_value == 0) {'),
 (20,010101, '    input_bytes = 60;'),
 (21,010101, '   output_bytes = 30;'),
 (22,010101, '    iconv_rc = iconv(converter,'),
 (23,010101, '                     &input, &input_bytes,'),
 (24,010101, '                     &output, &output_bytes);'),
 (25,010101, '    iconv_close(converter);'),
 (26,010101, '    if (iconv_rc >= 0)'),
 (27,010101, '      return; /* Conversion was successful. */'),
 (28,010101, '  }'),
 (29,010101, '  sprintf(output, "iconv_open() failed with: %d", converter.return_value);'),
 (30,010101, '}'),
 (31,010101, 'int trimmed_length(const char* str, int len)'),
 (32,010101, '{'),
 (33,010101, '  const char* first_blank = memchr(str, '' '', len);'),
 (34,010101, '  if (first_blank)'),
 (35,010101, '    return first_blank - str;'),
 (36,010101, '  return len;'),
 (37,010101, '}'),
 (38,010101, 'int main(int argc, char* argv[])'),
 (39,010101, '{'),
 (40,010101, '  char length_string[10];'),
 (41,010101, '  char cmd[600];'),
 (42,010101, '  char thresholdNameInJobCCSID[31];'),
 (43,010101, '  char msg[512];'),
 (44,010101, '  const QQQ_QRYSV_QRYS0100_t* input = (QQQ_QRYSV_QRYS0100_t*)argv[1];'),
 (45,010101, '  int* rc = (int*)argv[2];'),
 (46,010101, '  memset(thresholdNameInJobCCSID, 0, sizeof(thresholdNameInJobCCSID));'),
 (47,010101, '  convertThresholdNameToJobCCSID(input->Threshold_Name,thresholdNameInJobCCSID);'),
 (48,010101, '  if (memcmp("ZDA QUERY TIME > 30", thresholdNameInJobCCSID, 19) != 0) '),
 (49,010101, '    { return; } '),
 (50,010101, '  *rc = 1; /* terminate the query */'),
 (51,010101, '  memset(msg, 0, sizeof(msg));'),
 (52,010101, '  strcat(msg, "Query Supervisor: ");'),
 (53,010101, '  strcat(msg, thresholdNameInJobCCSID);'),
 (54,010101, '  strcat(msg," REACHED IN JOB ");'),
 (55,010101, '  strncat(msg, input->Job_Number, trimmed_length(input->Job_Number,6));'),
 (56,010101, '  strcat(msg, "/");'),
 (57,010101, '  strncat(msg, input->Job_User, trimmed_length(input->Job_User,10));'),
 (58,010101, '  strcat(msg, "/");'),
 (59,010101, '  strncat(msg, input->Job_Name, trimmed_length(input->Job_Name,10));'),
 (60,010101, '  strcat(msg, " FOR USER: ");'),
 (61,010101, '  strncat(msg, input->User_Name, 10);'),
 (62,010101, '  memset(length_string, 0, sizeof(length_string));'),
 (63,010101, '  sprintf(length_string,"%d",strlen(msg));'),
 (64,010101, '  memset(cmd, 0, sizeof(cmd));'),
 (65,010101, '  strcat(cmd, "SBMJOB CMD(RUNSQL SQL(''call qsys2.send_message(''''SQL7064'''',");'),
 (66,010101, '  strcat(cmd,length_string);'),
 (67,010101, '  strcat(cmd,",''''");'),
 (68,010101, '  strcat(cmd, msg);'),
 (69,010101, '  strcat(cmd, "'''')''))");'),
 (70,010101, '  system(cmd);'),
 (71,010101, '}');
 
cl: crtlib supervisor;

call qsys2.qcmdexc('CRTCMOD MODULE(QTEMP/ZDA_ELAP1) SRCFILE(QTEMP/ZDA_ELAP1)  OUTPUT(*print)  ');
call qsys2.qcmdexc('CRTPGM PGM(SUPERVISOR/ZDA_ELAP1) MODULE(QTEMP/ZDA_ELAP1) ACTGRP(*CALLER) USRPRF(*OWNER) DETAIL(*NONE)');
 
call qsys2.qcmdexc('ADDEXITPGM EXITPNT(QIBM_QQQ_QRY_SUPER) FORMAT(QRYS0100) PGMNBR(*LOW) PGM(SUPERVISOR/ZDA_ELAP1) THDSAFE(*YES) TEXT(''ZDA Elapsed Time > 30 seconds'')') ;


--
-- Review any instances where the Query Supervisor exit program terminated a ZDA query
--
select *
  from table (
      QSYS2.MESSAGE_QUEUE_INFO(MESSAGE_FILTER => 'ALL')
    )
  where message_id = 'SQL7064'
  order by MESSAGE_TIMESTAMP desc; 
  



--  category:  Db2 for i Services
--  description:  Utilities - Compare Database files
--  Note: If no rows are returned, there are no miscompares
--  minvrm: V7R4M0
--

--  For evaluation purposes, create two sample databases
call qsys.create_sql_sample('DOORSTORE1');
call qsys.create_sql_sample('DOORSTORE2');

--
-- Compare will find no differences and return an empty result set
--
select *
  from table (
      qsys2.compare_file(
        library1 => 'DOORSTORE1', 
        file1 => 'SALES', 
        library2 => 'DOORSTORE2',
        file2 => 'SALES', 
        compare_attributes => 'YES', 
        compare_data => 'YES')
    );
stop;  

-- Change one of the files to introduce a difference
update doorstore2.sales set sales = sales + 1 limit 3;

--
-- Compare will find 3 rows differ
--
select *
  from table (
      qsys2.compare_file(
        library1 => 'DOORSTORE1', 
        file1 => 'SALES', 
        library2 => 'DOORSTORE2',
        file2 => 'SALES', 
        compare_attributes => 'YES', 
        compare_data => 'YES')
    );
stop;    


--
-- Compare will return as soon as the first difference is found
--
select *
  from table (
      qsys2.compare_file(
        library1 => 'DOORSTORE1', 
        file1 => 'SALES', 
        library2 => 'DOORSTORE2',
        file2 => 'SALES', 
        compare_attributes => 'QUICK', 
        compare_data => 'QUICK')
    );
stop;  


--  category:  Db2 for i Services
--  description:  Utilities - Database Catalog analyzer
--  minvrm: V7R3M0
--
--  Find all database files in the QGPL library and validate that associated 
--  Database Cross Reference file entries contain the correct and complete detail
--
select *
  from table (
      qsys2.analyze_catalog(option => 'DBXREF', library_name => 'QGPL')
    );
stop;  



--  category:  Db2 for i Services
--  description:  Utilities - Database file data validation
--  Note: If no rows are returned, there are no instances of invalid data
--  minvrm: V7R3M0
--
--
-- Validate all rows within the last member of one file
--
select *
  from table (
      systools.validate_data(
        library_name => 'MARYNA', file_name => 'BADDATA', member_name => '*LAST')
    );
stop;

--
-- Validate all rows within all members of one file
--
select *
  from table (
      systools.validate_data_file(
        library_name => 'MARYNA', file_name => 'BADDATA')
    );
stop;

--
-- Validate all rows within all members of all files within a library
--
select *
  from table (
      systools.validate_data_library(
        library_name => 'MARYNA')
    );
stop;


--  category:  Db2 for i Services
--  description:  __ Where to find more detail __
--
--  Documentation can be found here:
--  --------------------------------
--  https://www.ibm.com/docs/en/i/7.5?topic=optimization-db2-i-services
-- 
--  Enabling Db2 PTF Group level and enhancement details can be found here:
--  -----------------------------------------------------------------------
--  https://ibm.biz/DB2foriServices
--
;



--  category:  Db2 Mirror
--  description:  Db2 Mirror - Install - Review Db2 Mirror product install detail
--  minvrm:  v7r4m0

cl:DSPSFWRSC OUTPUT(*OUTFILE) OUTFILE(QTEMP/SFWRSC); 

--
-- Is the Db2 Mirror LPP installed?
--
WITH db2m (install) AS (
      SELECT COUNT(*)
         FROM qtemp.sfwrsc
         WHERE lcprdi = '5770SS1' AND
               lcsfgi = '0048'
   )
   SELECT
      CASE
         WHEN install > 0 THEN
            'Db2 Mirror Product (5770SS1 Option 48) is installed'
         ELSE 
            'Db2 Mirror Product (5770SS1 Option 48) is not installed'
      END
      FROM db2m;


--
-- Is the Db2 Mirror GUI installed?
--
WITH db2m (install) AS (
      SELECT COUNT(*)
         FROM qtemp.sfwrsc
         WHERE lcprdi = '5770DBM' AND 
               lcsfgi = '0000'
   )
   SELECT
      CASE
         WHEN install > 0 THEN
            'Db2 Mirror GUI (5770DBM Option 0) is installed'
         ELSE 
            'Db2 Mirror GUI (5770DBM Option 0) is not installed'
      END
      FROM db2m;
      
--
-- Is the Db2 Mirror Clone support installed?
--
WITH db2m (install) AS (
      SELECT COUNT(*)
         FROM qtemp.sfwrsc
         WHERE lcprdi = '5770DBM' AND               
               lcsfgi = '0001'
   )
   SELECT
      CASE
         WHEN install > 0 THEN
            'Db2 Mirror Clone Support (5770DBM Option 1) is installed'
         ELSE 
            'Db2 Mirror Clone Support (5770DBM Option 1) is not installed'
      END
      FROM db2m;


--  category:  Db2 Mirror
--  description:  Db2 Mirror - License - Review Db2 Mirror licenses
--  minvrm:  v7r4m0

select * from qsys2.license_info
  where product_id = '5770DBM';


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Manage - Review important Db2 Mirror messages
--  minvrm:  v7r4m0

-- Which Db2 Mirror messages have been sent to QSYSOPR?
--
-- CPDC905 - Db2 Mirror Network Redundancy Group (NRG) link 11.22.3.4 is active.
-- CPDC906 - Network Redundancy Group (NRG) link 11.22.3.4 is inactive.
-- CPD3E43 - DRDA/DDM Db2 Mirror server error occurred with reason code 77.
-- CPF32CD - Db2 Mirror resynchronization failed for job *ALL.
-- CPIC901 - Db2 Mirror replication is suspended for ASP group IASP33P.  Reason code 280.
-- CPIC902 - Db2 Mirror replication is suspended for ASP group IASP33P due to an error.  Reason code 282.   
-- CPIC903 - Db2 Mirror replication is suspended for maintenance operations.
-- CPIC904 - Db2 Mirror replication is active for ASP group IASP33P.   
--   
SELECT *
   FROM TABLE (
         qsys2.message_queue_info('QSYS', 'QSYSOPR')
      )
   WHERE message_id IN (
         'CPDC905',
         'CPDC906',
         'CPD3E43',
         'CPF32CD',
         'CPIC901',
         'CPIC902',
         'CPIC903',
         'CPIC904'
      )
   ORDER BY message_timestamp DESC;

stop;

--
-- Have we encountered any Db2 Mirror failures?
--
with resync_failures(jn, msg, msgtime) as (
  SELECT from_job, message_id, message_timestamp
   FROM qsys2.message_queue_info a 
   WHERE message_queue_name = 'QSYSOPR' AND
         message_queue_library = 'QSYS' AND
         message_id in 
         ('CPD3E43', 'CPF32CD')
   order by message_timestamp desc
)
select jn, msg, msgtime from resync_failures;


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Manage - Suspend or Resume replication of SYSBAS
--  minvrm:  v7r4m0

stop;
-- Suspend replication for SYSBAS and any active IASPs
CALL QSYS2.CHANGE_MIRROR
     (IASP_NAME => '*SYSBAS', 
      REPLICATION_STATE => 'SUSPEND') ;
 
stop;
-- Resume replication and resynchronize any tracked changes
CALL QSYS2.CHANGE_MIRROR
     (IASP_NAME => '*SYSBAS', 
      REPLICATION_STATE => 'RESUME') ;
            
SELECT *
   FROM qsys2.mirror_info;            


--  category:  Db2 Mirror
--  description:  Db2 Mirror - NRG - Review and configure link priorities
--  minvrm:  v7r4m0

-- Review the current NRG Link detail
SELECT
  NRG_NAME,            -- NRG_NAME   VARCHAR(15)   
  ADDRESS_SPACE_TYPE,  -- ADDR_TYPE  CHARACTER(4)  
  SOURCE_ADDRESS,      -- SRC_ADDR   VARCHAR(45)   
  TARGET_ADDRESS,      -- TGT_ADDR   VARCHAR(45)   
  LINK_STATE,          -- STATE      VARCHAR(4)    
  LINK_PRIORITY,       -- PRIORITY   INTEGER       
  LINK_IN_USE,         -- IN_USE     VARCHAR(3)    
  LINE_DESCRIPTION,    -- LINE_DES   VARCHAR(10)   
  VIRTUAL_LAN_ID       -- LAN_ID     INTEGER       
FROM QSYS2.NRG_LINK_INFO;


-- Lower the IFS link priority
call qsys2.change_nrg_link(
   nrg_name       => 'MIRROR_IFS',
   SOURCE_ADDRESS => '10.61.1.11',
   link_priority  => 5
   );
   


--  category:  Db2 Mirror
--  description:  Db2 Mirror - NRG - Show all the network redundancy groups that have active links
--  minvrm:  v7r4m0

SELECT * FROM QSYS2.NRG_INFO
  WHERE ACTIVE_LINK_COUNT > 0;



--  category:  Db2 Mirror
--  description:  Db2 Mirror - OTL - Show all the tracked entries that have not yet been processed.
--  minvrm:  v7r4m0

SELECT * FROM QSYS2.RESYNC_STATUS
WHERE RESYNC_TYPE IS NOT NULL AND RESYNC_ENDTIME IS NULL
      AND RESYNC_DEFERRED = 'NOT DEFERRED'
ORDER BY TRACKING_TIME;
   


--  category:  Db2 Mirror
--  description:  Db2 Mirror - OTL - What's in the process of being resynchronized?
--  minvrm:  v7r4m0

WITH x AS
      (
      SELECT
             CASE
                WHEN resync_deferred IS NULL THEN 'PRIORITY ENTRY'
                WHEN failure_message IS NOT NULL AND
                   resync_endtime IS NOT NULL THEN 'ERROR RECOVERED'
                WHEN failure_message IS NOT NULL AND
                   resync_deferred = 'RESYNC DEFERRED' THEN 'ERROR DEFERRED'
                WHEN failure_message IS NOT NULL AND
                   resync_endtime IS NULL THEN 'ERROR UNRECOVERED'
                WHEN resync_deferred = 'RESYNC DEFERRED' THEN 'RESYNC DEFERRED'
                WHEN resync_deferred = 'USER DEFERRED' THEN 'USER DEFERRED'
                WHEN resync_endtime IS NOT NULL THEN 'HISTORICAL ENTRY'
                WHEN resync_starttime IS NOT NULL THEN 'ACTIVE RESYNC'
                ELSE 'WAITING RESYNC'
             END AS status,
             system_object_schema,
             system_object_name,
             system_object_type,
             member_name,
             suggested_priority,
             resync_type,
             resync_type_description,
             tracking_time,
             resync_starttime,
             resync_endtime,
             tracking_reason,
             job_name,
             failure_message,
             resync_group,
             resync_deferred,
             resync_cl_command,
             program_library,
             program_name,
             resync_number,
             resync_deferred_group,
             changed_row_estimate,
             CASE
                WHEN
                   resync_endtime IS NOT NULL
                   THEN (TIMESTAMP(resync_endtime) - TIMESTAMP(resync_starttime))
                ELSE NULL
             END AS resync_duration
         FROM qsys2.resync_status
   )
   SELECT status,
          system_object_schema,
          system_object_name,
          system_object_type,
          member_name,
          suggested_priority,
          resync_type,
          resync_type_description,
          tracking_time,
          resync_starttime,
          resync_endtime,
          tracking_reason,
          job_name,
          failure_message,
          resync_group,
          resync_deferred,
          resync_cl_command,
          program_library,
          program_name,
          resync_number,
          resync_deferred_group,
          changed_row_estimate,
          resync_duration
      FROM x
      WHERE status IN (
            'ACTIVE RESYNC',
            'WAITING RESYNC'
         )
      ORDER BY tracking_time DESC;


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Product - Determine if the current partition is the primary node
--  minvrm:  v7r4m0

SELECT
       CASE
          WHEN e.host_name = M.primary_node THEN
             e.host_name CONCAT ' is the Primary node'
          WHEN e.host_name = M.secondary_node THEN
             e.host_name CONCAT ' is the Secondary node'
          ELSE e.host_name CONCAT ' does not match the Primary or Secondary node'
       END AS IDENTITY, M.*
   FROM qsys2.system_status_info e, qsys2.mirror_info M
   WHERE M.iasp_usage IS NULL;
   
   
   


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Product - Review Db2 Mirror environment
--  minvrm:  v7r4m0

SELECT
  IASP_NAME,                     -- IASP_NAME   VARCHAR(10)    
  ASP_STATE,                     -- ASP_STATE   VARCHAR(13)    
  IASP_USAGE,                    -- USAGE       VARCHAR(8)     
  PRIMARY_NODE,                  -- PRIMARY     VARCHAR(8)     
  SECONDARY_NODE,                -- SECONDARY   VARCHAR(8)     
  REPLICATION_STATE,             -- STATE       VARCHAR(12)    
  REPLICATION_DETAIL,            -- REP_DETAIL  VARCHAR(13)    
  REPLICATION_DETAIL_INFO,       -- REP_INFO    INTEGER        
  REPLICATION_DETAIL_INFO_TEXT,  -- REP_INFO_T  VARCHAR(1024)  
  NRG_STATE,                     -- NRG_STATE   VARCHAR(8)     
  DEFAULT_INCLUSION_STATE,       -- INCLUSION   VARCHAR(7)     
  AUTO_RESUME,                   -- AUTORESUME  VARCHAR(3)     
  PARALLEL_DEGREE,               -- PARALLEL    VARCHAR(4)     
  SPLF_RESYNC_INTERVAL,          -- SPLFRESYNC  INTEGER        
  PRIMARY_HOSTNAME,              -- PRI_HOST    VARCHAR(256)   
  SECONDARY_HOSTNAME,            -- SEC_HOST    VARCHAR(256)   
  CLUSTER_RESOURCE_GROUP,        -- CRG         VARCHAR(10)    
  ASP_NUMBER,                    -- ASPNUM      INTEGER        
  RELATIONAL_DATABASE_NAME       -- RDB_NAME    VARCHAR(18)    
FROM QSYS2.MIRROR_INFO;


--  category:  Db2 Mirror
--  description:  Db2 Mirror - RCL - Add multiple rules at the same time
--  minvrm:  v7r4m0

-- At this point, the TOYSTORE library and its contents only exist on the primary
-- The Default Inclusion State being used is EXCLUDE
-- Next, we want to INCLUDE this library, but not all of the objects within
-- We'll use the pending apply rules support to make multiple changes to the RCL, in a coordinated rule change

-- By default, all current and future replication eligible objects in TOYSTORE 
-- will be included for replication
CALL QSYS2.ADD_REPLICATION_CRITERIA(INCLUSION_STATE => 'INCLUDE',
                                    IASP_NAME       => '*SYSBAS',
                                    LIBRARY_NAME    => 'TOYSTORE',
                                    APPLY           => 'PENDING',
                                    APPLY_LABEL     => 'ADD_TOYSTORE_RULES');

-- Exclude the TOYSTORE/IN_TRAY *FILE from replication
-- Activate the pending apply rules for the ADD_TOYSTORE_RULES apply label
CALL QSYS2.ADD_REPLICATION_CRITERIA(INCLUSION_STATE => 'EXCLUDE',
                                    IASP_NAME       => '*SYSBAS',
                                    LIBRARY_NAME    => 'TOYSTORE',
                                    object_name     => 'IN_TRAY',
                                    object_type     => '*FILE',
                                    APPLY           => 'ACTIVE',
                                    APPLY_LABEL     => 'ADD_TOYSTORE_RULES');

-- Exists on the primary
Select * from table(qsys2.object_statistics('TOYSTORE', 'FILE', 'IN_TRAY'));

-- Not replicated to the secondary
Select * from table(qsys2.object_statistics('TOYSTORE', 'FILE', 'IN_TRAY'))
  where exists (select 1 from qibm_db2m_00000.sysibm.sysdummy1);


--  category:  Db2 Mirror
--  description:  Db2 Mirror - RCL - Review user created rules
--  minvrm:  v7r4m0

-- Show all active user rules
SELECT * FROM QSYS2.REPLICATION_CRITERIA_INFO
  WHERE APPLY_STATE = 'ACTIVE' AND RULE_SOURCE = 'USER' 
  ORDER BY IASP_NAME, LIBRARY_NAME, OBJECT_TYPE, OBJECT_NAME;

-- Show all pending rule changes
SELECT APPLY_LABEL, P.*
  FROM QSYS2.REPLICATION_CRITERIA_INFO P
  WHERE APPLY_STATE IN ('PENDING ADD', 'PENDING REMOVE')
  ORDER BY APPLY_LABEL;



--  category:  Db2 Mirror
--  description:  Db2 Mirror - Security - Authorization to use SQL Services
--  minvrm:  v7r4m0

--
-- Who is authorized to use Db2 Mirror - SQL Services?
--
with Db2Mirror_SQL (libname, srvpgmname, purpose) as (

  values ('QSYS', 'QMRDBSSDBA', 'Configure Db2 Mirror Replication'),
         ('QSYS', 'QMRDBSSPRD', 'Configure Db2 Mirror Product'),
         ('QSYS', 'QMRDBSSOBJ', 'Work with Db2 Mirror Object details'),
         ('QSYS', 'QMRDBSSRTV', 'Review    Db2 Mirror details'),
         ('QSYS', 'QDBSRVIO1' , 'Configure Db2 Mirror Resynchronization'),
         ('QSYS2','CMPRSENT'  , 'Compare   Db2 Mirror Resynchronization'),
         ('QSYS', 'QMRDBSSNRG', 'Configure Db2 Mirror Communication'),
         ('QSYS', 'QTOCNRGRP' , 'Configure Db2 Mirror Communication')
) 

SELECT libname, srvpgmname, authorization_name, object_authority, purpose
   FROM Db2Mirror_SQL f,
        LATERAL (
           SELECT o.*
              FROM qsys2.object_privileges o
              WHERE system_object_name   = f.srvpgmname AND
                    system_object_schema = f.libname    AND 
                    object_type          = '*SRVPGM'    AND
                    DATA_EXECUTE         = 'YES'        AND
                    authorization_name  <> 'QSYS'
        ) p
  order by 1,2,3;


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Security - Review Db2 Mirror Audit Journal records
--  minvrm:  v7r4m0

--
-- See all M0, M6, M7, M8 and M9 audit journal records generated for all users
-- today and yesterday
--
-- M0 (Db2 Mirror Setup Tools)
-- M6 (Db2 Mirror Communication Services) 
-- M7 (Db2 Mirror Replication Services)  
-- M8 (Db2 Mirror Product Services)
-- M9 (Db2 Mirror Replication State) 
--
select * from table(QSYS2.MIRROR_DISPLAY_JOURNAL());

--
-- Retrieve the M7 and M9 audit journal records generated for all users two days ago 
--
select * from table(QSYS2.MIRROR_DISPLAY_JOURNAL(
   STARTING_DATE       => current date - 2 days,
   ENDING_DATE         => current date - 2 days,
   JOURNAL_ENTRY_TYPES => 'M7,M9' ));

--
-- Retrieve the M8 records for user profile SCOTTF from today, yesterday and the day prior
--
select * from table(QSYS2.MIRROR_DISPLAY_JOURNAL(
   STARTING_DATE       => current date - 2 day,
   ENDING_DATE         => current date,
   USER_PROFILE              => 'SCOTTF',
   JOURNAL_ENTRY_TYPES => 'M8' ));

--
-- Retrieve the M6 records for ALL users from today and yesterday
-- 
select * from table(QSYS2.MIRROR_DISPLAY_JOURNAL(
   USER_PROFILE        => '*ALL',
   JOURNAL_ENTRY_TYPES => 'M6' ));


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Serviceability - Compare a single table 
--  minvrm:  v7r4m0

cl: SBMJOB CMD(RUNSQL SQL('create or replace table DB2M_COMP.TOYSTORE_EMPLOYEE_COMPARE as (
SELECT * FROM TABLE(qsys2.mirror_compare_object(
                 library_name => ''TOYSTORE'', 
                 object_name  => ''EMPLOYEE'', 
                 object_type => ''*FILE''))
) with data on replace delete rows') commit(*NONE))  JOB(DB2MCOMP) INLASPGRP(*CURRENT) JOBMSGQFL(*PRTWRAP) LOG(4 00 *SECLVL);

--
-- Watch compare progress / activity
--
SELECT *
   FROM TABLE (
         active_job_info(
            job_name_filter => 'DB2MCOMP', subsystem_list_filter => 'QBATCH')
      );
      
--
-- Note: An Empty table indicates there were zero miscompares
--
select * from DB2M_COMP.TOYSTORE_EMPLOYEE_COMPARE;            



--  category:  Db2 Mirror
--  description:  Db2 Mirror - Serviceability - Compare all replicated objects within a library
--  minvrm:  v7r4m0

cl:SBMJOB CMD(runsql sql('CALL QSYS2.MIRROR_COMPARE_LIBRARY(         
                          LIBRARY_NAME        => ''TOYSTORE'',  
                          COMPARE_DATA        => ''YES'', 
                          COMPARE_ATTRIBUTES  => ''YES'', 
                          RESULT_LIBRARY      => ''DB2M_COMP'',
                          RESULT_FILE         => ''TOYSTORE'') ') 
                          commit(*NONE)) JOB(DB2MCOMP) 
                          INLASPGRP(*CURRENT) CCSID(37) JOBMSGQFL(*PRTWRAP) LOG(4 00 *SECLVL); 
--
-- Watch compare progress / activity
--
SELECT *
   FROM TABLE (
         active_job_info(
            job_name_filter => 'DB2MCOMP', subsystem_list_filter => 'QBATCH')
      );
      
--
-- Note: An Empty table indicates there were zero miscompares
--
select * from DB2M_COMP.TOYSTORE;    


--  category:  Db2 Mirror
--  description:  Db2 Mirror - Serviceability - Compare the following replicated object types: *AUTL, *USRPRF, *SYSVAL, *ENVVAR, *FCNUSG, and *SECATR
--  minvrm:  v7r4m0

-- Create a library which will contain the results of Db2 Mirror Compare services
cl: crtlib db2m_comp;

-- Construct helper functions to create a unique file name for today's compare QSYSddmmyy
begin
execute immediate 'create or replace variable db2m_comp.today varchar(10) default (values 'QSYS' concat varchar_format(current date, 'MMDDYY'))';
execute immediate 'create or replace alias    db2m_comp.QSYS_COMPARED_TODAY for db2m_comp.' concat db2m_comp.today;
end;

-- Compare all replication eligible objects in QSYS
-- Use the verbose option to review everything that was compared
CALL QSYS2.MIRROR_COMPARE_LIBRARY(LIBRARY_NAME => 'QSYS',
   RESULT_SET     => 'YES',
   RESULT_LIBRARY => 'DB2M_COMP',
   RESULT_FILE    => db2m_comp.today,
   VERBOSE_LOG    => 'YES');

-- Examine only instances of any miscompare
select * from db2m_comp.QSYS_COMPARED_TODAY
  where compare_result <> 'COMPARED';




--  category:  SQL Built-in Functions
--  description:  INTERPRET - Blob containing character data
--  minvrm:  v7r3m0

-- Interpret binary large object (BLOB) as character
create table qtemp.tempblob ( jblob blob(100) );
insert into qtemp.tempblob (jblob) values(BX'F1F2F3F4');
select * from qtemp.tempblob;
select interpret(substr(jblob,1,4) as char(4)) from qtemp.tempblob; 


--  category:  SQL Built-in Functions
--  description:  INTERPRET - Data Journal ESD
--  minvrm:  v7r3m0

-- Interpret journal entry specific data (ESD)
create schema demo;
set schema demo;
create table interpret1 (ddate date, ttime time, sint smallint, iint integer, bint bigint);
insert into interpret1
  values (current date, current time, 1, 2, 3);

select date(interpret(substr(entry_data, 1, 10) as char(10))) as ddate,
       time(interpret(substr(entry_data, 11, 8) as char(8))) as ttime,
       interpret(substr(entry_data, 19, 2) as smallint) as sint,
       interpret(substr(entry_data, 21, 4) as int) as iint,
       interpret(substr(entry_data, 25, 8) as bigint) as bint
  from table (
      qsys2.display_journal('DEMO', 'QSQJRN', journal_entry_types => 'PT')
    );
    


--  category:  SQL Built-in Functions
--  description:  INTERPRET - Simple examples
--  minvrm:  v7r3m0

-- Interpret binary as varying character
values interpret(bx'0003C1C2C3' as varchar(3)); 
-- returns ABC

-- Interpret binary as integer
VALUES INTERPRET(bX'00000011' AS integer);
-- 17

-- Interpret binary as smallint
VALUES INTERPRET(BX'000A' as SMALLINT);


--  category:  SQL Built-in Functions
--  description:  JSON_ARRAYAGG  - generate a JSON array
--  minvrm:  v7r3m0

call qsys.create_sql_sample('SHOESTORE');
--
-- Publish the data within a table using SQL
-- One JSON document for ALL rows, within a JSON Array
--
with json_rows (j) as (
    select json_object(
        key 'EMPNO' value empno, key 'FIRSTNME' value firstnme,
        key 'MIDINIT' value midinit, key 'LASTNAME' value lastname,
        key 'WORKDEPT' value workdept, key 'PHONENO' value phoneno,
        key 'HIREDATE' value hiredate, key 'JOB' value job,
        key 'EDLEVEL' value edlevel, key 'SEX' value sex,
        key 'BIRTHDATE' value birthdate, key 'SALARY' value salary,
        key 'BONUS' value bonus, key 'COMM' value comm
        absent on null returning clob(2g) ccsid 1208 format json
      )
      from shoestore.employee
      order by lastname)
  select json_object(
      key 'SHOESTORE.EMPLOYEE' value json_arrayagg(
        j format json
      ) absent on null returning clob(2g) ccsid 1208 format json
    )
    from json_rows;


--  category:  SQL Built-in Functions
--  description:  JSON_OBJECT  - generate a JSON object using the specified key:value pairs
--  minvrm:  v7r3m0

call qsys.create_sql_sample('SHOESTORE');

--
-- Publish the data within a table using SQL
-- One JSON document, per row
--
select json_object(
        key 'EMPNO' value empno, key 'FIRSTNME' value firstnme,
        key 'MIDINIT' value midinit, key 'LASTNAME' value lastname,
        key 'WORKDEPT' value workdept, key 'PHONENO' value phoneno,
        key 'HIREDATE' value hiredate, key 'JOB' value job,
        key 'EDLEVEL' value edlevel, key 'SEX' value sex,
        key 'BIRTHDATE' value birthdate, key 'SALARY' value salary,
        key 'BONUS' value bonus, key 'COMM' value comm
        absent on null returning clob(2g) ccsid 1208 format json
      )
from shoestore.employee
order by lastname;


--  category:  SQL Built-in Functions
--  description:  JSON_OBJECTAGG  - generate an aggregated JSON object
--  minvrm:  v7r3m0

call qsys.create_sql_sample('SHOESTORE');

--
-- Publish JSON objects where each department is the key
-- and the value is an array of department member surnames
-- in ascending alphabetical order
--
select json_object(key deptno value (json_array((select LASTNAME
      from shoestore.employee e
      where e.workdept = x.deptno
      order by LASTNAME))))
  from shoestore.dept x;
  
--
-- Publish a single JSON object where each department is the key
-- and the value is an array of department member surnames
-- in ascending alphabetical order
--
select json_objectagg(key deptno value (json_array((select LASTNAME
      from shoestore.employee e
      where e.workdept = x.deptno
      order by LASTNAME))))
  from shoestore.dept x;


--  category:  SQL Built-in Functions
--  description:  LOCATE_IN_STRING - Auditing objects created in the Ifs root
--  minvrm:  v7r3m0

--
--  description: Who is creating objects in the IFS root?
-- 
select user_name, count(*) as ifs_object_count
  from table (
      systools.audit_journal_co(STARTING_TIMESTAMP => current timestamp - 1 month)
    )
  where object_type <> '*DIR' and 
        locate_in_string(path_name, '/', 1, 2) = 0 
  group by user_name
  order by 2 desc;


--  category:  SQL Built-in Functions
--  description:  TIMESTAMP_FORMAT - Convert from DECIMAL --> DATE
--  minvrm:  v7r3m0

create or replace variable coolstuff.decimal_date decimal(8,0);
create or replace variable coolstuff.the_date date;

set coolstuff.the_date = '12/01/2022';

--
-- Turn the date into this format: YYYYMMDD
--
set coolstuff.decimal_date = year(coolstuff.the_date) concat lpad(month(coolstuff.the_date), 2, 0) concat lpad(day(coolstuff.the_date), 2, 0);

--
-- Turn YYYYMMDD into a DATE format
--
set coolstuff.the_date =  date(timestamp_format(char(coolstuff.decimal_date), 'YYYYMMDD'));


select coolstuff.decimal_date as dec_date, coolstuff.the_date as real_date from sysibm.sysdummy1;


--  category:  SQL Built-in Functions
--  description:  VARCHAR_FORMAT - Formatting big numbers
--  minvrm:  v7r3m0

--
--  Format output and break down by iASP
--
SELECT USER_NAME, 
       VARCHAR_FORMAT(sum(STGUSED),'999G999G999G999G999G999G999G999') AS STORAGE_KB 
  FROM QSYS2.USER_STORAGE 
  where user_name not in ('QSYS', 'QDFTOWN')
  group by USER_NAME 
  ORDER BY sum(STGUSED) DESC
  limit 10;




-- category: Geospatial Analytics
-- description: ST_Area
-- minvrm:  v7r4m0

-- Create a table with a polygon column and insert several polygons that represent different New York City Parks
CREATE TABLE sample_parks (park_name VARCHAR(50), geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Find the area of each New York City Park in square meters
SELECT park_name, 
       QSYS2.ST_AREA(geometry) as area_square_meters, 
       QSYS2.ST_AREA(geometry) * 0.000247 as area_acres
 FROM sample_parks;


-- category: Geospatial Analytics
-- description: ST_AsBinary
-- minvrm:  v7r4m0

-- Create a table with a polygon column and insert several polygons that represent different New York City Parks
CREATE TABLE sample_parks (park_name VARCHAR(50), geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Find the area of each New York City Park in square meters
SELECT park_name, 
       QSYS2.ST_AREA(geometry) as area_square_meters, 
       QSYS2.ST_AREA(geometry) * 0.000247 as area_acres
 FROM sample_parks;


-- category: Geospatial Analytics
-- description: ST_AsText
-- minvrm:  v7r4m0

-- Create a table with a geometry column and insert the geometries of various New York City landmarks
CREATE TABLE sample_geometries(location_name VARCHAR(50), geo QSYS2.ST_GEOMETRY);
INSERT INTO sample_geometries VALUES
 ('Empire State Building', QSYS2.ST_POINT('point(-73.9854 40.7488)')),
 ('Brooklyn Bridge', QSYS2.ST_LINESTRING('linestring (-73.9993 40.7081,-73.9937 40.7035)')),
 ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))'));

-- Convert the geometry back into readable text
SELECT location_name, QSYS2.ST_ASTEXT(geo) AS geometry
  FROM sample_geometries;


-- category: Geospatial Analytics
-- description: ST_Buffer
-- minvrm:  v7r4m0


-- Create a new geometry that is a 1 kilometer buffer around a polygon
VALUES QSYS2.ST_ASTEXT(QSYS2.ST_BUFFER(QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'), 1000));


-- category: Geospatial Analytics
-- description: ST_Contains
-- minvrm:  v7r4m0

-- Create a table with a point column and insert various New York City landmarks
CREATE TABLE sample_points(location_name VARCHAR(50), point QSYS2.ST_POINT);
INSERT INTO sample_points VALUES
 ('Empire State Building', QSYS2.ST_POINT(-73.9854, 40.7488)),
 ('Central Park Castle', QSYS2.ST_POINT(-73.9753, 40.7703)),
 ('Chrysler Building', QSYS2.ST_POINT(-73.9755, 40.7516)),
 ('Belvidere Castle', QSYS2.ST_POINT(-73.9690, 40.7797));

-- Create a polygon variable 
-- Set the variables default value to the polygon the defines the boundary for New York City's Central Park
CREATE VARIABLE central_park_geometry QSYS2.ST_POLYGON DEFAULT(QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))'));

-- Query to find out if Central Park contains any New York City landmarks in the table 
SELECT location_name, QSYS2.ST_CONTAINS(central_park_geometry, point) AS central_park_contains
  FROM sample_points;
  



-- category: Geospatial Analytics
-- description: ST_Covers
-- minvrm:  v7r4m0

-- Create a table with a polygon column and insert several example polygons that define the boundaries of different parks in New York City
DROP TABLE sample_parks;
CREATE TABLE sample_parks (park_name VARCHAR(50), park_geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, park_geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Create a ST_Polygon variable and set the default value to the polygon that defines the boundary of the Central Park Tennis Center
CREATE VARIABLE central_park_tennis_center QSYS2.ST_POLYGON;
SET central_park_tennis_center = QSYS2.ST_POLYGON('polygon((-73.9631 40.7900, -73.9610 40.7903, -73.9609 40.7897, -73.9630 40.7894))');

-- Query to find if one of the parks fully covers the Tennis Center
SELECT park_name, QSYS2.ST_COVERS(park_geometry, central_park_tennis_center) AS covers
  FROM sample_parks;


-- category: Geospatial Analytics
-- description: ST_Crosses
-- minvrm:  v7r4m0

-- Create a table with a polygon column and insert several example polygons that define the boundaries of different parks in New York City
CREATE TABLE sample_parks (park_name VARCHAR(50), park_geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, park_geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Create a linestring that defines the path of a street and set it to 97th Street in New York City
CREATE VARIABLE sample_street QSYS2.ST_LINESTRING;
SET sample_street = QSYS2.ST_LINESTRING('linestring(-73.9743 40.7966, -73.9436 40.7837)');

-- Query to find if the street crosses one of the parks
SELECT park_name, QSYS2.ST_CROSSES(sample_street, park_geometry) AS covers
  FROM sample_parks;


-- category: Geospatial Analytics
-- description: ST_Difference
-- minvrm:  v7r4m0

-- Find the difference between two disjoint polygons.
VALUES QSYS2.ST_ASTEXT(
   QSYS2.ST_DIFFERENCE(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                       QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))')));
                       
-- Find the difference between two intersecting polygons.
VALUES QSYS2.ST_ASTEXT(
   QSYS2.ST_DIFFERENCE(QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'),
                       QSYS2.ST_POLYGON('polygon((40 40, 60 40, 60 60, 40 60, 40 40))')));


-- category: Geospatial Analytics
-- description: ST_Disjoint
-- minvrm:  v7r4m0

-- Determine if two polygons are disjoint
VALUES QSYS2.ST_DISJOINT(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                         QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'));
                       
-- Determine if two polygons are disjoint
VALUES QSYS2.ST_DISJOINT(QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'),
                         QSYS2.ST_POLYGON('polygon((40 40, 60 40, 60 60, 40 60, 40 40))'));


-- category: Geospatial Analytics
-- description: ST_Distance
-- minvrm:  v7r4m0

-- Create a table with a point column and insert into it different geometries 
-- that represent points of interest in New York City
CREATE TABLE sample_points(location_name VARCHAR(50), location_point QSYS2.ST_POINT);
INSERT INTO sample_points VALUES
 ('Empire State Building', QSYS2.ST_POINT(-73.9854, 40.7488)),
 ('Chrysler Building', QSYS2.ST_POINT(-73.9755, 40.7516)),
 ('Rockefeller Center', QSYS2.ST_POINT(-73.9787, 40.7587));

-- Create a table with a polygon column and insert several example polygons that define the boundaries of different parks in New York City
CREATE TABLE sample_parks (park_name VARCHAR(50), park_geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, park_geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Find the distance from Washington Square Park to different points of interest in New York City
SELECT location_name, QSYS2.ST_DISTANCE(location_point, park_geometry) as distance_meters
  FROM sample_points, sample_parks
  WHERE park_name = 'Washington Square Park';


-- category: Geospatial Analytics
-- description: ST_GeometryType
-- minvrm:  v7r4m0

-- Create a table and insert a variety of different geometries into it
CREATE TABLE sample_geometries (id INTEGER, geometry QSYS2.ST_GEOMETRY);
INSERT INTO sample_geometries(id, geometry) VALUES
  (7101, QSYS2.ST_GEOMETRY('point(1 2)')),
  (7102, QSYS2.ST_GEOMETRY('linestring(33 2, 34 3, 35 6)')),
  (7103, QSYS2.ST_GEOMETRY('polygon((3 3, 4 6, 5 3, 3 3))')),
  (7104, QSYS2.ST_GEOMETRY('multipoint((1 2), (4 3))')),
  (7105, QSYS2.ST_GEOMETRY('multilinestring((10 10, 20 20),(-10 -10, -20 -20))')),
  (7106, QSYS2.ST_GEOMETRY('multipolygon(((10 10, 10 20, 20 20, 20 15, 10 10)),((60 60, 70 70, 80 60, 60 60 )))')),
  (7107, QSYS2.ST_GEOMETRY('GeometryCollection(POINT (10 10), POINT (30 30), LINESTRING (15 15, 20 20))'));

-- Find the type of each geometry in the table
SELECT id, QSYS2.ST_GEOMETRYTYPE(geometry) AS geometry_type
  FROM sample_geometries;


-- category: Geospatial Analytics
-- description: ST_Intersection
-- minvrm:  v7r4m0

-- Find the intersection of two overlapping polygons
VALUES QSYS2.ST_ASTEXT(
  QSYS2.ST_INTERSECTION(QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'),
                        QSYS2.ST_POLYGON('polygon((40 40, 60 40, 60 60, 40 60, 40 40))')));

-- Find the intersection of two disjoint polygons
VALUES QSYS2.ST_ASTEXT(
  QSYS2.ST_INTERSECTION(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                        QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))')));


-- category: Geospatial Analytics
-- description: ST_Intersects
-- minvrm:  v7r4m0

-- Determine if two polygons intersect
VALUES 
  QSYS2.ST_INTERSECTS(QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'),
                      QSYS2.ST_POLYGON('polygon((40 40, 60 40, 60 60, 40 60, 40 40))'));

-- Determine if two polygons intersect
VALUES
  QSYS2.ST_INTERSECTS(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                      QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'));


-- category: Geospatial Analytics
-- description: ST_IsSimple
-- minvrm:  v7r4m0

-- Create a table with a geometry column and insert different geometries
DROP TABLE sample_geometries;
CREATE TABLE sample_geometries (id INTEGER, geometry QSYS2.ST_GEOMETRY);
INSERT INTO sample_geometries VALUES
 (1, QSYS2.ST_GEOMETRY('point EMPTY')),
 (2, QSYS2.ST_POINT('point (21 33)')),
 (3, QSYS2.ST_MULTIPOINT('multipoint((10 10), (20 20), (30 30))')),
 (4, QSYS2.ST_MULTIPOINT('multipoint((10 10), (20 20), (30 30), (20 20))')),
 (5, QSYS2.ST_LINESTRING('linestring(60 60, 70 60, 70 70)')),
 (6, QSYS2.ST_LINESTRING('linestring(20 20, 30 30, 30 20, 20 30)')),
 (7, QSYS2.ST_POLYGON('polygon((40 40, 50 40, 50 50, 40 40))'));

-- Determine if the geometries in the table are simple or not
SELECT id,
    CASE QSYS2.ST_ISSIMPLE(geometry)
      WHEN 0 THEN 'Geometry is not simple'
      WHEN 1 THEN 'Geometry is simple'
    END AS simple
  FROM sample_geometries;


-- category: Geospatial Analytics
-- description: ST_IsValid
-- minvrm:  v7r4m0

-- Create a table with a geometry column and insert different geometries into it
-- Insert one invalid row that does not use a function to construct a geometry
CREATE TABLE sample_geometries (id INTEGER, geometry QSYS2.ST_GEOMETRY);
INSERT INTO sample_geometries VALUES
  (1, QSYS2.ST_GEOMETRY('point EMPTY')),
  (2, QSYS2.ST_POLYGON('polygon((40 20, 90 20, 90 50, 40 50, 40 20))')),
  (3, QSYS2.ST_MULTIPOINT('multipoint((10 10), (50 10), (10 30))')),
  (4, QSYS2.ST_LINESTRING('linestring (10 10, 20 10)')),
  (5, CAST('point(10 20)' AS BLOB(2G)));

-- Determine if any of the rows are invalid
SELECT id, QSYS2.ST_ISVALID(geometry) Is_Valid
  FROM sample_geometries;


-- category: Geospatial Analytics
-- description: ST_MaxX, ST_MaxY, ST_MinX, ST_MinY
-- minvrm:  v7r4m0

-- Create a table with a polygon column and insert several polygons that represent different New York City Parks
DROP TABLE sample_parks;
CREATE TABLE sample_parks (park_name VARCHAR(50), geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Find the maximum and minimum x and y coordinate for various New York City parks
SELECT park_name, 
       QSYS2.ST_MAXX(geometry) AS max_x,
       QSYS2.ST_MAXY(geometry) AS max_y,
       QSYS2.ST_MINX(geometry) AS min_x,
       QSYS2.ST_MINY(geometry) AS min_y
 FROM sample_parks;


-- category: Geospatial Analytics
-- description: ST_NumPoints
-- minvrm:  v7r4m0

-- Create a table with a geometry column and insert sample geometries of different types
DROP TABLE sample_geometries;
CREATE TABLE sample_geometries (id VARCHAR(18), geometry QSYS2.ST_GEOMETRY);
INSERT INTO sample_geometries (id, geometry)
  VALUES (1, QSYS2.ST_POINT('point (44 14)')),
         (2, QSYS2.ST_LINESTRING('linestring (0 0, 20 20)')),
         (3, QSYS2.ST_POLYGON('polygon((0 0, 0 40, 40 40, 40 0, 0 0))')),
         (4, QSYS2.ST_MULTIPOINT('multipoint((0 0), (10 20), (15 20), (30 30))')),
         (5, QSYS2.ST_MULTILINESTRING('MultiLineString((10 10, 20 20), (15 15, 30 15))')),
         (6, QSYS2.ST_MULTIPOLYGON('MultiPolygon(((10 10, 10 20, 20 20, 20 15, 10 10)),
                                                 ((60 60, 70 70, 80 60, 60 60 )))'));

-- Find how many points each geometries has
SELECT id, QSYS2.ST_GEOMETRYTYPE(geometry) AS spatial_type, 
       QSYS2.ST_NUMPOINTS (geometry) AS num_points
  FROM sample_geometries;


-- category: Geospatial Analytics
-- description: ST_Overlap
-- minvrm:  v7r4m0

-- Determine if two polygons overlap
VALUES QSYS2.ST_OVERLAPS(QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'),
                         QSYS2.ST_POLYGON('polygon((40 40, 60 40, 60 60, 40 60, 40 40))'));

-- Determine if two polygons overlap (polygons are disjoint)
VALUES QSYS2.ST_OVERLAPS(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                         QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'));
                       
-- Determine if two polygons overlap (polygons are the same)
VALUES QSYS2.ST_OVERLAPS(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                         QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'));


-- category: Geospatial Analytics
-- description: ST_Point
-- minvrm:  v7r4m0

-- This example shows how to create a table with a ST_POINT column, insert into the table, 
-- and query the table.

CREATE TABLE NATIONAL_PARKS
  (ID INT,
   NAME VARCHAR(30),
   LOCATION QSYS2.ST_POINT);

-- The point at the center of Yosemite National Park in the USA, using (longitude, latitude)
INSERT INTO NATIONAL_PARKS VALUES 
  (101, 'Yosemite National Park', QSYS2.ST_POINT(-119.539, 37.865));
  
-- A point at the center of Yellowstone National Park in the USA, using Well-Known Text (WKT)
INSERT INTO NATIONAL_PARKS VALUES
  (201, 'Yellowstone National Park', QSYS2.ST_POINT('point (-110.40 44.45)'));

-- The center of the Grand Canyon in the USA, using WKT
INSERT INTO NATIONAL_PARKS VALUES
  (301, 'Grand Canyon National Park', QSYS2.ST_POINT('point (-112.1129 36.1213)'));

-- Query the table, converting the ST_POINT value into a readable text format
SELECT ID, NAME, QSYS2.ST_ASTEXT(LOCATION)
  FROM NATIONAL_PARKS;


-- category: Geospatial Analytics
-- description: ST_Touches
-- minvrm:  v7r4m0

-- Determine if two linestrings touch
VALUES QSYS2.ST_TOUCHES(QSYS2.ST_LINESTRING('linestring(0 0, 1 1)'),
                        QSYS2.ST_LINESTRING('linestring(1 1, 2 2)'));
                        
-- Determine if a linestring and polygon touch
VALUES QSYS2.ST_TOUCHES(QSYS2.ST_LINESTRING('linestring(0 0, 5 5)'),
                        QSYS2.ST_POLYGON('polygon((1 1, 1 2, 2 2, 2 1, 1 1))'));


-- category: Geospatial Analytics
-- description: ST_Union
-- minvrm:  v7r4m0

-- Get the union of two intersecting polygons
VALUES QSYS2.ST_ASTEXT(
  QSYS2.ST_UNION(QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))'),
                 QSYS2.ST_POLYGON('polygon((40 40, 60 40, 60 60, 40 60, 40 40))')));

-- Get the union of two disjoint polygons
VALUES QSYS2.ST_ASTEXT(
  QSYS2.ST_UNION(QSYS2.ST_POLYGON('polygon((10 10, 20 10, 20 20, 10 20, 10 10))'),
                 QSYS2.ST_POLYGON('polygon((30 30, 50 30, 50 50, 30 50, 30 30))')));


-- category: Geospatial Analytics
-- description: ST_Within
-- minvrm:  v7r4m0

-- Create a table with a polygon column and insert several example polygons that define the boundaries of different parks in New York City
DROP TABLE sample_parks;
CREATE TABLE sample_parks (park_name VARCHAR(50), park_geometry QSYS2.ST_POLYGON);
INSERT INTO sample_parks (park_name, park_geometry) VALUES
  ('Central Park', QSYS2.ST_POLYGON('polygon((-73.9817 40.7682, -73.9581 40.8005, -73.9495 40.7968, -73.9732 40.7644, -73.9817 40.7682))')),
  ('Washington Square Park', QSYS2.ST_POLYGON('polygon((-73.9995 40.7310, -73.9986 40.7321, -73.9957 40.7307, -73.9966 40.7297, -73.9995 40.7310))'));

-- Create a ST_Polygon variable 
-- Set the value to the polygon that defines the boundary of the Central Park Tennis Center
CREATE VARIABLE central_park_tennis_center QSYS2.ST_POLYGON;
SET central_park_tennis_center = QSYS2.ST_POLYGON('polygon((-73.9631 40.7900, -73.9610 40.7903, -73.9609 40.7897, -73.9630 40.7894))');

-- Query to find if the Tennis Center is fully within one of the parks
SELECT park_name, QSYS2.ST_WITHIN(central_park_tennis_center, park_geometry) AS within
  FROM sample_parks;


values user;


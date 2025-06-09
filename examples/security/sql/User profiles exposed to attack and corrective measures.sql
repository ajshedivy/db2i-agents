-- Scott Forstie
-- Date: June 6, 2025

-- To test... make sure that at least 1 user profile is exposed to this attack
cl: crtusrprf topadmin;
cl: crtusrprf topadmin2;
cl:GRTOBJAUT OBJ(QSYS/TOPADMIN) OBJTYPE(*USRPRF) USER(*PUBLIC) AUT(*USE);
cl:GRTOBJAUT OBJ(QSYS/TOPADMIN2) OBJTYPE(*USRPRF) USER(*PUBLIC) AUT(*USE);

stop;

--  category:  IBM i Services
--  description:  Security - User profile attack vector
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- How many *USRPRF's do not have *PUBLIC set to *EXCLUDE?
--
SELECT COUNT(*)
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
          'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
        '*EXCLUDE';
stop;

--
-- Which *USRPRF's do not have *PUBLIC set to *EXCLUDE?
--
SELECT object_name AS user_name, object_authority
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
          'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
        '*EXCLUDE';
stop;

--
-- Which *USRPRF's do not have *PUBLIC set to *EXCLUDE?
-- Include a query that corrects the exposure
--
SELECT object_name AS user_name, object_authority,
       'select qsys2.qcmdexc(''QSYS/GRTOBJAUT OBJ(QSYS/' CONCAT object_name CONCAT
         ') OBJTYPE(*USRPRF) USER(*PUBLIC) AUT(*EXCLUDE)'') from sysibm.sysdummy1'
         AS corrective_query
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
          'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
        '*EXCLUDE';
stop;

SELECT object_name AS user_name, 
        object_authority,
        'SELECT qsys2.qcmdexc(''GRTOBJAUT OBJ(QSYS/' || object_name || 
          ') OBJTYPE(*USRPRF) USER(*PUBLIC) AUT(*EXCLUDE)'') FROM sysibm.sysdummy1'
          AS corrective_query
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' 
    AND object_type = '*USRPRF' 
    AND object_name NOT IN ('QDBSHR', 'QDBSHRDO', 'QDOC', 'QTMPLPD') 
    AND user_name = '*PUBLIC' 
    AND object_authority <> '*EXCLUDE';

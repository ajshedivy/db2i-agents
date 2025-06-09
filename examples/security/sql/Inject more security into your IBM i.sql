--  category:  IBM i Services
--  description:  Security - IFS home directories
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- IFS home directories - Summary
-- Where *PUBLIC authorization is NOT set to DTAAUT(*EXCLUDE) OBJAUT(*NONE)--  category:  IBM i Services
--  description:  Security - IFS home directories
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- IFS home directories - Summary
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
         group by data_authority;
         
         --  category:  IBM i Services
--  description:  Security - IFS home directories
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- IFS home directories - Summary
-- Where *PUBLIC authorization is NOT set to DTAAUT(*EXCLUDE) OBJAUT(*NONE)--  category:  IBM i Services
--  description:  Security - IFS home directories
--  Use Db2 for i to Inject more Security into your IBM i
--  minvrm:  v7r3m0

--
-- IFS home directories - Summary
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
stop;  
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
stop;  
  
--
-- IFS home directories - Detail
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
stop;  
  
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
stop;


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
stop;

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
stop;

--
-- Files where ANY user can insert rows
--
WITH libs (lib_name) AS (
    SELECT object_name
      FROM qsys2.object_privileges
      WHERE system_object_schema = 'QSYS' AND object_type = '*LIB' AND user_name = '*PUBLIC' AND
            data_execute = 'YES'
  )
  SELECT count(*)
    FROM libs, qsys2.object_privileges
    WHERE system_object_schema = lib_name AND object_type = '*FILE' AND user_name = '*PUBLIC' AND
          data_add = 'YES' AND ('PF' = (SELECT objattribute
                FROM TABLE (
                    qsys2.object_statistics(lib_name, '*FILE', object_name)
                  )));

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
stop;

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
stop;

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
                  ))) and owner = 'QSYS'; 
stop;

--
-- What is *PUBLIC set to for the most productive attack vector commands?
--
SELECT object_name, object_type, object_authority
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*CMD' AND 
        object_name IN ('ADDPFTRG', 'CRTPGM', 'CRTSRVPGM', 'SAVOBJ', 
                        'SAVLIB', 'CRTDUPOBJ', 'CPYF') AND 
        user_name = '*PUBLIC';
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
stop;
   
--
-- Enable object auditing of a command
--
cl: QSYS/CHGOBJAUD OBJ(QSYS/ADDPFTRG) OBJTYPE(*CMD) OBJAUD(*ALL); 
stop;

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
stop;

--
-- Which *USRPRF's do not have *PUBLIC set to *EXCLUDE?
--
SELECT object_name AS user_name, object_authority, owner
  FROM qsys2.object_privileges
  WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
          'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
        '*EXCLUDE';
stop;

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
stop;

--
-- Which users are configured with "Limited Capabilities"?
--
SELECT *
  FROM qsys2.user_info_basic
  WHERE limit_capabilities = '*YES';
  

stop;

--
-- Which commands can be executed by users with "Limited Capabilities"?
--
SELECT *
  FROM qsys2.command_info
  WHERE allow_limited_user = 'YES';
stop;







   

--
-- Additional health checks
--
-- If any of these health checks fail, the user will not be 
-- able to understand how the IBM i got into its current state
--
-- Note: To see this information, the current user needs to 
--       have *ALLOBJ or *AUDIT special authority.


-- 
-- Audit journal check 
--
select count(*) from qsys2.security_info
  where audit_journal_exists <> 'YES';
stop;

-- or would this be better?
SELECT audit_journal_exists,
       CASE
         WHEN audit_journal_exists = 'YES' THEN 'QSYS/QAUDJRN exists'
         ELSE 'QSYS/QAUDJRN does not exist'
       END as QAUDJRN_health_check
  FROM qsys2.security_info;
stop;
  
--
-- Audit journaling check
--
select auditing_control,
       CASE
         WHEN (select 1 from qsys2.security_info where auditing_control like '%AUDLVL%') = 1 
         THEN 'QAUDCTL has audit journing enabled'
         ELSE 'QAUDCTL does not have audit journing enabled'
       END as QAUDCTL_health_check from qsys2.security_info ;
 
stop; 
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

-- what's the current audit journal receiver?
with aj(aj_lib, aj_rcv) as (
select audit_journal_receiver_library, audit_journal_receiver from qsys2.security_info
) 
select * from aj;

--
-- How far back in time can audit journal queries go?
--

-- what's the current audit journal receiver?
with aj(aj_lib, aj_rcv) as (
select audit_journal_receiver_library, audit_journal_receiver from qsys2.security_info
) 
select timestamp(jj.attach_timestamp, 0) as earliest_online_audit_data from aj, lateral
 (select * from qsys2.journal_receiver_info where journal_receiver_library = aj_lib and 
 left(journal_receiver_name, 6) = left(aj_rcv, 6) order by attach_timestamp
 limit 1) jj  ;

--
-- Is this IBM i configured to capture security related changes?
-- Note: auditing_control         == QAUDCTL 
--       auditing_level           == QAUDLVL and
--       auditing_level_extension == QAUDLVL2
--
select case when count(*) = 1 then 'Audit journal includes security changes'
  else 'Security changes are not being audited, review the audit journal configuration' 
  end as audit_journal_configuration_for_security
  from qsys2.security_info
  where (auditing_control like '%*AUDLVL%') and
          (((auditing_level like '%*SECURITY%') or (auditing_level like '%*SECRUN%'))) or
        (auditing_level like '%*AUDLVL2%' and
          ((auditing_level like '%*SECURITY%') or (auditing_level like '%*SECRUN%')));


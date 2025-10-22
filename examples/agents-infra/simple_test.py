
from db.ibmi import run_sql_statement

if __name__ == "__main__":
    print(run_sql_statement("select * from sample.employee limit 2"))

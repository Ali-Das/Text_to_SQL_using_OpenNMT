from onmt.utilities.sql_gen_util import SqlGenUtil

sql_file = SqlGenUtil()
print("Creating text files containing SQL queries .......")
sql_file.build_sql_from_txt("test", "pred")
sql_file.build_sql_from_txt("test", "tgt-test")
print("over")
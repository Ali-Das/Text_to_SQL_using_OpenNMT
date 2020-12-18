from onmt.utilities.sql_gen_util import SqlGenUtil

sql_file = SqlGenUtil()
print("Creating SQL text file for NMT model.......")
sql_file.build_sql_from_txt("test", "pred")
sql_file.build_sql_from_txt("test", "tgt-test")
print("over")
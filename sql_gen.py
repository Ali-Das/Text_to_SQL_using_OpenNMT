from onmt.utilities.sql_gen_util import SqlGenUtil
from argparse import ArgumentParser
from onmt.library.dbengine import DBEngine

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('text_file', help='text file generated from WikiSQL data or model')
    parser.add_argument('db_jsonl_file', help='database name')
    parser.add_argument('output_sql_file', help='output SQL file')
    parser.add_argument('--ordered', action='store_true', help='whether the exact match should consider the order of conditions')
    args = parser.parse_args()

   
sql_file = SqlGenUtil()
print("Creating text files containing SQL queries .......")
sql_file.build_sql_from_txt(args.text_file, args.db_jsonl_file, args.output_sql_file)
print("over")
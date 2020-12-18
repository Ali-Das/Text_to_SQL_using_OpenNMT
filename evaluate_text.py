#!/usr/bin/env python
import json
from argparse import ArgumentParser
from onmt.library.dbengine import DBEngine

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('goldText_file', help='Gold file for the prediction')
    parser.add_argument('db_file', help='source database for the prediction')
    parser.add_argument('predText_file', help='predictions by the model')
    parser.add_argument('--ordered', action='store_true', help='whether the exact match should consider the order of conditions')
    args = parser.parse_args()

    engine = DBEngine(args.db_file)

    fg = open(args.goldText_file, "r", encoding="utf-8")
    fp = open(args.predText_file, "r", encoding="utf-8")

    fg_contents = fg.readlines()
    fp_contents = fp.readlines()
    flen = len(fp_contents)
    print("length of files: ", flen)
    exact_match = []
    grades = []
    length = None
    count_gold = 0
    count_pred = 0
    ex_count = 0
    lf_count = 0
    count = 0
    for line1, line2 in zip(fg_contents, fp_contents):

        try:
            gold = engine.execute_query(line1)
            if gold is not None:
              count_gold += 1
        except Exception as e:
            gold = repr(e)
        try:
            pred = engine.execute_query(line2)
            if pred is not None:
              count_pred += 1
        except Exception as e:
            pred = repr(e)
        if pred is not None:
          if gold is not None:
            count += 1

            if pred == gold:
              ex_count += 1

        if line1 == line2:
          lf_count += 1

    print(json.dumps({
        'execution accuracy': ex_count / count,
        'Exact match accuracy': lf_count / count,
        }, indent=2))
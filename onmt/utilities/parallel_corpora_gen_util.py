from __future__ import unicode_literals, print_function, division
from onmt.library.query import Query
import pandas as pd
import nltk


class ParallelCorporaGenUtil:
    """Class is responsible for converting all the sql structured output to plain text sql queries"""

    def __init__(self):
        pass

    def build_parallel_corpora_from_json(self, dataset):

        """Reads the input training files and generates a new file containing plain text sql queries"""
        # self.build_table_mapping(dataset)
        queries = pd.read_json("data/tokenized_" + dataset + ".jsonl", lines=True)
        tables = pd.read_json("data/tokenized_" + dataset + ".tables.jsonl", lines=True)
        # iterate over the queries and convert each one to plain text sql
        filename_tgt = "data/tgt_" + dataset + ".txt"
        filet = open(filename_tgt, "w", encoding="utf-8")
        filename_src = "data/src_" + dataset + ".txt"
        files = open(filename_src, "w", encoding="utf-8")
        for index, line in queries.iterrows():
            # get query and nlq representations
            #query_str, nlq = self.get_corpora_from_json(line)
            #print("\n query_str:", query_str, " nlq:", nlq)
            # Save dataframe to file
            t_id = line["table_id"]
            title = None
            for indx, ln in tables.iterrows():
                table_id = ln["id"]
                if table_id == t_id:
                    title = ln["page_title"]
                    break
            #title_str = "".join(title)

            tokens_en = line["tokenized_question"]
            tokens_sql = line["tokenized_query"]

            for i in range(len(tokens_en)):
                if tokens_en [i] == '?':
                    tokens_en [i] = ''
            nlq_str = " ".join(tokens_en)
            nlq_str += " from "
            nlq_str += str(title)
            files.write(nlq_str)
            files.write("\n")

            for i in range(len(tokens_sql)):
                if tokens_sql[i].lower() == 'table' or tokens_sql[i].lower() == 'table_':
                    tokens_sql[i] = str(title)
            query_str = " ".join(tokens_sql)

            filet.write(query_str)
            filet.write("\n")
            #print("\n nlq_str:", nlq_str, "query_str:", query_str)
        filet.close()
        files.close()

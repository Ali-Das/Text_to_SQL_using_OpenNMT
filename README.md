## Text_to_SQL_using_OpenNMT: Redefining Text-to-SQL Task as a Machine Translation problem
This repo provides an implementation of a model for predicting SQL queries on [WikiSQL dataset](https://github.com/salesforce/WikiSQL). 
The open-source neural machine translation toolkit [OpenNMT](http://opennmt.net/) is used to train this model on a parallel corpora generated using WikiSQL dataset.

Table of Contents
=================
  * [Installation](#Installation)
  * [Quickstart](#quickstart)
  * [Alternative: Run on google colab](#alternative-run-on-google-colab)
  * [Citation](#citation)
  * [Acknowledgement](#Acknowledgement)


## Installation
The code is written in Python 3.5 and above.

### Step I:Install `OpenNMT-py` :

from `pip`:
```bash
pip install OpenNMT-py==1.2.0
```

or from the sources:
```bash
git clone https://github.com/OpenNMT/OpenNMT-py.git
cd OpenNMT-py
python setup.py install
```
### Step II: You can install other dependency by running 
```bash
pip install -r requirements.opt.txt

```

### Step III: Download the glove embedding.
Download the pretrained glove embedding from [here](https://github.com/stanfordnlp/GloVe).

### Step IV: Downloading the WikiSQL dataset.
The WikiSQL dataset is already downloaded from [here](https://github.com/salesforce/WikiSQL) .
From these files 'tokenized.dev.tables.jsonl', 'tokenized.test.tables.jsonl' and 'tokenized.train.tables.jsonl' have been generated and kept in the data/wikisql_data folder.

## Quickstart

### Step 1: generation of parallel corpora

We have already generated the parallel source (`src`) and target (`tgt`) data from the WikiSQL data and stored in the data/text_files folder:
* `src_train.txt`
* `tgt_train.txt`
* `src_val.txt`
* `tgt_val.txt`
* `src_test.txt`
* `tgt_test.txt`

Validation files are required and used to evaluate the convergence of the training. 


### Step 2: Preprocess the data

```bash
onmt_preprocess -train_src data/text_files/src_train.txt -train_tgt data/text_files/tgt_train.txt -valid_src data/text_files/src_dev.txt -valid_tgt data/text_files/tgt_dev.txt -save_data data/demo
```

After running the preprocessing, the following files are generated and stored in the data folder:

* `demo.train.pt`: serialized PyTorch file containing training data
* `demo.valid.pt`: serialized PyTorch file containing validation data
* `demo.vocab.pt`: serialized PyTorch file containing vocabulary data

Internally the system never touches the words themselves, but uses these indices.

### Step 3: Create Glove embedding to torch 

```bash 
python tools/embeddings_to_torch.py -emb_file_both glove/glove.6B.100d.txt -dict_file venv/demo.vocab.pt -output_file data/embeddings
```

After running the embeddings_to_torch.py, the following files are generated and stored in the data folder:

* `embeddings.enc.pt`: serialized PyTorch file containing embeddings for encoder
* `embeddings.dec.pt`: serialized PyTorch file containing embeddings for decoder
### Step 4: Train the model

To train on CPU:

```bash
onmt_train -save_model data/model -batch_size 64 -layers 2 -rnn_size 500 -word_vec_size 500 -pre_word_vecs_enc data/embeddings.enc.pt -pre_word_vecs_dec data/embeddings.dec.pt -data data -world_size 1 -save_checkpoint_steps 10000 -report_every 5000   
```

To train on GPU:

```bash
onmt_train -save_model data/model -batch_size 64 -layers 2 -rnn_size 500 -word_vec_size 500 -pre_word_vecs_enc data/embeddings.enc.pt -pre_word_vecs_dec data/embeddings.dec.pt -data data -world_size 1 -gpu_ranks 0 -save_checkpoint_steps 10000 -report_every 5000 
```
The training parameters can be changed. Read [OpenNMT](http://opennmt.net/) for more information.

### Step 5: Translate
Now you have a model which you can use to predict on new data. We do this by running beam search. This will output predictions into `pred.txt`.

```bash
onmt_translate -model data/model_step_100000.pt -src data/text_files/src_test.txt -tgt data/text_files/tgt_test.txt -output data/text_files/pred.txt
```

### Step 6: Evaluate
After translation,the output pred.text file is converted to a text file that contains SQL queries. Similarly the tgt_test.text file is also converted to contain SQL queries.
Then queries of these two files are executed and compared to test the accuracy of the predicted model.

```bash
python sqlgen.py data/text_files/tgt_test.txt data/wikisql_data/tokenized_test.tables.jsonl data/text_files/tgt_test_sql.txt
python sqlgen.py data/text_files/pred.txt data/wikisql_data/tokenized_test.tables.jsonl data/text_files/pred_sql.txt
python evaluate.py data/text_files/tgt_test_sql.txt data/wikisql_data/test.db data/text_files/pred_sql.txt
```

## Alternative: Run on google colab
If you want to train in GPU or your system is not good enough to train the model, you can use [google colab](https://colab.research.google.com/notebooks/intro.ipynb).
upload the folder Text_to_SQL_using_OpenNMT to google drive. Open the file 'Text_to_SQL_using_OpenNMT.ipynb' in google colaboratory and execute the notebook codes of the file.

## Citation

> Alaka Das, Redefining Text-to-SQL Task as a Machine Translation problem

## Acknowledgement

The implementation is based on 
[OpenNMT: Neural Machine Translation Toolkit](https://arxiv.org/pdf/1805.11462), 
[WikiSQL dataset](https://github.com/salesforce/WikiSQL). 
Please cite them too if you use this code.


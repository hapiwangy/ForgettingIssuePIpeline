# ForgettingIssuePipeline
## final file system
- dataset
    - dataset
        - prompt.txt (optional)
        - data_process.py (optional)
        - train.csv
        - test.csv
        - val.csv
    - datasetb
    ...
## data preprocessing
### how to function: run a 1_pre_processing.ipynb

- input: dataset
    - from huggingface/ local/ on the net
- output: directory under "dataset"
    - directory name: dataset name
        - files:
            - train.csv
            - test.csv
            - val.csv
        - data_process: contain in the cell in .ipynb file
        - prompt: contained in the cell in .ipynb file
        - dataset discription: contained in the cell in .ipynb file
> each of them should contain 
    - "label" for True label
    - "prompt" for the prompt with questions 

## change dataset into the aplaca format (.jsonl)
> with aplaca_formattter.py

## combine two dataset with X% 
- new python file
- input (datasetA, datasetB, X%) > output (datasetAX%datasetB) // X % of datasetB are included in datasetA
- output (under) adding one directoty into the dataset folder
    - datasetAX%datasetB(folder)
        - train.csv(file) // only contain with the train since this is the only matter
(V)

## update dataset_info.jsonl
- new python file
(V)

## produce the config.yaml > for training
- new python file
- input(dataset1, dataset2)
- output three files under the folder(with name of dataset1)
    - finetune_dataset1
        - base: llama-3.2-1B-instruct
        - out: llama-finetune-dataset1
    - finetune_dataset1_dataset2
        - base: llama-finetune-dataset1
        - out: llama-finetune-dataset1-dataset2
    - finttune_dataset1_dataset21percentdataset1
        - base: llama-finetune-dataset1
        - out: llama-finetune-dataset1x%dataset2
## produce the evaluate,yaml
- new dataset file
- input(dataset)
- output    
    - zero-shot: dataset1_zeroshot
    - fist_finetune: dataset1_firsttune
    - second_finetune: dataset1_fsceondtune
    - third_finetune: datasett1_thirdfinetune


## more files to produce
- produce .job file
## produce the compare the answer
- if too hard, this part can be done with manual 
- for each dataset, we need to check the result to know how to transfer the answer 

token: 
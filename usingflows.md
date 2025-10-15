running flow
# 1. python 1_pre_processing.ipynb 
```
output: 
directory "dataset" with subdirectory name with each dataset
```
# 2. python 2_aplaca_formatter.py
```
output:
directory "files_to_server/dataset" with subdirectory with each dataset
```
# 3. run bash 3_help_script.sh
```
output:
under directory "files_to_server/dataset" create the different of mixed dataset train.jsonl
```
# 4. python 4_dataset_info.py
```
output: 
under directory "files_to_server/dataset" create dataset_info.json
```
# 5. bash 5_train_config.sh
```
under directory "files_to_server/dataset/ each dataset" create the specific train_config and evaluate_config yaml
```
# 6. python makeing_job.py
```
under directory "files_to_server/dataset/ each dataset" create the .job for the main dataset
```

# Things to take care of
## when adding new dataset
- update help_script.sh to every two dataset
    - implement > use a new list to record the current used datasets, and write combination about them
- train_config to make sure that create right config for new dataset
## how to record the different kind of datasets used in last step
- create a script after 1_pre_processing.ipynb, which have to be used manual since it is hard to create the automate flow
    - after that get the datasetset from the "dataset" directory
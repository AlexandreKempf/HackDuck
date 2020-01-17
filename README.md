# IDEAL HACKDUCK PROJECT


Several pipelines for dataflow (Prefect):
  - nothing -> data_generation -> save to disk
  - preprocessing
  - augmentation
  - postprocessing

Model handle (Pytorch & Ignite):
  - fit -> give X and Y and learn
  - evaluate -> give X and Y, predict and return metrics
  - predict -> give X, return Y

Save logs and artifacts (MLflow):
  - save metrics during training (ignite)
  - save a bunch of data before and after each pipeline

Run model from with a REST app (MLflow):
  - save a github folder for each project
  - can easely have predition on a bunch of data



# FEATURES:
 - seed for reproducibility
 - map arguments to loop over a list
 - mlflow integration (automatic logs parameters, can log metrics or artifacts)
 - all prefect avantages
 - handle subflows
 - task bank to do basic operations
 - unit test handle by ward


# TODO:
[ ] map over subflows ?
[ ] create a script to run it with HackDuck file.yaml --argsname argvalue ...
[ ] save version for all requirements (needed to rerun the flow)
[ ] save python files inside mlruns/... and git them and save git commit
[ ] being able to rerun a previous flow (save args and kwargs and output ref)
[ ] run it in a docker
[ ] put to prod thanks to travis CI that create the MLflow git repo
[ ] do deep learning with it


# use it
```python
config = yaml.load(open('/home/alex/awesome/HackDuck/iris/flows/iris_classif_with_sub.yaml', 'r'), Loader=yaml.FullLoader)
run_flow(config, {})
```

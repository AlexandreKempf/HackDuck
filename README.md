# IDEAL HACKDUCK PROJECT

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
 - [ ] map over subflows ?
 - [ ] run it in a docker
 - [ ] save version for all requirements (needed to rerun the flow)
 - [ ] save python files inside mlruns/... and git them and save git commit
 - [ ] being able to rerun a previous flow (save args and kwargs and output ref)
 - [ ] put to prod thanks to travis CI that create the MLflow git repo
 - [ ] generate examples for people to use


# use it

```bash
hackduck config.yaml --threshold 5
```

or

```python
from HackDuck import run_flow
import yaml
config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
run_flow(config, {'threshold': 5})
```

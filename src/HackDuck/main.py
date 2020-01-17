import numpy as np
from prefect import task, Parameter, Flow, unmapped
from prefect.tasks.core.constants import Constant
from mlflow import log_param, log_artifact, set_experiment, set_tags
import yaml
import TaskBank as tb
import simplejson
import os
import torch


def get_args(args):
    if isinstance(args, str):
        return [args]
    return args


def get_task_args(op, ref, maps):
    args = get_args(op.get('args', []))
    return [ref[arg] if arg in maps else unmapped(ref[arg]) for arg in args]


def get_task_kwargs(op, ref, maps):
    new_kwargs = {}
    for k, v in op.get('kwargs', {}).items():
        if isinstance(v, str) and v.startswith(':'):
            v = ref[v[1:]]
        else:
            v = Constant(v)
        if k not in maps:
            v = unmapped(v)
        new_kwargs[k] = v
    return new_kwargs


def get_task_output(op, run):
    out = get_args(op.get('out', []))
    if len(out) == 1:
        return {k: run for k in out}
    else:
        return {k: run[i] for i, k in enumerate(out)}


def _run(op, args, kwargs, maps):
    if len(maps):
        return task(getattr(tb, op['f'])).map(*args, **kwargs)
    else:
        return task(getattr(tb, op['f']))(*args, **kwargs)


def run_task(op, ref):
    maps = get_args(op.get('map', []))
    args = get_task_args(op, ref, maps)
    kwargs = get_task_kwargs(op, ref, maps)
    run = _run(op, args, kwargs, maps)
    ref.update(get_task_output(op, run))
    return ref


def load_flow_inputs(config, main):
    ref = {}
    for i, arg in enumerate(get_args(config.get("args", []))):
        ref[arg] = Parameter(arg)
        if main:
            log_param(f"args{i}", arg)
    for k, v in config.get("kwargs", {}).items():
        ref[k] = Parameter(k, default=v)
        if main:
            log_param(k, v)

    return ref


def return_flow_output(config, ref, state):
    out = get_args(config.get('out', []))
    if len(out) == 1:
        return state.result[ref[out[0]]].result
    else:
        return [state.result[ref[k]].result for k in out]


def _log_xp(config, name):
    set_experiment(name)
    set_tags(config.get('tags', {}))

    simplejson.dump(config, open(f"/tmp/config.json", "w"))
    log_artifact(f"/tmp/config.json")
    os.remove(f"/tmp/config.json")
    return name


def _set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)

def run_flow(config, callargs, main=True):

    name = config.get('name', 'Default')
    if main:
        _set_seed(config.get('seed', 0))
        # save python code here:
        # os.path.dirname(os.path.dirname(mlflow.get_artifact_uri()))
        name = _log_xp(config, name)

    with Flow(name) as flow:
        ref = load_flow_inputs(config, main)
        for op in config.get('flow', []):
            if op['f'].endswith('.yaml'):
                subconfig = yaml.load(open(op['f'], 'r'), Loader=yaml.FullLoader)
                args = dict(zip(subconfig.get('args', []), get_task_args(op, ref, [])))
                kwargs = get_task_kwargs(op, ref, [])
                kwargs.update(args)
                run = task(run_flow)(subconfig, kwargs, main=False)
                ref.update(get_task_output(op, run))
            else:
                ref = run_task(op, ref)
    if main:
        flow.save(f"/tmp/flow.flow")
        log_artifact(f"/tmp/flow.flow")
        os.remove(f"/tmp/flow.flow")
    state = flow.run(**callargs)
    return return_flow_output(config, ref, state)

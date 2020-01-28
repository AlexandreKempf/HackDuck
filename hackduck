#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import HackDuck
from clint.arguments import Args
from clint.textui import puts, colored
import yaml

args = Args().grouped

config = args.pop('_').all[0] # get_config
config = yaml.load(open(config.strip(), 'r'), Loader=yaml.FullLoader)

callargs = {}
for k, v in args.items():
    k = k.strip("-")
    v = v[0] if len(v)==1 else v
    callargs[k] = v

def main(config, callargs):
    HackDuck.run_flow(config, callargs)

if __name__ == "__main__":
    main(config, callargs)

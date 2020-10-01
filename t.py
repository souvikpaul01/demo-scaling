import copy
import sys
from ruamel.yaml import YAML
import os
import json
from pathlib import Path
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.compat import ordereddict
from collections import OrderedDict
import fileinput
#import glob
#print(glob.glob("/.opera/"))

path = '/home/ubuntu/opera/xopera-opera/examples/nginx_openstack/webApp-loadbalancer-node_exporter-TOSCA/demo-scaling/.opera/'

with open(path +'root_file','r') as file:
   filedata = file.read()

#print(data[0])

replacement_text = 'checkpoint_1.yaml'

filedata = filedata.replace(filedata, replacement_text)

with open(path +'root_file', 'w') as file:
  file.write(filedata)

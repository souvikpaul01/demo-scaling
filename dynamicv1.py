#pip install ruamel.yaml
import copy
import sys
from ruamel.yaml import YAML
import os
import json
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.compat import ordereddict
from collections import OrderedDict
'''
Not in use For Current Scenerio
def find(x):
    nodes = cntnt["topology_template"]["node_templates"]
    for node in nodes:
        u = node.split('_')
        if u[0] == x :
            break
    return u[0], node

def change(c):
    name, name_i = find(c)
    if name == c and name_i[-2:] == 'xx' :
        r = name_i.replace("xx","09")

        return r
'''


def run(c):
    if c:
        next_node = check_host(c)
        nodesToChange[c]= ''

        if next_node not in nodesToChange:
           run(next_node)
        findNodesToChange(c)


def findNodesToChange(c):
      for node in cntnt["topology_template"]["node_templates"]:
        i = check_host(node)
        if i == c:
          if node not in nodesToChange:
            run(node)


def update_dy(v,var):
    var = str(var)
    node_to_change = v.replace("xx",var)
    original_node = v
    cntnt["topology_template"]["node_templates"][node_to_change] = copy.deepcopy(cntnt["topology_template"]["node_templates"][original_node])
    if 'requirements' in cntnt["topology_template"]["node_templates"][node_to_change].keys():
        for i in cntnt["topology_template"]["node_templates"][node_to_change]['requirements']:
            if 'host' in i.keys():
                i['host'] = i['host'].replace("xx",var)
    if 'properties' in cntnt["topology_template"]["node_templates"][node_to_change].keys():
        if 'name' in cntnt["topology_template"]["node_templates"][node_to_change]['properties'].keys():
            cntnt["topology_template"]["node_templates"][node_to_change]['properties']['name']=cntnt["topology_template"]["node_templates"][node_to_change]['properties']['name'].replace("xx",var)
    print(cntnt["topology_template"]["node_templates"])
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
def check_host(k):
    node = k
    nodes = cntnt["topology_template"]["node_templates"][node] 
    if 'requirements' in nodes.keys():
        for requirement in nodes['requirements']:
            if 'host' in requirement.keys():
                host_i = requirement['host']
                return host_i



if __name__ == "__main__":
    input_file  =  open(sys.argv[1],'r')
    req = sys.argv[2] + '_xx'

    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False
    cntnt = yaml.load(input_file)
    file = cntnt

    # Check the latest number of scalable instance and get  the num from the json file
    data_file = open('data.json','w')
    if os.stat("data.json").st_size == 0:
        node_to_write = {
		'scale_index':0
		}
        with open('data.json','w') as write_file:
            json.dump(node_to_write,write_file)
        data = node_to_write
        var = data['scale_index'] + 1

    else:
        data =json.load(data_file)
        var = data['scale_index']+1

    nodesToChange = {}
    run(req)
    for scalable_nodes in nodesToChange.keys():
       update_dy(scalable_nodes,var)

    tmp = cntnt["topology_template"]["node_templates"]['nginx-lb']
    del cntnt["topology_template"]["node_templates"]['nginx-lb']
    cntnt["topology_template"]["node_templates"]['nginx-lb']=tmp

    '''

    tmp = cntnt["topology_template"]["node_templates"]
    del cntnt["topology_template"]["node_templates"]
    cntnt["topology_template"]["node_templates"] = {}
    update

    for a in tmp:
        cntnt["topology_template"]["node_templates"].add(a)

    '''


    #Save the num to a json file.
    data['scale_index'] = var
    with open('data.json','w') as write_file:
        json.dump(data,write_file)

    with open('service_test_gen.yaml','w') as yamlfile:
        yaml.dump(cntnt, yamlfile)

    input_file.close()



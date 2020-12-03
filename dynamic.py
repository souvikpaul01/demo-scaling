#pip install ruamel.yaml
import copy
import sys
from ruamel.yaml import YAML
import os
import json
from pathlib import Path
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

def update_dy2(v,var):
    var = str(var)
    node_to_change = v.replace("xx",var)
    original_node = v


    newNode = copy.deepcopy(cntnt["topology_template"]["node_templates"][original_node])

    if 'requirements' in newNode.keys():
        for i in newNode['requirements']:
            if 'host' in i.keys():
                i['host'] = i['host'].replace("xx",var)
    if 'properties' in newNode.keys():
        if 'name' in newNode['properties'].keys():
            newNode['properties']['name']=newNode['properties']['name'].replace("xx",var)

#    cntnt["topology_template"]["node_templates"][node_to_change] = newNode
#    print(newNode)
    return node_to_change, newNode

   # print(cntnt["topology_template"]["node_templates"])
   # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")



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
    checkpoint = cntnt


# Check the latest number of scalable instance and get  the num from the json file
    my_file = Path("data.json")
    if my_file.is_file():
        data_file = open('data.json','r+')
        data =json.load(data_file)
        var = data['scale_index']+1
    else:
        node_to_write = {
		'scale_index':0
		}
        with open('data.json','w') as write_file:
            json.dump(node_to_write,write_file)
        data = node_to_write
        var = data['scale_index'] + 1


    list_node = []
    list_prop = []
    nodesToChange = {}
    run(req)
    dict_res = {}

    for scalable_nodes in nodesToChange.keys():
        newNode, newNode_properties = update_dy2(scalable_nodes,var)
        list_prop.append(newNode_properties)
        list_node.append(newNode)
    dict_res = dict(zip(list_node,list_prop))
  #  print(dict_res)
    tmp = cntnt["topology_template"]["node_templates"]


    cntnt["topology_template"]["node_templates"] = {}
    checkpoint["topology_template"]["node_templates"] = {}


    checkpoint["topology_template"]["node_templates"].update(dict_res)
    with open('checkPoint_'+str(var) +'.yaml','w') as yamlfile:
        yaml.dump(checkpoint, yamlfile)



    dict_res.update(tmp)
    cntnt["topology_template"]["node_templates"].update(dict_res)

    #Save the num to a json file.

    data['scale_index'] = var
    with open('data.json','w') as write_file:
        json.dump(data,write_file) 

    with open('service.yaml','w') as yamlfile:
        yaml.dump(cntnt, yamlfile)

    input_file.close()




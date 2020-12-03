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
import fileinput


if __name__ == "__main__":

#Normal things with Yaml 
    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False


#Get the scale index from data.json
    my_file = Path("data.json")

    if my_file.is_file():
        data_file = open('data.json','r+')
        data =json.load(data_file)
        if data['scale_index'] == 0:
            print("Nothing to downscale")
        else:
            var = data['scale_index']
    else:
        node_to_write = {
                'scale_index':0
                }
        with open('data.json','w') as write_file:
            json.dump(node_to_write,write_file)
        data = node_to_write
        var = data['scale_index']

#Remove the block of nodes_var from the template topology
#do this as early as possible. high priority

    toUndeployFile = open("checkPoint_" +str(var) + '.yaml','r')

    input_file  = 'service.yaml'
    cntnt = yaml.load(input_file)


    undeployList = []
    toUndeploy = yaml.load(toUndeployFile)
    for keys in  toUndeploy["topology_template"]["node_templates"].keys():
        undeployList.append(keys)

    for items in undeployList:
        if  items in cntnt["topology_template"]["node_templates"].keys():
            cntnt["topology_template"]["node_templates"].pop(items, None)

    with open('service_test_gen.yaml','w') as yamlfile:
        yaml.dump(cntnt, yamlfile)



#Redeploy  the  main service file
    os.system('opera deploy service.yaml')

#Change the .opera/root_file context to checkpoint_var
#And Remove the '\n' from the /.opera/root_file

    path = os.getcwd()
    with open(path +'/.opera/root_file','r') as file:
        filedata = file.read()

    replacement_text = "checkPoint_" +str(var) + ".yaml"

    filedata = filedata.replace(filedata, replacement_text)
    filedata.rstrip()

    with open(path +'/.opera/root_file', 'w') as file:
        file.write(filedata)


#remove references/relationships to missing node types
    toUndeployNodes = toUndeploy["topology_template"]["node_templates"]
    for nodes in toUndeployNodes.values():
        if 'requirements' in  nodes.keys():
            for requirement in nodes['requirements']:
                reqHosts = list(requirement.values())
                for reqHost in reqHosts:
                    if reqHost not in undeployList:
                        keyToDelete = list(requirement.keys())
                        nodes['requirements'].remove(requirement)

    with open("checkPoint_" +str(var) + ".yaml",'w') as yamlfile:
        yaml.dump(toUndeploy, yamlfile)




#Perform undeploy on the rootfile
    os.system('opera undeploy')

#Decrement the scale indx in data.json file
    data['scale_index'] -=1
    with open('data.json','w') as write_file:
        json.dump(data,write_file)







'''

    input_file  =  open(sys.argv[1],'r')

    req = sys.argv[2] + '_xx'

    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False
    cntnt = yaml.load(input_file)
#    checkpoint = 
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

    tmp = cntnt["topology_template"]["node_templates"]

    cntnt["topology_template"]["node_templates"] = {}
    dict_res.update(tmp)
    cntnt["topology_template"]["node_templates"].update(dict_res)

    #Save the num to a json file.

    data['scale_index'] = var
    with open('data.json','w') as write_file:
        json.dump(data,write_file) 
    with open('service_test_gen.yaml','w') as yamlfile:
        yaml.dump(cntnt, yamlfile)

    input_file.close()



'''

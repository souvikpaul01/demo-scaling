#pip install ruamel.yaml
import copy
import sys
from ruamel.yaml import YAML


def find(x):
    nodes = cntnt["topology_template"]["node_templates"]
    for node in nodes:
        u = node.split('_')
        if u[0] == x :
            break
   # print(u[0],node)
    return u[0], node

def change(c):
    name, name_i = find(c)
  #  print(name, name_i)
    if name == c and name_i[-2:] == 'xx' :
   #     print("okay",name_i)
        r = name_i.replace("xx","09")

        return r

def run(c):
    if c:
        update_dy(c)
        next_node = check_host(c)
        nodesToChange[c]= ''
        return run(next_node)
    else:
        for i in nodesToChange.keys():
            print(i)

        with open('exp.yaml','w') as yamlfile:
            yaml.dump(cntnt, yamlfile)

def update_dy(v):
    node_to_change = v.replace("xx","09")      #str(change(v))
    original_node = v 
    #node_to_change_next = check_host(original_node)
   # print(node_to_change_next)
    cntnt["topology_template"]["node_templates"][node_to_change] = copy.deepcopy( cntnt["topology_template"]["node_templates"][original_node])
    #del cntnt["topology_template"]["node_templates"][original_node]
    if 'requirements' in cntnt["topology_template"]["node_templates"][node_to_change].keys():   
        for i in cntnt["topology_template"]["node_templates"][node_to_change]['requirements']:
     #       print(i.keys())
            if 'host' in i.keys():
                i['host'] = i['host'].replace("xx",'09')

#        with open('exp.yaml','w') as yamlfile:
#            yaml.dump(cntnt, yamlfile)
    #original_node = original_node.replace("_xx",'')
    #print(original_node)
#        node_to_change_next = check_host(original_node)
#        return update_dy(node_to_change_next)
    

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
    cntnt =  yaml.load(input_file)

    nodesToChange = {}
    #findNodesToChange()
    
    run(req)
    #check_host(req)
    input_file.close()



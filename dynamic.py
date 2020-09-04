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
#    print(nodesToChange, c)
    if c:
        next_node = check_host(c)
        nodesToChange[c]= ''

   # print(nodesToChange, next_node)
        if next_node not in nodesToChange:
           run(next_node)
        findNodesToChange(c)

#       with open('exp.yaml','w') as yamlfile:
#          yaml.dump(cntnt, yamlfile)


def findNodesToChange(c):
      for node in cntnt["topology_template"]["node_templates"]:
        i = check_host(node)
        if i == c:
          if node not in nodesToChange:
            run(node)

#	    print(node,i)
#            if node not in nodesToChange.keys():
#                print("Need to deploy ", node)
                #update_dy(node)

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
    run(req) 
    for scalable_nodes in nodesToChange:
        update_dy(scalable_nodes)
    with open('exp.yaml','w') as yamlfile:
        yaml.dump(cntnt, yamlfile)

    input_file.close()


   

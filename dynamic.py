#pip install ruamel.yaml

import sys
from ruamel.yaml import YAML



def update_service(num,out):
    var = num
    new_yaml_data_dict = {
    'vm_'+var: {
    	'type' : 'my.nodes.VM.OpenStack',
        'properties': {
        	'name': 'nginxRadon_Host_'+var,
		'image': 'centos7',
		'flavor': 'm2.xsmall',
		'network': 'provider_64_net',
		'key_name': 'key_paul'


                    }           

            },

    
     'node_'+var: {
         'type': 'my.nodes.NodeExporter',
         'requirements':[{
             'host': 'vm_'+var
        }]
      },
    
    'nginx_'+var:{
      'type': 'my.nodes.Nginx',
      'requirements':[
          {
          'host': 'vm_'+var },
          {'connectToLB': 'nginx-lb'}
        ]
      },


    'site_'+var:{
      'type': 'my.nodes.Nginx.Site',
      'properties':{
            'hostname': 'site_'+var
            },
      'requirements':[
       
          {'host': 'nginx_'+var}
        ]
      }
      
      
    }
    

    for nodeName in list(cntnt["topology_template"]["node_templates"]):
        node = cntnt["topology_template"]["node_templates"]
        print(node)
        node.update(new_yaml_data_dict)
    if cntnt:
        with open(out,'w') as yamlfile:
            yaml.dump(cntnt, yamlfile)

def find(x):
    for nodeName in list(cntnt["topology_template"]["node_templates"]):
        nodes = cntnt["topology_template"]["node_templates"]
    for node in nodes:
        u = node.split('_')
        if u[0] == x :
            break
    return u[0], node

def change(c):
    name, name_i = find(c)
  #  print(name, name_i)
    if name == c and name_i[-2:] == 'xx' :
   #     print("okay",name_i)
        r = name_i.replace("xx","09")

        return r


def update_dy(v):
    node_to_change = str(change(v))
    
    node_to_change_next = check_host(v)
    print(node_to_change_next)
    cntnt["topology_template"]["node_templates"][node_to_change]=cntnt["topology_template"]["node_templates"]['node_xx']
    with open('exp.yaml','w') as yamlfile:
        yaml.dump(cntnt, yamlfile)
    
    return update_dy(node_to_change_next)


#############################################################

def check_host():
    nodes = cntnt["topology_template"]["node_templates"]
    print(nodes.values())
    for node in nodes.values():
        print(node)
        if 'requirements' in node.keys():
            for requirement in node['requirements']:
                if 'host' in requirement.keys():
                    host = requirement['host']
                 #   print(host)
                    return host
#############################################################





if __name__ == "__main__":
    input_file  =  open(sys.argv[1],'r')
    req = sys.argv[2]
    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False
    cntnt =  yaml.load(input_file)
    
    check_host()

    input_file.close()



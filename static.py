'''
##################################
    vm1:
      type: my.nodes.VM.OpenStack
      properties:
        name: nginxRadon_Host1
        image: centos7
        flavor: m1.xsmall
        network: provider_64_net
        key_name: key_khan

    node1:
      type: my.nodes.NodeExporter
      requirements:
        - host: vm1
##################################

'''
#pip install ruamel.yaml

import sys
from ruamel.yaml import YAML

#input_file=open('service.yaml', 'r')
#output_file=open('service.yaml', 'w')

def dump_yaml_file(cntnt, file_name):
    yaml_file = open(file_name, "w")
    yaml.dump(cntnt, yaml_file)
    yaml_file.close()

def getnum():
     
    return num


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
        #print(node)
        node.update(new_yaml_data_dict)
    if cntnt:
        with open(out,'w') as yamlfile:
            yaml.dump(cntnt, yamlfile)



if __name__ == "__main__":
#   print("python upscale.py <input_file> <output_file>")
    input_file  =  open(sys.argv[1],'r')
    out = sys.argv[2]
    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False
    #yaml.sort_keys = False
    cntnt =  yaml.load(input_file)
    #print(cntnt)
    #num = get_num()
    update_service('7',out)
    # put the vm number here
    input_file.close()



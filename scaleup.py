import sys
import os
#need to use the other python file was module library to this file
file_to_delete = "/home/ubuntu/opera/xopera-opera/examples/nginx_openstack/webApp-loadbalancer-node_exporter-TOSCA/demo-scaling/.opera/instances/nginx-lb_0"
try:
    os.remove(file_to_delete)
    os.system('python dynamic.py service_test_gen.yaml site')
#    sleep(10)
#    os.system('opera deploy service_test_gen.yaml')

#    os.system('opera deploy service_test.yaml')

    print ('File deleted')
except FileNotFoundError:
    print ('File not found:', file_to_delete)


#os.system('python upscale.py service.yaml service_test.yaml')

os.system('opera deploy service_test_gen.yaml')


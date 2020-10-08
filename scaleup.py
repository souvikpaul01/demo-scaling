import sys
import os

path = os.getcwd()
relativePathToFile = "/.opera/instances/nginx-lb_0"
file_to_delete = path + relativePathToFile


try:
    os.remove(file_to_delete)
    os.system('python dynamic.py service_test_gen.yaml site')

    print ('File deleted')
except FileNotFoundError:
    print ('File not found:', file_to_delete)

os.system('opera deploy service_test_gen.yaml')


import sys
import os

path = os.getcwd()
relativePathToFile = "/.opera/instances/nginx-lb_0"
file_to_delete = path + relativePathToFile

<<<<<<< HEAD

try:
    os.remove(file_to_delete)
    os.system('python dynamic.py service_test_gen.yaml site')
=======
try:
    os.remove(file_to_delete)
    os.system('python dynamic.py service.yaml site')
>>>>>>> upstream/master

    print ('File deleted')
except FileNotFoundError:
    print ('File not found:', file_to_delete)

<<<<<<< HEAD
os.system('opera deploy service_test_gen.yaml')
=======
os.system('opera deploy service.yaml')
>>>>>>> upstream/master


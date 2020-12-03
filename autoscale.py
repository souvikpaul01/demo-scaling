import sys
import os

path = os.getcwd()
relativePathToFile = "/.opera/instances/nginx-lb_0"
file_to_delete = path + relativePathToFile
toDo  =  int(sys.argv[1])
print(toDo)


try:
    os.remove(file_to_delete)
    print ('File deleted')

#Call UpScale and can be specified how many servers to upscale at one stage
    if toDo >=1:
        for i in range(0,toDo):
            os.system('python dynamic.py service.yaml site')
            os.system('opera deploy service.yaml')
#Call DOwnscale on one server only
    elif toDo <1:
            os.system('python downScale.py')

except FileNotFoundError:
    print ('File not found:', file_to_delete)




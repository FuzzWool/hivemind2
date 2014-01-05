#Grabbing a list of items in a directory, dropdown format.

import os
print os.getcwd()

def grab_list(directory):
	os.chdir(directory)
	l = []
	for files in os.listdir("."):
		if files.endswith(".png"):
			l.append(files)
		else:
			l.append([files]+grab_list(directory+"/"+files))
	return l

print grab_list(os.getcwd()+"/assets/tilesheets/")
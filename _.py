#Create a folder.

import os
mypath = os.getcwd()
if not os.path.isdir(mypath+"\maps"):
	os.makedirs(mypath+"\maps")
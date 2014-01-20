#Remove objects in a list.

lst = [True, True, False]

def false_list(arg):
	for l in arg:
		if l != True: yield l

print list(false_list(lst))
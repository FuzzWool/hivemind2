#Split a string every four characters.

t = ""
for i in range(5):
	t = t+(str(i)*4)

# >>> line = '1234567890'
# >>> n = 2
# >>> [line[i:i+n] for i in range(0, len(line), n)]

t = [t[i:i+4] for i in range(0, len(t), 4)]

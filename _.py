#Find the index of every space inside a sentence. (to find each word's gap)

def find(string, wanted_char):
	for i, char in enumerate(string):
		if char == wanted_char:
			yield i 

sentence = "Hello there, my name is Sam."
print list(find(sentence, " "))
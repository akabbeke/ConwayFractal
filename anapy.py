import sys

def allSame(items):
    return all(x == items[0] for x in items)

def main():
	hmap = {'e':2, 't':3, 'a':5, 'o':7, 'i':11, 'n':13, 's':17, 'h':19, 'r':23, 'd':29, 'l':31, 'c':37, 'u':41, 'm':43, 'w':47, 'f':53, 'g':59, 'y':61, 'p':67, 'b':71, 'v':73, 'k':79, 'j':83, 'x':89, 'q':97, 'z':101}
	shash = 0
	i = []
	for inputString in sys.stdin:
		for char in inputString:
			shash += hmap[char]
		i += [shash]
		shash = 0

	if allSame(i):
		print "ANAGRAM"
	else:
		print "NOT ANAGRAM"

if __name__ == "__main__":
    main()

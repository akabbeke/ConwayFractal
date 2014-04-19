import sys

def getCoords(inp):
	# sanitize and get input
	coords = []

	i = 0

	for line in inp:
		if i > 0:
			coords += [[float(line.split()[0]),float(line.split()[1])]]
		i += 1
	return coords

def getEqu(point1,point2):
	if point2[0] == point1[0]:
		return ['inf',str(point2[0])]
	else:
		m = (point2[1]-point1[1])/(point2[0]-point1[0])
		b = point1[1] - m*point1[0]
		print m
		print point2[1] - m*point2[0]
		print point1[1] - m*point1[0]
		print point1[1] - m*point1[0] - point2[1] + m*point2[0]
		a = str(point1[1] - m*point1[0])
		b = str(point2[1] - m*point2[0])
		print a == b
		print (point1[1] - m*point1[0]) == (point2[1] - m*point2[0])
		print point1,point2
		return [m,b]

def getLines(coords):
	# gets equations for all linies between points then hashes the quations into equDict
	# if a equation occurs 4 times there must be 4 points along the l

	equDict = dict()

	x=0

	y = 0

	for point1 in coords:
		for point2 in coords[x:]:
			if point1 != point2:

				ehash = str(getEqu(point1,point2))
				y += 1
				print y
				if ehash in equDict:
					equDict[ehash] += 1
				else:
					equDict[ehash] = 1

				if equDict[ehash] >= 4:
					return True


		x += 1
		

	return False

coords = getCoords(sys.stdin)

if getLines(coords):
	sys.stdout.write('YES')
else:
	sys.stdout.write('NO')



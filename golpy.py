
import numpy
import Image
import math
from scipy import signal
import matplotlib.pyplot as plt

def addToColorMap(loc,sub,cMap):
	cMap[loc[0]:loc[0]+sub.shape[0], loc[1]:loc[1]+sub.shape[1]] = sub
	return cMap

def findSubMarix(X,sub):

	a = numpy.copy(X)
	b = numpy.copy(sub)

	a[a==0] = -1
	b[b==0] = -1

	max_peak = numpy.prod(b.shape)
	c = signal.correlate(a,b, 'valid')
	return numpy.where(c == max_peak)

def colorMap(X,sub,cMap):

	cMap = colorMap2(X,sub,cMap)
	cMap = colorMap2(X,numpy.rot90(sub,1),cMap)
	cMap = colorMap2(X,numpy.rot90(sub,2),cMap)
	cMap = colorMap2(X,numpy.rot90(sub,3),cMap)
	return cMap

def colorMap2(X,sub,cMap):

	locs = findSubMarix(X,sub)

	for i in range(len(locs[0])):
		addToColorMap([locs[0][i],locs[1][i]],sub,cMap)

	return cMap


def lifeStep(X):

    # Game of life step using generator expressions

    X = numpy.asarray(X)
    assert X.ndim == 2
    X = X.astype(bool)

    nbrs_count = sum(numpy.roll(numpy.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    X = ((nbrs_count == 3) | (X == 1))&(nbrs_count != 8)

    return X

def tessellate(X,m,n):

	# Tesselates the field X into n*n subdevisions

	Xn = numpy.zeros([numpy.array(X.shape)[0]*m,numpy.array(X.shape)[1]*n])

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Xn[i*m:(i+1)*m,j*n:(j+1)*n] = X[i,j]*numpy.ones((m,n))
	return Xn

def tessellate2(X,m,n):

	Xn = numpy.zeros(numpy.array(X.shape)*3)

	inner = numpy.ones((m,n))
	inner[1,1] = 0

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Xn[i*3:(i+1)*3,j*3:(j+1)*3] = X[i,j]*inner
	return Xn

def tessellate3(X,m,n):

	# Tesselates the field X into n*n subdevisions

	Xn = numpy.zeros([numpy.array(X.shape)[0]*(m+1),numpy.array(X.shape)[1]*(n+1)])

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			outer = numpy.ones(((m+1),(n+1)))
			outer[0:m,0:n] = X[i,j]*numpy.ones((m,n))
			Xn[i*(m+1):(i+1)*(m+1),j*(n+1):(j+1)*(n+1)] = outer
	return Xn

def tessellate4(X,m,n):

	# Tesselates the field X into n*n subdevisions

	Xn = numpy.zeros([numpy.array(X.shape)[0]*(m+1),numpy.array(X.shape)[1]*(n+1)])

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			outer = numpy.zeros(((m+1),(n+1)))
			outer[0:m,0:n] = X[i,j]*numpy.ones((m,n))
			Xn[i*(m+1):(i+1)*(m+1),j*(n+1):(j+1)*(n+1)] = outer
	return Xn

def renderIm(Xi,q):
	img = Image.new( 'RGB', Xi.shape, "white")
	pixels = img.load()

	for i in range(img.size[1]):
		for j in range(img.size[0]):
			if Xi[i,j] == 1:
				pixels[j,i] = (0,0,0) # set the colour
	img.save(name+str(q)+'.gif')

def iterate(X,name,l,m,n):

	# Iterates the field l times
	# X = field
	# name = file name prefix
	# l = number of life cycles
	# m,n = x & y tessellation factors

	for q in range(l):


		for r in range(2):
			X = lifeStep(X)

		X = tessellate(X,m,n)

		print math.log(numpy.sum(X))/math.log(numpy.sum(n**(q+1)))

		Xi = tessellate(X,m**(l-1-q),n**(l-1-q))

		img = Image.new( 'RGBA', Xi.shape)
		pixels = img.load()

		for i in range(img.size[0]):
			for j in range(img.size[1]):
				if Xi[i,j] == 1:
					pixels[i,j] = (0,0,0) # set the colo

		img.save(name+str(q+1)+'.png')


def main():
	X = numpy.zeros((5,5))
	X[2,2] = 1
	# X = numpy.array([
	# 				[0,0,0,0,0,0,0],
	# 				[0,0,0,0,0,0,0],
	# 				[0,0,1,1,1,0,0],
	# 				[0,0,1,0,1,0,0],
	# 				[0,0,1,1,1,0,0],
	# 				[0,0,0,0,0,0,0],
	# 				[0,0,0,0,0,0,0]])

	iterate(X,'Renders/lobes',9,2,2)

if __name__ == "__main__":
    main()



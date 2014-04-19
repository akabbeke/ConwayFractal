
import numpy
import Image
import pp
import math
from scipy import signal

def addToColorMap(loc,sub,cMap,val):
	cMap[loc[0]:loc[0]+sub.shape[0], loc[1]:loc[1]+sub.shape[1]] = sub*val
	return cMap

def findSubMarix(X,sub):

	a = numpy.copy(X)
	b = numpy.copy(sub)

	a[a==0] = -1
	b[b==0] = -1

	max_peak = numpy.prod(b.shape)

	c = signal.correlate(a,b, 'valid')

	return numpy.where(c == max_peak)

def colorMap(X,sub,val,cMap):

	cMap = colorMap2(X,sub,val,cMap)
	cMap = colorMap2(X,numpy.rot90(sub,1),val,cMap)
	cMap = colorMap2(X,numpy.rot90(sub,2),val,cMap)
	cMap = colorMap2(X,numpy.rot90(sub,3),val,cMap)
	return cMap

def colorMap2(X,sub,val,cMap):

	locs = findSubMarix(X,sub)

	for i in range(len(locs[0])):
		addToColorMap([locs[0][i],locs[1][i]],sub,cMap,val)

	return cMap


def lifeStep(X,m):

    # Game of life step using generator expressions

    X = numpy.asarray(X)
    assert X.ndim == 2
    X = X.astype(bool)

    nbrs_count = sum(numpy.roll(numpy.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    X = (nbrs_count == 3) | (X & (nbrs_count == 2))

    return tessellate(X,m)

def tessellate(X,n):

	# Tesselates the field X into n*n subdevisions

	Xn = numpy.zeros(numpy.array(X.shape)*n)

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Xn[i*n:(i+1)*n,j*n:(j+1)*n] = X[i,j]*numpy.ones((n,n))
	return Xn

def sliceX(X,m):

	# Slices the X into smaller chunks to be worked on by each core

	return(numpy.delete(numpy.delete(X,range(X.shape[1]/2+1,X.shape[1]-1),axis=1),range(X.shape[0]/2+1,X.shape[0]-1),axis=0),
			numpy.delete(numpy.delete(X,range(1,X.shape[1]/2-1),axis=1),range(X.shape[0]/2+1,X.shape[0]-1),axis=0),
			numpy.delete(numpy.delete(X,range(X.shape[1]/2+1,X.shape[1]-1),axis=1),range(1,X.shape[0]/2-1),axis=0),
			numpy.delete(numpy.delete(X,range(1,X.shape[1]/2-1),axis=1),range(1,X.shape[0]/2-1),axis=0))

def renderIm(Xi,q):
	img = Image.new( 'RGB', Xi.shape, "white")
	pixels = img.load()

	for i in range(img.size[1]):
		for j in range(img.size[0]):
			if Xi[i,j] == 1:
				pixels[j,i] = (0,0,0) # set the colour
	print X.sum()
	img.save(name+str(q)+'.gif')

def iterate(X,name,n,m):

	# Iterates the field n times
	# X = field
	# name = file name Prefix
	# n = number of life cycles
	# m = tessellation factor

	ppservers = ()

	# Creates jobserver with automatically detected number of workers

	jobServer = pp.Server(ppservers=ppservers)


	for q in range(n):

		arrayList = sliceX(X,m)
		jobs = [jobServer.submit(lifeStep, (part,m), (tessellate,), ("numpy",))() for part in arrayList]

		X = numpy.vstack([numpy.hstack([jobs[0][:jobs[0].shape[0]-(2*m),:jobs[0].shape[1]-(2*m)],
		 								jobs[1][:jobs[1].shape[0]-(2*m),(2*m):]]),
		 				  numpy.hstack([jobs[2][(2*m):,:jobs[3].shape[1]-(2*m)],
		 								jobs[3][(2*m):,(2*m):]])])
		cMap = numpy.zeros(X.shape)
		cMap2 = numpy.zeros(X.shape)
		sub = numpy.array([[0,0,0,0],
						   [0,1,1,0],
						   [1,0,0,1],
						   [0,0,0,0]])

		sub2= numpy.array([[0,0,0,0,0,0],
						   [0,0,1,1,0,0],
						   [0,1,0,0,1,0],
						   [0,1,0,0,1,0],
						   [0,0,1,1,0,0],
						   [0,0,0,0,0,0]])

		sub = tessellate(sub,2)

		sub2 = tessellate(sub2,2)
		
		cMap = colorMap(X,sub,1,numpy.copy(cMap))
		cMap2 = colorMap2(X,sub2,1,numpy.copy(cMap2))
		if n-(q+1) == 0: 
			Xi = X
		else:
			Xi = tessellate(X,m**(n-(q+1)))
			cMap2 = tessellate(cMap2,m**(n-(q+1)))
			cMap = tessellate(cMap,m**(n-(q+1)))

		#jobServer.print_stats()
		
		img = Image.new( 'RGB', Xi.shape, "white")
		pixels = img.load()

		for i in range(img.size[1]):
			for j in range(img.size[0]):
				if Xi[i,j] == 1:
					pixels[j,i] = (0,0,0) # set the colour
				if cMap[i,j]!= 0:
					pixels[j,i] = (255,0,0)
				if cMap2[i,j]!= 0:
					pixels[j,i] = (0,255,0)

		print math.log(X.sum())/math.log(X.shape[0])
		img.save(name+str(q)+'.gif')

def main():

	X = numpy.array([
					[0,0,0,0,0,0],
					[0,0,1,1,0,0],
					[0,1,0,0,1,0],
					[0,1,0,0,1,0],
					[0,0,1,1,0,0],
					[0,0,0,0,0,0]])

	iterate(X,'Renders/testicals',9,2)

if __name__ == "__main__":
    main()



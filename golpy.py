
import numpy
import Image
import pp

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
	if n-(q+1) == 0: 
		Xi = X
	else:
		Xi = tessellate(X,m**(n-(q+1)))

	jobServer.print_stats()
	
	img = Image.new( 'RGB', Xi.shape, "black")
	pixels = img.load()

	for i in range(img.size[0]):
		for j in range(img.size[1]):
			if Xi[i,j] == 1:
				pixels[i,j] = ((i*255)/img.size[0],(j*255)/img.size[1],100) # set the colour

	img.save(name+str(q)+'.png')

def main():

	X = numpy.array([[1,0,0,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0,0,0,0,1]])
	iterate(X,'Renders/Ctest2',10,2)

if __name__ == "__main__":
    main()



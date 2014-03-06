
import numpy
import Image
import pp

def lifeStep(X):

    # Game of life step using generator expressions
    X = numpy.asarray(X)
    assert X.ndim == 2
    X = X.astype(bool)

    nbrs_count = sum(numpy.roll(numpy.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    X = (nbrs_count == 3) | (X & (nbrs_count == 2))
    return tessellate(X,2)

def tessellate(X,n):

	# Tesselates the field into n*n subdevisions

	Xn = numpy.zeros(numpy.array(X.shape)*n)

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Xn[i*n:(i+1)*n,j*n:(j+1)*n] = X[i,j]*numpy.ones((n,n))
	return Xn

def sliceX(X):

	# Slices the X into smaller chunks

	return(numpy.delete(numpy.delete(X,range(X.shape[1]/2+1,X.shape[1]-1),axis=1),range(X.shape[0]/2+1,X.shape[0]-1),axis=0),
			numpy.delete(numpy.delete(X,range(1,X.shape[1]/2-1),axis=1),range(X.shape[0]/2+1,X.shape[0]-1),axis=0),
			numpy.delete(numpy.delete(X,range(X.shape[1]/2+1,X.shape[1]-1),axis=1),range(1,X.shape[0]/2-1),axis=0),
			numpy.delete(numpy.delete(X,range(1,X.shape[1]/2-1),axis=1),range(1,X.shape[0]/2-1),axis=0))

def iterate(X,name,n):

	# Iterates the field n times

	ppservers = ()

	# Creates jobserver with automatically detected number of workers
	job_server = pp.Server(ppservers=ppservers)


	for q in range(n):

		arrayList = sliceX(X)

		jobs = [(job_server.submit(lifeStep, (part,), (tessellate,), ("numpy",))) for part in arrayList]

		wat = [job() for job in jobs]

		X = numpy.vstack([numpy.hstack([wat[0][:wat[0].shape[0]-4,:wat[0].shape[1]-4],
										wat[1][:wat[1].shape[0]-4,4:]]),
						  numpy.hstack([wat[2][4:,:wat[3].shape[1]-4],
										wat[3][4:,4:]])])
		print X
		job_server.print_stats()
		
		img = Image.new( 'RGB', X.shape, "white")
		pixels = img.load()

		for i in range(img.size[0]):
			for j in range(img.size[1]):
				if X[i,j] == 1:
					pixels[i,j] = (0,0,0) # set the colour

		img.save(name+str(q)+'.png')

def main():
	X= numpy.array([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]])
	iterate(X,'Renders/2x2-',11)

if __name__ == "__main__":
    main()



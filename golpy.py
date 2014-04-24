
import numpy
import Image

def lifeStep(X):

    # Game of life step using generator expressions

    X = numpy.asarray(X)
    assert X.ndim == 2
    X = X.astype(bool)

    # Rolls the matrix to find neighbours of each cell
    nbrs_count = sum(numpy.roll(numpy.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))

    # Defines the rules of Conways Game of Life in Boolian logic.
    X = ((nbrs_count == 2) & X) | (nbrs_count == 3)

    return X

def tessellate(X,m,n):

	# Tesselates the field X into n*m subdevisions

	Xn = numpy.zeros([numpy.array(X.shape)[0]*m,numpy.array(X.shape)[1]*n])

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Xn[i*m:(i+1)*m,j*n:(j+1)*n] = X[i,j]*numpy.ones((m,n))
	return Xn

def generateFractal(X,name,l,m,n,c):

	# Iterates the field l times
	# X = field
	# name = file name prefix
	# l = number of life cycles
	# m,n = x & y tessellation factors
	# c = number of iterations of Conway rules

	for q in range(c):

		for i in range(1):
			# plays the game of life
			X = lifeStep(X)

		# Scale up image to size of final step
		Xi = tessellate(X,m**(l-1-q),n**(l-1-q))

		# Creates a blank image the size of the final step
		img = Image.new( 'RGBA', Xi.shape)
		pixels = img.load()

		# Color the pixels.
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				if Xi[i,j] == 1:
					pixels[i,j] = (0,0,0)

		# Save the image
		img.save(name+str(q+1)+'.png')

		#Teselate the field, doesn't need to do this on last step.
		if q != (l-1):
			X = tessellate(X,m,n)

		

def main():
	
	# Specify an inital Conditon X

	X = numpy.array([
					[0,0,0,0],
					[0,1,1,0],
					[0,1,1,0],
					[0,0,0,0]])

	generateFractal(X,'Renders/bgs',9,2,2,1)

if __name__ == "__main__":
    main()



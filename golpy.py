
import numpy as np
import Image
import threading
import time

def lifeStep(X):

    ## Game of life step using generator expressions
    X = np.asarray(X)
    assert X.ndim == 2
    X = X.astype(bool)

    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (X & (nbrs_count == 2))

def tessellate(X,n):

	## Tesselates the field into n*n subdevisions

	Xn = np.zeros(np.array(X.shape)*n)

	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Xn[i*n:(i+1)*n,j*n:(j+1)*n] = X[i,j]*np.ones((n,n))
	return Xn

def iterate(X,name,n):
	# Iterates the field n times
	for q in range(n):
		start = time.time()
		for h in range(2):
			X=lifeStep(X)
		X=tessellate(X,2)
		
		img = Image.new( 'RGB', X.shape, "white")
		pixels = img.load()

		for i in range(img.size[0]):
			for j in range(img.size[1]):
				if X[i,j] == 1:
					pixels[i,j] = (int((i*255)/img.size[0]), int((j*255)/img.size[1]), 100) # set the colour accordingly

		img.save(name+str(q)+'.png')
		print time.time()-start
		print np.sum(X)

X = np.array([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]])
# a = np.random.random(())


# b = np.zeros((a.shape[0]+2,a.shape[1]+2))

#X = np.zeros((6, 9), dtype=bool)
#r = np.random.random((4, 7))
#X[1:5, 1:8] = (r > 0.75)
#a[2:5,4] = np.array([[1,1,1]])
iterate(X,'Renders/beacon',10)


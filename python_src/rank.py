#import numpy
from math import sqrt

#def myrank(A, eps=1e-12):
#	u, s, vh = numpy.linalg.svd(A)
#	return len([x for x in s if abs(x) > eps])
def RankMat(A):
	m = len(A)
	n = len(A[0])
	# Computation of a numerical rank of a given m-by-n matrix with m >=n */
	# written  Oct. 13, 2013  T. Ogita */
	# revised  Oct. 14, 2013  T. Ogita */
	
	R = [None]*(n*m)

	if (m>=n):
		for j in range(n):
			for i in range(m):
				R[i+j*m] = A[i][j]
		mR = m
		nR = n
	else:
		for j in range(n):
			for i in range(m):
				R[j+i*n] = A[i][j]
		mR = n
		nR = m

	R = QlessQR(mR,nR,R)

	# Frobenius norm
	s = 0.0
	for i in range(m*n):
		s += R[i]*R[i]
	s = sqrt(s)
	tol = 1e-15*s

	r = 0

	for i in range(nR):
		if(abs(R[i+i*mR])>tol):
			r += 1
	return r

def QlessQR(m,n,A):
	v = [None]*m
	w = [None]*n

	for k in range(n):
		# Householder vector [v,beta] = house(A(k:m,k))
		for i in range(k,m):
			v[i] = A[i+k*m]
		s = 0.0
		for i in range(k+1,m):
			s += v[i]*v[i]
		if (s == 0.0):
			beta = 0.0
		else:
			t = v[k]
			mu = sqrt(t*t + s)
			if (t <= 0.0):
				v[k] = t - mu
			else:
				v[k] = -s/(t + mu)
			t = v[k]*v[k]
			beta = 2.0*t/(s+t)
			for i in range(k+1,m):
				v[i] /= v[k]
			v[k] = 1.0

		# Update
		# w = v'*A(j:m,j:n)
		for j in range(k,n):
			s = 0.0
			for i in range(k,m):
				s += v[i]*A[i+j*m]
			w[j] = s
		for i in range(k,m):
			v[i] *= beta
		for j in range(k,n):
			for i in range(k,m):
				A[i+j*m] -= v[i]*w[j]
	return A


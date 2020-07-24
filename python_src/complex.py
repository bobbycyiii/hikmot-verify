# The following is not necessary in Python 3.
# from __future__ import division

class complex(object):

	inner_types = (float, int)

	def __init__(self, *args):
		if len(args) == 0:
			self.real = None
			self.imag = None
		elif len(args) == 1:
			self.real = args[0]
			self.imag = 0
		elif len(args) == 2:
			self.real = args[0]
			self.imag = args[1]
		else:
			raise TypeError
	def __str__(self):
		return "(" + str(self.real) + ")+(" + str(self.imag) + ")i"

	def __repr__(self):
		return "(" + repr(self.real) + ")+(" + repr(self.imag) + ")i"

	def __add__(self, x):
		if isinstance(x, complex):
			r = complex()
			r.real = self.real + x.real
			r.imag = self.imag + x.imag
		elif isinstance(x, complex.inner_types):
			r = complex()
			r.real = self.real + x
			r.imag = self.imag
		else:
			return NotImplemented
		return r

	def __radd__(self, x):
		if isinstance(x, complex.inner_types):
			r = complex()
			r.real = x + self.real
			r.imag = self.imag
		else:
			return NotImplemented
		return r

	def __sub__(self, x):
		if isinstance(x, complex):
			r = complex()
			r.real = self.real - x.real
			r.imag = self.imag - x.imag
		elif isinstance(x, complex.inner_types):
			r = complex()
			r.real = self.real - x
			r.imag = self.imag
		else:
			return NotImplemented
		return r

	def __rsub__(self, x):
		if isinstance(x, complex.inner_types):
			r = complex()
			r.real = x - self.real
			r.imag = - self.imag
		else:
			return NotImplemented
		return r

	def __neg__(self):
		r = complex()
		r.real = - self.real
		r.imag = - self.imag
		return r

	def __mul__(self, x):
		if isinstance(x, complex):
			r = complex()
			r.real = self.real * x.real - self.imag * x.imag
			r.imag = self.real * x.imag + self.imag * x.real
		elif isinstance(x, complex.inner_types):
			r = complex()
			r.real = self.real * x
			r.imag = self.imag * x
		else:
			return NotImplemented
		return r

	def __rmul__(self, x):
		if isinstance(x, complex.inner_types):
			r = complex()
			r.real = x * self.real
			r.imag = x * self.imag
		else:
			return NotImplemented
		return r

	def __div__(self, x):
		if isinstance(x, complex):
			r = complex()
			tmp = x.real * x.real + x.imag * x.imag
			r.real = (x.real * self.real + x.imag * self.imag) / tmp
			r.imag = (x.real * self.imag - self.real * x.imag) / tmp
		elif isinstance(x, complex.inner_types):
			r = complex()
			r.real = self.real / x 
			r.imag = self.imag / x
		else:
			return NotImplemented
		return r

	def __rdiv__(self, x):
		if isinstance(x, complex.inner_types):
			r = complex()
			tmp = self.real * self.real + self.imag * self.imag
			r.real = (self.real * x) / tmp
			r.imag = (- x * self.imag) / tmp
		else:
			return NotImplemented
		return r

	__truediv__ = __div__
	__rtruediv__ = __rdiv__

	@staticmethod
	def add_type(x):
		tmp = set(complex.inner_types)
		tmp.add(x)
		complex.inner_types = tuple(tmp)

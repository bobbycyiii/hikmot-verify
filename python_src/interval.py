# The following is not necessary in Python 3.
# from __future__ import division
import math
from . import ftostr

class interval(object):

	# __slots__ = ["inf", "sup"]

	inner_types = (float, int)

	def __init__(self, *args):
		if len(args) == 0:
			self.inf = None
			self.sup = None
		elif len(args) == 1:
			self.inf = args[0]
			self.sup = args[0]
			# interval.inner_types.add(type(args[0]))
		elif len(args) == 2:
			self.inf = args[0]
			self.sup = args[1]
			# interval.inner_types.add(type(args[0]))
			# interval.inner_types.add(type(args[1]))
		else :
			raise TypeError

	def __str__(self):
		return "[" + ftostr.ftostr(self.inf, precision=12, form="g", mode=-1) + "," + ftostr.ftostr(self.sup, precision=12, form="g", mode=1) + "]"

	def __repr__(self):
		return "[" + ftostr.ftostr(self.inf, precision=17, form="g", mode=-1) + "," + ftostr.ftostr(self.sup, precision=17, form="g", mode=1) + "]"

	def __add__(self, x):
		if isinstance(x, interval):
			r = interval()
			r.inf = interval.pred(self.inf + x.inf)
			r.sup = interval.succ(self.sup + x.sup)
		elif isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(self.inf + x)
			r.sup = interval.succ(self.sup + x)
		else:
			return NotImplemented
		return r

	def __radd__(self, x):
		if isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(x + self.inf)
			r.sup = interval.succ(x + self.sup)
		else:
			return NotImplemented
		return r

	def __sub__(self, x):
		if isinstance(x, interval):
			r = interval()
			r.inf = interval.pred(self.inf - x.sup)
			r.sup = interval.succ(self.sup - x.inf)
		elif isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(self.inf - x)
			r.sup = interval.succ(self.sup - x)
		else:
			return NotImplemented
		return r

	def __rsub__(self, x):
		if isinstance(x, interval.inner_types):
			r = interval()
			r.inf = interval.pred(x - self.sup)
			r.sup = interval.succ(x - self.inf)
		else:
			return NotImplemented
		return r

	def __neg__(self):
		r = interval()
		r.inf = - self.sup
		r.sup = - self.inf
		return r

	def __mul__(self, x):
		if isinstance(x, interval):
			r = interval()
			tmp = (self.inf * x.inf, self.inf * x.sup, self.sup * x.inf, self.sup * x.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		elif isinstance(x, interval.inner_types):
			r = interval()
			tmp = (self.inf * x, self.sup * x)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r

	def __rmul__(self, x):
		if isinstance(x, interval.inner_types):
			r = interval()
			tmp = (x * self.inf, x * self.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r

	def __div__(self, x):
		if isinstance(x, interval):
			if x.inf <= 0 and x.sup >= 0:
				raise ZeroDivisionError("division by interval which contains 0")
			r = interval()
			tmp = (self.inf / x.inf, self.inf / x.sup, self.sup / x.inf, self.sup / x.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		elif isinstance(x, interval.inner_types):
			r = interval()
			tmp = (self.inf / x, self.sup / x)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r

	def __rdiv__(self, x):
		if isinstance(x, interval.inner_types):
			if self.inf <= 0 and self.sup >= 0:
				raise ZeroDivisionError("division by interval which contains 0")
			r = interval()
			tmp = (x / self.inf, x / self.sup)
			r.inf = interval.pred(min(tmp))
			r.sup = interval.succ(max(tmp))
		else:
			return NotImplemented
		return r

	__truediv__ = __div__
	__rtruediv__ = __rdiv__

	def __abs__(self) :
		if self.inf < 0 :
			if self.sup < 0 : 
				return -self
			else :
				return interval(0, max(-self.inf, self.sup))
		else :
			return self

	def __pow__(self, x):
		if isinstance(x, interval):
			return (x * self.log()).exp()
		elif isinstance(x, interval.inner_types):
			if isinstance(x, int) or (isinstance(x, float) and x == math.floor(x)):
				a = abs(x)
				r = interval(1)
				xp = self
				tmp = a
				while tmp != 0:
					if tmp % 2 != 0:
						r *= xp
					tmp //= 2
					xp = xp * xp
				if a % 2 == 0 and r.inf < 0:
					r.inf = 0
				if x < 0:
					r = 1. / r
				return r
			else:
				return (x * self.log()).exp()
		else:
			return NotImplemented

	def __rpow__(self, x):
		if isinstance(x, interval.inner_types):
			return (self * interval(x).log()).exp()
		else:
			return NotImplemented

	def sqrt(self):
		if self.inf < 0:
			raise ValueError("sqrt of negative interval")
		r = interval()
		r.inf = interval.pred(math.sqrt(self.inf))
		r.sup = interval.succ(math.sqrt(self.sup))
		r.inf = max(r.inf, 0)
		return r

	@staticmethod
	def exp_point(x):
		e12 = interval(7425180500362907. / 4503599627370496., 7425180500362908. / 4503599627370496.)
		em12 = interval(5463142506141193. / 9007199254740992., 5463142506141194. / 9007199254740992.)

		if x >= 0:
			x_i = math.floor(x)
			x_f = x - x_i
			if x_f >= 0.5:
				x_f -= 1
				x_i += 1
		else:
			x_i = -math.floor(-x)
			x_f = x - x_i
			if x_f <= -0.5:
				x_f += 1
				x_i -= 1
		r = interval(1)
		y = interval(1)
		for i in range(1, 16):
			y *= x_f
			y /= i
			if i == 15:
				r += y * interval(em12.inf, e12.sup)
			else:
				r += y
		if x_i >= 0:
			r *= interval.e()**x_i
		else:
			r /= interval.e()**(-x_i)
		return r

	def exp(self):
		return interval(interval.exp_point(self.inf).inf, interval.exp_point(self.sup).sup)

	def expm1(self) :
		def expm1_origin(x) :
			e12 = interval(7425180500362907. / 4503599627370496., 7425180500362908. / 4503599627370496.)
			em12 = interval(5463142506141193. / 9007199254740992., 5463142506141194. / 9007199254740992.)

			r = interval(0)
			y = interval(1)
			for i in range(1, 16):
				y *= x
				y /= i
				if i == 15:
					r += y * interval(em12.inf, e12.sup)
				else:
					r += y
			return r
		def expm1_point(x) :
			if x >= -0.5 and x <= 0.5 :
				return expm1_origin(x)
			else:
				return interval.exp_point(x) - 1

		return interval(expm1_point(self.inf).inf, expm1_point(self.sup).sup)

	@staticmethod
	def log_point(x):
		ln2 = interval(6243314768165359. / 9007199254740992., 6243314768165360. / 9007199254740992.)
		sqrt2 = interval(6369051672525772. / 4503599627370496., 6369051672525773. / 4503599627370496.)

		p = math.floor(math.log(x) / math.log(2) + 0.5)
		if p >= 0:
			x2 = interval(x / 2**p)
		else:
			x2 = interval(x * 2**(-p))

		while x2.inf > 4 * math.sqrt(2) - 4:
			x2 = interval(x.inf * 0.5, x.sup * 0.5)
			p += 1
		while x2.inf > 4 - 2 * math.sqrt(2):
			x2 /= sqrt2
			p += 0.5
		while x2.sup < 2 - math.sqrt(2):
			x2 = interval(x.inf * 2, x.sup * 2)
			p -= 1
		while x2.sup < 2 * math.sqrt(2) - 2:
			x2 *= sqrt2
			p -= 0.5

		x2m1 = interval(x2.inf - 1, x2.sup - 1)
		cinv = 1 / interval.hull(x2, 1)
		r = interval(0)
		xn = interval(-1)
		xn2 = interval(-1)
		for i in range(1, 23):
			xn = -xn * x2m1
			xn2 = -xn * cinv * x2m1
			if i == 22 :
				r += xn2 / i
			else:
				r += xn / i
		r += ln2 * p
		return r

	def log(self):
		return interval(interval.log_point(self.inf).inf, interval.log_point(self.sup).sup)

	def log1p(self):
		def log1p_origin(x):
			cinv = 1 / interval.hull(x + 1, 1)
			r = interval(0)
			xn = interval(-1)
			xn2 = interval(-1)
			for i in range(1, 23):
				xn = -xn * x
				xn2 = -xn * cinv * x
				if i == 22 :
					r += xn2 / i
				else:
					r += xn / i
			return r
		def log1p_point_down(x) :
			if x >= -(3-2*math.sqrt(2)) and x <= 3 - 2*math.sqrt(2):
				return log1p_origin(x)
			else:
				return interval.log_point((x + interval(1)).inf)
		def log1p_point_up(x) :
			if x >= -(3-2*math.sqrt(2)) and x <= 3 - 2*math.sqrt(2):
				return log1p_origin(x)
			else:
				return interval.log_point((x + interval(1)).sup)
		return interval(log1p_point_down(self.inf).inf, log1p_point_up(self.sup).sup)

	@staticmethod
	def sin_origin(x):
		r = interval(0)
		y = interval(1)
		for i in range(1, 18):
			y *= x
			y /= i
			if i == 17:
				r += y * interval(-1, 1)
			else:
				if i % 2 != 0:
					if i % 4 == 1:
						r += y
					else:
						r -= y
		return r
	@staticmethod
	def cos_origin(x):
		r = interval(1)
		y = interval(1)
		for i in range(1, 18):
			y *= x
			y /= i
			if i == 17:
				r += y * interval(-1, 1)
			else:
				if i % 2 == 0:
					if i % 4 == 0:
						r += y
					else:
						r -= y
		return r

	@staticmethod
	def sin_point(x):
		pi21 = interval(7074237752028440. / 1125899906842624., 7074237752028441. / 1125899906842624.)
		pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)

		if not isinstance(x, interval) :
			x = interval(x)
		if x.inf >= math.pi :
			return sin_point(x - pi21)
		if x.sup <= -math.pi * 3 / 4 :
			return -interval.sin_origin(x + interval.pi())
		if x.sup <= -math.pi / 2 :
			return -interval.cos_origin(-pi12 - x)
		if x.sup <= -math.pi / 4 :
			return -interval.cos_origin(x + pi12)
		if x.sup <= 0 : 
			return -interval.sin_origin(-x)
		if x.sup <= math.pi / 4 : 
			return interval.sin_origin(x)
		if x.sup <= math.pi / 2 : 
			return interval.cos_origin(pi12 - x)
		if x.sup <= math.pi * 3 / 4 : 
			return interval.cos_origin(x - pi12)
		return interval.sin_origin(interval.pi() - x)

	@staticmethod
	def cos_point(x):
		pi21 = interval(7074237752028440. / 1125899906842624., 7074237752028441. / 1125899906842624.)
		pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)

		if not isinstance(x, interval) :
			x = interval(x)
		if x.inf >= math.pi :
			return cos_point(x - pi21)
		if x.sup <= -math.pi * 3 / 4 :
			return -interval.cos_origin(x + interval.pi())
		if x.sup <= -math.pi / 2 :
			return -interval.sin_origin(-pi12 - x)
		if x.sup <= -math.pi / 4 :
			return interval.sin_origin(x + pi12)
		if x.sup <= 0 : 
			return interval.cos_origin(-x)
		if x.sup <= math.pi / 4 : 
			return interval.cos_origin(x)
		if x.sup <= math.pi / 2 : 
			return interval.sin_origin(pi12 - x)
		if x.sup <= math.pi * 3 / 4 : 
			return -interval.sin_origin(x - pi12)
		return -interval.cos_origin(interval.pi() - x)

	def sin(self):
		pi21 = interval(7074237752028440. / 1125899906842624., 7074237752028441. / 1125899906842624.)
		pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)
		pi32 = interval(5305678314021330. / 1125899906842624., 5305678314021331. / 1125899906842624.)
		pi52 = interval(8842797190035550. / 1125899906842624., 8842797190035551. / 1125899906842624.)

		x = self
		while x.inf <= -interval.pi().sup or x.inf >= interval.pi().sup:
			n = math.floor(x.inf / pi21.inf + 0.5)
			x -= n * pi21

		if (interval(x.sup) - x.inf).inf >= pi21.sup :
			return interval(-1, 1)

		r = interval.hull(interval.sin_point(x.inf), interval.sin_point(x.sup))

		if interval.subset(pi12, x) :
			r = interval.hull(r, 1)
		if interval.subset(pi52, x) :
			r = interval.hull(r, 1)
		if interval.subset(-pi12, x) :
			r = interval.hull(r, -1)
		if interval.subset(pi32, x) :
			r = interval.hull(r, -1)

		return interval.intersect(r, interval(-1, 1))
					
	def cos(self):
		pi21 = interval(7074237752028440. / 1125899906842624., 7074237752028441. / 1125899906842624.)
		pi31 = interval(5305678314021330. / 562949953421312., 5305678314021331. / 562949953421312.)

		x = self
		while x.inf <= -interval.pi().sup or x.inf >= interval.pi().sup:
			n = math.floor(x.inf / pi21.inf + 0.5)
			x -= n * pi21

		if (interval(x.sup) - x.inf).inf >= pi21.sup :
			return interval(-1, 1)

		r = interval.hull(interval.cos_point(x.inf), interval.cos_point(x.sup))

		if interval.subset(0, x) :
			r = interval.hull(r, 1)
		if interval.subset(pi21, x) :
			r = interval.hull(r, 1)
		if interval.subset(-interval.pi(), x) :
			r = interval.hull(r, -1)
		if interval.subset(interval.pi(), x) :
			r = interval.hull(r, -1)
		if interval.subset(pi31, x) :
			r = interval.hull(r, -1)

		return interval.intersect(r, interval(-1, 1))

	def tan(self):
		def tan_point(x):
			return interval.sin_point(x) / interval.cos_point(x)

		pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)

		x = self
		while x.inf <= -pi12.sup or x.inf >= pi12.sup:
			n = math.floor(x.inf / interval.pi().inf + 0.5)
			x -= n * interval.pi()

		if x.sup >= pi12.sup:
			return interval(-float("inf"), float("inf"))

		return interval(tan_point(self.inf).inf, tan_point(self.sup).sup)

	@staticmethod
	def atan_origin(x):
		r = interval(0)
		y = interval(1)
		for i in range(1, 39) :
			y *= x
			if i == 38 :
				r += y * interval(-1, 1) / i
			else :
				if i % 2 != 0 :
					if i % 4 == 1 :
						r += y / i
					else :
						r -= y / i
		return r

	def atan(self):
		def atan_point(x):
			pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)
			pi14 = interval(7074237752028440. / 9007199254740992., 7074237752028441. / 9007199254740992.)

			if x < -(math.sqrt(2) + 1) :
				return -pi12 - interval.atan_origin(1 / interval(x))
			if x < -(math.sqrt(2) - 1) :
				return -pi14 + interval.atan_origin((1 + interval(x)) / (1 - interval(x)))
			if x < math.sqrt(2) - 1 :
				return interval.atan_origin(interval(x))
			if x < math.sqrt(2) + 1 :
				return pi14 + interval.atan_origin((interval(x) - 1) / (interval(x) + 1))
			return pi12 - interval.atan_origin(1 / interval(x))

		return interval(atan_point(self.inf).inf, atan_point(self.sup).sup)

	def asin(self):
		def asin_point(x):
			pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)

			if x == 1:
				return pi12
			if x == -1:
				return -pi12
			if math.fabs(x) < math.sqrt(6) / 3 :
				return (x / (1 - interval(x) * x).sqrt()).atan()
			else:
				if x > 0 :
					return (x / ((1 + interval(x)) * (1 - x)).sqrt()).atan()
				else:
					return (x / ((1 + x) * (1 - interval(x))).sqrt()).atan()
		
		return interval(asin_point(self.inf).inf, asin_point(self.sup).sup)

	def acos(self):
		def pi12_m_atan_point(x):
			pi34 = interval(5305678314021330. / 2251799813685248., 5305678314021331. / 2251799813685248.)
			pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)
			pi14 = interval(7074237752028440. / 9007199254740992., 7074237752028441. / 9007199254740992.)
			if (not isinstance(x, interval)):
				x = interval(x)

			if x.inf < -(math.sqrt(2) + 1) :
				return interval.pi() + interval.atan_origin(1 / x)
			if x.inf < -(math.sqrt(2) - 1) :
				return pi34 - interval.atan_origin((1 + x) / (1 - x))
			if x.inf < math.sqrt(2) - 1 :
				return pi12 - interval.atan_origin(x)
			if x.inf < math.sqrt(2) + 1 :
				return pi14 - interval.atan_origin((x - 1) / (x + 1))
			return interval.atan_origin(1 / x)
		def acos_point(x):
			if x == 1:
				return interval(0)
			if x == -1:
				return interval.pi()
			if math.fabs(x) < math.sqrt(6) / 3 :
				return pi12_m_atan_point(x / (1 - interval(x) * x).sqrt())
			else:
				if x > 0 :
					return pi12_m_atan_point(x / ((1 + interval(x)) * (1 - x)).sqrt())
				else:
					return pi12_m_atan_point(x / ((1 + x) * (1 - interval(x))).sqrt())
		return interval(acos_point(self.sup).inf, acos_point(self.inf).sup)

	@staticmethod
	def atan2(y, x):
		def atan2_point(y, x):
			pi12 = interval(7074237752028440. / 4503599627370496., 7074237752028441. / 4503599627370496.)
			ix = interval(x)
			iy = interval(y)

			if y <= x and y > -x :
				return (iy / ix).atan()
			if y > x and y > -x :
				return pi12 - (ix / iy).atan()
			if y > x and y <= -x :
				if y >= 0:
					return interval.pi() + (iy / ix).atan()
				else:
					return -interval.pi() + (iy / ix).atan()
			return -pi12 - (ix / iy).atan()

		pi21 = interval(7074237752028440. / 1125899906842624., 7074237752028441. / 1125899906842624.)
		if not isinstance(x, interval) :
			x = interval(x)
		if not isinstance(y, interval) :
			y = interval(y)
			
		if interval.subset(0, x) :
			if interval.subset(0, y) :
				return interval(-interval.pi().sup, interval.pi().sup)
			else:
				if y.inf > 0 :
					return interval(atan2_point(y.inf, x.sup).inf, atan2_point(y.inf, x.inf).sup)
				else:
					return interval(atan2_point(y.sup, x.inf).inf, atan2_point(y.sup, x.sup).sup)
		else :
			if interval.subset(0, y) :
				if x.inf > 0 :
					return interval(atan2_point(y.inf, x.inf).inf, atan2_point(y.sup, x.inf).sup)
				else:
					return interval(atan2_point(y.sup, x.sup).inf, pi21 + atan2_point(y.inf, x.sup).sup)
			else :
				if x.inf > 0 :
					if y.inf > 0 :
						return interval(atan2_point(y.inf, x.sup).inf, atan2_point(y.sup, x.inf).sup)
					else:
						return interval(atan2_point(y.inf, x.inf).inf, atan2_point(y.sup, x.sup).sup)
				else:
					if y.inf > 0 :
						return interval(atan2_point(y.sup, x.sup).inf, atan2_point(y.inf, x.inf).sup)
					else:
						return interval(atan2_point(y.sup, x.inf).inf, atan2_point(y.inf, x.sup).sup)

	@staticmethod
	def sinh_point(x):
		def sinh_origin(x):
			cosh12 = interval(5078375876716752. / 4503599627370496., 5078375876716753. / 4503599627370496.)
			r = interval(0)
			y = interval(1)
			for i in range(1, 16) :
				y *= x
				y /= i
				if i == 15 :
					r += y * interval(-cosh12.sup, cosh12.sup)
				else:
					if i % 2 != 0:
						r += y
			return r

		if x >= -0.5 and x <= 0.5 :
			return sinh_origin(x)
		else:
			tmp = interval.exp_point(x)
			return (tmp - 1/tmp) * 0.5

	def sinh(self):
		return interval(interval.sinh_point(self.inf).inf, interval.sinh_point(self.sup).sup)

	@staticmethod
	def cosh_point(x):
		tmp = interval.exp_point(x)
		return (tmp + 1/tmp) * 0.5

	def cosh(self):
		r = interval.hull(interval.cosh_point(self.inf), interval.cosh_point(self.sup))
		if interval.subset(0, self) :
			r = interval.hull(r, 1)
		return r

	def tanh(self):
		def tanh_point(x):
			return interval.sinh_point(x) / interval.cosh_point(x)
		return interval(tanh_point(self.inf).inf, tanh_point(self.sup).sup)

	def asinh(self) :
		def asinh_point(x) :
			if x < -0.5 :
				return -(-x +(1 + interval(x) * x).sqrt()).log()
			elif x <= 0.5 :
				return ((1 + x / (1 + (1 + interval(x) * x).sqrt())) * x).log1p()
			else:
				return (x +(1 + interval(x) * x).sqrt()).log()
		return interval(asinh_point(self.inf).inf, asinh_point(self.sup).sup)

	def acosh(self) :
		def acosh_point(x) :
			if x == 1 :
				return interval(0)
			elif x <= 1.5 :
				y = interval(x - 1)
				return (y + (y * (interval(x) + 1)).sqrt()).log1p()
			else :
				return (x + (interval(x) * x - 1).sqrt()).log()
		return interval(acosh_point(self.inf).inf, acosh_point(self.sup).sup)

	def atanh(self) :
		def atanh_point(x) :
			if x < -0.5 :
				return 0.5 * ((1 + x) / (1 - interval(x))).log()
			elif x <= 0.5 :
				return 0.5 * (2 * x / (1 - interval(x))).log1p()
			else:
				return 0.5 * ((1 + interval(x)) / (1 - x)).log()
		return interval(atanh_point(self.inf).inf, atanh_point(self.sup).sup)

	@staticmethod
	def e():
		return interval(6121026514868073. / 2251799813685248., 6121026514868074. / 2251799813685248.)

	@staticmethod
	def pi():
		return interval(7074237752028440. / 2251799813685248., 7074237752028441. / 2251799813685248.)

	@staticmethod
	def subset(x, y):
		if isinstance(y, interval):
			if (isinstance(x, interval)):
				return x.inf >= y.inf and x.sup <= y.sup
			else:
				return x >=  y.inf and x <= y.sup
		else:
			raise ValueError

	@staticmethod
	def overlap(x, y):
		if isinstance(x, interval):
			rinf = x.inf
			rsup = x.sup
		else:
			rinf = x
			rsup = x
		if isinstance(y, interval):
			rinf = max(rinf, y.inf)
			rsup = min(rsup, y.sup)
		else:
			rinf = max(rinf, y)
			rsup = min(rsup, y)

		return rinf <= rsup

	@staticmethod
	def intersect(x, y):
		if isinstance(x, interval):
			rinf = x.inf
			rsup = x.sup
		else:
			rinf = x
			rsup = x
		if isinstance(y, interval):
			rinf = max(rinf, y.inf)
			rsup = min(rsup, y.sup)
		else:
			rinf = max(rinf, y)
			rsup = min(rsup, y)

		if rinf <= rsup:
			return interval(rinf, rsup)
		else:
			return None

	@staticmethod
	def hull(x, y):
		if isinstance(x, interval):
			rinf = x.inf
			rsup = x.sup
		else:
			rinf = x
			rsup = x
		if isinstance(y, interval):
			rinf = min(rinf, y.inf)
			rsup = max(rsup, y.sup)
		else:
			rinf = min(rinf, y)
			rsup = max(rsup, y)
		return interval(rinf, rsup)

	@staticmethod
	def mag(x):
		if not isinstance(x, interval):
			return abs(x)
		return max(abs(x.inf), abs(x.sup))

	@staticmethod
	def norm(x):
		return abs(x)

	@staticmethod
	def mig(x):
		if not isinstance(x, interval):
			return abs(x)
		else:
			if x.inf <=0 and x.sup >=0:
				return 0
			else:
				return min(abs(x.inf), abs(x.sup))

	@staticmethod
	def mid(x):
		if isinstance(x, interval):
			return (x.inf + x.sup) / 2
		else:
			return x

	@staticmethod
	def width(x):
		if isinstance(x, interval):
			return interval.succ(x.sup - x.inf)
		else:
			return 0
	@staticmethod
	def rad(x):
		if isinstance(x, interval):
			# is it correct?
			return interval.succ((x.sup - x.inf) / 2)
		else:
			return 0

	"""
	@staticmethod
	def abssucc(x):
		return x / (1 - 2**(-53))

	@staticmethod
	def abspred(x):
		return x * (1 - 2**(-53))

	@staticmethod
	def succ(x):
		if abs(x) < 2**(-1022):
			return x + 2**(-1074)
		if x > 0:
			return interval.abssucc(x)
		else:
			return interval.abspred(x)

	@staticmethod
	def pred(x):
		if abs(x) < 2**(-1022):
			return x - 2**(-1074)
		if x > 0:
			return interval.abspred(x)
		else:
			return interval.abssucc(x)
	"""

	@staticmethod
	def succ(x):
		a = abs(x)
		if a > 2.**(-1020):
			return x + a * (2.**(-53)+2.**(-55))
		if x >= -2.**(-1021) and x < 2.**(-1021):
			return x + 2.**(-1074)
		if x < 0. or x < 2.**(-1020):
			return x + 2.**(-1073)
		else:
			return x + 2.**(-1072)

	@staticmethod
	def pred(x):
		a = abs(x)
		if a > 2.**(-1020):
			return x - a * (2.**(-53)+2.**(-55))
		if x > -2.**(-1021) and x <= 2.**(-1021):
			return x - 2.**(-1074)
		if x > 0. or x > -2.**(-1020):
			return x - 2.**(-1073)
		else:
			return x - 2.**(-1072)

	@staticmethod
	def add_type(x):
		tmp = set(interval.inner_types)
		tmp.add(x)
		interval.inner_types = tuple(tmp)


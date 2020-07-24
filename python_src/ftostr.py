#
# Copyright (c) 2013 Masahide Kashiwagi (kashi@waseda.jp)
#
# ftostr(x, precision, form, mode)
#   convert double number x to string
#    mode == -1 : down
#    mode ==  0 : nearest
#    mode ==  1 : up
#    form == "e" : like %e of printf
#    form == "f" : like %f of printf
#    form == "g" : like %g of printf
#    form == "a" : print all digits with no rounding
#

import math

def getsign(x):
	s = math.copysign(1., x)
	if s > 0:
		return 1
	else:
		return -1
	

def getexponent(x):
	if x >= 2.**1023 :
		return 1023

	# special case for 0
	if x < 2.**(-1074) :
		return -1075

	return math.frexp(x)[1] - 1


def ftostr(x, precision=17, form="g", mode=0):

	if x != x :
		return "nan"

	sign = getsign(x)
	absx = math.fabs(x)

	if absx == 0 :
		if sign == -1 :
			return "-0"
		else :
			return "0"

	if absx == float("inf") :
		if sign == -1 :
			return "-inf"
		else :
			return "inf"

	ex = getexponent(absx)

	buf = {}
	tmp = absx
	tmp2 = 2.**ex
	for i in range(0, 53) :
		if tmp >= tmp2 :
			buf[ex-i] = 1
			tmp = tmp - tmp2
		else :
			buf[ex-i] = 0
		if tmp == 0 :
			emax = ex
			emin = ex-i
			break
		tmp2 = tmp2 / 2

	# print(emax)
	# print(emin)

	if emin > 0 :
		for i in range(0, emin) :
			buf[i] = 0
		emin = 0

	if emax < 0 :
		for i in range(emax+1, 1) :
			buf[i] = 0
		emax = 0 

	result = {}
	result_max = -1

	while emax >= 0 :
		if emax >= 17 :
			m = 5
		elif emax >= 14 :
			m = 4
		elif emax >= 10 :
			m = 3
		elif emax >= 7 :
			m = 2
		else :
			m = 1
		pm = 10**m

		carry = 0
		for i in range(emax, -1, -1) :
			tmp = carry * 2 + buf[i]
			buf[i] = tmp // pm
			carry = tmp % pm

		for i in range(1, m+1) :
			result_max = result_max + 1
			result[result_max] = carry % 10
			carry = carry // 10

		while emax >= 0 and buf[emax] == 0 :
			emax = emax - 1

	result_min = 0

	while emin < 0 :
		m = min(8, -emin)
		pm = 10**m

		carry = 0
		for i in range(emin, 0) :
			tmp = buf[i] * pm + carry
			buf[i] = tmp % 2
			carry = tmp // 2

		for i in range(1, m+1) :
			result_min = result_min - 1
			pm = pm / 10
			result[result_min] = carry // pm
			carry = carry % pm

		while emin < 0 and buf[emin] == 0 :
			emin = emin + 1

	if sign == 1 :
		result_str = ""
	else :
		result_str = "-"

	if form == "f" :

		if -(precision+1)>=result_min :
			result_min = -precision
			tmp = result[result_min-1]
			if   (mode == 1 and sign == 1) \
			  or (mode == -1 and sign == -1) \
			  or (mode == 0 and tmp >= 5) :
				# result[result_min-1] = 0
				result[result_max+1] = 0
				result_max = result_max+1
				for i in range(result_min, result_max+1) :
					result[i] = result[i] + 1
					if result[i] != 10 :
						break
					result[i] = 0
				if result[result_max] == 0 :
					result_max = result_max-1

		while result_min < 0 and result[result_min] == 0 :
			result_min = result_min + 1
		
		for i in range(result_max, result_min-1, -1) :
			if i == -1 :
				result_str = result_str + "."
			result_str = result_str + str(result[i])

	elif form == "e" :

		while result[result_max] == 0 :
			result_max = result_max - 1

		if result_max-precision-1 >= result_min :
			result_min = result_max - precision
			tmp = result[result_min-1]
			if   (mode == 1 and sign == 1) \
			  or (mode == -1 and sign == -1) \
			  or (mode == 0 and tmp >= 5) :
				# result[result_min-1] = 0
				result[result_max+1] = 0
				result_max = result_max+1
				for i in range(result_min, result_max+1) :
					result[i] = result[i] + 1
					if result[i] != 10 :
						break
					result[i] = 0
				if result[result_max] == 0 :
					result_max = result_max-1
				else :
					result_min = result_min+1

		while result[result_min] == 0 :
			result_min = result_min + 1

		for i in range(result_max, result_min-1, -1) :
			if i == result_max - 1 :
				result_str = result_str + "."
			result_str = result_str +  str(result[i])
		# result_str = string.format("%se%02d", result_str, result_max)
		result_str = result_str +  "e" + str(result_max)

	elif form == "g" :

		while result[result_max] == 0 :
			result_max = result_max - 1

		if result_max-precision >= result_min :
			result_min = result_max - precision + 1
			tmp = result[result_min-1]
			if   (mode == 1 and sign == 1) \
			  or (mode == -1 and sign == -1) \
			  or (mode == 0 and tmp >= 5) :
				# result[result_min-1] = 0
				result[result_max+1] = 0
				result_max = result_max+1
				for i in range(result_min, result_max+1) :
					result[i] = result[i] + 1
					if result[i] != 10:
						break
					result[i] = 0
				if result[result_max] == 0 :
					result_max = result_max-1
				else :
					result_min = result_min+1

		if -4 <= result_max and result_max <= precision -1 :
			while result_min < 0 and result[result_min] == 0 :
				result_min = result_min + 1
			if result_max < 0 :
				result_max = 0
			for i in range(result_max, result_min-1, -1) :
				if i == -1 :
					result_str = result_str + "."
				result_str = result_str + str(result[i])
		else :
			while result[result_min] == 0 :
				result_min = result_min + 1
			for i in range(result_max, result_min-1, -1) :
				if i == result_max - 1 :
					result_str = result_str + "."
				result_str = result_str + str(result[i])
			# result_str = string.format("%se%02d", result_str, result_max)
			result_str = result_str + "e" + str(result_max)

	elif form == "a" :

		for i in range(result_max, result_min-1, -1) :
			if i == -1 :
				result_str = result_str + "."
			result_str = result_str + str(result[i])

	return result_str

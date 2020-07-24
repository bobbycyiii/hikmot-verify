# This file contains some functions that use the manifold class.

from math import sqrt, pi
from cmath import log

# A dictionary gives a number for each degeneracy level of solution

degeneracy_level = {'all tetrahedra positively oriented': 0,
'contains negatively oriented tetrahedra': 1,
'contains flat tetrahedra': 2,
'contains degenerate tetrahedra': 3,
'unrecognized solution type': 4,
'no solution found': 5,
'not attempted': 6}

# Returns the minimum imaginary part of all tetrahedra shapes

def min_imaginary_shapes(M):
	imaginary_shapes = []
	for i in M.tetrahedra_shapes(part = 'rect'):
		imaginary_shapes.append(i.imag)
	return min(imaginary_shapes)

# Checks that the solution is positive
# Here M.solution_type == 'all tetrahedra positively oriented' is not enough,
# we require that the imaginary part of every tetrahedron shape 
# is bigger than the constant 'min_imaginary'

def positive_solution(M, min_imaginary):
	return min_imaginary_shapes(M) > min_imaginary

# Tries to hyperbolize the manifold M. 
# It returns a copy of M whose solution has the least degree of degeneracy 
# among those investigated.

def try_to_hyperbolize(M, number_of_randomizes, try_permanent_fillings, min_imaginary):
	answer = M.copy()

	# The best solution is 'all tetrahedra positively oriented' 
	# AND positive solution == True, which checks that imaginary parts are big enough  
	# If the algorithm finds such a best solution, it stops and returns it.

	if degeneracy_level[answer.solution_type()] == 0 and positive_solution(answer, min_imaginary):
		return answer

	Mcopy = answer.copy()

	# Try to randomize the triangulation 'number_of_randomizes' times.

	for tentative in range(number_of_randomizes):
		Mcopy.randomize()
		if degeneracy_level[Mcopy.solution_type()] == 0 and positive_solution(Mcopy, min_imaginary):
			return Mcopy
		if degeneracy_level[Mcopy.solution_type()] < degeneracy_level[answer.solution_type()]:
			answer = Mcopy.copy()

	# Try to permanently fill some cusps (if try_permanent_fillings == True):

	if try_permanent_fillings == True: 
		num_cusps = M.num_cusps() 
		if num_cusps >= 2:		
			for i in range(num_cusps):
				if M.cusp_info('complete?')[i] == False:
					Mfilled = M.filled_triangulation([i])		
					another_answer = try_to_hyperbolize(Mfilled, number_of_randomizes, try_permanent_fillings, min_imaginary)
					if degeneracy_level[another_answer.solution_type()] == 0 and positive_solution(another_answer, min_imaginary):
						return another_answer	
					if degeneracy_level[another_answer.solution_type()] < degeneracy_level[answer.solution_type()]:
						answer = another_answer.copy()
	return answer

# Prints the numerical solution and the gluing equations matrix in order
# to be read by Moser's code
"""
def print_for_Moser(M, Moser_data):
	shapes = M.tetrahedra_shapes(part = 'rect')
	shapes_string = '['
	for shape in shapes:
		shapes_string = shapes_string + str(shape.real) + ' + ' + str(shape.imag) + '*I, '
	shapes_string = shapes_string[:-2] + ']'

	# Prints the shapes

	#Moser_data.append(shapes_string)
	Moser_data.write(shapes_string + '\n')
	n = M.num_tetrahedra()
	num_cusps = M.num_cusps()
	equations = M.gluing_equations(form = 'rect')
	equations_string = '['

	# There are n variables. The equations are:
	# * 1 for each edge (so n in total)
	# * 2 for each complete cusp
	# * 1 for each filled cusp
	# On a complete cusp Snappy produces 2 equations, on a filled cusp only 1.
	# We must print only one equation for each cusp.
	# If the cusp is complete, we thus need to ignore the second equation. 
	# We store in 'ignore' the positions of the equations that must be ignored.

	ignore = []
	counter = n
	for i in range(num_cusps):
		if M.cusp_info('complete?')[i] == True:
			ignore.append(counter + 1)
			counter = counter + 1
		counter = counter + 1
	counter = 0
	num_equations_check = 0
	for row in equations:
		if ignore.count(counter) == 0:
			num_equations_check = num_equations_check + 1

			# Put all integers on a single row:

			new_row = []
			for i in row[:-1]:
				new_row.extend(i)

			# Find experimentally the correct multiple of pi*i:

			result = 0
			for i in range(n):
				result = result + row[0][i] * log(shapes[i]) + row[1][i] * log(1-shapes[i])
			num_multiples = - int(round(result.imag / pi, 0))
			new_row.append(num_multiples)

			# Write this newly formatted row:

			for i in new_row:
				equations_string = equations_string + str(i) + ', '
			equations_string = equations_string[:-2] + '; '
		counter = counter + 1
	equations_string = equations_string[:-2] + ']'

	# Prints the equations

	#Moser_data.append(equations_string)#
	Moser_data.write(equations_string + '\n')

	# A sanity check

	if num_equations_check != n + num_cusps:
		print 'There is a problem in printing the algorithm for Moser'
"""

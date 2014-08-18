
MAX_ITERATIONS = 100
ERROR_MARGIN = 1.0E-15

def marginalize(data, marginal_totals):
	for iteration in range(MAX_ITERATIONS):
		worst_error = 0

		for dimension in marginal_totals:

			for value, marginal_total in dimension.items():

				# Find all the cells that belong to this dimension-value
				cells = {key: cell for key, cell in data.items() if value in key}

				value_total = sum(cells.values())
				error = marginal_total - value_total
				worst_error = max(worst_error, error)

				updated_cells = {key: (cell / value_total) * marginal_total for key, cell in cells.items()}
				data.update(updated_cells)

		if worst_error <= ERROR_MARGIN:
			print "Converged after {} iterations".format(iteration)
			return

	print "Did not converge after {} iterations".format(MAX_ITERATIONS)

def threeDimensionalExample():
	marginal_totals = (
		{
			'NSW': 200.0,
			'VIC': 125.0,
			'QLD': 75.0
		},
		{
			'Male': 150.0,
			'Female': 250.0
		},
		{
			'iOS': 300,
			'Andriod': 100
		}
	)

	data = {
		('NSW', 'Male', 'iOS'):   1.0,
		('NSW', 'Female', 'iOS'): 1.0,
		('VIC', 'Male', 'iOS'):   1.0,
		('VIC', 'Female', 'iOS'): 1.0,
		('QLD', 'Male', 'iOS'):   1.0,
		('QLD', 'Female', 'iOS'): 1.0,

		('NSW', 'Male', 'Andriod'):   50.0,
		('NSW', 'Female', 'Andriod'): 45.0,
		('VIC', 'Male', 'Andriod'):   60.0,
		('VIC', 'Female', 'Andriod'): 80.0,
		('QLD', 'Male', 'Andriod'):   82.0,
		('QLD', 'Female', 'Andriod'): 83.0,
	}

	marginalize(data, marginal_totals)

	print_data(data)


def twoDimensionalExample():
	marginal_totals = (
		{
			'NSW': 200.0,
			'VIC': 125.0,
			'QLD': 75.0
		},
		{
			'Male': 150.0,
			'Female': 250.0
		}
	)

	data = {
		('NSW', 'Male'):   50.0,
		('NSW', 'Female'): 45.0,
		('VIC', 'Male'):   60.0,
		('VIC', 'Female'): 80.0,
		('QLD', 'Male'):   82.0,
		('QLD', 'Female'): 83.0,
	}

	marginalize(data, marginal_totals)

	print_data(data)


def print_data(data):
	print "AFTER"
	for key in sorted(data.keys()):
		print ','.join(key) + ',' + str(data[key])

if __name__ == '__main__':
	threeDimensionalExample()

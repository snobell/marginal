import random


def merge_sort(l):

	if len(l) > 1:
		mid = len(l) // 2

		left = merge_sort(l[:mid])
		right = merge_sort(l[mid:])

		return merge(left, right)

	return l


def merge(left, right):
	merged = []

	left_index = 0
	right_index = 0

	while left_index < len(left) and right_index < len(right):
		if left[left_index] <= right[right_index]:
			merged.append(left[left_index])
			left_index += 1
		else:
			merged.append(right[right_index])
			right_index += 1

	while left_index < len(left):
		merged.append(left[left_index])
		left_index += 1

	while right_index < len(right):
		merged.append(right[right_index])
		right_index += 1

	return merged


def insertion_sort(l):
	for i in range(len(l)):
		for j in range(i, len(l)):
			if l[j] < l[i]:
				l[i], l[j] = l[j], l[i]


def main():

	l = [random.randint(0, 100) for x in range(50)]

	print l
	insertion_sort(l)
	print l

	for x in xrange(10000):
		l = [random.randint(0, 100) for x in range(10)]
		sl = merge_sort(l)

		assert sorted(l) == sl


if __name__ == '__main__':
	main()
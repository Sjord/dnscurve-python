
def divide(a, c, p):
	"""
	Extended Euclid's Algorithm
	return b == a/c mod p
	"""
	one = (p, 0) # p * b = 0
	two = (c % p, a % p) # a * b = c
	while two[0] != 0:
		(quotient, remainder) = divmod(one[0], two[0])
		newone = two
		# Subtract two as often as possible from one
		two = (remainder, (one[1] - quotient * two[1]) % p)
		one = newone
	b = one[1];
	assert (b * c) % p == a % p
	return b
		

def gcd(a, b):
	"""Euclid's algorithm"""
	while b != 0:
		(a, b) = (b, a % b)
	return a


if __name__ == "__main__":
	assert gcd(9, 6) == 3
	assert gcd(23, 101) == 1
	print divide(7, 10, 23)

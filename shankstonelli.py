
def shanks_tonelli(n, p):
	""" x^2 = n (mod p)
	returns x
	"""

	assert p % 2 != 0 and p % 3 != 0 # p is prime

	s = 0
	q = p - 1
	while q % 2 == 0:
		q /= 2
		s += 1
	assert q * pow(2, s) == p - 1
	
	w = 2
	while legendre_symbol(w, p) != -1:
		w += 1

	r = pow(n, (q + 1) / 2, p)
	v = pow(w, q, p)

	while True:
		i = find_lowest_i(n, q, p)
		assert 0 <= i
		assert i <= s - 1
		assert pow(pow(pow(r, 2) / n, 2), i, p) == 1
		if i == 0:
			return (r, p - r)
		r = (r * pow(v, pow(2, s - i -1), p)) % p

def find_lowest_i(n, q, p):
	# Wikipedia says to start with R^2n^-1, but this is the same as n^Q
	start = pow(n, q, p)
	i = 0
	while True:
		if start == 1:
			return i
		start = pow(start, 2, p)
		i += 1
	
def legendre_symbol(a, p):
	ls = pow(a, (p-1)/2, p)
	if ls == p-1:
		return -1
	else:
		return ls

if __name__ == "__main__":
	assert 4 in shanks_tonelli(2, 7)
	assert 5 in shanks_tonelli(3, 11)
	assert 3 in shanks_tonelli(9, 19)


def shanks_tonelli(n, p):
	""" x^2 = n (mod p)
	returns x
	"""
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
		i = find_lowest_i(r, n, p)
		assert i <= s - 1
		assert 0 <= i
		assert pow(pow(r, 2) / n, 2 * i, p) == 1
		if i == 0:
			return r
		r = (r * pow(v, pow(2, s - i -1), p)) % p

def find_lowest_i(r, n, p):
	i = pow(r, 2) / n
	while True:
		result = pow(i, 2, p)
		if result == 1:
			return i
		i = result
	
def legendre_symbol(a, p):
	ls = pow(a, (p-1)/2, p)
	if ls == p-1:
		return -1
	else:
		return ls

if __name__ == "__main__":
	assert 3 == shanks_tonelli(1, 8) # 3^2 = 9 = 1 mod 8
	assert 4 == shanks_tonelli(2, 7)
	assert 5 == shanks_tonelli(4, 6)

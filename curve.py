from shanks_tonelli import shanks_tonelli

def add(p, q):
	(xp, yp) = p
	(xq, yq) = q
	s = (yp - yq) / (xp - xq)
	xr = pow(s, 2) - xp - xq
	yr = s * (xp - xr) - yp
	return (xr, yr)

def double(p, a):
	(xp, yp) = p
	s = (3 * pow(xp, 2) + a) / (2 * yp)
	xr = pow(s, 2) - 2 * xp
	yr = s * (xp - xr) - yp
	return (xr, yr)

class curve:
	def __init__(self, a, p):
		"""y ** 2 = x ** 3 + a * x ** 2 + x mod p"""
		self.a = a
		self.p = p
	def ysquare(self, x):
		return (pow(x, 3, self.p) + self.a * pow(x, 2, self.p) + x) % self.p
	def ys(self, x):
		ysquare = self.ysquare(x)
		ys = shanks_tonelli(ysquare, self.p)
		return ys
	def points(self, x):
		ys = self.ys(x)
		assert len(ys) == 2
		return ((x, ys[0]), (x, ys[1]))
		

if __name__ == "__main__":
	curve25519 = curve(486662, pow(2, 255) - 19)
	points = curve25519.points(9)
	p0 = points[0]
	a = 486662
	twice = double(p0, a)
	four0 = double(twice, a)
	three = add(twice, p0)
	four1 = add(three, p0)
	assert four0[0] == four1[0]



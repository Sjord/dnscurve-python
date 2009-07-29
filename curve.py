from shanks_tonelli import shanks_tonelli

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
	def double(self, p):
		(xp, yp) = p
		s = (3 * pow(xp, 2) + self.a) / (2 * yp)
		xr = (pow(s, 2, self.p) - 2 * xp) % self.p
		yr = (s * (xp - xr) - yp) % self.p
		return (xr, yr)
	def add(self, p, q):
		(xp, yp) = p
		(xq, yq) = q
		s = (yp - yq) / (xp - xq)
		xr = (pow(s, 2, self.p) - xp - xq) % self.p
		yr = (s * (xp - xr) - yp) % self.p
		return (xr, yr)

if __name__ == "__main__":
	simple = curve(0, 23)
	(p0, p1) = simple.points(1)
	print p1
	print simple.double(p1)
else:
	curve25519 = curve(486662, pow(2, 255) - 19)
	points = curve25519.points(9)
	p0 = points[0]
	a = 486662
	twice = double(p0, a)
	four0 = double(twice, a)
	three = add(twice, p0)
	four1 = add(three, p0)
	assert four0[0] == four1[0]



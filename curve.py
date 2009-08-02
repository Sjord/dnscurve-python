from shanks_tonelli import shanks_tonelli
from divide import divide

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
		s = divide(3 * pow(xp, 2) + self.a, 2 * yp, self.p)
		xr = (pow(s, 2, self.p) - 2 * xp) % self.p
		yr = (s * (xp - xr) - yp) % self.p
		return (xr, yr)
	def add(self, p, q):
		(xp, yp) = p
		(xq, yq) = q
		s = divide(yp - yq, xp - xq, self.p)
		xr = (pow(s, 2, self.p) - xp - xq) % self.p
		yr = (s * (xp - xr) - yp) % self.p
		return (xr, yr)

if __name__ == "__main__":
	simple = curve(0, 23)
	(p0, p1) = simple.points(1)
	twice = simple.double(p1)
	four0 = simple.double(twice)
	three = simple.add(twice, p1)
	four1 = simple.add(three, p1)
	assert four0 == four1

	curve25519 = curve(486662, pow(2, 255) - 19)
	points = curve25519.points(9)
	p0 = points[0]
	a = 486662
	twice = curve25519.double(p0)
	four0 = curve25519.double(twice)
	three = curve25519.add(twice, p0)
	four1 = curve25519.add(three, p0)
	assert four0 == four1


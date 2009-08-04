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
		if p == 0: return q
		if q == 0: return p
		if p == q: return self.double(p)
		(xp, yp) = p
		(xq, yq) = q
		s = divide(yp - yq, xp - xq, self.p)
		xr = (pow(s, 2, self.p) - xp - xq) % self.p
		yr = (s * (xp - xr) - yp) % self.p
		return (xr, yr)
	def multiply(self, p, n):
		q = p
		r = 0
		while n > 0:
			if n & 1:
				r = self.add(r, q)
			q = self.double(q)
			n /= 2
		return r

if __name__ == "__main__":
	def testcurve(curve, (p0, p1)):
		assert p1 == curve.add(0, p1)
		assert p1 == curve.add(p1, 0)
		assert curve.add(p1, p1) == curve.double(p1)
		p1x2 = curve.double(p1)
		p1x3 = curve.add(p1x2, p1)
		p1x4 = curve.double(p1x2)
		assert p1x4 == curve.add(p1x3, p1)
		assert p1x4 == curve.multiply(p1, 4)
		assert p1x4 == curve.add(curve.multiply(p1, 3), p1)
		# X of both points stays the same under multiplication - Theorem 2.1
		assert curve.double(p0)[0] == curve.double(p1)[0]

	simple = curve(0, 23)
	testcurve(simple, simple.points(1))

	curve25519 = curve(486662, pow(2, 255) - 19)
	testcurve(curve25519, curve25519.points(9))



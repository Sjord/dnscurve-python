# coding: utf8
from shanks_tonelli import shanks_tonelli
from divide import divide

class curve:
	def __init__(self, a, p):
		"""y ** 2 = x ** 3 + a * x ** 2 + x mod p"""
		assert a ** 2 - 4 != 0
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
		# l, slope of the line
		l = divide(3 * pow(xp, 2) + 2 * self.a * xp + 1, 2 * yp, self.p)
		xr = (pow(l, 2, self.p) - self.a - xp - xp) % self.p
		yr = ((2*xp+xp+self.a)*l - pow(l, 3, self.p) - yp) % self.p
		return (xr, yr)

	def add(self, p, q):
		if p == 0: return q
		if q == 0: return p
		if p == q: return self.double(p)
		(xp, yp) = p
		(xq, yq) = q

		# line y=lx+m through p and q
		l = divide(yq - yp, xq - xp, self.p)
		m = yp - l*xp

		xr = (pow(l, 2, self.p) - self.a - xp - xq) % self.p
		yr = -(l * xr + m) % self.p
		return xr, yr

	def multiply(self, p, n):
		q = p
		r = 0
		while n > 0:
			if n & 1:
				r = self.add(r, q)
			q = self.double(q)
			n /= 2
		return r

	def is_on_curve(self, p):
		xp, yp = p
		y2_through_x = self.ysquare(xp)
		y2_through_y = pow(yp, 2, self.p)
		return y2_through_x == y2_through_y
	def __str__(self):
		return """y² = x³ + %dx² + x mod %d""" % (self.a, self.p)



if __name__ == "__main__":
	def testcurve(curve, (p0, p1)):
		assert curve.is_on_curve(p0)
		assert curve.is_on_curve(p1)

		assert p1 == curve.add(0, p1)
		assert p1 == curve.add(p1, 0)
		assert curve.add(p1, p1) == curve.double(p1)

		p1x2 = curve.double(p1)
		assert curve.is_on_curve(p1x2)
		
		p1x3 = curve.add(p1x2, p1)
		assert curve.is_on_curve(p1x3)

		p1x4 = curve.double(p1x2)
		assert curve.is_on_curve(p1x4)

		assert p1x4 == curve.add(p1x3, p1)
		assert p1x4 == curve.multiply(p1, 4)
		assert p1x4 == curve.add(curve.multiply(p1, 3), p1)
		# X of both points stays the same under multiplication - Theorem 2.1
		assert curve.double(p0)[0] == curve.double(p1)[0]

	# simple = curve(0, 23)
	# testcurve(simple, simple.points(1))

	curve25519 = curve(486662, pow(2, 255) - 19)
	testcurve(curve25519, curve25519.points(9))



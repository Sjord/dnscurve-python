
class curve25519:
	def curve25519(n, q):
		"""
		`n` is the private key. It is at least 2**254 and a multiple 
		of 8. It is the scalar which with we want to multiply.
		`q` is the x of point Q. The point Q is the point we want to
		multiply. `q` is an element of the field over `p`.
		Returns `s`, which is the x of `n` * `Q`
		"""

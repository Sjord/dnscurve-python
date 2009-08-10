
class salsa20:
	wordsize = 32
	def quarterround(self, *y):
		z = 4 * [0]
		p = 2 ** self.wordsize
		z[1] = y[1] ^ self.left_rotate((y[0] + y[3]) % p, 7)
		z[2] = y[2] ^ self.left_rotate((z[1] + y[0]) % p, 9)
		z[3] = y[3] ^ self.left_rotate((z[2] + z[1]) % p, 13)
		z[0] = y[0] ^ self.left_rotate((z[3] + z[2]) % p, 18)
		return tuple(z)
	def rowround(self, *y):
		z = 16 * [0]
		(z[0], z[1], z[2], z[3]) = quarterround(y[0], y[1], y[2], y[3])
		(z[5], z[6], z[7], z[4]) = quarterround(y[5], y[6], y[7], y[4])
		(z[10], z[11], z[8], z[9]) = quarterround(y[10], y[11], y[8], y[9])
		(z[15], z[12], z[13], z[14]) = quarterround(y[15], y[12], y[13], y[14])
		return tuple(z)
	def columnround(self, *x):
		y = 16 * [0]
		(y[0], y[4], y[8], y[12]) = quarterround(x[0], x[4], x[8], x[12])
		(y[5], y[9], y[13], y[1]) = quarterround(x[5], x[9], x[13], x[1])
		(y[10], y[14], y[2], y[6]) = quarterround(x[10], x[14], x[2], x[6])
		(y[15], y[3], y[7], y[11]) = quarterround(x[15], x[3], x[7], x[11])
		return tuple(y)
	def doubleround(self, *x):
		return rowround(*columnround(*x))
	def left_rotate(self, number, bits):
		wraparound = number >> self.wordsize - bits
		shifted = number << bits & 2 ** 32 - 1
		return shifted | wraparound 
	def littleendian(self, *b):
		return b[0] + 2 ** 8 * b[1] + 2 ** 16 * b[2] + 2 ** 24 * b[3]

if __name__ == "__main__":
	s20 = salsa20()
	assert s20.left_rotate(0x12345678, 8) == 0x34567812
	for i in 7, 9, 13, 18:
		assert s20.left_rotate(0, i) == 0
	assert s20.left_rotate(0xd3917c5b, 4) == 0x3917c5bd
	assert s20.left_rotate(0xc0a8787e, 5) == 0x150f0fd8
	

	# examples are given in spec
	quarterround = s20.quarterround
	assert quarterround(0x00000000, 0x00000000, 0x00000000, 0x00000000) \
		  == (0x00000000, 0x00000000, 0x00000000, 0x00000000)
	assert quarterround(0x00000001, 0x00000000, 0x00000000, 0x00000000) \
		  == (0x08008145, 0x00000080, 0x00010200, 0x20500000)
	assert quarterround(0x00000000, 0x00000001, 0x00000000, 0x00000000) \
		  == (0x88000100, 0x00000001, 0x00000200, 0x00402000)
	assert quarterround(0x00000000, 0x00000000, 0x00000001, 0x00000000) \
		  == (0x80040000, 0x00000000, 0x00000001, 0x00002000)
	assert quarterround(0x00000000, 0x00000000, 0x00000000, 0x00000001) \
		  == (0x00048044, 0x00000080, 0x00010000, 0x20100001)
	assert quarterround(0xe7e8c006, 0xc4f9417d, 0x6479b4b2, 0x68c67137) \
		  == (0xe876d72b, 0x9361dfd5, 0xf1460244, 0x948541a3)
	assert quarterround(0xd3917c5b, 0x55f1c407, 0x52a58a7a, 0x8f887a3b) \
		  == (0x3e2f308c, 0xd90a8f36, 0x6ab2a923, 0x2883524c)

	rowround = s20.rowround
	assert rowround(0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000001, 0x00000000, 0x00000000, 0x00000000) \
		== (0x08008145, 0x00000080, 0x00010200, 0x20500000, \
		0x20100001, 0x00048044, 0x00000080, 0x00010000, \
		0x00000001, 0x00002000, 0x80040000, 0x00000000, \
		0x00000001, 0x00000200, 0x00402000, 0x88000100)
	assert rowround(0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365, \
		0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6, \
		0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e, \
		0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a) \
		== (0xa890d39d, 0x65d71596, 0xe9487daa, 0xc8ca6a86, \
		0x949d2192, 0x764b7754, 0xe408d9b9, 0x7a41b4d1, \
		0x3402e183, 0x3c3af432, 0x50669f96, 0xd89ef0a8, \
		0x0040ede5, 0xb545fbce, 0xd257ed4f, 0x1818882d)

	columnround = s20.columnround
	assert columnround(0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000001, 0x00000000, 0x00000000, 0x00000000) \
		== (0x10090288, 0x00000000, 0x00000000, 0x00000000, \
		0x00000101, 0x00000000, 0x00000000, 0x00000000, \
		0x00020401, 0x00000000, 0x00000000, 0x00000000, \
		0x40a04001, 0x00000000, 0x00000000, 0x00000000)
	assert columnround(0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365, \
		0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6, \
		0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e, \
		0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a) \
		== (0x8c9d190a, 0xce8e4c90, 0x1ef8e9d3, 0x1326a71a, \
		0x90a20123, 0xead3c4f3, 0x63a091a0, 0xf0708d69, \
		0x789b010c, 0xd195a681, 0xeb7d5504, 0xa774135c, \
		0x481c2027, 0x53a8e4b5, 0x4c1f89c5, 0x3f78c9c8)

	doubleround = s20.doubleround
	assert doubleround(0x00000001, 0x00000000, 0x00000000, 0x00000000, \
		0x00000000, 0x00000000, 0x00000000, 0x00000000, \
		0x00000000, 0x00000000, 0x00000000, 0x00000000, \
		0x00000000, 0x00000000, 0x00000000, 0x00000000) \
		== (0x8186a22d, 0x0040a284, 0x82479210, 0x06929051, \
		0x08000090, 0x02402200, 0x00004000, 0x00800000, \
		0x00010200, 0x20400000, 0x08008104, 0x00000000, \
		0x20500000, 0xa0000040, 0x0008180a, 0x612a8020)
	assert doubleround(0xde501066, 0x6f9eb8f7, 0xe4fbbd9b, 0x454e3f57, \
		0xb75540d3, 0x43e93a4c, 0x3a6f2aa0, 0x726d6b36, \
		0x9243f484, 0x9145d1e8, 0x4fa9d247, 0xdc8dee11, \
		0x054bf545, 0x254dd653, 0xd9421b6d, 0x67b276c1) \
		== (0xccaaf672, 0x23d960f7, 0x9153e63a, 0xcd9a60d0, \
		0x50440492, 0xf07cad19, 0xae344aa0, 0xdf4cfdfc, \
		0xca531c29, 0x8e7943db, 0xac1680cd, 0xd503ca00, \
		0xa74b2ad6, 0xbc331c5c, 0x1dda24c7, 0xee928277)

	littleendian = s20.littleendian
	assert littleendian(0, 0, 0, 0) == 0x00000000
	assert littleendian(86, 75, 30, 9) == 0x091e4b56
	assert littleendian(255, 255, 255, 250) == 0xfaffffff



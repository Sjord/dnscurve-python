
class salsa20:
	wordsize = 32
	def quarterround(self, *y):
		z = [0, 0, 0, 0]
		p = 2 ** self.wordsize
		z[1] = y[1] ^ self.left_rotate((y[0] + y[3]) % p, 7)
		z[2] = y[2] ^ self.left_rotate((z[1] + y[0]) % p, 9)
		z[3] = y[3] ^ self.left_rotate((z[2] + z[1]) % p, 13)
		z[0] = y[0] ^ self.left_rotate((z[3] + z[2]) % p, 18)
		return tuple(z)
	def left_rotate(self, number, bits):
		wraparound = number >> self.wordsize - bits
		shifted = number << bits & 2 ** 32 - 1
		return shifted | wraparound 

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

		

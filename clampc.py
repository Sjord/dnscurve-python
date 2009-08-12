
def clampc(str):
	assert len(str) == 32
	n0 = ord(str[0])
	n0 = n0 - (n0 % 8)
	n31 = ord(str[31])
	n31 = 64 + (n31 % 64)
	return chr(n0) + str[1:31] + chr(n31)

if __name__ == "__main__":
	def test_clampc(str):
		out = clampc(str)
		assert len(out) == 32
		assert ord(out[0]) & 7 == 0
		assert ord(out[31]) & 128 == 0
		assert ord(out[31]) & 64 == 64
	test_clampc('\0' * 32)
	test_clampc('\xff' * 32)

import struct

class little_endian:
	def to_string(self, number):
		res = ''
		for _ in range(0, 32):
			res += chr(number % 256)
			number /= 256
		return res
	def from_string(self, string):
		assert len(string) == 32
		numbers = struct.unpack('<4Q', string)
		res = numbers[3]
		res <<= 64
		res += numbers[2]
		res <<= 64
		res += numbers[1]
		res <<= 64
		res += numbers[0]
		return res

class base32:
	# Performance can be improved by using bitshifting instead of
	# diding, or maybe even by using divmod()
	# Also, in decode, don't do 32 ** i every loop
	alphabet = "0123456789bcdfghjklmnpqrstuvwxyz"
	def __init__(self):
		i = 0
		self.lookup = {}
		for letter in self.alphabet:
			self.lookup[letter] = i
			i += 1
	def encode(self, number):
		result = ''
		while (number > 0):
			index = number % 32
			result += self.alphabet[index]
			number /= 32
		return result
	def decode(self, str):
		str = str.lower()
		result = 0
		i = 0
		for char in str:
			value = self.lookup[char]
			result += value * 32 ** i
			i += 1
		return result


if __name__ == "__main__":
	le = little_endian()
	assert 9 == le.from_string("\x09" + 31 * "\0");
	assert 2 ** 255 == le.from_string(31 * "\0" + "\x80")

	assert le.to_string(9) == "\x09" + 31 * "\0"
	assert le.to_string(2 ** 255) == 31 * "\0" + "\x80"

	b32 = base32()
	# 4321 == 34916, from the dnscurve.org website
	assert "4321" == b32.encode(34916)
	assert 34916 == b32.decode("4321")

	i = 1
	while i < 2 ** 255 - 19:
		i += 2 ** 247 - 1
		assert i == b32.decode(b32.encode(i))
	
	test = "BBBBCCCCddddZzZz0000111122223333"
	assert test.lower() == b32.encode(b32.decode(test))

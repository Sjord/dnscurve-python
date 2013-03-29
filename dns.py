import socket
import struct
import StringIO

# OCTET 1,2 	ID 
# OCTET 3,4	QR(1 bit) + OPCODE(4 bit)+ AA(1 bit) + TC(1 bit) + RD(1 bit)+ RA(1 bit) + 
# 		Z(3 bit) + RCODE(4 bit)
# OCTET 5,6	QDCOUNT 
# OCTET 7,8	ANCOUNT	
# OCTET 9,10	NSCOUNT	
# OCTET 11,12	ARCOUNT

class DnsHeader:
	def __init__(self):
		self.id = 0x1234
		self.bits = 0x0100 # recursion desired
		self.qdCount = 0
		self.anCount = 0
		self.nsCount = 0
		self.arCount = 0
	def toBinary(self):
		return struct.pack('!HHHHHH',
			self.id,
			self.bits,
			self.qdCount,
			self.anCount,
			self.nsCount,
			self.arCount);
	def fromBinary(self, bin):
		if bin.read:
			bin = bin.read(12)
		(self.id,
		 self.bits,
		 self.qdCount,
		 self.anCount,
		 self.nsCount,
		 self.arCount) = struct.unpack('!HHHHHH', bin)
		return self
	def __repr__(self):
		return '<DnsHeader %d, %d questions, %d answers>' % (self.id, self.qdCount, self.anCount)

class DnsResourceRecord:
	pass

class DnsAnswer(DnsResourceRecord):
	pass

class DnsQuestion:
	def __init__(self):
		self.labels = []
		self.qtype = 1  # A-record
		self.qclass = 1 # the Internet
	def toBinary(self):
		bin = '';
		for label in self.labels:
			assert len(label) <= 63
			bin += struct.pack('B', len(label))
			bin += label
		bin += '\0' # Labels terminator
		bin += struct.pack('!HH', self.qtype, self.qclass)
		return bin

class DnsPacket:
	def __init__(self, header = None):
		self.header = header
		self.questions = []
		self.answers = []
	def addQuestion(self, question):
		self.header.qdCount += 1
		self.questions.append(question)
	def toBinary(self):
		bin = self.header.toBinary()
		for question in self.questions:
			bin += question.toBinary()
		return bin
	def __repr__(self):
		return '<DnsPacket %s>' % (self.header)

class BinReader(StringIO.StringIO):
	def unpack(self, fmt):
		size = struct.calcsize(fmt)
		bin = self.read(size)
		print bin.encode('hex')
		return struct.unpack(fmt, bin)

class DnsPacketConverter:
	def fromBinary(self, bin):
		reader = BinReader(bin)
		header = DnsHeader().fromBinary(reader)
		packet = DnsPacket(header)
		for qi in range(header.qdCount):
			q = self.readQuestion(reader)
			packet.questions.append(q)
		for ai in range(header.anCount):
			a = self.readAnswer(reader)
			packet.answers.append(a) 
		return packet
	def readQuestion(self, reader):
		question = DnsQuestion()
		question.labels = self.readLabels(reader)
		(question.qtype, question.qclass) = reader.unpack('!HH')
		return question
	def readAnswer(self, reader):
		print "reading answer"
		answer = DnsAnswer()
		answer.name = self.readLabels(reader)
		(type, rrclass, ttl, rdlength) = reader.unpack('!HHiH')
		answer.rdata = reader.read(rdlength)
		print answer.rdata
	def readLabels(self, reader):
		labels = []
		while True:
			(length,) = reader.unpack('B')
			if length == 0: break

			# Compression
			compressionMask = 0b11000000;
			if length & compressionMask:
				byte1 = length & ~compressionMask;
				(byte2,) = reader.unpack('B')
				offset = byte1 << 8 | byte2
				oldPosition = reader.tell()
				result = self.readLabels(reader)
				reader.seek(oldPosition)
				return result

			label = reader.read(length)
			labels.append(label)
		return labels
	


if __name__ == '__main__':
	header = DnsHeader()
	bin = header.toBinary()
	print 'header', bin.encode('hex')

	question = DnsQuestion()
	question.labels = ['google', 'com']
	print 'question', question.toBinary().encode('hex')

	packet = DnsPacket(header)
	packet.addQuestion(question)
	print 'packet', packet.toBinary().encode('hex')

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# dest = ('127.0.0.1', 5353)
	dest = ('8.8.4.4', 53)
	sock.sendto(packet.toBinary(), dest)
	(response, address) = sock.recvfrom(1024)
	print 'respon', response.encode('hex')

	conv = DnsPacketConverter()
	packet = conv.fromBinary(response)
	print packet


	

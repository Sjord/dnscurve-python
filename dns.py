from struct import pack
import socket

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
		self.bits = 0
		self.qdCount = 0
		self.anCount = 0
		self.nsCount = 0
		self.arCount = 0
	def toBinary(self):
		return pack('!HHHHHH',
			self.id,
			self.bits,
			self.qdCount,
			self.anCount,
			self.nsCount,
			self.arCount);

class DnsQuestion:
	def __init__(self):
		self.labels = []
		self.qtype = 1  # A-record
		self.qclass = 1 # the Internet
	def toBinary(self):
		bin = '';
		for label in self.labels:
			assert len(label) <= 63
			bin += pack('B', len(label))
			bin += label
		bin += '\0' # Labels terminator
		bin += pack('!HH', self.qtype, self.qclass)
		return bin

class DnsPacket:
	def __init__(self, header):
		self.header = header
		self.questions = []
	def addQuestion(self, question):
		self.header.qdCount += 1
		self.questions.append(question)
	def toBinary(self):
		bin = self.header.toBinary()
		for question in self.questions:
			bin += question.toBinary()
		return bin


if __name__ == '__main__':
	header = DnsHeader()
	bin = header.toBinary()
	print 'header', bin.encode('hex')

	question = DnsQuestion()
	question.labels = ['hello', 'world']
	print 'question', question.toBinary().encode('hex')

	packet = DnsPacket(header)
	packet.addQuestion(question)
	print 'packet', packet.toBinary().encode('hex')

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.sendto(packet.toBinary(), ('8.8.4.4', 53))
	result = sock.recvfrom(1024)
	print 'result', result


	

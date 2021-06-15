import heapq	 #for priority queue
import os		 #for file operations 


class HuffmanCoding:
	def __init__(self, path):
		self.path = path	#used in compressing and decompressing 
		self.heap = []		#for storing frequencies of each character
		self.codes = {}		#encoded code for each character
		self.reverse_mapping_codes = {}

	class HeapNode:
		def __init__(self, data, freq):
			self.data = data
			self.freq = freq
			self.left = None
			self.right = None

		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, self)):
				return False
			return self.freq == other.freq

#make frequency table of input text
	def freq_table(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency


#make priority queue for storing characters according to freq table
	def make_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)


#build the huffman tree
	def merge_nodes(self):
		while(len(self.heap)>1):	#while only the root is left in the tree
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


#recursively get the codes for all characters
	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.data != None):
			self.codes[root.data] = current_code
			self.reverse_mapping_codes[current_code] = root.data
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


#make codes for each character
	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


#convert input text to compressed text
	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


#add padding to code to make it multiple of 8 to convert it inot bytes
	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"
					#convert into 8 bytes
		padded_info = "{0:08b}".format(extra_padding)	 #stored so that we can know how many padding was added
		encoded_text = padded_info + encoded_text
		return encoded_text


#create bytes of each 8 characters and store in a array
	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]			 #conver the string into 2 base number
			b.append(int(byte, 2))
		return b


#compress the input file
	def compress(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"
		#get file name and its extension to save the compressed file with similar name


		 #open input file as read only and output as write  in binary mode
		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()		#read input file
			text = text.rstrip()	#strip out any white spaces

			frequency = self.freq_table(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))

		return output_path




	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping_codes):
				character = self.reverse_mapping_codes[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + file_extension

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)					#get the integer value
				bits = bin(byte)[2:].rjust(8, '0')	#it append 0b to start so trim it
				bit_string += bits					#append 0 in starting to make it 8 bit
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)

		return output_path


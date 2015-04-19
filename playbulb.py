import sys, re, subprocess, getopt
from time import sleep

def write(colour, bulb_list):
	# Set Playbulb colour
	for e in bulb_list:
		print('gatttool -b ' + e + ' --char-write -a 0x0016 -n ' + colour)
		subprocess.call(('gatttool -b ' + e + ' --char-write -a 0x0016 -n ' + colour).split())
	#	sleep(1)

def read(bulb_list):
	for e in bulb_list:
		proc = subprocess.Popen(('gatttool -b ' + e + ' --char-read -a 0x0016').split(), stdout = subprocess.PIPE)
	#	sleep(1)
		for line in iter(proc.stdout.readline,''):
	  		print 'output: ' + line


def main(argv):

	PLAYBULB_ADDRESS_1 = "AC:E6:4B:07:70:E8"
	PLAYBULB_ADDRESS_2 = "AC:E6:4B:07:A9:8E"
	PLAYBULB_ADDRESS_3 = "AC:E6:4B:06:C9:12"
	color = 'white'
	mode = 'write'

	COLOUR_MAP = { 'red': '00ff0000',
		       'blue': '000000ff',
		       'green': '0000ff00',
			'white': 'FFFF6000',
			'orange': '00FF0F00',
			'yellow': '00FF7700',
			'purple': '00FF00F0',
			'off': '00000000'}
	bulb_list = []
	bulb_list.append(PLAYBULB_ADDRESS_1)

	try:
		opts, args = getopt.getopt(argv,"hc:t:m:",["colour", "target","mode"])
	except getopt.GetoptError:
		print 'playbulb.py -c <color> -t <targetbulb> -m <mode>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'playbulb.py -c <color> -t <targetbulb> -m <mode>'
			sys.exit()
		elif opt in ("-c", "--color"):
			color = arg
		elif opt in ("-m", "--mode"):
			mode = arg
		elif opt in ("-t", "--target"):
			if arg== '1':
				# todo: Find a better way to do this list in python
				bulb_list = []
				bulb_list.append(PLAYBULB_ADDRESS_1)
			elif arg == '2':
				bulb_list = []
				bulb_list.append(PLAYBULB_ADDRESS_2)
			elif arg == '3':
				bulb_list = []
				bulb_list.append(PLAYBULB_ADDRESS_3)
			elif arg == 'all':
				bulb_list = []
				bulb_list.append(PLAYBULB_ADDRESS_1)
				bulb_list.append(PLAYBULB_ADDRESS_2)
				bulb_list.append(PLAYBULB_ADDRESS_3)

	colour = COLOUR_MAP[color]
	print 'colour is '+ color+' code is '+colour 


	# Your Playbulb address (obtained with 'sudo hcitool lescan')



	# Show the name of the playbulb
	for e in bulb_list:
		proc = subprocess.Popen(('gatttool -b ' + e + ' --char-read -a 0x0003').split(), stdout = subprocess.PIPE)
	#	sleep(1)
		for line in iter(proc.stdout.readline,''):
	  		name = ''.join(x.strip() for x in re.findall(r'[0-9a-f]{2}\s', line)).decode("hex")
	  	print 'Playbulb name: ' + name

	read(bulb_list)
	write(colour, bulb_list)
	read(bulb_list)

if __name__ == "__main__":
	main(sys.argv[1:])



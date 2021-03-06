# -*- coding: utf-8 -*-
import ConfigParser
import subprocess
from subprocess import call
from sys import argv
from sys import exit

#TODO
# - implement tests
# 	- download test data
# - place into pip package
# - write readme
# - write docs
paired_end=False

# step 1: read in configuration file
def read_conf(conf):
	"""read config file and set it internal variables to config variables"""
	config = ConfigParser.ConfigParser()
	config.read(conf)
	k = config.get('options', 'k')
	data = config.get('options', 'data')
	outprefix = config.get('options', 'outprefix')
	assemblers = config.items("assemblers")
	other = config.items("other")
	return [k, data, outprefix, assemblers, other]

#step 2: run the assemblers
def velvet(k, outprefix, data):
	"""function to run the velvet assembler on the data"""
	directory = outprefix+".velvet"
	data_type = "-short -fmtAuto " + data
	#print subprocess.list2cmdline(["velveth", directory, k, "-short", "-fmtAuto", data])
	call(["velveth", directory, k, "-short", "-fmtAuto", data]) #simplest case where k is one value and data is also one value
	call(["velvetg", directory])
	run_quast(directory+"/contigs.fa")

def abyss(k, outprefix, data):
	"""function to run the abyss-pe assembler on the data"""
        if not paired_end:
                raise ValueError("Abyss can only be used with paired end data and it looks like you are only supplying one file. \n Please provide paired end data.")
	directory = outprefix+".abyss-pe"
	string_data = "".join(data)
        call(["mkdir", directory])
	call(["abyss-pe", "k="+k, "name="+outprefix, "in="+string_data])
	run_quast(directory+outprefix+"-contigs.fa")

def run_other(command, outprefix):
	"""function for running arbitrary assemblers not included in this script"""
	input_cmd = command.split(" ")
	call(["mkdir", outprefix+"."+input_cmd[0]])
	call(["cd", outprefix+"."+input_cmd[0]])
	call([command])

def run_quast(contigs):
	"""function to run QUAST on contigs generated by assemblers for quality assessment"""
	call(["quast.py", contigs])


# run the program
if __name__ == '__main__':
	# import config and set variables
	try:
		conf = argv[1]
	except IndexError:
		print ">>>You need to supply a configuration file!"
		exit()
	k, data, outprefix, assemblers, other = read_conf(conf)
	known_assemblers = {'velvet':velvet,
 						'abyss':abyss}

	paired_end = False
        if len(data.split(" ")) > 1:
                paired_end = True
        # run assemblies
	if len(assemblers) > 0:
		for item in assemblers:
			current_assembler = item[1]
			if current_assembler in known_assemblers:
				try:
					known_assemblers[current_assembler](k, outprefix, data) #run the command
				except OSError:
					print ">>>"+current_assembler+" is not installed or is not on your path. Please make sure you have this assembler installed."
			else:
				print ">>>"+current_assembler + " is not a known assembler, please supply the full command to run it in the [other] section of the config file.\nPlease submit an issue to add this assembler on Github."
	
	if len(other) > 0:
		for item in other:
			current_command = item[1]
			try:
				run_other(current_command, outprefix)
			except OSError:
				print ">>>"+current_command+" is not installed or is not on your path. Please make sure you have this assembler installed."


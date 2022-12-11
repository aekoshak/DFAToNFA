# Name: pa1.py
# Author(s) Abdulqader Koshak, abdulqaderkoshak@sandiego.edu,
# 			Noelle Tuchscherer, ntuchscherer@sandiego.edu:
# Date 9/1/2020:
# Description This program simulates the computation of a DFA M on an input string s, and reports if s is
# accepted by M. (That is, if s is in the language of M, or s ∈ L(M).):
import sys

class DFA:
	""" Simulates a DFA """

	def __init__(self, filename):
		"""
		Initializes DFA from the file whose name is
		filename
		"""
		#open file and initializing vars
		file = open(filename, 'r')
		num_states = int(file.readline())
		alphabet = file.readline()
		num_trans = num_states*(len(alphabet)-1) #We need the number of traansitions to loop though it from the file
		
		self.transitions = [] #initializing transitiions
		for _ in range(num_trans):
			self.transitions.append(file.readline().split()) #Stoing transitions form dfaX.txt file
		
		
		#Starting state
		self.starting_state = file.readline().split()[0]
		
		#List of all accept states
		self.accept_states = file.readline().split()

		#dfaX.txt into strX.txt and extracting strings from strX.txt
		strfilename = filename.replace("dfa", "str")
		strfile = open(strfilename, 'r') 
		strings_list = strfile.read().split()#Splting each strings
		
		#Running the simulater with each string in the file
		for string in strings_list:
			self.simulate(string)
		
		#closing files
		strfile.close()
		file.close()
	
	def simulate(self, str):
		""" 
		Simulates the DFA on input str.  Returns
		True if str is in the language of the DFA,
		and False if not.
		"""
		#Current_state always start from the starting state
		current_state = self.starting_state
		
		#Loop through each char in the sting str
		for ch in str:
			#Loop through each transtiion into the transtions list
			for transition in self.transitions:
				if transition[0] == current_state and transition[1].replace("'", "") == ch:#If we found the right transition 
					current_state = transition[2]#Advance current_state to the next state
					break #Skip to the next char
		
		#If currrent_state (Last state) is acceptence state retun True otherwise return False
		if current_state in self.accept_states:
			return True
		else:
			return False
	
	
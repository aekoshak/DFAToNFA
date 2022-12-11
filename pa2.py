# Name: pa2.py
# Author(s): Abdulqader Koshak - abdulqaderkoshak@sandiego.edu
#			 Noelle Tuchscherer - ntuchscherer@sandiego.edu
# Date: 09-21-2020
# Last updated: 10-01-2020
# Description: This program reads an NFA from a file and converts it to an equivalent DFA, which it then outputs to a file

class NFA:
	""" Simulates an NFA """

	# Initializes an NFA from nfa_filename and outputs an equivalent DFA
	# to dfa_filename
	def __init__(self, nfa_filename):
		"""
		Initializes NFA from the file whose name is
		nfa_filename.  (So you should create an internal representation
		of the nfa.)
		"""
		# Open file and initialize variables
		file = open(nfa_filename, 'r')
		self.num_states = file.readline()
		self.alphabet = file.readline()

		# Initialize transitions
		self.transitions = []
		tran = file.readline()
		while(tran != "\n"):
			clean_tran = tran.split()
			clean_tran[1] = clean_tran[1].replace("'", "")
			self.transitions.append(clean_tran) # String transitions form dfaX.txt file
			tran = file.readline()
		
		
		# Starting state
		self.starting_state = file.readline().split()[0]
		
		# List of all accept states
		self.accept_states = file.readline().split()
		
		# Call toDFA to convert NFA to DFA
		dfa_filename = nfa_filename.replace("nfa", "dfa")
		self.toDFA(dfa_filename)
		
		# Closing files
		file.close()
	
		print(self.num_states)
		print(self.alphabet)
		print(self.transitions)
		print(self.starting_state)
		print(self.accept_states)

	# Converts input NFA to an equivalent DFA and writes DFA to dfa_filename
	def toDFA(self, dfa_filename):
		"""
		Converts the "self" NFA into an equivalent DFA
		and writes it to the file whose name is dfa_filename.
		The format of the DFA file must have the same format
		as described in the first programming assignment (pa1).
		This file must be able to be opened and simulated by your
		pa1 program.

		This function should not read in the NFA file again.  It should
		create the DFA from the internal representation of the NFA that you 
		created in __init__.
		"""

		
		dfafile = open(dfa_filename, 'w') 
	
		
		dfa_transitions = []
		dfa_states = []

		
		# Determine DFA start state
		start_state = []
		start_state.append(self.starting_state)
		for start in start_state:
			for tran in self.transitions:
				if tran[0] == start and tran[1] == 'e':
					if tran[2] not in start_state:
						start_state.append(tran[2])

		# Add start state to DFA
		dfa_states.append(start_state)
		
		# Determine rest of DFA states			
		for states in dfa_states:
			for s in self.alphabet:
				if s == '\n':
					continue
				states_subset = []
				for state in states:
					for tran in self.transitions:
						# Add all possible states from current state scanning s
						if tran[0] == state and tran[1] == s:
							if tran[2] not in states_subset:
								states_subset.append(tran[2])
						# Add all possible states reachable from an epsilon transition
						if tran[0] == state and tran[1] == 'e':
							eps = tran[2]
							for tran in self.transitions:
								if tran[0] == eps and tran[1] == s:
									if tran[2] not in states_subset:
										states_subset.append(tran[2])
				
				# If the new set of sub states is not in the DFA, add it to DFA
				if len(states_subset) != 0 and states_subset not in dfa_states:
					dfa_states.append(states_subset)
				if len(states_subset) != 0:
					new_tran = [states, s, states_subset]
					if new_tran not in dfa_transitions:
						dfa_transitions.append(new_tran)
				# Add a reject state for cases where the string extends beyond an accept
				# state with no pre-existing transitions out
				elif len(states_subset) == 0:
					new_tran = [states, s, ['r']]
					if new_tran not in dfa_transitions:
						dfa_transitions.append(new_tran)
					if ['r'] not in dfa_states:
						dfa_states.append(['r'])
		
		# Determine DFA accept states
		dfa_accept_states = []
		for states in dfa_states:
			for accept in self.accept_states:
				if accept in states:
					dfa_accept_states.append(states)
					
		
		
		# Write DFA structure to new file
		dfafile.write(str(len(dfa_states)) + "\n")
		

		dfafile.write(self.alphabet)
		
		for transition in dfa_transitions:
			string = str(dfa_states.index(transition[0]) + 1)
			string += " '" + transition[1] + "' "
			string += str(dfa_states.index(transition[2]) + 1)
			dfafile.write(string + "\n")
		dfafile.write('1' + "\n")

		for dfa_accept in dfa_accept_states:
			dfafile.write(str(dfa_states.index(dfa_accept) + 1) + " ")
		
		dfafile.close()


if __name__ == "__main__":
	NFA("nfa3.txt")
		
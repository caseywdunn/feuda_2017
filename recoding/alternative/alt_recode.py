import sys
import re
from string import maketrans
import random
import collections

# Tools to recode phylip data matrices, ie to substitute every occurance of a
# particular state with another state.
#
# These tools support a reduced representation recoding scheme, as well as
# transforms that modify the recoding scheme.
#
# Here is how I refer to these processes:
# - Recoding is the application of a reduced state recoding map that results
#   in a smaller number of character states.
#   A Recoding is specified by a space delimeted string called the code, where
#   all the states to be mapped to the same state are in an uniterrupted block.
#   The first state in each block is used as the new state for all states in
#   the block. This code is converted to a map that defines the recoding.
#   This map is a tuple that contains two strings of equal length. The first
#   has all the original states, and the second has the reduced states that
#   each of those states map to (as defined by conserved position).
# - Transforming is the application of a map that changes some states to other
#   states. It results in the same number of states after as before the
#   transform. It is used to scramble states. A transform is defined by a
#   tuple that contains two strings of equal length. The first has all the
#   original states, and the second has the states that each of those states
#   map to (as defined by conserved position). These tools apply the transform
#	to the recoding code, rather than to the data. The transform is useful to
#	build up null expectations under random recodings.


def sr_codes():
	# The SR codings are from the left side of Table 1 of
	# https://academic.oup.com/mbe/article-lookup/doi/10.1093/molbev/msm144
	#
	# Put an empty string in position 0 so that the index of the tuple
	# corresponds to the number of recoded states
	return (
	"",
	"ADEGKNPQRSTCFHILMVWY",
	"ADEGKNPQRST CFHILMVWY",
	"ADEGNPST CHKQRW FILMVY",
	"AGNPST CHWY DEKQR FILMV",
	"AGPST CFWY DEN HKQR ILMV",
	"APST CW DEGN FHY ILMV KQR",
	"AGST CW DEN FY HP ILMV KQR",
	"AST CG DEN FY HP ILV KQR MW",
	"AST CW DE FY GN HQ ILV KR MP",
	"AST CW DE FY GN HQ IV KR LM P",
	"AST C DE FY GN HQ IV KR LM P W",
	"AST C DE FY G HQ IV KR LM N P W",
	"AST C DE FY G H IV KR LM N P Q W",
	"AST C DE FL G H IV KR M N P Q W Y",
	"AST C DE F G H IV KR L M N P Q W Y",
	"AT C DE F G H IV KR L M N P Q S W Y",
	"AT C DE F G H IV K L M N P Q R S W Y",
	"A C DE F G H IV K L M N P Q R S T W Y",
	"A C D E F G H IV K L M N P Q R S T W Y",
	"A C D E F G H I V K L M N P Q R S T W Y"
	)

def get_recode_map( code ):
	# Convert the space-delimited string to a tuple where the
	# first string is the original states and the second string
	# is the recoded states

	original_states = code.replace( " ", "" )

	blocks = code.split(" ")
	recoded_states = ""

	for block in blocks:
		block_string = block[0] * len( block )
		recoded_states = recoded_states + block_string

	assert len( original_states ) == len( recoded_states )

	recode_map = ( original_states, recoded_states )
	return recode_map

def apply_map( sequence, map ):
	recode_table = maketrans( map[0], map[1] )
	return sequence.translate( recode_table )

def write_recoded_matrix( file_name, header, seq_names, sequences, transform_map, code ):

	# Apply the transform to the code
	transformed_code = apply_map( code, transform_map )

	# Buld a recode map that applies both the transform and the recoding
	recode_map = get_recode_map( transformed_code )

	#print( "file: {}\n  original: {}\n  recoded:  {}".format( file_name, recode_map[0], recode_map[1] ) )
	print( "output file: {}  transform map in: {}".format( file_name, transform_map[0] ) )
	print( "output file: {} transform map out: {}".format( file_name, transform_map[1] ) )
	print( "output file: {}     original code: {}".format( file_name, code ) )
	print( "output file: {}  transformed code: {}".format( file_name, transformed_code ) )
	print( "output file: {}   complete map in: {}".format( file_name, recode_map[0] ) )
	print( "output file: {}  complete map out: {}".format( file_name, recode_map[1] ) )

	observed_states = set( list( ''.join( sequences ) ) )
	recode_in = set( list( recode_map[ 0 ] ) )

	print( "output file: {}  states in data but not recode: {}".format( file_name, ''.join( list(observed_states - recode_in ) ) ) )
	print( "output file: {}  states in recode but not data: {}".format( file_name, ''.join( list(recode_in - observed_states ) ) ) )



	out_file = open(file_name, "w")
	out_file.write(header + "\n")
	for i in range(0,len(seq_names)):
		new_seq = apply_map( sequences[i], recode_map )
		out_file.write( seq_names[i] + new_seq + "\n" )
	out_file.close()

def write_recoded_matrices( file_base_name, header, seq_names, sequences, transform_map, codes, n_states ):
	for n_state in n_states:
		code = codes[ n_state ]
		file_name =  '{}_states-{:02d}.phy'.format(file_base_name, n_state)
		write_recoded_matrix( file_name, header, seq_names, sequences, transform_map, code )

def read_phylip( inmatrix_name ):
	# Read the source file
	inmatrix = open( inmatrix_name, "r" )
	lines = [ line.rstrip('\n') for line in inmatrix ]
	lines = list(filter(None, lines)) # Remove empty lines
	header = lines[0]
	n_taxa = int( header.split(" ")[0] )
	print( "n_taxa: {}".format(n_taxa) )
	assert len(lines) == (n_taxa+1)

	p = re.compile(r'^([\w-]+\s+)([\w-]+)$')
	seq_names = []
	sequences = []
	n = 0
	for line in lines[1:]:
		n = n + 1
		m = p.match(line)
		if not m:
			print( line[0:30] + "..." )
			raise ValueError('Taxon number {} not formatted correctly'.format(n))
		seq_names.append( m.group(1) )
		sequences.append( m.group(2) )

	assert len( seq_names ) == len( sequences )

	return header, seq_names, sequences

def phylip_summary( inmatrix_name ):
	# Some basis matrix stats to help validate results
	header, seq_names, sequences = read_phylip( inmatrix_name )
	print( "Name: {}".format( inmatrix_name ) )
	print( "Taxa: {}".format( len( seq_names ) ) )
	observed_states = set( list( ''.join( sequences ) ) )
	state_counts = collections.Counter( ''.join( sequences ) )
	print( "State counts: {}".format( state_counts ) )


def single_transform( inmatrix_name, n_states, transformed_states, name ):
	# For writing out a single matrix, given a transformed code
	inmatrix_name_base = inmatrix_name.replace(".phy", "")
	codes = sr_codes()
	states = codes[ 1 ]
	header, seq_names, sequences = read_phylip( inmatrix_name )
	file_base_name = inmatrix_name_base + "_mod_transform-{}".format(name)
	transform_map = ( states, transformed_states )
	write_recoded_matrices( file_base_name, header, seq_names, sequences, transform_map, codes, n_states )

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python alt_recode.py matrix.phy n_transforms"
		sys.exit(0)
	print( "Command: " + ' '.join(sys.argv) )
	inmatrix_name = sys.argv[1]
	inmatrix_name_base = inmatrix_name.replace(".phy", "")
	n_transforms = int( sys.argv[2] )

	codes = sr_codes()

	# Get the original states to consider
	states = codes[ 1 ]

	# Read the phylip
	header, seq_names, sequences = read_phylip( inmatrix_name )

	# First perform recoding on original matrix
	n_states = [20, 18, 16, 14, 12, 10, 8, 6] # The numbers of recoded states to consider
	file_base_name = inmatrix_name_base + "_mod_transform-none"
	transform_map = ( states, states ) # Map the states to themselves, ie don't transform anything
	write_recoded_matrices( file_base_name, header, seq_names, sequences, transform_map, codes, n_states )

	# Now do recoding n_transforms times:
	n_states = [18, 16, 14, 12, 10, 8, 6] # The numbers of recoded states to consider
	for i in range( 0, n_transforms ):
		file_base_name = inmatrix_name_base + "_mod_transform-{:02d}".format(i)
		transformed_states = ''.join( random.sample( states, len( states ) ) )
		transform_map = ( states, transformed_states )
		write_recoded_matrices( file_base_name, header, seq_names, sequences, transform_map, codes, n_states )

import random
import logging

from flask import Flask
from flask import g

import helpers

# Set up logging
logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s')
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

# Path to the DB file
DATABASE = '../moves.db'

# How many entries the DB file contains
ENTRY_COUNT = 1148770438

# How many bytes one entry takes
ENTRY_SIZE = 6

app = Flask(__name__)

@app.before_request
def before_request():
    try:
        g.db = open(DATABASE, 'r')
    except IOError as e:
        logger.error( e )

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/<int:wbr>/<int:wpa>/<int:wsc>/<int:wst>/<int:sbr>/<int:spa>/<int:ssc>/<int:sst>/<int:topdown>/<int:difficulty>/<int:mean>")
def play(wbr, wpa, wsc, wst, sbr, spa, ssc, sst, topdown, difficulty, mean):
	position = [wbr, wpa, wsc, wst, sbr, spa, ssc, sst]

	# All input values must be in range
	for i in xrange(8):
		if not 0 <= position[i] <= 24:
			return "Error: Invalid argument %s" % (i + 1)
	if not 0 <= topdown <= 1:
		return "Error: Invalid argument 9"
	if not 0 <= mean <= 1:
		return "Error: Invalid argument 10"

	# Pieces must not overlap
	living_pieces = [x for x in position if x != 0]
	if len(set(living_pieces)) != len(living_pieces):
		return "Error: Pieces overlap"

	# The position must not be won already
	if helpers.is_won_by_either_side(position):
		return "Error: Already won"

	# Turn the board for topdown view
	if (topdown == 1):
		position = helpers.turn(position)

	# Look at all possible moves
	movelist = [] # Contains 32 values, each indicating how many moves the enemy will need for the resulting position
	for move in xrange(32):
		# Apply the move and turn the board
		next_position = helpers.make_move(position, move)
		if not next_position:
			movelist.append(None)
			continue
		next_position = helpers.turn(next_position)

		# Is this position won?
		if helpers.is_won_by_either_side(next_position):
			movelist.append(0)
			continue

		# Can the position be won in one move?
		if helpers.get_first_winning_move(next_position) != -1:
			movelist.append(1)
			continue

		# Will be game be lost in two moves?
		if helpers.get_first_losing_move(next_position) != -1:
			movelist.append(2)
			continue

		# Can the game be won in three moves?
		if helpers.get_first_winning_move_3(next_position) != -1:
			movelist.append(3)
			continue

		# Does the position exist in the database?
		if helpers.is_mirrored(next_position):
			next_position = helpers.mirror_position(next_position)
		next_position = helpers.encode_compact_position(next_position)
		count = retrieve_count(next_position, 0, ENTRY_COUNT)

		# This position is a draw
		if count is None:
			movelist.append(-1)
			continue

		# Found it!
		movelist.append(count)

	# Apply difficulty: High numbers are seen as draw
	for move in xrange(32):
		if difficulty < movelist[move]:
			movelist[move] = -1

	# Find the highest odd and lowest even number
	#print "%s %s %s %s" % (movelist[0:8], movelist[8:16], movelist[16:24], movelist[24:32])
	lowest_even = 100 # Cant be more than 65 moves
	highest_odd = None
	for move in xrange(32):
		if movelist[move] is None:
			continue
		if movelist[move] % 2 == 0:
			lowest_even = min(lowest_even, movelist[move])
		else:
			highest_odd = max(highest_odd, movelist[move])

	# Find the best moves
	if lowest_even is not 100:
		# This position is won
		if mean == 1:
			best_moves = [x for x in xrange(32) if movelist[x] is not None and movelist[x] % 2 == 0]
		else:
			best_moves = [x for x in xrange(32) if movelist[x] == lowest_even]
	elif -1 in movelist:
		# This position results in a draw
		# Go forward if possible
		best_moves = filter(lambda x: movelist[x] == -1, [0, 1, 7, 8, 9, 15, 16, 17, 23, 24, 25, 31])
		# Go to the side
		if not best_moves:
			best_moves = filter(lambda x: movelist[x] == -1, [2, 6, 10, 14, 18, 22, 26, 30])
		# Go backwards
		if not best_moves:
			best_moves = filter(lambda x: movelist[x] == -1, [3, 4, 5, 11, 12, 13, 19, 20, 21, 27, 28, 29])
	elif highest_odd is not None:
		# This position is lost
		best_moves = [x for x in xrange(32) if movelist[x] == highest_odd]
	else:
		# This position is impossible
		return "Error: No move possible"

	# Pick a random move from the best moves
	move = random.choice(best_moves)
	logger.info('Situation is %s, returning move %s' % (str((wbr, wpa, wsc, wst, sbr, spa, ssc, sst, topdown, difficulty, mean)), move))
	return "%s %s" % (move if topdown == 0 else helpers.mirror_move(move), movelist[move])

# Binary search in the DB file
# "start" is included, "end" is excluded
def retrieve_count(position, start, end):
	logger.debug( "retrieving count for %s between %s and %s" % ( position, start, end ) )

	# Recursion anchor
	if end <= start:
		logger.debug( "no result" )
		return None

	# Find the position in the middle
	middle = (start + end) / 2
	g.db.seek( middle * ENTRY_SIZE, 0 )
	bytes = g.db.read( ENTRY_SIZE )
	found = (
		( ord( bytes[0] ) << 32 ) +
		( ord( bytes[1] ) << 24 ) +
		( ord( bytes[2] ) << 16 ) +
		( ord( bytes[3] ) <<  8 ) +
		( ord( bytes[4] ) )
	)

	# Search in a lower interval
	if (position < found):
		return retrieve_count(position, start, middle)

	# Search in a higher interval
	if (found < position):
		return retrieve_count(position, middle + 1, end)

	# Found it!
	logger.debug( "found result %s" % bytes[5] )
	return ord( bytes[5] )

if __name__ == "__main__":
	logger.info("Server starting")
	app.run(host="0.0.0.0", port=8000)

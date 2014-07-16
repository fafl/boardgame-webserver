# Encodes a position (8 number from 0 to 24) to be stored in the DB as 40 bit
def encode_compact_position(position):
	return \
		(position[0] * 6103515625) + \
		(position[1] * 244140625) + \
		(position[2] * 9765625) + \
		(position[3] * 390625) + \
		(position[4] * 15625) + \
		(position[5] * 625) + \
		(position[6] * 25) + \
		(position[7])

# Turns the board 180 degrees and swaps white and black pieces
def turn(position):
	return (
		(25 - position[4]) % 25,
		(25 - position[5]) % 25,
		(25 - position[6]) % 25,
		(25 - position[7]) % 25,
		(25 - position[0]) % 25,
		(25 - position[1]) % 25,
		(25 - position[2]) % 25,
		(25 - position[3]) % 25,
	)

# Returns True if one or both sides won by speed or elimination
def is_won_by_either_side(position):
	(wbr, wpa, wsc, wst, sbr, spa, ssc, sst) = position
	return (
		wbr == 21 or wbr == 22 or wbr == 23 or wbr == 24 or
		wpa == 21 or wpa == 22 or wpa == 23 or wpa == 24 or
		wsc == 21 or wsc == 22 or wsc == 23 or wsc == 24 or
		wst == 21 or wst == 22 or wst == 23 or wst == 24 or
		sbr == 1 or sbr == 2 or sbr == 3 or sbr == 4 or
		spa == 1 or spa == 2 or spa == 3 or spa == 4 or
		ssc == 1 or ssc == 2 or ssc == 3 or ssc == 4 or
		sst == 1 or sst == 2 or sst == 3 or sst == 4 or
		(wbr == 0 and wpa == 0 and wsc == 0 and wst == 0) or
		(sbr == 0 and spa == 0 and ssc == 0 and sst == 0)
	)

# Checks if this position is already mirrored by another position
# Returns false if the highest ranking white piece is on the left side of the board
def is_mirrored(position):
	if position[0] != 0:
		return position[0] % 4 == 0 or position[0] % 4 == 3
	elif position[1] != 0:
		return position[1] % 4 == 0 or position[1] % 4 == 3
	elif position[2] != 0:
		return position[2] % 4 == 0 or position[2] % 4 == 3
	elif position[3] != 0:
		return position[3] % 4 == 0 or position[3] % 4 == 3
	else:
		return False

# Mirrors all pieces of a position along the longer axis
def mirror_position(position):
	return [
		#4 * ((x-1) / 4) + 4 - ((x-1) % 4) if x != 0 else 0
		5 - x + 8 * ((x-1) / 4)) if x != 0 else 0
		for x in position
	]

def mirror_move(move):
	return (move / 8) * 8 + ((move + 4) % 8)

# Returns the first of all winning moves of a position.
# Always returns the same move if several winning moves are possible.
# Prefers to win by elimination rather than speed
# Returns -1 if no instant winning move is possible.
# Precondition: Neither side has already won
def get_first_winning_move(position):
	(wbr, wpa, wsc, wst, sbr, spa, ssc, sst) = position

	# Use wbr to eliminate ssc
	if wbr != 0 and sbr == 0 and spa == 0 and ssc != 0 and sst == 0:
		if wbr + 4 == ssc:
			return 0
		if wbr + 5 == ssc and wbr % 4 != 0:
			return 1
		if wbr + 1 == ssc and wbr % 4 != 0:
			return 2
		if wbr - 3 == ssc and wbr % 4 != 0 and 8 < wbr:
			return 3
		if wbr - 4 == ssc                  and 8 < wbr:
			return 4
		if wbr - 5 == ssc and wbr % 4 != 1 and 8 < wbr:
			return 5
		if wbr - 1 == ssc and wbr % 4 != 1:
			return 6
		if wbr + 3 == ssc and wbr % 4 != 1:
			return 7

	# Use wbr to eliminate sst
	if wbr != 0 and sbr == 0 and spa == 0 and ssc == 0 and sst != 0:
		if wbr + 4 == sst:
			return 0
		if wbr + 5 == sst and wbr % 4 != 0:
			return 1
		if wbr + 1 == sst and wbr % 4 != 0:
			return 2
		if wbr - 3 == sst and wbr % 4 != 0 and 8 < wbr:
			return 3
		if wbr - 4 == sst                  and 8 < wbr:
			return 4
		if wbr - 5 == sst and wbr % 4 != 1 and 8 < wbr:
			return 5
		if wbr - 1 == sst and wbr % 4 != 1:
			return 6
		if wbr + 3 == sst and wbr % 4 != 1:
			return 7

	# Use wpa to eliminate sbr
	if wpa != 0 and sbr != 0 and spa == 0 and ssc == 0 and sst == 0:
		if wpa + 4 == sbr:
			return 8
		if wpa + 5 == sbr and wpa % 4 != 0:
			return 9
		if wpa + 1 == sbr and wpa % 4 != 0:
			return 10
		if wpa - 3 == sbr and wpa % 4 != 0 and 8 < wpa:
			return 11
		if wpa - 4 == sbr                  and 8 < wpa:
			return 12
		if wpa - 5 == sbr and wpa % 4 != 1 and 8 < wpa:
			return 13
		if wpa - 1 == sbr and wpa % 4 != 1:
			return 14
		if wpa + 3 == sbr and wpa % 4 != 1:
			return 15

	# Use wpa to eliminate sst
	if wpa != 0 and sbr == 0 and spa == 0 and ssc == 0 and sst != 0:
		if wpa + 4 == sst:
			return 8
		if wpa + 5 == sst and wpa % 4 != 0:
			return 9
		if wpa + 1 == sst and wpa % 4 != 0:
			return 10
		if wpa - 3 == sst and wpa % 4 != 0 and 8 < wpa:
			return 11
		if wpa - 4 == sst                  and 8 < wpa:
			return 12
		if wpa - 5 == sst and wpa % 4 != 1 and 8 < wpa:
			return 13
		if wpa - 1 == sst and wpa % 4 != 1:
			return 14
		if wpa + 3 == sst and wpa % 4 != 1:
			return 15

	# Use wsc to eliminate spa
	if wsc != 0 and sbr == 0 and spa != 0 and ssc == 0 and sst == 0:
		if wsc + 4 == spa:
			return 16
		if wsc + 5 == spa and wsc % 4 != 0:
			return 17
		if wsc + 1 == spa and wsc % 4 != 0:
			return 18
		if wsc - 3 == spa and wsc % 4 != 0 and 8 < wsc:
			return 19
		if wsc - 4 == spa                  and 8 < wsc:
			return 20
		if wsc - 5 == spa and wsc % 4 != 1 and 8 < wsc:
			return 21
		if wsc - 1 == spa and wsc % 4 != 1:
			return 22
		if wsc + 3 == spa and wsc % 4 != 1:
			return 23

	# Use wst to eliminate ssc
	if wst != 0 and sbr == 0 and spa == 0 and ssc != 0 and sst == 0:
		if wst + 4 == ssc:
			return 24
		if wst + 5 == ssc and wst % 4 != 0:
			return 25
		if wst + 1 == ssc and wst % 4 != 0:
			return 26
		if wst - 3 == ssc and wst % 4 != 0 and 8 < wst:
			return 27
		if wst - 4 == ssc                  and 8 < wst:
			return 28
		if wst - 5 == ssc and wst % 4 != 1 and 8 < wst:
			return 29
		if wst - 1 == ssc and wst % 4 != 1:
			return 30
		if wst + 3 == ssc and wst % 4 != 1:
			return 31

	# wbr moves on last row
	if (wbr == 17 and sbr != 21 and spa != 21)\
	or (wbr == 18 and sbr != 22 and spa != 22)\
	or (wbr == 19 and sbr != 23 and spa != 23)\
	or (wbr == 20 and sbr != 24 and spa != 24):
		return 0
	if (wbr == 17 and sbr != 22 and spa != 22)\
	or (wbr == 18 and sbr != 23 and spa != 23)\
	or (wbr == 19 and sbr != 24 and spa != 24):
		return 1
	if (wbr == 18 and sbr != 21 and spa != 21)\
	or (wbr == 19 and sbr != 22 and spa != 22)\
	or (wbr == 20 and sbr != 23 and spa != 23):
		return 7

	# wpa moves on last row
	if (wpa == 17 and spa != 21 and ssc != 21)\
	or (wpa == 18 and spa != 22 and ssc != 22)\
	or (wpa == 19 and spa != 23 and ssc != 23)\
	or (wpa == 20 and spa != 24 and ssc != 24):
		return 8
	if (wpa == 17 and spa != 22 and ssc != 22)\
	or (wpa == 18 and spa != 23 and ssc != 23)\
	or (wpa == 19 and spa != 24 and ssc != 24):
		return 9
	if (wpa == 18 and spa != 21 and ssc != 21)\
	or (wpa == 19 and spa != 22 and ssc != 22)\
	or (wpa == 20 and spa != 23 and ssc != 23):
		return 15

	# wsc moves on last row
	if (wsc == 17 and sbr != 21 and ssc != 21 and sst != 21)\
	or (wsc == 18 and sbr != 22 and ssc != 22 and sst != 22)\
	or (wsc == 19 and sbr != 23 and ssc != 23 and sst != 23)\
	or (wsc == 20 and sbr != 24 and ssc != 24 and sst != 24):
		return 16
	if (wsc == 17 and sbr != 22 and ssc != 22 and sst != 22)\
	or (wsc == 18 and sbr != 23 and ssc != 23 and sst != 23)\
	or (wsc == 19 and sbr != 24 and ssc != 24 and sst != 24):
		return 17
	if (wsc == 18 and sbr != 21 and ssc != 21 and sst != 21)\
	or (wsc == 19 and sbr != 22 and ssc != 22 and sst != 22)\
	or (wsc == 20 and sbr != 23 and ssc != 23 and sst != 23):
		return 23

	# wst moves on last row
	if (wst == 17 and sbr != 21 and spa != 21 and sst != 21)\
	or (wst == 18 and sbr != 22 and spa != 22 and sst != 22)\
	or (wst == 19 and sbr != 23 and spa != 23 and sst != 23)\
	or (wst == 20 and sbr != 24 and spa != 24 and sst != 24):
		return 24
	if (wst == 17 and sbr != 22 and spa != 22 and sst != 22)\
	or (wst == 18 and sbr != 23 and spa != 23 and sst != 23)\
	or (wst == 19 and sbr != 24 and spa != 24 and sst != 24):
		return 25
	if (wst == 18 and sbr != 21 and spa != 21 and sst != 21)\
	or (wst == 19 and sbr != 22 and spa != 22 and sst != 22)\
	or (wst == 20 and sbr != 23 and spa != 23 and sst != 23):
		return 31

	# No winning move possible
	return -1

# If this position is lost with the enemies next move, this function returns the first possible move
# Returns -2 if the position can be won in one move
# Returns -1 if the position is not lost
def get_first_losing_move(position):
	# If this position can be won instantly, it is not lost
	if get_first_winning_move(position) != -1:
		return -2
	first_losing_move = -1
	for move in xrange(31, -1, -1):
		resulting_position = make_move(position, move)
		if resulting_position is None:
			continue
		resulting_position = turn(resulting_position)
		# If the resulting position is not immediately winnable by the
		# enemy, this position is not lost within the next two moves
		if get_first_winning_move(resulting_position) == -1:
			#print "Not lost! Can still do move %s!" % move
			return -1
		# Set first_losing move if not already set
		first_losing_move = move
	return first_losing_move

# If this position is win with three moves, this function returns the first possible move
# Returns -2 if the position is lost or can be won earlier
# Returns -1 if the position is can not be won in three moves
def get_first_winning_move_3(position):
	# If this position can be won instantly, it is not lost
	if get_first_losing_move(position) != -1:
		return -2
	for move in xrange(32):
		resulting_position = make_move(position, move)
		if resulting_position is None:
			continue
		resulting_position = turn(resulting_position)
		# If the resulting position is not immediately winnable by the
		# enemy, this position is not lost within the next two moves
		if 0 <= get_first_losing_move(resulting_position):
			#print "Not lost! Can still do move %s!" % move
			return move
		# Set first_losing move if not already set
	return -1

# Returns the resulting position of a move or None if the move is not possible
# TODO: Use "dst" instead of "wbr + 4" and stuff like that
def make_move(position, move):
	(wbr, wpa, wsc, wst, sbr, spa, ssc, sst) = position

	######################### WBR #########################

	if move == 0:
		if wbr != 0 and wbr < 21:
			dst = wbr + 4
			if not dst in (wpa, wsc, wst, sbr, spa):
				if dst == ssc:
					return (dst, wpa, wsc, wst, sbr, spa, 0, sst)
				if dst == sst:
					return (dst, wpa, wsc, wst, sbr, spa, ssc, 0)
				return (dst, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 1:
		if wbr != 0 and wbr < 21 and wbr % 4 != 0:
			dst = wbr + 5
			if not dst in (wpa, wsc, wst, sbr, spa):
				if dst == ssc:
					return (dst, wpa, wsc, wst, sbr, spa, 0, sst)
				if dst == sst:
					return (dst, wpa, wsc, wst, sbr, spa, ssc, 0)
				return (dst, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 2:
		if wbr != 0              and wbr % 4 != 0 and wbr + 1 not in (wpa, wsc, wst, sbr, spa):
			if wbr + 1 == ssc:
				return (wbr + 1, wpa, wsc, wst, sbr, spa, 0, sst)
			if wbr + 1 == sst:
				return (wbr + 1, wpa, wsc, wst, sbr, spa, ssc, 0)
			return (wbr + 1, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 3:
		if wbr != 0 and 4 < wbr  and wbr % 4 != 0 and wbr - 3 not in (wpa, wsc, wst, sbr, spa):
			if wbr - 3 == ssc:
				return (wbr - 3, wpa, wsc, wst, sbr, spa, 0, sst)
			if wbr - 3 == sst:
				return (wbr - 3, wpa, wsc, wst, sbr, spa, ssc, 0)
			return (wbr - 3, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 4:
		if wbr != 0 and 4 < wbr                   and wbr - 4 not in (wpa, wsc, wst, sbr, spa):
			if wbr - 4 == ssc:
				return (wbr - 4, wpa, wsc, wst, sbr, spa, 0, sst)
			if wbr - 4 == sst:
				return (wbr - 4, wpa, wsc, wst, sbr, spa, ssc, 0)
			return (wbr - 4, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 5:
		if wbr != 0 and 4 < wbr  and wbr % 4 != 1 and wbr - 5 not in (wpa, wsc, wst, sbr, spa):
			if wbr - 5 == ssc:
				return (wbr - 5, wpa, wsc, wst, sbr, spa, 0, sst)
			if wbr - 5 == sst:
				return (wbr - 5, wpa, wsc, wst, sbr, spa, ssc, 0)
			return (wbr - 5, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 6:
		if wbr != 0              and wbr % 4 != 1 and wbr - 1 not in (wpa, wsc, wst, sbr, spa):
			if wbr - 1 == ssc:
				return (wbr - 1, wpa, wsc, wst, sbr, spa, 0, sst)
			if wbr - 1 == sst:
				return (wbr - 1, wpa, wsc, wst, sbr, spa, ssc, 0)
			return (wbr - 1, wpa, wsc, wst, sbr, spa, ssc, sst)
	elif move == 7:
		if wbr != 0 and wbr < 21 and wbr % 4 != 1 and wbr + 3 not in (wpa, wsc, wst, sbr, spa):
			if wbr + 3 == ssc:
				return (wbr + 3, wpa, wsc, wst, sbr, spa, 0, sst)
			if wbr + 3 == sst:
				return (wbr + 3, wpa, wsc, wst, sbr, spa, ssc, 0)
			return (wbr + 3, wpa, wsc, wst, sbr, spa, ssc, sst)

	######################### WPA #########################

	elif move == 8:
		if wpa != 0 and wpa < 21                  and wpa + 4 not in (wbr, wsc, wst, spa, ssc):
			if wpa + 4 == sbr:
				return (wbr, wpa + 4, wsc, wst, 0, spa, ssc, sst)
			if wpa + 4 == sst:
				return (wbr, wpa + 4, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa + 4, wsc, wst, sbr, spa, ssc, sst)
	elif move == 9:
		if wpa != 0 and wpa < 21 and wpa % 4 != 0 and wpa + 5 not in (wbr, wsc, wst, spa, ssc):
			if wpa + 5 == sbr:
				return (wbr, wpa + 5, wsc, wst, 0, spa, ssc, sst)
			if wpa + 5 == sst:
				return (wbr, wpa + 5, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa + 5, wsc, wst, sbr, spa, ssc, sst)
	elif move == 10:
		if wpa != 0              and wpa % 4 != 0 and wpa + 1 not in (wbr, wsc, wst, spa, ssc):
			if wpa + 1 == sbr:
				return (wbr, wpa + 1, wsc, wst, 0, spa, ssc, sst)
			if wpa + 1 == sst:
				return (wbr, wpa + 1, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa + 1, wsc, wst, sbr, spa, ssc, sst)
	elif move == 11:
		if wpa != 0 and 4 < wpa  and wpa % 4 != 0 and wpa - 3 not in (wbr, wsc, wst, spa, ssc):
			if wpa - 3 == sbr:
				return (wbr, wpa - 3, wsc, wst, 0, spa, ssc, sst)
			if wpa - 3 == sst:
				return (wbr, wpa - 3, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa - 3, wsc, wst, sbr, spa, ssc, sst)
	elif move == 12:
		if wpa != 0 and 4 < wpa                   and wpa - 4 not in (wbr, wsc, wst, spa, ssc):
			if wpa - 4 == sbr:
				return (wbr, wpa - 4, wsc, wst, 0, spa, ssc, sst)
			if wpa - 4 == sst:
				return (wbr, wpa - 4, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa - 4, wsc, wst, sbr, spa, ssc, sst)
	elif move == 13:
		if wpa != 0 and 4 < wpa  and wpa % 4 != 1 and wpa - 5 not in (wbr, wsc, wst, spa, ssc):
			if wpa - 5 == sbr:
				return (wbr, wpa - 5, wsc, wst, 0, spa, ssc, sst)
			if wpa - 5 == sst:
				return (wbr, wpa - 5, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa - 5, wsc, wst, sbr, spa, ssc, sst)
	elif move == 14:
		if wpa != 0              and wpa % 4 != 1 and wpa - 1 not in (wbr, wsc, wst, spa, ssc):
			if wpa - 1 == sbr:
				return (wbr, wpa - 1, wsc, wst, 0, spa, ssc, sst)
			if wpa - 1 == sst:
				return (wbr, wpa - 1, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa - 1, wsc, wst, sbr, spa, ssc, sst)
	elif move == 15:
		if wpa != 0 and wpa < 21 and wpa % 4 != 1 and wpa + 3 not in (wbr, wsc, wst, spa, ssc):
			if wpa + 3 == sbr:
				return (wbr, wpa + 3, wsc, wst, 0, spa, ssc, sst)
			if wpa + 3 == sst:
				return (wbr, wpa + 3, wsc, wst, sbr, spa, ssc, 0)
			return (wbr, wpa + 3, wsc, wst, sbr, spa, ssc, sst)

	######################### WSC #########################

	elif move == 16:
		if wsc != 0 and wsc < 21                  and wsc + 4 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc + 4 == spa:
				return (wbr, wpa, wsc + 4, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc + 4, wst, sbr, spa, ssc, sst)
	elif move == 17:
		if wsc != 0 and wsc < 21 and wsc % 4 != 0 and wsc + 5 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc + 5 == spa:
				return (wbr, wpa, wsc + 5, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc + 5, wst, sbr, spa, ssc, sst)
	elif move == 18:
		if wsc != 0              and wsc % 4 != 0 and wsc + 1 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc + 1 == spa:
				return (wbr, wpa, wsc + 1, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc + 1, wst, sbr, spa, ssc, sst)
	elif move == 19:
		if wsc != 0 and 4 < wsc  and wsc % 4 != 0 and wsc - 3 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc - 3 == spa:
				return (wbr, wpa, wsc - 3, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc - 3, wst, sbr, spa, ssc, sst)
	elif move == 20:
		if wsc != 0 and 4 < wsc                   and wsc - 4 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc - 4 == spa:
				return (wbr, wpa, wsc - 4, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc - 4, wst, sbr, spa, ssc, sst)
	elif move == 21:
		if wsc != 0 and 4 < wsc  and wsc % 4 != 1 and wsc - 5 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc - 5 == spa:
				return (wbr, wpa, wsc - 5, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc - 5, wst, sbr, spa, ssc, sst)
	elif move == 22:
		if wsc != 0              and wsc % 4 != 1 and wsc - 1 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc - 1 == spa:
				return (wbr, wpa, wsc - 1, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc - 1, wst, sbr, spa, ssc, sst)
	elif move == 23:
		if wsc != 0 and wsc < 21 and wsc % 4 != 1 and wsc + 3 not in (wbr, wpa, wst, sbr, ssc, sst):
			if wsc + 3 == spa:
				return (wbr, wpa, wsc + 3, wst, sbr, 0, ssc, sst)
			return (wbr, wpa, wsc + 3, wst, sbr, spa, ssc, sst)

	######################### WST #########################

	elif move == 24:
		if wst != 0 and wst < 21                  and wst + 4 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst + 4 == ssc:
				return (wbr, wpa, wsc, wst + 4, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst + 4, sbr, spa, ssc, sst)
	elif move == 25:
		if wst != 0 and wst < 21 and wst % 4 != 0 and wst + 5 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst + 5 == ssc:
				return (wbr, wpa, wsc, wst + 5, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst + 5, sbr, spa, ssc, sst)
	elif move == 26:
		if wst != 0              and wst % 4 != 0 and wst + 1 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst + 1 == ssc:
				return (wbr, wpa, wsc, wst + 1, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst + 1, sbr, spa, ssc, sst)
	elif move == 27:
		if wst != 0 and 4 < wst  and wst % 4 != 0 and wst - 3 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst - 3 == ssc:
				return (wbr, wpa, wsc, wst - 3, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst - 3, sbr, spa, ssc, sst)
	elif move == 28:
		if wst != 0 and 4 < wst                   and wst - 4 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst - 4 == ssc:
				return (wbr, wpa, wsc, wst - 4, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst - 4, sbr, spa, ssc, sst)
	elif move == 29:
		if wst != 0 and 4 < wst  and wst % 4 != 1 and wst - 5 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst - 5 == ssc:
				return (wbr, wpa, wsc, wst - 5, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst - 5, sbr, spa, ssc, sst)
	elif move == 30:
		if wst != 0              and wst % 4 != 1 and wst - 1 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst - 1 == ssc:
				return (wbr, wpa, wsc, wst - 1, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst - 1, sbr, spa, ssc, sst)
	elif move == 31:
		if wst != 0 and wst < 21 and wst % 4 != 1 and wst + 3 not in (wbr, wpa, wsc, sbr, spa, sst):
			if wst + 3 == ssc:
				return (wbr, wpa, wsc, wst + 3, sbr, spa, 0, sst)
			return (wbr, wpa, wsc, wst + 3, sbr, spa, ssc, sst)

	return None
# level02 - vertical blocks
for x in range(X_THIRD, X_2THIRD, BLOCK_HEIGHT*4) :
	for y in range(1, 4) :
		thisLevel.append(Block(x, y*Y_THIRD, PowerUps.PWR_NONE, Tilt.VERT)) 
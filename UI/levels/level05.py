# level05 PLACEHOLDER - horizontal blocks
for x in range(1, 4) :
	for y in range(Y_THIRD, Y_2THIRD, BLOCK_HEIGHT*4) :
		thisLevel.append(Block(x*X_THIRD, y, PowerUps.PWR_NONE, Tilt.HORZ))
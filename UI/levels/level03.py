# level03 - alternating horizontal and vertical blocks
for x in range(1, 4) :
    for y in range(Y_THIRD, Y_2THIRD, BLOCK_HEIGHT*4) :
        if y % 2 != 0 :
            thisLevel.append(Block(x*X_THIRD, y, PowerUps.PWR_NONE, Tilt.HORZ))
for x in range(X_THIRD, X_2THIRD, BLOCK_HEIGHT*4) :
    for y in range(1, 4) :
        if y % 2 = 0 :
            thisLevel.append(Block(x, y*Y_THIRD, PowerUps.PWR_NONE, Tilt.VERT)) 
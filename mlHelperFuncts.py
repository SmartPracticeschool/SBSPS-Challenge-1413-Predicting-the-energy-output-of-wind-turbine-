
def transform(speed, direction):

    MEAN_SPEED  = 8.761232
    STD_SPEED = 3.777679
    MEAN_DIRECTION = 115.594063
    STD_DIRECTION = 86.289155
    MEAN_POWER = 1662.363380
    STD_POWER = 1264.971258
    speed = (speed - MEAN_SPEED) / STD_SPEED
    direction = (direction - MEAN_DIRECTION) / STD_DIRECTION
    return [speed, direction]

def inverse(power):
    MEAN_SPEED  = 8.761232
    STD_SPEED = 3.777679
    MEAN_DIRECTION = 115.594063
    STD_DIRECTION = 86.289155
    MEAN_POWER = 1662.363380
    STD_POWER = 1264.971258
    power = power * STD_POWER + MEAN_POWER
    return power
    
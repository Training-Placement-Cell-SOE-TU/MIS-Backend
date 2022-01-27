import random, math

def otp_generator(length:int):
    otp = 0
    for i in range(length):
        otp += math.floor(random.random() * 10) * math.pow(10,i)

    return int(otp)


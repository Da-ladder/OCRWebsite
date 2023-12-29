import random as rng

primary = ["red","yellow","blue"]

def randomShit():
    randInt1 = rng.randint(0,2)
    randInt2 = rng.randint(0,2)
    if(primary[randInt1] == "red") and (primary[randInt2] == "yellow"):
        print("Your color is Orange")
    elif(primary[randInt1] == "red") and (primary[randInt2] == "blue"):
        print("Your color is Purple")
    elif(primary[randInt1] == "yellow") and (primary[randInt2] == "blue"):
        print("Your color is Green")
    elif(primary[randInt1] == "red") and (primary[randInt2] == "red"):
        print("Your color is Red")
    elif(primary[randInt1] == "blue") and (primary[randInt2] == "blue"):
        print("Your color is Blue")
    elif(primary[randInt1] == "yellow") and (primary[randInt2] == "yellow"):
        print("Your color is Yellow")
    

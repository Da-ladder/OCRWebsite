import random as rng

primary = ["red","yellow","blue"]

def randomShit():
    randInt1 = rng.randint(0,2)
    randInt2 = rng.randint(0,2)
    stringCont = primary[randInt1] + primary[randInt2]
    match stringCont:
        case "redred":
            print("Your color is red")
        case "redyellow":
            print("Your color is orange")
        case "yellowred":
            print("Your color is orange")
        case "yellowyellow":
            print("Your color is yellow")
        case "yellowblue":
            print("Your color is green")
        case "blueyellow":
            print("Your color is green")
        case "blueblue":
            print("Your color is blue")
        case "bluered":
            print("Your color is purple")
        case "redblue":
            print("Your color is purple")
    

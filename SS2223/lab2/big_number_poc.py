import requests

SERVER = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:22052'

# Start session
session = requests.session()
r = session.get(SERVER)

def guess_number(guess):
    r = session.get(SERVER + "/number/" + str(guess))
    return r

def get_big_number():
    guess = 50000
    max = 100000
    min = 1
    
    # Divide and conquer (Binary search)
    while True:
        r = guess_number(guess)
        if r.text.find("Higher") != -1:
            min = guess
            guess = (max + guess)//2
        elif r.text.find("Lower") != -1:
            max = guess
            guess = (min + guess)//2
        else:
            break

    print("The flag is: " + r.text + '\n' + "The number was: " + str(guess))

get_big_number()

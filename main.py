#This program will pit the computer against the computer, trying to guess a secret number

import random
import time
import re
import statistics



#A
allTimeGuesses = 0

#C
computerHints = []

#G
gamesPlayed = 0
# UP or DOWN
guessTrendDirection = "UP"
guessMin = 1
guessMax = 200
guessOutcomes = {}

#L
lastPlayerGuess = 0
lastGuessMin = 0
lastGuessMax = 0
lastGuessWidth = 0

#M
maxRandomNumber = 0

#O
oponentStatements = []

#P
playerIQ = 0
playerGuess = -1
previousGuesses = []

#R
reusedGuessesInt = 0

#S
secretNumber = 0
suspectedNumber = 0
smartAIOn = True
suspectVeryCold = []
suspectCold = []
suspectWarm = []
suspectVeryWarm = []

#T
thisGameTotalGuesses = 0
turnNumber = 0

def playerInternalDialog(newThought):
    global thoughts
    thoughts.append(newThought)

def suggestUpperLimit():
    #provides a smart guessMax
    global guessMax
    global guessMin
    global lastGuessMax
    global lastGuessMin
    global lastPlayerGuess

    newGame = False


    if (len(oponentStatements)<= 0 or turnNumber == 1):
        newGame = True



    if newGame == True :
        #it's a brand new game'
        guessMax = maxRandomNumber
        guessMax = ((maxRandomNumber // 4) * 3) + 2
    if turnNumber == 2:
        guessMax = ((maxRandomNumber // 2))
    print("PLAYER - I need a hint for upper")

def findSuspectedNumber():
    global suspectedNumber
    global previousGuesses
    global oponentStatements
    global guessOutcomes
    global suspectVeryCold
    global suspectCold
    global suspectWarm
    global suspectVeryWarm


    suspectVeryWarm = []
    suspectWarm = []
    suspectVeryCold = []
    susepctCold = []

    guessCount = 0

    #how many guesses have we made?
    guessCount = len(previousGuesses)

    #what range does VERY COLD make up
    #what range does COLD make up
    #what range does WARM make up
    #what range does VERY WARM make up

    #should we have a conflict if we secretly guess the number is SOMETHING WE'VE ALREADY GUESSED.....??
    #yeah, probably

    if len(guessOutcomes) > 0:
        for guess in guessOutcomes.keys():
            #print(guessOutcomes[guess])
            if guessOutcomes[guess].lower().find("very warm") > 0:
                # this is a very warm value
                suspectVeryWarm.append(guess)
                #print("Very warm number added - " + str(guess))
            elif guessOutcomes[guess].lower().find("warm") > 0:
                # this is a very warm value
                suspectWarm.append(guess)
                #print("Warm number added - " + str(guess))
            elif guessOutcomes[guess].lower().find("very cold") > 0:
                # this is a very cold value
                suspectVeryCold.append(guess)
                #print("Verycold number added - " + str(guess))
            elif guessOutcomes[guess].lower().find("cold") > 0:
                # this is a cold value
                suspectCold.append(guess)
                #print("Cold number added - " + str(guess))
            else:
                # print("I'm having an error showing outcomes")
                a = 1
        if len(suspectVeryWarm) > 2:
            # suspect number is middle of VERY WARM RANGE
            suspectedNumber = statistics.mean(suspectVeryWarm) // 1
            if suspectedNumber in suspectVeryWarm:
                suspectedNumber = suspectedNumber + 1
        elif len(suspectWarm) > 2:
            suspectedNumber = statistics.mean(suspectWarm) // 1
            suspectedNumber = suspectedNumber + 1

        else:
           suspectedNumber = lastPlayerGuess

    print("PLAYER - I secretly suspect the number is:" + str(suspectedNumber))
    #suspectVeryWarm.sort()
    #print(suspectVeryWarm)


def suggestLowerLimit():
    #provides a smart guessMin
    global guessMax
    global guessMin
    global lastGuessMax
    global lastGuessMin
    global lastPlayerGuess

    newGame = False

    if len(oponentStatements)<= 0:
        newGame = True

    if newGame == True :
        #it's a brand new game'
        guessMin = ((maxRandomNumber // 4) * 3 ) + 1

    if turnNumber == 2:
        guessMin = 1

    print("PLAYER - I need a hint for lower")

def smartAI():
    # Improves the guessing ability
    global previousGuesses
    global maxRandomNumber
    global playerGuess
    global computerHints
    global suspectedNumber
    global playerIQ
    global currentGuessOff
    global playerGuess
    global lastPlayerGuess
    global guessTrendDirection
    global turnNumber
    global oponentStatements
    global lastGuessMin
    global lastGuessMax
    global guessMin
    global guessMax
    global lastGuessWidth
    global newThought
    global thoughts
    global suspectedNumber
    global guessOutcomes

    needSuggestionLower = False
    needSuggestionUpper = False
    veryCold = 0
    veryWarm = 0
    cold = 0
    warm = 0


    guessMin = 1
    guessMax = maxRandomNumber
    guessWidth = lastGuessMax - lastGuessMin
    if guessWidth > lastGuessWidth:
        guessWidthTrend = "WIDE"
    else:
        guessWidthTrend = "NARROW"
    minModifier = 1
    maxModifier = 1
    guessQualityTrend = ""
    newThought = ""

    if len(oponentStatements) >= 1:
        mostRecentStatement = oponentStatements[(len(oponentStatements) - 1)]
        previousOpponentStatement = oponentStatements[(len(oponentStatements) - 2)]
        # if most recent is worse than previous, we went the wrong way
        if playerGuess > lastPlayerGuess:
            guessTrendDirection = "UP"
        else:
            guessTrendDirection = "DOWN"

        if (mostRecentStatement.lower().find("warm") and previousOpponentStatement.lower().find("warm")):
            guessQualityTrend = "BETTER"
        elif (mostRecentStatement.lower().find("cold") and previousOpponentStatement.lower().find("warm")):
            guessQualityTrend = "WORSE"
        elif (mostRecentStatement.lower().find("cold") and previousOpponentStatement.lower().find("cold")):
            guessQualityTrend = "WORSE"
        else:
            guessQualityTrend = "BETTER"

        if guessQualityTrend == "BETTER":
            if guessWidthTrend == "NARROW":
                minModifier = minModifier + 1
                maxModifier = maxModifier - 1
            else:
                minModifier = minModifier + 10
                maxModifier = maxModifier - 10

            if guessTrendDirection == "UP":
                minModifier = minModifier + 10
                maxModifier = maxModifier + 10
            else:
                minModifier = maxModifier
                maxModifier = maxModifier

        elif guessQualityTrend == "WORSE":
            minModifier = minModifier + 20
            maxModifier = maxModifier - 20

        else:
            minModifier = minModifier - 10
            maxModifier = maxModifier + 10

        #print(mostRecentStatement)
        if (len(oponentStatements) <= 3): #first three guessess use suggestLower() and suggestUpper()
            print("PLAYER - Okay, here we go!")
            newThought = "It's a new game."
            needSuggestionUpper = True
            needSuggestionLower = True
            playerGuess = random.randint(guessMin, guessMax) #
        elif (mostRecentStatement.lower().find("very warm") > 0 and len(oponentStatements) >= 3): # guess is great
            if previousOpponentStatement.lower().find("very warm") > 0:
                #last two guessess were very warm
                if (oponentStatements[(len(oponentStatements) - 4)].lower().find("very warm") > 0):
                    #last three guesses were very warm
                    # which way have we been guessing?
                    if suspectedNumber not in previousGuesses:
                        print("PLAYER - I THINK I KNOW THE ANSWER!!!")
                        guessMin = suspectedNumber
                        guessMax = suspectedNumber
                    elif previousGuesses[len(previousGuesses) - 2] > previousGuesses[len(previousGuesses) - 1]:
                        #we're going up - keep going down
                        print("PLAYER - Going down!")
                        guessMin = lastPlayerGuess - abs(lastPlayerGuess - previousGuesses[len(previousGuesses) - 2]) - 2
                        guessMax = lastPlayerGuess - 1
                    elif previousGuesses[len(previousGuesses) - 2] < previousGuesses[len(previousGuesses) - 1]:
                        #we're going up!
                        print("PLAYER - Going up!.")
                        guessMin = lastPlayerGuess + 1
                        guessMax = lastPlayerGuess + 5
                    elif previousGuesses[len(previousGuesses) - 2] == previousGuesses[len(previousGuesses) - 1]:
                        # we're trying the same number
                        print("PLAYER - I'm an idiot and guessed the same number.")
                        guessMin = lastPlayerGuess + 5
                        guessMax = lastPlayerGuess + 10
                    elif previousGuesses[len(previousGuesses) - 3] > previousGuesses[len(previousGuesses) - 1]:
                        print("PLAYER - I'm stuck!")
                        guessMin = previousGuesses[len(previousGuesses) - 2]
                        guessMax = previousGuesses[len(previousGuesses) -1]
                    else:
                        print("PLAYER - This game is hard")
                        guessMin = (maxRandomNumber - lastPlayerGuess) - lastPlayerGuess
                        guessMax = (maxRandomNumber - lastPlayerGuess) + lastPlayerGuess
                        # we are stuck
                elif(oponentStatements[(len(oponentStatements) - 3)].lower().find("very warm") > 0):
                    print ("PLAYER - I'm on a roll!!")
                    guessMin = lastGuessMin - 10
                    guessMax = lastGuessMax + 10
                else:
                    # player guess very well
                    print("PLAYER - I am great!")
                    guessMin = lastPlayerGuess - 1
                    guessMax = lastPlayerGuess + 1
            elif previousOpponentStatement.lower().find("warm") > 0:
                print("PLAYER - I have an idea. It's close.")
                guessMin = previousGuesses[len(previousGuesses) - 1] - abs(previousGuesses[len(previousGuesses) - 2] - previousGuesses[len(previousGuesses) - 1])
                guessMax = previousGuesses[len(previousGuesses) - 1] + abs(previousGuesses[len(previousGuesses) - 2] - previousGuesses[len(previousGuesses) - 1])
            elif previousOpponentStatement.lower().find("cold") > 0:
                print("PLAYER - I knew it, so close.")
                guessMin = lastPlayerGuess - 5
                guessMax = lastPlayerGuess + 5
            else:
                print("Player - I am good!")
                guessMin = lastPlayerGuess - 10
                guessMax = lastPlayerGuess + 10
        elif mostRecentStatement.lower().find("very cold") > 0:  # guess is very bad
            if previousOpponentStatement.lower().find("very cold") > 0:
                # two very good guesses in a row. Player needs help

                if lastPlayerGuess > (maxRandomNumber - lastPlayerGuess):
                    print("PLAYER - I'm going to guess lower this time.")
                    guessMin = (lastPlayerGuess // 2) - lastGuessMin
                    guessMax = lastGuessMin
                elif lastPlayerGuess < (maxRandomNumber - lastPlayerGuess):
                    print("PLAYER - I'm going to guess higher this time.")
                    guessMin = maxRandomNumber - lastPlayerGuess
                    guessMax = maxRandomNumber
            elif previousOpponentStatement.lower().find("cold") > 0:
                #we went the wrong way, turn back
                print("PLAYER - I went the wrong way.")
                guessMin = lastGuessMax + (maxRandomNumber // previousGuesses[len(previousGuesses) - 2] - previousGuesses[len(previousGuesses) - 1])
                guessMax = lastGuessMin + 20
            else:
                print("PLAYER - I am the horrible")
                if (maxRandomNumber - lastPlayerGuess < lastPlayerGuess):
                    guessMin = lastGuessMin
                    guessMax = lastPlayerGuess - 10
                else:
                    print("PLAYER - I am mostly horrible")
                    guessMin = lastPlayerGuess + 10
                    guessMax = lastGuessMax
        elif mostRecentStatement.lower().find("cold") > 0:  # guess is very bad
            if (oponentStatements[(len(previousGuesses)-1)]).lower().find("warm") > 0:
                print("PLAYER - Crap, I went the wrong way.")
                # lastGuessMin & lastGuessMax should influence our decension here
                guessMin = previousGuesses[len(previousGuesses) -1] - abs(lastGuessMin)
                guessMax = previousGuesses[len(previousGuesses) -1] + abs(maxRandomNumber - lastGuessMax)
            elif(oponentStatements[(len(previousGuesses)-1)]).lower().find("very warm") > 0:
                print("PLAYER - Crap, I REALLY went the wrong way.")
                # lastGuessMin & lastGuessMax should influence our decension here
                guessMin = previousGuesses[len(previousGuesses) - 1] - abs(lastGuessMin)
                guessMax = previousGuesses[len(previousGuesses) - 1] + abs(maxRandomNumber - lastGuessMax)
            elif (oponentStatements[(len(previousGuesses) - 1)]).lower().find("very cold") > 0:

                #the very cold value is something we want to avoid
                veryCold = previousGuesses[len(previousGuesses) - 2]
                cold = lastPlayerGuess
                if cold - veryCold > veryCold - cold:
                    print("PLAYER - Weird, I'm doing better.")
                    guessMin = lastPlayerGuess + 1
                    guessMax = lastPlayerGuess + ((maxRandomNumber - lastPlayerGuess) // 4)
                else:
                    print("PLAYER - Sooo, I'm doing better.")
                    guessMin = lastPlayerGuess - ((lastPlayerGuess) // 4)
                    guessMax = lastPlayerGuess - 1
            else:
                print("PLAYER - uh shit")
                #if we're guessing low, go high
                guessMin = lastPlayerGuess + lastGuessMin
                guessMax = lastPlayerGuess + lastGuessMax
        elif mostRecentStatement.lower().find("warm") > 0:  # guess is okay
            # we're in the ball park
            # previousGuesses[len(previousGuesses) - 1]
            #oponentStatements[(len(oponentStatements) - 4)].lower().find("very warm")
            if oponentStatements[(len(oponentStatements) - 2)].lower().find("very warm") > 0:
                #we went the wrong way, turn back
                print("PLAYER - Warm, but I went the wrong way.")
                guessMin = previousGuesses[len(previousGuesses) - 1] - (previousGuesses[len(previousGuesses) - 1] - previousGuesses[len(previousGuesses) - 2])
                guessMax = previousGuesses[len(previousGuesses) - 1] + 1
            elif oponentStatements[(len(oponentStatements) - 2)].lower().find("warm") > 0:
                #we're flailing in the dark around a possible number
                #try to guess COLD
                print("PLAYER - I'm testing a theory, my next guess will be COLD.")
                #The last two guesses are warm
                #previousGuesses[len(previousGuesses) - 2]
                #previousGuesses[len(previousGuesses) - 1]
                if previousGuesses[len(previousGuesses) - 1] > previousGuesses[len(previousGuesses) - 2]:
                    guessMin = previousGuesses[len(previousGuesses) - 2] - abs(maxRandomNumber - previousGuesses[len(previousGuesses) - 2])
                    guessMax = previousGuesses[len(previousGuesses) - 1]
                else:
                    guessMin = previousGuesses[len(previousGuesses) - 1] - abs(maxRandomNumber - previousGuesses[len(previousGuesses) - 2])
                    guessMax = previousGuesses[len(previousGuesses) - 2]
            elif oponentStatements[(len(oponentStatements) - 2)].lower().find("cold") > 0:
                print("PLAYER - I'm so confused.")
                guessMin = lastPlayerGuess + 10
                guessMax = lastPlayerGuess + 30
            elif oponentStatements[(len(oponentStatements) - 2)].lower().find("very cold") > 0:

                #what changed?
                veryCold = previousGuesses[len(previousGuesses) - 2]
                warm = previousGuesses[len(previousGuesses) - 1]
                if warm > veryCold:
                    print("PLAYER - I'm on the right track, up.")
                    # we got closer by guessing higher
                    guessMin = lastPlayerGuess + 1
                    guestMax = lastGuessMax + 1
                else:
                    print("PLAYER - I'm on the right track, down.")
                    # we got closer by guessing lower
                    guessMin = abs(lastPlayerGuess - lastGuessMin)
                    guestMax = lastPlayerGuess - 1

                guessMin = random.randint(1,(maxRandomNumber // 2))
                guessMax = maxRandomNumber
            else:
                print("PLAYER - Crap.")
                guessMin = lastPlayerGuess - 20
                guessMax = lastPlayerGuess + 20
        else:
            print ("PLAYER - This is too hard.")
    else: # first round of a game!!!
        needSuggestionLower = True
        needSuggestionUpper = True



    playerInternalDialog(newThought)
    if needSuggestionUpper:
        suggestUpperLimit()
    if needSuggestionLower:
        suggestLowerLimit()

    #make sure we're not guessing an illegal number
    if guessMin > guessMax:
        guessMinHolder = guessMin
        guessMaxHolder = guessMax
        guessMin = guessMaxHolder
        guessMax = guessMinHolder

    if guessMin <= 0 or guessMin > guessMax:
        guessMin = 1
        guessMax = maxRandomNumber
    if guessMax <= 0 or guessMax > maxRandomNumber:
        guessMin = 1
        guessMax = maxRandomNumber




    # finally, make our guess
    playerGuess = random.randint(guessMin, guessMax)
    previousGuesses.append(playerGuess)
    lastPlayerGuess = playerGuess
    lastGuessMax = guessMax
    lastGuessMin = guessMin
    lastGuessWidth = guessWidth


# COMPUTER opponent compares the player guess and gives feed back
def oponentReply():
    global currentGuessOff
    global playerGuess
    global secretNumber
    global lastGuessOff
    global thisGameTotalGuesses
    global oponentStatements
    global guessOutcomes

    oponentStatement = ""
    # Compare guess to secretNumber
    if (playerGuess == secretNumber):
        openentStatement = "COMPUTER - I AM SAD, YOU HAVE GUESSED MY SECRET NUMBER. COMPUTER - IT TOOK YOU " + str(thisGameTotalGuesses) + " ATTEMPTS, WHICH IS LAUGHABLE."
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 50):
        openentStatement = "COMPUTER - VERY COLD, GUESS AGAIN"
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 25):
        openentStatement = "COMPUTER - COLD, GUESS AGAIN"
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 10):
        openentStatement = "COMPUTER - WARM, GUESS AGAIN"
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 0):
        # a very good guess, stay at it
        openentStatement = "COMPUTER - VERY WARM, GUESS AGAIN"
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    else:
        openentStatement = "Something went wrong"
    # print("[secret=" + str(secretNumber) + "]")
    print(openentStatement)
    newOutcome = {playerGuess: openentStatement}
    #print(newOutcome)
    if playerGuess in guessOutcomes:
        guessOutcomes.update(newOutcome)
    else:
        guessOutcomes.update(newOutcome)
    #guessOutcomes

def newGuess():
    global allTimeGuesses
    global reusedGuessesInt
    global maxRandomNumber
    global playerIQ
    global previousGuesses
    global playerGuess
    global reusedGuesses
    global secretNumber
    global reusedGuessesInt
    global thisGameTotalGuesses
    global currentGuessOff
    global guessMin
    global guessMax

    if smartAIOn == True:
        smartAI() # this returns a guess
    else:
        playerGuess = random.randint(guessMin, guessMax)

    thisGameTotalGuesses = thisGameTotalGuesses + 1
    #time.sleep(.900)


def generateGame():
    global secretNumber
    global playerIQ
    global maxRandomNumber
    global previousGuesses
    global reusedGuessesInt
    global oponentStatements
    global previousGuesses
    global thoughts
    global suspectedNumber
    global guessOutcomes
    # clean up re-used globals
    thoughts = []
    guessOutcomes = {}
    oponentStatements = []
    previousGuesses = []
    suspectedNumber = 1

    reusedGuessesInt = 0


    maxRandomNumber = random.randint(1,100) + 100
    secretNumber = random.randint(1,maxRandomNumber)
    playerIQ = random.randint(1,10)

    #decide what type of opponent we have
    #loose
    #specific
    #

def playGame():
    #globals
    global playerGuess
    global secretNumber
    global gamesPlayed
    global allTimeGuesses
    global maxRandomNumber
    global reusedGuessesInt
    global currentGuessOff
    global previousGuesses
    global thisGameTotalGuesses
    global turnNumber

    thisGameTotalGuesses = 0
    turnNumber = 0
    #locals
    guessMin = 1
    guessMax = maxRandomNumber
    lastGuessOff = 0
    currentGuessType = "wild"

    print("")
    print("---------------[GAME "+ str(gamesPlayed) + "]---------------")
    print("")
    print("Guess a number between 1 and " + str(maxRandomNumber))

    #start the guessing game
    if playerGuess == -1:
        print("COMPUTER - PLEASE GUESS A NUMBER BETWEEN 1 AND " + str(maxRandomNumber))

    #Guess a new number
    while playerGuess != secretNumber:
        # Each iteration of this loop is a new turn
        turnNumber = turnNumber + 1
        print("[TURN "+str(turnNumber)+"- SECRET:"+str(secretNumber)+"]")
        # decide what type of guess we're going to make
        # wild - guess any damn number
        # educated guess within X of last number
        # specific - guess a specific number because it's right

        newGuess()
        playerReply()
        findSuspectedNumber()
        currentGuessOff = abs(secretNumber - playerGuess)
        if playerGuess == secretNumber: # player has guessed the answer
            gamesPlayed = gamesPlayed + 1
            allTimeGuesses = allTimeGuesses + thisGameTotalGuesses
            oponentReply()
            break
        else: # Guess was wrong, continue guessing
            oponentReply()




    #player guesses a unique number

def playerReply():
    global playerGuess
    global guessMin
    global guessMax

    print("PLAYER - ["+str(guessMin) +"-"+str(guessMax) +"]... I GUESS: " + str(playerGuess))



while gamesPlayed < 5:

    generateGame()
    playGame()

print("The computer played a total of " + str(gamesPlayed) + " games.")
print("You made " + str(allTimeGuesses) + " guesses.")
print("You averaged " + str (allTimeGuesses / gamesPlayed) + " guesses per game.")
print("The computer is dumb and made repetative guesses " + str(reusedGuessesInt) + " times.")

#for statement in guessOutcomes.items():
#    print(statement)
#This program will pit the computer against the computer, trying to guess a secret number

import random
import time
import re
import statistics

# A
allTimeGuesses = 0

# C
computerHints = []

# G
gamesPlayed = 0
# UP or DOWN
guessTrendDirection = "UP"
guessMin = 1
guessMax = 200
guessOutcomes = {}

# L
lastPlayerGuess = 0
lastGuessMin = 0
lastGuessMax = 0
lastGuessWidth = 0

# M
maxRandomNumber = 0

# O
oponentStatements = []

# P
playerIQ = 0
playerGuess = -1


#R
reusedGuessesInt = 0

# S
secretNumber = 0
suspectedNumber = 0
smartAIOn = True
suspectVeryCold = []
suspectCold = []
suspectWarm = []
suspectVeryWarm = []

# T
thisGameTotalGuesses = 0


class GameWorld:
    games_per_session = 5
    turn_number = 0
    last_player_guess = 0
    secret_number = 0
    total_games = 0

class PlayerTwo:
    total_guesses = 0
    suspected_number = 0
    suspected_confidence = 0
    suspected_upper = 0
    suspected_lower = 0
    very_warm_guess = []
    very_cold_guess = []
    warm_guess = []
    cold_guess = []
    guessed_numbers = []

def playerInternalDialog(newThought):
    global thoughts
    thoughts.append(newThought)

def suggestUpperLimit():
    # provides a smart guessMax
    global maxRandomNumber
    global guessMax
    global guessMin

    if GameWorld.turn_number < 1:
        guessMax = maxRandomNumber
        guessMin = ((maxRandomNumber // 4) * 3) + 2
    elif GameWorld.turn_number == 2:
        guessMax = maxRandomNumber // 2
    else:
        guessMax = (maxRandomNumber // 4)*2

    PlayerTwo.suspected_confidence = 1
    print("PLAYER - I need a hint for upper")

def suggestLowerLimit():
    # provides a smart guessMin
    global guessMax
    global guessMin

    if GameWorld.turn_number < 1:
        guessMin = ((maxRandomNumber // 4) * 3) + 1
    elif GameWorld.turn_number == 2:
        guessMin = 1
    else:
        guessMin = maxRandomNumber // 4

    PlayerTwo.suspected_confidence = 1
    print("PLAYER - I need a hint for lower")


def findSuspectedNumber():
    global suspectedNumber
    global oponentStatements
    global guessOutcomes
    global suspectVeryCold
    global suspectCold
    global suspectWarm
    global suspectVeryWarm


    suspectVeryWarm = []
    suspectWarm = []
    suspectVeryCold = []
    suspectCold = []

    # how many guesses have we made?
    guessCount = len(PlayerTwo.guessed_numbers)

    # what range does VERY COLD make up
    # what range does COLD make up
    # what range does WARM make up
    # what range does VERY WARM make up

    # should we have a conflict if we secretly guess the number is SOMETHING WE'VE ALREADY GUESSED.....??
    # yeah, probably

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

    # finally, make our guess
    # but don't guess something we're already guessed
    if suspectedNumber in PlayerTwo.guessed_numbers:
        suspectedNumber = random.randint(guessMin, guessMax)

    print("PLAYER - [C:" + str(PlayerTwo.suspected_confidence) + "] I secretly suspect the number is:" + str(suspectedNumber))

def smartAI():
    # Improves the guessing ability

    global maxRandomNumber
    global playerGuess
    global computerHints
    global suspectedNumber
    global playerIQ
    global currentGuessOff
    global playerGuess
    global lastPlayerGuess
    global guessTrendDirection
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

    guessed_numbers = PlayerTwo.guessed_numbers

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

        print("Player has guessed: " + str(len(PlayerTwo.guessed_numbers)) + " and opponent replied " + str(
            len(oponentStatements)))

        print(str(PlayerTwo.guessed_numbers)[1:-1])

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
                    if suspectedNumber not in PlayerTwo.guessed_numbers:
                        print("PLAYER - I THINK I KNOW THE ANSWER!!!")
                        guessMin = suspectedNumber
                        guessMax = suspectedNumber
                    elif PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] > PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]:
                        #we're going up - keep going down
                        print("PLAYER - Going down!")
                        guessMin = lastPlayerGuess - abs(lastPlayerGuess - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]) - 2
                        guessMax = lastPlayerGuess - 1
                    elif PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] < PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]:
                        #we're going up!
                        print("PLAYER - Going up!.")
                        guessMin = lastPlayerGuess + 1
                        guessMax = lastPlayerGuess + 5
                    elif PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] == PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]:
                        # we're trying the same number
                        print("PLAYER - I'm an idiot and guessed the same number.")
                        guessMin = lastPlayerGuess + 5
                        guessMax = lastPlayerGuess + 10
                    elif PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 3] > PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]:
                        print("PLAYER - I'm stuck!")
                        guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]
                        guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) -1]
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
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - abs(PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1])
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] + abs(PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1])
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
                guessMin = lastGuessMax + (maxRandomNumber // PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1])
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

            if (oponentStatements[(len(PlayerTwo.guessed_numbers)-1)]).lower().find("warm") > 0:
                print("PLAYER - Crap, I went the wrong way.")
                # lastGuessMin & lastGuessMax should influence our decension here
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) -1] - abs(lastGuessMin)
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) -1] + abs(maxRandomNumber - lastGuessMax)
            elif(oponentStatements[(len(PlayerTwo.guessed_numbers)-1)]).lower().find("very warm") > 0:
                print("PLAYER - Crap, I REALLY went the wrong way.")
                # lastGuessMin & lastGuessMax should influence our decension here
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - abs(lastGuessMin)
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] + abs(maxRandomNumber - lastGuessMax)
            elif (oponentStatements[(len(PlayerTwo.guessed_numbers) - 1)]).lower().find("very cold") > 0:

                #the very cold value is something we want to avoid
                veryCold = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]
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
            # PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]
            #oponentStatements[(len(oponentStatements) - 4)].lower().find("very warm")
            if oponentStatements[(len(oponentStatements) - 2)].lower().find("very warm") > 0:
                #we went the wrong way, turn back
                print("PLAYER - Warm, but I went the wrong way.")
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - (PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2])
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] + 1
            elif oponentStatements[(len(oponentStatements) - 2)].lower().find("warm") > 0:
                #we're flailing in the dark around a possible number
                #try to guess COLD
                print("PLAYER - I'm testing a theory, my next guess will be COLD.")
                #The last two guesses are warm
                #PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]
                #PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]
                if PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] > PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]:
                    guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2] - abs(maxRandomNumber - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2])
                    guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]
                else:
                    guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - abs(maxRandomNumber - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2])
                    guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]
            elif oponentStatements[(len(oponentStatements) - 2)].lower().find("cold") > 0:
                print("PLAYER - I'm so confused.")
                guessMin = lastPlayerGuess + 10
                guessMax = lastPlayerGuess + 30
            elif oponentStatements[(len(oponentStatements) - 2)].lower().find("very cold") > 0:

                #what changed?
                veryCold = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2]
                warm = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1]
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

    # make sure we're not guessing an illegal number
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
    # but don't guess something we're already guessed
    while True:
        playerGuess = random.randint(guessMin, guessMax)
        if not(playerGuess in PlayerTwo.guessed_numbers):
            print("DANG TRIED TO GUESS A DUPLICATE NUMBER")
            break

    # moved adding guesses to the newguess function
    # PlayerTwo.guessed_numbers.append(playerGuess)
    lastPlayerGuess = playerGuess
    lastGuessMax = guessMax
    lastGuessMin = guessMin
    lastGuessWidth = guessWidth


# COMPUTER opponent compares the player guess and gives feed back
def oponentReply():
    global currentGuessOff
    global playerGuess
    global lastGuessOff
    global thisGameTotalGuesses
    global oponentStatements
    global guessOutcomes

    oponentStatement = ""
    # Compare guess to secretNumber
    if playerGuess == GameWorld.secret_number:
        # they got it correct!
        openentStatement = "COMPUTER - I AM SAD, YOU HAVE GUESSED MY SECRET NUMBER. COMPUTER - IT TOOK YOU " + str(thisGameTotalGuesses) + " ATTEMPTS, WHICH IS LAUGHABLE."
        oponentStatements.append(openentStatement)

    elif (currentGuessOff > 50):
        openentStatement = "COMPUTER - VERY COLD, GUESS AGAIN"
        PlayerTwo.very_cold_guess.insert(0, playerGuess)
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 25):
        openentStatement = "COMPUTER - COLD, GUESS AGAIN"
        PlayerTwo.cold_guess.insert(0, playerGuess)
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 10):
        openentStatement = "COMPUTER - WARM, GUESS AGAIN"
        PlayerTwo.warm_guess.insert(0, playerGuess)
        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    elif (currentGuessOff > 0):
        # a very good guess, stay at it
        openentStatement = "COMPUTER - VERY WARM, GUESS AGAIN"
        PlayerTwo.very_warm_guess.insert(0, playerGuess)

        lastGuessOff = currentGuessOff
        oponentStatements.append(openentStatement)
    else:
        openentStatement = "Something went wrong"
    # print("[secret=" + str(secretNumber) + "]")
    print(openentStatement)
    newOutcome = {playerGuess: openentStatement}
    # print(newOutcome)
    if playerGuess in guessOutcomes:
        guessOutcomes.update(newOutcome)
    else:
        guessOutcomes.update(newOutcome)
    # guessOutcomes

def newGuess():
    global allTimeGuesses
    global reusedGuessesInt
    global maxRandomNumber
    global playerIQ

    global playerGuess
    global reusedGuesses

    global reusedGuessesInt
    global thisGameTotalGuesses
    global currentGuessOff
    global guessMin
    global guessMax

    if smartAIOn == True:
        smartAI() # this returns a guess
    else:
        playerGuess = random.randint(guessMin, guessMax)

    PlayerTwo.total_guesses += 1
    thisGameTotalGuesses = thisGameTotalGuesses + 1
    PlayerTwo.guessed_numbers.sort()
    PlayerTwo.guessed_numbers.append(playerGuess)
    # uncomment if you want the game to feel 'live'
    # time.sleep(.900)


def generateGame():
    global playerIQ
    global maxRandomNumber

    global reusedGuessesInt
    global oponentStatements

    global thoughts
    global suspectedNumber
    global guessOutcomes

    # this is a new game until the first turn is resolved

    # clean up re-used globals

    thoughts = []
    guessOutcomes = {}
    oponentStatements = []
    PlayerTwo.guessed_numbers = []
    suspectedNumber = 1

    reusedGuessesInt = 0


    maxRandomNumber = random.randint(1,100) + 100
    GameWorld.secret_number = random.randint(1,maxRandomNumber)
    GameWorld.secret_number = secretNumber
    playerIQ = random.randint(1,10)

    #decide what type of opponent we have
    #loose
    #specific
    #

def playGame():
    # globals
    # TODO: do away with all these damn globals
    global playerGuess

    global gamesPlayed
    global allTimeGuesses
    global maxRandomNumber
    global reusedGuessesInt
    global currentGuessOff

    global thisGameTotalGuesses

    thisGameTotalGuesses = 0
    GameWorld.turn_number = 0

    # locals
    guessMin = 1
    guessMax = maxRandomNumber
    lastGuessOff = 0
    currentGuessType = "wild"

    print("")
    print("---------------[GAME "+ str(gamesPlayed) + "]---------------")
    print("")
    print("Guess a number between 1 and " + str(maxRandomNumber))

    # start the guessing game
    if playerGuess == -1:
        print("COMPUTER - PLEASE GUESS A NUMBER BETWEEN 1 AND " + str(maxRandomNumber))

    # Guess a new number
    while playerGuess != GameWorld.secret_number:
        # Each iteration of this loop is a new turn
        GameWorld.turn_number = GameWorld.turn_number + 1
        print("[TURN "+str(GameWorld.turn_number)+"- SECRET:"+str(GameWorld.secret_number)+"]")
        # decide what type of guess we're going to make
        # wild - guess any damn number
        # educated guess within X of last number
        # specific - guess a specific number because it's right

        newGuess()
        playerReply()
        findSuspectedNumber()
        currentGuessOff = abs(GameWorld.secret_number - playerGuess)
        if playerGuess == GameWorld.secret_number: # player has guessed the answer
            gamesPlayed = gamesPlayed + 1
            if gamesPlayed > GameWorld.games_per_session:
                exit()
            PlayerTwo.total_guesses = PlayerTwo.total_guesses + thisGameTotalGuesses
            oponentReply()
            break
        else:
            # Guess was wrong, continue guessing
            oponentReply()

    # player guesses a unique number

def playerReply():
    global playerGuess
    global guessMin
    global guessMax

    print("PLAYER - [" + str(guessMin) + "-" + str(guessMax) + "]... I GUESS: " + str(playerGuess))



while gamesPlayed <= GameWorld.games_per_session:

    generateGame()
    playGame()

print("The computer played a total of " + str(gamesPlayed) + " games.")
print("You made " + str(PlayerTwo.total_guesses) + " guesses.")
print("You averaged " + str (PlayerTwo.total_guesses / gamesPlayed) + " guesses per game.")
print("The computer is dumb and made repetative guesses " + str(reusedGuessesInt) + " times.")

# for statement in guessOutcomes.items():
#    print(statement)

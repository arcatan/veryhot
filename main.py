#This program will pit the computer against the computer, trying to guess a secret number

import random
import time
import re
import statistics

from datetime import datetime
start_time = datetime.now()

# A
allTimeGuesses = 0

# C
computerHints = []

# G
gamesPlayed = 1
guessTrendDirection = "UP"
guessMin = 1
guessMax = 200
guessOutcomes = {}

# H
holmes_AI_on = True

# J
jug_AI_on = False

# L
lastPlayerGuess = 0
lastGuessMin = 0
lastGuessMax = 0
lastGuessWidth = 0

# M
# maxRandomNumber = 0

# O
opponent_statements = []

# P
playerIQ = 0
playerGuess = -1

#R
reusedGuessesInt = 0

# S
slow_game = False
secretNumber = 0
suspectedNumber = 0
smartAIOn = False
suspectVeryCold = []
suspectCold = []
suspectWarm = []
suspectVeryWarm = []

# T
thisGameTotalGuesses = 0

class GameWorld:
    games_per_session = 150000
    turn_number = 0
    last_player_guess = 0
    secret_number = 0
    total_games = 0
    max_random_number = 100
    min_random_number = 1
    total_guess_each_game = {}

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

class Guessed:
    numbers = []
    very_cold = []
    very_warm = []
    cold = []
    warm = []

class Holmes:
    suspected_number = 1
    guess_number = 1
    used_numbers = []
    available_numbers = []
    confidence_rating = {}
    very_cold_width = 10
    very_warm_width = 10
    warm_width = 20
    cold_width = 20
    known_cold = []
    known_warm = []
    known_very_warm = []
    known_very_cold = []

def playerInternalDialog(newThought):
    global thoughts
    thoughts.append(newThought)

def recordVictory():
    # player has guess the correct value
    global gamesPlayed
    game_update = {gamesPlayed: GameWorld.turn_number}
    GameWorld.total_guess_each_game.update(game_update)

def suggest_upper_limit():
    global guessMax
    global guessMin

    if GameWorld.turn_number == 1:
        guessMax = GameWorld.max_random_number
        # guess slightly above 75% of the range
        #guessMin = ((GameWorld.max_random_number // 4) * 3) + 2
        # alternative method of finding 75% + 2
        guessMin = int(round(GameWorld.max_random_number * .75) + 2)
        print("PLAYER - A new game, how interesting. Upper hint: " + str(guessMax))
    if GameWorld.turn_number == 2:
        guessMax = GameWorld.max_random_number
        # guess slightly above 75% of the range
        guessMin = 1
        # alternative method of finding 75% + 2
        guessMin = int(round(GameWorld.max_random_number * .75) + 2)
        print("PLAYER - I need a hint for upper, " + str(guessMax))
    elif GameWorld.turn_number == 3:
        guessMax = GameWorld.max_random_number // 2
    else:
        guessMax = (GameWorld.max_random_number // 4)*2

    PlayerTwo.suspected_confidence = 1

def reset_holmes():
    Holmes.suspected_number = 1
    Holmes.guess_number = 1
    Holmes.used_numbers = []
    Holmes.available_numbers = []
    Holmes.confidence_rating = {}
    Holmes.known_very_cold = []
    Holmes.known_very_warm = []
    Holmes.known_warm = []
    Holmes.known_cold = []
    i = 0
    for i in range(1, (GameWorld.max_random_number + 1)):
        # print("Adding numbers to Holmes dictionary " + str(i))
        Holmes.available_numbers.append(i)

    for i in range(1, (GameWorld.max_random_number + 1)):
        # print("Adding numbers to Holmes dictionary " + str(i))
        holmes_confidence(i, 0)

    holmes_confidence(1, 1)
    holmes_confidence(GameWorld.max_random_number, 1)
    three_forths = (GameWorld.max_random_number // 4)*3
    holmes_confidence(three_forths, 100)

def holmes_confidence(number, change):
    # number, amount to change confidence (+/-)
    if number < 1 or number > GameWorld.max_random_number:
        return
    try:
        # verify the number exists
        current_confidence = Holmes.confidence_rating[number]
        # update the value
        Holmes.confidence_rating[number] = current_confidence + change
    except:
        Holmes.confidence_rating[number] = change

    # print("[HOLMES] - I've reevaluated ", number, " and scored it: ", change, " Current value: ", Holmes.confidence_rating[number])

def detective_holmes():
    # what numbers are very warm, warm, cold, and very cold

    # add last guess to group
    if opponent_statements[(len(opponent_statements) - 1)].lower().find("very warm") > 0:
        Holmes.known_very_warm.append(lastPlayerGuess)
    elif opponent_statements[(len(opponent_statements) - 1)].lower().find("warm") > 0:
        Holmes.known_warm.append(lastPlayerGuess)
    elif opponent_statements[(len(opponent_statements) - 1)].lower().find("very cold") > 0:
        Holmes.known_very_cold.append(lastPlayerGuess)
    else:
        Holmes.known_cold.append(lastPlayerGuess)

    if len(Holmes.known_very_warm) >= 2:
        Holmes.very_warm_width = max(Holmes.known_very_warm) - min(Holmes.known_very_warm)
        print("[HOLMES] - LVW ", min(Holmes.known_very_warm), ", HVW ", max(Holmes.known_very_warm))
        mean_very_warm = int(round(statistics.mean(Holmes.known_very_warm)))
        if len(Holmes.known_warm) > 1:
            high_warm = max(Holmes.known_warm)
        else:
            high_warm = mean_very_warm - Holmes.very_warm_width
        if high_warm > mean_very_warm > min(Holmes.known_warm):
            # we sorta know where the very warm range is
            upper_width = max(Holmes.known_warm) - max(Holmes.known_very_warm)
            lower_width = min(Holmes.known_very_warm) - min(Holmes.known_warm)
            Holmes.warm_width = (upper_width + lower_width) // 2
            low = mean_very_warm - Holmes.very_warm_width
            high = mean_very_warm + Holmes.very_warm_width
            for number in range(low, high):
                holmes_confidence(number, 20)
                # add a small bump to numbers around the mean value range for very warm
    elif len(Holmes.known_very_warm) == 1:
        # we only know 1 very warm value
        if len(Holmes.known_very_cold) > 1:
            # we know two very cold
            if min(Holmes.known_very_cold) < max(Holmes.known_very_warm) < max(Holmes.known_very_cold):
                # we have very cold values on both sides of very warm
                low = Holmes.known_very_warm[0] - 2
                high = Holmes.known_very_warm[0] + 2
                for number in range(low, high):
                    holmes_confidence(number, 20)

    if len(Holmes.known_warm) > 2:
        Holmes.warm_width = max(Holmes.known_warm) - min(Holmes.known_warm)

    if len(Holmes.known_very_warm) < 1 and len(Holmes.known_very_cold) > 3:
        # we know many very colds, and no very warm
        print("[HOLMES] - I know very cold values. Shouldn't I be able to deduce where very warm is???")

    print("[HOLMES] - Detective Holmes ran - widths: vw ", Holmes.very_warm_width, ", w ", Holmes.warm_width)

def holmesAI():
    global guessMax
    global guessMin
    global playerGuess
    global opponent_statements
    global lastPlayerGuess

    # if it's a new game, wipe Holmes' memory for the new game
    if GameWorld.turn_number == 1:
        reset_holmes()
        print("[HOLMES] - I am fresh and new.")

    # remove previous guess from list of available numbers to guess from
    if lastPlayerGuess > 0 and GameWorld.turn_number > 1:
        detective_holmes()
        try:
            Holmes.available_numbers.remove(lastPlayerGuess)
        except:
            print("Available number not found")
        # since the guess was wrong, make the confidence rating zero
        holmes_confidence(lastPlayerGuess, -100)

    # ensure we don't give up on a very warm streak
    if GameWorld.turn_number > 2:
        if opponent_statements[(len(opponent_statements) - 1)].lower().find("very warm") > 0:
            # increase numbers around very warm
            low_number = lastPlayerGuess - 5
            high_number = lastPlayerGuess + 5
            if low_number < 1:
                low_number = 1
            if high_number > GameWorld.max_random_number:
                high_number = GameWorld.max_random_number
            for number in range(low_number, high_number):
                holmes_confidence(number, 10)

    # update confidence rating based on last guess
    if GameWorld.turn_number > 1:
        up_one = lastPlayerGuess + 1
        down_one = lastPlayerGuess - 1
        if opponent_statements[(len(opponent_statements) - 1)].lower().find("very cold") > 0:
            # subtract 1 from numbers above and below
            number = 0
            low_number = lastPlayerGuess - Holmes.very_cold_width
            high_number = lastPlayerGuess + Holmes.very_cold_width
            if low_number < 1:
                low_number = 1
            if high_number > GameWorld.max_random_number:
                high_number = GameWorld.max_random_number
            change = -10
            for number in range(low_number, high_number):
                # go negative very_cold and subtract 1 from confidence
                holmes_confidence(number, change)
            # increase the confidence for the opposite of a very cold guess
            number = GameWorld.max_random_number - lastPlayerGuess
            change = 1
            holmes_confidence(number, change)

        elif opponent_statements[(len(opponent_statements) - 1)].lower().find("cold") > 0:
            # subtract 1 from numbers above and below
            number = 0
            low_number = lastPlayerGuess - Holmes.cold_width
            high_number = lastPlayerGuess + Holmes.cold_width
            if low_number < 1:
                low_number = 1
            if high_number > GameWorld.max_random_number:
                high_number = GameWorld.max_random_number
            change = -1
            for number in range(low_number, high_number):
                # go negative very_cold and subtract 1 from confidence
                holmes_confidence(number, change)

            try:
                Holmes.available_numbers.remove(up_one)
                Holmes.available_numbers.remove(down_one)
            except:
                print("Couldn't remove cold numbers")
            try:
                number = up_one
                change = 0
                holmes_confidence(number, change)
                # Holmes.confidence_rating[(up_one + 1)] = 0
                # Holmes.confidence_rating[(down_one - 1)] = 0
            except:
                print("Couldn't modify numbers around cold number")

            try:
                number = down_one
                change = 0
                holmes_confidence(number, change)
            except:
                print("Couldn't modify numbers around cold number")

        elif opponent_statements[(len(opponent_statements) - 1)].lower().find("very warm") > 0:
            # add value to all nearby numbers
            change = 10
            low_number = lastPlayerGuess - Holmes.warm_width
            high_number = lastPlayerGuess + Holmes.warm_width
            if low_number < 1:
                low_number = 1
            if high_number > GameWorld.max_random_number:
                high_number = GameWorld.max_random_number

            for number in range(low_number, high_number):
                holmes_confidence(number, change)

            for number in range(1, low_number):
                holmes_confidence(number, -10)
            for number in range(high_number, GameWorld.max_random_number):
                holmes_confidence(number, -10)

        else:
            # add value to all nearby numbers
            change = 1

            # raise numbers below
            low_number = (lastPlayerGuess - Holmes.warm_width) - 10
            high_number = (lastPlayerGuess + Holmes.warm_width) - 10
            if low_number < 1:
                low_number = 1
            if high_number > GameWorld.max_random_number:
                high_number = GameWorld.max_random_number
            for number in range(low_number, high_number):
                holmes_confidence(number, 1)

            # raise numbers above
            low_number = (lastPlayerGuess - Holmes.warm_width) + 10
            high_number = (lastPlayerGuess + Holmes.warm_width) + 10
            if low_number < 1:
                low_number = 1
            if high_number > GameWorld.max_random_number:
                high_number = GameWorld.max_random_number
            for number in range(low_number, high_number):
                holmes_confidence(number, 1)

    else:
        #first round guess
        three_forths_number = (GameWorld.max_random_number // 4) * 3
        new_entry = {three_forths_number: 100}
        Holmes.confidence_rating.update(new_entry)

    if len(Holmes.confidence_rating) < 1:
        print("[HOLMES] - I have no confidence values. Let me think.")
    else:
        print("[HOLMES] - I have " + str(len(Holmes.confidence_rating)) + " confidence ratings.")
        print("[HOLMES] - I can guess from " + str(len(Holmes.available_numbers)) + " numbers.")

    v = []
    k = []
    # print("Keys: " + str(k))
    player_guess = 0
    i = 0
    while True:
        i = i + 1
        v = list(Holmes.confidence_rating.values())
        k = list(Holmes.confidence_rating.keys())
        player_guess = k[v.index(max(v))]
        if player_guess in Holmes.available_numbers:
            print("[HOLMES] - I have not guessed " + str(player_guess) + ".")
            break
        else:
            holmes_confidence(player_guess, -10)
        if i > 1000:
            # we stuck in this dumb loop
            player_guess = random.choice(Holmes.available_numbers)
            break
    if player_guess in Holmes.available_numbers:
        print("okay to guess")
    else:
        print("we need a new number")

    print("[HOLMES] - Highest rated number is " + str(player_guess))
    if lastPlayerGuess > 0:
        if player_guess == lastPlayerGuess:
            print("[HOLMES] - I must be losing my mind, I'm about to randomly guess....")
            player_guess = random.choice(Holmes.available_numbers)
    playerGuess = player_guess
    print("[HOLMES] - I DEDUCE THAT IT IS " + str(player_guess) + "!")
    if slow_game:
        time.sleep(2)
    Holmes.used_numbers.append(player_guess)

    return playerGuess

def jugAI():


    global guessMax
    global guessMin
    global playerGuess
    global opponent_statements
    global lastPlayerGuess

    player_name = "JUG_AI"
    is_very_warm = False


    upper_very_warm = GameWorld.max_random_number
    lower_very_warm = 1


    # if opponent_statements[(len(opponent_statements) - 1)].lower().find("very warm") > 0:
    #    is_very_warm = True

    middle_number = GameWorld.max_random_number // 2
    middle_very_warm = 0
    very_warm_sum = 0
    very_warm_points = 0
    i = 0
    jug_guess_min = 0
    jug_guess_max = GameWorld.max_random_number

    for i in Guessed.very_warm:
        very_warm_sum = very_warm_sum + i
        very_warm_points = very_warm_points + 1

    jug_has_guess = False
    if len(Guessed.very_warm) == 1:
        print("[JUG_AI] - MY FIRST VERY WARM GUESS!")
        middle_very_warm = very_warm_sum / len(Guessed.very_warm)
        jug_guess_min = middle_very_warm - 5
        jug_guess_max = middle_very_warm + 5
        print("[JUG_AI] - JUG GUESS BETWEEN " + str(jug_guess_min) + " - " + str(jug_guess_max))
        jug_has_guess = True
    elif len(Guessed.very_warm) == 2:
        print("[JUG_AI] - MY SECOND VERY WARM GUESS!")
        jug_has_guess = True
        middle_very_warm = very_warm_sum / len(Guessed.very_warm)
        jug_guess_min = middle_very_warm - 1
        jug_guess_max = middle_very_warm + 1
        print("[COMPUTER] - Math - mean of very warm is " + str(int(round(middle_very_warm))))
    elif len(Guessed.very_warm) == 3:
        jug_has_guess = True
        print("[JUG_AI] - MY THIRD VERY WARM GUESS!")
        middle_very_warm = very_warm_sum / len(Guessed.very_warm)
        jug_guess_min = middle_very_warm - 1
        jug_guess_max = middle_very_warm + 1
    elif len(Guessed.very_warm) == 4:
        jug_has_guess = True
        print("[JUG_AI] - MY FORTH VERY WARM GUESS!")
        middle_very_warm = very_warm_sum / len(Guessed.very_warm)
        jug_guess_min = middle_very_warm - 5
        jug_guess_max = middle_very_warm
    elif len(Guessed.very_warm) > 5 and len(Guessed.very_warm) < 10:
        jug_has_guess = True
        print("[JUG_AI] - MY " + str(len(Guessed.very_warm)) + " VERY WARM GUESS!")

        max_very_warm = max(Guessed.very_warm)
        min_very_warm = min(Guessed.very_warm)
        middle_very_warm = very_warm_sum / len(Guessed.very_warm)

        if max_very_warm - min_very_warm > len(Guessed.very_warm):
            # the value is likely between these two
            jug_guess_min = min_very_warm
            jug_guess_max = max_very_warm
        else:
            # distance between MIN and MAX is LESS than the amount of very warm numbers we have found
            jug_guess_min = min_very_warm - len(Guessed.very_warm)
            jug_guess_max = max_very_warm + len(Guessed.very_warm)

        print("[COMPUTER] - Math - mean of very warm is " + str(int(round(middle_very_warm))))
    elif len(Guessed.very_warm) > 10:
        jug_has_guess = True
        middle_very_warm = very_warm_sum / len(Guessed.very_warm)
        jug_guess_min = middle_very_warm - 1
        jug_guess_max = middle_very_warm + 1
        print("[COMPUTER] - Math - mean of very warm is " + str(int(round(middle_very_warm))))
    elif GameWorld.turn_number == 2 and len(Guessed.very_cold) > 0:
        # our first guess was very cold, guess away from it
        jug_has_guess = True
        # lastPlayerGuess - bad number
        if lastPlayerGuess < GameWorld.max_random_number // 4:
            # very cold is low
            jug_guess_min = int(round(GameWorld.max_random_number * .75))
            jug_guess_max = jug_guess_min + 50
        elif lastPlayerGuess < GameWorld.max_random_number // 2:
            jug_guess_min = GameWorld.max_random_number // 2
            jug_guess_max = jug_guess_min + 50
        else:
            jug_guess_min = int(round(GameWorld.max_random_number * .75))
            jug_guess_max = jug_guess_min + 50
    elif len(Guessed.very_cold) > 5:
        jug_has_guess = True
        # we have FIVE bad guesses, stop farting around
        all_cold = []
        i = 0
        sum_all_cold = 0
        for i in Guessed.very_cold:
            all_cold.append(i)
            sum_all_cold = sum_all_cold + i

        middle_very_cold = i // len(Guessed.very_cold)
        list_very_cold = Guessed.very_cold
        list_very_cold.sort()
        upper_very_cold = max(list_very_cold)
        lower_very_cold = min(list_very_cold)
        if (upper_very_cold - lower_very_cold > GameWorld.max_random_number // 2) and len(Guessed.very_warm) == 1:
            # we have extreme very cold values and only know 1 very warm
            upper_very_warm = max(Guessed.very_warm)
            lower_very_warm = min(Guessed.very_warm)
            jug_guess_min = lower_very_warm - 10
            jug_guess_max = upper_very_warm + 10
        elif len(Guessed.very_warm) > 1:
            # we know at least two very warm values, guess around it instead
            upper_very_warm = max(Guessed.very_warm)
            lower_very_warm = min(Guessed.very_warm)
            jug_guess_min = lower_very_warm - 1
            jug_guess_max = upper_very_warm + 1
        else:
            # we don't know any very warm values
            if middle_very_cold < GameWorld.max_random_number // 2:
                # guess high
                jug_guess_min = GameWorld.max_random_number // 2
                jug_guess_max = GameWorld.max_random_number
            else:
                # guess low
                jug_guess_min = 1
                jug_guess_max = GameWorld.max_random_number // 2

        print("[JUG_AI] - I KNOW LIKE ALL THE DAMN VERY COLD VALUES!" + str(lower_very_cold) + " - " + str(upper_very_cold))

    elif GameWorld.turn_number > 10:
        # we have made ten bad guesses

        # can we find a hole in the very cold values?
        print("[JUG_AI] - I KNOW " + str(len(Guessed.very_cold)) + " VERY COLD, " + str(len(Guessed.cold))  + " COLD, " + str(len(Guessed.warm)) + " WARM, and " + str(len(Guessed.very_warm)) + " VERY WARM")


        if opponent_statements[(len(opponent_statements) - 1)].lower().find("very warm") == 0 and len(Guessed.warm) > 2:
            middle_warm = (Guessed.warm / len(Guessed.warm))
            jug_has_guess = True
            jug_guess_min = int(round(middle_warm)) - 20
            jug_guess_max = int(round(middle_warm)) + 20
        else:
            jug_guess_min = random.randint(25, GameWorld.max_random_number)
            jug_guess_max = jug_guess_min + 50
    else:
        # haven't found a very warm number
        jug_has_guess = False

    # first turn instructions
    if jug_has_guess:
        print("["+ player_name + "] - HAS GUESS.")
        # don't fight the jug AI, let it guess!
        guessMin = jug_guess_min
        guessMax = jug_guess_max
        # okay, it guessed. Now put the monster away
        jug_has_guess = False

    elif GameWorld.turn_number == 1:
        print("["+ player_name + "] - I AM READY TO PLAY THE GUESSING GAME.")
        coin_toss = random.randint(1, 2)
        # heads (2) - go > 75%
        if coin_toss == 1:
            # tails (1) - go < 25%
            guessMin = 1
            guessMax = int(round(GameWorld.max_random_number * .25))
            print("[" + player_name + "] - I SUSPECT IT IS A SMALL NUMBER. < " + str(guessMax))
        else:

            # heads (2) - go > 75%
            guessMin = int(round(GameWorld.max_random_number * .75))
            guessMax = GameWorld.max_random_number
            print("[" + player_name + "] - I SUSPECT IT IS A LARGE NUMBER. > " + str(guessMin))

    elif GameWorld.turn_number <= 10:
        # test our cool logic here
        guessMin = 1
        guessMax = GameWorld.max_random_number
    else:
        guessMin = 1
        guessMax = GameWorld.max_random_number



    # make sure we're not guessing an illegal number

    guessMinHolder = 0
    guessMaxHolder = 0

    if guessMin > guessMax:
        print("[COMPUTER] - YOUR AI IS CONFUSED. MIN " + str(guessMin) + "MAX" + str(guessMin))
        guessMinHolder = guessMin
        guessMaxHolder = guessMax
        guessMin = guessMaxHolder
        guessMax = guessMinHolder

    if guessMin <= 0 or guessMin > guessMax:
        print("[COMPUTER] - YOUR AI IS CONFUSED. MIN " + str(guessMin) + "MAX" + str(guessMin))
        guessMin = 1
        guessMax = GameWorld.max_random_number
    if guessMax <= 0 or guessMax > GameWorld.max_random_number:
        print("[COMPUTER] - YOUR AI IS CONFUSED. MIN " + str(guessMin) + "MAX" + str(guessMin))
        guessMin = 1
        guessMax = maxRandomNumber

    # finally, make our guess
    guessMin = int(round(guessMin))
    guessMax = int(round(guessMax))
    # but don't guess something we're already guessed

    i = 0
    playerGuess = 0
    while True:
        playerGuess = random.randint(guessMin, guessMax)

        if not(playerGuess in PlayerTwo.guessed_numbers):
            print("[" + player_name + "] - " + str(playerGuess) + " IS UNIQUE, I GUESS!")
            break
        elif (guessMax - guessMin) < i:
            guessMin = guessMin - 1
            guessMax = guessMax + 1
        elif i > 100:
            # increase the scope more
            guessMin = guessMin - 2
            guessMax = guessMax + 2
            i = 0

        if guessMin < 1 or guessMin > GameWorld.max_random_number:
            guessMin = 1
        if guessMax < guessMin or guessMax > GameWorld.max_random_number:
            guessMax = GameWorld.max_random_number

        print("guess " + str(playerGuess) + " min " + str(guessMin) + " max " + str(guessMax))
        i = i + 1

def suggest_lower_limit():
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
    print("PLAYER - I need a hint for lower, " + str(guessMin))

def findSuspectedNumber():
    global suspectedNumber
    global opponent_statements
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
    guessCount = GameWorld.turn_number

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
    global opponent_statements
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

    if len(opponent_statements) >= 1:
        mostRecentStatement = opponent_statements[(len(opponent_statements) - 1)]
        previousOpponentStatement = opponent_statements[(len(opponent_statements) - 2)]
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
            len(opponent_statements)))

        print(str(PlayerTwo.guessed_numbers)[1:-1])

        #print(mostRecentStatement)
        if (len(opponent_statements) <= 3): #first three guessess use suggestLower() and suggestUpper()
            print("PLAYER - Okay, here we go!")
            newThought = "It's a new game."
            needSuggestionUpper = True
            needSuggestionLower = True
            playerGuess = random.randint(guessMin, guessMax) #
        elif (mostRecentStatement.lower().find("very warm") > 0 and len(opponent_statements) >= 3): # guess is great
            if previousOpponentStatement.lower().find("very warm") > 0:
                #last two guessess were very warm
                if (opponent_statements[(len(opponent_statements) - 4)].lower().find("very warm") > 0):
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
                elif(opponent_statements[(len(opponent_statements) - 3)].lower().find("very warm") > 0):
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

            if (opponent_statements[(len(PlayerTwo.guessed_numbers)-1)]).lower().find("warm") > 0:
                print("PLAYER - Crap, I went the wrong way.")
                # lastGuessMin & lastGuessMax should influence our decension here
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) -1] - abs(lastGuessMin)
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) -1] + abs(maxRandomNumber - lastGuessMax)
            elif(opponent_statements[(len(PlayerTwo.guessed_numbers)-1)]).lower().find("very warm") > 0:
                print("PLAYER - Crap, I REALLY went the wrong way.")
                # lastGuessMin & lastGuessMax should influence our decension here
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - abs(lastGuessMin)
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] + abs(maxRandomNumber - lastGuessMax)
            elif (opponent_statements[(len(PlayerTwo.guessed_numbers) - 1)]).lower().find("very cold") > 0:

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
            #opponent_statements[(len(opponent_statements) - 4)].lower().find("very warm")
            if opponent_statements[(len(opponent_statements) - 2)].lower().find("very warm") > 0:
                #we went the wrong way, turn back
                print("PLAYER - Warm, but I went the wrong way.")
                guessMin = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - (PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] - PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 2])
                guessMax = PlayerTwo.guessed_numbers[len(PlayerTwo.guessed_numbers) - 1] + 1
            elif opponent_statements[(len(opponent_statements) - 2)].lower().find("warm") > 0:
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
            elif opponent_statements[(len(opponent_statements) - 2)].lower().find("cold") > 0:
                print("PLAYER - I'm so confused.")
                guessMin = lastPlayerGuess + 10
                guessMax = lastPlayerGuess + 30
            elif opponent_statements[(len(opponent_statements) - 2)].lower().find("very cold") > 0:

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
                    guessMax = lastPlayerGuess - 1

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
        suggest_upper_limit()
    if needSuggestionLower:
        suggest_lower_limit()

    # make sure we're not guessing an illegal number
    if guessMin > guessMax:
        print("[COMPUTER] - YOUR AI IS CONFUSED. MIN " + str(guessMin) + "MAX" + str(guessMin))
        guessMinHolder = guessMin
        guessMaxHolder = guessMax
        guessMin = guessMaxHolder
        guessMax = guessMinHolder

    if guessMin <= 0 or guessMin > guessMax:
        print("[COMPUTER] - YOUR AI IS CONFUSED. MIN " + str(guessMin) + "MAX" + str(guessMin))
        guessMin = 1
        guessMax = maxRandomNumber
    if guessMax <= 0 or guessMax > maxRandomNumber:
        print("[COMPUTER] - YOUR AI IS CONFUSED. MIN " + str(guessMin) + "MAX" + str(guessMin))
        guessMin = 1
        guessMax = maxRandomNumber

    # finally, make our guess
    # but don't guess something we're already guessed
    i = 0
    while True:
        i = i + 1
        playerGuess = random.randint(guessMin, guessMax)
        if not(playerGuess in PlayerTwo.guessed_numbers):
            print("DANG TRIED TO GUESS A DUPLICATE NUMBER")
            break
        if i > 100:
            # we might be stuck trying to get a unique number
            guessMin = guessMin - 1
            guessMax = guessMax + 1
            if guessMin < 1:
                guessMin = 1
            if guessMax > GameWorld.max_random_number:
                guessMax = GameWorld.max_random_number
            i = 0

    # moved adding guesses to the new guess function
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
    global opponent_statements
    global guessOutcomes

    oponentStatement = ""
    # Compare guess to secretNumber
    if playerGuess == GameWorld.secret_number:
        # they got it correct!
        openentStatement = "COMPUTER - I AM SAD, YOU HAVE GUESSED MY SECRET NUMBER. COMPUTER - IT TOOK YOU " + str(thisGameTotalGuesses) + " ATTEMPTS, WHICH IS LAUGHABLE."
        opponent_statements.append(openentStatement)

    elif (currentGuessOff > 50):
        openentStatement = "COMPUTER - VERY COLD, GUESS AGAIN"
        PlayerTwo.very_cold_guess.insert(0, playerGuess)
        lastGuessOff = currentGuessOff
        opponent_statements.append(openentStatement)
        Guessed.very_cold.append(playerGuess)
    elif (currentGuessOff > 25):
        openentStatement = "COMPUTER - COLD, GUESS AGAIN"
        PlayerTwo.cold_guess.insert(0, playerGuess)
        lastGuessOff = currentGuessOff
        opponent_statements.append(openentStatement)
        Guessed.cold.append(playerGuess)
    elif (currentGuessOff > 10):
        openentStatement = "COMPUTER - WARM, GUESS AGAIN"
        PlayerTwo.warm_guess.insert(0, playerGuess)
        lastGuessOff = currentGuessOff
        opponent_statements.append(openentStatement)
        Guessed.warm.append(playerGuess)
    elif (currentGuessOff > 0):
        # a very good guess, stay at it
        openentStatement = "COMPUTER - VERY WARM, GUESS AGAIN"
        PlayerTwo.very_warm_guess.insert(0, playerGuess)
        Guessed.very_warm.append(playerGuess)

        lastGuessOff = currentGuessOff
        opponent_statements.append(openentStatement)
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
    global lastPlayerGuess
    global playerGuess
    global reusedGuesses
    global reusedGuessesInt
    global thisGameTotalGuesses
    global currentGuessOff
    global guessMin
    global guessMax

    if smartAIOn:
        # this returns a guess
        smartAI()
    elif jug_AI_on:
        # this returns a guess
        jugAI()
    elif holmes_AI_on:
        holmesAI()
    else:
        playerGuess = random.randint(guessMin, guessMax)

    lastPlayerGuess = playerGuess
    PlayerTwo.total_guesses += 1
    thisGameTotalGuesses = thisGameTotalGuesses + 1
    PlayerTwo.guessed_numbers.sort()
    PlayerTwo.guessed_numbers.append(playerGuess)

    Guessed.numbers.sort()
    Guessed.numbers.append(playerGuess)

    # uncomment if you want the game to feel 'live'
    if slow_game:
        time.sleep(.300)

def generateGame():
    global playerIQ
    global maxRandomNumber
    global reusedGuessesInt
    global opponent_statements
    global thoughts
    global suspectedNumber
    global guessOutcomes
    global lastPlayerGuess


    # reset all guessed
    Guessed.very_cold = []
    Guessed.very_warm = []
    Guessed.cold = []
    Guessed.warm = []
    Guessed.numbers = []


    # this is a new game until the first turn is resolved
    # clean up re-used globals
    lastPlayerGuess = 0
    thoughts = []
    guessOutcomes = {}
    opponent_statements = []
    PlayerTwo.guessed_numbers = []
    suspectedNumber = 1

    reusedGuessesInt = 0
    GameWorld.max_random_number = random.randint(1, 6) + random.randint(0, 48) + random.randint(0, 96) + 100
    GameWorld.secret_number = random.randint(1, GameWorld.max_random_number)
    maxRandomNumber = GameWorld.max_random_number

    playerIQ = random.randint(1,10)

def playGame():
    # globals
    # TODO: do away with all these damn globals
    global playerGuess

    global gamesPlayed
    global allTimeGuesses
    # global maxRandomNumber
    global reusedGuessesInt
    global currentGuessOff

    global thisGameTotalGuesses

    thisGameTotalGuesses = 0
    GameWorld.turn_number = 0

    # locals
    guessMin = 1
    guessMax = GameWorld.max_random_number
    lastGuessOff = 0
    currentGuessType = "wild"

    player_name = "COMPUTER"
    if gamesPlayed > GameWorld.games_per_session:
        return


    print("")
    print("---------------[GAME " + str(gamesPlayed) + "]---------------")
    print("")
    print("Guess a number between 1 and " + str(GameWorld.max_random_number) + ". [the secret is " + str(GameWorld.secret_number) + "]")

    # start the guessing game
    if playerGuess == -1:
        print("[" + player_name + "] - PLEASE GUESS A NUMBER BETWEEN 1 AND " + str(GameWorld.max_random_number))

    # Guess a new number
    while playerGuess != GameWorld.secret_number:
        print(" ")
        # Each iteration of this loop is a new turn
        GameWorld.turn_number = GameWorld.turn_number + 1
        print("[TURN "+str(GameWorld.turn_number)+"- SECRET:"+str(GameWorld.secret_number)+"]")
        # decide what type of guess we're going to make
        # wild - guess any damn number
        # educated guess within X of last number
        # specific - guess a specific number because it's right

        newGuess()
        playerReply()
        # findSuspectedNumber()
        currentGuessOff = abs(GameWorld.secret_number - playerGuess)
        if playerGuess == GameWorld.secret_number:
            recordVictory()
            # player has guessed the answer
            gamesPlayed = gamesPlayed + 1
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

    # TODO: get dynamic player name here
    print("PLAYER - [" + str(guessMin) + "-" + str(guessMax) + "]... I GUESS: " + str(playerGuess))

def report():
    print("")
    print("--------------------------------[REPORT]-------------------------------------")
    print("")

    session_total_guesses = 0
    for game in GameWorld.total_guess_each_game:
        session_total_guesses = session_total_guesses + GameWorld.total_guess_each_game[game]
        print("Game:" + str(game) + " - Guesses = " + str(GameWorld.total_guess_each_game[game]))

    a = []
    b = []
    a = list(GameWorld.total_guess_each_game.values())
    b = list(GameWorld.total_guess_each_game.keys())
    best_game_number = b[a.index(min(a))]
    worst_game_number = b[a.index(max(a))]

    print("The computer played a total of " + str(gamesPlayed - 1) + " games.")
    print("It made " + str(session_total_guesses) + " guesses.")
    print("It averaged " + str(session_total_guesses / (gamesPlayed - 1)) + " guesses per game.")
    print("Best  - Game", best_game_number, ": ", GameWorld.total_guess_each_game[best_game_number])
    print("Worst - Game", worst_game_number, ": ", GameWorld.total_guess_each_game[worst_game_number])
    print("Mode ", statistics.mode(GameWorld.total_guess_each_game.values()))
    run_time = datetime.now() - start_time
    print("Script completed in:", run_time)
    # for statement in guessOutcomes.items():
    #    print(statement)


while gamesPlayed <= GameWorld.games_per_session:

    generateGame()
    playGame()

# Session finished, give us the stats
report()

'''
print("")
print("--------------------------------[REPORT]-------------------------------------")
print("")

session_total_guesses = 0
for game in GameWorld.total_guess_each_game:
    session_total_guesses = session_total_guesses + GameWorld.total_guess_each_game[game]
    print("Game:" + str(game) + " - Guesses = " + str(GameWorld.total_guess_each_game[game]))

a = []
b = []
a = list(GameWorld.total_guess_each_game.values())
b = list(GameWorld.total_guess_each_game.keys())
best_game_number = b[a.index(min(a))]
worst_game_number = b[a.index(max(a))]


print("The computer played a total of " + str(gamesPlayed - 1) + " games.")
print("It made " + str(session_total_guesses) + " guesses.")
print("It averaged " + str(session_total_guesses / (gamesPlayed - 1)) + " guesses per game.")
print("Best  - Game", best_game_number, ": ", GameWorld.total_guess_each_game[best_game_number])
print("Worst - Game", worst_game_number, ": ", GameWorld.total_guess_each_game[worst_game_number])


run_time = datetime.now() - start_time
print("Script completed in:", run_time)
# for statement in guessOutcomes.items():
#    print(statement)
'''
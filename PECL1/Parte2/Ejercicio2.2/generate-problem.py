#!/usr/bin/env python3

########################################################################################
# Problem instance generator skeleton for emergencies drones domain.
# Based on the Linköping University TDDD48 2021 course.
# https://www.ida.liu.se/~TDDD48/labs/2021/lab1/index.en.shtml
#
# You mainly have to change the parts marked as TODO.
#
########################################################################################


from optparse import OptionParser
import random
import math
import sys

########################################################################################
# Hard-coded options
########################################################################################

# Crates will have different contents, such as food and medicine.
# You can change this to generate other contents if you want.

content_types = ("comida", "medicina")
limit = 4


########################################################################################
# Random seed
########################################################################################

# Set seed to 0 if you want more predictability...
# random.seed(0);

########################################################################################
# Helper functions
########################################################################################

# We associate each location with x/y coordinates.  These coordinates
# won't actually be used explicitly in the domain, but we *will*
# eventually use them implicitly by using *distances* in order to
# calculate flight times.
#
# This function returns the euclidean distance between two locations.
# The locations are given via their integer index.  You won't have to
# use this other than indirectly through the flight cost function.

def distance(location_coords, location_num1, location_num2):
    x1 = location_coords[location_num1][0]
    y1 = location_coords[location_num1][1]
    x2 = location_coords[location_num2][0]
    y2 = location_coords[location_num2][1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# This function returns the action cost of flying between two
# locations supplied by their integer indexes.  You can use this
# function when you extend the problem generator to generate action
# costs.

def flight_cost(location_coords, location_num1, location_num2):
    return int(distance(location_coords, location_num1, location_num2)) + 1


# When you run this script you specify the *total* number of crates
# you want.  The function below determines randomly which crates
# will have a specific type of contents.  crates_with_contents[0]
# is a list of crates containing content_types[0] (in our
# example "food"), and so on.
# Note: Will have at least one crate per type!

def setup_content_types(options):
    while True:
        num_crates_with_contents = []
        crates_left = options.crates
        for x in range(len(content_types) - 1):
            types_after_this = len(content_types) - x - 1
            max_now = crates_left - types_after_this
            # print x, types_after_this, crates_left, len(content_types), max_now
            num = random.randint(1, max_now)
            # print num
            num_crates_with_contents.append(num)
            crates_left -= num
        num_crates_with_contents.append(crates_left)
        # print(num_crates_with_contents)

        # If we have 10 medicine and 4 food, with 7 people,
        # we can support at most 7+4=11 goals.
        maxgoals = sum(min(num_crates, options.persons) for num_crates in num_crates_with_contents)

        # Check if the randomization supports the number of goals we want to generate.
        # Otherwise, try to randomize again.
        if options.goals <= maxgoals:
            # Done
            break

    print()
    print("Types\tQuantities")
    for x in range(len(num_crates_with_contents)):
        if num_crates_with_contents[x] > 0:
            print(content_types[x] + "\t " + str(num_crates_with_contents[x]))

    crates_with_contents = []
    counter = 1
    for x in range(len(content_types)):
        crates = []
        for y in range(num_crates_with_contents[x]):
            crates.append("caja" + str(counter))
            counter += 1
        crates_with_contents.append(crates)

    return crates_with_contents


# This function populates the location_coords list with an X and Y
# coordinate for each location.  You won't have to use this other than
# indirectly through the flight cost function.

def setup_location_coords(options):
    location_coords = [(0, 0)]  # For the depot
    for x in range(1, options.locations + 1):
        location_coords.append((random.randint(1, 200), random.randint(1, 200)))

    print("Location positions", location_coords)
    return location_coords


# This function generates a random set of goals.
# After you run this, need[personid][contentid] is true if and only if
# the goal is for the person to have a crate with the specified content.
# You will use this to create goal statements in PDDL.
def setup_person_needs(options, crates_with_contents):
    need = [[False for i in range(len(content_types))] for j in range(options.persons)]
    goals_per_contents = [0 for i in range(len(content_types))]

    for goalnum in range(options.goals):

        generated = False
        while not generated:
            rand_person = random.randint(0, options.persons - 1)
            rand_content = random.randint(0, len(content_types) - 1)
            # If we have enough crates with that content
            # and the person doesn't already need that content
            if (goals_per_contents[rand_content] < len(crates_with_contents[rand_content])
                    and not need[rand_person][rand_content]):
                need[rand_person][rand_content] = True
                goals_per_contents[rand_content] += 1
                generated = True
    return need


########################################################################################
# Main program
########################################################################################

def main():
    # Take in all arguments and print them to standard output

    parser = OptionParser(usage='python generator.py [-help] options...')
    parser.add_option('-d', '--drones', metavar='NUM', dest='drones', action='store', type=int, help='the number of drones')
    parser.add_option('-r', '--carriers', metavar='NUM', type=int, dest='carriers',
                      help='the number of carriers, for later labs; use 0 for no carriers')
    parser.add_option('-l', '--locations', metavar='NUM', type=int, dest='locations',
                      help='the number of locations apart from the depot ')
    parser.add_option('-p', '--persons', metavar='NUM', type=int, dest='persons', help='the number of persons')
    parser.add_option('-c', '--crates', metavar='NUM', type=int, dest='crates', help='the number of crates available')
    parser.add_option('-g', '--goals', metavar='NUM', type=int, dest='goals',
                      help='the number of crates assigned in the goal')

    (options, args) = parser.parse_args()

    if options.drones is None:
        print("You must specify --drones (use --help for help)")
        sys.exit(1)

    if options.carriers is None:
        print("You must specify --carriers (use --help for help)")
        sys.exit(1)

    if options.locations is None:
        print("You must specify --locations (use --help for help)")
        sys.exit(1)

    if options.persons is None:
        print("You must specify --persons (use --help for help)")
        sys.exit(1)

    if options.crates is None:
        print("You must specify --crates (use --help for help)")
        sys.exit(1)

    if options.goals is None:
        print("You must specify --goals (use --help for help)")
        sys.exit(1)

    if options.goals > options.crates:
        print("Cannot have more goals than crates")
        sys.exit(1)

    if len(content_types) > options.crates:
        print("Cannot have more content types than crates:", content_types)
        sys.exit(1)

    if options.goals > len(content_types) * options.persons:
        print("For", options.persons, "persons, you can have at most", len(content_types) * options.persons, "goals")
        sys.exit(1)

    print("Drones\t\t", options.drones)
    print("Carriers\t", options.carriers)
    print("Locations\t", options.locations)
    print("Persons\t\t", options.persons)
    print("Crates\t\t", options.crates)
    print("Goals\t\t", options.goals)

    # Setup all lists of objects

    # These lists contain the names of all Drones, locations, and so on.

    drone = []
    person = []
    crate = []
    carrier = []
    location = []

    for x in range(options.locations):
        location.append("loc" + str(x + 1))
    for x in range(options.drones):
        drone.append("dron" + str(x + 1))
    for x in range(options.carriers):
        carrier.append("transportador" + str(x + 1))
    for x in range(options.persons):
        person.append("persona" + str(x + 1))
    for x in range(options.crates):
        crate.append("caja" + str(x + 1))
    
    # Determine the set of crates for each content.
    # If content_types[0] is "food",
    # then crates_with_contents[0] is a list
    # containing the names of all crates that contain food.
    crates_with_contents = setup_content_types(options)

    # Generates coordinates for each location.
    # You will only use this indirectly,
    # through the flight_cost() function in lab 2.

    location_coords = setup_location_coords(options)

    # Determine which types of content each person needs.
    # If person[0] is "person0",
    # and content_types[1] is "medicine",
    # then needs[0][1] is true iff person0 needs medicine.
    need = setup_person_needs(options, crates_with_contents)

    # Define a problem name
    problem_name = "drone_problem_d" + str(options.drones) + "_r" + str(options.carriers) + \
                   "_l" + str(options.locations) + "_p" + str(options.persons) + "_c" + str(options.crates) + \
                   "_g" + str(options.goals) + "_ct" + str(len(content_types))

    # Open output file
    with open(problem_name + ".pddl", 'w') as f:
        # Write the initial part of the problem

        f.write("(define (problem " + problem_name + ")\n")
        f.write("(:domain dron-strips)\n")
        f.write("(:objects\n")

        ######################################################################
        # Write objects

        # TODO: Change the type names below (drone, location, ...)
        # to suit your domain.

        for x in drone:
            f.write("\t" + x + " - dron\n")

        f.write("\tdeposito - localizacion\n")
        for x in location:
            f.write("\t" + x + " - localizacion\n")

        for x in crate:
            f.write("\t" + x + " - caja\n")

        for x in content_types:
            f.write("\t" + x + " - contenido\n")

        for x in person:
            f.write("\t" + x + " - persona\n")

        for x in carrier:
            f.write("\t" + x + " - transportador\n")

        for i in range(limit + 1):
            f.write("\tn" + str(i) + " - num\n")

        f.write(")\n")

        ######################################################################
        # Generate an initial state

        f.write("(:init\n")

        # TODO: Initialize all facts here!

        #Inicializar localizaciones de los objetos
        for i in drone:
            f.write("\t(dron-en " + i + " deposito)\n")
        for i in crate:
            f.write("\t(caja-en " + i + " deposito)\n")
        for i in crate:
            f.write("\t(caja-disponible " + i + " )\n")
        for i in person:
            f.write("\t(persona-en " + i + " " + random.choice(location) + ")\n")
        for i in carrier:
            f.write("\t(transportador-en " + i + " deposito)\n")
        f.write("\n")

        #Inicializar contenido de las cajas
        for i in range(len(crates_with_contents)):
            for j in crates_with_contents[i]:
                f.write("\t(caja-contiene " + j + " " + content_types[i] + ")\n")
        f.write("\n")

        #Inicializar lo que necesita una persona
        for i in range(len(person)):
            for j in range(len(content_types)):
                if (need[i][j] == True):
                    f.write("\t(persona-necesita persona" + str(i + 1) + " " + content_types[j] + ")\n")
        f.write("\n")

        for i in range(limit):
            f.write("\t(siguiente n" + str(i) + " n" + str(i + 1) + ")\n")
        f.write("\n")

        for i in carrier:
            f.write("\t(limite-de " + i + " n0)\n")

        for i in drone:
            f.write("\t(dron-libre " + i + ")\n")
            f.write("\n")
            f.write("\t(= (total-cost) 0)\n")

        f.write("\n")
        for i in range(0, len(location) + 1):
            for j in range(0, len(location) + 1):

                if (i == 0 and j != 0):
                    distance= flight_cost(location_coords, i, j)
                    f.write("\t(= (fly-cost deposito loc" + str(j) + ") " + str(distance) + ")\n")

                elif (i != j):
                    distance= flight_cost(location_coords, i, j)
                    if (j == 0):
                        f.write("\t(= (fly-cost loc" + str(i) + " deposito) " + str(distance) + ")\n")
                    else:
                        f.write("\t(= (fly-cost loc" + str(i) + " loc" + str(j) + ") " + str(distance) + ")\n")
                else:
                    if (i == 0):
                        f.write("\t(= (fly-cost deposito deposito) 0)\n")
                    else:
                        f.write("\t(= (fly-cost loc" + str(i) + " loc" + str(j) + ") 0)\n")

        f.write(")\n")

        ######################################################################
        # Write Goals

        f.write("(:goal (and\n")

        #Objetivo 
        for i in range(len(person)):
            for j in range(len(content_types)):
                if (need[i][j] == True):
                    f.write("\t(persona-tiene persona" + str(i + 1) + " " + content_types[j] + ")\n")
        f.write("\n")

        # All Drones should end up at the depot
        for x in drone:
            f.write("\t(dron-en " + x + " deposito)\n")
            # TODO: Write a goal that the drone x is at the depot

        for x in range(options.persons):
            for y in range(len(content_types)):
                if need[x][y]:
                    person_name = person[x]
                    content_name = content_types[y]
                    # TODO: write a goal that the person needs a crate
                    # with this specific content

        f.write("))\n")
        f.write("(:metric minimize (total-cost))\n")
        f.write(")\n")

if __name__ == '__main__':
    main()

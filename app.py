import random
import matplotlib.pyplot as plotter
import json

# First we have to know all the types of valid,invalid and boundary cases
valid_cases = ["V:30Day","V:31Day","V:LeapYear","V:NonLeapYear"]
invalid_cases = ["IV:Year","IV:Month","IV:Day","IV:30Day","IV:31Day","IV:LeapYear","IV:28Day"]
boundary_cases = ["V:30DayBoundary","V:31DayBoundary","V:LeapYearBoundary","V:NonLeapYearBoundary","V:Month Boundary","V:Year Boundary"]

# These are the weights that are assigned to each category based on their rarity in the generation process and
# also their value for testing
category_weights = {
    "V:30Day": 10.0,
    "V:31Day": 10.0,
    "V:LeapYear": 110.5,
    "V:NonLeapYear": 90,
    "V:30DayBoundary": 20,
    "V:31DayBoundary": 18,
    "V:LeapYearBoundary": 440,
    "V:NonLeapYearBoundary": 380,
    "V:Month Boundary": 130,
    "V:Year Boundary": 101,
    "IV:Year": 100.0,
    "IV:Month": 100.0,
    "IV:Day": 100.0,
    "IV:30Day": 150,
    "IV:31Day": 200,
    "IV:LeapYear": 100,
    "IV:28Day": 50,
}
def intialize_population(size):
    """

    This function is primarily used to generate a random population of dates that
    will be used as the initial population for our Genetric Algorithm

    :param size: The size of the population to be generated
    :return: The population in the form of a list
    """
    population = []
    for i in range(0,size):
        day = random.randint(1,31)
        month = random.randint(1,12)
        year = random.randint(0,9999)
        new_date = (day,month,year)
        population.append(new_date)
    return population

def determine_category(test_case):
    """
    Here we determine which category does the test case fall into
    A single test case can come into multiple categories and hence a list is returned instead of a single category as a
     string
    :param test_case: The test_case for which the categories have to be determined
    :return: List of categories
    """

    # Initially category list is empty
    category = []
    day,month,year = test_case

    # Bellow are all the cases on the basis of which category is evaluated of our test case
    if year < 0 or year > 9999:
        category.append("IV:Year")

    if month <1 or month >12 :
        category.append("IV:Month")

    if day<1 or day>31:
        category.append("IV:Day")

    if month in [4,6,9,11] and day > 30:
        category.append("IV:30Day")
    elif month in [4,6,9,11] and day <= 30:
        if day == 30 or day == 1:
            category.append("V:30DayBoundary")
        else:
            category.append("V:30Day")

    if month in [4,6,9,11] and day > 31:
         category.append("IV:31Day")
    elif month in [1,3,5,7,8,10,12] and day <= 31:
        if day == 31 or day == 1:
            category.append("V:31DayBoundary")
        else:
            category.append("V:31Day")

    # This is for February to check leap year cases
    if month == 2:
        is_leap = (year %4 ==0 and year %100 !=0 ) or (year % 400 == 0)
        if is_leap and day > 29:
            category.append("IV:LeapYear")
        elif not is_leap and day>28:
            category.append("IV:28Day")

        if is_leap and day<=29:
            if day == 29:
                category.append("V:LeapYearBoundary")
            else:
                category.append("V:LeapYear")
        if not is_leap and day<=28:
            if day == 28 or day == 1:
                category.append("V:NonLeapYearBoundary")
            else:
                category.append("V:NonLeapYear")

    if month == 1 or month == 12:
         category.append("V:Month Boundary")
    if year == 1 or year == 9999:
        category.append("V:Year Boundary")

    # At the end we return the required category
    return category

def fitness_calculation(population):

    """
    This function is used to calculate the fitness value for each test case by counting the number of categories it is
    testing and dividing by the number of times the category is already tested by other test cases

    :param population: The population for which the fitness value has to be calculated
    :return: List of list containing the test case, and it's fitness value
    """

    # We first calculate the total counts of each number of categories. Initially they are all zero

    counts = {}
    for i in valid_cases:
        counts[i] = 0
    for i in invalid_cases:
        counts[i] = 0
    for i in boundary_cases:
        counts[i] = 0

    fitness_list = []

    # Count the amount for each category
    for date in population:
        category_list = determine_category(date)
        for i in category_list:
            counts[i] += 1
    # Now based on count and weights of the category we calculate the total fitness
    for date in population:
        category = determine_category(date)
        fitness = 0
        for i in category:

            fitness += category_weights[i]/(counts[i]+1)
        fitness_list.append([date,fitness])
    return fitness_list


def selection(fitness_list):
    """
    Now we select the population that has the best fitness based on ranking and half of the population is removed
    if they have lower fitness value. Half of the population is selected.
    :param fitness_list: The population with its fitness value
    :return: List of selected test cases on the basis of fitness value
    """

    # Sort the list based on fitness value in descending order
    for i in range(0,len(fitness_list)):
        for j in range(i,len(fitness_list)):
            if fitness_list[i][1]<fitness_list[j][1]:
                fitness_list[i],fitness_list[j] = fitness_list[j],fitness_list[i]
    end = int(len(fitness_list)/2)

    # Now selected half of the population and remove the rest
    selected = []
    for i in range(0,int(len(fitness_list)/2)):
        selected.append(fitness_list[i][0])
    return selected


def crossover_population(selected_population):
    """
    Crossover done of the population till the required population size has been reached
    :param selected_population: The population that needs to have cross over
    :return: New population in the form of a list
    """

    # Selecting one the top half of the population to be produce children. We set the boundary for the top half
    max_val = len(selected_population)-1

    # Keep on creating new children till the required population size has been reached which is 100

    while len(selected_population)<100:

        # Select one of the top 50 parents
        parent1 = random.randint(0, max_val)
        parent2 = random.randint(0, max_val)
        while parent1 == parent2:
            value = random.randint(0, max_val)
            parent2 = random.randint(0, max_val)

        rand_num = random.randint(1, 100)
        child_day = 0
        child_month = 0
        child_year = 0

        # Now randomly do crossover between the parents
        if rand_num <= 50:
            child_day = selected_population[parent1][0]
        else:
            child_day = selected_population[parent2][0]
        rand_num = random.randint(1, 100)
        if rand_num <= 50:
            child_month = selected_population[parent1][1]
        else:
            child_month = selected_population[parent2][1]
        rand_num = random.randint(1, 100)
        if rand_num <= 50:
            child_year = selected_population[parent1][2]
        else:
            child_year = selected_population[parent2][2]

        child = (child_day, child_month, child_year)
        selected_population.append(child)

    # Return the selected population
    return selected_population


def mutator(selected_population):
    """
    Mutate the population on the basis of a certain chance of mutation and range of mutation of value
    :param selected_population: That needs to be mutated
    :return:  population that is mutated
    """
    for i in range(0,len(selected_population)):
        # 15 percent change it is changed
        value = random.randint(1,100)
        if value<=15:
            date = list(selected_population[i])
            date[0] += max(1,min(32,random.randint(-1,1)))
            date[1] += max(1,min(13,random.randint(-1,1)))
            date[2] += max(0,min(9999,random.randint(-1,1)))

            if random.random() < 0.05:
                # 5% chance to force a boundary in one component for checking the boundaries
                boundary_choice = random.choice([0, 1, 2])
                if boundary_choice == 0:
                    date[0] = random.choice([1, 30, 31])
                elif boundary_choice == 1:
                    date[1] = random.choice([1, 12])
                else:
                    date[2] = random.choice([0, 1, 9999])
            selected_population[i] = tuple(date)

    # Return mutated population

    return selected_population

def run_genetic_algo(n):

    """
    This is the genetic algorithm for generating test cases that have cover the maximum number of coverage for
    categories
    :param n: Number of maximum generations of the genetic algorithm to be run for
    :return: Population,Number of generations and count of the number of categories tested
    """

    # Different variables used for setting up the population,local search,getting the required population and
    # calculating coverages for each generation

    count = 0
    population = intialize_population(100)
    tested_categories = set()
    max_test = 0
    answer = population
    max_tested = None
    coverage_per_generations = []
    no_of_generations = n

    # Run the genetic algorithm while specific number of generations or when 96 coverage criteria has been reached
    while count<no_of_generations or 100*(len(tested_categories)/17.0) >= 95:
        tested_categories = set()
        fitness_list = fitness_calculation(population)
        selected = selection(fitness_list)
        crossover_population(selected)
        population = mutator(selected)
        population = list(set(population))
        count+=1

        for test_case in population:
            for category in determine_category(test_case):
                tested_categories.add(category)

        coverage_percent = (max_test / 17.0) * 100
        coverage_per_generations.append(coverage_percent)

        # Compare with the current local maximum

        if max_test<len(tested_categories):
            answer = population
            max_test = len(tested_categories)
            max_tested = tested_categories

    # Print the coverages,the number of generations and also the plot
    print("Coverage Complete = ",max_test/17*100)
    print("Total generations run = ",count)
    plotter.plot(range(1, len(coverage_per_generations) + 1), coverage_per_generations, marker='o', linestyle='-')
    plotter.xlabel("Generation runs")
    plotter.ylabel("Coverage Percentage per generation")
    plotter.title("Genetic Algorithm Coverage Over The Generations")
    plotter.grid(True)
    plotter.show()

    return answer,count,max_tested
def test_validity(test_case):
    # Test if the test cases is valid r not based on their category
    for i in determine_category(test_case):
        if i in invalid_cases:
            return False
    return True
def test_boundary(test_case):
    # Test if the test case if a boundary test case
    for i in determine_category(test_case):
        if i in boundary_cases:
            return True
    return False
def best_test_cases():
    """
    This function is used to run the genetic algorithm and to print the top 10 best valid/invalid test cases and 5 best
    boundary testing cases and also generating the JSON file and plotting the line graph
    :return:None
    """
    count_valid = 0
    count_invalid = 0
    count_boundary = 0
    best_population,categoires_count,category_tested = None,None,None

    # Run the genetic algorithm till we reach this threshold
    while count_valid<10 and count_invalid<10 and count_boundary<5:

        best_population,categoires_count,category_tested = run_genetic_algo(100)
        for test_case in best_population:
            if test_validity(test_case):
                count_valid+=1
            else:
                count_invalid+=1
            if test_boundary(test_case) and test_validity(test_case):
                count_boundary+=1

    # Print the test cases based on if they are valid,invalid or boundary test case and also stored them in a dictionary
    # That will be converted to a JSON file
    best_population.sort(key = lambda x: (-len(determine_category(x))))
    print("Test Cases: ")
    test_cases_dict = {"Valid Test Cases": [], "Invalid Test Cases": [], "Boundary Test Cases": []}
    print("Valid: ")
    count = 0
    for test_case in best_population:
        if count >=10:
            break
        if test_validity(test_case):
            date = f"{test_case[0]:02d}/{test_case[1]:02d}/{test_case[2]:04d}"
            print(date," | Categories "," , ".join(determine_category(test_case)))
            count+=1

    count = 0
    print("Invalid: ")
    for test_case in best_population:
        if count >=10:
            break
        if not test_validity(test_case):
            date = f"{test_case[0]:02d}/{test_case[1]:02d}/{test_case[2]:04d}"
            print(date, " | Categories ", " , ".join(determine_category(test_case)))
            count+=1

    count = 0
    print("Boundary: ")
    for test_case in best_population:
        if count >=5:
            break
        if test_boundary(test_case) and test_validity(test_case):
            date = f"{test_case[0]:02d}/{test_case[1]:02d}/{test_case[2]:04d}"
            print(date, " | Categories ", " , ".join(determine_category(test_case)))
            count += 1

    count = 0
    for test_case in best_population:
        if count >= 10:
            break
        if test_validity(test_case):
            date = f"{test_case[0]:02d}/{test_case[1]:02d}/{test_case[2]:04d}"
            test_cases_dict["Valid Test Cases"].append({
                "date": date,
                "categories_tested": determine_category(test_case)
            })
            count += 1

    count = 0
    for test_case in best_population:
        if count >= 10:
            break
        if not test_validity(test_case):
            date = f"{test_case[0]:02d}/{test_case[1]:02d}/{test_case[2]:04d}"
            test_cases_dict["Invalid Test Cases"].append({
                "date": date,
                "categories_tested": determine_category(test_case)
            })
            count += 1

    count = 0
    for test_case in best_population:
        if count >= 5:
            break
        if test_boundary(test_case) and test_validity(test_case):
            date = f"{test_case[0]:02d}/{test_case[1]:02d}/{test_case[2]:04d}"
            test_cases_dict["Boundary Test Cases"].append({
                "date": date,
                "categories_tested": determine_category(test_case)
            })
            count += 1

    # Save test cases to a JSON file
    with open("best_test_cases.json", "w") as json_file:
        json.dump(test_cases_dict, json_file, indent=4)

    print("Test cases successfully saved to 'best_test_cases.json'!")

best_test_cases()
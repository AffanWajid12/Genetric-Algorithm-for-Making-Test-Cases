import random

valid_cases = ["V:30Day","V:31Day","V:LeapYear","V:NonLeapYear","V:Year","V:Month","V:Day"]
invalid_cases = ["IV:Year","IV:Month","IV:Day","IV:30Day","IV:31Day","IV:LeapYear","IV:28Day"]
boundary_cases = ["V:30DayBoundary","V:31DayBoundary","V:LeapYearBoundary","V:NonLeapYearBoundary","V:Month Boundary","V:Year Boundary"]
category_weights = {
    "V:Year": 0.5,
    "V:Month": 0.5,
    "V:Day": 0.5,
    "V:30Day": 1.0,
    "V:31Day": 1.0,
    "V:LeapYear": 1.5,
    "V:NonLeapYear": 6,
    "V:30DayBoundary": 20,
    "V:31DayBoundary": 20,
    "V:LeapYearBoundary": 40,
    "V:NonLeapYearBoundary": 40,
    "V:Month Boundary": 30,
    "V:Year Boundary": 30,
    "IV:Year": 1.0,
    "IV:Month": 1.0,
    "IV:Day": 1.0,
    "IV:30Day": 20,
    "IV:31Day": 20,
    "IV:LeapYear": 50,
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
    category = []
    day,month,year = test_case

    if year < 0 or year > 9999:
        category.append("IV:Year")
    else:
        category.append("V:Year")

    if month <1 or month >12 :
        category.append("IV:Month")
    else:
        category.append("V:Month")

    if day<1 or day>31:
        category.append("IV:Day")
    else:
        category.append("V:Day")

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
    return category

def fitness_calculation(population):
    counts = {}
    for i in valid_cases:
        counts[i] = 0
    for i in invalid_cases:
        counts[i] = 0
    for i in boundary_cases:
        counts[i] = 0
    fitness_list = []
    #Count the amount of each category
    for date in population:
        category_list = determine_category(date)
        for i in category_list:
            counts[i] += 1
    for date in population:
        category = determine_category(date)
        fitness = 0
        for i in category:

            fitness += category_weights[i]/(counts[i]+1)
        fitness_list.append([date,fitness])
    return fitness_list


def selection(fitness_list):

    for i in range(0,len(fitness_list)):
        for j in range(0,len(fitness_list)):
            if fitness_list[i][1]>fitness_list[j][1]:
                fitness_list[i],fitness_list[j] = fitness_list[j],fitness_list[i]
    end = int(len(fitness_list)/2)
    selected = []
    for i in range(0,int(len(fitness_list)/2)):
        selected.append(fitness_list[i][0])
    return selected


def crossover_population(selected_population):
    while len(selected_population) < 100:
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            while parent1 == parent2:
                parent2 = random.choice(selected_population)
            rand_num = random.randint(1,50)
            child_day = 0
            child_month =0
            child_year = 0
            if rand_num <=50:
                child_day = parent1[0]
            else:
                child_day = parent2[0]
            rand_num = random.randint(1, 50)
            if rand_num <=50:
                child_month = parent1[1]
            else:
                child_month = parent2[1]
            rand_num = random.randint(1, 50)
            if rand_num <=50:
                child_year = parent1[2]
            else:
                child_year = parent2[2]

            child = (child_day,child_month,child_year)
            selected_population.append(child)
    return selected_population

def mutator(selected_population):
    for i in range(0,len(selected_population)):
        # 15 percent change it is changed
        value = random.randint(1,100)
        if value<=15:
            date = list(selected_population[i])
            date[0] += max(1,min(31,random.randint(-1,1)))
            date[1] += max(1,min(12,random.randint(-1,1)))
            date[2] += max(0,min(9999,random.randint(-1,1)))

            if random.random() < 0.05:
                # 5% chance to force a boundary in one component
                boundary_choice = random.choice([0, 1, 2])
                if boundary_choice == 0:
                    date[0] = random.choice([1, 30, 31])
                elif boundary_choice == 1:
                    date[1] = random.choice([1, 12])
                else:
                    date[2] = random.choice([0, 1, 9999])
            selected_population[i] = tuple(date)
    return selected_population

def run_genetic_algo(n):
    count = 0
    population = intialize_population(100)
    tested_categories = set()
    max_test = 0
    answer = population
    max_tested = None
    while count<=n or len(tested_categories)/20.0 > 80:
        tested_categories = set()
        fitness_list = fitness_calculation(population)
        selected = selection(fitness_list)
        crossover_population(selected)
        population = mutator(selected)
        count+=1
        for test_case in population:
            for category in determine_category(test_case):
                tested_categories.add(category)
        print(tested_categories)

        if max_test<len(tested_categories):
            answer = population
            max_test = len(tested_categories)
            max_tested = tested_categories
    print(max_tested)
    print(len(max_tested))
    return answer


print(run_genetic_algo(1000))
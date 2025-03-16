import random
print('works')
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

    day,month,year = test_case

    if year < 0 or year > 9999:
        return "IV:Year"
    if month <1 or month >12 :
        return "IV:Month"
    if day<1 or day>31:
        return"IV:Day"

    if month in [4,6,9,11] and day > 30:
        return "IV:30Day"
    elif month in [4,6,9,11] and day <= 30:
        return "V:30Day"

    if month in [4,6,9,11] and day > 31:
        return "IV:31Day"
    elif month in [1,3,5,7,8,10,12] and day <= 31:
        return "V:31Day"

    if month == 2:
        is_leap = (year %4 ==0 and year %100 !=0 ) or (year % 400 == 0)
        if is_leap and day > 29:
            return "IV:Leap year"
        elif not is_leap and day>28:
            return "IV:28Day"
        elif is_leap:
            "V:LeapYear"

    return "V:Generic Valid"

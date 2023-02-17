import scipy.constants as sc
import math
import pares_data as pd
import numpy as np


def num_of_planets(multiple_data):
    nuMultiple_data = multiple_data.to_numpy()

    # number of planets
    totalPlanets = 1
    FirstPlannet = nuMultiple_data[0][0]
    for i in range(1, len(nuMultiple_data)):
        if nuMultiple_data[i][0] != FirstPlannet:
            totalPlanets += 1
        else:
            break
    return totalPlanets


def simulation_step(data, time_delta):
    """
    Computes the positions of objects after one time_delta
    :param data: a dataframe containing stellar objects' details at a certain time
    :param time_delta: time in seconds to advance positions
    :return: a dataframe containing updated data for the objects
    """
    # my next expected vectors position
    len_data = len(data)  # checks how many planets in the data
    planets_exp_dayX = []  # creates list for expected positionX in each day
    planets_exp_dayY = []  # creates list for expected positionY in each day
    planets_exp_dayZ = []  # creates list for expected positionZ in each day
    dataX = []  # creates list for current positionX in each day
    dataY = []  # creates list for current positionY in each day
    dataZ = []  # creates list for current positionZ in each day
    for i in range(len_data):  # for loop to find expected position
        expected_dayX = data[i][1] + data[i][4] * time_delta
        expected_dayY = data[i][2] + data[i][5] * time_delta
        expected_dayZ = data[i][3] + data[i][6] * time_delta
        dataX.append(data[i][1])  # adds to the list the current positionX of a planet
        dataY.append(data[i][2])  # adds to the list the current positionY of a planet
        dataZ.append(data[i][3])  # adds to the list the current positionZ of a planet
        planets_exp_dayX.append(expected_dayX)  # adds to the list the expected positionX of a planet
        planets_exp_dayY.append(expected_dayY)  # adds to the list the expected positionY of a planet
        planets_exp_dayZ.append(expected_dayZ)  # adds to the list the expected positionz of a planet

    accelaration_old = create_sigmaWM(dataX, dataY, dataZ)  # cur day sigma
    accelaration_new = create_sigmaWM(planets_exp_dayX, planets_exp_dayY, planets_exp_dayZ)  # next day sigma

    velocity_next_day = []
    for i in range(len_data):
        curd0X, curd0Y, curd0Z = accelaration_old[i]  # a0
        curd1X, curd1Y, curd1Z = accelaration_new[i]  # a1

        velocity_next_dayX = data[i][4] + ((curd0X + curd1X) / 2) * time_delta
        velocity_next_dayY = data[i][5] + ((curd0Y + curd1Y) / 2) * time_delta
        velocity_next_dayZ = data[i][6] + ((curd0Z + curd1Z) / 2) * time_delta
        velocity_next_day.append(
            (velocity_next_dayX, velocity_next_dayY, velocity_next_dayZ))  # list of velocity vecors

    position_next_day = []
    for i in range(len_data):
        # Vi+1
        curdayX, curdayY, curdayZ = velocity_next_day[i]
        position_next_dayX = data[i][1] + ((data[i][4] + curdayX) / 2) * time_delta
        position_next_dayY = data[i][2] + ((data[i][5] + curdayY) / 2) * time_delta
        position_next_dayZ = data[i][3] + ((data[i][6] + curdayZ) / 2) * time_delta

        position_next_day.append([data[i][0], position_next_dayX, position_next_dayY,
                                  position_next_dayZ, curdayX, curdayY, curdayZ, data[i][7] + 1,
                                  data[i][8]])  # all the new data foe every day

    return position_next_day


def vector_distance(x1, y1, z1, x2, y2, z2):
    """"
    a function that calculates the vector distance between 2 vectors
    :param
    :return
    """
    return x2 - x1, y2 - y1, z2 - z1


def calc_distance(x1, y1, z1, x2, y2, z2):  #
    """"
    a function that calculates the distance between 2 vectors
    :param
    :return
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def create_sigmaWM(listX, listY, listZ):
    """"
    a function that calculates the Sigma: (-G*Mj*Mi/|r|^3)*r
    for all the planets in a list
    :param
    :return
    """
    len_data = len(listX)
    G = sc.G
    # Sigma: (-G*Mj*Mi/|r|^3)*r
    vec_withOutM = []  # a list of the acceleration vectors

    for i in range(len_data):
        Fx = 0
        Fy = 0
        Fz = 0
        for j in range(len_data):
            if i != j:
                # vector r
                newx, newy, newz = vector_distance(listX[i], listY[i], listZ[i],
                                                   listX[j], listY[j], listZ[j])

                gravconst_e = G * ((pd.data[j][8]) * (pd.data[i][8]))
                # sqrt() ** 3 => () ** 1.5
                dist = (newx ** 2 + newy ** 2 + newz ** 2) ** 1.5
                Fx += gravconst_e * newx / dist
                Fy += gravconst_e * newy / dist
                Fz += gravconst_e * newz / dist

        ax = (Fx / (pd.data[i][8]))
        ay = (Fy / (pd.data[i][8]))
        az = (Fz / (pd.data[i][8]))

        vec_withOutM.append((ax, ay, az))

    return vec_withOutM


def simulate(steps, time_delta):
    """
    Loads initial positions using parse_data.open_data_csv, performs a specified amount of simulation steps with
    time_delta seconds between steps
    :param steps: number of steps to simulate
    :param time_delta: time in seconds to advance positions between steps
    :return: a dataframe containing all objects' positions at all times
    """
    mydata = pd.data
    alldays = []
    # containing the matrixes as rows of ALL THE DAYS!
    forDf = []

    # number of days to simulate
    for i in range(steps):
        alldays.append(mydata)
        for j in range(len(mydata)):
            forDf.append(mydata[j])
        # create the next day
        mydata = simulation_step(mydata, time_delta)
    df = pd.pd.DataFrame(data=forDf, columns=["name", "x", "y", "z", "v_x", "v_y", "v_z", "step", "mass"])

    return df


def get_kinetic_energy(multiple_data):
    """
    Computes the kinetic energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the kinetic energy at each step (list or numpy array)
    """
    npMultiple_dataK = multiple_data.to_numpy()  # changing this data frame to numpy

    daysKE = []  # kinetic energy for each day
    kineticEnergy = 0
    for i in range(len(npMultiple_dataK)):
        if i % 9 == 0 and kineticEnergy != 0:  # one day
            daysKE.append(kineticEnergy)
            kineticEnergy = 0
        kineticEnergy += (1 / 2) * npMultiple_dataK[i][8] * (
                npMultiple_dataK[i][4] ** 2 + npMultiple_dataK[i][5] ** 2 + npMultiple_dataK[i][6] ** 2)
    daysKE.append(kineticEnergy)

    return daysKE


def get_potential_energy(multiple_data):
    """
    Computes the gravitational potential energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the potential energy at each step (list or numpy array)
    """
    # changing this data frame to numpy
    npMultiple_dataP = multiple_data.to_numpy()
    totalPlanets = num_of_planets(multiple_data)

    G = sc.G
    # potential energy for each day
    daysPE = []
    potentialEnergy = 0
    for i in range(len(npMultiple_dataP) + 1):
        if i % totalPlanets == 0 and i != 0:  # one day
            j = i - 9  # for every planet
            k = j + 1  # for every planet besides j in one day
            while j < i:  # all planets in one day
                if k == i:
                    j += 1
                    k = j + 1
                else:
                    potentialEnergy += (-G * npMultiple_dataP[j][8] * npMultiple_dataP[k][8]) / calc_distance(
                        npMultiple_dataP[j][1], npMultiple_dataP[j][2], npMultiple_dataP[j][3],
                        npMultiple_dataP[k][1], npMultiple_dataP[k][2], npMultiple_dataP[k][3])
                    k += 1
            daysPE.append(potentialEnergy)
            potentialEnergy = 0
    return daysPE


def get_total_energy(multiple_data):
    """
    Computes the total energy of the system as a function of simulation step
    :param multiple_data: a DataFrame containing planet data for many steps
    :return: the total energy at each step (list or numpy array)
    """
    PE = get_potential_energy(multiple_data)
    KE = get_kinetic_energy(multiple_data)
    TOTenergy = []
    for i in range(len(PE)):  # 365 days
        energy_total = PE[i] + KE[i]  # sum the kinetic energy with the potential energy for one day
        TOTenergy.append(energy_total)  # total energy for every day
    return TOTenergy


def get_sun_distances(multiple_data, planet_name):
    """
    Computes the distance of a planet from the sun as a function of time
    :param multiple_data: object data returned from simulate
    :param planet_name: the name of the planet to find distances from the sun (a string)
    :return: list/array of distances of the planet from the sun (at different times)
    """
    npMultiple_data = multiple_data.to_numpy()
    sun_distances = []
    planet_index = sun_index = 0
    foundPlanet = False
    foundSun = False
    while planet_index < len(multiple_data) and sun_index < len(multiple_data):
        if foundPlanet is False or foundSun is False:
            if npMultiple_data[planet_index][0] != planet_name:  # not the planet that i want
                planet_index += 1  # try the one after
            else:
                foundPlanet = True  # the planet I want
            if npMultiple_data[sun_index][0] != 'sun':  # if the planet is not the sun
                sun_index += 1  # try the one after
            else:
                foundSun = True  # found the sun
        else:
            cur_sun_dist = calc_distance(npMultiple_data[planet_index][1], npMultiple_data[planet_index][2],
                                         npMultiple_data[planet_index][3],
                                         npMultiple_data[sun_index][1], npMultiple_data[sun_index][2],
                                         npMultiple_data[sun_index][3])  # distance from planet to the sun for one day
            sun_distances.append(cur_sun_dist)  # distance from planet to the sun for one day
            planet_index += 9  # the next day
            sun_index += 9
    return sun_distances


def get_orbit_period(sun_distances):
    """
    Estimates the orbital period (in simulation steps) of a planet from the time series of distances from the sun
    :param sun_distances: a list of distances from the sun (as a function of time)
    :return: the estimated period of the motion
    """
    sun_distances_orb = np.array(sun_distances)
    sun_dist = np.average(sun_distances_orb)  # avg distance of a planet from the sun
    G = sc.G
    pie = math.pi
    sun_mass = pd.data[6][8]  # mass of the sun
    time_orbit = math.sqrt((4 * pie ** 2 * sun_dist ** 3) / (G * sun_mass))  # gets the time in seconds
    return time_orbit


if __name__ == "__main__":
    data = simulate(365, 86400)
    get_potential_energy(data)

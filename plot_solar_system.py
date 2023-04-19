import simulation as simu
import matplotlib.pyplot as plt
import numpy as nu


def plot_trajectory(multiple_data):
    """
    Plots the trajectory and current position of objects, from a dataframe containing positions at multiple times
    :param multiple_data: object data returned from simulate
    """
    ax = plt.figure().add_subplot(projection='3d')  # to make a 3D enviorment
    planets = multiple_data.head(9).copy()  # get all the 9 planets
    names = planets['name'].to_numpy()  # make a numpay array of all the planets names
    for name in names:
        colX = nu.array(multiple_data.loc[multiple_data['name'] == name, 'x'])  # position X of every planet
        colY = nu.array(multiple_data.loc[multiple_data['name'] == name, 'y'])  # position y of every planet
        colZ = nu.array(multiple_data.loc[multiple_data['name'] == name, 'z'])  # position z of every planet
        ax.plot(colX, colY, colZ, label=name)
    ax.legend()
    plt.show()


def plot_sun_distances(multiple_data):
    """
    Plots the distance of planets from the sun as a function of time
    :param multiple_data: object data returned from simulate
    """
    nuMultiple_data = multiple_data.to_numpy()

    # number of planets
    totalPlanets = simu.num_of_planets(multiple_data)

    for i in range(totalPlanets):
        if nuMultiple_data[i][0] != 'sun':  # if the planet is not the sun plot the distance from the sun
            sun_dists = simu.get_sun_distances(multiple_data, nuMultiple_data[i][0])
            days = [i for i in range(len(sun_dists))]
            plt.plot(days, sun_dists, label=nuMultiple_data[i][0])
            plt.title('sun distances')
    plt.legend()
    plt.show()


def plot_kepler_third_law(multiple_data):
    """
    Plots the (orbital period)^2 of planet's motion as a function of (mean distance to the sun)^3
    :param multiple_data: object data returned from simulate
    """
    # number of planets
    totalPlanets = simu.num_of_planets(multiple_data)
    x = []
    y = []
    for i in range(totalPlanets):
        numultiple_data = multiple_data.to_numpy()
        planet_name = numultiple_data[i][0]
        sun_dist = simu.get_sun_distances(multiple_data, planet_name)
        orbit_period_sq = simu.get_orbit_period(sun_dist) ** 2  # the formula for time orbit squered
        sun_dist = nu.array(sun_dist)
        radius = nu.average(sun_dist) ** 3
        x.append(radius)
        y.append(orbit_period_sq)
    plt.plot(x, y)
    plt.title('kepler third law')
    plt.show()


def plot_KE(multiple_data):
    """
    Plot of kinetic energy of the system as a function of time
    :param multiple_data: object data returned from simulate
    """
    daysKE = simu.get_kinetic_energy(multiple_data)
    days = [i for i in range(len(daysKE))]
    plt.plot(days, daysKE, label="Kinetic Energy")
    plt.legend()
    plt.show()

def plot_PE(multiple_data):
    """
    Plot of potential energy of the system as a function of time
    :param multiple_data: object data returned from simulate
    """
    daysPE = simu.get_potential_energy(multiple_data)
    days = [i for i in range(len(daysPE))]
    plt.plot(days, daysPE, label="Potential Energy")
    plt.legend()
    plt.show()

def plot_ToTE(multiple_data):
    """
    Plot of total energy of the system as a function of time
    :param multiple_data: object data returned from simulate
    """
    TOTenergy = simu.get_total_energy(multiple_data)
    days = [i for i in range(len(TOTenergy))]
    plt.plot(days, TOTenergy, label="Total Energy")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    years = input("Welcome :)\n"
          "For how many years would you like to see the simulation?\n")
    if years.isdigit():
        opperations = [plot_trajectory,plot_sun_distances,plot_kepler_third_law,plot_KE,plot_PE,plot_ToTE]
        years = int(years)*365
        data = simu.simulate(years, 86400)# 86400 = seconds in a single day = (seconds in a minute)*(minutes in an hour)*(hours in a day)
        print("allright, what would you like to see now?:\n")
        while True:
            option = input(
                  "1.Trajectory\n"
                  "2.Sun distances\n"
                  "3.Kepler third law\n"
                  "4.Kinetic energy\n"
                  "5.potentional energy\n"
                  "6.total energy that spent\n"
                  "7.Change year\n"
                  "8.Exit program\n")
            if option.isdigit():
                option = int(option)
                if 1 <= option <= 6:
                    print("before trying a new option, please exit from the plot")
                    opperations[option-1](data)
                elif option == 7:
                    oldYear = years
                    years = input("insert here the new year :)\n")
                    if years.isdigit():
                        print("this number is valid,changeing time line.")
                        years = int(years) * 365
                        data = simu.simulate(years, 86400)
                    else:
                        print("Failed to change year. keeping the last years option")
                        years = oldYear
                elif option == 8:
                    print("goodbye!:)")
                    break
                else:
                    print("Invalid option. goodbye! :)")
                    break
                print("allright, whats next?")
    else:
        print("Invalid year. goodbye! :)")

#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()


        step = step + 1
        if (step == 100):
            traci.route.add('route1', ["0a", "8"])
            traci.vehicle.add('carX', 'route1', typeID="reroutingType")
            print(traci.vehicle.getRouteID('carX'))
            print('***************')

        if (step <= 200):
            x, y = traci.vehicle.getPosition('car1')
            lon, lat = traci.simulation.convertGeo(x, y)
            print(lon, lat)
            # x2, y2 = traci.simulation.convertGeo(lon, lat, fromGeo=True)
            # print(x2, y2)

        if (step == 200):
            print('***************')
            print(traci.vehicle.getAccel("car1"))
            print(traci.vehicle.getRouteID('car1'))
            print(traci.vehicle.getLanePosition('car1'))
            print(traci.vehicle.getRoute('carX'))
            print(traci.vehicle.getRouteIndex('car1'))



        if (step == 220):
            traci.vehicle.remove('car1')

    print(step)

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "parking.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()

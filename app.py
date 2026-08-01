import sys, subprocess, platform, copy

defaultProcesses = {
    # Name: {processing time: minutes (int), downtime: minutes (int), defect rate: as a decimal, daily: capacity}
    "Frame Assembly":       {"processing time":8.0, "downtime":0.0, "defect rate":0.01, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Wheel Installation":   {"processing time":12.0, "downtime":0.05, "defect rate":0.03, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Brake Installation":   {"processing time":7.0, "downtime":0.0, "defect rate":0.02, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Quality Inspection":   {"processing time":9.0, "downtime":0.0, "defect rate":0.01, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Packaging":            {"processing time":5.0, "downtime":0.0, "defect rate":0.005, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
}

factoryUpgrades = {
    "Faster Wheel Equipment": {"bought":False, "cost":20000, "description": "Wheel time -4 min"},
    "Additional Brake Workstation": {"bought":False, "cost":15000, "description": "Brake capacity doubles"},
    "Better Inspection equipment": {"bought":False, "cost":12000, "description": "Inspection time -3 min"},
    "Worker Training": {"bought":False, "cost":8000, "description": "Defects reduced by 40%"},
    "Conveyor Improvement": {"boug4ht":False, "cost":10000, "description": "Reduce each station processing time by 0.5 min"}
}

factoryAttributes = {
    "workingMinutes": 480.0,
    "sellingPrice": 160.0,
    "customerDemand": 55.0,
    "currentBudget": 30000.0,
    "systemCapacity": 0.0,
    "systemYield": 0.0,
    "bottleneck": "",
    "profitPerBike": 160.0,
    "dailyProfit": 0.0,
    "year": 2026,
}

simluationProcesses = {}
simulationUpgrades = {}
simulationAttributes = {}

def calculateStationCapacity(processes, attributes):
    for i in processes:
        pt = processes[i]["processing time"]
        capacity = attributes['workingMinutes']/pt
        capacity *= (1-processes[i]["downtime"])
        processes[i]["daily"] = capacity

def calculateSystemCapacity(processes, attributes):
    calculateStationCapacity(processes, attributes)

    tempSysCap = float('inf')
    for i in processes:
        if processes[i]["daily"] < tempSysCap:
            tempSysCap = processes[i]["daily"]
    attributes['systemCapacity'] = tempSysCap

def calculateProcessYield(processes, attributes):
    calculateSystemCapacity(processes, attributes)

    productionMultiplier = 1.0
    individualProductionMultipler = 1.0
    for i in processes:
        productionMultiplier *= (1-processes[i]["defect rate"])
        individualProductionMultipler = 1 * (1-processes[i]["defect rate"]) * (1-processes[i]["downtime"])
        processes[i]["yield"] = processes[i]["daily"] * individualProductionMultipler
        individualProductionMultipler = 1.0
    attributes['systemYield'] = attributes['systemCapacity'] * productionMultiplier
    
def calculateBottleneck(processes, attributes):
    calculateSystemCapacity(processes, attributes)

    for processName in processes:
        if processes[processName]["daily"] <= attributes['systemCapacity']:
            attributes['bottleneck'] = processName

def calculateDailyProfit(processes, attributes):
    calculateProcessYield(processes, attributes)

    attributes['dailyProfit'] = attributes['systemYield'] * attributes['profitPerBike']

def calculateUtilization(processes, attributes):
    calculateSystemCapacity(processes, attributes)
    
    for i in processes:
        processes[i]["utilization"] = attributes['systemCapacity']/processes[i]["daily"]


def calculateIdleCapacity(processes,attributes):
    calculateSystemCapacity(processes,attributes)

    for i in processes:
        processes[i]["idle"] = processes[i]["daily"] - attributes['systemCapacity']

def clearConsole():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def updateNumbers(processes, attributes):
    calculateUtilization(processes, attributes)
    calculateIdleCapacity(processes, attributes)
    calculateDailyProfit(processes, attributes)
    calculateBottleneck(processes, attributes)

def getInt(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number.")

def getFloat(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")


def createMenu(processes, attributes):
    updateNumbers(processes, attributes)
    while True:
        userChoice = None
        print("=====================================")
        print("Velocity Cycles Manufacturing Simulator")
        print("=====================================")
        print(f"Current Year: {attributes['year']}")
        print(f"Customer Demand: {attributes['customerDemand']} bikes/day")
        print(f"Production: {attributes['systemYield']} bikes/day")
        print(f"Current Bottleneck: {attributes['bottleneck']}")
        print(f"Budget Remaining: ${attributes['currentBudget']}")
        print("   1. View Factory")
        print("   2. Modify Factory")
        print("   3. Invest in Improvements")
        print("   4. Run Future Simulation")
        print("   5. View Financial Report")
        print("   6. Exit")


        userChoice = getInt("Select an option: ")
        match userChoice:
            case 1:
                viewFactory(processes, attributes)
            case 2:
                modifyFactory(processes, attributes)
            case 3:
                investImprove(processes, attributes)
            case 4:
                runSimulation()
            case 5: 
                ViewFinancials()
            case 6: 
                sys.exit()
            case _:
                print("unknown input")

def viewFactory(processes, attributes):
    while True:
        print("============")
        print("View Factory")
        print("============")

        for i, process in enumerate(processes, start=1):
            print(str(i) + ". " + str(process))
        print(str(len(processes) + 1) + ". Factory Stats")
        print(str(len(processes) + 2) + ". Return")

        while True:
            userChoice = getInt("Choose an option: ")

            if 1 <= userChoice <= len(processes) + 2:
                break
            else:
                print("Please choose a valid option.")
        if userChoice == len(processes) + 2:
            return()
        if userChoice == len(processes) + 1:
            print(f"Factory Stats:")
            print(f"   Working Minutes: {attributes['workingMinutes']}")
            print(f"   Selling Price: {attributes['sellingPrice']}")
            print(f"   Customer Demand: {attributes['customerDemand']}")
            print(f"   Current Budget: {attributes['currentBudget']}")
            print(f"   System Capacity: {attributes['systemCapacity']}")
            print(f"   System Yield: {attributes['systemYield']}")
            print(f"   Bottleneck: {attributes['bottleneck']}")
            print(f"   Profit Per Bike: {attributes['profitPerBike']}")
            print(f"   Daily Profits: {attributes['dailyProfit']}")
        else:
            listOfProcesses = list(processes.keys())
            selectedProcess = listOfProcesses[userChoice - 2]
            print(f"{selectedProcess}:")
            print(f"   Processing Time: {processes[selectedProcess]['processing time']}")
            print(f"   Downtime: {processes[selectedProcess]['downtime']}")
            print(f"   Defect Rate: {processes[selectedProcess]['defect rate']}")
            print(f"   Daily Capacity: {processes[selectedProcess]['daily']}")
            print(f"   Process Yield: {processes[selectedProcess]['yield']}")
            print(f"   Utilization: {processes[selectedProcess]['utilization']}")
            print(f"   Idle Capacity: {processes[selectedProcess]['idle']}")
    
def modifyFactory(processes, attributes):
    while True:
        choice = None
        print("==============")
        print("Modify Factory")
        print("==============")

        for i, process in enumerate(processes, start=1):
            print(f"   {i}. {process}")
        print(f"   {len(processes) + 1}. Factory Stats")
        print(f"   {len(processes) + 2}. Return")

        while True:
            userChoice = getInt("Choose an option: ")

            if 1 <= userChoice <= len(processes) + 2:
                break
            else:
                print("Please choose a valid option.")

        if userChoice == len(processes) + 2:
            return()
        if userChoice == len(processes) + 1:
            print(f"Factory Stats:")
            print(f"   1. Working Minutes: {attributes['workingMinutes']}")
            print(f"   2. Selling Price: {attributes['sellingPrice']}")
            print(f"   3. Customer Demand: {attributes['customerDemand']}")
            print(f"   4. Current Budget: {attributes['currentBudget']}")
            print(f"   5. Profit Per Bike: {attributes['profitPerBike']}")
            print(f"   6. Return")
            while True:
                userChoice = getInt("Choose an option: ")

                match userChoice:
                    case 1:
                        attributes['workingMinutes'] = getFloat("Choose new value: ")
                    case 2:
                        attributes['sellingPrice'] = getFloat("Choose new value: ")
                    case 3:
                        attributes['customerDemand'] = getFloat("Choose new value: ")
                    case 4:
                        attributes['currentBudget'] = getFloat("Choose new value: ")
                    case 5:
                        attributes['profitPerBike'] = getFloat("Choose new value: ")
                    case 6:
                        return
                updateNumbers(processes, attributes)   
        else:
            updateNumbers(processes, attributes)
            listOfProcesses = list(processes.keys())
            selectedProcess = listOfProcesses[userChoice - 1]
            print(f"{selectedProcess}:")
            print(f"   1. Processing Time: {processes[selectedProcess]['processing time']}")
            print(f"   2. Downtime: {processes[selectedProcess]['downtime']}")
            print(f"   3. Defect Rate: {processes[selectedProcess]['defect rate']}")
            print(f"   4. Return")
            while True:
                userChoice = getInt("Choose an option: ")

                match userChoice:
                    case 1:
                        processes[selectedProcess]['processing time'] = getFloat("Choose new value: ")
                    case 2:
                        processes[selectedProcess]['downtime'] = getFloat("Choose new value: ")
                    case 3:
                        processes[selectedProcess]['defect rate'] = getFloat("Choose new value: ")
                    case 4:
                        return
                updateNumbers(processes, attributes)


def investImprove(processes, attributes):
    while True:
        print("===============")
        print("Upgrade Factory")
        print("===============")
        print(f"Budget Available: ${attributes['currentBudget']}")
        for i, upgrade in enumerate(factoryUpgrades, start=1):
            print(f"   {i}. ${factoryUpgrades[upgrade]['cost']} - {upgrade} - {factoryUpgrades[upgrade]['bought']}")
        print(f"   {len(factoryUpgrades) + 1}. Return")

        while True:
            userChoice = getInt("Choose an option: ")

            if 1 <= userChoice <= len(factoryUpgrades) + 1:
                break
            else:
                print("Please choose a valid option.")

        if userChoice == len(factoryUpgrades) + 1:
            return
        else:
            listOfUpgrades = list(factoryUpgrades.keys())
            selectedUpgrade = listOfUpgrades[userChoice - 1]
            print(f"{selectedUpgrade} selected!")
            print(f"   {factoryUpgrades[selectedUpgrade]['description']}")
            print(f"   1. Buy")
            print(f"   2. Do not")
            userChoice = getInt("Purchase? ")
            match userChoice:
                case 1:
                    if factoryUpgrades[selectedUpgrade]["cost"] <= attributes['currentBudget'] and factoryUpgrades[selectedUpgrade]["bought"] == False:
                        attributes['currentBudget'] -= factoryUpgrades[selectedUpgrade]["cost"]
                        factoryUpgrades[selectedUpgrade]["bought"] = True
                        purchaseUpgrade(selectedUpgrade, processes, attributes)
                case 2:
                    return
            updateNumbers(processes, attributes)

def purchaseUpgrade(selectedUpgrade, processes, attributes):
    print(selectedUpgrade)
    if selectedUpgrade == "Faster Wheel Equipment":
        if processes["Wheel Installation"]["processing time"] > 4:
            processes["Wheel Installation"]["processing time"] -= 4
    elif selectedUpgrade == "Additional Brake Workstation":
        processes[selectedUpgrade]["processing time"] /= 2
    elif selectedUpgrade == "Better Inspection equipment":
        if processes["Brake Installation"]["processing time"] > 3:
            processes["Brake Installation"]["processing time"] -= 3
    elif selectedUpgrade == "Worker Training":
        for process in processes:
            processes[process]["defect rate"] *= 0.6
    elif selectedUpgrade == "Conveyor Improvement":
        for process in processes:
            if processes[process]["processing time"] > 0.5:
                processes[process]["processing time"] -= 0.5
    updateNumbers(processes, attributes)

def runSimulation():
    simluationProcesses = copy.deepcopy(defaultProcesses)
    print("==============")
    print("Run Simulation")
    print("==============")
    # print(f"   Current Year: {year}")
    # print(f"   Current Budget: {currentBudget}")
    # print(f"   Current Demand: {customerDemand}")
    print(f"   1. Option")

def ViewFinancials():
    print("ViewFinancials")













createMenu(defaultProcesses, factoryAttributes)


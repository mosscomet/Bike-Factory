import sys, subprocess, platform, copy, random

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
    "Conveyor Improvement": {"bought":False, "cost":10000, "description": "Reduce each station processing time by 0.5 min"}
}

factoryAttributes = {
    "workingMinutes": 480.0,
    "customerDemand": 55.0,
    "currentBudget": 30000.0,
    "systemCapacity": 0.0,
    "systemYield": 0.0,
    "bottleneck": "",
    "profitPerBike": 160.0,
    "dailyProfit": 0.0,
    "year": 2026,
    "annualProfit": 0,
}

simluationProcesses = {}
simulationUpgrades = {}
simulationAttributes = {}

simulationDemandIncrease = 1.05
simulationBudgetIncrease = 5000

simulationRandomEvents = {
    "Supplier Delay": "Delays have increased downtime",
    "Demand Decrease": "Customers want fewer bicycles",
    "Quality Decrease": "Defect rates have gone up",
    "Quality Improvement": "Defect rates have gone down",
    "Equipment Breakdown": "suffers a decrease in production",
    "Selling Price Changes": "The selling price of bicycles has changed",
}

def calculateStationCapacity(processes, attributes):
    for i in processes:
        pt = processes[i]["processing time"]
        capacity = attributes['workingMinutes']/pt
        capacity *= (1-processes[i]["downtime"])
        processes[i]["daily"] = capacity

# # calc only one station at a time
# def singleStationCapacity(processes, attributes, index):
#     pt = processes[index]["processing time"]
#     capacity = attributes['workingMinutes']/pt
#     capacity *= (1-processes[i]["downtime"])
#     processes[index]["daily"] = capacity

# # use single station to calc all stations
# def calculateMultipleStationCapacities(processes, attributes):
#     for i in processes:
#         singleStationCapacity(processes, attributes, i)

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

def calculateAnnualProfit(processes, attributes):
    calculateDailyProfit(processes, attributes)

    attributes['annualProfit'] = attributes['dailyProfit'] * 365

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
    calculateAnnualProfit(processes, attributes)
    calculateBottleneck(processes, attributes)

def validateInt(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number.")

def validateFloat(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")

def createMenu(processes, upgrades, attributes, randomEvents):
    updateNumbers(processes, attributes)
    while True:
        userChoice = None
        print("\n=======================================")
        print("Velocity Cycles Manufacturing Simulator")
        print("=======================================")
        print(f"Current Year: {attributes['year']}")
        print(f"Customer Demand: {attributes['customerDemand']:.2f} bikes/day")
        print(f"Production: {attributes['systemYield']:.2f} bikes/day")
        print(f"Current Bottleneck: {attributes['bottleneck']}")
        print(f"Budget Remaining: ${attributes['currentBudget']:.2f}")
        recommendUpgrade(processes, upgrades, attributes)
        print("   1. View Factory")
        print("   2. Modify Factory")
        print("   3. Invest in Improvements")
        print("   4. Run Future Simulation")
        print("   5. View Financial Report")
        print("   6. Exit")


        userChoice = validateInt("Select an option: ")
        match userChoice:
            case 1:
                viewFactory(processes, attributes)
            case 2:
                modifyFactory(processes, attributes)
            case 3:
                investImprove(processes, upgrades, attributes)
            case 4:
                runSimulation(processes, upgrades, attributes, randomEvents)
            case 5: 
                viewFinancials(attributes)
            case 6: 
                sys.exit()
            case _:
                print("unknown input")
        clearConsole()

def viewFactory(processes, attributes):
    while True:
        print("\n============")
        print("View Factory")
        print("============")

        for i, process in enumerate(processes, start=1):
            print(str(i) + ". " + str(process))
        print(str(len(processes) + 1) + ". Factory Stats")
        print(str(len(processes) + 2) + ". Return")

        while True:
            userChoice = validateInt("Choose an option: ")

            if 1 <= userChoice <= len(processes) + 2:
                break
            else:
                print("Please choose a valid option.")
        if userChoice == len(processes) + 2:
            return()
        if userChoice == len(processes) + 1:
            print(f"\nFactory Stats:")
            print(f"   Working Minutes: {attributes['workingMinutes']:.2f}")
            print(f"   System Capacity: {attributes['systemCapacity']:.2f}")
            print(f"   System Yield: {attributes['systemYield']:.2f}")
            print(f"   Customer Demand: {attributes['customerDemand']:.2f}")
            print(f"   Bottleneck: {attributes['bottleneck']}")
            print(f"   Current Budget: ${attributes['currentBudget']:.2f}")
            print(f"   Profit Per Bike: ${attributes['profitPerBike']:.2f}")
            print(f"   Daily Profits: ${attributes['dailyProfit']:.2f}")
            print(f"   1. Return")
            goBack = input()
        else:
            listOfProcesses = list(processes.keys())
            selectedProcess = listOfProcesses[userChoice - 2]
            print(f"\n{selectedProcess}:")
            print(f"   Processing Time: {processes[selectedProcess]['processing time']:.2f}")
            print(f"   Downtime: {processes[selectedProcess]['downtime']:.4f}")
            print(f"   Defect Rate: {processes[selectedProcess]['defect rate']*100:.2f}%")
            print(f"   Daily Capacity: {processes[selectedProcess]['daily']:.2f}")
            print(f"   Process Yield: {processes[selectedProcess]['yield']:.2f}")
            print(f"   Utilization: {processes[selectedProcess]['utilization']*100:.2f}%")
            print(f"   Idle Capacity: {processes[selectedProcess]['idle']:.2f}")
            print(f"   1. Return")
            goBack = input()
    
def modifyFactory(processes, attributes):
    while True:
        print("\n==============")
        print("Modify Factory")
        print("==============")

        for i, process in enumerate(processes, start=1):
            print(f"   {i}. {process}")
        print(f"   {len(processes) + 1}. Factory Stats")
        print(f"   {len(processes) + 2}. Return")

        while True:
            userChoice = validateInt("Choose an option: ")

            if 1 <= userChoice <= len(processes) + 2:
                break
            else:
                print("Please choose a valid option.")

        if userChoice == len(processes) + 2:
            return()
        if userChoice == len(processes) + 1:
            while True:
                print(f"\nFactory Stats:")
                print(f"   1. Working Minutes: {attributes['workingMinutes']}")
                print(f"   2. Customer Demand: {attributes['customerDemand']}")
                print(f"   3. Current Budget: ${attributes['currentBudget']}")
                print(f"   4. Profit Per Bike: ${attributes['profitPerBike']}")
                print(f"   5. Return")
                userChoice = validateInt("Choose an option: ")

                match userChoice:
                    case 1:
                        attributes['workingMinutes'] = validateFloat("Choose new value: ")
                    case 2:
                        attributes['customerDemand'] = validateFloat("Choose new value: ")
                    case 3:
                        attributes['currentBudget'] = validateFloat("Choose new value: ")
                    case 4:
                        attributes['profitPerBike'] = validateFloat("Choose new value: ")
                    case 5:
                        return
                updateNumbers(processes, attributes)   
        else:
            updateNumbers(processes, attributes)
            listOfProcesses = list(processes.keys())
            selectedProcess = listOfProcesses[userChoice - 1]
            while True:
                print(f"\n{selectedProcess}:")
                print(f"   1. Processing Time: {processes[selectedProcess]['processing time']}")
                print(f"   2. Downtime: {processes[selectedProcess]['downtime']}")
                print(f"   3. Defect Rate: {processes[selectedProcess]['defect rate']*100:.2f}%")
                print(f"   4. Return")
                userChoice = validateInt("Choose an option: ")

                match userChoice:
                    case 1:
                        processes[selectedProcess]['processing time'] = validateFloat("Choose new value: ")
                    case 2:
                        processes[selectedProcess]['downtime'] = validateFloat("Choose new value: ")
                    case 3:
                        processes[selectedProcess]['defect rate'] = validateFloat("Choose new value: ")
                    case 4:
                        return
                updateNumbers(processes, attributes)


def investImprove(processes, upgrades, attributes):
    while True:
        print("\n===============")
        print("Upgrade Factory")
        print("===============")
        print(f"Budget Available: ${attributes['currentBudget']}")
        for i, upgrade in enumerate(upgrades, start=1):
            print(f"   {i}. ${upgrades[upgrade]['cost']} - {upgrade} - {upgrades[upgrade]['bought']}")
        print(f"   {len(upgrades) + 1}. Return")

        while True:
            userChoice = validateInt("Choose an option: ")

            if 1 <= userChoice <= len(upgrades) + 1:
                break
            else:
                print("Please choose a valid option.")

        if userChoice == len(upgrades) + 1:
            return
        else:
            listOfUpgrades = list(upgrades.keys())
            selectedUpgrade = listOfUpgrades[userChoice - 1]
            print(f"\n{selectedUpgrade} selected:")
            print(f"   Effect: {upgrades[selectedUpgrade]['description']}")
            print(f"   1. Buy")
            print(f"   2. Do not")
            userChoice = validateInt("Purchase? ")
            match userChoice:
                case 1:
                    if upgrades[selectedUpgrade]['cost'] <= attributes['currentBudget'] and upgrades[selectedUpgrade]['bought'] == False:
                        purchaseUpgrade(selectedUpgrade, processes, upgrades, attributes)
                    elif upgrades[selectedUpgrade]['bought'] == True:
                        print("Already purchased.")
                    else:
                        print("Cannot afford upgrade.")
                case 2:
                    return
            updateNumbers(processes, attributes)

def purchaseUpgrade(selectedUpgrade, processes, upgrades, attributes):
    if selectedUpgrade == "Faster Wheel Equipment":
        if processes["Wheel Installation"]["processing time"] > 4:
            processes["Wheel Installation"]["processing time"] -= 4
            attributes['currentBudget'] -= upgrades[selectedUpgrade]['cost']
            upgrades[selectedUpgrade]['bought'] = True
    
    elif selectedUpgrade == "Additional Brake Workstation":
        processes["Brake Installation"]["processing time"] /= 2
        attributes['currentBudget'] -= upgrades[selectedUpgrade]['cost']
        upgrades[selectedUpgrade]['bought'] = True
    
    elif selectedUpgrade == "Better Inspection equipment":
        if processes["Brake Installation"]["processing time"] > 3:
            processes["Brake Installation"]["processing time"] -= 3
            attributes['currentBudget'] -= upgrades[selectedUpgrade]['cost']
            upgrades[selectedUpgrade]['bought'] = True
    
    elif selectedUpgrade == "Worker Training":
        for process in processes:
            processes[process]["defect rate"] *= 0.6
        attributes['currentBudget'] -= upgrades[selectedUpgrade]['cost']
        upgrades[selectedUpgrade]['bought'] = True
    
    elif selectedUpgrade == "Conveyor Improvement":
        for process in processes:
            if processes[process]["processing time"] > 0.5:
                processes[process]["processing time"] -= 0.5
        attributes['currentBudget'] -= upgrades[selectedUpgrade]['cost']
        upgrades[selectedUpgrade]['bought'] = True
    
    updateNumbers(processes, attributes)

def runSimulation(processes, upgrades, attributes, randomEvents):
    simluationProcesses = copy.deepcopy(processes)
    simulationUpgrades = copy.deepcopy(upgrades)
    simulationAttributes = copy.deepcopy(attributes)
    
    while True:
        print("\n==============")
        print("Run Simulation")
        print("==============")
        print(f"Year: {simulationAttributes['year']}")
        print(f"Budget: ${simulationAttributes['currentBudget']:.2f}")
        print(f"Annual Profit: ${simulationAttributes['annualProfit']:.2f}")
        print(f"Demand: {simulationAttributes['customerDemand']:.2f}")
        print(f"Production: {simulationAttributes['systemYield']:.2f} bikes/day")
        print(f"Bottleneck: {simulationAttributes['bottleneck']}")
        recommendUpgrade(simluationProcesses, simulationUpgrades, simulationAttributes)
        print(f"    1. Step forward 1 year")
        print(f"    2. Upgrade Factory")
        print(f"    3. View Factory")
        print(f"    4. Exit")
        userChoice = validateInt("Select an option: ")
        match userChoice:
            case 1:
                stepForwardOneYear(simulationAttributes)
                randomEvent(simluationProcesses, simulationUpgrades, simulationAttributes, randomEvents)
            case 2:
                investImprove(simluationProcesses, simulationUpgrades, simulationAttributes)
            case 3:
                viewFactory(simluationProcesses, simulationAttributes)
            case 4: 
                return
        

def stepForwardOneYear(attributes):
    print(f"Customer Demand Increase: {attributes['customerDemand']:.2f} -> {(attributes['customerDemand'] * simulationDemandIncrease):.2f}")
    attributes['customerDemand'] *= simulationDemandIncrease
    print(f"Budget Increase: {attributes['currentBudget']} -> {attributes['currentBudget'] + simulationBudgetIncrease}")
    attributes['currentBudget'] += simulationBudgetIncrease
    attributes['year'] += 1
    viewFinancials(attributes)
    

def randomEvent(processes, upgrades, attributes, randomEvents):
    event = random.choice(list(simulationRandomEvents.keys()))
    print(f"\n===Random Event===")
    match event:
        case "Supplier Delay":
            downtime = random.uniform(0.01, 0.03)
            for i in processes:
                if processes[i]['defect rate'] + downtime < 1:
                    processes[i]['defect rate'] += downtime
                processes[i]['downtime'] += downtime
            print(f"Supplier Delay: {randomEvents[event]}, +{round(downtime,5)*100}% on all stations")

        case "Demand Decrease":
            demandDec = random.randint(1, 10)
            attributes['customerDemand'] -= demandDec
            print(f"Demand Decrease: {randomEvents[event]}, -{demandDec} demand")

        case "Quality Decrease":
            defect = random.uniform(0.01, 0.03)
            for i in processes:
                if processes[i]['defect rate'] + defect < 1:
                    processes[i]['defect rate'] += defect
            print(f"Quality Decrease: {randomEvents[event]}, +{round(defect,5)*100}% error on all stations")

        case "Quality Improvement":
            defect = random.uniform(0.01, 0.03)
            if upgrades["Worker Training"]["bought"]:
                defect *= 0.6
            for i in processes:
                if processes[i]['downtime'] > defect:
                    processes[i]['downtime'] -= defect
            print(f"Quality Increase: {randomEvents[event]}, -{round(defect,5)*100}% error on all stations")

        case "Equipment Breakdown":
            mult = random.uniform(0.8, 1.00)
            station = random.choice(list(processes.keys()))
            processes[station]['downtime'] *= mult
            print(f"Equipment Breakdown: {station} {randomEvents[event]}, -{round((1-mult),5)*100}% decrease in capacity")

        case "Selling Price Changes":
            change = random.randint(-10,10)
            attributes['profitPerBike'] += change
            if change > 0:
                print(f"Selling Price Changes: {randomEvents[event]}, ${change} increase")
            else:
                print(f"Selling Price Changes: {randomEvents[event]}, ${abs(change)} decrease")
            
    updateNumbers(processes, attributes)
    calculateBottleneck(processes, attributes)

def viewFinancials(attributes):
    print("\n===============")
    print("View Financials")
    print("===============")
    print(f"Production Capacity: {attributes['systemCapacity']:.2f}")
    print(f"Good Bicycles Produced: {attributes['systemYield']:.2f}")
    print(f"Daily Profit: ${attributes['dailyProfit']:.2f}")
    print(f"Annual Profit: ${attributes['annualProfit']:.2f}")
    print(f"Budget Remaining: ${attributes['currentBudget']:.2f}")
    print(f"Bottleneck: {attributes['bottleneck']}")
    if attributes['customerDemand'] > attributes['systemYield']: # Lost Sales:
        print(f"Remaining Potential Sales: {(attributes['customerDemand']-attributes['systemYield']):.2f}")
    else:
        print(f"Remaining Potential Sales: 0")
    print(f"    1. Continue")
    userChoice = input("Type Any: ")
    return
    
def recommendUpgrade(processes, upgrades, attributes):
    currentProfit = attributes["dailyProfit"]
    bestGain = 0
    bestChoice = None

    for upgrade in upgrades:
        if upgrades[upgrade]["bought"] == False and upgrades[upgrade]["cost"] <= attributes["currentBudget"]:

            testProcesses = copy.deepcopy(processes)
            testUpgrades = copy.deepcopy(upgrades)
            testAttributes = copy.deepcopy(attributes)

            purchaseUpgrade(upgrade, testProcesses, testUpgrades, testAttributes)
            updateNumbers(testProcesses, testAttributes)
            gain = testAttributes["dailyProfit"] - currentProfit
            if gain > bestGain:
                bestGain = gain
                bestChoice = upgrade
    print(f"Recommended Upgrade: {bestChoice} -> ${bestGain:.2f}/day & ${bestGain*365:.2f}/year")



createMenu(defaultProcesses, factoryUpgrades, factoryAttributes, simulationRandomEvents)
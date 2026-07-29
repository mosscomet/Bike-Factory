import sys, subprocess, platform

processes = {
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

workingMinutes = 480.0
sellingPrice = 160.0
customerDemand = 55.0
currentBudget = 30000.0
systemCapacity = 0.0
systemYield = 0.0
bottleneck = ""
profitPerBike = 160.0
dailyProfit = 0.0


def calculateStationCapacity():
    for i in processes:
        pt = processes[i]["processing time"]
        capacity = workingMinutes/pt
        capacity *= (1-processes[i]["downtime"])
        processes[i]["daily"] = capacity

def calculateSystemCapacity():
    global systemCapacity
    calculateStationCapacity()

    tempSysCap = float('inf')
    for i in processes:
        if processes[i]["daily"] < tempSysCap:
            tempSysCap = processes[i]["daily"]
    systemCapacity = tempSysCap

def calculateProcessYield():
    global systemYield
    calculateSystemCapacity()

    productionMultiplier = 1.0
    individualProductionMultipler = 1.0
    for i in processes:
        productionMultiplier *= (1-processes[i]["defect rate"])
        individualProductionMultipler = 1 * (1-processes[i]["defect rate"]) * (1-processes[i]["downtime"])
        processes[i]["yield"] = processes[i]["daily"] * individualProductionMultipler
        individualProductionMultipler = 1.0
    # print(f"syscap {systemCapacity}")
    # print(f"productionMultiplier {productionMultiplier}")
    systemYield = systemCapacity * productionMultiplier
    
def calculateBottleneck():
    global bottleneck
    calculateSystemCapacity()
    listOfProcesses = list(processes.keys())

    for processName in processes:
        if processes[processName]["daily"] <= systemCapacity:
            bottleneck = processName
            break

def calculateDailyProfit():
    global dailyProfit
    calculateProcessYield()

    dailyProfit = systemYield * profitPerBike

def calculateUtilization():
    calculateSystemCapacity()
    
    for i in processes:
        processes[i]["utilization"] = systemCapacity/processes[i]["daily"]


def calculateIdleCapacity():
    calculateSystemCapacity()

    for i in processes:
        processes[i]["idle"] = processes[i]["daily"]-systemCapacity

def clearConsole():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def updateNumbers():
    calculateUtilization()
    calculateIdleCapacity()
    calculateDailyProfit()
    calculateBottleneck()

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


def createMenu():
    updateNumbers()
    while True:
        userChoice = None
        print("=====================================")
        print("Velocity Cycles Manufacturing Simulator")
        print("=====================================")
        print("Current Year: " + str(2026))
        print("Customer Demand: " + str(55) + " bikes/day")
        print("Production Capacity: " + str(55) + " bikes/day")
        print("Current Bottleneck: ______")
        print("Budget Remaining: $30,000")
        print("   1. View Factory")
        print("   2. Modify Factory")
        print("   3. Invest in Improvements")
        print("   4. Run Future Simulation")
        print("   5. View Financial Report")
        print("   6. Exit")


        userChoice = getInt("Select an option: ")
        match userChoice:
            case 1:
                viewFactory()
            case 2:
                modifyFactory()
            case 3:
                investImprove()
            case 4:
                runSimulation()
            case 5: 
                ViewFinancials()
            case 6: 
                sys.exit()
            case _:
                print("unknown input")

def viewFactory():
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
            print(f"   Working Minutes: {workingMinutes}")
            print(f"   Selling Price: {sellingPrice}")
            print(f"   Customer Demand: {customerDemand}")
            print(f"   Current Budget: {currentBudget}")
            print(f"   System Capacity: {systemCapacity}")
            print(f"   System Yield: {systemYield}")
            print(f"   Bottleneck: {bottleneck}")
            print(f"   Profit Per Bike: {profitPerBike}")
            print(f"   Daily Profits: {dailyProfit}")
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
    
def modifyFactory():
    global workingMinutes, sellingPrice, customerDemand, currentBudget, systemCapacity, systemYield, bottleneck, profitPerBike, dailyProfit
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
            print(f"   1. Working Minutes: {workingMinutes}")
            print(f"   2. Selling Price: {sellingPrice}")
            print(f"   3. Customer Demand: {customerDemand}")
            print(f"   4. Current Budget: {currentBudget}")
            print(f"   5. Profit Per Bike: {profitPerBike}")
            print(f"   6. Return")
            while True:
                userChoice = getInt("Choose an option: ")

                match userChoice:
                    case 1:
                        workingMinutes = getFloat("Choose new value: ")
                    case 2:
                        sellingPrice = getFloat("Choose new value: ")
                    case 3:
                        customerDemand = getFloat("Choose new value: ")
                    case 4:
                        currentBudget = getFloat("Choose new value: ")
                    case 5:
                        profitPerBike = getFloat("Choose new value: ")
                    case 6:
                        return
                updateNumbers()   
        else:
            updateNumbers()
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
                updateNumbers()


def investImprove():
    global currentBudget
    while True:
        print("===============")
        print("Upgrade Factory")
        print("===============")
        print(f"Budget Available: ${currentBudget}")
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
                    if factoryUpgrades[selectedUpgrade]["cost"] <= currentBudget and factoryUpgrades[selectedUpgrade]["bought"] == False:
                        currentBudget -= factoryUpgrades[selectedUpgrade]["cost"]
                        factoryUpgrades[selectedUpgrade]["bought"] = True
                        purchaseUpgrade(selectedUpgrade)
                case 2:
                    return
            updateNumbers()

def purchaseUpgrade(selectedUpgrade):
    print(selectedUpgrade)
    if selectedUpgrade == "Faster Wheel Equipment":
        if processes["Wheel Installation"]["processing time"] > 4:
            processes["Wheel Installation"]["processing time"] -= 4
            updateNumbers()
    elif selectedUpgrade == "Additional Brake Workstation":
        processes[selectedUpgrade]["processing time"] /= 2
        updateNumbers()
    elif selectedUpgrade == "Better Inspection equipment":
        if processes["Brake Installation"]["processing time"] > 3:
            processes["Brake Installation"]["processing time"] -= 3
            updateNumbers()
    elif selectedUpgrade == "Worker Training":
        for process in processes:
            processes[process]["defect rate"] *= 0.6
            updateNumbers()
    elif selectedUpgrade == "Conveyor Improvement":
        for process in processes:
            if processes[process]["processing time"] > 0.5:
                processes[process]["processing time"] -= 0.5
        updateNumbers()

def runSimulation():
    print("runSimulation")

def ViewFinancials():
    print("ViewFinancials")

















createMenu()


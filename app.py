import sys, subprocess, platform

processes = {
    # Name: {processing time: minutes (int), downtime: minutes (int), defect rate: as a decimal, daily: capacity}
    "Frame Assembly":       {"processing time":8.0, "downtime":0.0, "defect rate":0.01, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Wheel Installation":   {"processing time":12.0, "downtime":0.05, "defect rate":0.03, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Brake Installation":   {"processing time":7.0, "downtime":0.0, "defect rate":0.02, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Quality Inspection":   {"processing time":9.0, "downtime":0.0, "defect rate":0.01, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
    "Packaging":            {"processing time":5.0, "downtime":0.0, "defect rate":0.005, "daily":0.0, "yield":0.0, "utilization": 0.0, "idle":0.0},
}

workingMinutes = 480
sellingPrice = 160
customerDemand = 55
currentBudget = 30000
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
    print("syscap " + str(systemCapacity))
    print("productionMultiplier" + str(productionMultiplier))
    systemYield = systemCapacity * productionMultiplier
    
def calculateBottleneck():
    global bottleneck
    calculateSystemCapacity()

    for i in processes:
        if processes[i]["daily"] <= systemCapacity:
            bottleneck = processes[i]
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

def createMenu():
    print("=====================================")
    print("Velocity Cycles Manufacturing Simulator")
    print("=====================================")
    print("Current Year: " + str(2026))
    print("Customer Demand: " + str(55) + "bikes/day")
    print("Production Capacity: " + str(55) + "bikes/day")
    print("Current Bottleneck: ______")
    print("Budget Remaining: $30,000")
    print("   1. View Factory")
    print("   2. Modify Factory")
    print("   3. Invest in Improvements")
    print("   4. Run Future Simulation")
    print("   5. View Financial Report")
    print("   6. Exit")

def viewFactory():
    pass

def modifyFactory():
    pass

def investImprove():
    pass

def runSimulation():
    pass

def ViewFinancials():
    pass

def exit():
    pass





print(processes)
print()
calculateStationCapacity()
print()
calculateSystemCapacity()
print()
calculateProcessYield()
print()
calculateUtilization()
print()
calculateIdleCapacity()
print()
print(processes)
print()
calculateDailyProfit()
print("daily profit" + str(dailyProfit) + " daily sales" + str(systemYield) + " systemYield " + str(systemYield))
createMenu()






import sys

processes = {
    # Name: {processing time: minutes (int), downtime: minutes (int), defect rate: as a decimal, daily: capacity}
    "Frame Assembly":       {"processing time":8.0, "downtime":0.0, "defect rate":0.01, "daily":0.0, "yield":0.0},
    "Wheel Installation":   {"processing time":12.0, "downtime":0.0, "defect rate":0.03, "daily":0.0, "yield":0.0},
    "Brake Installation":   {"processing time":7.0, "downtime":0.0, "defect rate":0.02, "daily":0.0, "yield":0.0},
    "Quality Inspection":   {"processing time":9.0, "downtime":0.0, "defect rate":0.01, "daily":0.0, "yield":0.0},
    "Packaging":            {"processing time":5.0, "downtime":0.0, "defect rate":0.005, "daily":0.0, "yield":0.0},
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

def initializeVariables():
    pass

def calculateStationCapacity():
    for i in processes:
        pt = processes[i]["processing time"]
        capacity = workingMinutes/pt
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
    for i in processes:
        productionMultiplier *= 1-processes[i]["defect rate"]
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
    pass

def calculateIdleCapacity():
    pass





print(processes)
print()
calculateStationCapacity()
print()
calculateSystemCapacity()
print()
calculateProcessYield()







import argparse, json, os
from datetime import datetime

try:
    with open("tasks.json", 'r') as file:
        currentData = json.load(file)
except FileNotFoundError:
    with open("tasks.json", 'w') as file:
        currentData = {}

parser = argparse.ArgumentParser(description = "Task commands")
parser.add_argument('--add', type=str, help='Add a task')
parser.add_argument('--updateName', nargs=2, metavar=('ID', 'NEW'), help="Update task: 'old task ID', 'new task name'")
parser.add_argument('--notStarted', action='store_true', help='View tasks that have not been started')
parser.add_argument('--inProgress', action='store_true', help='View tasks that are in progress')
parser.add_argument('--completed', action='store_true', help='View completed tasks')
parser.add_argument('--viewAll', action='store_true', help='View all tasks')
parser.add_argument('--delete', type=str, help='Delete specific task')
parser.add_argument('--updateStatus', nargs=2, metavar=("ID", 'NEW'), help="Update the status of the current task. Must be changed to either notStarted, inProgress or completed")
args = parser.parse_args()

class Task:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.status = "notStarted"
        self.createdAt = datetime.now()
        self.updatedAt = None

def genID():
    try:
        with open("id.txt", 'r') as file:
            currentID = int(file.read())
            newID = currentID + 1
            with open("id.txt", 'w') as file:
                file.write(str(newID))
    except FileNotFoundError:
        with open("id.txt", 'w') as file:
            currentID = newID = 0
            file.write(str(currentID))
    return newID

def add(newTask):
    global currentData
    taskDict = {"name" : newTask.name, "status" : newTask.status, "createdAt" : str(newTask.createdAt), "updatedAt" : newTask.updatedAt, "id" : newTask.id}
    key = taskDict["id"]
    currentData[key] = taskDict
    print(f"{newTask.name} added")
    save(taskDict)

def delete(taskID):
    global currentData
    del currentData[taskID]
    with open("tasks.json", 'w') as file:
        json.dump(currentData, file)

def view():
    global currentData
    for key, dict in currentData.items():
        print()
        print(f"Task {key}:")
        for innerKey, value in dict.items():
            print(f"{innerKey} - {value}")

def viewCat(category):
    global currentData
    for key, dict in currentData.items():
        if category == "notStarted":
            if dict["status"] == "notStarted":
                print(dict)
                print()
        elif category == "inProgress":
            if dict["status"] == "inProgress":
                print(dict)
                print()
        elif category == "completed":
            if dict["status"] == "completed":
                print(dict)
                print()

def updateName(oldID, newName, curTime):
    global currentData
    for task in currentData.values():
        if task["id"] == oldID:
            task["name"] = newName
            task["updatedAt"] = str(curTime)
    with open("tasks.json", 'w') as file:
        json.dump(currentData, file)

def updateStatus(oldID, newStatus, curTime):
    global currentData
    for task in currentData.values():
        if task["id"] == oldID:
            task["status"] = newStatus
            task["updatedAt"] = str(curTime)
    with open("tasks.json", 'w') as file:
        json.dump(currentData, file)

def save(newData):
    if os.path.getsize("tasks.json") > 0:
        with open("tasks.json", 'r') as file:
            fileData = json.load(file)
            fileData[newData["id"]] = newData
            with open ("tasks.json", 'w') as file:
                json.dump(fileData, file)
    else:
        fileData = {}
        fileData[newData["id"]] = newData
        with open ("tasks.json", 'w') as file:
            json.dump(fileData, file)

if args.add:
    name = args.add
    id = genID()
    newTask = Task(id, name)
    add(newTask)
elif args.delete:
    task = args.delete
    delete(task)
elif args.viewAll:
    view()
elif args.notStarted:
    viewCat("notStarted")
elif args.inProgress:
    viewCat("inProgress")
elif args.completed:
    viewCat("completed")
elif args.updateName:
    oldID = int(args.updateName[0])
    newName = args.updateName[1]
    curTime = datetime.now()
    updateName(oldID, newName, curTime)
elif args.updateStatus:
    oldID = int(args.updateStatus[0])
    newStatus = args.updateStatus[1]
    allowed = ["notStarted", "inProgress", "completed"]
    if newStatus not in allowed:
        print("status must be changed to either 'notStarted', 'inProgress' or 'completed'")
    else:
        curTime = datetime.now()
        updateStatus(oldID, newStatus, curTime)




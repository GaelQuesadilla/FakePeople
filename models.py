import uuid
import random
import errors
import json
import csv
from colorama import init, Fore

init(autoreset=True)


class Persons:
    def __init__(self):
        self.items = []

    def create(self, number):
        for x in range(number):
            self.items.append({})
        print(Fore.GREEN + f"{number} items has ben added")

    def addGenre(self):
        mods = 0
        for item in self.items:
            if item.get("gender") is None:
                item["gender"] = random.choice(["male", "female"])
                mods += 1
        print(Fore.GREEN + f"Genre has ben added to {mods} items")

    def addNames(self, attempts=5, unique=True):
        mods = 0
        for item in self.items:
            if item.get("name") is not None:
                continue
            for attempt in range(attempts):
                try:
                    availableLastNames = json.load(
                        open("./names/lastNames.json", "r", encoding="UTF-8"))

                    if item.get("gender") is None:
                        raise errors.ItemNeedHaveGenreProperty

                    if item.get("gender") == "male":
                        availableNames = json.load(
                            open("./names/maleNames.json", "r", encoding="UTF-8"))
                    elif item.get("gender") == "female":
                        availableNames = json.load(
                            open("./names/femaleNames.json", "r", encoding="UTF-8"))

                    name = random.choice(availableNames)
                    hasSecondName = random.choice([True, False])
                    if hasSecondName:
                        secondName = random.choice(availableNames)
                        name += f" {secondName}"

                    fLastName = random.choice(availableLastNames)
                    mLastName = random.choice(availableLastNames)
                    newName = {
                        "name": name,
                        "fLastName": fLastName,
                        "mLastName": mLastName
                    }
                    if self.genFullNameString(newName) in [self.genFullNameString(item) for item in self.items]:
                        raise errors.ItemPropertyAlreadyExist
                        continue

                    item.update(newName)
                    mods += 1
                    break
                except errors.ItemPropertyAlreadyExist:
                    print(Fore.YELLOW + f"NAME ALREADY EXIST, ATTEMPT {
                        attempt+1} OF {attempts}")
                    if attempt+1 == attempts:
                        print("ERROR, CAN NOT GENERATE A UNIQUE NAME")
                        break
                except errors.ItemNeedHaveGenreProperty:
                    break
        print(Fore.GREEN + f"Name has ben added to {mods} items")

    def genFullNameString(self, item):
        return f"{item.get("fLastName")} {item.get("mLastName")} {item.get("name")}"

    def saveAsCsv(self, docName="data.csv"):
        with open(docName, "w", encoding="UTF-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.items[0].keys())
            writer.writeheader()
            writer.writerows(self.items)


class Students(Persons):
    def addGrade(self, number, grade, **kwargs):
        mods = 0
        for index in range(len(self.items)):
            item = self.items[index]
            if item.get("grade") is None:
                item["grade"] = grade
                for key in kwargs:
                    item[key] = kwargs.get(key)
                mods += 1
            if mods == number:
                break

        if mods == number:
            print(
                Fore.GREEN + f"grade has ben added to {mods} of {number} items")
        else:
            print(
                Fore.YELLOW + f"grade has ben added to {mods} of {number} items")

    def addScore(self, mu, sigma, minimalScore=5, maxScore=10, floatNumbers=2):
        mods = 0
        for item in self.items:
            if item.get("score") is None:
                idealScore = round(random.gauss(mu, sigma), floatNumbers)

                score = idealScore
                if idealScore > maxScore:
                    score = maxScore
                elif idealScore < minimalScore:
                    score = minimalScore

                item["score"] = score
                mods += 1
        print(Fore.GREEN + f"score has ben added to {mods} items")


students = Students()
students.create(540)
students.addGenre()
students.addNames()
students.addGrade(45, "2", group="A")
students.addGrade(45, "2", group="B")
students.addGrade(45, "2", group="C")
students.addGrade(45, "2", group="D")
students.addGrade(45, "4", group="A")
students.addGrade(45, "4", group="B")
students.addGrade(45, "4", group="C")
students.addGrade(45, "4", group="D")
students.addGrade(45, "6", group="A")
students.addGrade(45, "6", group="B")
students.addGrade(45, "6", group="C")
students.addGrade(45, "6", group="D")
students.addScore(8.5, 1)

students.saveAsCsv()

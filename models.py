import random
import errors
import json
import csv
from colorama import init, Fore
import datetime

init(autoreset=True)
dateFormat = "%d/%m/%Y"

characters = "ABCDEFGHIJKLNMNOPQRSTUVWXYZ1234567890"


def dateBetweenYears(date, minYears, maxYears):
    minDays = minYears * 365.25
    maxDays = maxYears * 365.25
    daysSinceDate = random.randrange(round(minDays), round(maxDays))
    newDate = date + datetime.timedelta(days=daysSinceDate)
    return newDate


def shuffleList(inputList: list or tuple):
    newList = inputList
    random.shuffle(newList)
    return newList


def genKey(chars, n):
    key = ""
    for _ in range(0, n):
        key += random.choices(chars)[0]
    return key


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

    def addBirthDate(self, minAge=18, maxAge=60):
        today = datetime.date.today()
        mods = 0
        for item in self.items:
            if item.get("birthday") is not None:
                continue
            birthday = dateBetweenYears(today, -50, -18)
            item["birthday"] = birthday.strftime(dateFormat)
            mods += 1
        print(Fore.GREEN + f"Birthday has ben added to {mods} items")

    def addBirthState(self):
        mods = 0
        for item in self.items:
            if item.get("birthState") is not None:
                continue
            availableStates = json.load(
                open("./names/states.json", "r", encoding="UTF-8"))
            mods += 0
            item["birthState"] = random.choice(availableStates)[0]
        print(Fore.GREEN + f"Birthday state has ben added to {mods} items")

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


class Mexican(Persons):
    def addRFC(self):
        mods = 0
        for item in self.items:
            if item.get("RFC") is not None:
                continue
            RFC = "{mlname}{flname}{name}{bdate}{key}".format(
                mlname=item.get("mLastName")[0:2],
                flname=item.get("fLastName")[0:1],
                name=item.get("name")[0:1],
                bdate=datetime.datetime.strptime(
                    item.get("birthday"), dateFormat).strftime("%y%m%d"),
                key=genKey(characters, 3)
            )
            item["RFC"] = RFC.upper()
            mods += 1
        print(Fore.GREEN + f"RFC has ben added to {mods} items")

    def addCURP(self):
        mods = 0
        for item in self.items:
            if item.get("CURP") is not None:
                continue
            CURP = "{mlname}{flname}{name}{bdate}{gender}{bstate}{consa}{consb}{consc}".format(
                mlname=item.get("mLastName")[0] +
                "".join(char for char in item.get(
                    "mLastName") if char in "aeiou")[0],
                flname=item.get("fLastName")[0:1].upper(),
                name=item.get("name")[0:1].upper(),
                bdate=datetime.datetime.strptime(
                    item.get("birthday"), dateFormat).strftime("%y%m%d"),
                gender=item.get("gender")[0].upper().replace(
                    "M", "H").replace("F", "M"),
                bstate="".join(
                    x[1] for x in json.load(open("./names/states.json", "r", encoding="UTF-8")) if x[0] == item.get("birthState")),
                consa="".join(
                    char for char in item.get("mLastName")if char in "bcdfghjklmnñpqrstvwxyz")[0],
                consb="".join(
                    char for char in item.get("fLastName")if char in "bcdfghjklmnñpqrstvwxyz")[0],
                consc="".join(
                    char for char in item.get("name")if char in "bcdfghjklmnñpqrstvwxyz")[0],
                key=genKey(characters, 1)
            )
            if datetime.datetime.strptime(item.get("birthday"), dateFormat).year <= 1999:
                CURP += str(random.randrange(0, 9))
            else:
                CURP += genKey(characters, 1)

            def getValue(char):
                values = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
                return values.find(str(char))

            tmpCURP = CURP + "0"
            total = 0
            for i in range(0, len(tmpCURP)):
                char = tmpCURP[::-1][i]
                total += getValue(char)*(i+1)

            CURP += str(total % 10)

            item["CURP"] = CURP.upper()

            mods += 1
        print(Fore.GREEN + f"CURP has ben added to {mods} items")

    def addNSS(self):
        mods = 0
        for item in self.items:
            if item.get("NSS") is not None:
                continue
            NSS = "{clinic}{registerDate}{bYear}{consecutive}{verificationNumber}".format(
                clinic=random.randrange(10, 99),
                registerDate=str(int(datetime.datetime.strptime(
                    item.get("birthday"), dateFormat).strftime("%y")) + 18 + round(random.random()*5))[-2:],
                bYear=datetime.datetime.strptime(
                    item.get("birthday"), dateFormat).strftime("%y"),
                consecutive=random.randrange(1000, 9999),
                verificationNumber=random.randrange(0, 9)

            )
            item["NSS"] = NSS


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

    def addScore(self, mu, sigma, minimalScore=5, maxScore=10, floatNumbers=1):
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

    def addSelections(self, options: list or tuple):
        mods = 0
        for item in self.items:
            numbers = list(range(1, len(options)+1))
            selections = shuffleList(numbers)
            for option in options:
                item[option] = selections.pop()
                mods += 1
        print(Fore.GREEN + f"selections has ben added to {mods} items")


if __name__ == "__main__":
    persons = Mexican()
    persons.create(150)
    persons.addGenre()
    persons.addNames()
    persons.addBirthDate()
    persons.addRFC()
    persons.addBirthState()
    persons.addCURP()
    persons.addNSS()
    persons.saveAsCsv()

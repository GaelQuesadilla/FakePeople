import uuid
import random
import errors
import json
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

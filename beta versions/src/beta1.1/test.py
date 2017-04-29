import random
random.seed()

ls = [line.rstrip('\n') for line in open('assets/names.txt')]
ls.remove("")

days = [x+1 for x in range(29)]
months = [x+1 for x in range(12)]
years = [x for x in range(75,94)]
jobs = ["engineer", "task manager", "supervisor", "snack person", "engineer", "engineer", "janitor", "cheer-leader", "tech support"]

random.shuffle(ls)

for n in ls:
    print()
    print("Name:",n)
    print("DOB:",random.choice(days),"/",random.choice(months),"/",random.choice(years))
    print("Title:",random.choice(jobs))
    print()
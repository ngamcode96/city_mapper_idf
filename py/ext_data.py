data = open("network_bus.csv", "r")

for line in data:
    items = line.rstrip("\n").split(";")
    for item in items:
        print(str(item))
        x = input("Entrer ")
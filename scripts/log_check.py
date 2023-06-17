import csv

file_name = "log.csv"
dict= {"Herbivore": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
       "Carnivore": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

with open(file_name, "w") as file:
    writer = csv.writer(file)

    headers = list(dict.keys())

    years = len(dict[headers[0]])

    writer.writerow(dict.keys())

    for year in range(years):
        writer.writerow([dict[header][year] for header in headers])

print("done")


"""
with open(file_name, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
"""
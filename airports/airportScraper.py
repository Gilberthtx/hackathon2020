import csv

# returns list of strings with each string in format "DFW Dallas Fort Worth International Airport Dallas-Fort Worth TX"
csv_file = open("airports/us-airports.csv")
read_csv = csv.reader(csv_file, delimiter=',')
airport_list = []
for row in read_csv:
    airport_info = ""
    airport_info += row[0] + " - " + row[1] + " - " + row[2] + " - " + row[3]
    airport_list.append(airport_info)

j = 0
for x in range(0, len(airport_list)):
    if airport_list[x - j] == ',':
        airport_list.remove(airport_list[x - j])
        j += 1
    elif airport_list[x - j][0].isupper() is not True or airport_list[x - j][1].isupper() is not True or airport_list[x - j][2].isupper() is not True:
        airport_list.remove(airport_list[x - j])
        j += 1

symbol_list = []
for m in airport_list:
    symbol_list.append(m[0:3])

num_of_airports = len(symbol_list)

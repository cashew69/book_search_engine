import csv

file = open("titles.csv", "r")
data = list(csv.reader(file, delimiter=","))

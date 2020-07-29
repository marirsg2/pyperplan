import csv

with open("state-deepplan.csv", newline='') as csvfile:
    feature_reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    print(feature_reader.__next__())
    # for row in feature_reader:
    #     print(row)
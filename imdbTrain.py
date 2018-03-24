import csv

with open('datasets/imdb/unlabeledTrainData.tsv','rb') as tsvin, open('new.csv', 'wb') as csvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    csvout = csv.writer(csvout)

    for row in tsvin:
        count = int(row[4])
        if count > 0:
            csvout.writerows([row[2:4] for _ in range(count)])

unlabeled= open("datasets/imdb/unlabeledTrainData.tsv","r")

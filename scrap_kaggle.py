
import csv
from bs4 import BeautifulSoup

with open("InData/Global Cost of Living _ Kaggle.html") as file:
    content = file.read()
# scrap Kaggle to get columns names:
soup=BeautifulSoup(content,"html.parser")

columns=soup.tbody

list=[]


for column in columns.strings:
    if len(column)>1:

        list.append(column.strip())
list=list[1::2]

# function that return lazy iterator of csv file
def csv_extract(f_name, header = False):
    with open(f_name) as file:
        reader = csv.reader(file)
        if not header:
            next(reader)
        for line in reader:
            yield(line)

# write into csv file after data cleaning
def csv_write_file(reader, f_name,columns, mode="a"):
    csvfile_read=reader

    with open(f_name,mode) as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for line in csvfile_read:
            if all(line):
                writer.writerow(line)

#apply functions to get new csv file
csv_write_file(reader=csv_extract("InData/cost-of-living.csv"),
                                    f_name="OutData/numbeo1.csv",
                                    columns=list)




# reads the dict from csv file
import csv

total_results = {}
csvfile = open('ningboYb.txt', 'r',encoding='utf-8')
reader = csv.reader(csvfile)
# csvfile.close()
f = open('ningboYb_supermapol_addr.csv', 'w', encoding='utf-8')
f1 = open('ningboYb_supermapol_name.csv', 'w', encoding='utf-8')
f2 = open('ningboYb_supermapol_3.csv', 'w', encoding='utf-8')

for row in reader:
    f.write("宁波," + row[1] + "\n")
    f1.write("宁波," + row[0] + "\n")
    f2.write("宁波," + row[0] + "," + row[1] + "\n")
f.close()
f1.close()
f2.close()
csvfile.close()
print("done")

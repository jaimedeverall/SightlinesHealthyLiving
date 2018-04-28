import csv

with open('Fulton_results.csv', 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)

	with open('Fulton.csv', 'rt') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for i, row in enumerate(reader):
			if i==0:
				continue
			code = row[0].strip('"')
			with open('Georgia_Coordinates.csv') as csvfile1:
				reader1 = csv.reader(csvfile1, delimiter=',', quotechar='|')
				for j, row1 in enumerate(reader1):
					if j==0:
						continue
					if row1[1].strip('"') == code:
						area = int(row1[2]) + int(row1[3])
						lat = row1[6]
						lng = row1[7]
						new_row = [code, area, lat, lng]
						filewriter.writerow(new_row)


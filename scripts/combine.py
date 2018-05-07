import csv

with open('Massachusetts_state_results.csv', 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)

	with open('Massachusetts_census_tracts.csv') as csvfile1:
		reader1 = csv.reader(csvfile1, delimiter=',', quotechar='|')
		for j, row1 in enumerate(reader1):
			area = int(row1[2])
			lat = row1[6]
			lng = row1[7]
			new_row = [code, area, lat, lng]
			filewriter.writerow(new_row)

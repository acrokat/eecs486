import csv
with open('sentiment.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	r=0
	for row in reader:
		r+=1
		if str(row['Sentiment']) == "1":
			print row['SentimentText'].lstrip(), row['Sentiment']
		
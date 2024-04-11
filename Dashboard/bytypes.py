import csv

# Open the CSV file
with open('netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Read the CSV data into a list of dictionaries
    data = [row for row in reader]

# Sort the data by the 'type' key
sorted_data = sorted(data, key=lambda x: x['title'])

# Print column headers
print("ID\tType\tTitle\tDirector\tCast\tCountry\tDate Added\tRelease Year\tRating\tDuration\tListed In\tDescription")

# Print the sorted data
for row in sorted_data:
    print(
        f"{row['title']}\t")

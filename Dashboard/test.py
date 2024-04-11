import csv

# Open the CSV file
with open('netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Print column headers
    print(
        "ID\tType\tTitle\tDirector\tCast\tCountry\tDate Added\tRelease Year\tRating\tDuration\tListed In\tDescription")

    # Iterate over each row in the CSV file
    for row in reader:
        # Print each line of data
        print(
            f"{row['show_id']}\t{row['type']}\t{row['title']}\t{row['director']}\t{row['cast']}\t{row['country']}\t{row['date_added']}\t{row['release_year']}\t{row['rating']}\t{row['duration']}\t{row['listed_in']}\t{row['description']}")
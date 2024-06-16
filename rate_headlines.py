import os
import csv

# Define the CSV file path and header
csv_file_path = 'ragebait_scores.csv'
header = ['Headline', 'Ragebait Score']

def get_ragebait_score(headline):
    print(f"Rate the headline '{headline}' on a scale of 1-10:")
    while True:
        try:
            return int(input("Enter your rating: "))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Initialize the CSV file with the header
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

    # Iterate through filenames in ./__stories__
    for filename in os.listdir('./__stories__/'):
        ragebait_score = get_ragebait_score(filename)
        with open(csv_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([filename, ragebait_score])

if __name__ == '__main__':
    main()

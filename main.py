import pandas as pd


def extract_data(file_path, start_row, end_row):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Extract the second column data from the specified rows
    # Adjusting the row indices as pandas DataFrame is 0-indexed
    data = df.iloc[start_row - 1:end_row, 1]

    # Print each item in quotes and separated by space
    output = ' '.join(f'"{item}"' for item in data)
    print(output)


# Replace with the path to your Excel file
file_path = '2022广西科学技术奖.xlsx'

# Input for start and end row numbers
a = int(input("Enter start row number: "))
b = int(input("Enter end row number: "))

extract_data(file_path, a, b)
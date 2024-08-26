from datetime import datetime, timedelta

# Get the current date
today = datetime.now()

# Set the end date to December 2025
end_date = datetime(2026, 12, 31)


def get_csv(fd: datetime, ld: datetime, file_name: str):
    import requests

    url = "https://downloads.salahtimes.com/api/prayerDownload"
    headers = {
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
    }

    params = {
        "format": "csv",
        "country": "uk",
        "place": "bristol",
        "hlm": "4",
        "pcm": "5",
        "acm": "1",
        "ds": fd.strftime("%Y-%m-%d"),
        "de": ld.strftime("%Y-%m-%d"),
        "as24": "true",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
            print(f"{file_name} downloaded successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


# Loop through each month until the end of 2025
current_date = today

while current_date <= end_date:
    # Calculate the first day of the current month
    fd = datetime(current_date.year, current_date.month, 1)

    # Calculate the last day of the current month
    if current_date.month == 12:
        ld = datetime(current_date.year + 1, 1, 1) - timedelta(days=1)
    else:
        ld = datetime(current_date.year, current_date.month + 1, 1) - timedelta(days=1)

    # Generate a file name for the current month
    file_name = f"{current_date.strftime('%m_%y')}.csv"

    # Download the CSV file for the current month
    get_csv(fd, ld, file_name)

    # Move to the next month
    if current_date.month == 12:
        current_date = datetime(current_date.year + 1, 1, 1)
    else:
        current_date = datetime(current_date.year, current_date.month + 1, 1)

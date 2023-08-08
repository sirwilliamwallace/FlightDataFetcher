# FlightDataFetcher

FlightDataFetcher is a Python command-line tool that simplifies the process of fetching, storing, and managing real-time flight data using the FlightAware API and SQLite database.

## Features

- **Real-time Updates:** Retrieve the latest flight data from the FlightAware API to keep your database current.
- **Efficient Storage:** Store retrieved flight details in a structured SQLite database for easy querying and management.
- **Search Capabilities:** Search for flights using parameters such as airline, flight ID, departure/arrival airport, and more.
- **User-friendly Interface:** Interact with the tool through a command-line interface with clear commands and informative responses.
- **Data Presentation:** Display flight details in an organized tabular format for easy interpretation.
- **Customizable Searches:** Customize your searches by specifying the data type you want to search for.
- **Automated Updates:** Schedule automated updates to synchronize your flight data database seamlessly.

## Usage

1. Install the required packages:

```bash
pip install requests tabulate
git clone https://github.com/sirwilliamwallace/FlightDataFetcher.git
cd FlightDataFetcher
```
1. Create a FlightAware account and obtain an API key.

2. Change the API key in `main.py` to your own.

3. Run the program:

```bash
python main.py
```

## Usage
    - To update the database with new flights:
        - ```bash
           python main.py update
          ```
    - To search for flights:
        - ```bash
           python main.py search [keyword] [type]
          ```
    - To list all flights:
        - ```bash
           python main.py list
          ```


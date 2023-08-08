import requests
import sqlite3
import sys
from tabulate import tabulate

# Flightaware.com API Key
API_KEY = 'API_KEY_HERE'

def fetch_flight_data():
    params = {'access_key': API_KEY, "limit": 100}
    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
    api_response = api_result.json()
    return api_response.get('data')

def update_database():
    if sys.platform == 'win32':
        temp = 'C:\\temp\\flights.db'
    else:
        temp = '/tmp/flights.db'

    flights = fetch_flight_data()
    with sqlite3.connect(temp) as conn:
        
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS flights (flight_id TEXT, flight_status TEXT, airline TEXT, departure_airport TEXT, arrival_airport TEXT, departure_date TEXT, arrival_date TEXT)')
        c.execute('CREATE INDEX IF NOT EXISTS airline_index ON flights (airline)')
        c.execute('CREATE INDEX IF NOT EXISTS flight_status_index ON flights (flight_id)')
        c.execute('CREATE INDEX IF NOT EXISTS departure_airport_index ON flights (departure_airport)')
        c.execute('CREATE INDEX IF NOT EXISTS arrival_airport_index ON flights (arrival_airport)')
        c.execute('CREATE INDEX IF NOT EXISTS departure_date_index ON flights (departure_date)')
        c.execute('CREATE INDEX IF NOT EXISTS arrival_date_index ON flights (arrival_date)')
        
        flight_data = []
        for flight in flights:
            flight_id = flight.get('flight').get('iata')
            flight_status = flight.get('flight_status')
            airline = flight.get('airline').get('name', "N/A")
            departure_airport = flight.get('departure').get('airport', "N/A")
            arrival_airport = flight.get('arrival').get('airport', "N/A")
            departure_date = flight.get('departure').get('scheduled', "N/A")
            arrival_date = flight.get('arrival').get('scheduled', "N/A")
            flight_data.append((
                flight_id,
                flight_status,
                airline,
                departure_airport,
                arrival_airport,
                departure_date,
                arrival_date
            ))
        
        c.executemany('INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?)', flight_data)
        conn.commit()
        changes = conn.total_changes
        print(f"Updated database with {changes} flights" if changes > 0 else "No new flights to update")

def search_flights(keyword, search_type='airline'):
    query_map = {
        'airline': 'airline',
        'flight_id': 'flight_id',
        'departure_airport': 'departure_airport',
        'arrival_airport': 'arrival_airport',
        'departure_date': 'departure_date',
        'arrival_date': 'arrival_date'
    }
    query_column = query_map.get(search_type, 'airline')
    query = f"SELECT * FROM flights WHERE {query_column} LIKE ?"
    
    with sqlite3.connect('/tmp/flights.db') as conn:
        c = conn.cursor()
        c.execute(query, ('%' + keyword + '%',))
        return c.fetchall()

def list_flights():
    with sqlite3.connect('/tmp/flights.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flights")
        return c.fetchall()


def cli():
    if len(sys.argv) == 1:
        print("Usage: python main.py [update|search]")
        return
    
    command = sys.argv[1]
    if command == 'update':
        update_database()
    elif command == 'list':
        results = list_flights()
        headers = ["Flight ID", "Flight Status", "Airline", "Departure Airport", "Arrival Airport", "Departure Date"]
        data = []
        
        for row in results:
            formatted_row = []
            for value in row[:6]:
                formatted_value = value if value is not None else "N/A"
                formatted_row.append(formatted_value)
            data.append(formatted_row)
        
        table = tabulate(data, headers, tablefmt="grid")
        print(table)
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: python main.py search [keyword] [type]")
            return
        keyword = sys.argv[2]
        search_type = sys.argv[3] if len(sys.argv) == 4 else 'airline'
        results = search_flights(keyword, search_type)
        
        headers = ["Flight ID", "Flight Status", "Airline", "Departure Airport", "Arrival Airport", "Departure Date"]
        data = []
        
        for row in results:
            formatted_row = []
            for value in row[:6]:
                formatted_value = value if value is not None else "N/A"
                formatted_row.append(formatted_value)
            data.append(formatted_row)
        
        table = tabulate(data, headers, tablefmt="grid")
        print(table)
    else:
        print("Usage: python main.py [update|search]")
        return
    
if __name__ == '__main__':
    cli()
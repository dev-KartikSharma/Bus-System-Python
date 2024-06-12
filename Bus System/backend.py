import random
import threading
import time
import string

# Stations list (A to Z)
stations = list(string.ascii_uppercase)
passengers = {}
currentStationIndex = 0

class BusStation:
    def __init__(self):
        self.stations = stations
        self.current_station_index = 0
        self.station_change_callback = None
        
    def changing_station(self):
        global currentStationIndex
        while True:
            current_station = self.stations[currentStationIndex]
            self.current_station_index = currentStationIndex
            print('-' * 15)
            print(f'Current Station is: {current_station}')
            if self.station_change_callback:
                self.station_change_callback(current_station)
            next_station_index = (currentStationIndex + 1) % len(self.stations)
            currentStationIndex = next_station_index
            time.sleep(5)
    # this function was for console app but this is useless in gui app    
    # def destination_station(self):
    #     departure_index = currentStationIndex
    #     destination_index = random.randint(departure_index + 1, len(self.stations) - 1)
    #     print(f'The destination station is: {self.stations[destination_index]}')
    #     return self.stations[destination_index]

    def register_station_change_callback(self, callback):
        self.station_change_callback = callback
    
class TicketFair:
    def __init__(self, stations):
        self.stations = stations
        self.fare_per_station = 10

    def calculate_fare(self, departure, destination):
        try:
            departure_index = self.stations.index(departure)
            destination_index = self.stations.index(destination)
        except ValueError:
            raise ValueError('Invalid station name')

        if departure_index == destination_index:
            return 0
        
        num_stations = abs(destination_index - departure_index)
        fare = num_stations * self.fare_per_station
        return fare

class PassengersData:
    def __init__(self, stations):
        self.passengers = passengers
        self.stations = stations

    def generate_random_string(self, length=8):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choices(characters, k=length))
        return random_string

    def add_data(self, departure_station, destination_station, fare):
        p_id = self.generate_random_string()
        self.passengers[p_id] = {
            'Departure Station': departure_station,
            'Destination Station': destination_station,
            'Ticket Fare': fare
        }
        print(f"Passenger ID: {p_id}")
        print(self.passengers)

    def step_down(self, current_station):   
        for p_id, data in list(self.passengers.items()):
            if data['Destination Station'] == current_station:
                print(f"Passenger {p_id}, your destination {data['Destination Station']} has arrived. Please step down the bus.")
                del self.passengers[p_id]

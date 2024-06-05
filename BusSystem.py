import threading
import random
import time
import string

# Stations list (A to Z)
stations = list(string.ascii_uppercase)
passengers = {}
currentStationIndex = 0

class BusStation:
    def __init__(self):
        self.stations = stations

    def changing_station(self):
        global currentStationIndex
        while True:
            current_station = self.stations[currentStationIndex]
            print('-' * 15)
            print(f'Current Station is: {current_station}')
            next_station_index = (currentStationIndex + 1) % len(self.stations)
            currentStationIndex = next_station_index
            time.sleep(10)  # Set this to 10 seconds for real use

    def destination_station(self):
        departure_index = currentStationIndex
        destination_index = random.randint(departure_index + 1, len(self.stations) - 1)
        print(f'The destination station is: {self.stations[destination_index]}')
        return self.stations[destination_index]
    
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
        # print(self.passengers)

    def step_down(self, current_station):   
        for p_id, data in list(self.passengers.items()):
            if data['Destination Station'] == current_station:
                print(f"Passenger {p_id}, your destination {data['Destination Station']} has arrived. Please step down the bus.")
                del self.passengers[p_id]


def main():
    bus_station = BusStation()
    ticket_fair = TicketFair(stations)
    passengers_data = PassengersData(stations)

    print('Welcome To Bus System')

    def book_ticket():
        while True:
            time.sleep(random.randint(1, 3))  
            departure_station = stations[currentStationIndex]
            destination_station = bus_station.destination_station()
            fare = ticket_fair.calculate_fare(departure_station, destination_station)
            passengers_data.add_data(departure_station, destination_station, fare)

    def check_step_down():
        while True:
            time.sleep(1)
            station_index = currentStationIndex-1
            temp = stations[station_index]
            # print(temp)  
            passengers_data.step_down(temp)

    t1 = threading.Thread(target=bus_station.changing_station)
    t2 = threading.Thread(target=book_ticket)
    t3 = threading.Thread(target=check_step_down)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

if __name__ == "__main__":
    main()

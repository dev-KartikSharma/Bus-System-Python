import threading
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BusRoute:
    def __init__(self, route_name, stops):
        self.route_name = route_name
        self.stops = stops
        self.current_stop_index = 0
        self.fair =  0.0
        

    def route_mapper(self,start_destination,end_destination):
        print()


class Ticket:
    def __init__(self) -> None:
        pass


class BusSystem:
    def __init__(self) -> None:
        pass

def main():
    while True:
        print('Welcome to Bus System!')
        print('1. Take Bus Route')
        print('2. Exit')
        choice = input('Enter your choice : ')
        if choice == '1':
            start_destination = input('Enter your start station : ')
            print('Destination : ')
            print('1. A')
            print('2. B')
            print('3. C')
            print('4. D')
            print('5. E')
            end_destination = input('Enter your destination : ')
            if end_destination == '1':
                print(f'Ticket Fair : {fair}')
            elif end_destination == '2':
                print()
            elif end_destination == '3':
                print()
            elif end_destination == '4':
                print()
            elif end_destination == '5':
                print()
        elif choice == '2':
            print('Thank you for using the Bus!')
            break
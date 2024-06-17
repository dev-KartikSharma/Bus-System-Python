# Final Build 
# Author --> Kartik Sharma

import threading
from backend import BusStation, TicketFare, PassengersData, stations, passengers
import customtkinter as ctk
from tkinter import messagebox
from CTkTable import CTkTable 
import string

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.userList = []

        self.title('Bus Management System')
        self.geometry('900x700')
        self.iconbitmap('untitled.tmx')  # comment this if you don't have this file

        self.BusStation = BusStation()
        self.TicketFare = TicketFare(stations)
        self.passengers_data = PassengersData(stations)
        self.BusStation.register_station_change_callback(self.update_current_station)

        self.option_list = list(string.ascii_uppercase)
        print(self.option_list)

        self.widgets()
        self.start_station_thread()
    
    def widgets(self):
        # Title Frame
        self.title_frame = ctk.CTkFrame(self, height=40)
        self.title_frame.pack(side='top', fill='x', padx=10, pady=10)

        self.title_label = ctk.CTkLabel(self.title_frame, text='Bus Services', font=('Arial bold', 30))
        self.title_label.pack(pady=10, padx=10)

        # Left Frame
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=(10, 0), pady=5)

        self.book_ticket_button = ctk.CTkButton(self.left_frame, text="Book Ticket", command=self.book_ticket)
        self.book_ticket_button.pack(pady=10, side='bottom')

        self.welcome_label = ctk.CTkLabel(self.left_frame, text="Welcome to Bus Services", font=("Arial bold", 28))
        self.welcome_label.pack(padx=10, pady=10)

        self.book_now_label = ctk.CTkLabel(self.left_frame, text='Book Your Ticket!', font=('Arial thin bold', 26))
        self.book_now_label.pack(pady=10)

        self.fare_label = ctk.CTkLabel(self.left_frame, text="Fare: ", font=("Arial", 18))
        self.fare_label.pack(side='bottom', pady=10)

        self.destination_choice = ctk.StringVar()
        self.stations_option = ctk.CTkOptionMenu(self.left_frame, values=self.option_list, variable=self.destination_choice, command=(self.update_destination_label))
        self.stations_option.pack(side='bottom', pady='10')

        self.destination_label = ctk.CTkLabel(self.left_frame, text="Destination Station: ", font=("Arial", 18))
        self.destination_label.pack(side='bottom', pady=10)

        self.current_station_label = ctk.CTkLabel(self.left_frame, text=f"Current Station: {stations[0]} ", font=("Arial", 18))
        self.current_station_label.pack(side='bottom', pady=10)

        # Right Frame
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.logs_label = ctk.CTkLabel(self.right_frame, text='System Logs', font=('Arial', 20))
        self.logs_label.pack(padx=10, pady=10)

        # Initialize the table
        self.value = [["Passenger ID", "Departure Station", "Destination Station", "Ticket Fare"]]
        self.table = CTkTable(self.right_frame, values=self.value)
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

    def prepare_passenger_data(self):
        # Prepare the data from passengers_data to fit into the table
        data = []
        for passenger_id, info in self.passengers_data.passengers.items():
            row = [passenger_id, info["Departure Station"], info["Destination Station"], info["Ticket Fare"]]
            data.append(row)
        return data[-1] 

    def update_optionMenu(self):
        menu = stations[self.BusStation.current_station_index]
        if menu == 'Z':
            self.option_list = list(string.ascii_uppercase)
        else:
            self.option_list.remove(menu)
        self.stations_option.configure(values=self.option_list)

    def update_destination_label(self, choice):
        self.destination_label.configure(text=f"Destination Station: {choice}")
        self.calculate_fare_in_thread()

    def update_fare(self):
        departure_station = stations[self.BusStation.current_station_index]
        destination_station = self.destination_choice.get()
        fare = self.TicketFare.calculate_fare(departure_station, destination_station)
        self.fare_label.configure(text=f"Fare: {fare}")

    def book_ticket(self):
        departure_station = stations[self.BusStation.current_station_index]
        destination_station = self.destination_choice.get()
        fare = self.TicketFare.calculate_fare(departure_station, destination_station)
        self.passengers_data.add_data(departure_station, destination_station, fare)
        self.update_passenger_table()
        self.fare_label.configure(text=f"Fare: {fare}")
        messagebox.showinfo("Ticket Booked", f"Your ticket has been booked!\nDeparture: {departure_station}\nDestination: {destination_station}\nFare: {fare}")

    def update_passenger_table(self):
        self.value = self.passengers_data.passengers.items()
        for passenger_id, info in self.passengers_data.passengers.items():
            row = [passenger_id, info["Departure Station"], info["Destination Station"], info["Ticket Fare"]]
            try:
                if  self.passengers_data.userList[-1] == row:
                    self.table.add_row(values=row)
                else:
                    pass
            except :
                print("An unknow error is occurred")
                pass

    def update_current_station(self, current_station):
        self.update_optionMenu()
        self.current_station_label.configure(text=f"Current Station: {current_station}")
        self.passengers_data.step_down(current_station)
        # Show a popup for each passenger who needs to step down
        for p_id, data in list(self.passengers_data.passengers.items()):
            if data['Destination Station'] == current_station:
                
                try:
                    del self.passengers_data.passengers[p_id]
                except RuntimeError:
                    pass
                for row in self.passengers_data.userList:
                    if row[0] == p_id:
                        index = self.passengers_data.userList.index(row)  
                        print("-"*10)
                        print(self.passengers_data.userList) 
                        print(index+1)
                        print("-"*10)
                        self.table.delete_row(index+1)
                        messagebox.showinfo("Station Arrived", f"Passenger {p_id}, your destination {data['Destination Station']} has arrived. Please step down the bus.")

    def start_station_thread(self):
        station_thread = threading.Thread(target=self.BusStation.changing_station)
        station_thread.start()

    def calculate_fare_in_thread(self):
        fare_thread = threading.Thread(target=self.update_fare, daemon=True)
        fare_thread.start()

if __name__ == "__main__":
    app = App()
    app.mainloop()

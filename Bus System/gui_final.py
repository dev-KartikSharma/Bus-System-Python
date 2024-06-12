# Final Build 
# Author --> Kartik Sharma

import threading
import random
from backend import BusStation, TicketFair, PassengersData, stations, passengers
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode('Light')
ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title('Bus Management System')
        self.geometry('800x600')
        # self.iconbitmap('Bus System/untitled.tmx')  # comment this if you don't have this file

        self.BusStation = BusStation()
        self.TicketFair = TicketFair(stations)
        self.passengers_data = PassengersData(stations)

        self.BusStation.register_station_change_callback(self.update_current_station)

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
        self.stations_option = ctk.CTkOptionMenu(self.left_frame, values=stations, variable=self.destination_choice, command=self.update_destination_label)
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

        self.text_area = ctk.CTkTextbox(self.right_frame, width=400, height=500)
        self.text_area.pack(pady=10, padx=10)

    def update_destination_label(self, choice):
        self.destination_label.configure(text=f"Destination Station: {choice}")
        self.calculate_fare_in_thread()

    def calculate_fare_in_thread(self):
        fare_thread = threading.Thread(target=self.update_fare, daemon=True)
        fare_thread.start()

    def update_fare(self):
        departure_station = stations[self.BusStation.current_station_index]
        destination_station = self.destination_choice.get()
        fare = self.TicketFair.calculate_fare(departure_station, destination_station)
        self.fare_label.configure(text=f"Fare: {fare}")

    def book_ticket(self):
        departure_station = stations[self.BusStation.current_station_index]
        destination_station = self.destination_choice.get()
        fare = self.TicketFair.calculate_fare(departure_station, destination_station)
        self.passengers_data.add_data(departure_station, destination_station, fare)
        self.update_passenger_text_area()
        self.fare_label.configure(text=f"Fare: {fare}")
        messagebox.showinfo("Ticket Booked", f"Your ticket has been booked!\nDeparture: {departure_station}\nDestination: {destination_station}\nFare: {fare}")

    def update_passenger_text_area(self):
        self.text_area.delete('1.0', 'end')
        for passenger in self.passengers_data.passengers.items():
            self.text_area.insert('end', f"{passenger}\n")

    def update_current_station(self, current_station):
        self.current_station_label.configure(text=f"Current Station: {current_station}")
        self.passengers_data.step_down(current_station)
        # Show a popup for each passenger who needs to step down
        for p_id, data in list(self.passengers_data.passengers.items()):
            if data['Destination Station'] == current_station:
                messagebox.showinfo("Station Arrived", f"Passenger {p_id}, your destination {data['Destination Station']} has arrived. Please step down the bus.")

    def start_station_thread(self):
        station_thread = threading.Thread(target=self.BusStation.changing_station)
        station_thread.start()


if __name__ == "__main__":
    app = App()
    app.mainloop()

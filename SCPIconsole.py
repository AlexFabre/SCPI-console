import tkinter as tk
from tkinter import messagebox as tkMessageBox
import threading
import serial.tools.list_ports

class SCPIConsole:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SCPI console")
        self.root.minsize(width=600,height=350)


        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side = tk.TOP, padx = 50, pady = 20)

        # Add a dropdown box to select the serial port
        available_ports = [port[0] for port in serial.tools.list_ports.comports()]
        self.selected_port = tk.StringVar(self.top_frame)
        self.selected_port.set(available_ports[0])

        self.port_dropdown = tk.OptionMenu(self.top_frame, self.selected_port, *available_ports)
        self.port_dropdown.pack(side=tk.LEFT)
        self.port_dropdown.configure(width=20)

        # Add an entry field to specify the baudrate
        self.baudrate_entry = tk.Entry(self.top_frame)
        self.baudrate_entry.insert(tk.END, "115200")
        self.baudrate_entry.pack(side=tk.LEFT)
        self.baudrate_entry.configure(width=10)

        self.connect_button = tk.Button(self.top_frame, text="Connect", command=self.connect_serial_port)
        self.connect_button.pack(side=tk.LEFT)


        self.received_text = tk.Text(self.root, height=11, width=50, state = "disabled")
        self.received_text.pack(expand=True, fill=tk.BOTH, padx = 50, pady = 20)

        self.received_text.configure(font=('TkDefaultFont', 11))


        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(side=tk.BOTTOM, padx = 50, pady = 20)

        self.message_entry = tk.Entry(self.message_frame)
        self.message_entry.pack(side=tk.LEFT)
        self.message_entry.configure(width=20)

        self.tail_var = tk.BooleanVar(self.message_frame, value = True)
        self.tail_checkbox = tk.Checkbutton(self.message_frame, text='Tail CRLF (\\r\\n)', variable=self.tail_var)
        self.tail_checkbox.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.message_frame, text="Send", command=self.send_data, state="disabled")
        self.send_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.message_frame, text="Clear", command=self.clear_received_text, state="disabled")
        self.clear_button.pack(side=tk.LEFT)


        self.ser = None

        # Bind the <Return> event to the send_data() function
        self.message_entry.bind("<Return>", lambda event: self.send_data())

        # Initialize messages list
        self.messages = []
        self.prev_messages = []

        # Bind the up arrow key to a function that sets the last message in the list as the value of the message entry field
        self.message_entry.bind('<Up>', lambda event: self.display_previous_message())

    def update_received_text(self, data):
        self.received_text.config(state = "normal")
        if "ERROR" in data.upper():
            self.received_text.insert(tk.END, data + "\n", "received_error")
            self.received_text.tag_config("received_error", foreground="firebrick3", font=("TkDefaultFont", 11, "bold"))
        else:
            self.received_text.insert(tk.END, data + "\n")
        self.received_text.see("end")
        self.received_text.config(state = "disabled")

    def receive_data(self):
        while True:
            if self.ser.in_waiting > 0:
                try:
                    received_data = self.ser.readline().decode('utf-8').strip()
                    self.update_received_text(received_data)
                except:
                    pass

    def connect_serial_port(self):
        try:
            # Get the selected serial port and baudrate
            port = self.selected_port.get()
            baudrate = int(self.baudrate_entry.get())

            # Connect to the serial port
            self.ser = serial.Serial(port, baudrate)

            # Start receiving data
            receive_thread = threading.Thread(target=self.receive_data)
            receive_thread.daemon = True
            receive_thread.start()

            # Disable the port selection and baudrate fields
            self.port_dropdown.config(state='disabled')
            self.baudrate_entry.config(state='disabled')

            # Change the "Connect" button to a "Disconnect" button
            self.connect_button.config(text="Disconnect", command=self.disconnect_serial_port)

            # Enable send button
            self.send_button.config(state="normal")
            self.clear_button.config(state="normal")

        except Exception as e:
            # Show an error message if connection fails
            message = "Error connecting to serial port: {}".format(str(e))
            tkMessageBox.showerror("Error", message)

    def disconnect_serial_port(self):
        # Stop receiving data
        self.ser.close()

        # Enable the port selection and baudrate fields
        self.port_dropdown.config(state='normal')
        self.baudrate_entry.config(state='normal')

        # Change the "Disconnect" button back to a "Connect" button
        self.connect_button.config(text="Connect", command=self.connect_serial_port)

        # Disable send button
        self.send_button.config(state="disabled")

    def send_data(self):
        message = self.message_entry.get().upper()

        if message == "\r" or message == "":
            return
        
        cmd = message

        if self.tail_var.get() == True:
            cmd = cmd + "\r\n"

        self.ser.write(cmd.encode())
        self.received_text.config(state = "normal")
        self.received_text.insert(tk.END, message + "\n", "sent_message")
        self.received_text.tag_config("sent_message", foreground="dodgerblue", font=("TkDefaultFont", 11, "bold"))
        self.received_text.see("end")
        self.received_text.config(state = "disabled")
        # Clear the message entry field after sending the message
        self.message_entry.delete(0, tk.END)
        # Append message to messages list
        self.messages.append(message)
        self.prev_messages = list(self.messages)

    def display_previous_message(self):
        if len(self.prev_messages) > 0:
            # Get last message in messages list
            previous_message = self.prev_messages.pop()
            # Set the value of the message entry field to the last message
            self.message_entry.delete(0, tk.END)
            self.message_entry.insert(0, previous_message)
    
    def clear_received_text(self):
        self.received_text.config(state = "normal")
        self.received_text.delete("1.0", tk.END)
        self.received_text.config(state = "disabled")

    def main(self):
        self.root.mainloop()


if __name__ == "__main__":
    console = SCPIConsole()
    console.main()

# SCPI-console
Little serial GUI intended for SCPI communication

<img width="712" alt="Capture d’écran 2023-05-12 à 13 21 25" src="https://github.com/AlexFabre/SCPI-console/assets/12525735/922a662c-929f-44db-b085-ad3582350638">

## Dependencies

- Python 3
- Tkinter
- PySerial

## Run the script

~~~bash
$ python3 SCPIconsole.py 
~~~

## Connect to target

- Select the Serial port
- Correct the baudrate if `115200` is not the desired speed
- Click `Connect` to open the serial port

## Type your commands

- Input your command in the bottom text area
- You can send the command by pressing "enter" or clicking "send"
- Tab key sends the help command related to your current input to let you see available commands

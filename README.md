# Slutprojekt Programmering 2

Anton Norman och Caspian Mörling

Blackjack game that saves your login information and balance. If you run out of balance, just create a new account ;).

## Requirements

### Python and PIP

Python3.x ~ <https://www.python.org/downloads/>
Pip20.1 ~ <https://pip.pypa.io/en/stable/installing/>

### Dependencies

There is a conflict between pycrypto, crypto and pycryptodome. So make sure you have removed both of these packages before you install pycryptodome.

`# pip uninstall pycrypto crypto`
`# pip install -r requirements.txt`

## Executing

### Server

Run the script to expose a server of localhost
usage: python3 server/main.py [-h] [-c (Clears database)] [-p Port]

Or reset Database without starting server:
python3 scripts/dbReset.py

Note databse must be reset first time running.

### Client

Connect to server and start the client.
Run the client with the ip and port of the server to establish a connection, then log in with your credentials and start playing balackjack. You can save your credentials in config.txt.

usage: client.py [-h] [-i IP] [-p Port]

## TODO

Implement Change Password, logout and delete account on client side.

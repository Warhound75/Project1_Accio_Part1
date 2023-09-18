import sys
import socket
import os

def main():
    # Check the number of command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <hostname> <port> <filename>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    try:
        # Create a socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))

        # Implement the logic to receive accio commands, send confirmations, and transfer the file
        # You'll need to handle timeouts and errors here

        # Example: Receive the first accio command
        first_accio = client_socket.recv(8).decode('utf-8')
        if first_accio != "accio\r\n":
            print("ERROR: Unexpected response from the server.")
            sys.exit(1)

        # Send the first confirmation
        client_socket.send("confirm-accio\r\n".encode('utf-8'))

        # Receive the second accio command
        second_accio = client_socket.recv(8).decode('utf-8')
        if second_accio != "accio\r\n":
            print("ERROR: Unexpected response from the server.")
            sys.exit(1)

        # Send the second confirmation
        client_socket.send("confirm-accio-again\r\n\r\n".encode('utf-8'))

        # Open the file for binary reading
        with open(filename, 'rb') as file:
            while True:
                # Read a chunk of data from the file
                chunk = file.read(10000)
                if not chunk:
                    break

                # Send the chunk to the server
                client_socket.send(chunk)

        # Close the socket and exit with a success code
        client_socket.close()
        sys.exit(0)

    except socket.error as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

import sys
import socket
import gradescope

def main():
    # Check command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 client.py <hostname> <port> <filename>")
        sys.exit(1)

    # Parse command-line arguments
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    try:
        # Create a socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))

        # Step 1: Receive the first "accio\r\n" command from the server
        accio1 = client_socket.recv(8).decode('utf-8')
        if accio1 != "accio\r\n":
            print("ERROR: Unexpected response from the server.")
            sys.exit(1)

        # Step 2: Send the first confirmation "confirm-accio\r\n"
        client_socket.send("confirm-accio\r\n".encode('utf-8'))

        # Step 3: Receive the second "accio\r\n" command from the server
        accio2 = client_socket.recv(8).decode('utf-8')
        if accio2 != "accio\r\n":
            print("ERROR: Unexpected response from the server.")
            sys.exit(1)

        # Step 4: Send the second confirmation "confirm-accio-again\r\n\r\n"
        client_socket.send("confirm-accio-again\r\n\r\n".encode('utf-8'))

        # Step 5: Open the file for binary reading
        with open(filename, 'rb') as file:
            while True:
                # Step 6: Read and send the file in chunks
                chunk = file.read(10000)
                if not chunk:
                    break
                client_socket.send(chunk)

        # Step 7: Close the socket and exit with a success code
        client_socket.close()

    except socket.error as e:
        # Handle socket errors here
        print(f"ERROR: {str(e)}")
        sys.exit(1)

    except Exception as e:
        # Handle other exceptions and errors here
        print(f"ERROR: {str(e)}")
        sys.exit(1)

    # Submit the file to Gradescope before exiting
    gradescope.submit(filename)

if __name__ == "__main__":
    main()

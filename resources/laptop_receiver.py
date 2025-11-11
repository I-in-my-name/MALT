import serial
import time
import csv

# --- Configuration ---
SERIAL_PORT = '/dev/ttyUSB0' # Change this to your ESP32's serial port (e.g., 'COM3' on Windows)
BAUD_RATE = 115200
OUTPUT_FILENAME = 'esp32_data_log.csv'

def receive_and_log_data():
    """Reads data from the ESP32 and logs it to a CSV file."""
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE}...")
    
    try:
        # Open the serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 
        time.sleep(2) # Wait for the connection to stabilize

        # Open the CSV file for writing
        with open(OUTPUT_FILENAME, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Write a header row (assuming you send three values: Time, Value1, Value2)
            csv_writer.writerow(['Timestamp', 'Value1', 'Value2']) 
            
            print(f"Data will be logged to {OUTPUT_FILENAME}. Press Ctrl+C to stop.")
            
            # Loop indefinitely to receive data
            while True:
                # Read until a newline character is found (our delimiter)
                line = ser.readline().decode('utf-8').strip()

                if line:
                    # The ESP32 should send comma-separated values (CSV format)
                    data_values = line.split(',') 
                    
                    if len(data_values) == 3: # Check if we received the expected number of values
                        csv_writer.writerow(data_values)
                        csvfile.flush() # Force write to disk immediately
                        print(f"Received: {line}")
                    else:
                        print(f"Skipped malformed line: {line}")

    except serial.SerialException as e:
        print(f"\nSerial communication error: {e}")
        print("Check if the ESP32 is connected and the port is correct.")
    except KeyboardInterrupt:
        print("\nStopping data logging and closing port.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == '__main__':
    receive_and_log_data()
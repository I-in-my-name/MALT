import serial
import time
import csv

# --- Configuration ---
SERIAL_PORT = '/dev/ttyUSB1' # <-- CHECK THIS! (e.g., 'COM3' on Windows)
BAUD_RATE = 115200
OUTPUT_FILENAME = 'esp32_data_log.csv'

def receive_and_log_data():
    """Reads data from the ESP32 and logs it to a CSV file."""
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE}...")
    
    # Initialize 'ser' to None so it is always bound (The Fix)
    ser = None 
    
    try: 
        with open(OUTPUT_FILENAME, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 
            time.sleep(2) # Wait for the connection to stabilize
        
            csv_writer = csv.writer(csvfile)
            
            # Write a header row (assuming three values: Timestamp, Value1, Value2)
            csv_writer.writerow(['Index', 'Value1']) 
            
            print(f"Data will be logged to {OUTPUT_FILENAME}. Press Ctrl+C to stop.")
            
            while True:
                try:
                    # Read until a newline character is found (our delimiter)
                    # It's better to use readline() than read() for line-delimited data
                    line = ser.readline().decode('utf-8').strip()

                    if line:
                        # The ESP32 should send comma-separated values (CSV format)
                        data_values = line.split(',') 
                        
                        if len(data_values) == 2: 
                            csv_writer.writerow(data_values)
                            csvfile.flush() # Force write to disk immediately
                            print(f"Received: {line}")
                        else:
                            print(f"Skipped malformed line: {line} (Expected 2 values)")          
                except Exception: 
                    pass
        
            
    except Exception: 
        print(f"FUCK")

if __name__ == '__main__':
    receive_and_log_data()
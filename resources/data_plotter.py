import pandas as pd
import matplotlib.pyplot as plt

# --- Configuration ---
INPUT_FILENAME = 'esp32_data_log.csv'

def plot_data():
    """Reads data from the CSV file and generates a simple plot."""
    try:
        # 1. Read the data using pandas
        df = pd.read_csv(INPUT_FILENAME)
        
        # Ensure the 'Timestamp' column is treated as the index for time-series plotting
        # Note: If your Timestamp is a float/integer, you might need to convert it to datetime
        # df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
        
        # 2. Plotting
        plt.figure(figsize=(12, 6))
        
        # Plot Value1 against Timestamp
        plt.plot(df['Timestamp'], df['Value1'], label='Value 1', marker='o', linestyle='-', markersize=2)
        
        # Plot Value2 against Timestamp
        plt.plot(df['Timestamp'], df['Value2'], label='Value 2', marker='x', linestyle='--', markersize=2)
        
        # 3. Finalize Plot
        plt.title('ESP32 Sensor Data Plot')
        plt.xlabel('Timestamp')
        plt.ylabel('Sensor Value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILENAME}' not found. Run the receiver script first.")
    except Exception as e:
        print(f"An error occurred during plotting: {e}")

if __name__ == '__main__':
    # Ensure you have the required libraries: pip install pandas matplotlib
    plot_data()
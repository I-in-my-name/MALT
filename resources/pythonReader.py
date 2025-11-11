import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np

# --- Configuration ---
PORT = 'COM3'  # !! CHANGE THIS to your ESP32's serial port !!
BAUD_RATE = 115200 
MAX_POINTS = 100 # How many data points to show in the scrolling window
# ---------------------

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2) # Wait for serial connection to stabilize
except serial.SerialException as e:
    print(f"Error opening serial port {PORT}: {e}")
    exit()

# Data structures to store the rolling data for the plot
time_data = deque(maxlen=MAX_POINTS)
y1_data = deque(maxlen=MAX_POINTS)
y2_data = deque(maxlen=MAX_POINTS)

# Matplotlib setup for live plotting
fig, ax = plt.subplots(figsize=(10, 6))
# Create the initial plot lines
line1, = ax.plot(time_data, y1_data, label='Signal 1 (Sin)', color='r')
line2, = ax.plot(time_data, y2_data, label='Signal 2 (Cos)', color='b')
ax.legend()
ax.set_title("Live Data from ESP32")
ax.set_xlabel("Time Step (Index)")
ax.set_ylabel("Value")


def animate(i):
    """Function called repeatedly by FuncAnimation to update the plot."""
    global ser # Use the global serial object

    try:
        # Read all available lines from the serial buffer
        while ser.in_waiting:
            line = ser.readline().decode('ascii').strip()
            
            if line:
                # Expecting CSV: Index, Value1, Value2
                data_points = line.split(',')
                if len(data_points) >= 3:
                    try:
                        index, val1, val2 = map(float, data_points[:3])
                        
                        # Add new data to the deques (oldest data is automatically removed)
                        time_data.append(index)
                        y1_data.append(val1)
                        y2_data.append(val2)
                        
                    except ValueError:
                        # Ignore malformed data lines
                        pass

        # Update plot data only if we have collected new points
        if time_data:
            line1.set_data(list(time_data), list(y1_data))
            line2.set_data(list(time_data), list(y2_data))
            
            # Auto-scale X-axis
            ax.set_xlim(time_data[0], time_data[-1])
            
            # Auto-scale Y-axis based on all current data
            all_y = list(y1_data) + list(y2_data)
            if all_y:
                ax.set_ylim(min(all_y) - 0.1, max(all_y) + 0.1)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Stop animation on error or serial disconnect
        ani.event_source.stop()
        ser.close()


print(f"Listening on {PORT}. Press Ctrl+C to stop...")

# Set up the animation: calls 'animate' function every 50ms
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False) 

try:
    plt.show() # Blocks execution until the plot window is closed
except KeyboardInterrupt:
    print("\nPlotting stopped by user.")
finally:
    if ser.is_open:
        ser.close()
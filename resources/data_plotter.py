import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

def plot_data():
    """
    Reads the embedded CSV data and generates a time-series plot of
    'Value1' and 'Value2' against 'Timestamp'.
    """
    # The user-provided data is embedded as a multi-line string

    # Use io.StringIO to treat the string as a file and load it into a pandas DataFrame
    try:
        df = pd.read_csv("esp32_data_log.csv")
    except Exception as e:
        print(f"Error loading data into pandas: {e}")
        return

    print("Data successfully loaded. Displaying DataFrame head:")
    print(df.head())

    # --- Plotting the Data ---
    df.reset_index(drop=False,inplace=True)
    df['Value1'] = np.log(df['Value1'])
    df['Value2'] = np.log(df['Value2'])
    
    # df['Value1'] = df.loc[(df['Value1'] < df['Value1'].mean()+ 3*df['Value1'].std()) & (df['Value1'] > df['Value1'].mean() - 3*df['Value1'].std()), 'Value1'] # type: ignore
    # df['Value2'] = df.loc[(df['Value2'] < df['Value2'].mean()+ 3*df['Value2'].std()) &(df['Value2'] > df['Value2'].mean() - 3*df['Value2'].std()), 'Value2'] # type: ignore
    # 1. Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # 2. Plot Value1 and Value2 against Timestamp
    # Timestamp is on the x-axis (time in seconds)
    ax.plot(df['index'], df['Value1'], label='Value 1 (Units)', marker='o', linestyle='-', color='teal')
    ax.plot(df['index'], df['Value2'], label='Value 2 (Units)', marker='x', linestyle='--', color='darkorange')

    # 3. Add Titles and Labels
    ax.set_title('Time-Series Analysis of Value 1 and Value 2', fontsize=16, fontweight='bold')
    ax.set_xlabel('Time (Seconds)', fontsize=12)
    ax.set_ylabel('Data Values (Units)', fontsize=12)

    # 4. Enhance the Plot
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Optional: Rotate x-axis ticks for better readability if timestamps were complex
    # plt.xticks(rotation=45, ha='right') 

    # 5. Add a tight layout to prevent labels from overlapping
    plt.tight_layout()

    # 6. Display the plot
    plt.show()

if __name__ == "__main__":
    plot_data()
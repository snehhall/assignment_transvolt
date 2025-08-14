import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from flask import Flask, render_template
import os

#importing my data
df = pd.read_csv(r"C:\Users\hp\Downloads\Sample_Data.csv") 
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.rename(columns={'Values': 'Voltage'}, inplace=True)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

print(df.head())


# 5 day moving average
df['MA_5'] = df['Voltage'].rolling(window=5).mean()

peaks, _ = find_peaks(df['Voltage'])
lows, _ = find_peaks(-df['Voltage'])

peaks_df = df.iloc[peaks][['Timestamp', 'Voltage']]
lows_df = df.iloc[lows][['Timestamp', 'Voltage']]

low_voltage_df = df[df['Voltage'] < 20][['Timestamp', 'Voltage']]

df['diff'] = df['Voltage'].diff()
df['accel'] = df['diff'].diff()
downward_accel_df = df[(df['accel'] < 0) & (df['diff'] < 0)][['Timestamp', 'Voltage', 'diff', 'accel']]

os.makedirs("static", exist_ok=True)

plt.figure(figsize=(12,6))
plt.plot(df['Timestamp'], df['Voltage'], label='Original Values', color='blue')
plt.plot(df['Timestamp'], df['MA_5'], label='5-day Moving Average', color='orange')
plt.xlabel("Timestamp")
plt.ylabel("Voltage")
plt.title("Voltage vs Timestamp with 5-day Moving Average")
plt.legend()
plt.grid(True)
plt.savefig("static/voltage_ma.png")
plt.close()

plt.figure(figsize=(12,6))
plt.plot(df['Timestamp'], df['Voltage'], color='blue')
plt.scatter(peaks_df['Timestamp'], peaks_df['Voltage'], color='red', label='Peaks')
plt.scatter(lows_df['Timestamp'], lows_df['Voltage'], color='green', label='Lows')
plt.xlabel("Timestamp")
plt.ylabel("Voltage")
plt.title("Voltage Peaks & Lows")
plt.legend()
plt.grid(True)
plt.savefig("static/peaks_lows.png")
plt.close()

plt.figure(figsize=(12,6))
plt.plot(df['Timestamp'], df['Voltage'], color='blue')
plt.scatter(downward_accel_df['Timestamp'], downward_accel_df['Voltage'], color='purple', label='Downward Accel')
plt.xlabel("Timestamp")
plt.ylabel("Voltage")
plt.title("Downward Acceleration Points")
plt.legend()
plt.grid(True)
plt.savefig("static/downward_accel.png")
plt.close()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html",
        peaks=peaks_df.to_html(index=False),
        lows=lows_df.to_html(index=False),
        low_voltage=low_voltage_df.to_html(index=False),
        downward_accel=downward_accel_df.to_html(index=False)
    )

if __name__ == "__main__":
    app.run(debug=True)

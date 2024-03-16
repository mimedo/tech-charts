import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

# Step 1: Data Collection
stock_symbol = "AAPL"
data = yf.download(stock_symbol, start="2020-01-01", end="2023-01-01")

# Step 2: Data Preprocessing
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data["Close"].values.reshape(-1, 1))

# Split data into train and test sets
train_size = int(len(scaled_data) * 0.80)
train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]

# Step 3: Model Training
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

time_steps = 100
X_train, y_train = create_dataset(train_data, time_steps)
X_test, y_test = create_dataset(test_data, time_steps)

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(time_steps, 1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=32)

# Step 4: Prediction
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# Step 5: Visualization
plt.plot(data.index[train_size + time_steps + 1:], data["Close"][train_size + time_steps + 1:], label='Actual Stock Price')
plt.plot(data.index[train_size + time_steps + 1:], predictions, label='Predicted Stock Price')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('Stock Price Prediction')
plt.legend()
plt.show()

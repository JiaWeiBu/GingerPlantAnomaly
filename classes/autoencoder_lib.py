import torch # type: ignore
import torch.nn as nn # type: ignore
import torch.optim as optim # type: ignore
import numpy as np
from sklearn.preprocessing import StandardScaler # type: ignore
from torch.utils.data import DataLoader, TensorDataset # type: ignore

# 1. Data Preprocessing
def preprocess_data(data):
    """
    Scales data to have zero mean and unit variance.
    
    Args:
        data (numpy array): Input data to be preprocessed.

    Returns:
        torch.Tensor: Scaled data as PyTorch tensor.
        StandardScaler: Fitted scaler for inverse transformation.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return torch.tensor(scaled_data, dtype=torch.float32), scaler

# 2. Building the Autoencoder Model
class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU()
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# 3. Training the Autoencoder
def train_autoencoder(model, data, epochs=50, batch_size=32, learning_rate=0.001):
    """
    Trains the autoencoder model on the given data.

    Args:
        model (nn.Module): Autoencoder model.
        data (torch.Tensor): Training data.
        epochs (int): Number of training epochs.
        batch_size (int): Batch size for training.
        learning_rate (float): Learning rate for optimizer.

    Returns:
        list: Training loss for each epoch.
    """
    data_loader = DataLoader(TensorDataset(data, data), batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()
    losses = []

    for epoch in range(epochs):
        epoch_loss = 0
        for batch_data, _ in data_loader:
            optimizer.zero_grad()
            reconstructed = model(batch_data)
            loss = criterion(reconstructed, batch_data)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        losses.append(epoch_loss / len(data_loader))
    return losses

# 4. Calculating Reconstruction Error
def calculate_reconstruction_error(model, data):
    """
    Computes the reconstruction error for each sample in the data.
    
    Args:
        model (nn.Module): Trained autoencoder model.
        data (torch.Tensor): Data on which to calculate reconstruction error.

    Returns:
        numpy array: Reconstruction error for each sample.
    """
    with torch.no_grad():
        reconstructed_data = model(data)
    errors = torch.mean((data - reconstructed_data) ** 2, dim=1).numpy()
    return errors

# 5. Setting Threshold and Detecting Anomalies
def set_threshold(errors, factor=1.5):
    """
    Sets a threshold for anomaly detection based on the error distribution.
    
    Args:
        errors (numpy array): Reconstruction errors.
        factor (float): Multiplicative factor for setting threshold above mean error.

    Returns:
        float: Threshold for anomaly detection.
    """
    threshold = np.mean(errors) + factor * np.std(errors)
    return threshold

def detect_anomalies(errors, threshold):
    """
    Identifies samples with reconstruction error above the threshold as anomalies.
    
    Args:
        errors (numpy array): Reconstruction errors for each sample.
        threshold (float): Threshold for determining anomalies.

    Returns:
        numpy array: Boolean array where True indicates an anomaly.
    """
    anomalies = errors > threshold
    return anomalies


def run_model():
    # Example data
    data = np.random.normal(0, 1, (1000, 20))  # Random normal data for demonstration
    scaled_data, scaler = preprocess_data(data)

    # Build and train autoencoder
    input_dim = scaled_data.shape[1]
    autoencoder = Autoencoder(input_dim=input_dim)
    train_autoencoder(autoencoder, scaled_data, epochs=100)

    # Calculate reconstruction error
    errors = calculate_reconstruction_error(autoencoder, scaled_data)

    # Set threshold and detect anomalies
    threshold = set_threshold(errors, factor=1.5)
    anomalies = detect_anomalies(errors, threshold)

    print("Number of anomalies detected:", np.sum(anomalies))

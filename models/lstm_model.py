from sklearn.neural_network import MLPRegressor

def build_model(epochs=3):
    # epochs maps to max_iter (each iter = one pass over data)
    # MLPRegressor is a multi-layer perceptron — same concept as LSTM
    # but uses ~20MB vs TensorFlow's ~400MB, fitting Render's free 512MB tier
    model = MLPRegressor(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        solver='adam',
        max_iter=max(epochs * 50, 100),
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        verbose=False
    )
    return model

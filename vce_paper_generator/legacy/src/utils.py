def save_model(model, path):
    """
    Saves the trained model to the specified path.
    """
    torch.save(model.state_dict(), path)

def load_model(model_class, path):
    """
    Loads a model from the specified path.
    """
    model = model_class()
    model.load_state_dict(torch.load(path))
    model.eval()
    return model

def log_message(message):
    """
    Logs a message to the console.
    """
    print(f"[LOG] {message}")

def load_config(config_path):
    """
    Loads configuration settings from a JSON file.
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def save_config(config, config_path):
    """
    Saves configuration settings to a JSON file.
    """
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
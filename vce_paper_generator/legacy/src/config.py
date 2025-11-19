# Configuration settings for the VCE Papers Model project

import os

class Config:
    # Data directories
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    METHODS_DATA_DIR = os.path.join(PROCESSED_DATA_DIR, 'methods')
    SPECIALIST_DATA_DIR = os.path.join(PROCESSED_DATA_DIR, 'specialist')

    # Model directories
    MODELS_DIR = os.path.join(os.path.dirname(__file__), '../models')
    METHODS_MODEL_PATH = os.path.join(MODELS_DIR, 'methods', 'm1.pt')
    SPECIALIST_MODEL_PATH = os.path.join(MODELS_DIR, 'specialist', 's1.pt')

    # Training parameters
    EPOCHS = 10
    BATCH_SIZE = 32
    LEARNING_RATE = 5e-5

    # Other configurations
    SEED = 42
    MAX_LENGTH = 512  # Maximum length of input sequences

    @staticmethod
    def print_config():
        print("Configuration Settings:")
        print(f"Data Directory: {Config.DATA_DIR}")
        print(f"Raw Data Directory: {Config.RAW_DATA_DIR}")
        print(f"Processed Data Directory: {Config.PROCESSED_DATA_DIR}")
        print(f"Methods Data Directory: {Config.METHODS_DATA_DIR}")
        print(f"Specialist Data Directory: {Config.SPECIALIST_DATA_DIR}")
        print(f"Methods Model Path: {Config.METHODS_MODEL_PATH}")
        print(f"Specialist Model Path: {Config.SPECIALIST_MODEL_PATH}")
        print(f"Epochs: {Config.EPOCHS}")
        print(f"Batch Size: {Config.BATCH_SIZE}")
        print(f"Learning Rate: {Config.LEARNING_RATE}")
        print(f"Seed: {Config.SEED}")
        print(f"Max Length: {Config.MAX_LENGTH}")
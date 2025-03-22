# VCE Papers Model

This project aims to develop two separate models for generating VCE (Victorian Certificate of Education) Maths papers: one for Methods and another for Specialist Maths. The models will be trained using a collection of VCE papers in PDF format.

## Project Structure

- **data/**: Contains the original and processed VCE papers.
  - **raw/**: Original VCE papers in PDF format.
  - **processed/**: Processed data for both models.
    - **methods/**: Processed data specifically for the VCE Methods model.
    - **specialist/**: Processed data specifically for the VCE Specialist Maths model.

- **models/**: Contains the trained model files.
  - **methods/**: Trained model for VCE Methods.
    - **model.pt**: Model weights for the VCE Methods model.
  - **specialist/**: Trained model for VCE Specialist Maths.
    - **model.pt**: Model weights for the VCE Specialist Maths model.

- **notebooks/**: Contains Jupyter notebooks for exploratory data analysis and experimentation.
  - **exploratory.ipynb**: Notebook for visualizations and analysis.

- **src/**: Contains source code for preprocessing, training, and evaluation.
  - **preprocessing.py**: Functions for loading, cleaning, and preprocessing PDF data.
  - **training_methods.py**: Code for training the VCE Methods model.
  - **training_specialist.py**: Code for training the VCE Specialist Maths model.
  - **evaluation.py**: Functions for evaluating model performance.
  - **utils.py**: Utility functions for logging, saving models, and loading configurations.
  - **config.py**: Configuration settings for data paths, model parameters, and training hyperparameters.

- **requirements.txt**: Lists the Python dependencies required for the project.

## Setup Instructions

1. **Clone the Repository**: 
   Clone this repository to your local machine.

2. **Install Dependencies**: 
   Navigate to the project directory and install the required packages using:
   ```
   pip install -r requirements.txt
   ```

3. **Prepare Data**: 
   Place your original VCE papers in the `data/raw/` directory. The papers should be in PDF format.

4. **Preprocess Data**: 
   Run the preprocessing script to convert the raw PDF files into a format suitable for training. This can be done by executing:
   ```
   python src/preprocessing.py
   ```

5. **Train Models**: 
   Train the VCE Methods and Specialist Maths models by running:
   ```
   python src/training_methods.py
   python src/training_specialist.py
   ```

6. **Evaluate Models**: 
   After training, evaluate the models using:
   ```
   python src/evaluation.py
   ```

## Usage Guidelines

- Use the Jupyter notebook in the `notebooks/` directory for exploratory data analysis and visualizations.
- Modify the configuration settings in `src/config.py` as needed for different training parameters or data paths.
- Ensure that the processed data is correctly structured in the `data/processed/` directory before training the models.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Blood Report Disease Diagnosis with Machine Learning

This project is a Flask web application that uses a machine learning model to predict various blood disorders based on user-provided blood test results. The application uses a **Random Forest Classifier** to analyze blood parameters such as WBC count, RBC count, Hemoglobin levels, and more to predict potential blood disorders like Anemia, Leukocytosis, Thrombocytopenia, and others.

<div style="text-align: center;">
    <img src="images/HomePage.jpg" alt="Blood Disease Detection App" width="500"/>
</div>

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- Predicts blood disorders based on user inputs of blood parameters.
- Provides reasons or potential causes for each prediction.
- Allows users to register, log in, and save prediction history.
- Displays a history of past predictions for logged-in users.

## Installation

### Prerequisites
- Python 3.x
- `pip` (Python package manager)
- SQLite (for the database)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Rifaque/Blood-Report-Disease-Diagnosis-App.git
    ```
2. **Navigate into the project directory**:
    ```bash
    cd Blood-Report-Disease-Diagnosis-App
    ```
3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the application**:
    ```bash
    flask run
    ```
   The app will run locally, and you can access it at `http://127.0.0.1:5000/`.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Register or log in with your credentials.
3. Enter the blood test results such as WBC, RBC, Hemoglobin, Platelets, etc.
4. Click "Submit" to see the prediction and potential causes of the disorder.
5. View your prediction history by navigating to the "History" page.

### Example Input:
- WBC: 5.0
- RBC: 4.7
- Hemoglobin: 13.0
- Platelets: 200
- Neutrophils: 60
- Lymphocytes: 30
- Monocytes: 4
- Eosinophils: 2
- Basophils: 0.5

### Example Output:
- **Predicted Disorder**: Anemia
- **Possible Causes**:
    - Anemia due to blood loss
    - Bone marrow disorders
    - Nutritional deficiency
    - Chronic kidney disease

## Technologies Used

- **Python**: Core programming language for backend and machine learning.
- **Flask**: Web framework for handling HTTP requests and routing.
- **scikit-learn**: Used for the Random Forest Classifier model.
- **Pandas and NumPy**: For data manipulation and handling.
- **SQLite**: Database for storing user information and history.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

- **Authors**: Rifaque Ahmed and Raif Karani
- **Email**: [rifaque123@gmail.com](mailto:rifaque123@gmail.com)
- **GitHub**: [https://github.com/Rifaque](https://github.com/Rifaque)

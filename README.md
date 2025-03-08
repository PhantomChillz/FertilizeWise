 # FertilizeWise

FertilizeWise is a Django-based machine learning application that provides fertilizer recommendations based on soil type, weather conditions, and crop selection. It utilizes a Decision Tree algorithm to analyze data and suggest the best fertilizer options.

## Features
- **Machine Learning Model:** Implements a Decision Tree algorithm for accurate fertilizer prediction.
- **Django Backend:** Handles user input, processes data, and delivers recommendations.
- **SQLite Database:** Stores soil, crop, and fertilizer-related information.
- **REST API Support:** Provides API endpoints for integration.
- **User-Friendly Interface:** Simple input form for users to get fertilizer suggestions.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django
- SQLite
- Required Python libraries (see `requirements.txt`)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/PhantomChillz/FertilizeWise.git
   cd FertilizeWise
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
6. Open your browser and go to `http://127.0.0.1:8000/`

## Usage
- Enter soil type, weather conditions, and crop type in the input form.
- Click on the "Get Recommendation" button.
- The system will analyze the data and provide the best fertilizer suggestion.

## Dataset
The system uses an SQLite database containing predefined soil types, weather conditions, crop varieties, and recommended fertilizers.

## Machine Learning Model
- Implemented using **Decision Tree Algorithm**.
- Trained on a dataset featuring various soil conditions, weather parameters, and crop-fertilizer relationships.
- Predicts the most suitable fertilizer based on user input.

## API Endpoints
FertilizeWise also provides API endpoints for external integration:
- `GET /predict/` - Fetch fertilizer suggestions based on query parameters.
- `POST /predict/` - Submit input data to receive fertilizer recommendations.

## Contributing
Contributions are welcome! Feel free to fork this repository, create a new branch, and submit a pull request.

## Contact
For any issues or inquiries, reach out via email or open an issue on GitHub.

---
### Authors
[Akshay Rushi](https://github.com/PhantomChillz)
[Harshitha Gummadi](https://github.com/Harshitha9407)
[Akshay Reddy Kalem](https://github.com/A-R-K-7)
[Sri bala Tejesh](https://github.com/SRIBALATEJESH)

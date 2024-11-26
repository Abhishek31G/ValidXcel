# ValidXcel  

ValidXcel is a Django-based web application that allows users to upload, validate, and manage Excel files containing specific data. It provides a user-friendly interface for uploading `.xlsx` files, 
performs structure and content validation, and stores valid data in the database. Users can also view and analyze uploaded data with ease.

## Features  
- **File Upload:** Upload Excel files with `.xlsx` extension through a web interface.  
- **Data Validation:**  
  - Ensures the file contains the required columns (`Sno`, `FirstName`, `LastName`, `Gender`, `DateofBirth`) in the correct order.  
  - Validates data for content rules like non-empty fields, specific value formats, and uniqueness.  
- **Error Reporting:** Provides detailed feedback on validation errors, including row and column details.  
- **Database Storage:** Inserts valid data into the database, linked to the uploaded file's unique identifier.  
- **Data Viewing:** Allows users to view uploaded data by file and analyze it graphically.  
- **User Dashboard:** Displays graphical representations of user demographics (age and gender distribution).  

---

## Prerequisites  
Before setting up the project, ensure the following dependencies are installed:  
- **Python**: Version 3.10 or higher.  
- **Django**: Version 5.1.2.  
- **A virtual environment tool**: `venv` or `virtualenv`.  
- **pip**: Python package manager.  
- **Stable Internet Connection**: Required for downloading dependencies.  

---

## Setup Instructions  

### 1. Clone the Repository  
Clone the repository to your local machine:  
```bash  
git clone https://github.com/your-username/ValidXcel.git  
cd ValidXcel  
```
### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
Copy code
python -m venv venv  
source venv/bin/activate    # For macOS/Linux  
venv\Scripts\activate       # For Windows
```
### 3. Install Dependencies
Install the required Python packages:
```
bash
pip install -r requirements.txt
```
### 4. Apply Migrations
Set up the database by running migrations:
```
bash
python manage.py makemigrations  
python manage.py migrate
```
### 5. Create a Superuser
Create an admin user to manage the application:
```
bash
python manage.py createsuperuser
```
### 6. Run the Development Server
Start the local development server:
```
bash
python manage.py runserver
```
### 7. Access the Application
Application: http://127.0.0.1:8000
Admin Panel: http://127.0.0.1:8000/admin
Application Functionality
- i) File Upload Page
Allows users to upload .xlsx files. Validates the file structure and content before processing.

- ii) Validation and Error Reporting
Ensures the file contains five specific columns:
Sno, FirstName, LastName, Gender, DateofBirth.
Checks data for:
Non-empty and valid values.
Unique Sno entries.
Proper date format (YYYY-MM-DD).
Gender restricted to M, F, or O.
Provides feedback on any validation errors, including the specific rows and columns causing issues.
- iii) Data Management
Inserts valid data into the database.
Links data to the corresponding uploaded file for easy reference.
- iv) View Data
Displays data uploaded for each file, showing details like upload date and the number of valid rows.

- v) Dashboard Page
Provides graphical representations of user demographics based on:
- Age distribution.
- Gender ratios.
### Additional Notes
- i) Static Files
Ensure the STATIC_ROOT is configured properly when deploying the app to serve static files.

- ii) Media Files
Uploaded files are stored in the MEDIA_ROOT directory. Make sure to configure media handling in the deployment environment.

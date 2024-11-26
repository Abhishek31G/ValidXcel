from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ExcelUploadForm
from .models import *
from django.db import transaction
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt  # type: ignore
from io import BytesIO
import base64
from django.db.models import Count

from valix import models

from django.db import IntegrityError

from datetime import datetime
import pandas as pd

from django.db import IntegrityError



def validate_and_process_excel(file):
    # Ensure the file has the correct extension
    if not file.name.endswith('.xlsx'):
        return False, "Invalid file format. Only .xlsx files are accepted."
    
    try:
        df = pd.read_excel(file, engine='openpyxl')
    except ValueError:
        return False, "Invalid file format. Please upload a valid .xlsx file."
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

    required_columns = ["Sno", "FirstName", "LastName", "Gender", "DateofBirth"]
    if list(df.columns) != required_columns:
        return False, f"Invalid columns. Required: {', '.join(required_columns)}."

    errors = []
    for i, row in df.iterrows():
        # Validation for each column
        if not isinstance(row['Sno'], str):
            errors.append(f"Row {i + 1}, Sno must be a string.")
        if not isinstance(row['FirstName'], str) or not (0 < len(row['FirstName']) <= 50):
            errors.append(f"Row {i + 1}, FirstName is invalid.")
        if not isinstance(row['LastName'], str) or not (0 < len(row['LastName']) <= 50):
            errors.append(f"Row {i + 1}, LastName is invalid.")
        if row['Gender'] not in ['M', 'F', 'O']:
            errors.append(f"Row {i + 1}, Gender must be 'M', 'F', or 'O'.")

        # Handle the DateofBirth column
        try:
            dob = row['DateofBirth']
            if pd.isna(dob):
                errors.append(f"Row {i + 1}, DateofBirth is missing.")
            elif isinstance(dob, pd.Timestamp):
                dob = dob.date()
            elif isinstance(dob, str):
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            else:
                errors.append(f"Row {i + 1}, DateofBirth is invalid format. Expected YYYY-MM-DD.")

            # Ensure DateofBirth is in the past
            if dob >= datetime.now().date():
                errors.append(f"Row {i + 1}, DateofBirth must be in the past.")
        except Exception as e:
            errors.append(f"Row {i + 1}, DateofBirth error: {str(e)}.")

    if errors:
        return False, errors

    # Only create the UploadedFile instance if no validation errors were found
    with transaction.atomic():
        uploaded_file = UploadedFile.objects.create(file=file, row_count=len(df))
        for _, row in df.iterrows():
            # Ensure there are no duplicates before creating UserData entries
            if not UserData.objects.filter(first_name=row['FirstName'], last_name=row['LastName']).exists():
                UserData.objects.create(
                    file=uploaded_file,
                    sno=row['Sno'],
                    first_name=row['FirstName'],
                    last_name=row['LastName'],
                    gender=row['Gender'],
                    date_of_birth=row['DateofBirth']
                )
            else:
                errors.append(f"Duplicate entry for {row['FirstName']} {row['LastName']} found.")
    
    # Check again if any errors occurred after user data creation (like duplicate detection)
    if errors:
        uploaded_file.delete()  # Rollback by deleting the file entry if errors occurred
        return False, errors
    return True, uploaded_file.file_id


def upload_file_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Debugging: Check the file details
            uploaded_file = request.FILES['excel_file']
            print("Uploaded file name:", uploaded_file.name)
            print("Uploaded file size:", uploaded_file.size)

            # Validate and process the file
            is_valid, result = validate_and_process_excel(uploaded_file)
            if is_valid:
                messages.success(request, "File uploaded successfully!")
                return redirect('view_data', file_id=result)
            else:
                messages.error(request, ' '.join(result))
    else:
        form = ExcelUploadForm()
    return render(request, 'upload.html', {'form': form})


def view_data(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, file_id=file_id)
    data = uploaded_file.data.all()
    return render(request, 'view_data.html', {'data': data, 'file': uploaded_file})

from django.urls import reverse

def dashboard_view(request):
    # Retrieve all uploaded files and user data
    uploaded_files = UploadedFile.objects.all()  # Assuming UploadedFile stores each uploaded file record
    users = UserData.objects.all()

    # Gender distribution data
    gender_data = users.values('gender').annotate(count=Count('gender'))
    
    # Calculate age distribution from date of birth
    ages = [datetime.now().year - user.date_of_birth.year for user in users]

    # Plotting gender distribution
    fig, ax = plt.subplots()
    ax.bar([x['gender'] for x in gender_data], [x['count'] for x in gender_data])
    plt.xlabel("Gender")
    plt.ylabel("Count")

    # Encode plot to display in template
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Pass the uploaded files along with the plot data to the template
    return render(request, 'dashboard.html', {
        'image_base64': image_base64,
        'uploaded_files': uploaded_files  # Pass the list of files for linking
    })


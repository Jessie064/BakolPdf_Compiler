# PDF Compiler

A sleek and efficient Django-based web application that allows users to upload, arrange, and merge multiple PDF files into a single document. 

## Features

- **Multi-File Upload**: Select or drag & drop multiple PDF files at once (up to 20 MB per file).
- **Interactive Arrangement**: Rearrange the order of your uploaded PDFs intuitively before compiling them.
- **Fast PDF Merging**: Combines your PDFs into a single, seamless document using the robust `pypdf` library.
- **Session-Based Storage**: Keeps track of user uploads securely using Django sessions, ensuring files from different users do not overlap.
- **File Management**: individually remove PDFs you no longer need, or clear all files from your session at once.

## Tech Stack

- **Backend Framework**: Django 5.x
- **PDF Manipulation**: `pypdf`
- **Database**: SQLite3 (Local and Production via Render Persistent Disk)
- **Static File Serving**: WhiteNoise
- **WSGI Server**: Gunicorn (for production)

## Local Development Setup

To run this application on your local machine:

1. **Clone the repository** (if you haven't already).
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On Mac/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
6. **Access the App**:
   Open a web browser and navigate to `http://127.0.0.1:8000/`.

## Deployment (PythonAnywhere)

This application is ready to be deployed on **PythonAnywhere** for 100% free hosting with persistent file storage. This ensures your SQLite database and uploaded PDFs are safely stored!

**To deploy to PythonAnywhere:**
1. Push this repository to GitHub.
2. Create a free account at [PythonAnywhere](https://www.pythonanywhere.com/).
3. Open a **Bash Console** in PythonAnywhere and clone your repository:
   ```bash
   git clone https://github.com/Jessie064/BakolPdf_Compiler.git
   ```
4. Navigate to the folder and create a virtual environment:
   ```bash
   cd BakolPdf_Compiler
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5. Go to the **Web** tab in PythonAnywhere and click **Add a new web app**.
6. Select **Manual configuration** and choose **Python 3.10**.
7. In the **Virtualenv** section, set the path to: `/home/yourusername/BakolPdf_Compiler/venv`
8. In the **Code** section, set the Source Code path to: `/home/yourusername/BakolPdf_Compiler`
9. Edit the **WSGI configuration file** to point to your Django project. Replace the file's contents with the Django template provided by PythonAnywhere and update the path string to point to `BakolPdf_Compiler`.
10. Click the big green **Reload** button! Your app is now live for free.

## Limits & Considerations

- Maximum file size per PDF is set to **20 MB** within `settings.py`.
- Ensure proper cleanup mechanisms are maintained to eventually delete aged PDF files and free up persistent storage, depending on app usage.

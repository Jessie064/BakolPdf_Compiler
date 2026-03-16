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

## Deployment (Render.com)

This application is fully configured to be deployed on **Render.com** using a **Blueprint**. Render provides a Persistent Disk natively, meaning the SQLite database and PDF files survive application restarts natively without requiring AWS S3.

**To deploy to Render:**
1. Push this repository to GitHub.
2. Log into the Render Dashboard and click **New > Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically read the `render.yaml` file to provision the necessary web service (using `gunicorn`), serve static files via WhiteNoise, and attach a 1GB persistent disk located at `/data` automatically.
5. Your Django app will run safely, keeping user PDFs and data intact.

## Limits & Considerations

- Maximum file size per PDF is set to **20 MB** within `settings.py`.
- Ensure proper cleanup mechanisms are maintained to eventually delete aged PDF files and free up persistent storage, depending on app usage.

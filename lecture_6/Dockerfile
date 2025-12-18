# Official Python image as the base
FROM python:3.13-slim
# Installation of  required Python dependencies
RUN pip install fastapi uvicorn
# The working directory in the container
WORKDIR /app
# Copy of the application source code is placed inside the container
COPY app.py /app
# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
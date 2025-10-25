# Use official lightweight Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies with compatible numpy version
# Pin numpy to a version compatible with tensorflow 2.17
RUN pip install "numpy>=1.23.5,<2.0.0" && \
    pip install -r requirements.txt

# Expose default port for Render
EXPOSE 10000

# Start the app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]

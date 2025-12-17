#previous deployment of gold_fetch

FROM selenium/standalone-chrome:4.20.0

# Switch to root to install Python packages
USER root

# Install Python 3.12 + pip + Streamlit
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create symlink for convenience
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create app directory
WORKDIR /app

# Copy requirements early for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Switch back to seluser (security + compatibility)
USER seluser

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
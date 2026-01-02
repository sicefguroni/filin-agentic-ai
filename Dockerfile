# 1. Use a slim version of Python (Industry standard for smaller images)
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (Docker Layer Caching optimization)
# If you change your code but not your requirements, Docker won't re-install everything.
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir keeps the image small by not saving the cache
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application
COPY . .

# 6. Default command (We will override this in docker-compose, but good to have)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
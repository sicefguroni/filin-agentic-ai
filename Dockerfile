# 1. Base Image
FROM python:3.10-slim

# 2. Set Working Directory
WORKDIR /app

# 3. INSTALL SYSTEM DEPENDENCIES
# We add --no-install-recommends to keep it small and stable
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. UPGRADE PIP (Crucial for modern wheels)
# Old pip versions try to compile from source. New pip downloads pre-built binaries.
RUN pip install --upgrade pip

# 5. INSTALL TORCH CPU VERSION SPECIFICALLY (The "Lite" Version)
# This forces downloading the Linux binary instead of compiling it.
# It saves ~1GB of download and massive CPU time.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 6. INSTALL OTHER HEAVY LIBRARIES INDIVIDUALLY
RUN pip install --no-cache-dir sentence-transformers
RUN pip install --no-cache-dir langchain-huggingface

# 7. INSTALL REMAINING APP DEPENDENCIES
COPY requirements.txt .
# We use --no-deps to avoid re-installing the heavy stuff
RUN pip install --no-cache-dir --no-deps -r requirements.txt

# 8. Copy Application Code
COPY . .

# 9. Start Command
CMD ["streamlit", "run", "src/app.py", "--server.address", "0.0.0.0"]
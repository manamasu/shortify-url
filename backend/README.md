# Backend for URL-Shortener

---

## Step 1: Open your Terminal (e.g Git Bash) and Create a venv folder by using following Command

on Unix/MacOS:  ```python3 -m venv .venv```

on Windows:     ```py -m venv .venv```

## Step 2: Activate your virtual environment

on Unix/MacOS:  ```source .venv/bin/activate```

on Windows:     ```cd .venv\Scripts\Activate.ps1```

## Step 3: Confirm that your virtual environment is activated with following Command

on Unix/MacOS:  ```which python```

on Windows:     ````where python```

## Step 4: Upgrade your pip Version

on Unix/MacOS:  ```python3 -m pip install --upgrade pip```

on Windows:     ```py -m pip install --upgrade pip```

## Step 5: Install all requirements by using the provided requirements.txt

on Unix/MacOS:  ```python3 -m pip install -r requirements.txt```

on Windows:     ```py -m pip install -r requirements.txt```

## Step 6: Once all requirements are installed, start up the local-server

Terminal Command: ```uvicorn app.api:app```

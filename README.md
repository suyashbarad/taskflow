# 📋 Task Manager

A simple Task Management System built with **Python Flask** and **MySQL**.

## Features

- ✅ Add tasks with a title and description
- 📋 View all tasks
- ✔️ Mark tasks as completed (toggle)
- 🗑️ Delete tasks
- 💾 Persistent MySQL storage

---

## Project Structure

```
CCD/
├── app.py                  # Flask application (routes + DB helpers)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # One-command local setup (app + MySQL)
├── .env.example            # Template for environment variables
├── .gitignore
├── static/
│   └── css/
│       └── style.css       # Application styles
├── templates/
│   ├── base.html           # Base layout template
│   └── index.html          # Main page (form + task list)
└── tests/
    ├── __init__.py
    └── test_app.py          # Automated tests (no DB required)
```

---

## Run Locally (without Docker)

### 1. Prerequisites

- Python 3.10+
- MySQL 8.0+ running locally

### 2. Create the database

```sql
CREATE DATABASE task_manager;
```

### 3. Set environment variables

```bash
# Linux / macOS
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=task_manager
export SECRET_KEY=any-random-string

# Windows PowerShell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="task_manager"
$env:SECRET_KEY="any-random-string"
```

### 4. Install dependencies and run

```bash
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** in your browser.

---

## Run with Docker Compose (recommended for local dev)

```bash
docker compose up --build
```

This starts **MySQL** and the **Flask app** together.  
Open **http://localhost:5000** once both containers are healthy.

Stop everything:

```bash
docker compose down            # keeps data
docker compose down -v         # removes data volume too
```

---

## Run Tests

Tests mock the database, so no MySQL is needed:

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## Deploy on AWS (EC2 + RDS)

### 1. Create an RDS MySQL instance

- Engine: MySQL 8.0
- Note the **endpoint**, **port**, **username**, and **password**

### 2. Launch an EC2 instance

- Amazon Linux 2023 or Ubuntu 22.04
- Security group: allow inbound **TCP 5000** (or 80 if using a reverse proxy)
- Ensure the EC2 security group can reach the RDS instance on port 3306

### 3. On the EC2 instance

```bash
# Install Docker
sudo yum install -y docker        # Amazon Linux
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# Build and run
git clone <your-repo-url> app
cd app
docker build -t task-manager .

docker run -d -p 5000:5000 \
  -e DB_HOST=<rds-endpoint> \
  -e DB_PORT=3306 \
  -e DB_USER=<rds-user> \
  -e DB_PASSWORD=<rds-password> \
  -e DB_NAME=task_manager \
  -e SECRET_KEY=$(openssl rand -hex 16) \
  task-manager
```

### 4. Initialize the database

On first run, connect to the RDS instance and create the database:

```sql
CREATE DATABASE IF NOT EXISTS task_manager;
```

The `tasks` table is created automatically when the app starts.

---

## Environment Variables Reference

| Variable      | Description                  | Default         |
|---------------|------------------------------|-----------------|
| `DB_HOST`     | MySQL hostname               | `localhost`     |
| `DB_PORT`     | MySQL port                   | `3306`          |
| `DB_USER`     | MySQL user                   | `root`          |
| `DB_PASSWORD` | MySQL password               | *(empty)*       |
| `DB_NAME`     | Database name                | `task_manager`  |
| `SECRET_KEY`  | Flask session secret key     | `dev-secret-key`|

---

## License

MIT

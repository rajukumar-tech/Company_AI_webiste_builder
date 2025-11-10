# Mastersolis Infotech Backend

An AI-powered backend for Mastersolis Infotech with PostgreSQL database integration.

## Features

- Page Management (Home, About, Services, Projects)
- Job Listings & Applications
- AI-Powered Portfolio Generator
- Resume Parsing & Scoring
- Blog Posts & Testimonials
- Analytics Dashboard
- Theme Customization
- SEO Analysis
- Voice Text Optimization

## Setup Instructions

### 1. Database Setup

#### Windows
1. Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. During installation, note down the password for postgres user
3. Open pgAdmin or psql and run:
```sql
CREATE ROLE mastersolis_user WITH LOGIN PASSWORD 'YourStrongPassword';
CREATE DATABASE mastersolis_db OWNER mastersolis_user;
GRANT ALL PRIVILEGES ON DATABASE mastersolis_db TO mastersolis_user;
```

#### macOS
```bash
# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Create database and user
psql postgres
CREATE ROLE mastersolis_user WITH LOGIN PASSWORD 'YourStrongPassword';
CREATE DATABASE mastersolis_db OWNER mastersolis_user;
GRANT ALL PRIVILEGES ON DATABASE mastersolis_db TO mastersolis_user;
```

#### Linux (Ubuntu/Debian)
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE ROLE mastersolis_user WITH LOGIN PASSWORD 'YourStrongPassword';
CREATE DATABASE mastersolis_db OWNER mastersolis_user;
GRANT ALL PRIVILEGES ON DATABASE mastersolis_db TO mastersolis_user;
```

### 2. Python Setup

1. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install flask flask-cors sqlalchemy psycopg2-binary python-dotenv openai
```

3. Configure environment:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

4. Edit `.env` and update:
- DATABASE_URL with your database credentials
- OPENAI_API_KEY (optional) for AI features

5. Initialize database:
```bash
python seed_db.py
```

6. Start the server:
```bash
python app.py
```

## API Endpoints

### Basic Routes
- `GET /` - Health check
- `GET /api/pages/<pagename>` - Get page content
- `POST /api/admin/pages/<pagename>` - Create/update page
- `GET/POST /api/jobs` - List/add jobs
- `POST /api/apply` - Apply for job

### AI Features
- `POST /api/portfolio/generate` - Generate portfolio from resume
- `GET /api/portfolio/<id>` - View portfolio
- `POST /api/chatbot` - Ask question
- `POST /api/ai/seo_analyze` - Analyze content for SEO
- `POST /api/ai/theme` - Get theme suggestions
- `POST /api/resume/parse` - Parse & score resume
- `POST /api/ai/auto_build` - Auto-build website
- `POST /api/voice/text` - Voice text optimization

### Admin
- `GET/POST /api/admin/ensure_seed` - Ensure sample data exists
- `GET /api/admin/applications` - List all applications

## Development

The project uses:
- Flask for the web framework
- SQLAlchemy for database ORM
- PostgreSQL for persistent storage
- OpenAI for AI features (optional)

## File Structure

- `app.py` - Main application and routes
- `db.py` - Database configuration
- `models.py` - SQLAlchemy models
- `seed_db.py` - Database initialization
- `data/uploads/` - File upload directory
# Database setup script
Write-Host "Setting up the database..." -ForegroundColor Green

$env:PGPASSWORD = "postgres123"
$psql = "C:\Program Files\PostgreSQL\15\bin\psql.exe"
$sql = @"
CREATE ROLE mastersolis_postgres WITH LOGIN PASSWORD 'YourPassword';
CREATE DATABASE mastersolis_db OWNER mastersolis_postgres;
GRANT ALL PRIVILEGES ON DATABASE mastersolis_db TO mastersolis_postgres;
"@

try {
    # Wait for PostgreSQL service to be ready
    Write-Host "Waiting for PostgreSQL service..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5

    # Create database and user
    Write-Host "Creating database and user..." -ForegroundColor Yellow
    $sql | & $psql -U postgres -h localhost

    # Update .env file
    Write-Host "Updating .env file..." -ForegroundColor Yellow
    $envContent = "DATABASE_URL=postgresql+psycopg2://mastersolis_postgres:YourPassword@localhost:5432/mastersolis_db"
    $envContent | Set-Content -Path ".env"

    Write-Host "`nDatabase setup completed!" -ForegroundColor Green
    Write-Host "You can now run: python seed_db.py" -ForegroundColor Yellow

} catch {
    Write-Host "Error setting up database: $_" -ForegroundColor Red
    exit 1
}
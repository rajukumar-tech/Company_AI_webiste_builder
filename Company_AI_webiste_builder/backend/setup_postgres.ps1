# PostgreSQL installation and setup script
Write-Host "Setting up PostgreSQL..." -ForegroundColor Green

# Download PostgreSQL installer
Write-Host "Downloading PostgreSQL installer..." -ForegroundColor Yellow
$downloadUrl = "https://get.enterprisedb.com/postgresql/postgresql-15.5-1-windows-x64.exe"
$installerPath = "$env:TEMP\postgresql_setup.exe"

try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
    Write-Host "PostgreSQL installer downloaded successfully!" -ForegroundColor Green

    # Run the installer
    Write-Host "Installing PostgreSQL..." -ForegroundColor Yellow
    Write-Host "Please follow these steps in the installer:" -ForegroundColor Yellow
    Write-Host "1. Use default installation directory" -ForegroundColor Yellow
    Write-Host "2. Set password for postgres user to: postgres123" -ForegroundColor Yellow
    Write-Host "3. Use default port 5432" -ForegroundColor Yellow
    Write-Host "4. Use default locale" -ForegroundColor Yellow
    
    Start-Process -FilePath $installerPath -ArgumentList "--mode unattended --unattendedmodeui minimal --superpassword postgres123" -Wait

    Write-Host "`nPostgreSQL installation completed!" -ForegroundColor Green
    Write-Host "Please wait a few moments for the service to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

} catch {
    Write-Host "Error downloading PostgreSQL: $_" -ForegroundColor Red
    exit 1
}
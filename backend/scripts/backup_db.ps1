$dbName = "dipalearning"
$dbUser = "postgres"
$timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$backupFile = "C:\dipalearning\backend\database\backups\backup_$dbName_$timestamp.sql"

# Require user to enter password unless PGPASSWORD env variable is set
pg_dump -U $dbUser -h localhost -p 5432 -F c -b -v -f $backupFile $dbName

if ($?) {
    Write-Host "Backup successfully created at $backupFile"
} else {
    Write-Host "Failed to create backup."
}
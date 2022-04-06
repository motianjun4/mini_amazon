cd "$(dirname "$0")"
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -W -f "./create.sql" -f "./load.sql"

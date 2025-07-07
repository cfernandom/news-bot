# PreventIA CLI Usage Examples

## Quick Start

```bash
# Check system status
./preventia-cli status

# Start API server
./preventia-cli serve --port 8000

# View documentation
./preventia-cli docs
```

## Scraper Management

```bash
# List all scrapers
./preventia-cli scraper list

# Run specific scraper
./preventia-cli scraper run 1

# Run all active scrapers
./preventia-cli scraper run-all

# Check scraper status
./preventia-cli scraper status

# Validate source compliance
./preventia-cli scraper validate 1
```

## Source Management

```bash
# List all sources
./preventia-cli source list

# Show source details
./preventia-cli source show 1

# Create new source
./preventia-cli source create "Medical News" "https://example.com" \
    --language en --country US \
    --legal-contact-email legal@example.com \
    --description "Medical news source"

# Update source
./preventia-cli source update 1 --status inactive

# Delete source
./preventia-cli source delete 1 --force

# Validate source compliance
./preventia-cli source validate 1
```

## User Management

```bash
# List all users
./preventia-cli user list

# Show user details
./preventia-cli user show admin

# Create new user
./preventia-cli user create john john@example.com "John Doe" \
    --role source_editor

# Update user
./preventia-cli user update john --full-name "John Smith"

# Reset password
./preventia-cli user reset-password john

# Assign role
./preventia-cli user assign-role john source_admin

# Revoke role
./preventia-cli user revoke-role john source_editor

# List available roles
./preventia-cli user list-roles
```

## Compliance Management

```bash
# Show compliance dashboard
./preventia-cli compliance dashboard

# List compliance violations
./preventia-cli compliance violations

# Validate all sources
./preventia-cli compliance validate-all

# View audit trail
./preventia-cli compliance audit --days 7

# Create legal notice
./preventia-cli compliance create-notice 1 fair_use "Fair Use Notice" \
    --content "This source is used under academic fair use"

# List legal notices
./preventia-cli compliance notices
```

## System Operations

```bash
# Create database backup
./preventia-cli backup --backup-file my_backup.json

# Start development server with auto-reload
./preventia-cli serve --reload

# Check detailed system status
./preventia-cli status --verbose
```

## Output Formats

Most commands support different output formats:

```bash
# Table format (default)
./preventia-cli source list

# JSON format
./preventia-cli source list --format json

# Verbose output
./preventia-cli source list --verbose

# Quiet output (errors only)
./preventia-cli source list --quiet
```

## Common Options

- `--verbose`, `-v`: Enable verbose output
- `--quiet`, `-q`: Suppress output except errors
- `--format`: Output format (table, json)
- `--help`: Show command help

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: JWT token secret key
- `API_HOST`: API server host
- `API_PORT`: API server port

## Examples with Environment Variables

```bash
# Set database URL
export DATABASE_URL="postgresql://user:pass@localhost:5433/db"

# Run with custom settings
JWT_SECRET_KEY="my-secret" ./preventia-cli serve --port 9000
```

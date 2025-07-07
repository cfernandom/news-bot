# PreventIA CLI Tools

Comprehensive command-line interface for PreventIA News Analytics system management and automation.

## Overview

The PreventIA CLI provides a complete automation suite for managing all aspects of the news analytics system, including:

- **System Management**: Status monitoring, health checks, and service management
- **Source Administration**: CRUD operations for news sources with compliance validation
- **Scraper Operations**: Automated scraping, validation, and performance monitoring
- **User Management**: User creation, role assignment, and permission management
- **Compliance Monitoring**: Legal compliance tracking and audit trail management
- **Database Operations**: Backup, migration, and maintenance operations

## Quick Start

### Installation

```bash
# Setup CLI tools
python setup_cli.py

# Verify installation
./preventia-cli --help
```

### Basic Usage

```bash
# Check system status
./preventia-cli status

# List news sources
./preventia-cli source list

# Run scraper for specific source
./preventia-cli scraper run 1

# Create backup
./preventia-cli backup --backup-file backup.json
```

## Command Structure

### System Commands

```bash
# System health and status
./preventia-cli status                    # System health check
./preventia-cli status --verbose          # Detailed system information
./preventia-cli version                   # Version information
./preventia-cli docs                      # Documentation links

# API server management
./preventia-cli serve                     # Start FastAPI server
./preventia-cli serve --port 8000         # Custom port
./preventia-cli serve --reload            # Development mode with auto-reload
```

### Source Management

```bash
# List and view sources
./preventia-cli source list                           # All sources
./preventia-cli source list --status active          # Filter by status
./preventia-cli source list --compliance compliant   # Filter by compliance
./preventia-cli source show 1                        # Detailed source info

# Create and manage sources
./preventia-cli source create "Medical News" "https://example.com" \
    --language en --country US \
    --legal-contact-email legal@example.com

# Update existing sources
./preventia-cli source update 1 --status inactive
./preventia-cli source update 1 --description "Updated description"

# Validate compliance
./preventia-cli source validate 1                    # Validate specific source
./preventia-cli source validate 1 --no-update       # Check only, don't update DB

# Delete sources
./preventia-cli source delete 1                      # Delete (with confirmation)
./preventia-cli source delete 1 --force             # Force delete with articles
```

### Scraper Operations

```bash
# List scrapers and status
./preventia-cli scraper list                         # All scrapers
./preventia-cli scraper list --status active         # Filter by status
./preventia-cli scraper status                       # Detailed scraper status
./preventia-cli scraper status 1                     # Specific scraper status

# Run scrapers
./preventia-cli scraper run 1                        # Run specific scraper
./preventia-cli scraper run 1 --force               # Force run (ignore status)
./preventia-cli scraper run-all                     # Run all active scrapers
./preventia-cli scraper run-all --max-concurrent 5   # Control concurrency

# Validate scrapers
./preventia-cli scraper validate 1                   # Validate specific scraper
```

### User Management

```bash
# List and view users
./preventia-cli user list                            # All users
./preventia-cli user list --active                   # Active users only
./preventia-cli user show admin                      # User details

# Create and manage users
./preventia-cli user create john john@example.com "John Doe" \
    --role source_editor

# Update users
./preventia-cli user update john --full-name "John Smith"
./preventia-cli user update john --active false      # Deactivate user

# Password management
./preventia-cli user reset-password john             # Reset password
./preventia-cli user change-password john            # Change password (interactive)

# Role management
./preventia-cli user assign-role john source_admin   # Assign role
./preventia-cli user revoke-role john source_editor  # Revoke role
./preventia-cli user list-roles                      # Available roles
```

### Compliance Monitoring

```bash
# Compliance dashboard
./preventia-cli compliance dashboard                 # Overview
./preventia-cli compliance dashboard --detailed      # Detailed view

# Compliance violations
./preventia-cli compliance violations                # All violations
./preventia-cli compliance violations --severity high # Filter by severity

# Validate compliance
./preventia-cli compliance validate-all              # All sources
./preventia-cli compliance validate-all --update     # Update database

# Audit trail
./preventia-cli compliance audit                     # Recent audit events
./preventia-cli compliance audit --days 30           # Last 30 days
./preventia-cli compliance audit --user admin        # Filter by user

# Legal notices
./preventia-cli compliance create-notice 1 fair_use "Fair Use Notice" \
    --content "This source is used under academic fair use"
./preventia-cli compliance notices                   # List all notices
```

### Database Operations

```bash
# Backup and restore
./preventia-cli backup                               # Create backup (timestamp)
./preventia-cli backup --backup-file my_backup.json # Custom filename

# Database status
./preventia-cli database status                      # Database health
./preventia-cli database migrate                     # Run migrations
./preventia-cli database validate                    # Validate schema
```

## Output Formats

All commands support multiple output formats:

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

## Configuration

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://preventia:preventia123@localhost:5433/preventia_news

# Optional
JWT_SECRET_KEY=your-secret-key
API_HOST=localhost
API_PORT=8000
```

### CLI Configuration

```bash
# Enable bash completion
source cli/completion/preventia-cli-completion.bash

# Add to your shell profile
echo 'source /path/to/preventia-cli-completion.bash' >> ~/.bashrc
```

## Advanced Usage

### Batch Operations

```bash
# Process multiple sources
for id in 1 2 3; do
    ./preventia-cli scraper run $id
done

# Bulk user creation
while IFS=, read -r username email name role; do
    ./preventia-cli user create "$username" "$email" "$name" --role "$role"
done < users.csv
```

### Monitoring and Automation

```bash
# Cron job for regular scraping
0 */6 * * * /path/to/preventia-cli scraper run-all

# Health check monitoring
*/5 * * * * /path/to/preventia-cli status --quiet || alert-system

# Daily compliance check
0 9 * * * /path/to/preventia-cli compliance validate-all --update
```

### Error Handling

```bash
# Check exit codes
./preventia-cli scraper run 1
if [ $? -eq 0 ]; then
    echo "Scraper succeeded"
else
    echo "Scraper failed"
fi

# Capture output
output=$(./preventia-cli source list --format json)
echo "$output" | jq '.[] | select(.status == "active")'
```

## Integration Examples

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Run System Health Check
  run: ./preventia-cli status --verbose

- name: Validate All Sources
  run: ./preventia-cli compliance validate-all

- name: Create System Backup
  run: ./preventia-cli backup --backup-file "backup-$(date +%Y%m%d).json"
```

### Monitoring Scripts

```bash
#!/bin/bash
# system-monitor.sh

# Check system health
if ! ./preventia-cli status --quiet; then
    echo "System health check failed"
    exit 1
fi

# Check compliance status
violations=$(./preventia-cli compliance violations --format json | jq '. | length')
if [ "$violations" -gt 0 ]; then
    echo "Compliance violations found: $violations"
    ./preventia-cli compliance violations
fi

# Check scraper performance
./preventia-cli scraper status --format json | \
    jq '.[] | select(.health != "healthy") | .name'
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database status
   ./preventia-cli status

   # Verify environment variables
   echo $DATABASE_URL
   ```

2. **Permission Denied**
   ```bash
   # Check CLI executable permissions
   chmod +x ./preventia-cli

   # Verify user has required database permissions
   ./preventia-cli user show $(whoami)
   ```

3. **Command Not Found**
   ```bash
   # Reinstall CLI tools
   python setup_cli.py

   # Check if CLI is in PATH
   which preventia-cli
   ```

### Debug Mode

```bash
# Enable verbose logging
./preventia-cli --verbose status

# Check CLI version and paths
./preventia-cli version --verbose

# Test database connectivity
./preventia-cli database status --verbose
```

## Development

### Adding New Commands

1. **Create command module** in `cli/` directory
2. **Implement BaseCLI pattern** with async methods
3. **Add Click decorators** for CLI interface
4. **Register in main CLI** (`cli/main.py`)
5. **Add tests** in `tests/integration/test_cli_integration.py`

### Testing CLI Commands

```bash
# Run CLI integration tests
python tests/run_integration_tests.py cli

# Test specific CLI functionality
pytest tests/integration/test_cli_integration.py -v

# Manual testing
./preventia-cli --help
```

---

**Status**: ✅ Production Ready
**Documentation**: Complete command reference
**Testing**: Comprehensive integration test coverage
**Integration**: Full system automation support

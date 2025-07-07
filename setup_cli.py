#!/usr/bin/env python3
"""
Setup script for PreventIA CLI
Creates executable command and installs dependencies
"""

import os
import stat
import subprocess
import sys
from pathlib import Path


def create_executable():
    """Create executable script for the CLI"""
    project_root = Path(__file__).parent
    cli_script = project_root / "preventia-cli"

    script_content = f"""#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ.setdefault('PYTHONPATH', str(project_root))

if __name__ == '__main__':
    from cli.main import cli
    cli()
"""

    # Write the script
    with open(cli_script, "w") as f:
        f.write(script_content)

    # Make it executable
    cli_script.chmod(cli_script.stat().st_mode | stat.S_IEXEC)

    print(f"✅ Created executable: {cli_script}")
    return cli_script


def install_cli_dependencies():
    """Install CLI-specific dependencies"""
    dependencies = [
        "click>=8.0.0",
        "rich>=10.0.0",  # For better terminal output
    ]

    print("📦 Installing CLI dependencies...")

    for dep in dependencies:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"  ✅ {dep}")
            else:
                print(f"  ❌ {dep}: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ❌ {dep}: {e}")


def create_shell_completion():
    """Create shell completion files"""
    project_root = Path(__file__).parent
    completion_dir = project_root / "cli" / "completion"
    completion_dir.mkdir(exist_ok=True)

    # Bash completion
    bash_completion = completion_dir / "preventia-cli-completion.bash"
    bash_content = """
# Bash completion for preventia-cli
_preventia_cli_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Main commands
    if [ $COMP_CWORD -eq 1 ]; then
        opts="scraper source user compliance status serve backup version docs"
        COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
        return 0
    fi

    # Subcommands
    case "${COMP_WORDS[1]}" in
        scraper)
            opts="list run run-all status validate"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        source)
            opts="list show create update delete validate"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        user)
            opts="list show create update reset-password assign-role revoke-role list-roles"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        compliance)
            opts="dashboard violations validate-all audit create-notice notices"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
    esac
}

complete -F _preventia_cli_completion preventia-cli
"""

    with open(bash_completion, "w") as f:
        f.write(bash_content)

    print(f"✅ Created bash completion: {bash_completion}")
    print("   To enable: source cli/completion/preventia-cli-completion.bash")


def create_usage_examples():
    """Create usage examples file"""
    project_root = Path(__file__).parent
    examples_file = project_root / "cli" / "EXAMPLES.md"

    examples_content = """# PreventIA CLI Usage Examples

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
./preventia-cli source create "Medical News" "https://example.com" \\
    --language en --country US \\
    --legal-contact-email legal@example.com \\
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
./preventia-cli user create john john@example.com "John Doe" \\
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
./preventia-cli compliance create-notice 1 fair_use "Fair Use Notice" \\
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
"""

    with open(examples_file, "w") as f:
        f.write(examples_content)

    print(f"✅ Created usage examples: {examples_file}")


def main():
    """Main setup function"""
    print("🔧 Setting up PreventIA CLI...")

    # Create executable
    cli_script = create_executable()

    # Install dependencies
    install_cli_dependencies()

    # Create completion files
    create_shell_completion()

    # Create examples
    create_usage_examples()

    print("\n✅ CLI setup completed!")
    print(f"\nTo use the CLI:")
    print(f"  {cli_script} --help")
    print(f"  {cli_script} status")
    print(f"  {cli_script} docs")

    print("\nTo enable bash completion:")
    print("  source cli/completion/preventia-cli-completion.bash")

    print("\nFor usage examples:")
    print("  cat cli/EXAMPLES.md")


if __name__ == "__main__":
    main()

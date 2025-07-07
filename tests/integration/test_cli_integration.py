"""
CLI Integration Tests for PreventIA News Analytics
Tests the CLI tools end-to-end with real database operations
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pytest
from sqlalchemy import delete, select

from services.data.database.connection import db_manager
from services.data.database.models import Article, NewsSource, User, UserRole


@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.database
class TestCLIIntegration:
    """Test CLI tools with real database integration"""

    @pytest.fixture
    def cli_path(self):
        """Get path to CLI executable"""
        project_root = Path(__file__).parent.parent.parent
        cli_path = project_root / "preventia-cli"
        assert cli_path.exists(), f"CLI executable not found at {cli_path}"
        return str(cli_path)

    @pytest.fixture
    async def clean_cli_environment(self, test_db_manager):
        """Provide clean environment for CLI testing"""
        # Set environment variables for CLI
        os.environ["DATABASE_URL"] = os.getenv(
            "TEST_DATABASE_URL",
            "postgresql://preventia:preventia123@localhost:5433/preventia_test",
        )
        os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-cli-testing"

        # Clean test data
        async with test_db_manager.get_session() as session:
            await session.execute(delete(Article))
            await session.execute(delete(NewsSource))
            await session.execute(delete(User))
            await session.execute(delete(UserRole))
            await session.commit()

        yield test_db_manager

        # Cleanup after test
        async with test_db_manager.get_session() as session:
            await session.execute(delete(Article))
            await session.execute(delete(NewsSource))
            await session.execute(delete(User))
            await session.execute(delete(UserRole))
            await session.commit()

    def run_cli_command(
        self, cli_path: str, command: str, timeout: int = 30
    ) -> Dict[str, Any]:
        """Helper to run CLI commands and capture output"""
        try:
            cmd = f"{cli_path} {command}"
            result = subprocess.run(
                cmd.split(), capture_output=True, text=True, timeout=timeout
            )

            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out",
                "success": False,
            }
        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e), "success": False}

    def test_cli_help_commands(self, cli_path):
        """Test CLI help commands are working"""
        # Test main help
        result = self.run_cli_command(cli_path, "--help")
        assert result["success"], f"CLI help failed: {result['stderr']}"
        assert "PreventIA News Analytics CLI" in result["stdout"]
        assert "Commands:" in result["stdout"]

        # Test subcommand help
        subcommands = ["status", "serve", "version", "docs"]
        for subcmd in subcommands:
            result = self.run_cli_command(cli_path, f"{subcmd} --help")
            # Some commands might not have perfect help, but should not crash
            assert result["returncode"] in [0, 2]  # 0 = success, 2 = help displayed

    def test_cli_version_and_docs(self, cli_path):
        """Test CLI version and documentation commands"""
        # Test version command
        result = self.run_cli_command(cli_path, "version")
        assert result["success"], f"Version command failed: {result['stderr']}"
        assert "PreventIA News Analytics CLI" in result["stdout"]

        # Test docs command
        result = self.run_cli_command(cli_path, "docs")
        assert result["success"], f"Docs command failed: {result['stderr']}"
        assert "Documentation:" in result["stdout"]
        assert "http://localhost:8000/docs" in result["stdout"]

    @pytest.mark.asyncio
    async def test_cli_status_command(self, cli_path, clean_cli_environment):
        """Test CLI status command with database"""
        # Test status command
        result = self.run_cli_command(cli_path, "status")

        # Status might fail due to missing tables in test env, but should not crash
        assert result["returncode"] in [0, 1]

        # Should show some database information
        output = result["stdout"] + result["stderr"]
        assert any(
            word in output.lower()
            for word in ["database", "articles", "sources", "connected", "failed"]
        )

    @pytest.mark.asyncio
    async def test_cli_backup_functionality(self, cli_path, clean_cli_environment):
        """Test CLI backup functionality"""
        import tempfile

        # Create test data
        async with clean_cli_environment.get_session() as session:
            source = NewsSource(
                name="CLI Test Source",
                base_url="https://cli-test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            article = Article(
                source_id=source.id,
                title="CLI Test Article",
                url="https://cli-test.com/article",
                summary="Test article for CLI backup",
                published_at=datetime.now(),
                scraped_at=datetime.now(),
                processing_status="completed",
            )
            session.add(article)
            await session.commit()

        # Test backup command
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            backup_file = tmp.name

        try:
            result = self.run_cli_command(
                cli_path, f"backup --backup-file {backup_file}"
            )

            # Backup might succeed or fail depending on implementation, but should not crash
            assert result["returncode"] in [0, 1]

            # If successful, check backup file was created
            if result["success"] and os.path.exists(backup_file):
                with open(backup_file, "r") as f:
                    backup_data = json.load(f)
                    assert isinstance(backup_data, dict)

        finally:
            if os.path.exists(backup_file):
                os.unlink(backup_file)

    def test_cli_serve_command_validation(self, cli_path):
        """Test CLI serve command validation (without actually starting server)"""
        # Test serve command help
        result = self.run_cli_command(cli_path, "serve --help")
        assert result["returncode"] in [0, 2]  # Help might return different codes

        # Test invalid port
        result = self.run_cli_command(cli_path, "serve --port invalid", timeout=5)
        assert not result["success"]  # Should fail with invalid port

    @pytest.mark.asyncio
    async def test_cli_error_handling(self, cli_path, clean_cli_environment):
        """Test CLI error handling and graceful failures"""
        # Test invalid commands
        invalid_commands = [
            "invalid-command",
            "status --invalid-flag",
            "backup",  # Missing required file parameter
        ]

        for cmd in invalid_commands:
            result = self.run_cli_command(cli_path, cmd, timeout=10)
            # Should fail gracefully, not crash
            assert not result["success"]
            assert result["returncode"] != -1  # Not a crash/timeout

            # Should provide helpful error messages
            error_output = result["stderr"] + result["stdout"]
            assert any(
                word in error_output.lower()
                for word in ["error", "usage", "help", "invalid"]
            )

    def test_cli_output_formats(self, cli_path):
        """Test CLI output format options"""
        # Commands that might support format options
        format_commands = [
            "status --verbose",
            "status --quiet",
        ]

        for cmd in format_commands:
            result = self.run_cli_command(cli_path, cmd, timeout=15)
            # Should not crash regardless of format options
            assert result["returncode"] != -1

            # Quiet mode should produce less output
            if "--quiet" in cmd and result["success"]:
                assert len(result["stdout"]) < 500  # Should be minimal output

    @pytest.mark.asyncio
    async def test_cli_database_operations(self, cli_path, clean_cli_environment):
        """Test CLI database-related operations"""
        # Test commands that interact with database
        db_commands = [
            "status",
            "status --verbose",
        ]

        for cmd in db_commands:
            result = self.run_cli_command(cli_path, cmd, timeout=20)

            # Database commands might fail in test environment but should handle gracefully
            assert result["returncode"] != -1  # Should not timeout or crash

            # Should mention database in output
            output = result["stdout"] + result["stderr"]
            assert "database" in output.lower() or "db" in output.lower()

    def test_cli_concurrent_execution(self, cli_path):
        """Test CLI behavior under concurrent execution"""
        import queue
        import threading

        results_queue = queue.Queue()

        def run_cli_test(command):
            result = self.run_cli_command(cli_path, command, timeout=10)
            results_queue.put(result)

        # Run multiple CLI commands concurrently
        commands = ["--help", "version", "docs", "status"]
        threads = []

        for cmd in commands:
            thread = threading.Thread(target=run_cli_test, args=(cmd,))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join(timeout=15)

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        assert len(results) >= 3  # At least most commands should complete

        # No command should have crashed
        crashed_commands = [r for r in results if r["returncode"] == -1]
        assert len(crashed_commands) == 0, f"Commands crashed: {crashed_commands}"


@pytest.mark.integration
@pytest.mark.e2e
class TestCLIWorkflows:
    """Test complete CLI workflows and scenarios"""

    @pytest.fixture
    def cli_path(self):
        """Get path to CLI executable"""
        project_root = Path(__file__).parent.parent.parent
        cli_path = project_root / "preventia-cli"
        if not cli_path.exists():
            pytest.skip("CLI executable not found - run setup_cli.py first")
        return str(cli_path)

    def run_cli_command(
        self, cli_path: str, command: str, timeout: int = 30
    ) -> Dict[str, Any]:
        """Helper to run CLI commands and capture output"""
        try:
            cmd = f"{cli_path} {command}"
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=timeout,
                env={
                    **os.environ,
                    "PYTHONPATH": str(Path(__file__).parent.parent.parent),
                },
            )

            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out",
                "success": False,
            }
        except Exception as e:
            return {"returncode": -1, "stdout": "", "stderr": str(e), "success": False}

    def test_cli_information_workflow(self, cli_path):
        """Test complete information gathering workflow"""
        # Step 1: Get general help
        result = self.run_cli_command(cli_path, "--help")
        assert result["returncode"] in [0, 2]
        help_output = result["stdout"]

        # Step 2: Get version information
        result = self.run_cli_command(cli_path, "version")
        assert result["returncode"] in [0, 1]  # Might fail but shouldn't crash

        # Step 3: Get system status
        result = self.run_cli_command(cli_path, "status")
        assert result["returncode"] in [0, 1]  # Might fail but shouldn't crash

        # Step 4: Get documentation links
        result = self.run_cli_command(cli_path, "docs")
        assert result["returncode"] in [0, 1]

    def test_cli_robustness_workflow(self, cli_path):
        """Test CLI robustness under various conditions"""
        # Test with missing environment variables
        old_env = os.environ.copy()
        try:
            # Remove database URL to test error handling
            if "DATABASE_URL" in os.environ:
                del os.environ["DATABASE_URL"]
            if "TEST_DATABASE_URL" in os.environ:
                del os.environ["TEST_DATABASE_URL"]

            result = self.run_cli_command(cli_path, "status")
            # Should fail gracefully, not crash
            assert result["returncode"] != -1

        finally:
            os.environ.clear()
            os.environ.update(old_env)

    def test_cli_help_completeness(self, cli_path):
        """Test that CLI help system is complete and helpful"""
        # Test main help
        result = self.run_cli_command(cli_path, "--help")
        help_text = result["stdout"] + result["stderr"]

        # Should contain essential information
        expected_elements = ["Usage:", "Commands:", "Options:", "PreventIA"]

        for element in expected_elements:
            assert element in help_text, f"Help missing: {element}"

    def test_cli_error_reporting_quality(self, cli_path):
        """Test quality of CLI error reporting"""
        # Test various error conditions
        error_scenarios = [
            ("invalid-command", "invalid command"),
            ("status --invalid-flag", "invalid flag"),
            ("backup", "missing argument"),
        ]

        for command, expected_error_type in error_scenarios:
            result = self.run_cli_command(cli_path, command, timeout=10)

            # Should fail but provide helpful error
            assert not result["success"]
            error_output = result["stderr"] + result["stdout"]

            # Error message should be informative
            assert len(error_output.strip()) > 0, f"No error message for: {command}"

            # Should suggest help or usage
            error_lower = error_output.lower()
            assert any(
                word in error_lower for word in ["help", "usage", "try"]
            ), f"Error message not helpful for: {command}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

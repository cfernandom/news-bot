"""
Password hashing and verification utilities
Implements secure password handling with bcrypt
"""

import secrets
import string
from typing import Optional

import bcrypt


class PasswordManager:
    """Secure password hashing and verification"""

    def __init__(self):
        self.rounds = 12  # bcrypt rounds for hashing

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt with salt

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        # Convert password to bytes
        password_bytes = password.encode("utf-8")

        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Return as string
        return hashed.decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash

        Args:
            password: Plain text password to verify
            hashed_password: Stored hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            # Convert to bytes
            password_bytes = password.encode("utf-8")
            hashed_bytes = hashed_password.encode("utf-8")

            # Verify using bcrypt
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            # Return False for any errors (malformed hash, etc.)
            return False

    def generate_secure_password(self, length: int = 16) -> str:
        """
        Generate a cryptographically secure random password

        Args:
            length: Length of password to generate (minimum 12)

        Returns:
            Secure random password string
        """
        if length < 12:
            length = 12

        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Ensure at least one character from each set
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special_chars),
        ]

        # Fill remaining length with random characters from all sets
        all_chars = lowercase + uppercase + digits + special_chars
        for _ in range(length - 4):
            password.append(secrets.choice(all_chars))

        # Shuffle the password list
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    def check_password_strength(self, password: str) -> dict:
        """
        Check password strength and return analysis

        Args:
            password: Password to analyze

        Returns:
            Dictionary with strength analysis
        """
        analysis = {
            "length_ok": len(password) >= 8,
            "has_lowercase": any(c.islower() for c in password),
            "has_uppercase": any(c.isupper() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "no_common_patterns": not self._has_common_patterns(password),
        }

        # Calculate strength score
        score = sum(analysis.values())

        if score >= 6:
            strength = "strong"
        elif score >= 4:
            strength = "medium"
        else:
            strength = "weak"

        analysis["score"] = score
        analysis["strength"] = strength
        analysis["max_score"] = 6

        return analysis

    def _has_common_patterns(self, password: str) -> bool:
        """Check for common weak password patterns"""
        password_lower = password.lower()

        # Common weak patterns
        weak_patterns = [
            "password",
            "123456",
            "qwerty",
            "abc123",
            "admin",
            "letmein",
            "welcome",
            "monkey",
            "111111",
            "password123",
        ]

        # Check for sequential patterns
        sequences = ["abcdef", "123456", "qwerty", "asdfgh"]

        # Check weak patterns
        for pattern in weak_patterns:
            if pattern in password_lower:
                return True

        # Check sequences
        for sequence in sequences:
            if sequence in password_lower:
                return True

        return False


# Global password manager instance
password_manager = PasswordManager()


# Convenience functions
def hash_password(password: str) -> str:
    """Hash password - convenience function"""
    return password_manager.hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password - convenience function"""
    return password_manager.verify_password(password, hashed_password)


def generate_secure_password(length: int = 16) -> str:
    """Generate secure password - convenience function"""
    return password_manager.generate_secure_password(length)


def check_password_strength(password: str) -> dict:
    """Check password strength - convenience function"""
    return password_manager.check_password_strength(password)

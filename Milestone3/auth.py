import hashlib
import os

def hash_password(password):
    """
    Hash a password using SHA-256 with salt
    In production, use bcrypt or argon2 for better security
    """
    # Generate a random 32-byte salt and convert to hex
    salt = os.urandom(32).hex()
    # Combine password with salt and hash it
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    # Return formatted as salt$hash_value
    return f"{salt}${hashed}"

def verify_password(password, hashed_password):
    """
    Verify a password against its hash
    """
    try:
        # Split the stored string into salt and the actual hash
        salt, hash_value = hashed_password.split('$')
        # Re-hash the provided password with the extracted salt
        check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        # Compare and return result
        return check_hash == hash_value
    except Exception:
        # Return False if the hash format is invalid or any error occurs
        return False

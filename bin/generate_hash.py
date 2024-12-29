from werkzeug.security import generate_password_hash

# Prompt for the password via command line
password = input("Enter the password to hash: ")

# Generate the hashed password
hashed_password = generate_password_hash(password)

# Output the hashed password
print("Hashed Password: ", hashed_password)
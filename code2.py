# SQL injection patterns

sql_injection_patterns = [
    # Test case 1: SELECT statement with SQL injection
    "SELECT * FROM users WHERE username='admin' OR '1'='1'",

    # Test case 2: INSERT statement with SQL injection
    "INSERT INTO users (username, password) VALUES ('admin', 'password'); DROP TABLE users;",

    # Test case 3: UNION-based SQL injection
    "SELECT * FROM users WHERE username='admin' UNION SELECT 1, 'password'",

    # Test case 4: DELETE statement with SQL injection
    "DELETE FROM users WHERE username='admin' OR 1=1 --",

    # Test case 5: SQL injection in comments
    "SELECT * FROM users; --'",

    # Add more SQL injection patterns as needed
]

# Print SQL injection patterns
for pattern in sql_injection_patterns:
    print(pattern)

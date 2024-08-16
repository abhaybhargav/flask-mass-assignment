# Vulnerable Flask Application

This application demonstrates mass assignment vulnerabilities in a Flask web application. It's designed for educational purposes to help developers understand and identify such vulnerabilities.

## Setup and Running the Application

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vulnerable_flask_app
   ```

2. Build the Docker image:
   ```
   docker build -t vulnerable-flask-app .
   ```

3. Run the Docker container:
   ```
   docker run -p 8880:8880 vulnerable-flask-app
   ```

The application will be accessible at `http://localhost:8880`.

## Interacting with the Application

### Web Interface

1. Visit `http://localhost:8880/signup` to create a new user account.
2. Login at `http://localhost:8880/login` with your credentials.
3. After logging in, you'll be redirected to the dashboard where you can see your role (user or admin).

### API Endpoints

The application provides two API endpoints for user signup:

1. Vulnerable API (susceptible to mass assignment):
   ```
   POST http://localhost:8880/api/signup
   ```

2. Secure API (protected against mass assignment):
   ```
   POST http://localhost:8880/api/secure_signup
   ```

## Demonstrating the Vulnerability

### Vulnerable API

You can create an admin user using the vulnerable API:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"admin@example.com", "password":"adminpass", "name":"Admin User", "is_admin":true}' http://localhost:8880/api/signup
```

This will create an admin user, exploiting the mass assignment vulnerability.

### Secure API

Attempting to create an admin user using the secure API:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"user@example.com", "password":"userpass", "name":"Regular User", "is_admin":true}' http://localhost:8880/api/secure_signup
```

This will create a regular user, ignoring the `is_admin` parameter.

## Understanding the Vulnerability

### Vulnerable Code

The vulnerable code is in the `app.py` file:

```python
@app.route('/api/signup', methods=['POST'])
def api_signup():
    user_data = request.json
    user = User(**user_data)  # Vulnerable to mass assignment
    db.session.add(user)
    db.session.commit()
    return {'message': 'Account created successfully!'}, 201
```

This code is vulnerable because it directly uses the `**user_data` syntax to create a new User object. This allows an attacker to set any User model attribute, including `is_admin`.

### Secure Code

The secure version of the signup API is also in `app.py`:

```python
@app.route('/api/secure_signup', methods=['POST'])
def api_secure_signup():
    data = request.json
    if not all(k in data for k in ('email', 'password', 'name')):
        return {'message': 'Missing required fields'}, 400
    
    user = User(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        is_admin=False  # Explicitly set to False
    )
    db.session.add(user)
    db.session.commit()
    return {'message': 'Account created successfully!'}, 201
```

This code is secure because it:
1. Explicitly checks for required fields.
2. Manually assigns each attribute, preventing mass assignment.
3. Explicitly sets `is_admin` to `False`, preventing unauthorized privilege escalation.

## Security Considerations

- Never use `**kwargs` or similar constructs to directly create model instances from user input in production applications.
- Always validate and sanitize user input.
- Explicitly set sensitive fields like `is_admin` to ensure they can't be manipulated by user input.
- Use a secure session management system and HTTPS in production environments.

## Disclaimer

This application is for educational purposes only. Do not use it in a production environment or expose it to the public internet, as it contains intentional security vulnerabilities.
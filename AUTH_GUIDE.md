# Task Management API - Authentication Guide

## API Endpoints

### 1. Signup (Create Account)
**POST** `/auth/signup`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "message": "User created successfully"
}
```

### 2. Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "email": "john@example.com",
  "expires_in": 1800
}
```

## How to Use Bearer Token Authentication

### In API Documentation (Swagger UI)
1. Go to `http://localhost:8000/docs`
2. Click the "Authorize" button (🔒)
3. In the HTTPBearer field, enter: `<your_access_token>`
4. Click "Authorize"
5. Now you can access protected endpoints

### In HTTP Requests
Add the Authorization header to your requests:

```bash
curl -X GET "http://localhost:8000/projects/" \
  -H "Authorization: Bearer <your_access_token>"
```

### In JavaScript/Fetch
```javascript
const token = "your_access_token_here";

fetch('http://localhost:8000/projects/', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

### In Python Requests
```python
import requests

token = "your_access_token_here"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get("http://localhost:8000/projects/", headers=headers)
```

## Protected Endpoints
All endpoints that require authentication will show a 🔒 lock icon in the Swagger documentation. These include:
- `/projects/*` - Project management
- `/tasks/*` - Task management

## Token Expiration
- Tokens expire after 30 minutes
- You'll receive a 401 Unauthorized error when the token expires
- Simply login again to get a new token

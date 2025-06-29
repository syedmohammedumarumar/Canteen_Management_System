# cms
# cms_project


# CMS Authentication System - Complete Guide

## Overview

This authentication system provides separate endpoints and functionality for:
- **Regular Users (Customers)**: Students/staff who use the canteen
- **Admin Users**: Canteen management staff with administrative privileges

## API Endpoints

### 🔐 Authentication Endpoints

#### Customer Registration
```
POST /api/users/register/
```
**Body:**
```json
{
    "username": "student123",
    "email": "student@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Admin Registration (Admin Only)
```
POST /api/users/admin/register/
```
**Headers:** `Authorization: Bearer <admin_access_token>`
**Body:**
```json
{
    "username": "admin123",
    "email": "admin@canteen.com",
    "password": "adminpassword123",
    "password_confirm": "adminpassword123",
    "first_name": "Jane",
    "last_name": "Smith"
}
```

#### Customer Login
```
POST /api/users/login/
```
**Body:**
```json
{
    "username": "student123",
    "password": "securepassword123"
}
```

#### Admin Login
```
POST /api/users/admin/login/
```
**Body:**
```json
{
    "username": "admin123",
    "password": "adminpassword123"
}
```

#### Logout (Both User Types)
```
POST /api/users/logout/
```
**Headers:** `Authorization: Bearer <access_token>`
**Body:**
```json
{
    "refresh": "<refresh_token>"
}
```

#### Token Refresh
```
POST /api/token/refresh/
```
**Body:**
```json
{
    "refresh": "<refresh_token>"
}
```

### 👤 Profile Management

#### Get Current User Profile Info
```
GET /api/users/profile/info/
```
**Headers:** `Authorization: Bearer <access_token>`

#### Customer Profile Management
```
GET/PUT/PATCH /api/users/profile/
```
**Headers:** `Authorization: Bearer <customer_access_token>`
**Body (for PUT/PATCH):**
```json
{
    "phone": "+91-9876543210",
    "roll_number": "CS2021001",
    "address": "Hostel Block A, Room 205",
    "gender": "M",
    "date_of_birth": "2000-05-15",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

#### Admin Profile Management
```
GET/PUT/PATCH /api/users/admin/profile/
```
**Headers:** `Authorization: Bearer <admin_access_token>`
**Body (for PUT/PATCH):**
```json
{
    "phone": "+91-9876543210",
    "employee_id": "EMP001",
    "department": "KITCHEN",
    "position": "Head Chef",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@canteen.com"
}
```

### 👥 User Management (Admin Only)

#### List All Users
```
GET /api/users/admin/users/
```
**Headers:** `Authorization: Bearer <admin_access_token>`

#### Get/Update/Delete Specific User
```
GET/PUT/PATCH/DELETE /api/users/admin/users/<user_id>/
```
**Headers:** `Authorization: Bearer <admin_access_token>`

### 🔧 Utility Endpoints

#### Check Username Availability
```
POST /api/users/check-username/
```
**Body:**
```json
{
    "username": "newuser123"
}
```

## Response Examples

### Successful Login Response
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "student123",
        "email": "student@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2025-06-28T10:30:00Z"
    },
    "user_type": "customer",
    "profile": {
        "id": 1,
        "phone": "+91-9876543210",
        "roll_number": "CS2021001",
        "address": "Hostel Block A",
        "gender": "M",
        "date_of_birth": "2000-05-15",
        "profile_image": null,
        "created_at": "2025-06-28T10:30:00Z",
        "updated_at": "2025-06-28T10:30:00Z"
    }
}
```

## Key Features

### 🔒 Security Features
1. **Separate Login Endpoints**: Different endpoints for admin and customer login
2. **Role-based Access Control**: Admins can't access customer endpoints and vice versa
3. **JWT Authentication**: Secure token-based authentication
4. **Password Validation**: Strong password requirements
5. **Token Blacklisting**: Secure logout with token invalidation

### 📱 Profile Management
1. **Auto Profile Creation**: Profiles are automatically created when users register
2. **Comprehensive Profile Fields**: 
   - Customer: roll_number, phone, address, gender, date_of_birth, profile_image
   - Admin: employee_id, department, position, phone, profile_image
3. **Profile Updates**: Users can update their own profiles
4. **Image Upload**: Profile picture support

### 🎯 User Management
1. **Admin User Management**: Admins can view, update, and delete customer users
2. **User Type Detection**: Automatic detection of user type based on staff status
3. **Username Availability Check**: Real-time username validation

## Database Migrations

After implementing this system, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Creating Initial Admin User

```bash
python manage.py createsuperuser
```

## Frontend Integration Examples

### Login Flow
```javascript
// Customer Login
const loginCustomer = async (username, password) => {
    const response = await fetch('/api/users/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });
    
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('user_type', data.user_type);
        return data;
    }
    throw new Error('Login failed');
};

// Admin Login
const loginAdmin = async (username, password) => {
    const response = await fetch('/api/users/admin/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });
    
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('user_type', data.user_type);
        return data;
    }
    throw new Error('Admin login failed');
};
```

### Protected API Calls
```javascript
const makeAuthenticatedRequest = async (url, options = {}) => {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });
    
    if (response.status === 401) {
        // Token expired, try to refresh
        await refreshToken();
        // Retry the request
        return makeAuthenticatedRequest(url, options);
    }
    
    return response;
};
```

## Error Handling

### Common Error Responses
```json
{
    "error": "Invalid credentials"
}

{
    "username": ["A user with that username already exists."]
}

{
    "password": ["This password is too short. It must contain at least 8 characters."]
}

{
    "non_field_errors": ["Passwords don't match"]
}
```

## Permissions Summary

| Endpoint | Customer | Admin | Superuser |
|----------|----------|-------|-----------|
| Customer Registration | ✅ | ✅ | ✅ |
| Admin Registration | ❌ | ✅ | ✅ |
| Customer Login | ✅ | ❌ | ❌ |
| Admin Login | ❌ | ✅ | ✅ |
| Customer Profile | ✅ (own) | ❌ | ✅ |
| Admin Profile | ❌ | ✅ (own) | ✅ |
| User Management | ❌ | ✅ | ✅ |
| Logout | ✅ | ✅ | ✅ |

This comprehensive authentication system provides secure, role-based access control for your canteen management system with separate workflows for customers and administrators.



menu testing guide

# Canteen Management System - Postman API Testing Guide

## Prerequisites
- Ensure your Django server is running: `python manage.py runserver`
- Default server URL: `http://127.0.0.1:8000` or `http://localhost:8000`
- Replace `your-app-name` with your actual Django app name in URLs

---

## 1. GET - List All Items

**Purpose**: Retrieve all menu items

### Request Details:
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/your-app-name/`
- **Headers**: None required
- **Body**: None


### Expected Response:
```json
[
    {
        "id": 1,
        "name": "Orange Juice",
        "description": "Fresh orange juice",
        "price": "25.00",
        "available": true,
        "category": "juices"
    },
    {
        "id": 2,
        "name": "Samosa",
        "description": "Crispy fried samosa",
        "price": "15.00",
        "available": true,
        "category": "snacks"
    }
]
```

---

## 2. POST - Add New Item

**Purpose**: Create a new menu item

### Request Details:
- **Method**: POST
- **URL**: `http://127.0.0.1:8000/your-app-name/add/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: Raw JSON


### Sample Request Body:
```json
{
    "name": "Mango Juice",
    "description": "Fresh mango juice with pulp",
    "price": 30.00,
    "available": true,
    "category": "juices"
}
```

### Test Cases:

#### Test Case 1: Valid Data
```json
{
    "name": "Cold Coffee",
    "description": "Iced coffee with milk",
    "price": 45.00,
    "available": true,
    "category": "beverages"
}
```

#### Test Case 2: Minimum Required Fields
```json
{
    "name": "Plain Water",
    "price": 10.00,
    "category": "beverages"
}
```

#### Test Case 3: Invalid Category (Should fail)
```json
{
    "name": "Pizza",
    "price": 150.00,
    "category": "invalid_category"
}
```

### Expected Success Response (201 Created):
```json
{
    "id": 3,
    "name": "Mango Juice",
    "description": "Fresh mango juice with pulp",
    "price": "30.00",
    "available": true,
    "category": "juices"
}
```

---

## 3. PUT - Update Existing Item

**Purpose**: Update an existing menu item completely

### Request Details:
- **Method**: PUT
- **URL**: `http://127.0.0.1:8000/your-app-name/{id}/update/`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: Raw JSON


### Sample Request Body:
```json
{
    "name": "Fresh Orange Juice",
    "description": "Freshly squeezed orange juice - Updated",
    "price": 35.00,
    "available": false,
    "category": "juices"
}
```

### Test Cases:

#### Test Case 1: Update All Fields
```json
{
    "name": "Premium Coffee",
    "description": "Premium blend coffee with cream",
    "price": 55.00,
    "available": true,
    "category": "beverages"
}
```

#### Test Case 2: Update Only Price and Availability
```json
{
    "name": "Samosa",
    "description": "Crispy fried samosa",
    "price": 18.00,
    "available": false,
    "category": "snacks"
}
```

### Expected Success Response (200 OK):
```json
{
    "id": 1,
    "name": "Fresh Orange Juice",
    "description": "Freshly squeezed orange juice - Updated",
    "price": "35.00",
    "available": false,
    "category": "juices"
}
```

---

## 4. DELETE - Remove Item

**Purpose**: Delete a menu item

### Request Details:
- **Method**: DELETE
- **URL**: `http://127.0.0.1:8000/your-app-name/{id}/delete/`
- **Headers**: None required
- **Body**: None

### Expected Success Response (204 No Content):
```json
{
    "message": "Item deleted successfully"
}
```

### Expected Error Response (404 Not Found):
```json
{
    "error": "Item not found"
}
```

---

## Common Test Scenarios

### 1. Testing Error Handling

#### Missing Required Fields (POST):
```json
{
    "description": "Just description, no name or price"
}
```

#### Invalid Item ID (PUT/DELETE):
- URL: `http://127.0.0.1:8000/your-app-name/999/update/`
- Should return 404 error

#### Invalid Price Format:
```json
{
    "name": "Test Item",
    "price": "invalid_price",
    "category": "snacks"
}
```

### 2. Testing Data Validation

#### Price with more than 2 decimal places:
```json
{
    "name": "Test Item",
    "price": 25.999,
    "category": "snacks"
}
```

#### Very long name (over 100 characters):
```json
{
    "name": "This is a very long name that exceeds the maximum length limit of 100 characters for testing purposes and should be rejected",
    "price": 25.00,
    "category": "snacks"
}
```


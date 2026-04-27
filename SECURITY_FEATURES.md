# 🔐 RBAC Security System Documentation

## Overview
This application now includes a complete Role-Based Access Control (RBAC) system with user management and secure delete operations.

---

## 🔐 Role-Based Access Control (RBAC)

### Available Roles
1. **Admin** - Full access including user management and record deletion
2. **User** - Read-only access + can edit records (requires admin credentials for deletion)

### Login Dialog
- Users must authenticate with username and password
- Login credentials are verified against bcrypt-hashed passwords in the database
- User role is stored after successful authentication
- Demo credentials: `admin` / `admin123`

---

## 🗑️ Delete System

### How It Works

#### For Admin Users
✅ Can directly delete records without additional verification
- Select one or multiple records using checkboxes
- Click "🗑️ Delete Record" button
- Confirm deletion in the dialog
- Records are immediately deleted

#### For Regular Users
🔒 Must provide admin credentials to delete records
1. Select one or multiple records
2. Click "🗑️ Delete Record" button
3. **Admin Verification Dialog appears:**
   - Enter admin username
   - Enter admin password
   - Click "✓ Verify"
4. If credentials are valid and user is admin:
   - Delete confirmation dialog appears
   - Confirm to proceed with deletion
5. If credentials are invalid:
   - Access denied message shown
   - Deletion cancelled

### Multi-Select Deletion
- Use checkboxes to select multiple records
- "✅ Select All" button selects all visible records
- "❌ Deselect All" button clears all selections
- Delete confirmation shows:
  - Number of records to be deleted
  - First 5 client names
  - Count of remaining records if more than 5

---

## 👥 User Management (Admin Only)

### Access
- Click "👥 Manage Users" button in main window
- ⚠️ Only accessible to admin users
- Regular users will see "Access Denied" message

### Features

#### 1️⃣ View Users
- See all existing users in a table
- Display columns:
  - Username
  - Role (Admin/User)
  - Action buttons

#### 2️⃣ Add New User
- Enter username in text field
- Enter password in password field
- Select role from dropdown (Admin or User)
- Click "Add User" button
- Username must be unique
- Password is automatically hashed using bcrypt

#### 3️⃣ Change User Role
- Click "Change" button next to user
- Confirmation dialog appears
- Shows current role and new role
- Click "Yes" to confirm role change
- Role changes immediately (admin ↔️ user)

#### 4️⃣ Delete User
- Click "Delete" button next to user
- Confirmation dialog appears
- Shows username being deleted
- Click "Yes" to confirm deletion
- User is permanently removed

---

## 🔒 Security Features

### Password Security
✅ **bcrypt Hashing**
- Passwords are never stored in plain text
- Uses bcrypt for secure password hashing
- Automatically hashed on user creation and login

### Admin Credential Verification
✅ **Multi-step Verification**
- Only actual admin users (role = 'admin') can authorize operations
- Credentials verified against database
- Password checked against bcrypt hash
- Role validation ensures user is admin

### Access Control
✅ **RBAC Implementation**
- Delete operations check user role
- Non-admins must provide valid admin credentials
- User management restricted to admins only
- Role badge shown in main window header

### Audit Trail
📋 **Database Records**
- Users table tracks all user accounts
- Records table tracks all data with IDs
- Can identify which user might have performed actions

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
```

### Records Table
```sql
CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NO TEXT,
    CLIENT TEXT,
    LOCATION TEXT,
    CURRENCY TEXT,
    PROGRESS TEXT,
    IMAGE_PATH TEXT,
    PROJECT TEXT,
    GEMPHIL_DEVICE TEXT,
    DETAILS TEXT,
    CONTACT_PERSON TEXT,
    EMAIL TEXT
)
```

---

## 🚀 Quick Start

### Initial Setup
1. Run `database.py` to initialize tables and create default admin user
2. Login with credentials: `admin` / `admin123`
3. Go to "👥 Manage Users" to add more users

### Typical Workflow (Admin)
1. Login as admin
2. Click "👥 Manage Users" to add users or change roles
3. Return to main window
4. Select records and delete directly (no verification needed)
5. Manage other admin tasks

### Typical Workflow (Regular User)
1. Login with assigned credentials
2. View and edit records normally
3. To delete records:
   - Select records
   - Click delete button
   - Enter admin credentials when prompted
   - Records deleted if verification succeeds

---

## ⚠️ Important Notes

### No Password Reset
- Admins must manually delete and recreate user if password is forgotten
- Keep admin credentials secure

### No Advanced Permissions
- System uses only two roles: admin and user
- All admins have full access
- Cannot create custom permission sets

### Database Backup
- Keep regular backups of `data/app_database.db`
- Contains all user accounts and records
- Deletion is permanent

---

## 🔧 Technical Details

### RBAC Implementation
```python
# Check if user is admin before allowing admin-only operations
if self.role.lower() != 'admin':
    # Show admin credential verification dialog
    admin_dialog = AdminCredentialDialog(self)
    if not admin_dialog.exec() or not admin_dialog.verified:
        QMessageBox.warning(self, "Access Denied", "...")
        return
```

### Admin Verification Process
```python
1. Get username and password from dialog
2. Query users table for matching username
3. Use bcrypt.checkpw() to verify password
4. Verify that user.role == 'admin'
5. Set verified flag if all checks pass
```

### Classes Involved
- **LoginWindow**: Handles initial authentication
- **MainWindow**: Main application window with RBAC checks
- **AdminCredentialDialog**: Verifies admin credentials for operations
- **ManageUsersDialog**: Admin-only user management interface

---

## ✅ Verification Checklist

When testing the system, verify:

- [ ] Login works with correct credentials
- [ ] Login fails with wrong credentials
- [ ] Admin can delete records directly
- [ ] User is prompted for admin credentials when deleting
- [ ] User cannot delete with wrong admin credentials
- [ ] Admin can access "Manage Users" button
- [ ] User cannot access "Manage Users" button
- [ ] Can add new users with different roles
- [ ] Can change user roles
- [ ] Can delete users
- [ ] Passwords are hashed (check database)

---

## 📞 Support

For issues or questions about the security system, contact your administrator.

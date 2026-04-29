# 📖 USER MANUAL
## Project Management System v1.0

---

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Login System](#login-system)
4. [User Interface Guide](#user-interface-guide)
5. [Features by Role](#features-by-role)
6. [Common Tasks](#common-tasks)
7. [Data Management](#data-management)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)
10. [FAQs](#faqs)

---

## Overview

The **Project Management System** is a secure, role-based application designed for managing client projects, locations, and business information. The system provides controlled access through user roles and ensures data integrity with built-in security features.

### Key Features
- ✅ Secure login with password protection
- ✅ Role-Based Access Control (Admin and User roles)
- ✅ Create, Read, Update, and Delete project records
- ✅ Export data to Excel files
- ✅ User account management (Admin only)
- ✅ Multi-select operations for batch processing
- ✅ Search and filter capabilities
- ✅ Professional green-themed interface

---

## Getting Started

### System Requirements
- Windows Operating System
- Python 3.7 or higher (if running from source)
- 50 MB free disk space
- Standard display resolution (1024×768 or higher recommended)

### Starting the Application
1. Navigate to the application folder
2. Double-click **main.exe** (or run `python main.py` if using source code)
3. The login window will appear
4. Proceed to the [Login System](#login-system) section

### First Time Setup
- The application automatically creates a default admin account
- **Default Admin Credentials:**
  - Username: `admin`
  - Password: `admin123`
- ⚠️ **Important:** Change the default password immediately after first login for security

---

## Login System

### Logging In

#### Step-by-Step Instructions
1. **Enter Username:** Type your username in the "Username" field
2. **Enter Password:** Type your password in the "Password" field
3. **Click "🔓 Login":** Or press **Enter** key to submit
4. **Success:** You'll be directed to the main application
5. **Failed:** An error message will appear if credentials are incorrect

### Password Requirements
- Passwords are **case-sensitive**
- Passwords must match exactly (spaces count)
- Passwords are securely hashed and never stored in plain text

### Forgotten Password
- Contact your administrator to reset your password
- Only administrators can reset user passwords

### Demo Credentials (For Testing)
```
Username: admin
Password: admin123
Role: Admin (Full Access)
```

---

## User Interface Guide

### Main Window Layout

#### Top Bar
- **Application Title:** Shows "Project Manager"
- **User Role Badge:** Displays your current role (ADMIN or USER)
- **Role Color:** Green badge indicates your access level

#### Left Panel - Filter Section
- **Search Field:** Search records by any field value
- **Filter Options:** Quick filters for:
  - Currency (USD, PHP, EUR, etc.)
  - Progress (0%, 25%, 50%, 75%, 100%)
  - Gemphil Device (Yes/No)
- **Apply Filters:** Filters update results in real-time

#### Center Panel - Data Table
- **Column Headers:** Shows all record fields
- **Records List:** Displays all project records
- **Checkboxes:** Select records for bulk operations
- **Resizable Columns:** Drag column borders to resize

#### Bottom Bar - Action Buttons
| Button | Purpose | Access |
|--------|---------|--------|
| ➕ Add Record | Create a new project record | All Users |
| ✏️ Edit Record | Modify selected record | All Users |
| 🗑️ Delete Record | Remove selected record(s) | All Users* |
| 📊 Analytics | View project statistics | All Users |
| 📥 Import Excel | Load records from Excel file | All Users |
| 📤 Export Excel | Save records to Excel file | All Users |
| 👥 Manage Users | Manage user accounts | Admins Only |

*Delete requires admin verification for regular users

---

## Features by Role

### 👨‍💼 ADMIN FEATURES

#### Full Permissions
- ✅ Create, edit, and delete any record
- ✅ Delete records without additional verification
- ✅ Import/Export data to Excel
- ✅ View analytics and reports
- ✅ Manage user accounts (add, edit, delete users)
- ✅ Access all system features

#### Admin-Exclusive Actions
1. **Manage Users** - Only admins can access the user management interface
2. **Direct Delete** - Delete records without entering credentials
3. **Role Management** - Assign user roles during user creation

---

### 👤 USER FEATURES

#### Standard Permissions
- ✅ View all project records
- ✅ Create new records
- ✅ Edit existing records
- ✅ Import/Export data to Excel
- ✅ Search and filter records
- ✅ View analytics

#### Restricted Permissions
- ❌ Delete records only with admin verification
- ❌ Cannot manage users
- ❌ Cannot access user management interface

#### User Delete Process
1. Select one or more records
2. Click "🗑️ Delete Record"
3. **Admin Verification Dialog appears**
   - Enter admin username
   - Enter admin password
   - Click "✓ Verify"
4. If credentials valid: Proceed with deletion
5. If credentials invalid: Operation cancelled

---

## Common Tasks

### ➕ Adding a New Record

#### Step-by-Step Instructions
1. Click **"➕ Add Record"** button at bottom
2. The **Add Record Dialog** will open with empty fields
3. Fill in the required information:
   - **No.** (Optional) - Record number/identifier
   - **Client** - Client or company name
   - **Location** - Project location/address
   - **Currency** - Select currency type (USD, PHP, EUR, etc.)
   - **Progress** - Select progress percentage
   - **Image** - Upload project image (optional)
   - **Project** - Project name/description
   - **Gemphil Device** - Specify if applicable
   - **Details** - Additional notes or details
   - **Contact Person** - Primary contact name
   - **Email** - Contact email address
4. Click **"💾 Save Record"** to save
5. Click **"✖️ Cancel"** to discard changes

#### Data Entry Tips
- Required fields must be completed
- Email should be in valid format (example@domain.com)
- Use descriptive names for easy searching
- Add relevant details in the Details field for future reference

---

### ✏️ Editing a Record

#### Step-by-Step Instructions
1. **Select the record** to edit by clicking on it in the table
2. Click **"✏️ Edit Record"** button
3. The **Edit Record Dialog** opens with current information
4. **Modify the fields** as needed
5. Click **"💾 Save Record"** to save changes
6. Click **"✖️ Cancel"** to discard changes

#### Important Notes
- Click the **"📁"** button next to Image field to change the image
- All changes are saved to the database
- Edit history is not maintained (use with caution)

---

### 🗑️ Deleting Records

#### For ADMIN Users
1. **Select record(s)** using checkboxes
2. Click **"🗑️ Delete Record"** button
3. **Confirmation dialog** appears showing:
   - Number of records to delete
   - Client names of records
4. Click **"✓ Yes, Delete"** to confirm
5. Click **"✖️ Cancel"** to abort

#### For REGULAR Users
1. **Select record(s)** using checkboxes
2. Click **"🗑️ Delete Record"** button
3. **Admin Verification Dialog** appears requesting:
   - Admin username
   - Admin password
4. **Enter admin credentials** and click **"✓ Verify"**
5. If verified → **Confirmation dialog** appears
6. Click **"✓ Yes, Delete"** to confirm
7. If not verified → **"Access Denied"** message appears

#### ⚠️ Important Warnings
- **Deletion is permanent** - Deleted records cannot be recovered
- **Multi-delete capability** - You can delete multiple records at once
- **Careful verification** - Admin passwords are case-sensitive

---

### 🔍 Searching Records

#### Using the Search Field
1. Click the **search field** at the top of the filter section
2. Type your search term (any field value)
3. Press **Enter** or wait for auto-search
4. Results filter automatically in real-time
5. Click **"✖️ Clear"** to reset search

#### Search Tips
- Search is **case-insensitive**
- Partial matches work (e.g., "john" finds "Johnson")
- Searches across all record fields
- Empty search shows all records

---

### 🔘 Using Filters

#### Available Filters
1. **Currency Filter** - Select specific currency type
   - Options: USD, PHP, EUR, GBP, JPY, etc.
   - Dropdown menu at bottom

2. **Progress Filter** - Show records at specific completion level
   - Options: 0%, 25%, 50%, 75%, 100%
   - Dropdown menu at bottom

3. **Gemphil Device Filter** - Show records by device status
   - Options: Yes, No, All
   - Dropdown menu at bottom

#### How to Apply Filters
1. Click the filter dropdown you want to use
2. Select your filter criteria
3. Results update automatically
4. Select **"All"** or blank to remove that filter

#### Multi-Filter Usage
- You can apply multiple filters simultaneously
- Filters work with search function
- All filters apply together (AND logic)

---

### 📊 Viewing Analytics

#### To Access Analytics
1. Click **"📊 Analytics"** button at bottom
2. Analytics window opens with visual reports

#### Available Analytics
- **Project Count by Currency** - Bar chart showing distribution
- **Progress Distribution** - Pie chart of project completion levels
- **Device Usage** - Chart of Gemphil device usage
- **Project Trends** - Timeline or trend analysis

#### Using Analytics
- Hover over charts for detailed information
- Charts update automatically with filtered data
- Use filters before opening analytics for specific data views

---

### 📤 Exporting to Excel

#### Basic Export (All Records)
1. Click **"📤 Export Excel"** button
2. **Export Options Dialog** appears
3. Select columns to include (checkboxes)
4. Click **"Confirm Export"** button
5. Choose save location on your computer
6. File saved as **"records_[date].xlsx"**

#### Export with Options
1. Open **Export Options Dialog** (same as above)
2. **Select columns** to include:
   - No., Client, Location, Currency
   - Progress, Image, Project, Gemphil Device
   - Details, Contact Person, Email
3. **Optional: Enable** "Sort alphabetically by Client"
4. Use **"✓ Select All"** to include all columns
5. Use **"✗ Deselect All"** to clear selections
6. Click **"Confirm Export"**

#### Quick Export Tips
- Select "Select All" to export everything
- Excel format is compatible with Microsoft Office
- Files can be opened in Excel, Google Sheets, or other spreadsheet apps
- Large exports may take a few seconds

---

### 📥 Importing from Excel

#### How to Import
1. Click **"📥 Import Excel"** button
2. **File selection dialog** opens
3. Navigate to your Excel file (.xlsx)
4. Select the file and click **"Open"**
5. Data is imported into the system
6. Success message confirms import completion

#### Excel File Format Requirements
- File must be in **.xlsx format** (Excel 2007+)
- Column headers must match system fields:
  - NO, CLIENT, LOCATION, CURRENCY, PROGRESS
  - IMAGE_PATH, PROJECT, GEMPHIL_DEVICE, DETAILS
  - CONTACT_PERSON, EMAIL

#### Import Troubleshooting
- Ensure file is in Excel format
- Check column names match expected format
- Verify data types are correct
- File must not be open in another program

---

### 👥 Managing Users (Admin Only)

#### Accessing User Management
1. Click **"👥 Manage Users"** button (Admin only)
2. **Manage Users Dialog** opens
3. View, add, edit, or delete users

#### Adding a New User
1. Click **"Manage Users"** button
2. In the dialog, enter:
   - **Username** - Unique identifier for the user
   - **Password** - Secure password for login
   - **Role** - Select "Admin" or "User"
3. Click **"Add User"** button
4. Success message confirms user creation
5. New user can now login

#### Editing User Information
1. In User Management dialog
2. Select the user from the list
3. Click **"Edit"** button (if available)
4. Modify username, password, or role
5. Click **"Save"** to confirm changes

#### Deleting a User
1. In User Management dialog
2. Select the user from the list
3. Click **"Delete"** button
4. Confirmation dialog appears
5. Click **"✓ Yes, Delete"** to confirm
6. User account is permanently removed

#### Important Notes
- **Username must be unique** - Cannot have duplicate usernames
- **Password security** - Passwords are case-sensitive and hashed
- **Role assignment** - Admin has full access; User has limited access
- **Can't self-delete** - Admins cannot delete their own account

---

## Data Management

### Data Storage
- All data is stored in a **SQLite database**
- Database is automatically created on first launch
- Located in the application folder as `database.db`

### Data Backup
- **Recommended:** Export data to Excel regularly
- Use the **"📤 Export Excel"** feature for backups
- Store exported files in a safe location

### Data Recovery
- If database is corrupted, export backup to Excel
- Delete corrupted database file
- Restart application (new database will be created)
- Import backup data using **"📥 Import Excel"**

---

## Security

### Password Security
✅ **What's Protected:**
- Passwords are encrypted using bcrypt hashing
- Passwords never stored in plain text
- Each password is individually salted
- Passwords required for all login attempts

⚠️ **Best Practices:**
- Never share your password with anyone
- Change your password regularly
- Use a strong password (mix of letters, numbers, symbols)
- Don't use the same password across different systems

### Role-Based Security
✅ **Admin Access:**
- Full system access
- Can delete records directly
- Can manage user accounts
- Can modify any record

✅ **User Access:**
- Limited to viewing and editing records
- Cannot access user management
- Cannot delete without admin verification
- Can import/export data

### Delete Verification
- Regular users must provide admin credentials to delete
- Admin passwords are verified against stored hashes
- Failed verification attempts logged
- Each delete operation is confirmed

---

## Troubleshooting

### Login Issues

#### Problem: "Invalid username or password" Error
**Solution:**
- Check that username is typed correctly
- Verify password is correct (case-sensitive)
- Confirm Caps Lock is OFF
- Reset password through administrator

#### Problem: Application Won't Start
**Solution:**
- Ensure all files are in the application folder
- Try running as Administrator
- Restart your computer
- Check Windows system logs

### Data Issues

#### Problem: Data Not Saving
**Solution:**
- Check database file permissions
- Ensure disk space is available
- Verify database.db file is not corrupted
- Try restarting the application

#### Problem: Can't Delete Records
**Solution:**
- If Admin: Try restarting application
- If User: Ensure admin credentials are correct
- Check that records are selected (with checkboxes)
- Verify you have permission to delete

#### Problem: Export to Excel Not Working
**Solution:**
- Ensure you have write permissions to save location
- Check that Excel is installed (or compatible app)
- Try saving to Desktop first
- Clear disk space and try again

### Performance Issues

#### Problem: Application Runs Slowly
**Solution:**
- Close other programs running in background
- Reduce filter criteria to fewer records
- Restart the application
- Restart your computer

#### Problem: Large File Import Fails
**Solution:**
- Split large Excel file into smaller files
- Import in multiple batches
- Check file format is correct (.xlsx)
- Verify file is not corrupted

---

## FAQs

### General Questions

**Q: What happens if I forget my password?**
A: Contact your administrator to reset your password. Only administrators can reset user passwords.

**Q: Can I have multiple users with the same name?**
A: No, usernames must be unique in the system. You cannot create two users with identical usernames.

**Q: Is there a limit to how many records I can store?**
A: The system can handle thousands of records, but performance may decrease with very large datasets (10,000+). Regular backups are recommended.

---

### Feature Questions

**Q: Can I undo a delete operation?**
A: No, deleted records cannot be recovered. Ensure you have backups before deleting important data.

**Q: What's the difference between Admin and User roles?**
A: Admins have full system access including user management and direct record deletion. Users can create and edit records but need admin credentials to delete them.

**Q: Can I search for multiple values at once?**
A: Currently, the search field supports single search terms. Use filters for multi-criteria searching.

**Q: How often should I export backups?**
A: Export backups weekly or after significant data entry. More frequent backups are recommended for critical projects.

---

### Technical Questions

**Q: What file formats are supported for import?**
A: Only Excel (.xlsx) format is currently supported. CSV files must be converted to Excel first.

**Q: Where is my data stored?**
A: All data is stored in a local SQLite database file (database.db) in the application folder.

**Q: Can I share the database between multiple computers?**
A: Not recommended. Use the export/import features to share data between systems.

**Q: Is my data encrypted?**
A: Passwords are encrypted using bcrypt. Database file itself is not encrypted; store the application folder securely.

---

### Security Questions

**Q: Is it safe to use the default admin password?**
A: No. The default password (admin123) should be changed immediately after first login. It's only for initial setup.

**Q: Can users see other users' passwords?**
A: No. Passwords are hashed and cannot be viewed by any user. Only administrators can manage user accounts.

**Q: What if someone gains access to the database file?**
A: The database file itself is not password-protected, but individual passwords are encrypted with bcrypt. Regular database backups are important.

---

## Contact & Support

For additional assistance:
- Contact your system administrator
- Refer to the QUICK_REFERENCE.md file for command shortcuts
- Check SECURITY_FEATURES.md for detailed security information

---

## Document Information

- **Version:** 1.0
- **Last Updated:** April 2026
- **Compatible With:** Project Management System v1.0
- **Format:** Markdown (.md)

---

**End of User Manual**

# 🔐 RBAC System - Quick Reference Guide

## Login
```
Username: admin
Password: admin123
```

---

## 👨‍💼 Admin Capabilities

### Delete Records
1. Select records with checkbox
2. Click "🗑️ Delete Record"
3. Confirm deletion
✅ No additional verification needed

### Manage Users
1. Click "👥 Manage Users" button
2. Add, edit, or delete users

### View Role
- Role badge shows "ADMIN" in top right

---

## 👤 User Capabilities

### Delete Records (Requires Verification)
1. Select records with checkbox
2. Click "🗑️ Delete Record"
3. Enter admin username & password
4. If verified, confirm deletion
⚠️ Must have valid admin credentials

### View Role
- Role badge shows "USER" in top right

### Restricted
- Cannot access "👥 Manage Users" button
- Cannot create new users

---

## 🗂️ Multi-Select Options

- **✅ Select All** - Select all visible rows
- **❌ Deselect All** - Clear all selections
- **🗑️ Delete Record** - Delete selected rows (admin-only or with verification)

---

## 🔒 If You Forget Password

1. Ask an admin to delete your account
2. Admin creates new account with new credentials
3. Login with new credentials

---

## 📋 User Management (Admin Only)

### Add User
- Username: [unique]
- Password: [any]
- Role: Admin or User

### Change Role
- Click "Change" next to user
- Confirm new role

### Delete User
- Click "Delete" next to user
- Confirm deletion

---

## 🆘 Troubleshooting

### "Access Denied" on Delete
→ You are not admin. Enter admin credentials when prompted.

### "Invalid credentials" on Admin Verification
→ Username or password is wrong. Ask admin if unsure.

### Cannot Access User Management
→ You must be admin. Contact your administrator.

### "User not found" when adding
→ Username already exists. Use a different username.

---

## ⚠️ Security Tips

✅ Keep your password private
✅ Never share admin credentials
✅ Log out when leaving your computer
✅ Contact admin if credentials are compromised

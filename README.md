# 🚀 One-Page Website Builder + Mini CMS

A production-ready one-page website system with a built-in admin panel designed for cPanel shared hosting.

## ✨ Features

- **Built-in Mini CMS**: Secure admin panel to manage everything.
- **Section Builder**: Add, edit, delete, reorder, and duplicate sections.
- **Prebuilt Templates**: Hero, About, Services, Pricing, Contact, and Custom HTML.
- **Global Settings**: Control colors, typography (Google Fonts), logo, and header styles.
- **Media Manager**: Simple image upload and path management.
- **Responsive Design**: Built with Bootstrap 5.
- **Lead Generation**: Integrated with Formspree and WhatsApp.
- **Backup & Restore**: Export and import your entire site data as JSON.
- **Optimized**: Lightweight, lazy loading, and cPanel-safe `.htaccess`.

## 🛠️ cPanel Installation Steps

1. **Upload Files**:
   - Upload all files to your `public_html` directory (or a subdomain folder).
   - Ensure `uploads/` directory is writable (usually 755).

2. **Create MySQL Database**:
   - Go to **MySQL Database Wizard** in cPanel.
   - Create a new database and a user with all privileges.
   - **Important**: Import the `database.sql` file using **phpMyAdmin**.

3. **Configure Database Connection**:
   - Open `includes/config.php` and update the following constants:
     ```php
     define('DB_HOST', 'localhost');
     define('DB_NAME', 'your_database_name');
     define('DB_USER', 'your_database_user');
     define('DB_PASS', 'your_database_password');
     ```

4. **Access Admin Panel**:
   - Navigate to `yourdomain.com/admin/login.php`.
   - **Default Credentials**:
     - Username: `admin`
     - Password: `admin123`
   - **Action**: Change your password immediately in the database or via a custom settings page if added.

## 🎨 Design Customization

- **Colors & Fonts**: Go to **Settings** in the admin panel to change the primary/secondary colors and choose a Google Font.
- **Sections**: Use the **Sections** menu to add content. Each section can have its own background color, image, and padding.
- **Custom CSS**: Add global CSS in **Settings** or section-specific CSS in the **Section Editor**.

## 📩 Form Configuration

1. Create a free account at [Formspree.io](https://formspree.io).
2. Create a new form and get your ID or just use your email.
3. Enter your Formspree email in **Admin > Settings**.

## 🔐 Security Notes

- This system uses PHP PDO with prepared statements to prevent SQL injection.
- CSRF protection is implemented on all admin forms.
- Passwords are saved using `password_hash()`.
- `.htaccess` prevents direct access to the database file and configuration.

## 📁 File Structure

- `/admin`: CMS interface files.
- `/assets`: CSS, JS, and image assets.
- `/includes`: Core logic, config, and section templates.
- `/uploads`: User-uploaded images.
- `index.php`: The public-facing website.
- `database.sql`: MySQL schema and demo content.

---
Built with ❤️ for speed and portability. No Node.js or complex build tools required.

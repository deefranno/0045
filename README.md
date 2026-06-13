# QuickInvoice Caribbean

Caribbean-first invoicing SaaS.

## Quick Start
cd server && npm install
cd ../client && npm install

## Run Development
Terminal 1: cd server && npm run dev
Terminal 2: cd client && npm run dev

## Demo Login
Email: demo@quickinvoice.ky
Password: demo1234

## Admin Panel
URL: /admin
Email: admin@quickinvoice.ky
Password: AdminSecure2025!

## Environment Variables
Copy .env.example to .env and fill in values.

## Deployment to Railway
1. Install the Railway CLI or connect your GitHub repository to Railway.
2. Ensure you add the required Environment Variables in the Railway dashboard (see `server/.env.example`).
3. Railway will automatically detect the `railway.toml` and use Nixpacks to build and deploy the app.
4. The build command will bundle the React frontend, and the server will serve it statically in production.

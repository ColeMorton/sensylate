# Security Deployment Setup Guide

## Environment Variables Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Contact Form Configuration
CONTACT_EMAIL=your-business-email@domain.com
CONTACT_NOTIFICATION_SUBJECT="New Contact Form Submission - Your Website"

# Optional: SMTP Configuration (if needed for alerts)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Database Configuration (if using)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sensylate_db
DB_USER=your_username
DB_PASSWORD=your_password

# API Configuration (if needed)
API_BASE_URL=https://api.example.com
API_TOKEN=your_api_token_here
```

### Netlify Deployment Setup

1. **Environment Variables in Netlify Dashboard:**
   - Go to Site Settings > Environment Variables
   - Add the following variables:
     - `CONTACT_EMAIL`: Your business email address
     - `CONTACT_NOTIFICATION_SUBJECT`: Subject line for contact notifications

2. **Build Settings:**
   - Ensure build command is: `yarn build`
   - Publish directory: `dist`

### Local Development Setup

1. **Copy Environment Template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your values:**
   ```bash
   # Update with your actual email
   CONTACT_EMAIL=your.email@domain.com
   CONTACT_NOTIFICATION_SUBJECT="New Contact Form Submission"
   ```

3. **Verify Security:**
   ```bash
   ./scripts/security-check.sh
   ```

## Security Validation

### Automated Security Check

Run the security validation script before any deployment:

```bash
chmod +x scripts/security-check.sh
./scripts/security-check.sh
```

This script checks for:
- Exposed email addresses
- API keys or secrets in code
- Hardcoded credentials
- Proper environment file setup

### Manual Security Checklist

- [ ] No sensitive data in repository files
- [ ] `.env` file exists locally (but not committed)
- [ ] Environment variables configured in deployment platform
- [ ] Security validation script passes
- [ ] No personal information in public content

## Deployment Process

### 1. Pre-Deployment Validation
```bash
# Run security check
./scripts/security-check.sh

# Build and test locally
cd frontend
yarn build
yarn preview
```

### 2. Environment Setup
- Ensure all required environment variables are set in deployment platform
- Test contact form functionality with environment variables

### 3. Deployment
- Push to main branch (triggers automatic deployment)
- Monitor deployment logs for any environment variable errors
- Test contact form functionality on live site

## Troubleshooting

### Contact Form Not Working
1. Check environment variables are set in Netlify
2. Verify `CONTACT_EMAIL` variable is correct
3. Check Netlify form notifications are enabled

### Security Check Failing
1. Review security-check.sh output
2. Remove any exposed sensitive data
3. Update exclusion patterns in security script if needed

### Environment Variables Not Loading
1. Verify variable names match exactly
2. Check for typos in .env file
3. Restart development server after .env changes

## Maintenance

### Regular Security Audits
- Run `./scripts/security-check.sh` monthly
- Review and update environment variables as needed
- Monitor for any new sensitive data exposure

### Environment Variable Updates
1. Update in deployment platform first
2. Update local .env file
3. Test functionality
4. Update .env.example if new variables added

---

**Security Contact**: If you discover any security issues, report them immediately to the development team.

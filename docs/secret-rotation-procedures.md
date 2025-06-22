# Secret Rotation Procedures

This document outlines the procedures for securely rotating secrets and managing environment variables in the Sensylate platform.

## Overview

The Sensylate platform uses environment-based configuration with a fail-fast validation system to ensure secure secret management. This document provides step-by-step procedures for rotating secrets without service interruption.

## Environment Structure

### Environment Files
- `.env.development` - Development environment configuration
- `.env.staging` - Staging environment configuration
- `.env.production` - Production environment configuration
- `.env.local` - Local overrides (never committed to git)

### Security Principles
- **Fail-Fast**: Invalid or missing secrets cause immediate application failure
- **Validation**: All environment variables are validated at startup
- **Separation**: Public variables prefixed with `PUBLIC_`, private variables never exposed to client
- **Build-time Sanitization**: Automated scanning prevents secret leakage in builds

## Secret Categories

### 1. API Keys and Tokens
**Examples**: Third-party service API keys, authentication tokens
**Rotation Frequency**: Every 90 days or immediately if compromised
**Impact**: Service-specific functionality

### 2. Database Credentials
**Examples**: Database URLs, passwords, connection strings
**Rotation Frequency**: Every 180 days or immediately if compromised
**Impact**: Full application functionality

### 3. Encryption Keys
**Examples**: JWT secrets, session encryption keys
**Rotation Frequency**: Every 365 days or immediately if compromised
**Impact**: User sessions, authentication

### 4. External Service Credentials
**Examples**: Yahoo Finance API, social media APIs, analytics services
**Rotation Frequency**: Every 90 days or immediately if compromised
**Impact**: Data collection, analytics

## Rotation Procedures

### Pre-Rotation Checklist
1. [ ] Identify all systems using the secret
2. [ ] Verify backup and rollback procedures
3. [ ] Schedule rotation during low-traffic period
4. [ ] Notify relevant team members
5. [ ] Prepare new secret value

### Standard Rotation Process

#### Step 1: Generate New Secret
```bash
# For API keys - contact service provider
# For generated secrets - use secure generation
openssl rand -base64 32  # For 32-byte secrets
```

#### Step 2: Update Staging Environment
```bash
# Update staging environment file
cd frontend
cp .env.staging .env.staging.backup
vim .env.staging  # Update the secret value

# Validate configuration
node scripts/sanitize-build.js

# Test staging deployment
yarn build
yarn preview
```

#### Step 3: Validate Staging
1. Deploy to staging environment
2. Run functional tests
3. Verify all services operational
4. Monitor for 24 hours minimum

#### Step 4: Update Production Environment
```bash
# Update production environment file
cp .env.production .env.production.backup
vim .env.production  # Update the secret value

# Final validation
node scripts/sanitize-build.js
yarn build
```

#### Step 5: Deploy to Production
1. Deploy during maintenance window
2. Monitor application startup
3. Verify all services operational
4. Monitor for 48 hours
5. Clean up backup files after successful validation

### Emergency Rotation (Compromised Secret)

#### Immediate Actions (0-15 minutes)
1. **Revoke compromised secret** at the source (API provider, service)
2. **Generate new secret** immediately
3. **Update all environments** simultaneously
4. **Deploy to production** immediately

#### Short-term Actions (15-60 minutes)
1. **Verify new secret functionality** across all environments
2. **Monitor logs** for authentication failures
3. **Update backup systems** with new secrets
4. **Document incident** in security log

#### Post-incident Actions (1-24 hours)
1. **Conduct security review** to identify how secret was compromised
2. **Update rotation schedule** if necessary
3. **Review access controls** and permissions
4. **Update monitoring** to detect similar incidents

## Environment-Specific Procedures

### Development Environment
- **Rotation Frequency**: As needed, low priority
- **Process**: Update `.env.development`, restart dev server
- **Validation**: Run `yarn dev` and verify functionality

### Staging Environment
- **Rotation Frequency**: Before each production rotation
- **Process**: Update `.env.staging`, deploy, validate
- **Validation**: Full functional test suite

### Production Environment
- **Rotation Frequency**: Per schedule or emergency
- **Process**: Coordinated deployment with monitoring
- **Validation**: Health checks, monitoring, gradual rollout

## Validation and Testing

### Automated Validation
```bash
# Run environment validation
node scripts/sanitize-build.js

# Run build with validation
yarn build

# Run tests with new configuration
yarn test
```

### Manual Validation Checklist
1. [ ] Application starts without errors
2. [ ] All API integrations functional
3. [ ] Authentication systems operational
4. [ ] Database connections successful
5. [ ] External services accessible
6. [ ] Monitoring and logging operational

## Monitoring and Alerting

### Key Metrics to Monitor
- **Authentication failure rates**
- **API response times and error rates**
- **Database connection health**
- **Application startup times**
- **Error log patterns**

### Alert Thresholds
- Authentication failures > 5% baseline
- API error rates > 2% baseline
- Database connection failures > 1%
- Application startup failures > 0%

## Recovery Procedures

### Rollback to Previous Secret
```bash
# Restore from backup
cp .env.production.backup .env.production

# Validate and deploy
node scripts/sanitize-build.js
yarn build
# Deploy to production
```

### Complete Environment Restoration
```bash
# Restore entire environment configuration
git checkout HEAD~1 -- .env.production

# Validate historical configuration
node scripts/sanitize-build.js
yarn build
```

## Security Best Practices

### Secret Storage
- **Never commit secrets to git**
- **Use deployment-specific secret management**
- **Encrypt secrets at rest**
- **Limit access to production secrets**

### Secret Generation
- **Use cryptographically secure random generation**
- **Minimum length requirements**: 32 characters for API keys, 64 for encryption keys
- **Avoid predictable patterns**
- **Document secret format requirements**

### Access Control
- **Principle of least privilege**
- **Separate development and production access**
- **Regular access audits**
- **Immediate revocation for departed team members**

## Tools and Resources

### Environment Validation
```bash
# Validate all environments
for env in development staging production; do
  NODE_ENV=$env node scripts/sanitize-build.js
done
```

### Secret Generation Tools
```bash
# Generate API key (32 bytes)
openssl rand -base64 32

# Generate encryption key (64 bytes)
openssl rand -base64 64

# Generate UUID
uuidgen
```

### Monitoring Commands
```bash
# Check application health
curl -f https://colemorton.com/health

# Validate API endpoints
curl -f https://api.colemorton.com/status

# Check authentication
curl -H "Authorization: Bearer $TOKEN" https://api.colemorton.com/protected
```

## Incident Response

### Security Incident Classification
- **P0**: Active breach or compromised production secret
- **P1**: Suspected compromise or failed rotation
- **P2**: Routine rotation failure
- **P3**: Development environment issues

### Incident Response Team
- **Incident Commander**: Technical lead
- **Security Officer**: Secret rotation specialist
- **Communications**: Stakeholder notification
- **Operations**: Deployment and monitoring

### Post-Incident Review
1. Timeline of events
2. Root cause analysis
3. Process improvements
4. Updated documentation
5. Training recommendations

## Compliance and Auditing

### Audit Trail Requirements
- **All secret rotations logged** with timestamp and operator
- **Failed rotation attempts recorded** with error details
- **Access to secrets tracked** and regularly reviewed
- **Retention period**: 2 years for compliance

### Regular Audits
- **Monthly**: Review access permissions
- **Quarterly**: Validate rotation schedules
- **Annually**: Complete security review
- **After incidents**: Immediate process review

---

**Document Version**: 1.0
**Last Updated**: June 22, 2025
**Next Review**: September 22, 2025

#!/bin/bash
# Security validation script to check for exposed sensitive data

echo "🔍 Running security validation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Check for email patterns (excluding safe files)
echo "📧 Checking for exposed email addresses..."
EMAIL_RESULTS=$(grep -r ".*@.*\.com" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist --exclude-dir=.netlify --exclude-dir=htmlcov --exclude="*.log" --exclude="security-check.sh" . | grep -v ".env.example" | grep -v "test" | grep -v "docs" | grep -v "README" | grep -v ".env$" | grep -v "team-workspace" | grep -v "placeholder" | grep -v "example" | grep -v "bibig@me.com")

if [ ! -z "$EMAIL_RESULTS" ]; then
    echo -e "${RED}❌ Found exposed email addresses:${NC}"
    echo "$EMAIL_RESULTS"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No exposed email addresses found${NC}"
fi

# Check for API key patterns (excluding safe files)
echo "🔑 Checking for exposed API keys/secrets..."
SECRET_RESULTS=$(grep -ri "api[_-]key\|apikey\|secret.*=\|token.*=\|password.*=" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist --exclude="*.log" --exclude="security-check.sh" . | grep -v ".env.example" | grep -v "test" | grep -v "docs" | grep -v "README" | grep -v ".env$" | grep -v "your_" | grep -v "example" | grep -v "team-workspace" | grep -v "placeholder" | grep -v "Password.*crackdown.*revenue")

if [ ! -z "$SECRET_RESULTS" ]; then
    echo -e "${RED}❌ Found potential exposed secrets:${NC}"
    echo "$SECRET_RESULTS"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No exposed secrets found${NC}"
fi

# Check for hardcoded credentials
echo "🛡️  Checking for hardcoded credentials..."
CRED_RESULTS=$(grep -ri "username.*=.*[a-zA-Z]\|password.*=.*[a-zA-Z]" --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist --exclude="*.log" --exclude="security-check.sh" . | grep -v ".env.example" | grep -v "test" | grep -v "docs" | grep -v "README" | grep -v ".env$" | grep -v "your_" | grep -v "example" | grep -v "placeholder" | grep -v "team-workspace" | grep -v "Password.*crackdown")

if [ ! -z "$CRED_RESULTS" ]; then
    echo -e "${YELLOW}⚠️  Found potential hardcoded credentials (review needed):${NC}"
    echo "$CRED_RESULTS"
else
    echo -e "${GREEN}✅ No hardcoded credentials found${NC}"
fi

# Check .env file exists
echo "📁 Checking environment file setup..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
elif [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example template exists${NC}"
else
    echo -e "${YELLOW}⚠️  .env.example template not found${NC}"
fi

# Final result
echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 Security validation PASSED - No critical issues found${NC}"
    exit 0
else
    echo -e "${RED}🚨 Security validation FAILED - $ERRORS critical issues found${NC}"
    echo "Please fix the issues above before proceeding."
    exit 1
fi

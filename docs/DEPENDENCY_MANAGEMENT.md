# Dependency Management Guide

This document provides comprehensive guidance for managing dependencies in the Sensylate multi-component system.

## Overview

Sensylate uses a sophisticated dependency management strategy to ensure:
- **Security**: Regular vulnerability scanning and updates
- **Stability**: Version bounds to prevent breaking changes
- **Compatibility**: Cross-component testing and validation
- **Automation**: Dependabot for automated security updates

## Dependency Structure

### Python Dependencies
- **requirements.txt**: Production dependencies with version bounds
- **requirements-dev.txt**: Development and testing dependencies
- **Upper bounds**: Prevent major version updates that could break compatibility
- **Security scanning**: Safety and Bandit for vulnerability detection

### Frontend Dependencies
- **package.json**: Node.js dependencies managed by Yarn
- **React 19.1.0**: Latest React version (monitor ecosystem compatibility)
- **Astro 5.7+**: Modern SSG framework with TypeScript support
- **Development tools**: ESLint, Prettier, Vitest for quality and testing

## Security Procedures

### Python Security Scanning

```bash
# Run safety check for known vulnerabilities
python3 -m safety scan

# Run bandit for security issues in code
python3 -m bandit -r scripts/ -f json

# Check for outdated packages
pip list --outdated
```

### Frontend Security Scanning

```bash
# Run yarn audit for vulnerabilities
yarn audit

# Check for high-severity issues only
yarn audit --level high

# Update vulnerable packages
yarn upgrade [package-name]
```

## Automated Updates

### Dependabot Configuration

Dependabot is configured in `.github/dependabot.yml` to automatically:
- **Weekly updates**: Security patches and minor versions
- **Ignore major versions**: For critical dependencies (React, pandas, etc.)
- **Create PRs**: With appropriate labels and reviewers
- **Separate schedules**: Python (Tuesday 10:00) and Frontend (Tuesday 11:00)

### Manual Update Process

1. **Review Dependabot PRs**: Check compatibility and test results
2. **Run compatibility tests**: Use `scripts/test_dependencies.py`
3. **Validate functionality**: Ensure E2E tests pass
4. **Monitor for issues**: Watch for regressions after deployment

## Compatibility Testing

### Automated Testing Framework

Use the dependency compatibility testing framework:

```bash
# Run comprehensive compatibility tests
python3 scripts/test_dependencies.py

# Check specific component
python3 scripts/test_dependencies.py --component frontend
python3 scripts/test_dependencies.py --component python
```

### Manual Compatibility Checks

```bash
# Python environment validation
python3 -c "import pandas, numpy, sklearn; print('Python deps OK')"

# Frontend build validation
cd frontend && yarn build

# Full test suite
make test && cd frontend && yarn test
```

## Version Management Strategy

### Python Dependencies

**Version Bounds Pattern**: `>=MIN_VERSION,<NEXT_MAJOR`

```txt
# Example: Allow patch and minor updates, block major
pandas>=2.0.0,<3.0.0          # Allow 2.x.x, block 3.x.x
numpy>=1.24.0,<2.0.0          # Allow 1.24+, block 2.x.x
scikit-learn>=1.3.0,<2.0.0    # Allow 1.3+, block 2.x.x
```

**Rationale**:
- Patch updates (1.2.3 → 1.2.4): Usually safe, automatic
- Minor updates (1.2.0 → 1.3.0): Generally compatible, automatic
- Major updates (1.x.x → 2.x.x): Breaking changes, manual review

### Frontend Dependencies

**Caret Ranges**: `^MAJOR.MINOR.PATCH`

```json
{
  "react": "^19.1.0",           // Allow 19.x.x, block 20.x.x
  "astro": "^5.7.8",            // Allow 5.x.x, block 6.x.x
  "typescript": "^5.8.3"        // Allow 5.x.x, block 6.x.x
}
```

## Critical Dependency Guidelines

### React 19.1.0 Considerations

React 19.1.0 is very recent (released 2024). Monitor for:
- **Ecosystem compatibility**: Some packages may not support React 19 yet
- **Breaking changes**: New concurrent features and changes to legacy APIs
- **Performance**: New compiler and runtime optimizations

**Mitigation**:
- Pin to 19.1.x range to avoid automatic major updates
- Test thoroughly with existing component library
- Monitor React ecosystem for compatibility updates

### Python Core Dependencies

**Critical packages requiring careful management**:
- **pandas**: Core data processing, major version changes affect APIs
- **numpy**: Foundational numerical computing, breaking changes rare but impactful
- **scikit-learn**: ML algorithms, API changes in major versions
- **sqlalchemy**: Database ORM, major versions have significant API changes

## Emergency Procedures

### Security Vulnerability Response

1. **Immediate Assessment**:
   ```bash
   # Check severity of vulnerabilities
   python3 -m safety scan --short-report
   yarn audit --summary
   ```

2. **Rapid Patching**:
   ```bash
   # Update specific vulnerable package
   pip install --upgrade package-name==safe-version
   yarn upgrade package-name@safe-version
   ```

3. **Validation**:
   ```bash
   # Run compatibility tests
   python3 scripts/test_dependencies.py

   # Run critical functionality tests
   yarn test:e2e
   ```

4. **Deployment**:
   - Create hotfix branch
   - Apply security updates
   - Run full test suite
   - Deploy with monitoring

### Dependency Conflicts

1. **Identify Conflicts**:
   ```bash
   # Python dependency conflicts
   pip check

   # Frontend dependency conflicts
   yarn install --check-files
   ```

2. **Resolution Strategy**:
   - Check for alternative compatible versions
   - Consider dependency alternatives
   - Use virtual environments for isolation
   - Document any workarounds or constraints

## Best Practices

### Development Workflow

1. **Before Adding Dependencies**:
   - Research package maturity and maintenance
   - Check security track record
   - Verify license compatibility
   - Consider bundle size impact (frontend)

2. **When Updating Dependencies**:
   - Read release notes and breaking changes
   - Update in development environment first
   - Run full test suite including E2E tests
   - Monitor application behavior after deployment

3. **Regular Maintenance**:
   - Weekly review of Dependabot PRs
   - Monthly security scan review
   - Quarterly major version planning
   - Annual dependency audit and cleanup

### Monitoring and Alerts

- **GitHub Security Advisories**: Automatic notifications for vulnerabilities
- **Dependabot Alerts**: Weekly digest of update opportunities
- **Test Failures**: CI/CD pipeline alerts for dependency-related issues
- **Performance Monitoring**: Watch for regressions after updates

## Tools and Resources

### Security Tools
- **Safety**: Python vulnerability scanner
- **Bandit**: Python security linter
- **Yarn Audit**: Node.js vulnerability scanner
- **GitHub Security Advisories**: Platform security alerts

### Compatibility Tools
- **pip-check**: Python dependency conflict checker
- **npm ls**: Node.js dependency tree analyzer
- **Dependabot**: Automated dependency updates
- **Custom Testing Framework**: `scripts/test_dependencies.py`

### Documentation
- [Python Packaging Guide](https://packaging.python.org/)
- [Yarn Dependency Management](https://yarnpkg.com/getting-started/migration)
- [GitHub Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)

## Troubleshooting

### Common Issues

**"No module named 'package'"**:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**"Module not found" in frontend**:
```bash
cd frontend
yarn install
yarn build
```

**Version conflicts**:
```bash
# Create clean environment
python3 -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

**Build failures after updates**:
```bash
# Clear caches and reinstall
rm -rf node_modules yarn.lock
yarn install
yarn build
```

### Getting Help

1. **Check existing issues**: Search GitHub issues for similar problems
2. **Review logs**: Check detailed error messages and stack traces
3. **Test isolation**: Try updates in isolated environment
4. **Community resources**: Stack Overflow, package documentation
5. **Professional support**: Consider commercial support for critical issues

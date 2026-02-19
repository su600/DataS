# Security Best Practices for DataS

## Critical Security Issues (Must Fix Before Production)

### 1. Password Storage
**Current Issue:** Passwords stored in plaintext in `blue_prints/LOGIN/login.py`

**Fix Required:**
```python
# Install bcrypt
pip install bcrypt

# Use bcrypt for password hashing
import bcrypt

# When creating a user
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# When verifying login
if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
    # Login successful
```

### 2. Database-Backed Authentication
**Current Issue:** Users stored in a list (lost on restart)

**Fix Required:**
- Use SQLAlchemy models for user storage
- Implement proper session management
- Add user roles and permissions

### 3. Token Security
**Current Issue:** InfluxDB tokens passed through forms and logged

**Fix Required:**
- Store tokens in environment variables only
- Never log or display tokens
- Use token rotation for long-running services

### 4. CSRF Protection
**Current Issue:** CSRF protection is commented out

**Fix Required:**
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

### 5. File Upload Security
**Current Issue:** Hardcoded D:/ paths, no file validation

**Fix Required:**
- Use the new `utils.save_uploaded_file()` function
- Validate file types before saving
- Limit file sizes
- Scan uploads for malware in production

## Environment Variables Security

### Required for Production

1. **SECRET_KEY**: Generate with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **INFLUXDB_TOKEN**: Never commit this to version control

3. **DEFAULT_USER/PASSWORD**: Change immediately and use database auth instead

### Environment File Management

**Development:**
- Use `.env` file (gitignored)
- Copy from `.env.example`

**Production:**
- Use system environment variables
- Use secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
- Never deploy `.env` files to production servers

## Input Validation

### PLC Connections
**Add validation for:**
- IP address format
- Port ranges
- Rack/slot numbers
- Tag name format

**Example:**
```python
import ipaddress

def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False
```

### Excel File Uploads
**Add validation for:**
- File extension (.xlsx, .xls only)
- File size limits
- Column headers
- Data types

## Network Security

### PLC Communications
1. Use VPN for remote PLC access
2. Implement firewall rules
3. Use encrypted protocols where available
4. Log all PLC connections and operations

### Web Application
1. Use HTTPS in production (nginx with SSL)
2. Set secure cookie flags:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   app.config['SESSION_COOKIE_HTTPONLY'] = True
   app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
   ```
3. Implement rate limiting for login attempts
4. Add request logging and monitoring

## Error Handling

### Never Expose Internals
**Bad:**
```python
except Exception as e:
    flash(str(e), "error")  # Exposes stack traces
```

**Good:**
```python
import logging

try:
    # ... code ...
except SpecificException as e:
    logging.error(f"Operation failed: {e}")
    flash("An error occurred. Please try again.", "error")
```

### Use Specific Exceptions
Replace all bare `except:` and `except Exception:` with specific exception types.

## Logging Best Practices

### Setup Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
```

### What to Log
- Authentication attempts (success and failure)
- PLC connections and disconnections
- Configuration changes
- Errors and exceptions
- InfluxDB write operations

### What NOT to Log
- Passwords or tokens
- Personal identifiable information (PII)
- Full stack traces in production
- Sensitive PLC data

## Deployment Checklist

Before deploying to production:

- [ ] All secrets moved to environment variables
- [ ] Strong SECRET_KEY generated and set
- [ ] Database authentication implemented with password hashing
- [ ] CSRF protection enabled
- [ ] HTTPS/SSL configured
- [ ] Secure session cookies enabled
- [ ] File upload validation implemented
- [ ] Input validation for all forms
- [ ] Rate limiting configured
- [ ] Logging configured (no sensitive data)
- [ ] Error messages sanitized
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Dependencies updated to latest secure versions
- [ ] Firewall rules configured
- [ ] Regular backup strategy in place
- [ ] Monitoring and alerting configured

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

# Troubleshooting Guide

This guide covers common installation and usage issues with the Quickstart Prompt Generator.

## Installation Issues

### Network Connection Errors

If you encounter connection errors during `pip install -e .`:

#### 1. Proxy Issues
```bash
# Check current pip configuration
pip config list

# If behind corporate proxy, configure pip
pip config set global.trusted-host pypi.org files.pythonhosted.org pypi.python.org
pip config set global.proxy http://your-proxy:port  # If needed
```

#### 2. Setuptools Backend Error (Python 3.13+)
**Error:** `Cannot import 'setuptools.build_meta'`

**Solution:**
```bash
# Install setuptools explicitly first
pip install setuptools wheel
pip install -e .
```

#### 3. Alternative Installation Methods

**Option A: Install without build isolation**
```bash
pip install --no-build-isolation -e .
```

**Option B: Upgrade pip and setuptools first**
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

**Option C: Use different index URL**
```bash
pip install --index-url https://pypi.org/simple/ -e .
```

**Option D: Manual dependency installation**
```bash
# Install dependencies manually first
pip install -r requirements.txt
pip install setuptools wheel
pip install -e .
```

### Command Not Found Issues

If `quickstart-prompt-generator` command isn't found after installation:

#### 1. Verify Virtual Environment
```bash
# Check if virtual environment is activated
which python  # Should show path to venv/bin/python

# Activate if not active
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Check Package Installation
```bash
# Verify package is installed
pip list | grep quickstart-prompt-generator
```

#### 3. Alternative Execution Methods
```bash
# Run directly with Python module
python -m src.cli --help

# Or specify full path (if needed)
python /path/to/quickstart_prompt_generator/src/cli.py --help
```

### Python Version Issues

#### Minimum Version Requirements
- Python 3.9 or higher required
- Check version: `python --version`

#### Version-Specific Issues
- **Python 3.13+**: May need explicit setuptools installation (see above)
- **Python 3.8**: Not supported, please upgrade

## Runtime Issues

### Common Error Messages

#### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

#### Permission errors on Windows
```bash
# Run command prompt as administrator, or use:
pip install --user -e .
```

#### SSL certificate errors
```bash
# Add trusted hosts
pip config set global.trusted-host pypi.org files.pythonhosted.org pypi.python.org
```

## Getting Help

If none of these solutions work:

1. **Check the GitHub Issues**: Look for similar problems and solutions
2. **Create a new issue** with:
   - Your operating system and version
   - Python version (`python --version`)
   - Complete error message
   - Steps you've already tried
3. **Include environment details**:
   ```bash
   pip list
   pip config list
   python --version
   which python
   ```

## Fallback: Running Without Installation

If installation continues to fail, you can run the tool directly:

```bash
# Navigate to project directory
cd quickstart_prompt_generator

# Activate virtual environment
source venv/bin/activate

# Install only dependencies
pip install -r requirements.txt

# Run directly
python -m src.cli --help
python -m src.cli init
```

This bypasses the need for editable installation while still providing full functionality.

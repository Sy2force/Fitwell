# Contributing to FitWell

Thank you for your interest in contributing to FitWell! We welcome contributions from the community to help make this project better.

## Getting Started

1. Fork the repository.
2. Clone your fork: `git clone https://github.com/your-username/fitwell.git`
3. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```
4. Create a new branch for your feature or bugfix: `git checkout -b feature/amazing-feature`

## Coding Standards

- **Python**: Follow PEP 8 style guide.
- **JavaScript**: Use ES6+ features where appropriate.
- **Commits**: Use clear, descriptive commit messages.

## Testing

Before submitting a Pull Request, please ensure all tests pass:

```bash
python3 backend/manage.py test api web
```

## Pull Request Process

1. Ensure your code compiles and runs locally.
2. Update the `README.md` if necessary.
3. Submit a Pull Request to the `main` branch.
4. Describe your changes in detail.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

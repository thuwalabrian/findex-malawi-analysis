# Contributing to Financial Inclusion in Malawi Analysis

Thank you for your interest in this project! This document provides guidelines for contributions, data handling, and community participation.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Data Handling & Licensing](#data-handling--licensing)
- [Development Setup](#development-setup)
- [Reporting Issues](#reporting-issues)
- [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive environment. We welcome contributions from people of all backgrounds and experience levels.

**We Do Not Tolerate:**
- Harassment or discrimination
- Violation of data privacy or licensing terms
- Unauthorized use of protected datasets
- Malicious code or security exploits

---

## 💡 How to Contribute

### Types of Contributions

1. **Bug Reports** — Found an error in analysis or code?
2. **Feature Requests** — Ideas for new visualizations or analyses?
3. **Documentation** — Improve README, data dictionary, or code comments
4. **Code Improvements** — Refactoring, performance optimization, additional tests
5. **Policy Analysis** — Evidence-based recommendations for financial inclusion

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes** and test thoroughly
5. **Commit with clear messages**: `git commit -m "Add: feature description"`
6. **Push to your branch**: `git push origin feature/your-feature-name`
7. **Submit a Pull Request** with detailed description

---

## 🔐 Data Handling & Licensing

### Critical: Microdata Protection

⚠️ **The World Bank Global Findex microdata is NOT included in this repository.**

Users must:
1. Download the **Malawi subset** from [World Bank Global Findex Database](https://www.worldbank.org/en/publication/globalfindex)
2. Place `Findex_Microdata_2025_updateMalawi.csv` in `data/raw/`
3. Only use the data in accordance with World Bank Terms of Use

### Data Files in Contributions

**DO NOT commit:**
- Raw microdata (`.csv`, `.xlsx` files in `data/raw/`)
- Processed datasets containing sensitive information
- Database files (`.db`, `.sqlite`)
- API keys, tokens, or credentials

**Safe to commit:**
- Aggregated summary tables (in `outputs/tables/`)
- Anonymized examples
- Codebooks and data dictionaries
- Analysis code and notebooks

### Licensing

- **Code**: MIT License (see LICENSE)
- **Data**: World Bank Global Findex — cite as:
  ```
  Demirgüç-Kunt, A., Klapper, L., Singer, D., & Ansar, S. (2024). 
  The Global Findex Database 2024: Financial Inclusion, Digital Payments, 
  and Resilience. World Bank, Washington, DC.
  ```

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+ (see requirements.txt)
- Git
- GitHub account

### Installation for Development

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/findex-malawi-analysis.git
cd findex-malawi-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Code quality tools
pip install black flake8 pylint
```

### Running the Dashboard (Development)

```bash
python launch_dashboard.py
# Opens at http://127.0.0.1:8050/
```

### Running Notebooks

```bash
jupyter notebook
# Open notebooks/ directory and run in order: 01 → 05
```

---

## 🐛 Reporting Issues

### Issue Templates

Use GitHub Issues and include:

**Bug Report:**
- Description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Python version, OS, relevant packages
- Screenshots if applicable

**Feature Request:**
- Description of the feature
- Use case / motivation
- Proposed implementation (optional)
- Related issues

### Security Issues

⚠️ **Do NOT open public issues for security vulnerabilities.**

Email security concerns to: **thuwalabrian@gmail.com**

---

## 📥 Pull Request Process

### Before You Submit

- ✅ Tests pass (if applicable)
- ✅ Code follows project style (see below)
- ✅ NO sensitive data committed
- ✅ Documentation updated
- ✅ Commit messages are clear

### Pull Request Checklist

```markdown
- [ ] My code follows the project's style guidelines
- [ ] I have updated the relevant documentation
- [ ] I have NOT committed sensitive data (microdata, credentials, etc.)
- [ ] My changes have been tested
- [ ] No new security vulnerabilities introduced
```

### Review Process

1. **Automated checks** (CI/CD) must pass
2. **Code review** by project maintainers
3. **Discussion** of any requested changes
4. **Approval** and merge when ready

### Code Style

- **Python**: Follow [PEP 8](https://pep8.org/)
- **Docstrings**: Google-style docstrings for functions
- **Notebooks**: Add markdown context; avoid bare code cells

Example:
```python
def calculate_inclusion_rate(dataset, weight_col='wgt'):
    """
    Calculate population-weighted financial inclusion rate.
    
    Parameters
    ----------
    dataset : pd.DataFrame
        Findex microdata with account columns
    weight_col : str
        Name of survey weight column
        
    Returns
    -------
    float
        Weighted inclusion rate (0-1)
    """
    return (dataset['account'].sum() * dataset[weight_col]).sum() / dataset[weight_col].sum()
```

---

## 📚 Additional Resources

- [Global Findex Database](https://www.worldbank.org/en/publication/globalfindex)
- [Data Dictionary](DATA_DICTIONARY.md)
- [Dashboard Setup](DASHBOARD_SETUP.md)
- [Project Summary](PROJECT_SUMMARY.md)

---

## ❓ Questions?

- Open a GitHub Discussion
- Email: thuwalabrian@gmail.com
- Check existing issues/PRs before asking

---

**Thank you for contributing to evidence-based financial inclusion policy!** 🚀

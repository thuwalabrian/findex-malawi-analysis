# 📊 Financial Inclusion Dashboard

Interactive web dashboard for the Financial Inclusion in Malawi analysis project.

## Features

### 🎯 Five Interactive Tabs

1. **Overview** - National indicators, gender gaps, and key statistics
2. **Demographics** - Income and education gradients with trend analysis
3. **Barriers** - Prevalence and impact of financial inclusion barriers
4. **Policy Recommendations** - Evidence-based interventions and priorities
5. **Statistical Models** - Logistic regression results and coefficients

### ✨ Dashboard Highlights

- **Interactive Visualizations** - Built with Plotly for dynamic, publication-quality charts
- **KPI Cards** - At-a-glance key metrics with visual indicators
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Professional Styling** - Modern UI with Bootstrap LUX theme
- **Real-time Data** - Loads directly from analysis outputs

## Quick Start

### Installation

```bash
# Install dashboard dependencies
pip install dash plotly dash-bootstrap-components
```

### Running the Dashboard

```bash
# From project root
cd dashboard
python app.py
```

The dashboard will be available at: **http://127.0.0.1:8050/**

## Project Structure

```
dashboard/
├── app.py              # Main dashboard application
├── utils.py            # Data loading utilities
├── assets/
│   └── style.css       # Custom CSS styling
└── README.md           # This file
```

## Technology Stack

- **Framework**: Dash by Plotly (Python web framework)
- **Visualization**: Plotly Express & Plotly Graph Objects
- **UI Components**: Dash Bootstrap Components (LUX theme)
- **Data Processing**: Pandas, NumPy
- **Icons**: Font Awesome

## Data Sources

All visualizations load from pre-computed analysis outputs in `outputs/tables/`:

- `national_indicators.csv` - Overall financial inclusion rates
- `gender_gap.csv` - Gender-disaggregated statistics
- `income_gradient.csv` - Financial inclusion by income quintile
- `education_gradient.csv` - Financial inclusion by education level
- `mm_barrier_prevalence.csv` - Barrier prevalence rates
- `policy_priority_matrix.csv` - Policy intervention priorities
- `regression_any_account.csv` - Logistic regression (any account)
- `regression_formal_account.csv` - Logistic regression (formal account)

## Customization

### Changing Colors

Edit the `COLORS` dictionary in `app.py`:

```python
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    # ... add more colors
}
```

### Adding New Tabs

1. Create a new function in `app.py`: `def create_newtab():`
2. Add to the `dbc.Tabs` component in the layout
3. Create visualization using Plotly

### Styling

Modify `assets/style.css` to customize the appearance.

## Deployment

### Local Network Access

```bash
python app.py --host 0.0.0.0 --port 8050
```

### Production Deployment (Heroku)

1. Create `Procfile`:
```
web: gunicorn app:server
```

2. Update `app.py`:
```python
server = app.server  # Add this line for gunicorn
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Performance

- Dashboard loads data once on startup
- All visualizations are pre-rendered
- Responsive caching for optimal performance
- Handles datasets up to 10,000 rows efficiently

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run_server(debug=True, port=8051)
```

### Missing Data Files
Ensure you've run all analysis notebooks (01-05) to generate output tables.

### Import Errors
```bash
pip install -r ../requirements.txt
```

## License

Same as parent project (see root LICENSE file)

## Author

Brian Thuwala  
Global Findex 2024 Analysis

---

**Last Updated**: February 2026

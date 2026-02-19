"""
Dashboard Preview Generator
Creates a simple HTML preview of what the dashboard looks like
"""

html_preview = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Inclusion Dashboard - Preview</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background-color: #2c3e50 !important; }
        .kpi-card { border-radius: 10px; padding: 1.5rem; }
        .kpi-value { font-size: 2rem; font-weight: 700; }
        .chart-placeholder { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 300px; 
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
        }
        .feature-box { 
            padding: 2rem; 
            background: white; 
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-dark mb-4">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-chart-line me-2"></i>
                Financial Inclusion in Malawi
            </span>
            <span class="text-white-50 small">Global Findex 2024 Analysis | n ≈ 1,000</span>
        </div>
    </nav>

    <div class="container-fluid px-4">
        <!-- Preview Notice -->
        <div class="alert alert-info" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            <strong>Dashboard Preview</strong> - This is a static preview. Launch the actual dashboard to see interactive features!
        </div>

        <!-- KPI Cards -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-auto">
                                <i class="fas fa-user-check fa-2x" style="color: #1f77b4;"></i>
                            </div>
                            <div class="col">
                                <div class="kpi-value" style="color: #1f77b4;">50.4%</div>
                                <p class="text-muted mb-0">Any Account</p>
                                <small class="text-muted">Any financial account</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-auto">
                                <i class="fas fa-mobile-alt fa-2x" style="color: #9467bd;"></i>
                            </div>
                            <div class="col">
                                <div class="kpi-value" style="color: #9467bd;">47.4%</div>
                                <p class="text-muted mb-0">Mobile Money</p>
                                <small class="text-muted">Dominant channel</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card kpi-card shadow-sm">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-auto">
                                <i class="fas fa-university fa-2x" style="color: #e377c2;"></i>
                            </div>
                            <div class="col">
                                <div class="kpi-value" style="color: #e377c2;">12.4%</div>
                                <p class="text-muted mb-0">Formal Bank</p>
                                <small class="text-muted">Traditional banking</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tabs -->
        <ul class="nav nav-tabs mb-4">
            <li class="nav-item">
                <a class="nav-link active" href="#">Overview</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Demographics</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Barriers</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Policy Recommendations</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#">Statistical Models</a>
            </li>
        </ul>

        <!-- Chart Placeholders -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <div class="chart-placeholder">
                            <div class="text-center">
                                <i class="fas fa-chart-bar fa-3x mb-2"></i>
                                <div>National Indicators Chart</div>
                                <small>Interactive Bar Chart</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <div class="chart-placeholder">
                            <div class="text-center">
                                <i class="fas fa-chart-line fa-3x mb-2"></i>
                                <div>Gender Gap Analysis</div>
                                <small>Interactive Grouped Bar Chart</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Features -->
        <div class="row">
            <div class="col-md-12">
                <div class="feature-box">
                    <h4><i class="fas fa-star text-warning me-2"></i>Dashboard Features</h4>
                    <div class="row mt-4">
                        <div class="col-md-4">
                            <h6><i class="fas fa-mouse-pointer text-primary me-2"></i>Interactive Charts</h6>
                            <p class="text-muted small">Zoom, pan, hover for details, export as PNG</p>
                        </div>
                        <div class="col-md-4">
                            <h6><i class="fas fa-mobile text-success me-2"></i>Responsive Design</h6>
                            <p class="text-muted small">Works perfectly on desktop, tablet, and mobile</p>
                        </div>
                        <div class="col-md-4">
                            <h6><i class="fas fa-tachometer-alt text-danger me-2"></i>Real-Time KPIs</h6>
                            <p class="text-muted small">Live key performance indicators with visual appeal</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-4">
                            <h6><i class="fas fa-paint-brush text-info me-2"></i>Professional Styling</h6>
                            <p class="text-muted small">Bootstrap LUX theme with custom enhancements</p>
                        </div>
                        <div class="col-md-4">
                            <h6><i class="fas fa-table text-warning me-2"></i>Data Tables</h6>
                            <p class="text-muted small">Sortable, filterable regression results tables</p>
                        </div>
                        <div class="col-md-4">
                            <h6><i class="fas fa-lightbulb text-purple me-2"></i>Policy Insights</h6>
                            <p class="text-muted small">Evidence-based recommendations with priorities</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Launch Instructions -->
        <div class="alert alert-success mt-4" role="alert">
            <h5 class="alert-heading"><i class="fas fa-rocket me-2"></i>Ready to Launch!</h5>
            <p>Run the following command to start the interactive dashboard:</p>
            <code>python launch_dashboard.py</code>
            <hr>
            <p class="mb-0">Then open your browser to: <strong>http://127.0.0.1:8050/</strong></p>
        </div>

        <!-- Footer -->
        <footer class="mt-5 mb-4">
            <hr>
            <div class="row">
                <div class="col-md-6">
                    <p class="text-muted small mb-1">
                        <i class="fas fa-database me-2"></i>
                        <strong>Data Source:</strong> World Bank Global Findex 2024
                    </p>
                    <p class="text-muted small mb-1">
                        <i class="fas fa-user me-2"></i>
                        <strong>Author:</strong> Brian Thuwala
                    </p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="text-muted small mb-1">
                        <i class="fas fa-users me-2"></i>
                        <strong>Sample:</strong> n ≈ 1,000 adults
                    </p>
                    <p class="text-muted small mb-1">
                        <i class="fas fa-calendar me-2"></i>
                        <strong>Updated:</strong> February 2026
                    </p>
                </div>
            </div>
        </footer>
    </div>
</body>
</html>
"""

# Save the preview
with open("../dashboard_preview.html", "w", encoding="utf-8") as f:
    f.write(html_preview)

print("✓ Dashboard preview created: dashboard_preview.html")
print("Open this file in your browser to see a static preview of the dashboard layout.")

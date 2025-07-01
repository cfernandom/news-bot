# PreventIA Medical Design System

**Fecha**: 2025-07-01
**Versión**: 1.0
**Autor**: Cristhian Fernando Moreno Manrique
**Estado**: ✅ Definido - Listo para implementación

---

## 🎨 **Design Tokens**

### **Color Palette médica**

#### **Primary Medical Identity**
```css
:root {
    /* Core Medical Brand */
    --primary-pink: #F8BBD9;        /* Breast cancer awareness pink */
    --primary-blue: #4A90E2;        /* Medical trust blue */
    --medical-gradient: linear-gradient(135deg, #F8BBD9 0%, #4A90E2 100%);

    /* Semantic Medical Colors */
    --positive-sentiment: #d1fae5;  /* Medical positive - hope/progress */
    --positive-text: #065f46;       /* Accessible positive text */
    --negative-sentiment: #fef2f2;  /* Medical alert - concern/caution */
    --negative-text: #991b1b;       /* Accessible alert text */
    --neutral-sentiment: #f3f4f6;   /* Medical neutral - information */
    --neutral-text: #374151;        /* Professional neutral text */

    /* Interface Foundation */
    --clean-white: #FFFFFF;         /* Medical cleanliness */
    --light-clinical: #F5F5F5;      /* Clinical background */
    --professional-gray: #666666;   /* Medical text authority */

    /* Academic Enhancement */
    --academic-navy: #1e3a8a;       /* Deep trust for headers */
    --research-teal: #0d9488;       /* Research/data accent */
    --citation-gray: #64748b;       /* Academic secondary text */

    /* Status & Alert Colors */
    --success-green: #10b981;       /* Medical success */
    --warning-yellow: #f59e0b;      /* Medical caution */
    --error-red: #ef4444;           /* Medical error */
    --info-blue: #3b82f6;           /* Medical information */
}
```

#### **Accessibility Enhanced Palette**
```css
/* High contrast medical mode */
@media (prefers-contrast: high) {
  :root {
    --primary-pink: #C1185C;        /* Enhanced contrast */
    --primary-blue: #1565C0;        /* Medical blue enhanced */
    --positive-sentiment: #A5F3A5;  /* High contrast positive */
    --negative-sentiment: #FFCDD2;  /* High contrast negative */
    --professional-gray: #333333;   /* Higher contrast text */
  }
}

/* Color-blind safe patterns */
.colorblind-safe {
    --positive-pattern: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'><path d='M0,4L4,0' stroke='%23065f46' stroke-width='1'/></svg>");
    --negative-pattern: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'><circle cx='2' cy='2' r='1' fill='%23991b1b'/></svg>");
    --neutral-pattern: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'><path d='M0,2L4,2' stroke='%23374151' stroke-width='1'/></svg>");
}
```

### **Typography System**

#### **Font Stacks**
```css
:root {
    /* Primary Medical Font */
    --font-primary: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;

    /* Data/Monospace Font */
    --font-mono: 'JetBrains Mono', 'SF Mono', 'Monaco', 'Cascadia Code', monospace;

    /* Medical Symbol Font */
    --font-medical: 'Font Awesome 6 Pro', 'Font Awesome 6 Free', sans-serif;
}
```

#### **Typography Scale**
```css
:root {
    /* Font Sizes - Medical Information Hierarchy */
    --text-xs: 0.75rem;      /* 12px - Small medical labels */
    --text-sm: 0.875rem;     /* 14px - Secondary medical text */
    --text-base: 1rem;       /* 16px - Body medical text */
    --text-lg: 1.125rem;     /* 18px - Emphasized medical text */
    --text-xl: 1.25rem;      /* 20px - Small medical headings */
    --text-2xl: 1.5rem;      /* 24px - Medical section headers */
    --text-3xl: 1.875rem;    /* 30px - Medical page titles */
    --text-4xl: 2.25rem;     /* 36px - Major medical metrics */
    --text-5xl: 3rem;        /* 48px - Dashboard medical title */

    /* Line Heights - Medical Readability */
    --leading-tight: 1.25;   /* Medical headings */
    --leading-normal: 1.5;   /* Medical body text */
    --leading-relaxed: 1.625; /* Medical long-form content */

    /* Font Weights - Medical Authority */
    --font-light: 300;       /* Medical subtle text */
    --font-normal: 400;      /* Medical body text */
    --font-medium: 500;      /* Medical emphasized text */
    --font-semibold: 600;    /* Medical subheadings */
    --font-bold: 700;        /* Medical headings */
    --font-extrabold: 800;   /* Medical metrics */
}
```

#### **Typography Classes**
```css
/* Medical Typography Components */
.medical-title {
    font-size: var(--text-5xl);
    font-weight: var(--font-bold);
    line-height: var(--leading-tight);
    color: var(--academic-navy);
    letter-spacing: -0.025em;
}

.clinical-subtitle {
    font-size: var(--text-2xl);
    font-weight: var(--font-semibold);
    line-height: var(--leading-tight);
    color: var(--professional-gray);
    margin-bottom: 1rem;
}

.data-label {
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--citation-gray);
}

.metric-value {
    font-size: var(--text-4xl);
    font-weight: var(--font-extrabold);
    line-height: var(--leading-tight);
    color: var(--primary-blue);
}

.medical-body {
    font-size: var(--text-base);
    font-weight: var(--font-normal);
    line-height: var(--leading-normal);
    color: var(--professional-gray);
}

.medical-caption {
    font-size: var(--text-sm);
    font-weight: var(--font-normal);
    line-height: var(--leading-normal);
    color: var(--citation-gray);
}
```

### **Spacing System**

#### **Spacing Scale**
```css
:root {
    /* Medical Interface Spacing */
    --space-px: 1px;         /* 1px - Fine medical borders */
    --space-0-5: 0.125rem;   /* 2px - Micro medical spacing */
    --space-1: 0.25rem;      /* 4px - Tight medical data */
    --space-2: 0.5rem;       /* 8px - Close medical elements */
    --space-3: 0.75rem;      /* 12px - Small medical groups */
    --space-4: 1rem;         /* 16px - Standard medical spacing */
    --space-5: 1.25rem;      /* 20px - Medium medical spacing */
    --space-6: 1.5rem;       /* 24px - Section medical separation */
    --space-8: 2rem;         /* 32px - Large medical sections */
    --space-10: 2.5rem;      /* 40px - Major medical spacing */
    --space-12: 3rem;        /* 48px - Page medical sections */
    --space-16: 4rem;        /* 64px - Extra large medical spacing */
    --space-20: 5rem;        /* 80px - Huge medical spacing */
}
```

#### **Component Spacing**
```css
/* Medical Component Internal Spacing */
.medical-card-padding {
    padding: var(--space-6) var(--space-6);
}

.medical-section-margin {
    margin-bottom: var(--space-8);
}

.medical-grid-gap {
    gap: var(--space-6);
}

.medical-button-padding {
    padding: var(--space-3) var(--space-6);
}

.medical-input-padding {
    padding: var(--space-3) var(--space-4);
}
```

### **Border & Radius System**

#### **Border Widths**
```css
:root {
    /* Medical Border Widths */
    --border-0: 0px;         /* No border */
    --border-1: 1px;         /* Subtle medical borders */
    --border-2: 2px;         /* Standard medical borders */
    --border-4: 4px;         /* Prominent medical borders */
    --border-8: 8px;         /* Heavy medical borders */
}
```

#### **Border Radius**
```css
:root {
    /* Medical Border Radius */
    --radius-none: 0px;      /* Sharp medical edges */
    --radius-sm: 0.125rem;   /* 2px - Subtle medical rounding */
    --radius-base: 0.25rem;  /* 4px - Standard medical rounding */
    --radius-md: 0.375rem;   /* 6px - Medium medical rounding */
    --radius-lg: 0.5rem;     /* 8px - Large medical rounding */
    --radius-xl: 0.75rem;    /* 12px - Extra large medical rounding */
    --radius-2xl: 1rem;      /* 16px - Very large medical rounding */
    --radius-full: 9999px;   /* Full medical circle */
}
```

### **Shadow System**

#### **Medical Shadows**
```css
:root {
    /* Medical Shadow System */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);

    /* Medical Focus Shadow */
    --shadow-focus: 0 0 0 3px rgba(72, 144, 226, 0.1);
}
```

---

## 🧩 **Component Specifications**

### **Buttons**

#### **Medical Button Variants**
```css
/* Primary Medical Button */
.btn-medical-primary {
    background: var(--primary-blue);
    color: var(--clean-white);
    border: var(--border-2) solid var(--primary-blue);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-6);
    font-size: var(--text-base);
    font-weight: var(--font-medium);
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
}

.btn-medical-primary:hover {
    background: #3a7bc8;
    border-color: #3a7bc8;
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.btn-medical-primary:focus {
    outline: none;
    box-shadow: var(--shadow-focus);
}

/* Secondary Medical Button */
.btn-medical-secondary {
    background: var(--clean-white);
    color: var(--primary-blue);
    border: var(--border-2) solid var(--primary-blue);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-6);
    font-size: var(--text-base);
    font-weight: var(--font-medium);
    transition: all 0.2s ease;
}

.btn-medical-secondary:hover {
    background: #f0f7ff;
    box-shadow: var(--shadow-sm);
}

/* Medical Alert Button */
.btn-medical-alert {
    background: var(--error-red);
    color: var(--clean-white);
    border: var(--border-2) solid var(--error-red);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-6);
    font-size: var(--text-base);
    font-weight: var(--font-medium);
}

/* Medical Success Button */
.btn-medical-success {
    background: var(--success-green);
    color: var(--clean-white);
    border: var(--border-2) solid var(--success-green);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-6);
    font-size: var(--text-base);
    font-weight: var(--font-medium);
}
```

### **Cards**

#### **Medical Card Components**
```css
/* Base Medical Card */
.medical-card {
    background: var(--clean-white);
    border: var(--border-1) solid #e5e7eb;
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-base);
    padding: var(--space-6);
    transition: all 0.2s ease;
}

.medical-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

/* KPI Medical Card */
.kpi-medical-card {
    background: var(--clean-white);
    border-left: var(--border-4) solid var(--primary-pink);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-md);
    padding: var(--space-6);
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

/* Article Medical Card */
.article-medical-card {
    background: var(--clean-white);
    border: var(--border-1) solid #e5e7eb;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    padding: var(--space-5);
    transition: all 0.2s ease;
}

.article-medical-card:hover {
    border-color: var(--primary-blue);
    box-shadow: var(--shadow-md);
}
```

### **Badges**

#### **Medical Badge System**
```css
/* Base Medical Badge */
.medical-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: var(--font-medium);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Sentiment Medical Badges */
.badge-sentiment-positive {
    background: var(--positive-sentiment);
    color: var(--positive-text);
}

.badge-sentiment-negative {
    background: var(--negative-sentiment);
    color: var(--negative-text);
}

.badge-sentiment-neutral {
    background: var(--neutral-sentiment);
    color: var(--neutral-text);
}

/* Topic Medical Badges */
.badge-topic-treatment {
    background: #dbeafe;
    color: #1e40af;
}

.badge-topic-prevention {
    background: #d1fae5;
    color: #065f46;
}

.badge-topic-diagnosis {
    background: #fef3c7;
    color: #92400e;
}

.badge-topic-research {
    background: #e0e7ff;
    color: #3730a3;
}

/* Country Medical Badges */
.badge-country {
    background: var(--light-clinical);
    color: var(--professional-gray);
    border: var(--border-1) solid #d1d5db;
}
```

### **Forms**

#### **Medical Form Components**
```css
/* Medical Input Base */
.medical-input {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    border: var(--border-2) solid #d1d5db;
    border-radius: var(--radius-md);
    font-size: var(--text-base);
    font-weight: var(--font-normal);
    color: var(--professional-gray);
    background: var(--clean-white);
    transition: all 0.2s ease;
}

.medical-input:focus {
    outline: none;
    border-color: var(--primary-blue);
    box-shadow: var(--shadow-focus);
}

.medical-input::placeholder {
    color: var(--citation-gray);
    font-style: italic;
}

/* Medical Select */
.medical-select {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    border: var(--border-2) solid #d1d5db;
    border-radius: var(--radius-md);
    font-size: var(--text-base);
    color: var(--professional-gray);
    background: var(--clean-white);
    background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/></svg>");
    background-repeat: no-repeat;
    background-position: right var(--space-3) center;
    background-size: 1rem;
    padding-right: var(--space-10);
    appearance: none;
}

/* Medical Label */
.medical-label {
    display: block;
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    color: var(--academic-navy);
    margin-bottom: var(--space-2);
}

/* Medical Required Indicator */
.medical-required {
    color: var(--error-red);
    margin-left: var(--space-1);
}
```

### **Tables**

#### **Medical Table System**
```css
/* Medical Table Container */
.medical-table-container {
    background: var(--clean-white);
    border: var(--border-1) solid #e5e7eb;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

/* Medical Table */
.medical-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--text-sm);
}

/* Medical Table Header */
.medical-table th {
    background: var(--light-clinical);
    padding: var(--space-4) var(--space-6);
    text-align: left;
    font-weight: var(--font-semibold);
    color: var(--academic-navy);
    border-bottom: var(--border-2) solid #e5e7eb;
    font-size: var(--text-xs);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Medical Table Cell */
.medical-table td {
    padding: var(--space-4) var(--space-6);
    border-bottom: var(--border-1) solid #f3f4f6;
    color: var(--professional-gray);
    vertical-align: top;
}

/* Medical Table Row Hover */
.medical-table tbody tr:hover {
    background: #f9fafb;
}

/* Medical Table Striped */
.medical-table tbody tr:nth-child(even) {
    background: #fafafa;
}
```

---

## 📊 **Data Visualization Components**

### **Chart Styling**

#### **Medical Chart Colors**
```css
:root {
    /* Medical Chart Color Palette */
    --chart-primary: #4A90E2;
    --chart-secondary: #F8BBD9;
    --chart-tertiary: #0d9488;
    --chart-quaternary: #f59e0b;
    --chart-quinary: #8b5cf6;

    /* Sentiment Chart Colors */
    --chart-positive: #10b981;
    --chart-negative: #ef4444;
    --chart-neutral: #6b7280;

    /* Medical Data Visualization */
    --chart-grid: #f3f4f6;
    --chart-axis: #9ca3af;
    --chart-tooltip: var(--clean-white);
    --chart-tooltip-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

#### **Chart Component Styles**
```css
/* Medical Chart Container */
.medical-chart-container {
    background: var(--clean-white);
    border: var(--border-1) solid #e5e7eb;
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow-sm);
}

/* Medical Chart Title */
.medical-chart-title {
    font-size: var(--text-lg);
    font-weight: var(--font-semibold);
    color: var(--academic-navy);
    margin-bottom: var(--space-4);
    text-align: center;
}

/* Medical Chart Legend */
.medical-chart-legend {
    display: flex;
    justify-content: center;
    gap: var(--space-4);
    margin-top: var(--space-4);
    font-size: var(--text-sm);
}

.medical-legend-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.medical-legend-color {
    width: 12px;
    height: 12px;
    border-radius: var(--radius-sm);
}
```

### **Map Components**

#### **Medical Geographic Map**
```css
/* Medical Map Container */
.medical-map-container {
    background: var(--clean-white);
    border: var(--border-1) solid #e5e7eb;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    height: 400px;
    position: relative;
}

/* Medical Map Popup */
.medical-map-popup {
    background: var(--clean-white);
    border: var(--border-1) solid #e5e7eb;
    border-radius: var(--radius-md);
    padding: var(--space-4);
    box-shadow: var(--shadow-lg);
    font-size: var(--text-sm);
    max-width: 250px;
}

.medical-map-popup-title {
    font-weight: var(--font-semibold);
    color: var(--academic-navy);
    margin-bottom: var(--space-2);
}

/* Medical Map Controls */
.medical-map-controls {
    position: absolute;
    top: var(--space-4);
    right: var(--space-4);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.medical-map-control-button {
    background: var(--clean-white);
    border: var(--border-1) solid #d1d5db;
    border-radius: var(--radius-md);
    padding: var(--space-2);
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    color: var(--professional-gray);
}
```

---

## 📱 **Responsive Design Tokens**

### **Breakpoints**

#### **Medical Device Breakpoints**
```css
:root {
    /* Medical Device Breakpoints */
    --breakpoint-mobile: 320px;    /* Medical mobile minimum */
    --breakpoint-mobile-lg: 480px; /* Large medical mobile */
    --breakpoint-tablet: 768px;    /* Medical tablet (clinical rounds) */
    --breakpoint-tablet-lg: 1024px; /* Large medical tablet */
    --breakpoint-desktop: 1280px;  /* Medical workstation */
    --breakpoint-desktop-lg: 1440px; /* Large medical workstation */
    --breakpoint-desktop-xl: 1920px; /* Extra large medical display */
}
```

### **Responsive Typography**

#### **Fluid Medical Typography**
```css
/* Responsive Medical Typography */
@media (max-width: 768px) {
    :root {
        --text-xs: 0.7rem;       /* Smaller on mobile */
        --text-sm: 0.8rem;
        --text-base: 0.9rem;
        --text-lg: 1rem;
        --text-xl: 1.1rem;
        --text-2xl: 1.25rem;
        --text-3xl: 1.5rem;
        --text-4xl: 1.75rem;
        --text-5xl: 2rem;
    }
}

@media (min-width: 1280px) {
    :root {
        --text-xs: 0.8rem;       /* Larger on desktop */
        --text-sm: 0.95rem;
        --text-base: 1.1rem;
        --text-lg: 1.25rem;
        --text-xl: 1.4rem;
        --text-2xl: 1.75rem;
        --text-3xl: 2.25rem;
        --text-4xl: 2.75rem;
        --text-5xl: 3.5rem;
    }
}
```

### **Responsive Spacing**

#### **Adaptive Medical Spacing**
```css
/* Mobile Medical Spacing */
@media (max-width: 768px) {
    :root {
        --space-4: 0.75rem;      /* Tighter mobile spacing */
        --space-6: 1rem;
        --space-8: 1.5rem;
        --space-12: 2rem;
    }

    .medical-card-padding {
        padding: var(--space-4);
    }

    .medical-section-margin {
        margin-bottom: var(--space-6);
    }
}

/* Desktop Medical Spacing */
@media (min-width: 1280px) {
    :root {
        --space-4: 1.25rem;      /* More generous desktop spacing */
        --space-6: 2rem;
        --space-8: 2.5rem;
        --space-12: 4rem;
    }
}
```

---

## ♿ **Accessibility Design Tokens**

### **Focus States**

#### **Medical Focus Management**
```css
/* Medical Focus Ring */
.medical-focus-ring {
    outline: none;
    box-shadow: 0 0 0 3px var(--primary-blue), 0 0 0 6px rgba(72, 144, 226, 0.2);
    border-radius: var(--radius-md);
}

/* High Contrast Focus */
@media (prefers-contrast: high) {
    .medical-focus-ring {
        box-shadow: 0 0 0 3px #000000, 0 0 0 6px #ffffff;
    }
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
    .medical-focus-ring {
        transition: none;
    }

    .medical-card,
    .btn-medical-primary,
    .medical-input {
        transition: none;
    }
}
```

### **Screen Reader Support**

#### **Medical Screen Reader Classes**
```css
/* Screen Reader Only Text */
.sr-only-medical {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Medical Skip Links */
.medical-skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--primary-blue);
    color: var(--clean-white);
    padding: var(--space-2) var(--space-4);
    text-decoration: none;
    border-radius: var(--radius-md);
    z-index: 1000;
    font-weight: var(--font-medium);
}

.medical-skip-link:focus {
    top: 6px;
}
```

---

## 🎨 **Implementation Guidelines**

### **CSS Custom Properties Usage**

#### **Medical Component Implementation**
```css
/* Example: Medical KPI Card Implementation */
.kpi-medical-card {
    /* Use design tokens consistently */
    background: var(--clean-white);
    border-left: var(--border-4) solid var(--primary-pink);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-md);
    padding: var(--medical-card-padding);

    /* Responsive behavior */
    min-height: 120px;

    /* Medical typography */
    font-family: var(--font-primary);

    /* Accessibility */
    transition: box-shadow 0.2s ease;
}

.kpi-medical-card:focus-within {
    box-shadow: var(--shadow-focus);
}

/* Medical KPI Title */
.kpi-title {
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    color: var(--citation-gray);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--space-2);
}

/* Medical KPI Value */
.kpi-value {
    font-size: var(--text-3xl);
    font-weight: var(--font-extrabold);
    color: var(--primary-blue);
    line-height: var(--leading-tight);
}
```

### **Dark Mode Support**

#### **Medical Dark Mode Tokens**
```css
/* Medical Dark Mode (optional future enhancement) */
@media (prefers-color-scheme: dark) {
    :root {
        --clean-white: #1f2937;
        --light-clinical: #111827;
        --professional-gray: #d1d5db;
        --academic-navy: #93c5fd;
        --primary-blue: #60a5fa;
        --primary-pink: #f472b6;

        /* Maintain medical accessibility in dark mode */
        --positive-sentiment: #064e3b;
        --positive-text: #a7f3d0;
        --negative-sentiment: #7f1d1d;
        --negative-text: #fca5a5;
        --neutral-sentiment: #374151;
        --neutral-text: #d1d5db;
    }
}
```

---

## 📋 **Design System Checklist**

### **Implementation Checklist**

#### **Phase 1: Foundation**
- [ ] **Color Palette** - Implement medical color variables
- [ ] **Typography** - Set up medical font hierarchy
- [ ] **Spacing** - Define medical spacing tokens
- [ ] **Border & Radius** - Implement medical border system
- [ ] **Shadows** - Create medical shadow system

#### **Phase 2: Components**
- [ ] **Buttons** - All medical button variants
- [ ] **Cards** - Medical card components
- [ ] **Badges** - Medical badge system
- [ ] **Forms** - Medical form components
- [ ] **Tables** - Medical table styling

#### **Phase 3: Data Visualization**
- [ ] **Charts** - Medical chart styling
- [ ] **Maps** - Medical geographic components
- [ ] **Legends** - Medical chart legends
- [ ] **Tooltips** - Medical data tooltips

#### **Phase 4: Accessibility**
- [ ] **Focus States** - Medical focus management
- [ ] **Color Contrast** - WCAG AA compliance
- [ ] **Screen Readers** - Medical SR support
- [ ] **Keyboard Navigation** - Medical keyboard support
- [ ] **Reduced Motion** - Medical motion preferences

#### **Phase 5: Responsive**
- [ ] **Breakpoints** - Medical device breakpoints
- [ ] **Typography** - Responsive medical text
- [ ] **Spacing** - Adaptive medical spacing
- [ ] **Components** - Responsive medical components

---

## 🔧 **Development Integration**

### **Tailwind CSS Configuration**

#### **Medical Tailwind Config**
```javascript
// tailwind.config.js - Medical Configuration
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Medical Brand Colors
        'primary-pink': '#F8BBD9',
        'primary-blue': '#4A90E2',
        'medical-gradient': 'linear-gradient(135deg, #F8BBD9 0%, #4A90E2 100%)',

        // Medical Sentiment Colors
        'positive-sentiment': '#d1fae5',
        'positive-text': '#065f46',
        'negative-sentiment': '#fef2f2',
        'negative-text': '#991b1b',
        'neutral-sentiment': '#f3f4f6',
        'neutral-text': '#374151',

        // Medical Interface
        'clean-white': '#FFFFFF',
        'light-clinical': '#F5F5F5',
        'professional-gray': '#666666',
        'academic-navy': '#1e3a8a',
        'research-teal': '#0d9488',
        'citation-gray': '#64748b'
      },

      fontFamily: {
        'medical': ['Inter', 'Segoe UI', 'sans-serif'],
        'medical-mono': ['JetBrains Mono', 'SF Mono', 'monospace']
      },

      spacing: {
        // Medical spacing scale
        '18': '4.5rem',   // 72px
        '88': '22rem',    // 352px
        '128': '32rem'    // 512px
      },

      boxShadow: {
        'medical': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'medical-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'medical-focus': '0 0 0 3px rgba(72, 144, 226, 0.1)'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
};
```

### **CSS-in-JS Integration**

#### **Styled Components Medical Theme**
```javascript
// Medical Theme for Styled Components
export const medicalTheme = {
  colors: {
    primary: {
      pink: '#F8BBD9',
      blue: '#4A90E2'
    },
    sentiment: {
      positive: { bg: '#d1fae5', text: '#065f46' },
      negative: { bg: '#fef2f2', text: '#991b1b' },
      neutral: { bg: '#f3f4f6', text: '#374151' }
    },
    medical: {
      white: '#FFFFFF',
      clinical: '#F5F5F5',
      gray: '#666666',
      navy: '#1e3a8a',
      teal: '#0d9488',
      citation: '#64748b'
    }
  },

  typography: {
    fontFamily: {
      primary: ['Inter', 'Segoe UI', 'sans-serif'],
      mono: ['JetBrains Mono', 'SF Mono', 'monospace']
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem'
    }
  },

  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem'
  },

  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    focus: '0 0 0 3px rgba(72, 144, 226, 0.1)'
  }
};
```

---

**Este design system médico está listo para implementación inmediata en React con Tailwind CSS o Styled Components, optimizado para profesionales de la salud y el contexto académico de UCOMPENSAR.**

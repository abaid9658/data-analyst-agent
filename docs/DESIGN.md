# 🎨 Design System

## AI Data Analyst Agent — UI/UX Design Specification

---

## 1. Design Philosophy

**"Data Made Human"**

The interface should feel like a conversation with a brilliant data scientist — not like a technical dashboard. Every element guides users toward insight, never overwhelming them. The visual language is calm, confident, and intelligent.

### Core Principles

| Principle | Expression |
|---|---|
| **Clarity First** | Every pixel serves communication. No decorative noise. |
| **Progressive Disclosure** | Show simple first. Reveal complexity on demand. |
| **Data-Centric** | Charts, tables, and text have equal visual weight. |
| **Conversational** | The UI feels like talking, not operating machinery. |
| **Trustworthy** | Confidence levels, explanations, and source citations. |

---

## 2. Color System

### Primary Palette

```css
/* Brand / Primary — Deep Indigo */
--color-primary-50:  #EEF2FF;
--color-primary-100: #E0E7FF;
--color-primary-200: #C7D2FE;
--color-primary-300: #A5B4FC;
--color-primary-400: #818CF8;
--color-primary-500: #6366F1;   /* Main brand color */
--color-primary-600: #4F46E5;
--color-primary-700: #4338CA;
--color-primary-800: #3730A3;
--color-primary-900: #312E81;
--color-primary-950: #1E1B4B;
```

### Accent / Secondary — Cyan

```css
--color-accent-50:  #ECFEFF;
--color-accent-400: #22D3EE;
--color-accent-500: #06B6D4;   /* Secondary accent */
--color-accent-600: #0891B2;
```

### Semantic Colors

```css
/* Success */
--color-success-400: #4ADE80;
--color-success-500: #22C55E;

/* Warning */
--color-warning-400: #FACC15;
--color-warning-500: #EAB308;

/* Error */
--color-error-400: #F87171;
--color-error-500: #EF4444;

/* Info */
--color-info-400:  #60A5FA;
--color-info-500:  #3B82F6;
```

### Neutral (Dark Mode Base)

```css
/* Dark Mode */
--color-gray-950: #0A0A0F;    /* Page background */
--color-gray-900: #0F0F1A;    /* Card/panel background */
--color-gray-850: #141425;    /* Elevated surface */
--color-gray-800: #1C1C2E;    /* Border, divider */
--color-gray-700: #252540;    /* Input background */
--color-gray-600: #3A3A60;    /* Placeholder */
--color-gray-400: #6B7280;    /* Muted text */
--color-gray-200: #C4C6D0;    /* Body text */
--color-gray-100: #E2E3EA;    /* Heading text */
--color-gray-50:  #F3F4F6;    /* Inverse surface */

/* Light Mode */
--color-light-bg:       #F7F8FC;
--color-light-surface:  #FFFFFF;
--color-light-border:   #E5E7EB;
--color-light-text:     #111827;
--color-light-muted:    #6B7280;
```

---

## 3. Typography

### Font Families

```css
/* UI / Interface */
--font-sans: 'Inter', system-ui, -apple-system, sans-serif;

/* Code / SQL / Python */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

/* Display / Hero */
--font-display: 'Cal Sans', 'Inter', sans-serif;
```

### Type Scale

```css
--text-xs:   0.75rem;   /* 12px — captions, badges */
--text-sm:   0.875rem;  /* 14px — body small, labels */
--text-base: 1rem;      /* 16px — body default */
--text-lg:   1.125rem;  /* 18px — body large */
--text-xl:   1.25rem;   /* 20px — section headers */
--text-2xl:  1.5rem;    /* 24px — page titles */
--text-3xl:  1.875rem;  /* 30px — hero text */
--text-4xl:  2.25rem;   /* 36px — landing page hero */
--text-5xl:  3rem;      /* 48px — marketing headline */
```

### Font Weights

```css
--font-regular: 400;
--font-medium:  500;
--font-semibold: 600;
--font-bold:    700;
--font-black:   900;
```

### Line Heights

```css
--leading-tight:  1.25;   /* Headlines */
--leading-snug:   1.375;  /* Subheadings */
--leading-normal: 1.5;    /* Body text */
--leading-relaxed: 1.625; /* Prose */
```

---

## 4. Spacing System

8px grid system:

```css
--space-0:  0px;
--space-1:  4px;
--space-2:  8px;
--space-3:  12px;
--space-4:  16px;
--space-5:  20px;
--space-6:  24px;
--space-8:  32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
```

---

## 5. Border Radius

```css
--radius-sm:   4px;    /* Badges, tags */
--radius-md:   8px;    /* Inputs, small cards */
--radius-lg:   12px;   /* Cards */
--radius-xl:   16px;   /* Panels */
--radius-2xl:  24px;   /* Modals */
--radius-full: 9999px; /* Pills, avatars */
```

---

## 6. Shadows (Dark Mode)

```css
--shadow-sm:  0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3);
--shadow-md:  0 4px 6px rgba(0,0,0,0.4), 0 2px 4px rgba(0,0,0,0.3);
--shadow-lg:  0 10px 25px rgba(0,0,0,0.5), 0 4px 10px rgba(0,0,0,0.3);
--shadow-xl:  0 25px 50px rgba(0,0,0,0.6);

/* Glow effects */
--glow-primary: 0 0 20px rgba(99,102,241,0.3);
--glow-accent:  0 0 20px rgba(6,182,212,0.3);
```

---

## 7. Component Specifications

### 7.1 Chat Message — User

```
┌─────────────────────────────────────────────────────────────┐
│                              ┌─────────────────────────────┐│
│                              │ Show me monthly revenue     ││
│                              │ trend for last year         ││
│                              └─────────────────────────────┘│
│                                          John D.  10:34 AM  │
└─────────────────────────────────────────────────────────────┘

Style:
  Background: --color-primary-600 (indigo bubble)
  Border-radius: 18px 4px 18px 18px
  Max-width: 70%
  Align: right
  Font: Inter 14px, white
```

### 7.2 Chat Message — Assistant

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 ┌─────────────────────────────────────────────────────┐  │
│    │ Here's the monthly revenue analysis for 2025:      │  │
│    │                                                    │  │
│    │ [SQL Query Block]                                  │  │
│    │ [Interactive Chart]                                │  │
│    │ [Key Insights]                                     │  │
│    │ [Business Recommendations]                         │  │
│    └─────────────────────────────────────────────────────┘  │
│    AI Analyst  10:34:15 AM  · 2.3s · GPT-4o                 │
└─────────────────────────────────────────────────────────────┘

Style:
  Background: --color-gray-850
  Border: 1px solid --color-gray-800
  Border-radius: 4px 18px 18px 18px
  Max-width: 90%
  Align: left
```

### 7.3 SQL Code Block

```
┌─────────────────────────────────────────────────────────────┐
│ SQL Query                               [Copy] [Run] [Edit] │
│─────────────────────────────────────────────────────────────│
│  SELECT                                                     │
│    DATE_TRUNC('month', created_at) AS month,               │
│    SUM(revenue) AS total_revenue                           │
│  FROM orders                                               │
│  WHERE created_at >= '2025-01-01'                          │
│  GROUP BY 1                                                │
│  ORDER BY 1                                                │
└─────────────────────────────────────────────────────────────┘

Style:
  Background: #0D1117 (GitHub dark)
  Border: 1px solid #30363D
  Border-radius: --radius-lg
  Font: JetBrains Mono 13px
  Syntax highlighting: VSCode Dark+
  Top bar: --color-gray-800
```

### 7.4 Chart Card

```
┌─────────────────────────────────────────────────────────────┐
│ Monthly Revenue 2025              [Line ▾] [↓ PNG] [↓ PDF] │
│─────────────────────────────────────────────────────────────│
│                                                             │
│  $2.5M ┤                                    ╭──────         │
│  $2.0M ┤                           ╭────────╯              │
│  $1.5M ┤               ╭───────────╯                       │
│  $1.0M ┤  ╭────────────╯                                   │
│        └──┬────┬────┬────┬────┬────┬────┬────┬────┬────►  │
│          Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct   │
│                                                             │
│─────────────────────────────────────────────────────────────│
│ 💡 Revenue grew 23% YoY · Peak: December · Dip: Q2        │
└─────────────────────────────────────────────────────────────┘
```

### 7.5 KPI Widget

```
┌─────────────────────┐
│ Total Revenue       │
│ $2.3M              │
│ ↑ 23% vs last year │
└─────────────────────┘

Border-left: 4px solid --color-primary-500
Background: linear-gradient(135deg, rgba(99,102,241,0.1), transparent)
```

### 7.6 Dataset Upload Zone

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│          📂  Drop your file here                           │
│              or click to browse                            │
│                                                             │
│          CSV · Excel · JSON  ·  Max 500MB                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Normal: Border: 2px dashed --color-gray-700
Hover: Border: 2px dashed --color-primary-400, Glow: --glow-primary
Dragging: Background: rgba(99,102,241,0.05)
```

---

## 8. Page Layouts

### 8.1 Main Chat Layout

```
┌────────────────────────────────────────────────────────────────────┐
│ ┌──────────┐  ┌──────────────────────────────────────────────────┐ │
│ │          │  │ ▶ AI Data Analyst        🔍  🌙  🔔  Avatar     │ │
│ │ Sidebar  │  │──────────────────────────────────────────────────│ │
│ │          │  │                                                  │ │
│ │ + New    │  │                                                  │ │
│ │ Chat     │  │          ← Chat Messages Area →                 │ │
│ │          │  │                                                  │ │
│ │ Recent   │  │                                                  │ │
│ │ Sessions │  │                                                  │ │
│ │          │  │                                                  │ │
│ │ ─────── │  │                                                  │ │
│ │ Datasets │  │──────────────────────────────────────────────────│ │
│ │          │  │ Dataset: [sales.csv ▾]   [🗄️ DB connection]     │ │
│ │ ─────── │  │──────────────────────────────────────────────────│ │
│ │ Settings │  │ ┌──────────────────────────────────────┐ [Send] │ │
│ │ Help     │  │ │ Ask anything about your data...      │   ↑    │ │
│ │          │  │ └──────────────────────────────────────┘        │ │
│ └──────────┘  └──────────────────────────────────────────────────┘ │
│  240px                          flex: 1                            │
└────────────────────────────────────────────────────────────────────┘
```

### 8.2 Dashboard Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Dashboard: Q2 2026 Sales                     [Edit] [Share] [↓]  │
│────────────────────────────────────────────────────────────────────│
│  [Total Revenue  ] [Total Orders   ] [Avg Order Value] [Churn %  ] │
│  [$2.3M  ↑23%   ] [45,230  ↑12%  ] [$51.2   ↑8%   ] [2.1%  ↓0.3]│
│────────────────────────────────────────────────────────────────────│
│  ┌──────────────────────────────┐  ┌─────────────────────────────┐ │
│  │  Monthly Revenue             │  │  Revenue by Region          │ │
│  │  [Line Chart - full width]   │  │  [Pie/Donut Chart]          │ │
│  └──────────────────────────────┘  └─────────────────────────────┘ │
│  ┌──────────────────────────────┐  ┌─────────────────────────────┐ │
│  │  Top 10 Products             │  │  Customer Segments          │ │
│  │  [Bar Chart horizontal]      │  │  [Treemap]                  │ │
│  └──────────────────────────────┘  └─────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Orders Data Table                              [Filter] [↓] │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

---

## 9. Motion & Animation

### Timing Functions

```css
--ease-out:    cubic-bezier(0.0, 0.0, 0.2, 1);    /* Elements entering */
--ease-in:     cubic-bezier(0.4, 0.0, 1, 1);       /* Elements leaving */
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* Bouncy interactions */
```

### Durations

```css
--duration-fast:   100ms;   /* Hover states */
--duration-normal: 200ms;   /* Transitions */
--duration-slow:   350ms;   /* Page transitions */
--duration-slower: 500ms;   /* Complex animations */
```

### Key Animations

```css
/* Message appear */
@keyframes messageSlideIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Thinking dots */
@keyframes thinkingPulse {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50%       { opacity: 1;   transform: scale(1); }
}

/* Chart reveal */
@keyframes chartFadeIn {
  from { opacity: 0; transform: scale(0.97); }
  to   { opacity: 1; transform: scale(1); }
}

/* Sidebar item hover */
/* background: linear-gradient → transition 200ms ease */

/* Button press */
/* transform: scale(0.97) → 100ms ease-spring */
```

---

## 10. Iconography

Use **Lucide React** icon set throughout. Icon sizes:
- Navigation: 20px
- Inline: 16px
- Hero/Feature: 32px
- Empty state: 48px

Key icons:
- Chat: `MessageSquare`
- Dataset: `Database`
- Upload: `Upload`
- Chart: `BarChart2`
- SQL: `Code2`
- ML: `Brain`
- Report: `FileText`
- Dashboard: `LayoutDashboard`
- Insights: `Lightbulb`
- Settings: `Settings`
- User: `User`

---

## 11. Empty States

Each empty state has:
1. Illustration (subtle, on-brand)
2. Title (1 line)
3. Description (2 lines max)
4. Primary CTA

### No Conversations

```
     📊
  Start Analyzing
  Upload a dataset or connect a database
  to begin your AI-powered analysis.

  [Upload Dataset]  [Connect Database]
```

### No Datasets

```
     📁
  No datasets yet
  Drag & drop a CSV, Excel, or JSON file
  or connect to a live database.

  [Browse Files]
```

---

## 12. Loading States

- **Streaming text:** Typing cursor animation
- **Thinking:** Three animated dots with "Analyzing your data..."
- **Chart loading:** Skeleton placeholder → fade in
- **Table loading:** Row skeletons (6 rows)
- **Page load:** Indigo progress bar at top of viewport

---

## 13. Accessibility

- WCAG 2.1 AA compliant
- Color contrast ratio ≥ 4.5:1 for text
- All interactive elements: focus rings (2px, --color-primary-400)
- Keyboard navigation: full support
- Screen reader: aria-labels on all icons
- Motion: `prefers-reduced-motion` support
- Font size: minimum 14px for body text

---

## 14. Responsive Breakpoints

```css
--bp-sm:  640px;   /* Mobile landscape */
--bp-md:  768px;   /* Tablet */
--bp-lg:  1024px;  /* Small desktop */
--bp-xl:  1280px;  /* Desktop */
--bp-2xl: 1536px;  /* Wide screen */
```

### Mobile Adaptations
- Sidebar collapses to bottom navigation (5 items)
- Chat input: full width, sticky bottom
- Charts: horizontal scroll container
- Tables: horizontal scroll with frozen first column

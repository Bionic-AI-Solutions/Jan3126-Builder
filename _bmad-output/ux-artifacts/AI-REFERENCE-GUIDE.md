# WABuilder UI Mockups - AI Reference Guide

## Overview

This directory contains **137 HTML mockups** across all WABuilder portals, organized for easy reference during implementation. These mockups serve as visual specifications for development teams and AI assistants.

## Quick Stats

- **Total Screens:** 137
- **High Fidelity:** 3 screens (95% complete, pixel-accurate)
- **Medium Fidelity:** 29 screens (75% complete, template-based)
- **Low Fidelity:** 105 screens (wireframes with annotations)

## Directory Structure

```
_bmad-output/ux-artifacts/
├── mockups/
│   ├── index.html                          # Master navigation with search
│   ├── _assets/
│   │   └── styles.css                      # Design tokens as CSS variables
│   ├── business-owner-portal/              # 38+ mobile screens
│   │   ├── 01-onboarding-setup/
│   │   ├── 02-template-beta-testing/
│   │   ├── 03-escalation-handling/
│   │   ├── 04-dashboard-monitoring/
│   │   ├── 05-revenue-analytics/
│   │   ├── 06-settings-configuration/
│   │   └── 07-conversation-management/
│   ├── developer-portal/                   # 52+ desktop screens
│   │   ├── 01-authentication/
│   │   ├── 02-business-setup/
│   │   ├── 03-integration-testing/
│   │   ├── 04-approval-submission/
│   │   ├── 05-portfolio-management/
│   │   ├── 06-revenue-analytics/
│   │   └── 07-health-monitoring/
│   ├── admin-portal/                       # 25 desktop screens
│   │   ├── 01-approval-quality-gates/
│   │   ├── 02-platform-monitoring/
│   │   ├── 03-developer-management/
│   │   ├── 04-quality-review/
│   │   └── 05-manual-intervention/
│   └── system-screens/                     # 10 edge case screens
│       ├── 01-error-handling/
│       ├── 02-empty-states/
│       └── 03-loading-offline/
└── generator/                              # Source code (version controlled)
    ├── generate_mockups.py
    ├── screen_definitions.yaml
    ├── design_tokens.json
    └── templates/
```

## How to Use These Mockups

### 1. Browse All Mockups

Open the master index:
```
file:///workspaces/wabuilder/_bmad-output/ux-artifacts/mockups/index.html
```

Features:
- **Search:** Type any screen name to filter instantly
- **Portal Cards:** All screens organized by portal
- **Fidelity Badges:** Visual indicators of mockup completeness

### 2. Link Mockups in Epics & Stories

When writing epics or stories, reference mockups using this format:

**Example Epic:**
```markdown
## Epic: Business Owner Dashboard

### Related Mockups

**Primary Screens:**
- [Mobile Dashboard](file:///workspaces/wabuilder/_bmad-output/ux-artifacts/mockups/business-owner-portal/04-dashboard-monitoring/bo-dashboard.html)
  - Fidelity: High (95%)
  - Components: Metric cards, escalation widget, action buttons
  - Key Features: Real-time metrics, urgent escalations, WhatsApp integration

**Supporting Screens:**
- [Escalation Detail](file:///workspaces/wabuilder/_bmad-output/ux-artifacts/mockups/business-owner-portal/03-escalation-handling/bo-escalation-detail.html)
- [Settings Menu](file:///workspaces/wabuilder/_bmad-output/ux-artifacts/mockups/business-owner-portal/06-settings-configuration/bo-settings-menu.html)

### User Journey

1. User opens app → sees [Mobile Dashboard](#mockup-link)
2. Taps escalation → opens [Escalation Detail](#mockup-link)
3. Resolves via WhatsApp deeplink → returns to dashboard
```

### 3. AI Parsing: Screen Metadata

Each mockup includes embedded JSON metadata for AI parsing:

```html
<script type="application/json" id="screen-metadata">
{
  "screen_id": "bo-dashboard",
  "portal": "business-owner",
  "category": "dashboard-monitoring",
  "fidelity": "high",
  "components_used": ["metric-card", "escalation-card", "button"],
  "user_journey": "business-owner-daily-management",
  "critical_path": true
}
</script>
```

**AI can extract:**
- Screen ID and portal context
- Required components
- User journey association
- Implementation priority (critical_path)

### 4. Design Token Reference

All mockups use CSS variables from `_assets/styles.css`:

```css
/* Colors */
--color-primary-main: #25D366;        /* WhatsApp green */
--color-secondary-main: #075E54;      /* WhatsApp teal */
--color-bg-cream: #ECE5DD;            /* Business Owner portal */

/* Spacing */
--space-4: 16px;
--space-6: 24px;

/* Typography */
.heading-h3 { font-size: 20px; line-height: 28px; font-weight: 600; }
.metric-large { font-size: 24px; line-height: 32px; font-weight: 700; }
```

**For Implementation:**
- Reference design tokens, don't hardcode values
- Use same CSS variable names in production code
- Ensures consistency with mockups

## Fidelity Levels Explained

### High Fidelity (95% Complete)

**Characteristics:**
- Pixel-accurate spacing and measurements
- Realistic sample data
- All interactive states shown
- Complete component implementations

**Example Screens:**
- Business Owner Dashboard (`bo-dashboard.html`)
- Developer Portfolio Dashboard (`dev-portfolio-dashboard.html`)
- Admin Approval Queue (`admin-approval-queue.html`)

**Use When:**
- Implementing critical user journeys
- Need exact measurements
- Building reusable components

### Medium Fidelity (75% Complete)

**Characteristics:**
- Template-based layouts
- Representative content
- Simplified details
- Core functionality visible

**Example Screens:**
- Business setup screens
- List views and tables
- Form wizards

**Use When:**
- General feature implementation
- Layout structure is clear
- Some details can be inferred

### Low Fidelity (Wireframes, 40% Complete)

**Characteristics:**
- Wireframe boxes with annotations
- Component placeholders
- Purpose and context documented
- Interaction notes included

**Example Screens:**
- Edge cases and error states
- Secondary configuration screens
- Advanced admin features

**Use When:**
- Feature is straightforward
- Implementation can extrapolate from pattern
- Annotations provide sufficient context

## Common Usage Patterns

### Pattern 1: Feature Implementation

```markdown
## Story: Implement Emergency Shutoff

**Mockup:** [Emergency Shutoff Confirmation](file:///.../bo-emergency-shutoff.html)

**Implementation Notes:**
- Extract screen metadata → identify components needed
- Reference design tokens → apply WhatsApp color palette
- Check wireframe annotations → understand interaction flow
- Build component → match layout structure
```

### Pattern 2: Component Library Building

```markdown
## Task: Build Metric Card Component

**Reference Mockups:**
- [Business Owner Dashboard](file:///.../bo-dashboard.html) - Primary usage
- [Developer Portfolio](file:///.../dev-portfolio-dashboard.html) - Variant
- [Admin Platform Health](file:///.../admin-platform-health.html) - Desktop version

**Extract Common Patterns:**
1. Read all 3 mockups
2. Identify metric-card HTML structure
3. Note differences (mobile vs desktop, with/without trends)
4. Create flexible component with variants
```

### Pattern 3: User Journey Visualization

```markdown
## Epic: Developer Onboarding Flow

**Journey Mockups (in order):**
1. [Landing Page](file:///.../dev-landing-page.html)
2. [Registration Form](file:///.../dev-registration-form.html)
3. [Application Pending](file:///.../dev-application-pending.html)
4. [Dashboard Empty State](file:///.../dev-dashboard-empty.html)
5. [Onboarding Wizard](file:///.../dev-onboarding-wizard.html)

**Navigation Flow:**
Landing → Register → Wait → Approve → Dashboard → Onboard → First Business
```

## Screen Naming Convention

All screen files follow this pattern:
```
{portal-prefix}-{screen-function}.html
```

**Portal Prefixes:**
- `bo-` = Business Owner Portal
- `dev-` = Developer Portal
- `admin-` = Admin Portal
- `system-` = System/Edge Screens

**Examples:**
- `bo-dashboard.html` = Business Owner Dashboard
- `dev-portfolio-dashboard.html` = Developer Portfolio Dashboard
- `admin-approval-queue.html` = Admin Approval Queue
- `system-generic-error.html` = Generic Error Modal

## Updating Mockups

The generator allows quick updates to all screens:

```bash
cd /workspaces/wabuilder/_bmad-output/ux-artifacts/generator

# Update all screens with new design tokens
python3 generate_mockups.py

# This regenerates all 137 screens in ~30 seconds
```

**What's Version Controlled:**
- `screen_definitions.yaml` - Source of truth for all screens
- `design_tokens.json` - Design system values
- `templates/` - Jinja2 templates and components
- `generate_mockups.py` - Generator script

**What's NOT Version Controlled (Generated Output):**
- `../mockups/*.html` - All generated HTML files

## Integration with Development Workflow

### During Sprint Planning

1. **Review epics** → Identify required screens
2. **Open mockups** → Understand scope and complexity
3. **Check fidelity** → Determine if additional design needed
4. **Extract metadata** → Feed into story templates

### During Implementation

1. **Open relevant mockup** in browser
2. **Inspect HTML/CSS** to see exact structure
3. **Copy design token usage** for consistency
4. **Reference annotations** for interaction notes
5. **Test against mockup** visually during development

### For AI Assistants

1. **Parse screen metadata JSON** from mockup files
2. **Extract component list** → Know what to build
3. **Read wireframe annotations** → Understand intent
4. **Reference design tokens** → Generate matching code
5. **Follow user journey links** → Maintain flow consistency

## Key Mockups by User Journey

### Business Owner: Daily Management
- **Dashboard:** `bo-dashboard.html` (HIGH)
- **Escalation Detail:** `bo-escalation-detail.html` (HIGH)
- **Escalation List:** `bo-escalation-list.html` (MEDIUM)
- **Settings:** `bo-settings-menu.html` (MEDIUM)

### Developer: Business Setup
- **Portfolio Dashboard:** `dev-portfolio-dashboard.html` (HIGH)
- **New Business Form:** `dev-new-business-form.html` (MEDIUM)
- **Host AI Interview:** `dev-host-ai-interview.html` (MEDIUM)
- **Sandbox Dashboard:** `dev-sandbox-dashboard.html` (MEDIUM)

### Admin: Approval Queue
- **Approval Queue:** `admin-approval-queue.html` (HIGH)
- **Business Detail:** `admin-business-detail.html` (MEDIUM)
- **Bulk Action:** `admin-bulk-action.html` (MEDIUM)
- **Platform Health:** `admin-platform-health.html` (HIGH)

## Design System Quick Reference

### Colors (WhatsApp-Inspired)
```
Primary Green:   #25D366  (buttons, success states, metrics)
Secondary Teal:  #075E54  (headers, navigation, accents)
Background Cream: #ECE5DD  (Business Owner portal only)
Background Gray: #F5F5F5  (Developer/Admin portals)
```

### Typography
```
Headings: Inter Bold/SemiBold (700/600)
Body: Inter Regular (400)
Labels: Inter Medium (500)
Metrics: Inter ExtraBold/Bold (800/700)
```

### Spacing Scale
```
space-2: 8px   (tight gaps)
space-3: 12px  (card gaps)
space-4: 16px  (standard padding)
space-6: 24px  (section spacing)
```

### Border Radius
```
radius-sm: 4px   (badges, small elements)
radius-md: 8px   (cards, buttons)
radius-lg: 12px  (large cards)
radius-full: 9999px (pills, avatars)
```

## Questions?

- **Generator issues:** Check `generator/generate_mockups.py`
- **Design token questions:** See `generator/design_tokens.json`
- **Screen definitions:** Review `generator/screen_definitions.yaml`
- **Visual reference:** Open `mockups/index.html` and use search

---

**Last Generated:** 2026-02-03
**Total Screens:** 137
**Generator Version:** 1.0

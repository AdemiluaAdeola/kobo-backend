# Kobo

**Your Money, Smarter. An AI Coach in Your Pocket.**

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20iOS%20%7C%20WhatsApp-green.svg)]()
[![Status](https://img.shields.io/badge/status-In%20Development-yellow.svg)]()

## 🎯 The Problem: The "Salary Week" Trap

Young Nigerian professionals earn well but manage money reactively:

- 💸 **Broke 5 days before payday** despite decent income
- 😵 **Overwhelmed by multiple income streams** (9-5 + side hustles + family support)
- ⚠️ **Blindsided by expenses** — subscriptions, emergencies, social obligations
- 📉 **Intimidated by investing** — complex jargon, high minimums, trust issues

Existing solutions (PiggyVest, Kuda, Excel sheets) are passive. They show you what happened.

**Kobo tells you what's coming — and acts before it's too late.**

---

## ✨ Solution: Predictive Finance Coaching

Kobo combines real-time transaction intelligence, predictive AI, and behavioral nudges to make financial discipline automatic.

&gt; **"Don't just track your money. See the future, change the present."**

---

## 🚀 Core Features

### 1. Smart Cash Flow Forecasting
Predicts your balance **14 days ahead** with 85%+ accuracy.

| Capability | Example |
|------------|---------|
| Payday pattern recognition | *"You usually get paid 24th-26th. Forecast updated."* |
| Spending velocity tracking | *"At this rate, you'll hit ₦5k by Tuesday."* |
| Safe-to-spend calculation | *"You have ₦12,400 safe to spend today."* |

**Tech Stack:** Prophet time-series models trained on individual spending patterns + Nigerian salary cycles

---

### 2. Conversational AI Coach
WhatsApp-style chat interface. No banking app complexity.

**Sample Interactions:**

&gt; **User:** *"Can I afford dinner out tonight?"*
&gt; 
&gt; **Kobo:** *"You've spent ₦8,200/₦15,000 on food this week. Safe to spend: ₦3,400. Maybe keep it under ₦2,500?"* 🍜

&gt; **Kobo (proactive):** *"Your Netflix renews tomorrow (₦4,400). You'll still have ₦11,200 after. All good ✅"*

- **Tone:** Encouraging, never shaming
- **Language:** Pidgin-friendly
- **Input:** Voice note support

---

### 3. Predictive Nudges
Right message, right time, right channel.

| Trigger | Nudge | Action |
|---------|-------|--------|
| Salary detected | *"You just got paid! Auto-save 10% (₦45,000)?"* | One-tap save |
| Low balance forecast | *"You'll hit ₦2k by Friday. Pause subscriptions?"* | Manage subs |
| Unusual spending | *"You spent ₦15k at Shoprite — 2x normal. Everything okay?"* | Review/categorize |
| Goal milestone near | *"₦5k to hit your Emergency Fund goal. Top up?"* | Quick add |

**Delivery:** Push notification + In-app + Optional WhatsApp

---

### 4. Intelligent Transaction Categorization
Works with messy Nigerian bank data.

- **SMS Parsing:** Handles GTBank, UBA, Zenith, Access formats
- **Merchant Identification:** Knows Jumia vs. Jumia Food vs. Jumia Pay
- **Auto-categorization:** Food, Transport, Subscriptions, Transfers, "Black Tax"
- **Learning System:** Gets smarter with every manual correction

*Fallback: Manual categorization with gamified "train your Kobo"*

---

### 5. Goal-Based Micro-Investing
Wealth building for beginners.

**Spaces (Sub-accounts):**
- 🛡️ Emergency Fund (target: 3 months expenses)
- 🏠 Rent 2026
- 💼 Side Hustle Capital
- 🎉 "Detty December" (guilt-free fun fund)

**Automation Rules:**
- **Round-ups:** Save ₦50 on every ₦450+ spend
- **Percent rules:** *"Save 5% of all freelance income"*
- **Payday auto-save:** *"Take 10% before I touch it"*

---

### 6. Debt Intelligence
Tracks formal and informal obligations.

| Type | Examples | Features |
|------|----------|----------|
| **Formal** | Palmcredit, Carbon, bank loans | APR tracking, payoff dates |
| **Informal** | Esusu contributions, family loans, "I owe you" | Due date reminders |
| **Optimization** | — | Snowball vs. avalanche recommendations |
| **Credit Score** | — | Simulated based on payment behavior |

---

## 🛣️ User Journey

### Onboarding (3 minutes)
1. Phone number signup
2. Connect bank (Mono/Okra) OR forward 3 SMS alerts
3. Set one goal (Emergency fund recommended)
4. Choose nudge frequency (Minimal / Balanced / Verbose)

### Week 1: Baseline
- Kobo ingests 90 days of history (if available)
- Learns payday patterns, fixed expenses, spending velocity
- Daily check-ins: *"How would you categorize this ₦2,500?"*

### Week 2-4: First Predictions
- Cash flow forecast appears
- First "safe to spend" calculation
- First proactive nudge (likely payday-related)

### Month 2+: Habit Formation
- Automated savings rules active
- Goal progress visible
- Weekly **"Money Minute"** summary (shareable)

---

## 🎯 Target Users

### Primary
**Young professionals, 22-35, Lagos/Abuja**
- 💰 Income: ₦150k–₦800k/month
- 📱 Tech-savvy but financially overwhelmed
- 🔄 Multiple income streams
- 🏦 Skeptical of traditional banks, open to fintech

### Secondary
- Graduate trainees
- NYSC corps members
- Gig workers (Bolt drivers, freelance designers)

---

## 🗣️ Brand Voice

**Attributes:** Smart, empathetic, unpretentious, Nigerian

### Messaging Examples

| ❌ Don't Say | ✅ Say Instead |
|-------------|---------------|
| "Optimize your financial portfolio" | "Make your salary last longer" |
| "Budgeting made simple" | "No more 'gbese' days before payday" |

### Visual Identity
- **Deep Green:** Money, growth
- **Warm Orange:** Energy, alerts
- **Typography:** Clean sans-serif
- **Style:** Emoji-friendly

---

## 🛠️ Tech Stack

- **Frontend:** React Js(web) / React Native(app)
- **Backend:** Python (FastAPI for easy ai integration)
- **AI/ML:** Prophet (time-series), NLP for transaction parsing
- **Bank Integration:** Mono, Okra
- **Messaging:** WhatsApp Business API, Push notifications

---

## 📦 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/AdemiluaAdeola/kobo-backend.git

# Navigate to project directory
cd kobo

# Set up environment variables( this is for linux users, kindly check for windows and mac)
python3 -m venv venv
source venv/bin/activate

# Install dependencies( this is for linux users, kindly check for windows and mac)
pip install -r requirements.txt

# Run development server
python main.py
```

---

## Links
Landing page - [Click Here](https://kobo-ai.vercel.app/#)

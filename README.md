# AI Team Bot — Setup Guide

A Telegram group where you give orders and 5 AI agents do the work.

---

## Your Team

| Agent | Name | Does |
|-------|------|------|
| @ResumeBot | Alex | Resume rewrites, ATS optimization, cover letters, LinkedIn profiles |
| @ClientBot | Sarah | Client email replies, follow-ups, complaint handling, outreach |
| @LinkedInBot | Marcus | LinkedIn posts, hooks, personal brand content, profile summaries |
| @ResearchBot | Diana | Competitor analysis, market research, pricing intelligence, trends |
| @FinanceBot | Kevin | Pricing strategy, revenue planning, package design, unit economics |

---

## What You Need

1. **Telegram Bot Token** — free, takes 2 minutes
2. **Anthropic API Key** — ~$5–20/month depending on usage

---

## Step 1 — Create Your Telegram Bots (free)

You need one bot per agent (5 total).

1. Open Telegram and search for @BotFather
2. Send /newbot
3. Enter a display name (e.g. Resume AI)
4. Enter a username ending in bot (e.g. myresume_ai_bot)
5. Copy the token BotFather gives you
6. Repeat 4 more times for each agent

IMPORTANT: For each bot, go to BotFather → /mybots → select the bot →
Bot Settings → Group Privacy → Turn Off
This lets the bot read all messages in the group.

---

## Step 2 — Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Click API Keys → Create Key
4. Copy it immediately (only shown once)

---

## Step 3 — Install Dependencies

Make sure Python 3.8+ is installed, then run:

  cd ai-team-bot
  pip install -r requirements.txt

---

## Step 4 — Add Your Keys

Rename .env.example to .env and fill in:

  TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
  ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

Then load them before running:

  Mac/Linux:  export $(cat .env | xargs)
  Windows:    set TELEGRAM_TOKEN=your_token && set ANTHROPIC_API_KEY=your_key

---

## Step 5 — Create Your Telegram Group

1. Create a new Telegram group
2. Add all 5 bots to the group
3. Give each bot Admin permissions

---

## Step 6 — Run the Bot

  python bot.py

You'll see:
  AI TEAM BOT — Starting up
  @ResumeBot  → Alex — Resume Specialist
  @ClientBot  → Sarah — Client Communications
  ... etc

---

## How to Use It

Tag any agent + your instruction:

  @ResumeBot Rewrite this resume for a Senior PM role at a Series B startup: [paste resume]

  @LinkedInBot Write a post about why 95% of resumes never get read by a human.

  @ResearchBot Analyze the top 10 resume gigs on Fiverr — pricing, packages, gaps I can exploit.

  @ClientBot Client wants a refund after 3 weeks with zero interviews. Write an empathetic reply
  that doesn't just give the money back.

  @FinanceBot I have 4 clients at $149/mo = $596 MRR. Build a specific 90-day plan to $8k/month.

---

## Run 24/7 Free (Optional)

Deploy to Railway (railway.app):
1. Push to GitHub
2. New Project → Deploy from GitHub
3. Add TELEGRAM_TOKEN and ANTHROPIC_API_KEY as env vars
4. Deploy — runs forever, no computer needed

---

## Add a New Agent

In bot.py, add to the AGENTS dict:

  "@YourBot": {
      "name": "emoji Name — Role",
      "system": "You are [Name]... your responsibilities... your style..."
  },

Restart the bot and it works immediately.

---

## Costs

  Telegram Bot API    Free
  Anthropic API       ~$5-25/month depending on volume
  Railway hosting     Free tier available

---

## Troubleshooting

Bot doesn't respond in group  → Turn OFF Group Privacy in BotFather for each bot
"Unauthorized" error          → Wrong TELEGRAM_TOKEN in your .env
"Invalid API key" error       → Wrong or expired ANTHROPIC_API_KEY
Responds in DMs not group     → Bot needs Admin rights in the group

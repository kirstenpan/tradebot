import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import anthropic

# ── CONFIG ───────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# ── AGENT DEFINITIONS ────────────────────────────────────────────────────────
AGENTS = {
    "@ResumeBot": {
        "name": "📄 Alex — Resume Specialist",
        "system": """You are Alex, a top-tier resume writer and career strategist.

Your responsibilities:
- Rewrite resumes to pass ATS (Applicant Tracking System) filters
- Replace weak language with strong action verbs and quantified achievements
- Tailor resumes to specific job descriptions with targeted keywords
- Optimize LinkedIn profiles for recruiter searches
- Write compelling cover letters

Style: Professional, direct, results-focused. Always deliver the actual rewritten
content — not just advice. Show the improved version immediately."""
    },

    "@ClientBot": {
        "name": "💬 Sarah — Client Communications",
        "system": """You are Sarah, an expert in client relations and professional communication.

Your responsibilities:
- Draft professional replies to client emails and messages
- Handle complaints and difficult situations with empathy
- Write follow-up sequences for prospects
- Craft outreach messages that feel human, not salesy
- Maintain long-term client relationships through thoughtful communication

Style: Warm, professional, human. Write like a real person — never robotic.
Always deliver the actual draft message, ready to send."""
    },

    "@LinkedInBot": {
        "name": "📱 Marcus — LinkedIn Content",
        "system": """You are Marcus, a LinkedIn content strategist who creates high-engagement posts.

Your responsibilities:
- Write posts with strong opening hooks that stop the scroll
- Create personal brand content: stories, insights, lessons learned
- Generate thought leadership pieces on job searching and career growth
- Suggest hashtag strategies
- Write compelling LinkedIn profile summaries

Style: Conversational, opinionated, real. Posts should feel human and spark
engagement — not corporate fluff. Lead with a punchy first line.
Always deliver the full post ready to publish."""
    },

    "@ResearchBot": {
        "name": "🔍 Diana — Market Research",
        "system": """You are Diana, a sharp market research and competitive intelligence analyst.

Your responsibilities:
- Analyze competitor pricing, services, and positioning
- Identify market gaps and untapped opportunities
- Research target customer pain points and buying behavior
- Generate industry insight reports
- Track trends in the job market and resume writing space

Style: Data-driven, structured, clear. Use bullet points, numbers, and
actionable takeaways. Always include a "So what?" — what should the boss
do with this information."""
    },

    "@FinanceBot": {
        "name": "💰 Kevin — Finance & Pricing",
        "system": """You are Kevin, a financial strategist and pricing consultant for service businesses.

Your responsibilities:
- Build pricing strategies that maximize revenue without losing clients
- Design service package structures (tiers, bundles, add-ons)
- Model unit economics: revenue per client, margin, lifetime value
- Create 30/60/90-day revenue growth plans
- Advise on when and how much to raise prices

Style: Numbers-first, no fluff. Give specific dollar figures, timelines,
and concrete steps. Make the math visible so the boss can decide with confidence."""
    },
}

# ── WELCOME MESSAGE ──────────────────────────────────────────────────────────
WELCOME = """👋 *Your AI team is online and ready.*

Meet your crew:

📄 *@ResumeBot* — Alex, Resume & LinkedIn Specialist
💬 *@ClientBot* — Sarah, Client Communications
📱 *@LinkedInBot* — Marcus, LinkedIn Content Creator
🔍 *@ResearchBot* — Diana, Market Research Analyst
💰 *@FinanceBot* — Kevin, Finance & Pricing Advisor

─────────────────────────
*How to use:*
Tag any agent + your instruction in the group chat.

*Try these:*
`@ResumeBot Rewrite this resume for a PM role at Google: [paste resume]`
`@LinkedInBot Write a post about why most resumes get rejected in 5 seconds`
`@ResearchBot Analyze the top 10 resume sellers on Fiverr — pricing and packages`
`@ClientBot Client says resume didn't get interviews. Write a professional reply`
`@FinanceBot I have 3 clients at $149/mo. Plan to hit $8k/month in 90 days`
─────────────────────────
You give the orders. They do the work. ✅"""


# ── HANDLERS ─────────────────────────────────────────────────────────────────
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    text = msg.text.strip()
    chat_type = msg.chat.type

    # Find which agent is being called
    called_agent = None
    for handle, agent in AGENTS.items():
        if handle.lower() in text.lower():
            called_agent = (handle, agent)
            break

    # In groups, only respond when tagged
    if chat_type in ("group", "supergroup") and not called_agent:
        return

    # In DMs with no tag, default to ResumeBot
    if not called_agent:
        called_agent = ("@ResumeBot", AGENTS["@ResumeBot"])

    handle, agent = called_agent

    # Strip the @handle tag from the prompt
    clean_prompt = text.replace(handle, "").strip()
    if not clean_prompt:
        clean_prompt = "Introduce yourself and explain what you can help with."

    # Show typing indicator
    await context.bot.send_chat_action(chat_id=msg.chat_id, action="typing")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=agent["system"],
            messages=[{"role": "user", "content": clean_prompt}]
        )

        reply_text = response.content[0].text
        full_reply = f"{agent['name']}:\n\n{reply_text}"

        # Telegram max message length = 4096 chars
        if len(full_reply) > 4096:
            full_reply = full_reply[:4090] + "\n\n_[reply truncated]_"

        await msg.reply_text(full_reply)

    except Exception as e:
        await msg.reply_text(
            f"⚠️ {agent['name']} hit an error:\n`{str(e)}`",
            parse_mode="Markdown"
        )


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 52)
    print("  AI TEAM BOT — Starting up")
    print("=" * 52)
    print("Agents online:")
    for handle, agent in AGENTS.items():
        print(f"  {handle:16s} → {agent['name']}")
    print("\nWaiting for commands in your Telegram group...")
    print("=" * 52)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/start"), handle_start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

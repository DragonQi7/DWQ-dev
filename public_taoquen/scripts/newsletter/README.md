# Newsletter Sender

A lightweight Python script to send branded HTML newsletters from a CSV subscriber list.

## Files

| File | Purpose |
|------|---------|
| `send_newsletter.py` | Main script |
| `subscribers.csv` | Your subscriber list |
| `newsletter_content.md` | Newsletter content (write here each issue) |
| `.env.example` | Copy to `.env` and fill in your credentials |
| `sent_log.csv` | Auto-created after first send — tracks who was sent what |
| `unsubscribed.csv` | Optional — one email per row, these are skipped |

## Quick Start

```powershell
# 1. Install dependencies (one-time)
pip install markdown python-dotenv

# 2. Set up credentials
Copy-Item .env.example .env
# then open .env and fill in your SMTP details

# 3. Write your newsletter in newsletter_content.md

# 4. Preview without sending
python send_newsletter.py --dry-run

# 5. Test send to yourself
python send_newsletter.py --test you@gmail.com

# 6. Send to everyone
python send_newsletter.py
```

## newsletter_content.md Format

The file uses a simple header block followed by Markdown body:

```
SUBJECT: Your Subject Line
PREVIEW: Short preview text shown in inbox (~90 chars)
ISSUE: 12

---

## Your Newsletter Headline

Body content in Markdown...
```

Everything below `---` is the email body. Standard Markdown works: `**bold**`, `*italic*`, `## headings`, `- lists`, `> blockquotes`, `[links](url)`.

## subscribers.csv Format

```
first_name,last_name,email,goal,subscribed_date,active
Sarah,Chen,sarah@example.com,stress relief,2025-01-10,true
```

- `email` is the only required column
- Set `active` to `false` to skip a subscriber without deleting them
- Any extra columns are ignored

## Command Options

```
--dry-run          Print list of recipients, don't send anything
--test EMAIL       Send to one address only (good for previewing)
--limit N          Send to first N subscribers only
--subscribers PATH Use a different CSV file
--content PATH     Use a different content file
```

## Windows / Emoji Note

If your newsletter content contains emoji and you get a `UnicodeEncodeError`, run:

```powershell
$env:PYTHONUTF8=1
python send_newsletter.py
```

## Gmail App Password

Gmail requires an App Password (not your regular password) when sending via SMTP:

1. Enable 2-Step Verification on your Google account
2. Go to **myaccount.google.com/apppasswords**
3. Create a new App Password → copy the 16-character code
4. Paste it as `SMTP_PASS` in your `.env` file

## Scaling Up

For more than ~500 emails/day, move to a dedicated sending service:

| Service | Free tier | Setup |
|---------|-----------|-------|
| SendGrid | 100/day free | Change `SMTP_HOST` to `smtp.sendgrid.net`, `SMTP_USER` = `apikey`, `SMTP_PASS` = your API key |
| Mailgun | 1,000/month free | Same SMTP approach |
| Amazon SES | 62,000/month (from EC2) | Cheapest at scale |
| ConvertKit | 10,000 subscribers free | Full ESP — handles unsubscribes, templates, automations |

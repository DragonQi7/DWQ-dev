"""
send_newsletter.py — Taoquen Newsletter Sender
═══════════════════════════════════════════════════════════════════════════
Reads a subscriber list from a CSV file, reads newsletter content from a
Markdown/text file, converts it to a beautiful branded HTML email, and
sends it to every subscriber.

SETUP (one-time)
────────────────
1. Install dependencies:
       pip install markdown python-dotenv

2. Create a .env file in this folder (copy from .env.example):
       SMTP_HOST=smtp.gmail.com
       SMTP_PORT=587
       SMTP_USER=you@gmail.com
       SMTP_PASS=your_app_password        ← NOT your Gmail login password
       FROM_NAME=Taoquen Wellness
       FROM_EMAIL=you@gmail.com
       REPLY_TO=you@gmail.com

   Gmail users: Enable 2FA → go to myaccount.google.com/apppasswords
                → create an "App Password" → paste that 16-char code as SMTP_PASS

   Other SMTP options — change SMTP_HOST / PORT:
       Outlook/Hotmail : smtp-mail.outlook.com  port 587
       Yahoo           : smtp.mail.yahoo.com     port 587
       Zoho Mail       : smtp.zoho.com           port 587
       SendGrid        : smtp.sendgrid.net        port 587  (SMTP_USER = "apikey", SMTP_PASS = your SendGrid API key)
       Mailgun         : smtp.mailgun.org         port 587

3. Edit subscribers.csv — one subscriber per row (see sample file).

4. Write your newsletter in newsletter_content.md (Markdown supported).

5. Run:
       python send_newsletter.py

   Or do a DRY RUN first (prints emails to console, sends nothing):
       python send_newsletter.py --dry-run

   Send to ONE address to preview before bulk send:
       python send_newsletter.py --test you@gmail.com

USAGE
─────
python send_newsletter.py                    # sends to full list
python send_newsletter.py --dry-run          # preview only, no send
python send_newsletter.py --test me@x.com   # send to one address only
python send_newsletter.py --limit 10         # send to first 10 only
═══════════════════════════════════════════════════════════════════════════
"""

import argparse
import csv
import os
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ── optional dependencies ────────────────────────────────────────────────
try:
    import markdown
except ImportError:
    markdown = None

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # .env loading skipped; set environment variables manually

# ════════════════════════════════════════════════════════════════
# CONFIG  — edit these paths if your files are in a different location
# ════════════════════════════════════════════════════════════════
HERE               = Path(__file__).parent
SUBSCRIBERS_FILE   = HERE / "subscribers.csv"
CONTENT_FILE       = HERE / "newsletter_content.md"
UNSUBSCRIBED_FILE  = HERE / "unsubscribed.csv"   # optional; emails to skip
SENT_LOG_FILE      = HERE / "sent_log.csv"        # auto-created on first send

# Delay between emails (seconds) — keeps you off spam lists
SEND_DELAY_SECONDS = 1.5

# ════════════════════════════════════════════════════════════════
# EMAIL BRAND TEMPLATE  — Taoquen palette
# ════════════════════════════════════════════════════════════════
BRAND = {
    "name"        : "Taoquen",
    "tagline"     : "Wellness · Ancient Wisdom · Modern Life",
    "primary"     : "#55160A",
    "accent"      : "#C02026",
    "bg"          : "#E9E4DA",
    "card_bg"     : "#FAF7F2",
    "text"        : "#1a0804",
    "text_muted"  : "#6b4030",
    "footer_text" : "#8a6050",
    "website"     : "https://taoquen.com",
    "unsubscribe_url": "https://taoquen.com/unsubscribe",   # replace with real URL
    "social_ig"   : "https://instagram.com/taoquen",
    "social_fb"   : "https://facebook.com/taoquen",
}


def build_html_email(
    subject: str,
    body_html: str,
    first_name: str = "",
    issue_number: str = "",
    preview_text: str = "",
) -> str:
    """
    Wraps the newsletter body in a fully self-contained HTML email template.
    Works in Gmail, Outlook, Apple Mail, mobile clients.
    """
    greeting = f"Hello {first_name}," if first_name else "Hello,"
    date_str  = datetime.now().strftime("%B %d, %Y")
    issue_str = f"Issue #{issue_number} · " if issue_number else ""

    return f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{subject}</title>
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
<style>
  body, #bodyTable {{ margin:0; padding:0; background:{BRAND['bg']}; }}
  body {{ font-family: Georgia, 'Times New Roman', serif; color:{BRAND['text']}; }}
  a {{ color:{BRAND['accent']}; }}
  p {{ margin:0 0 16px 0; line-height:1.75; }}
  h1,h2,h3 {{ font-family: Georgia, serif; color:{BRAND['primary']}; line-height:1.25; margin:0 0 12px; }}
  h2 {{ font-size:22px; }}
  h3 {{ font-size:17px; }}
  ul,ol {{ margin:0 0 16px; padding-left:20px; }}
  li {{ margin-bottom:6px; line-height:1.65; }}
  blockquote {{
    border-left:3px solid {BRAND['accent']};
    margin:24px 0; padding:12px 20px;
    background:{BRAND['bg']}; font-style:italic;
    color:{BRAND['text_muted']};
  }}
  hr {{ border:none; border-top:1px solid rgba(85,22,10,0.15); margin:28px 0; }}
  @media only screen and (max-width:600px) {{
    .email-body {{ padding:24px 20px !important; }}
    .email-header {{ padding:28px 20px !important; }}
  }}
</style>
</head>
<body>
<!-- Preview text (hidden in inbox preview) -->
<div style="display:none;max-height:0;overflow:hidden;color:{BRAND['bg']};">
{preview_text or subject}&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;‌&nbsp;
</div>

<table id="bodyTable" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:{BRAND['bg']};min-height:100vh;">
  <tr><td align="center" style="padding:32px 16px 0;">

    <!-- ── WRAPPER ── -->
    <table width="600" cellpadding="0" cellspacing="0" border="0"
           style="max-width:600px;width:100%;">

      <!-- ── HEADER ── -->
      <tr><td class="email-header"
              style="background:{BRAND['primary']};padding:36px 40px;border-radius:8px 8px 0 0;text-align:center;">
        <a href="{BRAND['website']}" style="text-decoration:none;">
          <p style="font-family:Georgia,serif;font-size:26px;font-weight:700;
                    letter-spacing:0.12em;color:#E9E4DA;margin:0;text-transform:uppercase;">
            {BRAND['name']}
          </p>
          <p style="font-size:11px;letter-spacing:0.2em;color:rgba(233,228,218,0.65);
                    margin:6px 0 0;text-transform:uppercase;font-family:Arial,sans-serif;">
            {BRAND['tagline']}
          </p>
        </a>
      </td></tr>

      <!-- ── ISSUE META ── -->
      <tr><td style="background:{BRAND['accent']};padding:10px 40px;text-align:center;">
        <p style="font-family:Arial,sans-serif;font-size:11px;font-weight:700;
                  letter-spacing:0.18em;text-transform:uppercase;color:#E9E4DA;margin:0;">
          {issue_str}{date_str}
        </p>
      </td></tr>

      <!-- ── BODY ── -->
      <tr><td class="email-body"
              style="background:{BRAND['card_bg']};padding:44px 48px;border-radius:0 0 8px 8px;">

        <!-- Greeting -->
        <p style="font-size:17px;color:{BRAND['text']};margin-bottom:28px;">{greeting}</p>

        <!-- Newsletter content inserted here -->
        {body_html}

        <!-- Divider before sign-off -->
        <hr>

        <!-- Sign-off -->
        <p style="font-size:15px;color:{BRAND['text']};">
          With warmth and wisdom,<br>
          <strong style="color:{BRAND['primary']};">The Taoquen Team</strong>
        </p>

      </td></tr>

      <!-- ── SOCIAL ROW ── -->
      <tr><td style="padding:28px 40px;text-align:center;">
        <p style="font-family:Arial,sans-serif;font-size:12px;
                  color:{BRAND['footer_text']};margin-bottom:12px;">
          Follow along:
        </p>
        <a href="{BRAND['social_ig']}"
           style="display:inline-block;margin:0 6px;padding:8px 16px;
                  background:{BRAND['primary']};color:#E9E4DA;border-radius:3px;
                  font-family:Arial,sans-serif;font-size:11px;font-weight:700;
                  letter-spacing:0.1em;text-decoration:none;text-transform:uppercase;">
          Instagram
        </a>
        <a href="{BRAND['social_fb']}"
           style="display:inline-block;margin:0 6px;padding:8px 16px;
                  background:{BRAND['primary']};color:#E9E4DA;border-radius:3px;
                  font-family:Arial,sans-serif;font-size:11px;font-weight:700;
                  letter-spacing:0.1em;text-decoration:none;text-transform:uppercase;">
          Facebook
        </a>
        <a href="{BRAND['website']}"
           style="display:inline-block;margin:0 6px;padding:8px 16px;
                  border:1px solid {BRAND['primary']};color:{BRAND['primary']};border-radius:3px;
                  font-family:Arial,sans-serif;font-size:11px;font-weight:700;
                  letter-spacing:0.1em;text-decoration:none;text-transform:uppercase;">
          Website
        </a>
      </td></tr>

      <!-- ── FOOTER ── -->
      <tr><td style="padding:0 40px 32px;text-align:center;
                     border-top:1px solid rgba(85,22,10,0.12);">
        <p style="font-family:Arial,sans-serif;font-size:11px;
                  color:{BRAND['footer_text']};line-height:1.6;margin-top:20px;">
          You're receiving this because you subscribed at {BRAND['website']}.<br>
          © {datetime.now().year} Taoquen · All rights reserved.<br><br>
          <a href="{BRAND['unsubscribe_url']}"
             style="color:{BRAND['footer_text']};text-decoration:underline;">
            Unsubscribe
          </a>
          &nbsp;·&nbsp;
          <a href="{BRAND['website']}/privacy"
             style="color:{BRAND['footer_text']};text-decoration:underline;">
            Privacy Policy
          </a>
        </p>
      </td></tr>

    </table>
  </td></tr>
</table>
</body>
</html>"""


# ════════════════════════════════════════════════════════════════
# CONTENT READER
# ════════════════════════════════════════════════════════════════
def read_content(filepath: Path) -> tuple[str, str, str, str]:
    """
    Reads the newsletter content file.
    Returns (subject, preview_text, issue_number, body_html).

    The file format uses a simple front-matter block at the top:

        SUBJECT: Your Email Subject Line Here
        PREVIEW: Short preview shown in inbox (max ~90 chars)
        ISSUE: 12

        --- (three dashes = end of front-matter, start of body)

        ## Your Newsletter Headline

        The body goes here in plain Markdown...
    """
    raw = filepath.read_text(encoding="utf-8")

    subject      = "Taoquen Weekly Wellness"
    preview_text = ""
    issue_number = ""
    body_raw     = raw

    if raw.startswith(("SUBJECT:", "Subject:")):
        lines = raw.splitlines()
        body_lines = []
        in_body = False
        for line in lines:
            if in_body:
                body_lines.append(line)
            elif line.strip() == "---":
                in_body = True
            elif line.upper().startswith("SUBJECT:"):
                subject = line.split(":", 1)[1].strip()
            elif line.upper().startswith("PREVIEW:"):
                preview_text = line.split(":", 1)[1].strip()
            elif line.upper().startswith("ISSUE:"):
                issue_number = line.split(":", 1)[1].strip()
        body_raw = "\n".join(body_lines).strip()

    # Convert Markdown → HTML (if library available), else use plain text
    if markdown and (str(filepath).endswith(".md") or "##" in body_raw or "**" in body_raw):
        body_html = markdown.markdown(
            body_raw,
            extensions=["extra", "nl2br"],
        )
    else:
        # Fallback: wrap paragraphs in <p> tags
        paragraphs = [p.strip() for p in body_raw.split("\n\n") if p.strip()]
        body_html  = "\n".join(f"<p>{p}</p>" for p in paragraphs)

    return subject, preview_text, issue_number, body_html


# ════════════════════════════════════════════════════════════════
# SUBSCRIBER LIST READER
# ════════════════════════════════════════════════════════════════
def load_subscribers(filepath: Path) -> list[dict]:
    """
    Reads subscribers.csv.
    Required column: email
    Optional columns: first_name, last_name, goal, subscribed_date, active
    """
    if not filepath.exists():
        print(f"ERROR: Subscribers file not found: {filepath}")
        sys.exit(1)

    subscribers = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Normalise column names to lowercase
        for row in reader:
            norm = {k.lower().strip(): v.strip() for k, v in row.items()}
            email = norm.get("email", "").strip().lower()
            if not email or "@" not in email:
                continue
            # Skip if active column exists and is explicitly "false" / "no" / "0"
            active = norm.get("active", "true").lower()
            if active in ("false", "no", "0", "n"):
                continue
            subscribers.append(norm)

    return subscribers


def load_unsubscribed(filepath: Path) -> set[str]:
    if not filepath.exists():
        return set()
    emails = set()
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                emails.add(row[0].strip().lower())
    return emails


# ════════════════════════════════════════════════════════════════
# SMTP SENDER
# ════════════════════════════════════════════════════════════════
def get_smtp_config() -> dict:
    config = {
        "host"  : os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port"  : int(os.getenv("SMTP_PORT", "587")),
        "user"  : os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASS", ""),
        "from_name" : os.getenv("FROM_NAME", BRAND["name"]),
        "from_email": os.getenv("FROM_EMAIL", ""),
        "reply_to"  : os.getenv("REPLY_TO", ""),
    }
    if not config["user"] or not config["password"]:
        print("\nERROR: SMTP credentials not set.")
        print("Create a .env file in this folder with:")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USER=you@gmail.com")
        print("  SMTP_PASS=your_app_password\n")
        sys.exit(1)
    return config


def send_one_email(
    smtp_conn: smtplib.SMTP,
    cfg: dict,
    to_email: str,
    to_name: str,
    subject: str,
    html_body: str,
    text_body: str,
) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{cfg['from_name']} <{cfg['from_email']}>"
    msg["To"]      = f"{to_name} <{to_email}>" if to_name else to_email
    if cfg.get("reply_to"):
        msg["Reply-To"] = cfg["reply_to"]

    # Attach plain-text version first (fallback for old clients)
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    # Attach HTML version (clients prefer this)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        smtp_conn.sendmail(cfg["from_email"], to_email, msg.as_string())
        return True
    except smtplib.SMTPException as e:
        print(f"  ✗  Failed to send to {to_email}: {e}")
        return False


# ════════════════════════════════════════════════════════════════
# SENT LOG
# ════════════════════════════════════════════════════════════════
def log_sent(filepath: Path, email: str, subject: str, status: str):
    is_new = not filepath.exists()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp", "email", "subject", "status"])
        writer.writerow([datetime.now().isoformat(), email, subject, status])


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Taoquen Newsletter Sender")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print emails to console only — do not send")
    parser.add_argument("--test", metavar="EMAIL",
                        help="Send to this one address only (preview send)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Only send to first N subscribers")
    parser.add_argument("--subscribers", default=str(SUBSCRIBERS_FILE),
                        help="Path to subscribers CSV file")
    parser.add_argument("--content", default=str(CONTENT_FILE),
                        help="Path to newsletter content file")
    args = parser.parse_args()

    # ── Load content ────────────────────────────────────────
    content_path = Path(args.content)
    if not content_path.exists():
        print(f"ERROR: Content file not found: {content_path}")
        sys.exit(1)

    subject, preview_text, issue_number, body_html = read_content(content_path)
    print(f"\n{'═'*60}")
    print(f"  Newsletter: {subject}")
    print(f"  Issue     : {issue_number or '(not set)'}")
    print(f"  Content   : {content_path.name}")
    print(f"{'═'*60}")

    # ── Load subscribers ────────────────────────────────────
    if args.test:
        subscribers = [{"email": args.test, "first_name": "Subscriber"}]
        print(f"\n  TEST MODE → sending only to: {args.test}")
    else:
        subscribers  = load_subscribers(Path(args.subscribers))
        unsubscribed = load_unsubscribed(UNSUBSCRIBED_FILE)
        subscribers  = [s for s in subscribers if s["email"] not in unsubscribed]
        if args.limit:
            subscribers = subscribers[:args.limit]

    total = len(subscribers)
    print(f"\n  Subscribers to send to: {total}")

    if total == 0:
        print("  Nothing to send. Exiting.")
        sys.exit(0)

    if args.dry_run:
        print("\n  DRY RUN — no emails will be sent.\n")
        for i, sub in enumerate(subscribers, 1):
            print(f"  [{i:>4}] {sub['email']:<40} ({sub.get('first_name', '')})")
        print(f"\n  Would have sent {total} emails. Run without --dry-run to send.")
        return

    # ── Confirm before bulk send ─────────────────────────────
    if not args.test and total > 1:
        confirm = input(f"\n  Ready to send to {total} subscribers. Continue? [y/N]: ").strip().lower()
        if confirm != "y":
            print("  Cancelled.")
            sys.exit(0)

    # ── Connect SMTP and send ────────────────────────────────
    cfg = get_smtp_config()
    sent_ok  = 0
    sent_err = 0

    print(f"\n  Connecting to {cfg['host']}:{cfg['port']} ...\n")

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"]) as server:
            server.ehlo()
            server.starttls()
            server.login(cfg["user"], cfg["password"])
            print(f"  Connected ✓\n")

            for i, sub in enumerate(subscribers, 1):
                email      = sub["email"]
                first_name = sub.get("first_name", "").strip().title()

                # Personalise the HTML for this subscriber
                html = build_html_email(
                    subject      = subject,
                    body_html    = body_html,
                    first_name   = first_name,
                    issue_number = issue_number,
                    preview_text = preview_text,
                )

                # Plain text fallback (strip HTML tags roughly)
                import re
                plain = re.sub(r"<[^>]+>", "", body_html)
                plain = f"Hello {first_name},\n\n{plain}\n\nWith warmth,\nThe Taoquen Team"

                ok = send_one_email(server, cfg, email, first_name, subject, html, plain)
                status = "sent" if ok else "error"
                log_sent(SENT_LOG_FILE, email, subject, status)

                if ok:
                    sent_ok += 1
                    print(f"  ✓  [{i:>4}/{total}]  {email}")
                else:
                    sent_err += 1

                if i < total:
                    time.sleep(SEND_DELAY_SECONDS)

    except smtplib.SMTPAuthenticationError:
        print("\n  ERROR: Authentication failed.")
        print("  For Gmail: use an App Password, not your regular Gmail password.")
        print("  Go to: myaccount.google.com/apppasswords\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n  ERROR: {e}\n")
        sys.exit(1)

    print(f"\n{'═'*60}")
    print(f"  Done!  ✓ Sent: {sent_ok}   ✗ Failed: {sent_err}")
    print(f"  Log saved to: {SENT_LOG_FILE}")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()

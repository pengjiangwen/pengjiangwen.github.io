---
title: "Why Your Email Goes to Spam (And How to Fix It)"
date: "2026-11-19T19:59:10Z"
description: "Your email landing in spam isn't random. Learn the real technical reasons—from SPF and DKIM failures to spam traps—and exact steps to fix delivery."
tags: ["smartphones", "security-privacy", "networking"]
categories: ["tech"]
draft: false
---
## Introduction

You hit send. Twenty minutes later you check the Sent folder, then the Inbox, then—nothing. The recipient says it never arrived. You check your own spam folder and there it is: your own message, sitting in quarantine next to a phishing scam and a newsletter you unsubscribed from two years ago.

This happens to small businesses every day, and the diagnosis is almost never "the internet hates you." Email delivery is a scoring contest run by machines. Gmail, Outlook, and Yahoo each run your message through dozens of checks in under a second, then assign it a probability of being junk. Miss enough checks and you get filtered. The good news: nearly every failure has a specific, fixable cause.

Here's what's actually happening and how to find it.

## The Three Authentication Records Most People Get Wrong

Before content even matters, your message has to prove it came from you. That proof comes from three DNS records: SPF, DKIM, and DMARC. If you don't know whether yours are set up, that's probably your problem.

**SPF (Sender Policy Framework)** is a list of servers allowed to send mail for your domain. It lives as a TXT record in DNS. The classic mistake: you set up SPF for your web host, then start sending through a sales platform, a help desk, and a booking system—none of which are in the record. Every message from those tools fails SPF. You're allowed exactly one SPF record per domain, so you can't just add a second one; you have to merge everything into a single record with the `include:` mechanism.

**DKIM (DomainKeys Identified Mail)** attaches a cryptographic signature to each message. It's usually a TXT record like `selector._domainkey.yourdomain.com`. When you set up a new sending tool, it almost always gives you a DKIM record to add. People skip this step constantly. A message with a valid DKIM signature is dramatically more likely to reach the inbox.

**DMARC** tells receiving servers what to do when SPF or DKIM fails, and it sends you reports. Start with `v=DMARC1; p=none; rua=mailto:you@yourdomain.com` to collect data for two to four weeks, then move to `p=quarantine`. Without DMARC, Gmail and Yahoo have been far stricter since their 2024 bulk sender rules kicked in—and even for low-volume senders, a missing DMARC policy is a red flag.

**The 30-minute check:** Go to a free header analyzer (Google's "Check the headers" tool or MXToolbox's header analyzer), send yourself a test email, and paste the raw headers in. Look for `spf=pass`, `dkim=pass`, and `dmarc=pass`. If any say "fail" or "none," stop reading and fix that first. Nothing else matters until authentication is clean.

## Your Sending Domain Is Probably Brand New—and That Matters

A domain registered last Tuesday has no reputation. Receiving servers treat new domains with suspicion because spammers burn through domains constantly. If you bought `yourbrand-shop.com` three weeks ago and started sending 500 emails a week, you're asking a stranger for a favor.

The fix is a warm-up: send small volumes first—20 to 50 emails a day to your most engaged contacts—and increase gradually over two to four weeks. Open rates and replies during warm-up matter. If your first 200 emails get opened and replied to, you've built credibility. If they get marked as spam, you've dug a hole that takes months to climb out of.

Also check your domain age and history. A domain that previously belonged to someone who sent spam carries that baggage. Run it through a reputation tool like Google Postmaster Tools (free, but requires a verified domain) or MXToolbox's blacklist check. If you're on a blacklist like Spamhaus SBL or Barracuda, most receiving servers will reject or filter you outright until you request delisting—a process that typically takes 24 to 72 hours and requires you to fix the underlying cause first.

## The Content Mistakes That Trigger Filters

Filters read your subject line, your body, your links, and your images. Some patterns are near-guaranteed triggers.

**Link problems.** A single email with 15 links to the same domain looks like a phishing template. So does a link whose visible text says `yourbank.com` but points to a different domain—filters compare the two and flag mismatches. Use a link shortener sparingly; some are on shared blocklists because spammers abuse them.

**Image-heavy emails with little text.** A 600-pixel-wide image with one line of text underneath is the classic spam shape. Keep a healthy text-to-image ratio—roughly 60% text or more—and always include alt text.

**Spammy phrasing.** "Act now," "risk-free," "guaranteed," "limited time," excessive exclamation marks, ALL CAPS subject lines, and red text all add points. One or two won't sink you. Five together will.

**The attachment trap.** Executable files (.exe, .scr, .bat) and password-protected ZIPs are effectively banned by most filters. PDFs are fine but keep them under 5 MB; many corporate gateways reject anything larger.

**The subject line mistake nobody talks about:** writing a subject that doesn't match the body. Filters compare them. A subject saying "Invoice attached" with no invoice mentioned inside is a mismatch signal.

## A Step-by-Step Diagnostic Checklist

Work through this in order. Don't skip ahead—later steps assume earlier ones pass.

1. **Send a test to a Gmail address you control.** Open it, click the three-dot menu, and choose "Show original." Read the SPF, DKIM, and DMARC lines.
2. **Send the same message to a Outlook/Hotmail address.** Microsoft's filters are stricter than Google's and catch different problems.
3. **Run your domain through MXToolbox's blacklist checker.** Any listing means fix that first.
4. **Check Google Postmaster Tools.** If you have any volume, it shows your spam rate. Anything above 0.1% is a warning; above 0.3% is a serious problem.
5. **Inspect your DNS records manually.** Run `dig TXT yourdomain.com` (or use a free DNS lookup tool) and confirm you have exactly one SPF record, a DKIM record for each sending tool, and a DMARC record.
6. **Test the content.** Paste your email into a free spam checker like Mail-Tester (it gives you a score out of 10) or GlockApps. A score below 8 means content issues.
7. **Check your sending infrastructure.** Are you sending marketing email from a shared host's default mail server? That server's IP reputation is shared with everyone else on it—including spammers. This alone explains a huge share of small-business deliverability failures.
8. **Look at your list hygiene.** When did you last remove hard bounces? Are you emailing people who signed up three years ago and never opened anything? Inactive addresses are the single biggest driver of spam complaints.

## What Most Guides Get Wrong

**Myth 1: "Just ask people to whitelist you."** Whitelisting barely exists anymore. Gmail retired its old whitelist program years ago, and modern filters weigh engagement—opens, replies, moves out of spam—far more heavily than any manual approval. Telling subscribers to "add us to your contacts" is harmless advice but won't rescue a failing sender.

**Myth 2: "Spam filters are keyword-based."** Modern filters are mostly machine-learning models trained on user behavior. They care about whether recipients open, reply, delete, or report your mail—not whether you wrote "free." That's why two nearly identical emails can land in different folders: the difference is who engaged with them.

**Myth 3: "Buying an email list is fine if it's opt-in."** A purchased list is never truly opt-in to *you*. The recipients never chose your brand, so they mark you as spam at rates that will wreck your reputation within weeks. One 10,000-address list can take a year to recover from.

**The mistake almost everyone makes:** ignoring complaints. A spam complaint rate of even 0.5% sounds tiny, but it's ten times the threshold where Gmail starts throttling you. If 5 out of 1,000 recipients hit "Report spam," your next campaign is in trouble. Make unsubscribing a one-click process and honor it instantly—delays generate complaints.

## When It's Not You: Shared IPs and Recipient-Side Rules

Sometimes your setup is flawless and the message still gets filtered. Two possibilities.

**Shared IP reputation.** If you send through a budget host or a shared marketing platform, your messages go out from an IP shared with thousands of other senders. If a few of them spam, everyone on that IP suffers. Ask your provider whether you're on a dedicated IP (usually $20–$50/month extra) and whether their IP pools are monitored. For low-volume senders, a dedicated IP can actually hurt—it has no reputation of its own—so shared is fine if the provider is reputable.

**Recipient-side rules.** The person you're emailing may have a personal filter, a corporate gateway like Barracuda or Proofpoint, or an aggressive spam setting. Corporate gateways are notoriously strict; a legitimate invoice from a new vendor often lands in quarantine. There's nothing you can fix on your end except authentication and reputation. Ask the recipient to check their quarantine and mark you as safe—which, unlike public whitelists, does work at the individual level.

## The Fix That Takes the Longest but Works Best

Deliverability is a reputation game, and reputation is built on engagement. The single most effective long-term fix is sending mail people actually want to their inboxes—and stopping everything else.

That means segmenting your list by engagement, suppressing anyone who hasn't opened an email in 6 to 12 months, and never emailing a purchased list. It means making unsubscribe easy and honoring it immediately. It means sending from a consistent domain and IP, not rotating through whatever tool is cheapest this month.

Do the technical work first—authentication, DNS, blacklist checks—because that's binary. Then treat every send as a reputation transaction. Recipients who open, reply, and never complain are your strongest deliverability asset. Recipients who ignore you are a liability, and filters know the difference.

## Related Reading

- [How to Secure Your Home WiFi: A Practical Guide](https://pengjiangwen.github.io/tech/how-to-secure-your-home-wifi-a-practical-guide/)
- [How to Transfer Photos to Computer: 5 Fast Methods](https://pengjiangwen.github.io/tech/how-to-transfer-photos-to-computer-5-fast-methods/)
- [How to Clean Your PC Fans in 20 Minutes or Less](https://pengjiangwen.github.io/tech/how-to-clean-your-pc-fans-in-20-minutes-or-less/)


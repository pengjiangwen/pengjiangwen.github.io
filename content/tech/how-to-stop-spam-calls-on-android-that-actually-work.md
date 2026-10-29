---
title: "How to Stop Spam Calls on Android (That Actually Work)"
date: "2026-10-29T18:04:16Z"
description: "Tired of spam calls? Learn how to block them on Android using carrier filters, Google's tools, and settings most people miss. Real fixes, no fluff."
tags: ["smartphones"]
categories: ["tech"]
draft: false
---
## Introduction

My phone buzzed at 6:47 on a Tuesday morning. The screen showed a local number — same area code, same prefix as my own cell. I answered. A recorded voice told me my "vehicle warranty" had expired. I don't own a car.

That was the third spam call in 48 hours. If your Android phone rings more often from strangers than from people you actually know, you're in the same boat as most people with a phone number. The good news: Android has real, working tools to shut this down. The bad news: most guides tell you to install an app and call it a day, which fixes maybe half the problem.

Here's what actually works, in the order I'd do it.

## First, understand why blocking one number does nothing

Spam callers don't dial from a single phone. They use VoIP systems that rotate through thousands of numbers, often spoofing your own area code and prefix so the call looks local. Block one number and you'll see a different one tomorrow. This is why manually blocking numbers feels like bailing out a boat with a teaspoon.

The fix has to happen at the network or system level, before the call reaches your ringer. Everything below works that way.

## Step 1: Turn on your carrier's free spam filter (do this first)

All three major US carriers offer free spam call blocking, and most people never turn it on. It works at the network level, so it catches calls before your phone even sees them.

**Verizon:** Open the My Verizon app, go to Account > Blocks, and enable "Verizon Call Filter." The free tier blocks suspected spam and shows a spam risk level on incoming calls. The paid tier ($3.99/month per line) adds caller name ID and a personal block list. You can also dial `*611` and ask a rep to enable it.

**AT&T:** Dial `*61` from your phone, or use the AT&T Call Protect app. The free version blocks fraud calls automatically and labels suspected spam. The paid tier ($3.99/month) adds reverse number lookup.

**T-Mobile:** Scam Shield is free and includes Scam Block, which you enable by dialing `#662#` and pressing call. You'll get a confirmation text. To check it's on, dial `#632#`. T-Mobile also gives you a free second number through the Scam Shield app if you want a clean line for signups.

If you're on a smaller carrier or an MVNO like Mint Mobile or Visible, check their support pages — many piggyback on the major networks' filters but don't advertise it.

This step alone typically cuts spam calls by more than half. Do it before anything else.

## Step 2: Use Google's built-in caller ID and spam protection

Google Phone (the default dialer on Pixel phones and many others) has a spam filter that's genuinely good, and it's free. Here's how to check it's on:

1. Open the Phone app.
2. Tap the three-dot menu in the top right.
3. Tap **Settings** > **Caller ID & spam**.
4. Turn on **"Filter spam calls."**

With this on, calls Google identifies as spam won't ring your phone at all — they go straight to voicemail and show up in your call history with a "Suspected spam" label. You can also turn on "Verified calls," which shows a business's name and logo when a legitimate company calls.

One caveat: this only works if Google Phone is your default dialer app. Samsung phones use Samsung's dialer by default, which has its own spam protection (Settings > Call settings > Caller ID and spam protection). Both work fine — just make sure one of them is actually on.

## Step 3: Enable "Silence unknown callers" — but understand the tradeoff

Both Google Phone and Samsung's dialer have a setting that sends any call from a number not in your contacts straight to voicemail without ringing.

On Google Phone: Settings > **Silence unknown callers**.
On Samsung: Phone app > Settings > **Block numbers** > toggle on **"Block unknown callers."**

This is the nuclear option, and it works. But it has a real cost: your doctor's office calling from a new number, a delivery driver, a school nurse — all go to voicemail. If you run a business or have kids in school, this setting will frustrate you within a week.

My recommendation: turn it on for a trial period, see what you miss, and decide. Many people find the tradeoff worth it. If you can't risk it, skip to Step 4.

## Step 4: Set up Do Not Disturb as a spam backstop

This is the trick most guides skip. You can configure Do Not Disturb to silence calls from anyone not in your contacts during specific hours — say, 9 PM to 7 AM — while still letting favorites and repeat callers through.

On most Android phones: Settings > **Sound & vibration** > **Do Not Disturb** > **People** > **Calls** > select **"Contacts only."** Then set a schedule under "Turn on automatically."

The repeat-caller exception matters: if someone calls twice within 15 minutes, the second call rings through. That's how a real emergency gets past the filter while a spam bot dialing once gets silenced.

## Step 5: Report and block — but do it strategically

When a spam call does get through, don't just hang up. In the Google Phone app, long-press the call in your history and tap **"Block/report spam."** This feeds Google's spam database and helps flag the number for everyone else. It takes four seconds and has a compounding effect.

Don't bother blocking numbers one at a time in your settings menu — as covered above, the numbers rotate. Reporting is more useful than blocking because it trains the system.

## The checklist version

If you want the short version, here's the order:

- [ ] Enable your carrier's free spam filter (Verizon Call Filter, AT&T Call Protect, or T-Mobile Scam Shield via `#662#`)
- [ ] Confirm Google Phone or Samsung's caller ID and spam protection is turned on
- [ ] Decide whether "Silence unknown callers" is worth the tradeoff for you
- [ ] Set up Do Not Disturb with a contacts-only exception and a repeat-caller override
- [ ] Report every spam call that slips through instead of just blocking it
- [ ] Never press a key or say "yes" to an automated caller — that confirms your number is live

That last point deserves its own section.

## The mistake almost everyone makes: interacting with the bot

Pressing "1 to be removed from our list" does the opposite. It tells the spam operation that a real human answers this number, which makes your number more valuable and gets it sold to other lists. Same with saying "hello" and waiting — voice-recognition bots log your response.

The correct move on a suspected spam call: hang up without a word. Don't press anything. Don't call back. If you answer by accident, end the call silently.

There's a related myth worth killing: that answering and asking to be removed is legally protected. It isn't in any practical sense — the FTC's Do Not Call Registry covers legitimate telemarketers, but most spam calls come from operations that ignore it entirely, often from overseas. The registry is still worth using (donotcall.gov, takes two minutes), but treat it as a filter for legal marketers, not a shield against scammers.

## What most guides get wrong

**They tell you to install a third-party call blocker app as step one.** Most of these apps want broad permissions, some show ads, and the free tiers are limited. Your carrier filter plus Google's built-in tools cover the vast majority of spam for $0. Third-party apps like Truecaller can help, but they're a supplement, not a starting point — and Truecaller's free tier now shows ads and its caller ID database has had privacy questions raised about how it builds its directory.

**They ignore the spoofing problem.** A guide that says "block the number" misunderstands how modern spam works. Numbers rotate constantly. Blocking individual numbers is almost pure theater unless you're dealing with one persistent harasser, which is a different problem.

**They don't mention that spam texts need separate handling.** Robocalls and spam texts are different pipelines. On Google Messages, you can enable spam protection under Settings > **Spam protection** (it uses on-device filtering). Texts from unknown senders get moved to a spam folder rather than your inbox. If you're getting hammered by texts, that setting matters as much as anything above.

## A realistic expectation

After running through these steps, my own spam calls dropped from roughly a dozen a week to one or two — and the ones that get through are usually new numbers the filters haven't learned yet. You won't hit zero. Spam calling is an arms race, and the filters play catch-up.

But the difference between doing nothing and doing the five steps above is enormous. The carrier filter is the biggest single win, and it takes about 90 seconds. Start there tonight, before the next 6:47 AM call.

## Related Reading

- [How to Transfer Files from PC to Phone: 7 Reliable Methods](https://pengjiangwen.github.io/tech/how-to-transfer-files-from-pc-to-phone-7-reliable-methods/)
- [Android vs iOS: Which OS Wins in 2024?](https://pengjiangwen.github.io/tech/android-vs-ios-which-os-wins-in-2024/)
- [Best Android Phones for Seniors in 2025: Easy & Reliable](https://pengjiangwen.github.io/tech/best-android-phones-for-seniors-in-2025-easy-reliable/)


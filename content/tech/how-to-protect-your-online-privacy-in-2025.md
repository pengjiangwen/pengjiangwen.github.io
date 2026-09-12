---
title: "How to Protect Your Online Privacy in 2025"
date: "2026-09-12T14:44:06Z"
description: "Practical steps to protect your online privacy, from password managers to browser hardening, plus the data brokers quietly selling your info."
tags: ["online privacy", "cybersecurity", "data protection"]
categories: ["tech"]
draft: false
---
## Introduction

In 2019, a security researcher bought a used photocopier from a government surplus auction. The machine's hard drive still contained thousands of scanned documents, including sensitive records that should have been destroyed years earlier. The lesson wasn't about the copier. It was about how much data we leave behind without realizing it — and how little control we have over where it ends up.

Most people assume their online privacy is already gone, so there's no point trying. That's exactly what data brokers, ad networks, and lax companies are counting on. The truth is that privacy isn't a switch you flip. It's a series of small, deliberate decisions that, stacked together, make you a much harder target. Here's how to actually do it.

## Start With the Foundation: Passwords and Authentication

### Use a Password Manager (Seriously)

If you're reusing passwords across sites — and roughly 60% of people do — one breach anywhere can cascade into a breach everywhere. A password manager like Bitwarden, 1Password, or KeePass generates and stores unique passwords for every account.

The objection is always the same: "What if the manager gets hacked?" Reputable managers store your vault encrypted with a key derived from your master password, which they never see. It's a far smaller risk than using "Summer2024!" on twelve different sites.

### Turn On Two-Factor Authentication

Two-factor authentication (2FA) blocks the overwhelming majority of automated account takeovers. But not all 2FA is equal:

- **SMS codes** are better than nothing but vulnerable to SIM-swapping attacks.
- **Authenticator apps** (Google Authenticator, Authy) are significantly stronger.
- **Hardware keys** like a YubiKey are the gold standard, and many services now support them.
- **Passkeys** are increasingly replacing passwords entirely and are phishing-resistant by design.

Start with your email account. If someone controls your email, they can reset the password on almost everything else you own.

## Harden Your Browser

Your browser is where most of your tracking exposure happens. A few changes go a long way.

### Switch to a Privacy-Focused Browser

Brave, Firefox (with strict tracking protection enabled), and Mullvad Browser all block trackers by default. If you prefer Chrome, at least install uBlock Origin — though note Google's Manifest V3 changes have weakened ad-blocking extensions in Chrome, which is its own reason to consider switching.

### Adjust the Settings That Matter

- Set tracking protection to "strict."
- Block third-party cookies.
- Disable "precise location" access for any site that doesn't genuinely need it.
- Clear cookies on exit, or use container tabs to isolate sessions.

### Consider a Privacy-Respecting Search Engine

DuckDuckGo and Startpage don't build profiles of your searches. Google does — and that profile is one of the most detailed portraits of you that exists anywhere.

## Reduce What You Leak

### Your Email Address Is a Tracking Beacon

Every time you type your email into a signup form, you're creating another data point that can be sold, leaked, or used to link your activity across services. Use email aliasing to stay ahead of it:

- **Apple's Hide My Email** (iCloud+ subscribers)
- **Firefox Relay**
- **SimpleLogin** or **DuckDuckGo Email Protection**

Each service gets a unique alias. If one starts receiving spam, you know exactly who leaked or sold your address — and you can kill that alias instantly.

### Lock Down Social Media

Social platforms are designed to extract as much personal data as possible. You don't have to quit them, but you should:

- Set your profile to private or friends-only.
- Review which third-party apps have access to your account and revoke the ones you don't use.
- Avoid posting your location in real time, your pet's name, your mother's maiden name, or anything else commonly used as a security question.
- Check Facebook's "Off-Facebook Activity" tool, which shows how many sites and apps are feeding data back to Meta. The number is usually shocking.

### Audit App Permissions on Your Phone

Open your phone's settings and look at which apps have access to your microphone, camera, contacts, and location. A flashlight app doesn't need any of them. Revoke aggressively.

## Deal With Data Brokers

This is the part most privacy guides skip, and it's arguably the most important.

Data brokers like Acxiom, LexisNexis, and Spokeo compile profiles on hundreds of millions of people and sell them to marketers, insurers, and anyone else willing to pay. Your home address, phone number, relatives, and purchase history are often available for a few dollars.

### How to Fight Back

1. **Opt out directly.** Major brokers are required by law (in some jurisdictions) to honor opt-out requests. The process is tedious — often a form or email per broker.
2. **Use a removal service.** Services like DeleteMe or Kanary handle the opt-outs for you for a fee. Worth it if you don't want to spend hours on it.
3. **Check what's already public.** Search your name and phone number on Google periodically. If a people-search site has your address, request removal.

California's CCPA and similar laws in other states give you the legal right to demand deletion in many cases. Use it.

## Encrypt What You Can

### Use a VPN on Untrusted Networks

Public Wi-Fi at airports and coffee shops can expose your traffic to anyone on the same network. A reputable VPN (Mullvad, Proton VPN, IVPN) encrypts your connection. Skip the free ones — if you're not paying, your browsing data is often the product.

### Encrypt Your Messages

Signal and WhatsApp both use end-to-end encryption. Regular SMS does not. For sensitive conversations, move them to an encrypted app.

### Turn On Full-Disk Encryption

Both iOS and Android encrypt your device by default when you set a passcode. On Windows, enable BitLocker. On Mac, FileVault. This means a stolen laptop or phone is a paperweight to a thief, not a data goldmine.

## The Mindset Shift

Perfect privacy isn't achievable, and chasing it completely will make you miserable. The goal is asymmetry: make yourself more expensive to track than the next person. Every step here raises the cost of surveilling you.

Start with the highest-impact changes — a password manager, 2FA on your email, a privacy browser, and email aliases. Those four alone will eliminate the majority of casual tracking and dramatically reduce your breach risk. Then add layers as you have time.

Privacy isn't about having something to hide. It's about having something to protect: your autonomy, your finances, and your ability to live without being profiled, predicted, and sold.

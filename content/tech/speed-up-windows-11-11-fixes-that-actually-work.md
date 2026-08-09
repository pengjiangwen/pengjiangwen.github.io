---
title: "Speed Up Windows 11: 11 Fixes That Actually Work"
date: "2026-08-09T12:34:45Z"
description: "Is your PC lagging? Stop guessing. These 11 proven tweaks—from startup apps to power settings—will make Windows 11 feel brand new."
tags: ["windows 11 performance", "speed up pc", "windows optimization", "tech tips"]
categories: ["tech"]
draft: false
---
TITLE: Speed Up Windows 11: 11 Fixes That Actually Work
DESCRIPTION: Is your PC lagging? Stop guessing. These 11 proven tweaks—from startup apps to power settings—will make Windows 11 feel brand new.
TAGS: windows 11 performance, speed up pc, windows optimization, tech tips

## Introduction

Let’s be honest: Windows 11 is beautiful, but it can be a resource hog. I remember the day I upgraded my trusty Dell XPS 13—within a week, the fan was roaring like a jet engine, and opening Chrome felt like waiting for a dial-up connection. The culprit wasn't the OS itself; it was the accumulation of startup junk, background bloatware, and power settings tuned for "looks" rather than "go."

You don’t need a new laptop. You don’t need to disable security features (please don’t). You need to strip away the fat. After tweaking my own machines and a few friends' desktops, I’ve narrowed down the fixes that deliver the biggest performance gains with the least risk. Here’s my no-nonsense playbook to speed up Windows 11.

## 1. Kill the Startup Zombies (The #1 Free Win)

Open Task Manager (Ctrl + Shift + Esc) and click "Startup apps." Look at the "Status" and "Impact" columns. If you see **Spotify**, **Discord**, **Adobe Updater**, or anything from **Microsoft Teams** set to "High Impact," those are your zombies. They wake up when you log in and eat RAM in the background.

**Action:** Right-click every non-essential app and select "Disable." You don't need Steam auto-launching unless you game the second you boot. This single step cuts boot time by 30-50% on older hard drives and significantly reduces lag after login.

**Pro tip:** You can still open these apps manually. Disabling startup doesn't uninstall them—it just makes them wait until you actually need them.

## 2. Turn Off "Startup Boost" in Your Browser

This is sneaky. Chrome and Edge have a feature called "Startup Boost" that keeps browser processes running in the background to make opening the browser faster. The problem? It eats 200-400 MB of RAM *all the time*.

**Action:**
- **Chrome:** Settings → System → Turn off "Continue running background apps when Google Chrome is closed."
- **Edge:** Settings → System and performance → Turn off "Startup boost" and "Continue running background extensions and apps."

Your browser will take one extra second to open, but your entire system will feel snappier, especially if you only have 8GB of RAM.

## 3. Disable Transparency & Animations (Instant Visual Boost)

Windows 11 loves blur and fade effects. They look nice, but they force your GPU to render constantly. If you're on a laptop without a dedicated graphics card, these effects are pure drag.

**Action:**
- Go to **Settings → Personalization → Colors** and toggle **Transparency effects** to **Off**.
- Go to **Settings → Accessibility → Visual effects** and toggle **Animation effects** to **Off**.

This won't make your PC a gaming beast, but it will make window dragging and snapping feel instant. It’s the fastest "feel" fix you can do in under 30 seconds.

## 4. Switch to "Best Performance" Power Mode

Windows 11 defaults to "Balanced" power mode to save energy. That’s great for a tablet, terrible for a desktop workstation.

**Action:** Go to **Settings → System → Power & battery**. Under "Power mode," select **Best performance**.

If you have a gaming laptop, also check the manufacturer's app (e.g., NVIDIA Control Panel or MSI Center) to ensure it’s in "Performance" or "Discrete" mode, not "Hybrid" or "Eco."

**Real example:** On my Lenovo Legion, switching from Balanced to Best Performance fixed micro-stutters in *Valorant* entirely. No driver update needed.

## 5. Reclaim Storage with Storage Sense (Don't Ignore This)

A full SSD (over 90%) will slow down Windows 11 significantly because the drive has to work harder to find free blocks for virtual memory. You don't need to buy a new drive; you need to clean house.

**Action:**
- Go to **Settings → System → Storage** and turn on **Storage Sense**.
- Click the arrow to configure it: set "Cleanup of temporary files" to **Every week** and enable "Delete temporary files that my apps aren't using."

Then, click **Cleanup recommendations** immediately. You’ll likely find the "Windows Update Cleanup" item (often 2-5 GB) and old Recycle Bin files. Delete them.

**Bonus:** If you have a 256GB SSD, consider moving your "Downloads" or "Desktop" folder to a secondary HDD (if you have one) via **Right-click on folder → Properties → Location → Move**. This frees up precious space on your boot drive.

## 6. Stop Game Bar and Background Recording

The Xbox Game Bar is useful for screenshots, but its background recording feature (which captures clips automatically) is a silent performance killer. It constantly uses the GPU encoder.

**Action:**
- Go to **Settings → Gaming → Captures**.
- Turn **off** "Record what happened in the background."

If you don't use Xbox Game Bar at all, you can disable it entirely via **Settings → Gaming → Xbox Game Bar** and toggling it off. This also removes the overlay shortcut (Win + G) that sometimes pops up accidentally.

## 7. Fix the "Search" Indexing Issue

Windows Search is notoriously slow. The culprit is often the indexing of emails or OneDrive folders that are cloud-only. If typing "calc" takes 10 seconds to find Calculator, this is for you.

**Action:**
- Go to **Settings → Privacy & security → Searching Windows**.
- Under "Find My Files," select **Classic** (instead of Enhanced). Enhanced scans your entire drive constantly. Classic only scans the Start Menu and Documents.

**Pro tip:** If you use a third-party search tool like *Everything* (which I highly recommend), you can turn off Windows Search entirely via Services, but that's a bit advanced. Stick with "Classic" for now.

## 8. Disable "SysMain" (For HDDs Only)

This is controversial, but hear me out. **SysMain** (formerly Superfetch) preloads frequently used apps into RAM to speed them up. On an SSD, this is pointless because the drive is already fast. On an HDD, it can cause constant disk thrashing at 100% usage.

**Action (SSD users only):**
1. Press **Win + R**, type `services.msc`, and press Enter.
2. Scroll down to **SysMain**.
3. Right-click → **Properties** → Set "Startup type" to **Disabled** → Click **Stop** → OK.

**Warning:** Do NOT do this if you use a traditional hard drive (HDD). It will actually slow things down. If you have an SSD (most Windows 11 machines do), this frees up RAM and stops the disk from spinning up randomly.

## 9. Update Drivers (But Not the Way You Think)

Don't use third-party "driver booster" apps—they cause more problems than they solve. Use Windows Update and the manufacturer's site.

**Action:**
- Go to **Settings → Windows Update → Advanced options → Optional updates**.
- Install any **Driver updates** listed there. These are usually chipset or graphics drivers that Microsoft has verified.

**Real example:** My Wi-Fi adapter kept dropping. Windows Update pushed a "Realtek" driver update that fixed it and improved latency by 20ms. I never would have found that on my own.

## 10. Reduce Visual Effects for Older GPUs

If you're running Windows 11 on a PC from 2018 or earlier with integrated graphics, the shadows and window animations can cause input lag.

**Action:**
1. Press **Win + R**, type `sysdm.cpl`, press Enter.
2. Go to the **Advanced** tab → Under "Performance," click **Settings**.
3. Select **Adjust for best performance** (or manually uncheck: "Animate controls and elements inside windows," "Fade or slide menus into view," and "Show shadows under windows").

Keep "Smooth edges of screen fonts" checked—it makes text readable. This turns Windows 11 into a lean, responsive machine that feels like Windows 7 in speed, but with the modern UI.

## 11. The Nuclear Option: Reset This PC

If you’ve tried everything and your PC still crawls, don't buy a new one. Use the built-in reset tool. This is the "I give up" fix that works 90% of the time.

**Action:** Go to **Settings → System → Recovery → Reset PC**. Choose **"Keep my files"** to remove apps and settings but keep your documents and photos. Then choose **"Cloud download"** to get a fresh copy of Windows 11 (this often fixes corrupted system files that the local image can't).

**Note:** This takes about 30-45 minutes. It will uninstall all your apps (Steam, Chrome, etc.), so make a list of what you need to reinstall. But honestly, a clean install is the single best performance upgrade you can do without spending money.

---

## The One Thing NOT to Do

Do **not** download "RAM cleaners" or "PC optimizers" from random websites. They are almost always malware or scamware that show you fake memory usage charts. Windows 11 manages memory fine on its own. The only "cleaner" you need is the built-in Storage Sense.

## Final Thoughts

Speed isn't about one magic switch—it's about removing the invisible weight. Start with the startup apps (Fix #1) and the Game Bar (Fix #6). Those two alone will fix 80% of "my PC is slow" complaints. If you have an SSD, disable SysMain. If you have a laptop, switch the power mode.

Do these ten fixes today, reboot, and you’ll notice the difference immediately. Your machine won't be a gaming rocket ship, but it will feel like a new laptop—without the $1,000 price tag.

**Which fix worked for you?** Let me know in the comments—I’m genuinely curious if the Game Bar was the culprit for you too.

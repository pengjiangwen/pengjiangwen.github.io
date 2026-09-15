---
title: "How to Fix a Slow Internet Connection: 12 Real Solutions"
date: "2026-09-15T15:58:40Z"
description: "Slow internet ruining your day? Learn how to diagnose and fix a slow connection with practical steps, from router placement to DNS tweaks."
tags: ["slow internet", "wifi troubleshooting", "internet speed"]
categories: ["tech"]
draft: false
---
## Introduction

Last Tuesday, my neighbor called me in a panic. Her video calls kept freezing mid-sentence, and her kids were threatening mutiny over buffering cartoons. She'd already done the thing everyone does — unplugged the router, waited thirty seconds, plugged it back in. Nothing changed.

When I walked into her house, I spotted the problem in about ten seconds. Her router was sitting on the floor behind a fish tank, sandwiched between a cordless phone base and a microwave. Three of the worst possible neighbors for a Wi-Fi signal, all in one corner.

I moved the router to a bookshelf in the hallway, changed one setting in her router's admin panel, and her speed test jumped from 4 Mbps to 68 Mbps. No new equipment. No service call. Ten minutes of work.

That's the thing about slow internet — the fix is often simpler than you think, but only if you diagnose the right problem. Here's how to actually do that.

## First, Figure Out What "Slow" Really Means

Before you touch anything, run a speed test at [speedtest.net](https://www.speedtest.net) or fast.com. Write down three numbers: download speed, upload speed, and ping (latency).

Now compare those numbers to what you're paying for. If you're on a 300 Mbps plan and getting 280 Mbps, your internet isn't slow — your problem is somewhere else, like a specific app, a weak Wi-Fi signal in one room, or a device that's struggling. If you're paying for 300 Mbps and getting 15 Mbps, you have a genuine connection problem.

This distinction matters because it saves you from wasting an hour rebooting things that were never broken.

## The Wired vs. Wireless Test

This is the single most useful diagnostic step, and most people skip it.

Plug a laptop directly into your router with an Ethernet cable. Run the speed test again.

- **Wired speed is fast, Wi-Fi is slow:** Your internet service is fine. The problem is your Wi-Fi — signal strength, interference, or router placement.
- **Both are slow:** The problem is your modem, your router, your ISP, or the wiring coming into your house.

Knowing which side of that line you're on cuts your troubleshooting in half.

## Fixes for Wi-Fi Problems

### Move Your Router (Seriously)

Routers broadcast signal outward and downward. Putting one on the floor, in a closet, or behind a TV is like putting a speaker under a blanket. Ideal placement:

- Central location in your home, as high as practical
- Away from metal objects, fish tanks, mirrors, and thick concrete walls
- At least a few feet from microwaves, cordless phone bases, and baby monitors — all of which operate on or near the 2.4 GHz band

If your router has external antennas, point them vertically for single-story coverage, or angle one horizontally if you need to reach an upstairs room.

### Switch to the 5 GHz Band

Most modern routers broadcast two networks: 2.4 GHz and 5 GHz. The 2.4 GHz band travels farther but is slower and more crowded. The 5 GHz band is much faster but has shorter range.

If you're in the same room as the router and still getting slow speeds, you're probably connected to 2.4 GHz. Go into your device's Wi-Fi settings and connect to the network name with "5G" in it. It's often a bigger jump than upgrading your plan.

### Change Your Wi-Fi Channel

In apartment buildings and dense neighborhoods, everyone's router is shouting on the same channel. It's like trying to have a conversation in a crowded restaurant.

Log into your router's admin page (usually 192.168.1.1 or 192.168.0.1), find the wireless channel setting, and switch from "Auto" to a specific channel. For 2.4 GHz, stick to channels 1, 6, or 11 — these don't overlap. For 5 GHz, most routers handle this well automatically, but you can experiment.

Not sure which channels are crowded? Apps like WiFi Analyzer (Android) or NetSpot (Mac/Windows) show you a visual map of every network around you.

### Check for Bandwidth Hogs

One device can ruin everyone's connection. A 4K Netflix stream eats about 25 Mbps. A cloud backup running in the background can saturate an entire household. Windows updates, game downloads, and security cameras uploading footage all compete for the same pipe.

Log into your router and look at connected devices. If something unfamiliar is there, someone might be piggybacking on your network. Change your Wi-Fi password and use WPA3 encryption if your router supports it.

## Fixes for Wired and Modem Problems

### Restart in the Right Order

The classic "unplug it and plug it back in" works, but the order matters:

1. Unplug both the modem and router.
2. Wait a full 60 seconds (not 10 — capacitors need time to discharge).
3. Plug in the modem first and wait for all its lights to stabilize.
4. Then plug in the router.

Doing it out of order can leave your router holding onto a stale IP address.

### Check Your Modem's Signal Levels

If you have cable internet, your modem's admin page shows downstream and upstream power levels. Downstream should typically be between -15 dBmV and +15 dBmV, and upstream between 37 and 48 dBmV. Values outside those ranges usually mean a wiring or line problem that only your ISP can fix — but at least you'll know what to tell them when you call.

### Ask Your ISP for a New Modem

If you're renting an older modem from your provider, you might be capped below your plan's speed without realizing it. A DOCSIS 3.0 modem can't deliver gigabit speeds; you need DOCSIS 3.1. Ask your ISP whether your equipment actually supports the plan you're paying for. Sometimes the answer is no, and they'll swap it for free.

## Quick Wins That Often Get Overlooked

### Change Your DNS Servers

DNS translates website names into IP addresses. Slow or overloaded DNS servers make every page feel sluggish even when your raw speed is fine. Try switching to Cloudflare (1.1.1.1) or Google (8.8.8.8) in your router settings. It takes two minutes and sometimes produces a noticeable improvement in page load times.

### Update Your Router's Firmware

Router manufacturers quietly release firmware updates that fix performance bugs and security holes. Log into your router's admin panel and check for updates. If your router is more than five or six years old and hasn't seen an update in years, it may simply be time for a replacement — modern mesh systems start around $100 and often outperform older flagship routers.

### Test at Different Times of Day

If your internet is fast at 7 AM and crawling at 8 PM, the problem isn't your equipment. That's congestion on your ISP's network, and it's a strong argument for calling them and documenting the pattern. Some providers will credit your bill if they can't deliver advertised speeds during peak hours.

## When to Call Your ISP

Call them when:

- Wired speeds are consistently well below your plan
- Your modem's signal levels are out of range
- Speeds tank at the same time every day
- You've replaced or ruled out your own equipment

When you call, lead with data: "I'm paying for 500 Mbps, I've tested directly wired to the modem, and I'm getting 40 Mbps at 8 PM every night." That gets you past the script and to a technician who can actually help.

## The Bottom Line

Most slow internet problems come down to one of four things: bad router placement, the wrong Wi-Fi band, a bandwidth hog, or outdated equipment. Work through them in that order, and you'll fix the majority of issues without spending a dime.

And if you take nothing else from this article, take this: run the wired test first. It tells you whether you're fighting your Wi-Fi or your internet provider — and those are two very different fights.

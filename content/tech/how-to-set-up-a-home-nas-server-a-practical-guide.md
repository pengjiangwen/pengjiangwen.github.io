---
title: "How to Set Up a Home NAS Server: A Practical Guide"
date: "2026-07-02T10:19:52Z"
description: "Build your own home NAS from scratch. Step-by-step guide covering hardware, software, RAID, and remote access for backups and media streaming."
tags: ["home nas", "diy nas server", "network attached storage", "home server setup", "data backup"]
categories: ["tech"]
draft: false
---
TITLE: How to Set Up a Home NAS Server: A Practical Guide
DESCRIPTION: Build your own home NAS from scratch. Step-by-step guide covering hardware, software, RAID, and remote access for backups and media streaming.
TAGS: home NAS, DIY NAS server, network attached storage, home server setup, data backup

## Introduction

Last year, I lost three years of family photos when a laptop hard drive failed. The backup drive I’d been using was sitting right next to the laptop on the same desk during a power surge. Both died. That’s when I stopped treating backup as an afterthought and started building a home NAS.

A Network Attached Storage (NAS) is essentially your own private cloud. Unlike Dropbox or Google Drive, you own the hardware, you control the data, and there are no monthly subscription fees for storage. You can stream movies to your TV, back up every device in your house, and access files remotely—all without paying a recurring bill.

This guide walks through the entire process: choosing hardware, installing software, configuring storage, and setting up remote access. No assumptions about prior server experience. Just practical steps that work.

## Why Build a NAS Instead of Buying One?

Pre-built NAS units from Synology or QNAP are convenient. Plug in drives, click a few buttons, and you’re done. They also cost a premium. A 4-bay Synology enclosure with no drives runs around $400. For that same budget, you can build a machine with significantly more processing power, upgradeability, and storage capacity.

Building your own also means you’re not locked into proprietary software. If Synology decides to drop support for your model in three years, you’re stuck. With a DIY build, you can swap operating systems, upgrade components, or repurpose the hardware entirely.

The trade-off is time. You’ll spend an afternoon assembling and configuring. But once it’s running, maintenance is minimal.

## Step 1: Choose Your Hardware

### The "Just Works" Build

For most home users, this is the sweet spot. It handles file storage, media streaming, automated backups, and runs 24/7 without breaking the bank.

- **Case:** Fractal Design Node 304 (mini-ITX, holds 6 drives)
- **Motherboard:** ASRock B660M-ITX/ac (built-in WiFi is nice for initial setup)
- **CPU:** Intel Core i3-12100 (efficient, has integrated graphics for transcoding)
- **RAM:** 8GB DDR4 (start here, upgrade if you run virtual machines)
- **Power Supply:** 300W-400W 80+ Bronze (don’t overspend, NAS draws little power)
- **Boot Drive:** 120GB SATA SSD (for the operating system)
- **Storage Drives:** Two 4TB WD Red Plus (NAS-rated, CMR technology)

Total cost: roughly $350-400 without storage drives. Add $100-120 per 4TB NAS drive.

### The Budget Build

If you have an old desktop lying around, you can repurpose it. Minimum requirements:

- Any dual-core CPU from the last 10 years
- 4GB RAM (8GB recommended)
- SATA ports for your drives (add a PCIe SATA card if needed)
- A case that can hold at least two 3.5-inch drives

I started with a 2012 Dell Optiplex. It’s still running, serving files to five people without complaint.

### What to Avoid

- **Raspberry Pi with USB drives:** The USB bus is shared. One drive failing can corrupt the entire array. Also, USB drives aren’t designed for 24/7 operation.
- **Desktop hard drives (WD Blue, Seagate Barracuda):** These don’t have TLER (Time-Limited Error Recovery). In a RAID array, a desktop drive might drop out unnecessarily, causing rebuild headaches.
- **Gaming power supplies:** Overkill. A 1000W PSU running at 10% load is inefficient. Stick with 300-400W.

## Step 2: Assemble the Hardware

This is straightforward. Mount the motherboard in the case, install the CPU and RAM, connect the power supply. For the storage drives:

1. Install the boot SSD in any SATA port.
2. Install your storage drives. If using a case like the Node 304, drives mount on their side with rubber grommets to reduce vibration.
3. Connect SATA data cables to the motherboard and power cables from the PSU.

One tip: label your drives. Write "Boot", "Drive 1", "Drive 2" on masking tape and stick it on the cable. When a drive fails two years from now, you’ll thank yourself.

## Step 3: Install the Operating System

### TrueNAS Scale (Recommended)

TrueNAS Scale is free, open-source, and built on Linux. It supports ZFS, which is the gold standard for data integrity. It also runs Docker containers and virtual machines if you want to expand later.

1. Download the TrueNAS Scale ISO from their website.
2. Use BalenaEtcher or Rufus to write it to a USB stick (8GB or larger).
3. Plug the USB into your NAS, boot from it.
4. Follow the installer: select your boot SSD, set a root password, and let it install.
5. After reboot, remove the USB installer. The system will boot from the SSD.
6. Find the IP address shown on the monitor. Type that IP into a web browser on your main computer. You’ll see the TrueNAS web interface.

### Alternative: Unraid

Unraid costs $59+ but offers easier drive expansion. You can mix drive sizes, add drives one at a time, and it has a huge community for app support. If you’re less technical and want something that “just works,” Unraid is worth the money.

I use TrueNAS because ZFS’s checksumming catches silent data corruption. Unraid doesn’t do that by default. For family photos and financial documents, I want that extra layer.

## Step 4: Configure Your Storage Pool

In TrueNAS, storage is organized into pools. A pool is built from one or more virtual devices (vdevs). Each vdev can be a single drive, a mirror, or a RAID-Z array.

### For Two Drives: Mirror

Two 4TB drives in a mirror gives you 4TB of usable space. If one drive fails, you replace it and the system rebuilds automatically. This is the simplest and most reliable setup for beginners.

In the TrueNAS web UI:

1. Go to Storage → Create Pool.
2. Name it "tank" (or anything).
3. Drag both drives into the Data VDevs section.
4. Select "Mirror" from the dropdown.
5. Click Create.

### For Three or More Drives: RAID-Z

RAID-Z is similar to RAID 5. With three 4TB drives, you get 8TB usable. One drive can fail without data loss. With four drives in RAID-Z2, you get 8TB usable but can lose two drives.

Choose RAID-Z if you need more capacity and can tolerate slightly more complexity during recovery.

### Important: Don't Fill Past 80%

ZFS performance degrades when a pool is over 80% full. Plan your capacity accordingly. If you need 6TB of storage, get drives that give you at least 7.5TB usable.

## Step 5: Create Shares and Set Permissions

Now you need to make the storage accessible on your network.

### For Windows/Mac/Linux: SMB Shares

1. In TrueNAS, go to Shares → Windows (SMB) Shares → Add.
2. Select the dataset (folder) you want to share.
3. Enable "Allow Guest Access" only if you trust everyone on your network. Otherwise, create users under Accounts → Users and assign permissions.

### For Time Machine Backups (Mac)

1. Create a separate dataset just for Time Machine (e.g., "timemachine").
2. Enable the "Time Machine" flag in that dataset’s advanced options.
3. In the SMB share settings, check "Enable Time Machine support."

Now every Mac on your network will see the NAS as a backup destination. No more plugging in external drives.

## Step 6: Set Up Remote Access (Securely)

This is where most people get it wrong. They forward port 443 or 80 to their NAS and call it done. That’s how you get ransomwared.

### The Right Way: Tailscale

Tailscale creates a secure mesh VPN. You install it on your NAS and on your phone/laptop. All traffic goes through an encrypted tunnel. No ports open on your router.

1. Sign up for a free Tailscale account (up to 100 devices).
2. On TrueNAS, go to Apps → Available Apps → search for "Tailscale".
3. Install it. Authenticate with your Tailscale account.
4. Install the Tailscale app on your phone and laptop.
5. Now you can access your NAS by its Tailscale IP address from anywhere in the world.

### Alternative: WireGuard

If you prefer not to use a third-party service, WireGuard is built into TrueNAS. Set it up under System → Services → WireGuard. It’s more technical but completely self-hosted.

### What Not to Do

- **Do not** enable FTP or plain HTTP. They send passwords in cleartext.
- **Do not** forward port 22 (SSH) unless you disable password authentication and use SSH keys only.
- **Do not** use the "admin" account for daily use. Create a separate user with limited permissions.

## Step 7: Automate Backups (Yes, Back Up Your NAS)

A NAS is not a backup if it’s the only copy of your data. RAID protects against drive failure, not against fire, theft, or ransomware.

### Local Backup: USB Drive

Plug in a large external drive. In TrueNAS, go to Tasks → Periodic Snapshot Tasks to take daily snapshots of your datasets. Then set up a Replication Task to send those snapshots to the USB drive. If your NAS dies, you plug the USB into any Linux machine and recover.

### Offsite Backup: Backblaze B2

Backblaze B2 costs about $0.005/GB/month. For 500GB of critical data, that’s $2.50/month.

1. Create a Backblaze B2 account and generate an Application Key.
2. In TrueNAS, go to Tasks → Cloud Sync Tasks.
3. Select "Backblaze B2" as the destination.
4. Schedule it to run weekly.

This gives you a copy off-site. If your house burns down, your data survives.

## Real-World Usage After Setup

Here’s what my NAS does daily:

- **File storage:** All documents, photos, and videos live on the NAS. My laptop has a 256GB SSD. I don’t store anything locally.
- **Media streaming:** I run Jellyfin (free, open-source alternative to Plex) in a Docker container on TrueNAS. It streams 4K movies to my TV, phone, and tablet. The Intel iGPU handles hardware transcoding effortlessly.
- **Automated backups:** Every Mac in the house backs up via Time Machine. Windows machines use Veeam Agent to back up to an SMB share.
- **Photo management:** I use Immich (self-hosted Google Photos alternative) to auto-upload photos from my phone. They’re searchable by date, location, and even objects.
- **Home assistant:** The same machine runs Home Assistant in a VM to control smart lights and sensors.

Total power draw: about 35 watts idle. That’s roughly $3/month in electricity.

## Final Advice

Start small. A two-drive mirror with TrueNAS Scale will handle 90% of what most households need. You can always add drives or build a second NAS later. Don’t overthink the hardware—buy what you can afford, set it up, and start using it.

The hardest part isn’t the assembly or the software. It’s the discipline to actually use it. Set up automatic backups on every device on day one. Schedule a monthly check to verify your snapshots are running. And for the love of data, don’t skimp on the off-site backup.

Your future self, after a hard drive fails, will thank you.

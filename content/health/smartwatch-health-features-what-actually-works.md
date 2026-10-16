---
title: "Smartwatch Health Features: What Actually Works"
date: "2026-10-16T16:08:36Z"
description: "A practical look at which smartwatch health sensors deliver real value, which are hype, and how to use the data without fooling yourself."
tags: ["fitness", "nutrition", "sleep"]
categories: ["health"]
draft: false
---
## Introduction

A 52-year-old man I know got a notification on his Apple Watch at 2:14 a.m. on a Tuesday: heart rate 41 bpm, sustained for 10 minutes. He'd been asleep. He almost ignored it—he's a runner, low resting heart rates are normal for him. But the watch had flagged it three nights running, so he mentioned it to his doctor. One ECG later, he was on a beta-blocker and wearing a 14-day Holter monitor. The watch didn't diagnose him. It just noticed something his body was doing while he was unconscious, which is roughly 30% of your life you have no data on otherwise.

That's the actual value proposition of a smartwatch. Not step counts. Not "readiness scores." It's the fact that a $250–$800 device on your wrist is running a continuous, passive monitoring loop while you sleep, work, and sit in traffic. The question isn't whether these features are useful. It's which ones are useful, which ones are marketing, and how to interpret the numbers without spiraling.

## The sensors that actually hold up

### Optical heart rate (PPG)

Every mainstream smartwatch—Apple Watch Series 6 and later, Samsung Galaxy Watch 4+, Garmin Venu 3, Fitbit Charge 6, Pixel Watch 2—uses photoplethysmography. Green LEDs shine into your skin, and a photodiode measures how much light bounces back. Blood volume changes with each heartbeat, so the reflected light pulses.

Accuracy during steady-state cardio: good. Studies consistently find errors under 5% compared to chest straps during running and cycling. Accuracy during interval training, weightlifting, or anything involving rapid wrist flexion: much worse. Errors of 10–20 bpm are common when you're gripping a barbell or doing burpees. If you care about heart rate during those activities, get a chest strap (Polar H10, ~$90) or an armband (Polar Verity Sense, ~$90). The watch is fine for the other 22 hours.

### ECG

Apple Watch Series 4 and later, Samsung Galaxy Watch 3 and later, and Withings ScanWatch offer single-lead ECGs. You press a finger on the crown for 30 seconds. The FDA cleared these specifically to detect atrial fibrillation—not to diagnose heart attacks, not to detect blockages, not to replace a 12-lead ECG.

The Apple Heart Study, published in the New England Journal of Medicine in 2019, enrolled over 400,000 participants. Among those who got an irregular rhythm notification and followed up, 34% were confirmed to have AFib. That means two-thirds of notifications were false alarms—but also that the watch caught AFib in people who had no idea they had it. If you're over 65, or have hypertension, diabetes, or a family history of AFib, this feature is genuinely worth having. If you're 28 and healthy, it's mostly going to generate anxiety.

### Blood oxygen (SpO2)

Apple Watch Series 6+, most Galaxy Watches, and many Fitbits measure blood oxygen. Here's the problem: they're not medical-grade pulse oximeters, and the FDA has repeatedly warned consumers about this. A hospital pulse oximeter costs $30 and is calibrated to ±2%. Wrist-based SpO2 has wider error margins and is heavily affected by motion, skin pigmentation, and wrist position.

Useful for: spotting trends during sleep, especially if you're investigating sleep apnea. Not useful for: deciding whether you're too sick to go to the ER. If your SpO2 reads 88% and you feel fine, re-test with a fingertip device before panicking. If it reads 88% and you're short of breath, go to the ER and don't bother re-testing.

### Skin temperature

Apple Watch Series 8+, Galaxy Watch 5+, and Oura Ring track overnight skin temperature and compare it to your personal baseline. A rise of 0.5–1.0°C above your baseline often precedes illness by a day or two, and tracks with menstrual cycle phase.

This is one of the most underrated features. It won't tell you you're sick. It'll tell you something changed. Pair it with how you feel, and you have a decent early-warning system.

## The features that are mostly noise

### "Readiness" and "recovery" scores

Whoop, Garmin, and Oura all generate a single number each morning telling you how hard to train. The problem: these scores are black boxes. Garmin's Body Battery, for example, weighs heart rate variability, stress, sleep, and activity—but the exact formula isn't published, and it varies by firmware update.

Worse, the scores often contradict each other. I've seen mornings where Oura said "take it easy" and Garmin said "you're primed." Both were reading the same body. That's not a measurement problem; it's a modeling problem. Use the underlying data—HRV, resting heart rate, sleep duration—and ignore the composite score.

### Calorie burn estimates

Smartwatch calorie estimates for exercise are routinely off by 20–40%. A 2020 study in the Journal of Personalized Medicine found error rates up to 93% for some activities. If you're using a watch to "earn" food, stop. If you're using it to compare yesterday's run to today's, fine—relative changes are more reliable than absolute numbers.

### Stress scores

These are derived from heart rate variability, which is a real physiological signal. But "stress" is a loaded word. A hard workout tanks your HRV. So does alcohol. So does a cold. So does a stressful email. The watch can't tell the difference. Treat the stress score as "your nervous system is doing something" rather than "you are stressed."

## A practical checklist: setting up your watch so it's actually useful

Most people leave default settings on and then wonder why the data is garbage. Here's what to change in the first week.

**1. Set your sleep schedule.** Apple Watch, Garmin, and Fitbit all use your typical sleep window to calibrate. If you never tell it when you sleep, sleep tracking is unreliable.

**2. Turn on high/low heart rate alerts.** On Apple Watch: Watch app > Heart > Heart Rate Notifications. Set high alert at 120 bpm (resting) and low at 40–50 bpm depending on your fitness. These are the alerts that actually catch problems.

**3. Enable AFib history if you're over 65 or have risk factors.** Apple Watch: Heart > AFib History. This gives you a weekly burden percentage—how much of the week you spent in AFib.

**4. Wear it snug, one finger-width above the wrist bone.** Loose watches produce garbage HR data. If you can slide a finger under the band, it's too loose.

**5. Charge it during a fixed window.** Shower time works. So does your morning coffee. If you charge it randomly, you'll miss sleep data.

**6. Sync to Apple Health, Google Fit, or Strava.** The watch app is for glancing. The phone app is for trends. Export to a platform that aggregates.

**7. Do a two-week baseline before interpreting anything.** HRV, resting heart rate, and skin temperature only mean something relative to your own normal. Two weeks minimum, four is better.

**8. Check your data against a known quantity.** Next time you're at the doctor, compare the cuff blood pressure reading (if your watch has BP—Galaxy Watch only, and it needs calibration) or the pulse oximeter reading to your watch. Note the gap. That's your correction factor.

## What most guides get wrong

**They treat all sensors as equally accurate.** They're not. Heart rate during steady cardio: reliable. SpO2: unreliable. ECG for AFib: clinically validated. Calorie burn: barely better than a guess. A guide that doesn't rank these is useless.

**They ignore the anxiety problem.** Cardiologists are seeing a rise in "smartwatch-induced anxiety"—people who check their heart rate 40 times a day and panic at every fluctuation. Your heart rate varies by 10–20 bpm throughout the day based on posture, caffeine, digestion, and whether you just stood up. That's normal. The watch shows you a number without context. You have to supply the context.

**They confuse detection with diagnosis.** A notification is not a diagnosis. An irregular rhythm alert means "get this checked," not "you have AFib." The Apple Heart Study's 34% positive predictive value is a good reminder: most alerts are false positives, but the ones that aren't can save your life. Take them seriously without assuming the worst.

## The one feature worth paying for

If you're choosing a watch primarily for health, prioritize continuous heart rate monitoring with high/low alerts and, if you're over 50 or have risk factors, ECG. Sleep tracking and temperature are nice. SpO2 is a bonus. Blood pressure monitoring is coming (Samsung has it, Apple has patents, FDA clearance is pending) but isn't there yet for most people.

The best health feature on a smartwatch isn't any single sensor. It's the fact that it's on your wrist while you sleep, and it notices things you can't. That's worth the $250. The rest is details.

## Related Reading

- [How to Boost Metabolism: 12 Science-Backed Strategies](https://pengjiangwen.github.io/health/how-to-boost-metabolism-12-science-backed-strategies/)
- [10,000 Steps a Day: Real Benefits Backed by Science](https://pengjiangwen.github.io/health/10000-steps-a-day-real-benefits-backed-by-science/)
- [Natural Energy Boosters: 12 Science-Backed Ways to Beat Fatigue](https://pengjiangwen.github.io/health/natural-energy-boosters-12-science-backed-ways-to-beat-fatigue/)


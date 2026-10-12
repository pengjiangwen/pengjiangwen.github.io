#!/usr/bin/env python3
"""Controlled tag vocabulary so we don't create thousands of thin tag pages.

Each category has a small set of tags with a matching regex. Tags are derived
from the article title + body, so both existing and newly generated articles
end up using the same, stable vocabulary.
"""
import re

# category -> {tag: regex}
CATEGORY_TAGS = {
    "tech": {
        "smartphones": r"\b(smartphone|smart phone|iphone|android|pixel|galaxy|5g phone|mobile phone)\b",
        "laptops": r"\b(laptop|macbook|chromebook|notebook computer)\b",
        "pc-building": r"\b(gaming pc|build a pc|pc build|desktop pc|cpu|gpu|ram\b|ssd\b|motherboard)\b",
        "smart-home": r"\b(smart home|smart device|smart plug|smart bulb|smart thermostat|alexa|google home|home assistant|smart lock)\b",
        "audio": r"\b(earbud|earbuds|headphone|headphones|speaker|soundbar|bluetooth audio)\b",
        "software": r"\b(software|windows|linux|macos|app\b|apps\b|antivirus|vpn|cloud storage)\b",
        "security-privacy": r"\b(privacy|password|malware|hacker|cyber ?security|secure your|data protection)\b",
        "networking": r"\b(wi-?fi|router|internet|network|5g|bandwidth|mesh)\b",
        "productivity-tech": r"\b(remote work|work from home|productivity|dual monitor|home office)\b",
        "buying-guide": r"\b(best|top picks|review|reviews|buying guide|comparison|vs\b|under \$?\d+)\b",
    },
    "lifestyle": {
        "productivity": r"\b(productivity|time management|focus|procrastinat|deep work|getting things done)\b",
        "personal-finance": r"\b(money|budget|budgeting|saving|savings|debt|credit|income|salary|invest|finance|frugal)\b",
        "minimalism": r"\b(minimalist|minimalism|declutter|decluttering|simple living|capsule wardrobe)\b",
        "habits-routines": r"\b(habit|habits|routine|routines|morning|evening|journaling|daily)\b",
        "career": r"\b(career|job|jobs|interview|resume|workplace|promotion|negotiat)\b",
        "learning": r"\b(learn|learning|course|courses|language|study|skill|reading|book|books)\b",
        "travel": r"\b(travel|trip|vacation|flight|hotel|packing|backpacking)\b",
        "digital-wellbeing": r"\b(digital detox|screen time|phone addiction|social media|digital minimalism|digital wellbeing)\b",
        "self-improvement": r"\b(confidence|motivation|personal growth|mindset|self ?improvement|overcome fear|goals)\b",
        "food-shopping": r"\b(grocer|meal plan|meal prep|cooking|recipes|food shopping)\b",
    },
    "home": {
        "home-organization": r"\b(organiz|organis|declutter|storage|closet|cabinet|garage|shelv|tidy)\b",
        "cleaning": r"\b(clean|cleaning|vacuum|dust|laundry|stain|mop)\b",
        "gardening": r"\b(garden|gardening|plant|plants|vegetable|herb|lawn|houseplant|soil)\b",
        "home-security": r"\b(security system|security camera|doorbell|smart lock|alarm|surveillance|burglar)\b",
        "energy-efficiency": r"\b(energy|electricity|solar|thermostat|utility bill|insulation|efficiency|appliance energy)\b",
        "smart-home": r"\b(smart home|smart light|smart bulb|automation|smart plug|alexa|google home|home assistant)\b",
        "diy": r"\b(diy|build|repair|install|paint|deck|renovat|fix)\b",
        "interior-design": r"\b(interior|decor|decorat|furniture|lighting design|color scheme|room design|wall)\b",
        "appliances": r"\b(vacuum cleaner|air purifier|water filter|refrigerator|washer|dishwasher|robot vacuum|appliance)\b",
        "home-office": r"\b(home office|desk|chair|ergonomic|workspace|standing desk)\b",
    },
    "health": {
        "fitness": r"\b(workout|exercise|running|run\b|yoga|gym|stretch|walking|fitness|strength|cardio)\b",
        "nutrition": r"\b(nutrition|diet|protein|meal|food|eat|sugar|vegan|vegetarian|carbs|calorie)\b",
        "sleep": r"\b(sleep|insomnia|bedtime|nap|circadian|sleeping)\b",
        "mental-health": r"\b(anxiety|stress|mental health|meditation|mindful|depress|mood|burnout)\b",
        "supplements": r"\b(supplement|vitamin|creatine|probiotic|omega|magnesium|collagen)\b",
        "weight-loss": r"\b(weight loss|lose weight|fat loss|slim|obesity)\b",
        "hydration": r"\b(hydrat\w*|drink\w*\s+water|drinking\s+water|water\s+intake|electrolyte\w*|dehydrat\w*|water)\b",
        "posture-ergonomics": r"\b(posture|back pain|neck pain|ergonomic|desk job|sitting)\b",
        "immunity": r"\b(immune|immunity|gut health|digestion|microbiome|cold and flu)\b",
        "healthy-habits": r"\b(habit|routine|wellness|healthy lifestyle|self ?care|longevity)\b",
    },
}

CATEGORIES = list(CATEGORY_TAGS.keys())


def tags_for(title: str, body: str, category: str, limit: int = 3):
    """Return up to `limit` controlled tags for an article.

    Prefer tags that appear in the title (much more precise); fall back to the
    body only when the title yields nothing.
    """
    vocab = CATEGORY_TAGS.get(category, {})
    if not vocab:
        return [category]
    title_low = (title or "").lower()
    title_hits = [tag for tag, pat in vocab.items() if re.search(pat, title_low)]
    if title_hits:
        return title_hits[:limit]
    body_low = (body or "").lower()
    body_hits = [tag for tag, pat in vocab.items() if re.search(pat, body_low)]
    return body_hits[:limit] or [category]

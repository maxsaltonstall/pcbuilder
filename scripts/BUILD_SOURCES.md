# Where to Find Optimized D&D 3.5 Builds

## Top-Tier Community Sources

### 1. Giant in the Playground (GitP) - **BEST SOURCE**

**Character Optimization Forum:**
- URL: https://forums.giantitp.com/forumdisplay.php?46-Gaming
- Subforum: "D&D 3rd Edition/3.5 Edition/d20"

**Key Threads to Mine:**

1. **"CO Handbook" Sticky Threads**
   - Search: "handbook" in titles
   - Example threads:
     - "Cleric Handbook"
     - "Wizard Optimization Handbook"
     - "Melee Handbook"
     - "Gish Handbook"
   - Each handbook has 10-50 optimized builds

2. **"[Build]" Tagged Threads**
   - Search: `[Build]` or `[3.5]`
   - Filter by views/replies (popular = well-vetted)
   - Example: "[Build] The Mailman - Wizarding for Fun and Profit"

3. **Tier System Discussion**
   - Search: "tier system" or "class tier"
   - Tiers 1-2 have the most optimized builds
   - Good for understanding power levels

**How to Extract:**
```bash
# Manual extraction workflow:
# 1. Navigate to thread
# 2. Find "Spoiler" or code blocks with build details
# 3. Copy class progression, feats, stats
# 4. Convert to our JSON format

# Example thread:
# https://forums.giantitp.com/showthread.php?XXXXX
```

### 2. BrilliantGameologists (Archived)

**Archive Access:**
- Original site is down
- Wayback Machine: https://web.archive.org/web/*/brilliantgameologists.com
- Some content preserved on GitP and Reddit

**Notable Archived Content:**
- "Mailman Build" (Wizard optimization)
- "Pun-Pun" (theoretical maximum)
- Tier system origins
- Prestige class ranking

**How to Access:**
```
1. Go to Wayback Machine
2. Search for: brilliantgameologists.com
3. Navigate to forums section
4. Look for snapshots from 2010-2012 (peak activity)
```

### 3. Min/Max Boards

**Archive Status:**
- Also mostly archived
- Some mirrors exist
- Community moved to GitP and Reddit

### 4. CharOp Wiki

**URL:** http://www.minmaxboards.com/index.php?wiki=home (if accessible)

**Alternative:** Search for "D&D 3.5 character optimization wiki" for mirrors

**Content:**
- Feat rankings
- Spell rankings
- Class tier lists
- Prestige class guides

## Secondary Sources

### 5. EN World Forums

- URL: https://www.enworld.org/forums/
- Older forum with some 3.5 optimization content
- Search: "character optimization" or "optimized build"

### 6. Reddit - r/3d6

- URL: https://www.reddit.com/r/3d6/
- Mostly 5e now, but search history for "[3.5]" tag
- Less optimization focus than GitP

### 7. D&D Wiki

- URL: https://www.dandwiki.com/wiki/3.5e_Optimized_Character_Builds
- **WARNING:** Quality varies wildly
- Some builds are broken/illegal
- Good for edge cases and unusual combos
- Always cross-reference with community sources

## Published Sources (Official)

### 8. Dragon Magazine Character Builds

**Archive Access:** (If you have digital subscription)
- Issues #310-#359 had regular optimization articles
- "Class Acts" series
- "Countdown to 3.5" optimization articles

**Notable Articles:**
- Dragon #319: "The Psionic Archer" (Soulbow)
- Dragon #324: "Divine Might" builds
- Dragon #331: "Arcane Archer Redeemed"

### 9. WotC Character Builder Archive

**Historical:** Wizards had an online character builder
- Mostly lost to time
- Some builds preserved in forum discussions

## Specific Famous Builds to Test Against

### Tier 1 (God-Tier Optimization)

1. **"The Mailman"** - Conjurer/Incantatrix
   - Source: GitP, BrilliantGameologists
   - Focus: Summon swarms, action economy abuse
   - Search: "mailman build wizard"

2. **"CoDzilla"** - Cleric with Divine Metamagic
   - Source: Multiple forums
   - Focus: Persistent buffs, all-day duration
   - Search: "codzilla cleric druid"

3. **"Batman Wizard"** - Diviner specialist
   - Source: GitP optimization handbook
   - Focus: Prepared casting, divination cheese
   - Search: "batman wizard diviner"

### Tier 2 (Highly Optimized)

4. **"Ubercharger"** - Barbarian/Fighter/Lion Totem
   - Source: GitP Melee Handbook
   - Focus: Pounce + power attack
   - Search: "ubercharger barbarian pounce"

5. **"Arcane Archer Done Right"** - Wizard/Fighter/AA
   - Source: Dragon #331, GitP
   - Focus: Gish archer optimization
   - Search: "arcane archer optimization"

6. **"Crusader God"** - Tome of Battle Crusader
   - Source: GitP ToB Handbook
   - Focus: Maneuver optimization
   - Search: "crusader optimization tome of battle"

### Tier 3 (Well-Optimized)

7. **"Ultimate Skill Monkey"** - Factotum/Rogue
   - Source: GitP Skill Monkey threads
   - Focus: Maximum skills and versatility
   - Search: "factotum skill monkey"

8. **"Two-Weapon Ranger"** - Ranger/Tempest
   - Source: Complete Warrior optimization
   - Focus: TWF feat chain
   - Search: "two weapon fighter ranger tempest"

## Automated Collection Strategy

### Web Scraper for GitP (Concept)

```typescript
// scripts/scrapeBuilds.ts

async function scrapeGitPBuilds() {
  // 1. Get list of handbook threads
  const handbooks = [
    'https://forums.giantitp.com/showthread.php?XXXXX', // Wizard handbook
    'https://forums.giantitp.com/showthread.php?XXXXX', // Cleric handbook
    // ... etc
  ];

  for (const url of handbooks) {
    // 2. Parse thread HTML
    const html = await fetch(url).then(r => r.text());

    // 3. Find build blocks (usually in spoilers or code tags)
    const builds = extractBuilds(html);

    // 4. Parse build details
    for (const build of builds) {
      const parsed = parseBuildText(build);

      // 5. Convert to test JSON format
      const testCase = convertToTestCase(parsed);

      // 6. Save to test-builds/
      fs.writeFileSync(
        `test-builds/${parsed.name}.json`,
        JSON.stringify(testCase, null, 2)
      );
    }
  }
}

function parseBuildText(text: string) {
  // Extract:
  // - Class progression (Wizard 5 / Fighter 2 / AA 10)
  // - Feats by level
  // - Ability scores
  // - Key features

  // Regex patterns for common formats:
  // "Wizard 5 / Fighter 2 / Arcane Archer 10"
  // "Level 1: Scribe Scroll, Point Blank Shot"
  // "Str 10, Dex 18, Con 14, Int 16, Wis 10, Cha 8"
}
```

### Manual Collection Workflow

**For each build:**

1. **Find the build** on GitP or other source
2. **Read the build post** - look for:
   - Class progression
   - Feat selections
   - Ability scores
   - Key levels (prestige class entry)
   - Expected stats at level 20
3. **Create JSON file** in `test-builds/`
4. **Document source** - include URL and forum user
5. **Add to validation suite**

### Priority Builds to Collect (Top 10)

1. ✅ Arcane Archer (already done)
2. ⬜ CoDzilla Cleric (persistent spell abuse)
3. ⬜ Mailman Wizard (summoner)
4. ⬜ Ubercharger (melee charger)
5. ⬜ Factotum Skill Monkey
6. ⬜ Crusader (Tome of Battle)
7. ⬜ Dread Necromancer (undead army)
8. ⬜ Artificer (item optimization)
9. ⬜ Druid Wildshaper
10. ⬜ Beguiler/Mindbender (skill + spells)

## Quality Indicators

When evaluating builds from forums:

✅ **Good Signs:**
- High post count (100+ replies = well-vetted)
- Multiple contributors reviewing
- Mathematically detailed (shows calculations)
- Cites sourcebooks and page numbers
- Discusses trade-offs
- Updated/refined over time

❌ **Red Flags:**
- Low engagement (few replies)
- No sourcebook citations
- Claims that seem too good
- Rules misinterpretations
- Homebrew content mixed in
- "DM permission required" disclaimers

## Next Steps

1. **Manual Phase:**
   - Collect 10-15 high-quality builds manually
   - Convert to test JSON format
   - Document sources and rationale

2. **Automation Phase:**
   - Build web scraper for GitP
   - Parse common build formats
   - Auto-generate test cases

3. **Validation Phase:**
   - Run validator against all builds
   - Identify algorithm weaknesses
   - Iterate on optimization engine

4. **Community Phase:**
   - Allow users to submit builds
   - Crowdsource test cases
   - Build leaderboard

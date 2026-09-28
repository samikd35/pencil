# Marketing skills for SamToons

Researched 16 September 2026. Scope: discover agent skills for promoting the existing Manchester derby animation through YouTube, Shorts, Instagram Reels, and TikTok. No skill installation, advertising spend, publishing, or new film production was requested in this research step.

## Recommendation

Start with **coreyhaines31/marketingskills → social**. Its current instructions explicitly cover short-form scripts, extracting self-contained moments from longer videos, platform-specific captions, calendars, and reviewing performance. For SamToons, apply those workflows to complete comic setups and payoffs from the finished film. Preserve the channel's football comedy identity when adapting the pack's business-marketing examples.

Use the existing Pencil production workflow and tools for the first clips. Consider the official Remotion skills only if repeated caption animations, title layouts, or video variants justify a React-based editing layer. Add `ad-creative` if paid promotion becomes an actual requirement.

## Adoption and fit

Stars below were read directly from GitHub's repository API. They apply to the entire repository, not to an individual skill. Install counts are rounded values reported by skills.sh or its CLI, not unique active users or evidence of increased views.

| Source | GitHub stars | Reported relevant installs | Assessment |
|---|---:|---:|---|
| [Corey Haines Marketing Skills](https://github.com/coreyhaines31/marketingskills) | 50,590 | `social`: 63.9K; `ad-creative`: 112.4K | Best marketing starting point. `social` is immediately relevant; paid-ad modules can wait. |
| [Official Remotion Agent Skills](https://github.com/remotion-dev/skills) | 4,591 | `remotion-best-practices`: 527.2K; `remotion-captions`: 82.1K | Strongest coding-oriented companion for assembling and rendering social clips. Production guidance rather than audience strategy. |
| [Charlie Hills Social Media Skills](https://github.com/charlie947/social-media-skills) | 3,551 | `reels-scripting`: 1.3K, from the skills CLI | Relevant reference-analysis and script workflow, but designed around newsletter topics and creator voice. Selective adaptation required. |
| [Agency Agents](https://github.com/msitarzewski/agency-agents) | 152,855 | Individual role installs not verified | Large agent-prompt collection with YouTube, TikTok, and Instagram roles. Codex integration uses custom agents rather than ordinary standalone skills. Useful optional strategy references, more setup than needed initially. |

### 1. Corey Haines: social

[Current source](https://github.com/coreyhaines31/marketingskills/blob/main/skills/social/SKILL.md) · [Install listing](https://skills.sh/coreyhaines31/marketingskills/social)

Covers short-form hooks, video repurposing, standalone captions, content calendars, engagement, and performance review. Proposed use: identify the derby film's strongest standalone jokes, then package each for the three platforms. The current source folder and skill name are `social`; older listings also expose `social-content`.

```sh
npx skills add coreyhaines31/marketingskills --skill social
```

Optional for actual paid campaigns: [ad-creative](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ad-creative), for promotional variants and iteration from measured results.

```sh
npx skills add coreyhaines31/marketingskills --skill ad-creative
```

### 2. Remotion: production with code

[Maintainer documentation](https://github.com/remotion-dev/skills) · [Install counts](https://skills.sh/remotion-dev/skills)

The official repository explicitly supports Codex. Relevant skills include `remotion-best-practices`, `remotion-captions`, `remotion-create`, and `remotion-render`. They can guide video composition, text, captions, media timing, and export. This is optional: the SamToons film and production workflow already exist, and ordinary clipping does not require adopting a new renderer.

```sh
npx skills add remotion-dev/skills --skill remotion-best-practices
```

### 3. Charlie Hills: selective Reels scripting

[Reels source](https://github.com/charlie947/social-media-skills/blob/main/skills/reels-scripting/SKILL.md) · [Install listing](https://skills.sh/charlie947/social-media-skills/reels-scripting)

The full URL-analysis route uses Apify and Gemini credentials plus Node packages. Supplied video or transcript can bypass corresponding stages. It produces a script and caption; it does not include editing or publishing. Its fixed newsletter-to-Reel flow is less directly suited to a finished football cartoon than Corey's repurposing guidance.

```sh
npx skills add charlie947/social-media-skills --skill reels-scripting
```

The same pack's `hook-generator` is specifically a two-line LinkedIn hook workflow, and `youtube-thumbnail` assumes a creator portrait and Gemini prompt output. Neither should be presented as a ready-made SamToons workflow without adaptation.

### 4. Agency Agents: optional platform specialists

Relevant roles: [Video Optimization Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-video-optimization-specialist.md), [TikTok Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-tiktok-strategist.md), and [Instagram Curator](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-instagram-curator.md).

The maintainer provides conversion/install scripts for Codex custom agents. Treat role descriptions as reusable briefs, not verified expertise or performance results. Some instructions assert fixed CTR/algorithm thresholds and aggressive numerical targets without supporting evidence; those need independent checking before use.

## Lower-priority discoveries

- [sergebulaev/youtube-skills](https://github.com/sergebulaev/youtube-skills): directly relevant YouTube packaging and Shorts workflows, but only **29 stars** at this check. Does not meet the user's preference for widely adopted options.
- [blacktwist/social-media-skills](https://github.com/blacktwist/social-media-skills): **509 stars**; focuses on text-first social platforms, so weaker fit for this video-first channel.

## Source and evaluation notes

Checked the skills.sh leaderboard, specific package pages, `npx skills find reels`, GitHub repository metadata, and actual skill/agent instructions. Last observed repository pushes: Corey 5 September 2026; Remotion and Charlie 15 September; Agency Agents 12 September. Popularity is an adoption signal, not proof of fit or promised audience growth. Fixed platform limits and performance claims in skills should be verified when executing a campaign.

Live metadata endpoints: [Corey](https://api.github.com/repos/coreyhaines31/marketingskills), [Remotion](https://api.github.com/repos/remotion-dev/skills), [Charlie](https://api.github.com/repos/charlie947/social-media-skills), [Agency Agents](https://api.github.com/repos/msitarzewski/agency-agents). Counts will change after this dated snapshot.

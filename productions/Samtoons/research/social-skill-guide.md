# Using the social skill for SamToons

Installed 16 September 2026 from `coreyhaines31/marketingskills`, folder `skills/social`. Installed version: 2.2.0. Location: `/Users/samikd/.codex/skills/social/SKILL.md`. The installer completed successfully; its linked reference files were verified present.

## Start using it

The skill will be available on your next turn. Start a message with `$social`, then describe the result you want. You can also write “Use the social skill to…”. Codex can select a skill automatically when the request matches its description. If it does not appear, restart Codex and try again. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills).

Use the Pencil project so the assistant can inspect the SamToons film, scripts, and brand assets. The skill supplies marketing guidance for hooks, repurposing, captions, calendars, and performance reviews. Its installation does not connect social accounts or provide a video editor. Actual edits use the project's existing production workflow; publishing needs a separate request and available account access.

## SamToons context to supply in a new task

SamToons creates original animated football comedy and match parodies. The first completed film is the Manchester derby animation. The goal is to attract football fans, earn views on the full YouTube film, and build subscribers. The voice is playful football banter with expressive characters and complete jokes. The selected logo is the original coral S mascot. Match facts and authored parody remain distinct.

Sources in this workspace:

- Film: `/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/001-manchester-derby-2026-09-13/artifacts/delivery-v001/samtoons-final-1080p.mp4`
- Film context: `/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/001-manchester-derby-2026-09-13/brief.md`
- Brand kit: `/Users/samikd/MyProjects/Pencil/productions/Samtoons/branding/v001/README.md`
- Selected logo: `/Users/samikd/MyProjects/Pencil/productions/Samtoons/branding/v001/samtoons-logo.png`

## 1. Find the best moments

Copy this as the first request:

```text
$social Help promote SamToons' finished Manchester derby animation on YouTube Shorts, Instagram Reels, and TikTok. Read the project context and inspect the delivered film. Rank up to five standalone comedy moments that could become short clips. For each, give verified start/end timestamps, the hook, setup, payoff, suggested duration, and any problems adapting it to 9:16. Recommend the strongest three to make first. Keep every joke understandable to someone who has not seen the film. This step is a plan only.
```

Expected output: a small ranked clip list with concrete timestamps and edit notes. If the assistant cannot actually inspect a part of the film, it should mark that gap instead of inventing a viewing or timestamps.

## 2. Prepare the selected clip

After choosing a moment:

```text
$social Turn clip 1 into an edit brief. Give me three opening-hook options, precise cut points, on-screen text, subtitle treatment, and a short call to action for the full film. Preserve the original comic timing and dialogue. Then prepare a YouTube Shorts title and description, an Instagram caption, and a TikTok caption. Adapt each to the platform and use only relevant hashtags. Ask for the published full-video URL if a link is needed.
```

The resulting brief can be handed to the existing Pencil production workflow to make the clip. Marketing instructions do not replace the project's picture-and-sound review process.

## 3. Plan distribution

```text
$social Make a seven-day posting plan for our three selected clips across Shorts, Reels, and TikTok. Include the asset, caption, purpose, and follow-up for each post. Fit the schedule to what we can actually produce. Ask about the audience timezone and existing account data before proposing clock times. Label untested choices as experiments. Draft the plan without publishing.
```

## 4. Learn from results

Supply platform exports or a table with the clip, platform, posting date, views, watch time/retention where available, shares, comments, and new followers/subscribers. Then ask:

```text
$social Review these results separately by platform. Identify the strongest hook and joke, where viewers leave, and which clips attract followers or full-video viewers where attribution is available. Account for how long each post has been live and missing metrics. Recommend three specific changes for the next batch and distinguish observations from hypotheses.
```

## Keep requests focused

For good results, specify the source video, target audience, platforms, desired deliverable, and production capacity. Use the skill's templates selectively: SamToons is an entertainment channel, so software-sales examples and generic posting quotas should not dictate the creative treatment. Preserve a satisfying punchline in each standalone clip.

Source: [installed skill upstream](https://github.com/coreyhaines31/marketingskills/tree/main/skills/social). Only `social` was installed; the broader marketing pack and optional paid-ad or Remotion skills were not installed.

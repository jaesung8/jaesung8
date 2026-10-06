# GitHub profile maintenance

This independent repository maps to `jaesung8/jaesung8`. `README.md` is the public profile content; `assets/profile-banner.svg` is an original, committed banner. Preview files belong in ignored `.preview/`.

## Content preferences

- Lead with software development: the current development focus, projects, implementation work, and tools. Keep the quick-facts style of the original profile template. Use current facts rather than restoring outdated employment or learning claims from the old README.
- Use **AI Researcher at Auto-ID Labs Korea, KAIST** for the current position (**September 2026–Present**), following the user's 2026-10-06 wording preference. Keep administrative appointment titles in internal evidence.
- Introduce ClusterSplat as **First-author research** and RADBench / DashBench as **Collaborative research**. Do not state numerical coauthor rank or total author counts in introductory prose.
- Introduce only confirmed papers. Show the full paper title, conference, year, and Spotlight where applicable; omit redundant `accepted`, `acceptance`, `채택`, or `게재 예정` qualifiers in titles, tables, and introductory prose. Keep status/date provenance in internal evidence records rather than copying it into the profile. Do not invent publication dates, personal contributions, paper/code links, metrics, or contact details.
- Put Current focus, Development, and Tools before Selected research. Keep Selected research to one line per paper (venue, year, Spotlight, and role), with full titles in an expandable block. Describe past backend projects as experience rather than implying current employment or active maintenance. Do not invent active side projects or public code links. Group technology badges by actual use; avoid adding technologies simply to fill an icon wall.

## Visual structure

Retain the original profile's emoji headings and tools section. The banner uses navy, teal, and violet with an abstract Gaussian scene graph. The concise research list and expandable paper/career details use GitHub-supported Markdown and HTML; core content remains readable without images.

The banner is local. Static technology and navigation badges use Shields.io; they need external image access. Do not add custom CSS, scripts, or inline styles to the README: GitHub sanitizes them.

## Automated GitHub features (2026-10-06)

The user selected the activity rank/PR card, recent activity feed, and 3D contribution calendar. `.github/workflows/profile-activity.yml` runs daily at 06:00 Asia/Seoul and can also be dispatched manually. The action dependencies are pinned to reviewed upstream commits.

- Stats Extended generates light and dark SVGs in `assets/`, emphasizing commits, PRs, reviews, merged PRs, and merge percentage. The displayed rank is a composite activity indicator, not a review of PR code quality.
- `tools/update_activity.py` refreshes only the `START_SECTION:activity` / `END_SECTION:activity` block using the GitHub public events endpoint. Keep both markers exactly once. Exclude profile/site updates to keep generated commits from dominating the feed, and show an honest empty-state message when the recent event window has no qualifying activity.
- GitHub Profile 3D Contrib generates the contribution calendar; commit only the light green and night green SVGs referenced by the README. Respect the existing GitHub contribution visibility settings.

Use the repository's automatic `GITHUB_TOKEN`; no personal token or access to private repositories is configured. Commit generated SVGs so readers do not depend on a shared card server. Keep the last successful assets when generation fails; inspect the Actions run before claiming a refresh succeeded.

Sources: [Stats Action](https://github.com/stats-organization/github-readme-stats-action), [Stats options](https://github-stats-extended.vercel.app/frontend/docs/cards/stats/), [GitHub public events](https://docs.github.com/en/rest/activity/events#list-public-events-for-a-user), [3D Contrib](https://github.com/yoshi389111/github-profile-3d-contrib).

The personal-site repository is `jaesung8/jaesung8.github.io`. Publication was authorized on 2026-10-06. The source repository remains private, while its GitHub Pages site is public at [jaesung8.github.io](https://jaesung8.github.io/). The deployment workflow succeeded; retain links only to verified public destinations. Local edits are not publication.

## References reviewed on 2026-10-06

- [Anurag Hazra's profile](https://github.com/anuraghazra/anuraghazra): local hero artwork, technology icons, and visual section hierarchy. Visual reference only; original artwork and wording were not copied.
- [Sebastian Raschka's profile](https://github.com/rasbt/rasbt): concise introduction connecting AI research with software development.
- [Alexey Grigorev's profile](https://github.com/alexeygrigorev/alexeygrigorev): clearly separated areas of work.
- [GitHub formatting quickstart](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github): tables and expandable details.
- [GitHub Markup](https://github.com/github/markup): sanitization constraints.
- [Shields static badges](https://shields.io/badges/static-badge): badge paths, escaped hyphens, styles, and logos.
- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats): current maintenance and public-instance limitations.

# GitHub Profile Setup — Arafat Khan

## 1. Create the profile repository

Create a **public** repository named exactly:

`iamthearafatkhan`

## 2. Upload this structure

```text
iamthearafatkhan/
├── README.md
├── assets/
│   ├── profile-scan.png
│   ├── avatar-ascii.png
│   ├── profile-sequence.gif
│   └── github-stats.svg
└── .github/
    └── workflows/
        └── update-stats.yml
```

There is intentionally **no architecture.png**.

## 3. Commit to `main`

Upload/commit all files to the `main` branch.

## 4. Start the automatic stats

Go to:

**Repository → Actions → Update GitHub Profile Stats → Run workflow**

It also runs once per day.

## 5. Future repositories

Create another public repository normally.

Example:

`6 repos → create one → 7 repos`

The workflow fetches the current repository count from GitHub and updates `assets/github-stats.svg`. You do not manually change the number.

## 6. What you edit manually

Only add new curated project cards when you want to showcase a new project:

- project name
- GitHub link
- live demo link if available
- technology icons
- description

## 7. Why GIF?

GitHub README cannot run arbitrary JavaScript, so the scan animation is a GIF:

1. your profile-scan image appears
2. a scan line moves across it
3. scan completes
4. transition
5. ASCII avatar + identity panel appears

## 8. Profile views

GitHub does not expose an official public profile-view counter for a README. The profile-view badge therefore uses a third-party counter.

## 9. No architecture image

This version contains only:

- `profile-scan.png`
- `avatar-ascii.png`
- `profile-sequence.gif`
- `github-stats.svg`

No `architecture.png`.

## 10. If you change your identity text

Edit the Identity block in `README.md`. If you want the animated identity screen to change too, regenerate the GIF rather than manually editing a static image.

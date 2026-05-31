# MBBS Study Tracker

A static Next.js + Firebase web app for realtime MBBS chapter tracking, family accountability, revision reminders, analytics, and mobile-first progress updates.

## 1) Install

```bash
npm install
```

## 2) Environment variables

Copy `.env.example` to `.env.local` and fill in your Firebase web app values.

## 3) Firebase setup

1. Create a Firebase project.
2. Enable **Authentication → Google**.
3. Create a Firestore database.
4. Add a Web app and copy its config into `.env.local`.
5. Replace the placeholder emails in `firestore.rules` with your real brother and sister Google account emails.
6. Publish the rules.

## 4) Run locally

```bash
npm run dev
```

## 5) Build for Firebase Hosting

```bash
npm run build
```

The build outputs the static site into `out/` because `next.config.js` uses `output: 'export'`.

## 6) Deploy

```bash
firebase init hosting
firebase deploy
```

Use `out` as the public directory.

## 7) Firestore schema

Collections used:

- `users`
- `subjects`
- `chapters`
- `study_logs`
- `revision_queue`
- `analytics`

All records are scoped by `groupId` so the brother and sister share one live workspace.

## 8) Notes

- This app uses Firestore realtime listeners, not SSR.
- It is static-export compatible.
- The PWA manifest and service worker are included.
- Push notifications are browser-notification based; full remote push would need FCM + a backend.

## 9) Suggested Firebase rules update

Replace the placeholder emails in `firestore.rules` with the real authorized accounts.

## 10) First-seed data

The app seeds default subjects and chapters from the UI when a signed-in authorized user opens it.

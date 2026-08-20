# Constellation Transcript Development Rules

## Project Mission

Constellation Transcript is a lightweight, local-first Android/Termux
utility that converts available YouTube captions into verified plain-text
transcripts.

Version 1.0 is intentionally captions-only.

## Version 1.0 Architecture

All supported entry points must use the same Python application:

Android Share
    -> android/termux-url-opener
    -> constellation_transcript.py

Interactive launch
    -> constellation_transcript.py

The application flow is:

URL input
    -> security validation
    -> YouTube metadata retrieval
    -> caption retrieval
    -> transcript cleanup
    -> controlled export
    -> read-back verification
    -> exit

Do not duplicate transcript-processing logic inside Android integration
scripts or future launchers.

## Security Boundaries

These requirements must not be weakened without explicit review and approval.

- Local execution only.
- No listening network ports.
- No HTTP server.
- No remote administration.
- No telemetry or analytics.
- No hidden functionality or maintenance access.
- No automatic update mechanism.
- No background service or daemon.
- No cloud transcription.
- No automatic audio or video download fallback.
- No shell execution constructed from untrusted URL input.
- Only approved HTTPS YouTube hosts may reach yt-dlp.
- Final transcript files may only be created through the controlled
  filesystem/export path.
- Credentials, API keys, and secrets must not be stored in the repository.

## Phone Stability Rules

Protecting Android device stability is a release requirement.

Do not add or modify any capability involving:

- Android system settings
- accessibility services
- display overlays
- touchscreen/input control
- device administration
- persistent background processes
- wake locks
- boot receivers
- listening sockets
- continuous polling
- aggressive CPU or memory workloads

unless the capability has first been explicitly reviewed and approved.

Do not make system-level Termux or Android changes merely to solve an
application-level problem.

## Dependency Rules

- Do not add new Python packages without explicit approval.
- Prefer the Python standard library when practical.
- Prefer existing project dependencies over introducing new ones.
- Do not add automatic package installation.
- Do not add automatic model downloads.
- Dependency upgrades must be deliberate and tested.

## AI Development Rules

Treat every AI coding task as a small software-engineering task.

Before editing:

1. Identify the exact objective.
2. Identify the files that must be read.
3. Identify the files permitted to change.
4. State important behavior that must remain unchanged.
5. Define how the change will be tested.

During implementation:

- Make the smallest change that satisfies the task.
- Do not refactor unrelated code.
- Do not add speculative features.
- Do not change architecture without explicit approval.
- Do not weaken validation or security boundaries.
- Do not silently choose behavior when requirements are ambiguous.
- If an ambiguity materially changes behavior, present the alternatives
  and trade-offs before implementation.

After implementation:

1. Review the diff.
2. Explain why every changed file changed.
3. Run relevant tests.
4. Confirm security boundaries remain intact.
5. Confirm no unexpected files were created.
6. Commit only after review.

## Git Rules

- Keep commits small and focused.
- Maintain a working known-good checkpoint.
- Do not combine unrelated changes in one commit.
- Do not force-push release history.
- If a change becomes confusing or unstable, return to the last known-good
  checkpoint instead of stacking speculative fixes.

## Version 1.0 Scope

Included:

- Interactive YouTube URL input
- Command-line YouTube URL input
- Android Share integration
- Approved HTTPS YouTube URL validation
- Public video metadata retrieval
- English manual or automatic caption retrieval
- WebVTT-to-text cleanup
- Temporary caption cleanup
- Safe transcript filename generation
- Atomic transcript export
- Existing-file preservation
- Read-back transcript verification
- Controlled error handling

Excluded from Version 1.0:

- Whisper
- Local speech recognition
- Personal-media transcription
- Cloud processing
- Remote processing
- Backend services
- Remote administration
- Telemetry
- Automatic updates
- Audio/video fallback
- Unreviewed new features

## Known Pre-1.0 Review Items

The following were identified during the Version 0.9.0 architecture audit
and should be handled through separate, testable tasks:

1. Cache/job directory creation in transcript.py occurs before the main
   exception-handling block and should be tested for controlled failure.

2. Pure YouTube playlist URLs are currently accepted by URL validation even
   though Constellation Transcript is intended to process one video per
   invocation.

3. CHANGELOG.md contains a stale roadmap entry identifying Version 0.9.0 as
   the Home Screen Launcher milestone.

These items are observations, not authorization for broad refactoring.

## Release Principle

Version 1.0 is complete when the defined captions-only application is
stable, tested, documented, secure within its stated boundaries, and
reproducibly performs its intended workflow.

Do not delay Version 1.0 by adding unrelated features.

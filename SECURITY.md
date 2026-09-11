# Security Policy

## Reporting a Security Issue

Please do not report suspected security vulnerabilities through public GitHub Issues.

Instead, use GitHub's private vulnerability reporting or security advisory features when available.

When reporting a security issue, please include:

- A clear description of the issue
- Steps to reproduce it
- The affected version or commit
- Any relevant logs or screenshots
- The potential security impact

Please do not include passwords, authentication codes, API keys, private credentials,
personal information, or other sensitive data in reports.

## Project Security Boundaries

Constellation Transcript is intentionally designed as a local-first application.

The project does not intentionally provide:

- Remote administration
- Listening network services
- Telemetry or analytics
- Hidden access mechanisms
- Automatic update mechanisms
- Cloud transcription
- Background daemons or services

Security reports that indicate a violation of these boundaries are especially important.

## Response Expectations

Security reports will be reviewed as promptly as practical.

If a reported issue is confirmed, the goal will be to:

1. Understand the scope and impact
2. Develop and test a focused fix
3. Avoid unnecessary architectural expansion
4. Publish an appropriate update or advisory

## Supported Versions

The current public stable release is the supported version for security fixes.
Older development snapshots or unpublished branches may not receive security updates.

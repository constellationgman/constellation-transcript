# Constellation Transcript Changelog

All notable changes to this project are documented in this file.

This project follows a milestone-based development process toward Version 1.0.

---

## Version 0.7.0 — Project Identity

Released: July 2026

### Added
- Official project name: **Constellation Transcript**
- Expanded project documentation
- Defined project mission and security boundaries
- Improved README with installation and usage information

### Changed
- Renamed `yt2text.py` to `constellation_transcript.py`
- Updated application branding throughout the project
- Updated version information

### Security
- Confirmed local-only execution model remains unchanged
- Confirmed no telemetry
- Confirmed no hidden functionality
- Confirmed no remote administration
- Confirmed no new network entry points

---

## Version 0.6.0 — Secure Export System

### Added
- Secure transcript export module
- Atomic file writing
- Filename sanitization
- Automatic filename collision handling
- Transcript verification after writing
- Export error handling

### Security
- Prevent accidental overwriting of existing transcripts
- Verify exported data before reporting success

---

## Version 0.5.0 — Caption Processing

### Added
- Caption retrieval using yt-dlp
- Automatic caption download
- WebVTT parser
- Transcript cleanup
- Duplicate caption removal
- Temporary cache directory
- Automatic cache cleanup

### Improved
- Cleaner transcript formatting
- More reliable caption extraction

---

## Version 0.4.0 — YouTube Metadata Engine

### Added
- YouTube metadata retrieval
- Video title detection
- Channel detection
- Duration detection
- Caption availability detection
- `youtube_client.py` module
- `VideoInfo` data structure

### Improved
- Metadata retrieval without downloading media

---

## Version 0.3.0 — Configuration System

### Added
- Centralized configuration module
- Version tracking
- Program name configuration
- Output directory configuration
- Cache directory configuration
- Approved YouTube hostname list
- Maximum URL length configuration

### Improved
- Removed hard-coded values throughout the project

---

## Version 0.2.0 — Security Foundation

### Added
- HTTPS URL validation
- Approved YouTube domain validation
- URL input validation
- Security module
- Modular project architecture

### Security
- Reject non-HTTPS URLs
- Reject unsupported domains
- Reject malformed URLs

---

## Version 0.1.0 — Initial Prototype

### Added
- Initial executable application
- Python project structure
- Manual URL input
- Foundation for future development

---

# Road to Version 1.0

Planned milestones:

- **0.8.0** — Android Share Integration
- **0.9.0** — Home Screen Launcher
- **1.0.0** — Stable Release

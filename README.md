<p align="center">
  <img src="logo.png" width="300" alt="Constellation Transcript logo">
</p>

# Constellation Transcript

Constellation Transcript converts available YouTube captions into verified
plain-text files on an Android device through Termux>

## Development Status

**Current Version:** 0.8.0

### Completed

- ✅ 0.1.0 – Initial Prototype
- ✅ 0.2.0 – Security Foundation
- ✅ 0.3.0 – Configuration System
- ✅ 0.4.0 – YouTube Metadata Engine
- ✅ 0.5.0 – Caption Processing
- ✅ 0.6.0 – Secure Export System
- ✅ 0.7.0 – Project Identity
- ✅ 0.7.1 – GitHub Integration
- ✅ 0.8.0 – Dual Input Support (Interactive + Command Line)

### Next Milestones

- ⏳ 0.8.1 – Android Share Integration
- ⏳ 0.9.0 – Home Screen Launcher
- ⏳ 1.0.0 – Stable Release

## Current capabilities

- Validates approved HTTPS YouTube URLs
- Retrieves public video metadata
- Detects manual and automatic captions
- Retrieves English captions without downloading video or audio
- Cleans WebVTT captions into readable text
- Deletes temporary caption files
- Exports transcripts using atomic file writes
- Reads exported files back to verify their contents
- Preserves existing transcripts instead of overwriting them
- Accepts YouTube URLs from the command line
- Supports both interactive and automated execution

## Security design

- Local execution only
- No listening network services
- No remote administration
- No telemetry or analytics
- No hidden maintenance access
- No automatic code updates
- No cloud transcription
- No shell execution using untrusted URLs
- New capabilities require review before implementation

## Output location

Transcripts are saved to:

Documents/YouTubeText

## Run manually

From the project directory:

```bash
python constellation_transcript.py

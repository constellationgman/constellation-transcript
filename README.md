<p align="center">
  <img src="logo.png" width="300" alt="Constellation Transcript logo">
</p>

# Constellation Transcript

Constellation Transcript is a lightweight Android/Termux utility that converts
available YouTube captions into verified plain-text transcripts.

Its primary purpose is to turn intentionally selected YouTube material into
portable text suitable for reading, research, and AI-assisted learning.

## Why Constellation Transcript?

Constellation Transcript is built for people who want useful text from YouTube
without downloading video, uploading media to a cloud service, or running a
background server.

The project favors a small, auditable codebase, explicit security boundaries,
and predictable local files over unnecessary complexity.

## Installation

Constellation Transcript 1.0 is captions-only software for Android/Termux.
It runs locally on your phone and requires no account or cloud service.

### 1. Install Python and Git

In Termux:

```bash
pkg update
pkg install python git
```

### 2. Clone the repository

The Android Share bridge requires the repository at exactly this location:

```bash
git clone https://github.com/constellationgman/constellation-transcript.git ~/constellation-transcript
```

### 3. Install dependencies

```bash
cd ~/constellation-transcript
python -m pip install -r requirements.txt
```

### 4. Grant storage permission

Run the following command and accept the storage permission prompt when Android asks.

```bash
termux-setup-storage
```

This allows the program to write transcripts to Android shared storage.
The output directory (`Documents/YouTubeText/`) is created automatically when needed.

### 5. Install the Share bridge

```bash
mkdir -p ~/bin
cp ~/constellation-transcript/android/termux-url-opener ~/bin/termux-url-opener
chmod +x ~/bin/termux-url-opener
```

### Using Android Share

Once the Share bridge is installed:

1. Open a YouTube video in the YouTube app or another app that can share its YouTube URL.
2. Tap **Share**.
3. Choose **Termux**.

Termux opens and displays the program's progress; when processing succeeds, the transcript is saved to `Documents/YouTubeText/`.

## Development Status

**Current Version:** 1.0.0

### Completed

- ✅ 0.1.0 – Initial Prototype
- ✅ 0.2.0 – Security Foundation
- ✅ 0.3.0 – Configuration System
- ✅ 0.4.0 – YouTube Metadata Engine
- ✅ 0.5.0 – Caption Processing
- ✅ 0.6.0 – Secure Export System
- ✅ 0.7.0 – Project Identity
- ✅ 0.7.1 – GitHub Integration
- ✅ 0.8.0 – Dual Input Support
- ✅ 0.8.1 – Android Share Integration
- ✅ 0.9.0 – Release Candidate Cleanup
- ✅ 1.0.0 – First Stable Captions-Only Release

## Current Capabilities

- Accepts YouTube links directly from Android's Share menu
- Runs the transcript workflow without manual copy and paste
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

## Version 1.0 Scope

Constellation Transcript 1.0 is intentionally captions-only and processes
exactly one selected YouTube video per invocation.

Pure playlist URLs are rejected. A single video opened from within a playlist
remains supported and only that selected video is processed.

If usable English YouTube captions are unavailable, the program stops without
downloading the video's audio or video.

Offline speech recognition, personal-media transcription, cloud processing,
and remote processing are not part of Version 1.0.

## Project Philosophy

Constellation Transcript is intentionally narrow in scope.

The goal is not to build a general-purpose media platform. The goal is to solve
one useful problem well: turn intentionally selected YouTube captions into
clean, portable text with minimal complexity and clear security boundaries.

New capabilities are considered carefully so the project remains understandable,
auditable, and easy to adapt.

## Security Design

- Local execution only
- No listening network services
- No remote administration
- No telemetry or analytics
- No hidden maintenance access
- No automatic code updates
- No cloud transcription
- No shell execution using untrusted URLs
- New capabilities require review before implementation

## Output Location

Transcripts are saved to:

```text
Documents/YouTubeText
```

## Run Manually

From the project directory:

```bash
python constellation_transcript.py
```

The recommended everyday workflow is:

**YouTube → Share → Termux**

Constellation Transcript then retrieves available captions and saves the
verified transcript automatically.

## Feedback and Contributions

Bug reports, compatibility issues, and focused improvement ideas are welcome through GitHub Issues.

Please keep proposed changes aligned with the project's goals: local-first operation,
minimal complexity, clear security boundaries, and a narrow problem scope.

Large feature expansions, remote services, telemetry, and unrelated platform growth
are outside the project's current direction.

## License

This project is released under the MIT License. See the `LICENSE` file for details.


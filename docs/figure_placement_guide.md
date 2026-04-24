
# Where to Add Pictures in the Report

## Quick Summary

| # | Figure | Chapter & Section | How to Get It |
|---|---|---|---|
| 1 | System Architecture Diagram | Ch 4.1 | Draw in draw.io / PowerPoint |
| 2 | Data Flow Diagram | Ch 4.4 | Draw in draw.io / PowerPoint |
| 3 | Home Page (Idle State) | Ch 3.1.2 or Ch 4.2 | Screenshot of app |
| 4 | Recording State | Ch 3.1 or Ch 5.1 | Screenshot while recording |
| 5 | Processing Loader | Ch 3.1.2 | Screenshot during API call |
| 6 | Pipeline Output (Tamil + English + ISL tags) | Ch 3.2 or Ch 6.1 | Screenshot after processing |
| 7 | Video Playing with Avatar | Ch 3.2 or Ch 6.1 | Screenshot during playback |
| 8 | Fingerspelling Fallback | Ch 5.7 | Screenshot of [Spell] display |
| 9 | Latency Metrics Panel | Ch 5.8 or Ch 6.1 | Screenshot after playback |
| 10 | NLP Transformation Flowchart | Ch 5.4 | Draw in draw.io |
| 11 | API Request-Response Flow | Ch 4.5 | Draw in draw.io |
| 12 | Project Folder Structure | Ch 4.1 | Screenshot of VS Code explorer |
| 13 | 2D Avatar Gallery | Ch 3.2 or Ch 5.6 | Collage of avatar PNGs |

---

## Detailed Placement Guide

### CHAPTER 1: INTRODUCTION

No pictures needed here — this is all text.

---

### CHAPTER 2: LITERATURE SURVEY

**No mandatory pictures**, but you CAN add:

> **Figure 2.1** — Comparison table of existing systems (already in your report as a table — keep it as a table, no picture needed)

---

### CHAPTER 3: SPRINT PLANNING

#### Section 3.1.2 (Sprint I — Functional Document)

> **Figure 3.1 — Home Page Interface (Idle State)**
> Screenshot of your app at http://127.0.0.1:8000 showing the three-panel layout with "Start Recording" button, empty pipeline, and video placeholder.
> 📸 *How: Run the app → take a full browser screenshot*

> **Figure 3.2 — Recording State with Waveform Animation**
> Screenshot showing the red pulsing "Stop Recording" button and animated waveform bars.
> 📸 *How: Click Start Recording → quickly screenshot the waveform*

> **Figure 3.3 — Processing Loader**
> Screenshot showing the spinning loader and "Processing audio via FastAPI..." text.
> 📸 *How: Submit audio → quickly screenshot during loading*

#### Section 3.2.4 (Sprint II — Outcome)

> **Figure 3.4 — Translation Pipeline Output**
> Screenshot showing all three pipeline stages filled: Tamil text, English translation, and ISL word tags (with one tag highlighted/active).
> 📸 *How: Process any Tamil audio → screenshot the left panel*

> **Figure 3.5 — Video Player with 2D Avatar During Playback**
> Screenshot showing the sign video playing on the left, 2D avatar on the right, word overlay at the bottom of the video, and progress bar below.
> 📸 *How: Process audio → screenshot during video playback*

---

### CHAPTER 4: SYSTEM ARCHITECTURE AND DESIGN

#### Section 4.1 (Overall Architecture)

> **Figure 4.1 — System Architecture Diagram**
> A block diagram showing:
> ```
> [Browser/Frontend] ←→ [FastAPI Backend] ←→ [Google APIs]
>       ↕                    ↕
>  [RecordRTC]        [ISL_Dataset/]
>  [HTML5 Video]      [dataset/]
> ```
> 🎨 *How: Draw in draw.io, PowerPoint, or Canva. Show three boxes: Frontend, Backend, External APIs. Add arrows showing data flow.*

#### Section 4.2 (Frontend Architecture)

> **Figure 4.2 — Frontend Three-Panel Layout**
> Annotated screenshot of the app with labels pointing to:
> - Input Panel (top-left)
> - Processing Panel (bottom-left)  
> - Output Panel (right)
> 📸 *How: Take a screenshot → add labels/arrows in PowerPoint or Paint*

#### Section 4.4 (Data Flow)

> **Figure 4.3 — Data Flow Diagram (Tamil Speech → ISL Video)**
> A flowchart showing the 5 pipeline stages:
> ```
> Tamil Speech → [STT] → Tamil Text → [Translate] → English
>     → [NLP] → ISL Words → [Video Map] → Video Playback
> ```
> 🎨 *How: Draw in draw.io with boxes and arrows. Use different colors for each stage.*

#### Section 4.5 (API Design)

> **Figure 4.4 — API Request-Response Flow**
> Diagram showing:
> - Browser sends POST /api/process-audio → Backend returns JSON
> - Browser sends GET /api/video/go → Backend returns MP4
> - Browser sends GET /api/avatar/go → Backend returns PNG
> 🎨 *How: Draw in draw.io or PowerPoint*

---

### CHAPTER 5: IMPLEMENTATION DETAILS

#### Section 5.4 (NLP Processing)

> **Figure 5.1 — NLP Transformation Pipeline**
> A flowchart showing the worked example:
> ```
> "I am going to school"
>     ↓ Tokenize
> ["i", "am", "going", "to", "school"]
>     ↓ Remove stopwords
> ["i", "going", "school"]
>     ↓ Lemmatize
> ["i", "go", "school"]
>     ↓ Uppercase
> ["I", "GO", "SCHOOL"]
> ```
> 🎨 *How: Draw in draw.io or PowerPoint with boxes and arrows*

#### Section 5.6 (Video Mapping)

> **Figure 5.2 — 2D Avatar Gallery (Sample)**
> A collage/grid showing 6-8 sample avatar images from your dataset/2d_avatars/ folder, such as: avatar_hello.png, avatar_go.png, avatar_eat.png, avatar_help.png, etc.
> 📸 *How: Open 6-8 avatar PNGs → arrange in a grid in PowerPoint → save as image*

#### Section 5.7 (Sequential Playback)

> **Figure 5.3 — Fingerspelling Fallback Display**
> Screenshot showing the "[Spell] WORD" overlay and yellow warning bar when a word is not found in the dataset.
> 📸 *How: Process audio containing a rare word → screenshot the fallback*

---

### CHAPTER 6: RESULTS AND DISCUSSIONS

#### Section 6.1 (Project Outcomes)

> **Figure 6.1 — Complete System Output (Full Pipeline)**
> A FULL screenshot showing the entire app after a successful translation:
> - Left: Tamil text, English translation, ISL tags
> - Right: Video playing, avatar, word overlay, progress bar
> - Bottom: Latency metrics visible
> 📸 *How: Process "நான் பள்ளிக்கு செல்கிறேன்" → screenshot everything*

> **Figure 6.2 — Latency Metrics Display**
> Close-up screenshot of the latency panel showing End-to-End Latency and Avg Latency/Word values.
> 📸 *How: Crop from the full screenshot above*

---

## How to Capture Screenshots

1. **Run your app**: `python -m uvicorn backend.main:app --reload`
2. **Open**: http://127.0.0.1:8000
3. **Use Windows Snipping Tool** (Win+Shift+S) for clean captures
4. **For diagrams**: Use [draw.io](https://app.diagrams.net/) (free) — export as PNG at 300 DPI

---

## Priority Order (If Short on Time)

If you can only add a few pictures, these are the **MUST-HAVE** ones:

| Priority | Figure | Why |
|---|---|---|
| ⭐⭐⭐ | System Architecture Diagram (4.1) | Every report needs this |
| ⭐⭐⭐ | Full System Output Screenshot (6.1) | Proves the system works |
| ⭐⭐⭐ | Data Flow Diagram (4.3) | Shows the pipeline clearly |
| ⭐⭐ | NLP Transformation Flowchart (5.1) | Shows core logic visually |
| ⭐⭐ | Video + Avatar Playback (3.5) | Shows the main output |
| ⭐ | Home Page Screenshot (3.1) | Shows the UI design |
| ⭐ | Avatar Gallery (5.2) | Shows dataset work |


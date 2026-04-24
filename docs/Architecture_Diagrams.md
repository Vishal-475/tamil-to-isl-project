# Architecture Diagrams

Here are two detailed architectural diagrams for your project report. The first shows the overall system components (Frontend, Backend, Data, Cloud APIs), and the second details the exact step-by-step data flow through your translation pipeline.

*(Note: These are written in standard Mermaid charting syntax. You can take screenshots of the rendered diagrams below, or copy-paste the raw Mermaid code into a tool like [Mermaid Live Editor](https://mermaid.live/) to export high-quality PNG or SVG images for your Word document.)*

## 1. Overall System Architecture Diagram

This diagram illustrates the three-tier architecture of your system, showing how the frontend interacts with the FastAPI backend, local datasets, and external cloud services.

```mermaid
flowchart TB
    %% Styling
    classDef frontend fill:#1e1e1e,stroke:#00d2ff,stroke-width:2px,color:#fff
    classDef backend fill:#2c2c2c,stroke:#4CAF50,stroke-width:2px,color:#fff
    classDef data fill:#2c2c2c,stroke:#ff9800,stroke-width:2px,color:#fff
    classDef cloud fill:#0d47a1,stroke:#64b5f6,stroke-width:2px,color:#fff

    subgraph Frontend["Presentation Tier (Frontend Browser)"]
        direction TB
        UI["User Interface (HTML/CSS)"]:::frontend
        Rec["RecordRTC (Audio Capture)"]:::frontend
        Video["Video Player & Avatar rendering"]:::frontend
    end

    subgraph Backend["Application Tier (FastAPI Backend)"]
        direction TB
        API["FastAPI Entry Point (main.py)"]:::backend
        AudioProc["Audio Processing (FFmpeg + pydub)"]:::backend
        NLP_Mod["NLP Engine (nlp_processor.py)"]:::backend
    end

    subgraph Storage["Data Tier (Local Filesystem)"]
        direction TB
        ISL["ISL_Dataset (Primary MP4s)"]:::data
        Mock["dataset (Fallback MP4s)"]:::data
        Avatr["dataset/2d_avatars (PNGs)"]:::data
    end

    subgraph Cloud["External Cloud Services"]
        direction TB
        GSTT["Google Speech-to-Text API"]:::cloud
        GTrans["Google Translate API"]:::cloud
    end

    %% Network Connections
    Rec -- "POST /api/process-audio" --> API
    UI -- "GET /api/video/{word}" --> API
    UI -- "GET /api/avatar/{word}" --> API
    
    API --> AudioProc
    API --> NLP_Mod
    
    %% External API calls
    AudioProc -- "Audio Chunks" --> GSTT
    GSTT -- "Tamil Text" --> API
    API -- "Tamil Text" --> GTrans
    GTrans -- "English Translation" --> API
    
    %% Data Access
    API -. "Read Video" .-> ISL
    API -. "Read Video" .-> Mock
    API -. "Read Image" .-> Avatr
    
    %% Output to Frontend
    API -- "JSON Response + Media Streams" --> Video
```

---

## 2. Translation Pipeline Data Flow Diagram

This flowchart outlines the chronological data processing pipeline, tracing the input from the moment the user speaks until the ISL video is played on screen.

```mermaid
flowchart TD
    %% Styling
    classDef input fill:#4CAF50,stroke:#388E3C,color:#fff
    classDef process fill:#2196F3,stroke:#1976D2,color:#fff
    classDef nlp fill:#9C27B0,stroke:#7B1FA2,color:#fff
    classDef output fill:#FF9800,stroke:#F57C00,color:#fff

    A["User Speaks Tamil"]:::input --> B["RecordRTC captures 16kHz WAV"]:::process
    B --> C["Upload via /api/process-audio"]:::process
    C --> D["temp_audio file saved"]:::process
    
    subgraph Audio Prep
        D --> E["FFmpeg: Verify/Force 16kHz Mono WAV"]:::process
        E --> F["pydub: split_on_silence into chunks"]:::process
    end
    
    subgraph Translation Phase
        F --> |"Audio Chunks"| G["Google Speech-to-Text (ta-IN)"]:::process
        G --> |"Recognized Strings"| H["Concatenate Text"]:::process
        H --> |"Tamil Text string"| I["deep-translator GoogleTranslator"]:::process
        I --> |"English Text string"| J["ISLConverter.english_to_isl"]:::nlp
    end
    
    subgraph NLP Transformation
        J --> K["NLTK: Tokenize Words"]:::nlp
        K --> L["NLTK: Remove Stopwords (Keep Pronouns)"]:::nlp
        L --> M["NLTK: WordNetLemmatizer (pos='v')"]:::nlp
        M --> N["Uppercase Words"]:::nlp
    end
    
    N --> |"List of ISL Words"| O{"Video Mapping"}:::process
    
    O --> |"Primary Check"| P["Found in ISL_Dataset/"]:::output
    O --> |"Fallback Check"| Q["Found in dataset/"]:::output
    O --> |"Not Found"| R["Mark for [Spell] Fallback"]:::output
    
    P --> S["Format JSON Response"]:::process
    Q --> S
    R --> S
    
    subgraph Frontend Rendering
        S --> T["Sequence Player (playNextVideo)"]:::output
        T --> U["Update word overlay & 2D Avatar Image"]:::output
        T --> V["Play Video (onended event hooks next)"]:::output
    end
```

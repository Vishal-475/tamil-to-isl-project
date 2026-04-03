// DOM Elements
const recordBtn = document.getElementById('recordBtn');
const audioUpload = document.getElementById('audioUpload');
const recordingStatus = document.getElementById('recordingStatus');
const uploadStatus = document.getElementById('uploadStatus');
const fileNameDisplay = document.getElementById('fileName');
const processBtn = document.getElementById('processBtn');
const processingLoader = document.getElementById('processingLoader');
const errorMsg = document.getElementById('errorMsg');
const errorText = document.getElementById('errorText');

const tamilOutput = document.getElementById('tamilOutput');
const englishOutput = document.getElementById('englishOutput');
const islOutput = document.getElementById('islOutput');

const videoPlayer = document.getElementById('islVideoPlayer');
const videoPlaceholder = document.getElementById('videoPlaceholder');
const currentWordOverlay = document.getElementById('currentWordOverlay');
const missingWordWarning = document.getElementById('missingWordWarning');
const avatarContainer = document.getElementById('avatarContainer');
const avatarImage = document.getElementById('avatarImage');

const videoControls = document.getElementById('videoControls');
const replayBtn = document.getElementById('replayBtn');
const progressFill = document.getElementById('progressFill');
const sequenceCounter = document.getElementById('sequenceCounter');

// Audio variables
let mediaStream = null;
let recordRTC = null;
let audioBlob = null;
let isRecording = false;

// Video Data
let videoSequence = [];
let currentVideoIndex = 0;
let isPlaying = false;

// Latency Data
let sequenceStartTime = null;
let cumulativeE2eLatency = 0;
let cumulativeWordCount = 0;
const latencyDisplay = document.getElementById('latencyDisplay');
const e2eLatencyValue = document.getElementById('e2eLatencyValue');
const avgLatencyValue = document.getElementById('avgLatencyValue');

// API URL (Relative to origin as backend serves static)
const API_URL = '/api/process-audio';

// =============== AUDIO RECORDING HANDLING ===============
recordBtn.addEventListener('click', async () => {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // Use RecordRTC to reliably capture cross-browser PCM WAV
        recordRTC = RecordRTC(mediaStream, {
            type: 'audio',
            mimeType: 'audio/wav',
            recorderType: StereoAudioRecorder,
            desiredSampRate: 16000,
            numberOfAudioChannels: 1 // Mono is better for SpeechRecognition
        });

        recordRTC.startRecording();
        isRecording = true;

        // UI Updates
        recordBtn.innerHTML = `<i class="fa-solid fa-stop"></i> Stop Recording`;
        recordBtn.classList.add('recording');
        recordingStatus.classList.remove('hidden');
        uploadStatus.classList.add('hidden');
        resetPipeline();

    } catch (err) {
        showError("Microphone access denied or not available.");
        console.error("Mic error:", err);
    }
}

function stopRecording() {
    if (!isRecording || !recordRTC) return;

    recordRTC.stopRecording(function () {
        audioBlob = recordRTC.getBlob();

        // Stop mic stream
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            mediaStream = null;
        }

        isRecording = false;

        sequenceStartTime = performance.now(); // Start timing

        const file = new File([audioBlob], "recorded_audio.wav", { type: 'audio/wav' });
        processAudioFile(file);

        // UI Updates
        recordBtn.innerHTML = `<i class="fa-solid fa-microphone"></i> Start Recording`;
        recordBtn.classList.remove('recording');
        recordingStatus.classList.add('hidden');
    });
}


// =============== FILE UPLOAD HANDLING ===============
audioUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        if (!file.name.match(/\.(wav|mp3|ogg)$/i)) {
            showError("Please upload a .wav or .mp3 file.");
            e.target.value = ''; // Reset
            return;
        }

        // UI Updates
        recordingStatus.classList.add('hidden');
        uploadStatus.classList.remove('hidden');
        fileNameDisplay.textContent = file.name;
        audioBlob = file;
        resetPipeline();
        
        e.target.value = ''; // Allow selecting the same file again
    }
});

processBtn.addEventListener('click', () => {
    if (audioBlob) {
        sequenceStartTime = performance.now(); // Start timing
        processAudioFile(audioBlob);
    }
});

// =============== BACKEND PROCESSING ===============
async function processAudioFile(file) {
    uploadStatus.classList.add('hidden');
    processingLoader.classList.remove('hidden');
    errorMsg.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Server error processing audio");
        }

        const data = await response.json();
        updatePipelineUI(data);
        startVideoSequence(data.video_sequence);

    } catch (err) {
        showError(err.message);
    } finally {
        processingLoader.classList.add('hidden');
    }
}

// =============== UI UPDATES ===============
function updatePipelineUI(data) {
    tamilOutput.textContent = data.tamil_text;
    tamilOutput.classList.remove('placeholder');

    englishOutput.textContent = data.english_text;
    englishOutput.classList.remove('placeholder');

    islOutput.innerHTML = '';

    data.video_sequence.forEach(item => {
        const span = document.createElement('span');
        span.className = `isl-tag ${!item.found ? 'missing' : ''}`;
        span.textContent = item.word;
        if (!item.found) span.title = "Fingerspelling fallback";
        islOutput.appendChild(span);
    });
}

function resetPipeline() {
    tamilOutput.textContent = "Awaiting input...";
    tamilOutput.classList.add('placeholder');

    englishOutput.textContent = "Awaiting translation...";
    englishOutput.classList.add('placeholder');

    islOutput.innerHTML = '<span class="placeholder-tag">Wait...</span>';

    videoPlaceholder.classList.remove('hidden');
    currentWordOverlay.classList.add('hidden');
    missingWordWarning.classList.add('hidden');
    videoControls.classList.add('disabled');
    avatarContainer.classList.add('hidden');
    avatarContainer.classList.remove('signing');
    avatarImage.src = 'avatar.png';

    videoPlayer.src = "";
    videoSequence = [];

    // Reset Latency Display (retain overall avg latency if already set)
    if (latencyDisplay) {
        e2eLatencyValue.textContent = '-';
        if (cumulativeWordCount === 0) {
            latencyDisplay.classList.add('hidden');
            avgLatencyValue.textContent = '-';
        }
    }
}

function showError(msg) {
    errorMsg.classList.remove('hidden');
    errorText.textContent = msg;
    processingLoader.classList.add('hidden');
}

// =============== VIDEO PLAYBACK LOGIC ===============
function startVideoSequence(sequence) {
    if (!sequence || sequence.length === 0) return;

    videoSequence = sequence;
    currentVideoIndex = 0;

    videoPlaceholder.classList.add('hidden');
    videoControls.classList.remove('disabled');
    avatarContainer.classList.remove('hidden');

    // Display Latency Metrics
    if (sequenceStartTime) {
        const endTime = performance.now();
        const e2eLatency = (endTime - sequenceStartTime) / 1000; // in seconds
        const wordCount = sequence.length || 1;
        
        cumulativeE2eLatency += e2eLatency;
        cumulativeWordCount += wordCount;
        
        const avgLatency = cumulativeE2eLatency / cumulativeWordCount;

        if(e2eLatencyValue && avgLatencyValue && latencyDisplay) {
            e2eLatencyValue.textContent = e2eLatency.toFixed(2) + ' s';
            avgLatencyValue.textContent = avgLatency.toFixed(2) + ' s';
            latencyDisplay.classList.remove('hidden');
        }

        sequenceStartTime = null; // Reset for next run
    }

    playNextVideo();
}

function playNextVideo() {
    if (currentVideoIndex >= videoSequence.length) {
        // Sequence finished
        videoPlayer.pause();
        currentWordOverlay.classList.add('hidden');
        progressFill.style.width = '100%';
        avatarContainer.classList.remove('signing');
        return;
    }

    const currentItem = videoSequence[currentVideoIndex];

    // Highlight tag
    document.querySelectorAll('.isl-tag').forEach((el, idx) => {
        if (idx === currentVideoIndex) el.classList.add('active');
        else el.classList.remove('active');
    });

    // Update counter & progress
    sequenceCounter.textContent = `${currentVideoIndex + 1} / ${videoSequence.length}`;
    progressFill.style.width = `${((currentVideoIndex + 1) / videoSequence.length) * 100}%`;

    if (currentItem.found && currentItem.video_url) {
        // Play video
        missingWordWarning.classList.add('hidden');
        currentWordOverlay.textContent = currentItem.word;
        currentWordOverlay.classList.remove('hidden');
        avatarContainer.classList.add('signing');

        // Update 2D Avatar Sprite
        avatarImage.src = `avatar_${currentItem.word.toLowerCase()}.png`;
        avatarImage.onerror = function () { this.onerror = null; this.src = 'avatar.png'; };

        videoPlayer.src = currentItem.video_url;
        videoPlayer.load();

        // Wait for video mapping promise to play
        videoPlayer.play().catch(e => console.error("Video play error:", e));

        videoPlayer.onended = () => {
            currentVideoIndex++;
            playNextVideo();
        };

    } else {
        // Fallback: Show Word directly for 2 seconds (simulate fingerspelling)
        videoPlayer.src = "";
        missingWordWarning.classList.remove('hidden');
        currentWordOverlay.textContent = `[Spell] ${currentItem.word}`;
        currentWordOverlay.classList.remove('hidden');
        avatarContainer.classList.add('signing');

        // Update 2D Avatar Sprite
        avatarImage.src = `avatar_${currentItem.word.toLowerCase()}.png`;
        avatarImage.onerror = function () { this.onerror = null; this.src = 'avatar.png'; };

        setTimeout(() => {
            currentVideoIndex++;
            playNextVideo();
        }, 1500);
    }
}

// Replay logic
replayBtn.addEventListener('click', () => {
    if (videoSequence.length > 0) {
        currentVideoIndex = 0;
        playNextVideo();
    }
});

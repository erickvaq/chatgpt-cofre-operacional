# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import threading
import asyncio
import urllib.request
from flask import Flask, request, send_from_directory
import speech_recognition as sr
import websockets

app = Flask(__name__)

CONV_DIR = r"C:\Users\Windows User\AppData\Local\Temp" # fallback, but we will configure it dynamically
MEDIA_FILES = []
COMPLETED_EVENT = threading.Event()
ERROR_MESSAGE = None

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <title>Transcoder</title>
</head>
<body>
    <div id="status" style="font-size: 24px; font-family: sans-serif; margin: 20px;">Starting...</div>
    <script>
        function audioBufferToWav(buffer) {
            let numOfChan = buffer.numberOfChannels,
                length = buffer.length * numOfChan * 2 + 44,
                bufferArr = new ArrayBuffer(length),
                view = new DataView(bufferArr),
                channels = [], i, sample,
                offset = 0,
                pos = 0;

            // Write WAV header
            setUint32(0x46464952);                         // "RIFF"
            setUint32(length - 8);                         // file length - 8
            setUint32(0x45564157);                         // "WAVE"

            setUint32(0x20746d66);                         // "fmt " chunk
            setUint32(16);                                 // chunk length
            setUint16(1);                                  // sample format (raw)
            setUint16(numOfChan);                          // channel count
            setUint32(buffer.sampleRate);                  // sample rate
            setUint32(buffer.sampleRate * 2 * numOfChan);  // byte rate
            setUint16(numOfChan * 2);                      // block align
            setUint16(16);                                 // bits per sample

            setUint32(0x61746164);                         // "data" - chunk
            setUint32(buffer.length * numOfChan * 2);      // chunk length

            for(i = 0; i < buffer.numberOfChannels; i++)
                channels.push(buffer.getChannelData(i));

            while(pos < buffer.length) {
                for(i = 0; i < numOfChan; i++) {
                    sample = Math.max(-1, Math.min(1, channels[i][pos]));
                    sample = (sample < 0 ? sample * 0x8000 : sample * 0x7FFF) | 0;
                    view.setInt16(offset, sample, true);
                    offset += 2;
                }
                pos++;
            }

            return new Blob([view], {type: 'audio/wav'});

            function setUint16(data) {
                view.setUint16(offset, data, true);
                offset += 2;
            }

            function setUint32(data) {
                view.setUint32(offset, data, true);
                offset += 4;
            }
        }

        async function processFile(filename) {
            document.getElementById('status').innerText = 'Loading ' + filename + '...';
            const response = await fetch('/media/' + filename);
            const arrayBuffer = await response.arrayBuffer();
            
            document.getElementById('status').innerText = 'Decoding ' + filename + '...';
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
            
            let maxVal = 0;
            const chanData = audioBuffer.getChannelData(0);
            for (let j = 0; j < chanData.length; j++) {
                let v = Math.abs(chanData[j]);
                if (v > maxVal) maxVal = v;
            }
            await fetch('/log?msg=' + encodeURIComponent('Max value decoded for ' + filename + ': ' + maxVal));
            
            document.getElementById('status').innerText = 'Converting ' + filename + ' to WAV...';
            const wavBlob = audioBufferToWav(audioBuffer);
            
            document.getElementById('status').innerText = 'Uploading ' + filename + '...';
            const formData = new FormData();
            formData.append('file', wavBlob, filename.replace('.img', '.wav'));
            
            await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            document.getElementById('status').innerText = filename + ' done!';
        }

        async function start() {
            try {
                const params = new URLSearchParams(window.location.search);
                const files = params.get('files').split(',');
                for (const file of files) {
                    await processFile(file);
                }
                document.getElementById('status').innerText = 'All files completed!';
                fetch('/done');
            } catch (e) {
                document.getElementById('status').innerText = 'Error: ' + e.message;
                fetch('/error?msg=' + encodeURIComponent(e.message));
            }
        }
        
        start();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_CONTENT

@app.route('/media/<filename>')
def serve_media(filename):
    return send_from_directory(CONV_DIR, filename)

@app.route('/log')
def on_log():
    print("JS Log:", request.args.get('msg', ''))
    return 'OK'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    save_path = os.path.join(CONV_DIR, file.filename)
    file.save(save_path)
    print(f"Saved WAV file: {save_path}")
    return 'OK'

@app.route('/done')
def done():
    COMPLETED_EVENT.set()
    return 'OK'

@app.route('/error')
def on_error():
    global ERROR_MESSAGE
    ERROR_MESSAGE = request.args.get('msg', 'Unknown JS error')
    COMPLETED_EVENT.set()
    return 'OK'

async def open_tab_via_cdp(files_str):
    # Query Chrome tabs
    try:
        url = "http://localhost:9333/json"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as r:
            tabs = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"Error querying Chrome CDP: {e}")
        return False

    # Find the WebSocket Debugger URL of any page tab or browser
    ws_url = None
    for tab in tabs:
        if tab.get("type") == "page":
            ws_url = tab.get("webSocketDebuggerUrl")
            break
    if not ws_url:
        # Check browser type
        for tab in tabs:
            if "webSocketDebuggerUrl" in tab:
                ws_url = tab["webSocketDebuggerUrl"]
                break

    if not ws_url:
        print("Could not find WebSocket Debugger URL in Chrome tabs.")
        return False

    target_url = f"http://localhost:8080/?files={files_str}"
    
    target_id = None
    print(f"Connecting to CDP websocket: {ws_url}")
    async with websockets.connect(ws_url) as ws:
        # Create a new tab
        msg = {
            "id": 1,
            "method": "Target.createTarget",
            "params": {"url": target_url}
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        print("Tab created via CDP:", resp)
        try:
            target_id = json.loads(resp).get("result", {}).get("targetId")
        except Exception:
            pass
    return target_id

async def close_tab_via_cdp(target_id):
    if not target_id:
        return
    try:
        url = "http://localhost:9333/json"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as r:
            tabs = json.loads(r.read().decode('utf-8'))
    except Exception:
        return
    ws_url = None
    for tab in tabs:
        if tab.get("type") == "page":
            ws_url = tab.get("webSocketDebuggerUrl")
            break
    if ws_url:
        try:
            async with websockets.connect(ws_url) as ws:
                msg = {
                    "id": 2,
                    "method": "Target.closeTarget",
                    "params": {"targetId": target_id}
                }
                await ws.send(json.dumps(msg))
                await ws.recv()
                print(f"Tab {target_id} closed via CDP.")
        except Exception as e:
            print(f"Error closing tab: {e}")

def run_server():
    app.run(port=8080, debug=False, use_reloader=False)

def main():
    global CONV_DIR, MEDIA_FILES
    if len(sys.argv) < 3:
        print("Usage: python transcribe_audios.py <conversation_dir> <media_file1,media_file2,...>")
        sys.exit(1)
        
    CONV_DIR = sys.argv[1]
    files_str = sys.argv[2]
    MEDIA_FILES = files_str.split(',')
    
    print(f"Starting transcode server for files: {MEDIA_FILES} in {CONV_DIR}")
    
    # Start Flask server in background thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1) # wait for server to start
    
    # Open tab via CDP
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    target_id = loop.run_until_complete(open_tab_via_cdp(files_str))
    if not target_id:
        print("Failed to open tab via CDP. Trying manual run or wait.")
        
    # Wait for completion
    print("Waiting for transcode to complete...")
    completed = COMPLETED_EVENT.wait(timeout=60)
    
    # Close tab via CDP
    if target_id:
        try:
            loop.run_until_complete(close_tab_via_cdp(target_id))
        except Exception:
            pass
    
    if not completed:
        print("Transcode timed out after 60 seconds.")
    elif ERROR_MESSAGE:
        print(f"JS Transcode Error: {ERROR_MESSAGE}")
    else:
        print("Transcode finished successfully!")
        
        # Now run speech recognition on each WAV file
        recognizer = sr.Recognizer()
        transcripts = {}
        for f in MEDIA_FILES:
            wav_name = f.replace('.img', '.wav')
            wav_path = os.path.join(CONV_DIR, wav_name)
            if os.path.exists(wav_path):
                print(f"Transcribing {wav_path}...")
                try:
                    with sr.AudioFile(wav_path) as source:
                        audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio, language="pt-BR")
                    transcripts[f] = text
                    print(f"Transcript for {f}: {text}")
                except Exception as e:
                    print(f"Error transcribing {f}: {e}")
                    transcripts[f] = f"[Error: {e}]"
            else:
                print(f"WAV file not found: {wav_path}")
                transcripts[f] = "[WAV file not found]"
                
        # Write transcripts to a json file in conversation dir
        out_path = os.path.join(CONV_DIR, "transcripts.json")
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(transcripts, out_f, indent=4, ensure_ascii=False)
        print(f"Saved transcripts to: {out_path}")

if __name__ == "__main__":
    main()

import uuid
import keyboard

# =========================
# CORE
# =========================

from datetime import datetime
import os
import webbrowser
import asyncio
import json

# =========================
# AI
# =========================

import ollama
from faster_whisper import WhisperModel

# =========================
# VOICE
# =========================

import speech_recognition as sr
import edge_tts
import pygame

# =========================
# LOAD WHISPER MODEL
# =========================

model = WhisperModel(
    "base",
    compute_type="int8"
)

# =========================
# INIT PYGAME
# =========================

pygame.mixer.init()

# =========================
# MEMORY FUNCTIONS
# =========================

MEMORY_FILE = "memory.json"

def load_memory():

    try:

        with open(MEMORY_FILE, "r") as f:

            return json.load(f)

    except:

        return {
            "personal": [],
            "work": [],
            "preferences": [],
            "tasks": []
        }

def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:

        json.dump(memory, f, indent=4)

memory = load_memory()

# =========================
# SPEAK FUNCTION
# =========================

async def async_speak(text):

    print("Mama Bro:", text)

    filename = f"{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    )

    await communicate.save(filename)

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        if keyboard.is_pressed("s"):

            pygame.mixer.music.stop()

            break

    pygame.mixer.music.unload()

    os.remove(filename)

def speak(text):
    asyncio.run(async_speak(text))

# =========================
# LISTEN FUNCTION
# =========================

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        recognizer.energy_threshold = 300

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except:
            return ""

        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())

    # Whisper transcription
    segments, info = model.transcribe(
        "temp.wav",
        language="en"
    )

    text = ""

    for segment in segments:
        text += segment.text

    text = text.strip()

    print("You:", text)

    if len(text) < 2:
        return ""

    return text

# =========================
# START ASSISTANT
# =========================

speak("Mama Bro Started")

# =========================
# MAIN LOOP
# =========================

while True:

    user_input = listen()

    if not user_input:
        continue

    user_input = user_input.lower()

    # =========================
    # SMART MEMORY DETECTION
    # =========================

    memory_response = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "system",
                "content": """
                You are a memory classifier.

                Analyze the user input.

                If the message contains personal memory,
                return ONLY this format:

                CATEGORY: personal
                MEMORY: <memory>

                OR

                CATEGORY: work
                MEMORY: <memory>

                OR

                CATEGORY: preferences
                MEMORY: <memory>

                OR

                CATEGORY: tasks
                MEMORY: <memory>

                If no memory should be saved,
                return ONLY:

                CATEGORY: none
                """
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    memory_result = memory_response["message"]["content"]

    print(memory_result)

    if "CATEGORY:" in memory_result:

        if "CATEGORY: none" not in memory_result:

            lines = memory_result.split("\n")

            category = ""
            memory_text = ""

            for line in lines:

                if "CATEGORY:" in line:

                    category = line.replace(
                        "CATEGORY:",
                        ""
                    ).strip()

                if "MEMORY:" in line:

                    memory_text = line.replace(
                        "MEMORY:",
                        ""
                    ).strip()

            if category in memory:

                if memory_text not in memory[category]:

                    memory[category].append(memory_text)

                    save_memory(memory)

                    speak(
                        f"I will remember that in {category}"
                    )

    # =========================
    # SHOW MEMORY
    # =========================

    if "show memory" in user_input:

        memory_text = json.dumps(
            memory,
            indent=2
        )

        speak("Showing all memory.")

        print(memory_text)

        continue

    # =========================
    # EXIT
    # =========================

    if "exit" in user_input:

        speak("Goodbye Bro")

        break

    # =========================
    # DATE
    # =========================

    if "date" in user_input:

        today = datetime.now().strftime("%d %B %Y")

        speak(f"Today's date is {today}")

        continue

    # =========================
    # TIME
    # =========================

    if "time" in user_input:

        current_time = datetime.now().strftime("%I:%M %p")

        speak(f"Current time is {current_time}")

        continue

    # =========================
    # OPEN YOUTUBE
    # =========================

    if "open youtube" in user_input:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

        continue

    # =========================
    # OPEN GOOGLE
    # =========================

    if "open google" in user_input:

        speak("Opening Google")

        webbrowser.open("https://google.com")

        continue

    # =========================
    # OPEN CHATGPT
    # =========================

    if "open chatgpt" in user_input or "open chat g p t" in user_input:

        speak("Opening Chat GPT")

        webbrowser.open("https://chatgpt.com")

        continue

    # =========================
    # OPEN GMAIL
    # =========================

    if "open gmail" in user_input:

        speak("Opening Gmail")

        webbrowser.open("https://mail.google.com")

        continue

    # =========================
    # OPEN WHATSAPP
    # =========================

    if "open whatsapp" in user_input:

        speak("Opening WhatsApp")

        webbrowser.open("https://web.whatsapp.com")

        continue

    # =========================
    # OPEN TEAMS
    # =========================

    if "open teams" in user_input:

        speak("Opening Teams")

        os.system("start ms-teams:")

        continue

    # =========================
    # SEARCH GOOGLE
    # =========================

    if "search" in user_input:

        search_query = user_input.replace(
            "search",
            ""
        ).strip()

        speak(f"Searching for {search_query}")

        webbrowser.open(
            f"https://www.google.com/search?q={search_query}"
        )

        continue

    # =========================
    # MEMORY CONTEXT
    # =========================

    memory_context = json.dumps(
        memory,
        indent=2
    )

    # =========================
    # AI RESPONSE
    # =========================

    response = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are Mama Bro,
                a professional AI assistant.

                Speak clearly,
                intelligently,
                and concisely.

                Be friendly and helpful.

                Here is the user's memory:

                {memory_context}
                """
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    reply = response["message"]["content"]

    speak(reply)
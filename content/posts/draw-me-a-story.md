---
title: "Draw Me a Story: AI Creates & Reads Tiny Tales from Five Simple Prompts"
date: 2026-02-07T10:00:00-05:00
draft: false
tags: ["LLM", "Text-to-Speech", "Image Generation", "Toddler Story", "AI Engineering", "Prompt Engineering"]
summary: "An AI chatbot that takes five playful inputs and returns a toddler-friendly story, spoken aloud, and topped with a fun image." 
---

> I built a tiny creative assistant that asks for five things — a `character`, `color`, `place`, `feeling`, and an `action` — then crafts a short, age-appropriate story, reads it aloud, and generates a playful image to finish.

This project is a small experiment in constrained creative prompting, safety filtering for young audiences, and combining LLMs with TTS and image generation for an end-to-end, delight-first experience.

---

## ✨ Demo
{{< linkedin id="urn:li:ugcPost:7426154929372852224" >}}

## ✨ How it works (happy summary)

Give the bot five inputs:

- **Character:** e.g., "a tiny dragon"
- **Color:** e.g., "yellow"
- **Place:** e.g., "a cozy treehouse"
- **Feeling:** e.g., "curious"
- **Action:** e.g., "bakes a cake"

The chatbot then:

1. Builds a short 2–3 minute story with simple vocabulary and gentle pacing for toddlers.
2. Applies a safety + content filter to ensure the language, themes, and imagery are age-appropriate.
3. Sends the cleaned final text to a TTS system and produces an audio file (MP3/OGG).
4. Creates a bright, cartoon-style image based on the same inputs to display at the end.

---

## 🧩 Example

Inputs:

- Character: a tiny dragon
- Color: yellow
- Place: a cozy treehouse
- Feeling: curious
- Action: bakes a cake

Generated story (trimmed):

> Little Sunny was a tiny yellow dragon who lived in a cozy treehouse high in the branches. Sunny was very curious — every morning they peeped out the window to see what new giggles the day would bring. One sunny morning, Sunny decided to bake a cake for a new friend. They mixed flour, a little pretend sugar, and a sprinkle of laughter. "Whoosh!" said Sunny as the oven made a friendly humming sound. When the cake was ready, Sunny shared a slice and a big, warm dragon hug. The End.

The same text is passed to the TTS engine and a cheerful, slightly slower reading is produced to suit toddlers.

---

## 🔧 Implementation notes (technical details)

This section mirrors the technical approach from a similar project I wrote about in "From Web to Wonder" — but simplified for this five-prompt assistant.

- **Architecture & UI:** A lightweight server orchestrates story generation, TTS, and image creation. For demos and input collection I built a small Gradio UI that collects the five prompts, previews the generated story text, plays the TTS audio, and displays the final image.
- **LLM model API:** The core story generation uses an LLM model API (hosted or cloud provider). I call the model via its HTTP SDK, requesting a structured JSON response (e.g., `{"title":"...","story":"...","safetyScore":0.0}`). Using the API lets the app validate responses, retry with adjusted prompts, and log examples for analysis.
- **AI tools:** Separate cloud/hosted tools handle TTS and image generation (or local models). I pass the sanitized `story` to a TTS service (producing MP3/OGG) and send a controlled image prompt to an image model that returns a cartoon-style illustration.
- **Prompting / Constraints:** Prompts enforce short sentences, a small vocabulary list appropriate for toddlers, and an explicit ban on frightening or adult content. Example instruction snippet:
```
You are a storyteller for toddlers. Use simple words, short sentences, gentle tone. Return JSON with fields: title, story, safetyScore (0-1).
```

- **Safety filtering:** Two-stage filtering: model-side constraints plus app-side checks against a denylist and a readability simplifier that shortens sentences and replaces rare words.
- **Model tuning:** Low temperature (0.1–0.3) for consistent, child-friendly outputs; token limits keep stories brief.
- **API flow / functions:** The app calls `POST /generate_story` (LLM API) -> validate -> `POST /synthesize` (TTS) -> `POST /generate_image` (image API). The Gradio front-end calls the server, streams the audio preview, and shows the generated image.

---

## 🛡️ Safety & design decisions

- All generated text goes through a two-step sanitization before being used for TTS or image prompts.
- Prompts explicitly instruct the model to avoid real-world instructions (no cooking instructions with hot ovens, no small-object-choking risks), and to prefer playful, imaginative descriptions.
- Images use a cartoon style and avoid photorealism for younger audiences.

---

## 📂 Code 

Implementation details, prompt templates, and the small orchestration code are available in the repository: 
[LLM Engineering Github source code](https://github.com/ed-donner/llm_engineering/blob/main/week2/community-contributions/draw_my_story.ipynb)



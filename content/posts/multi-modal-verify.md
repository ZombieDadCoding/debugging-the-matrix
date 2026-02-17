---
title: "Multi Modal Verify: Automated Video Analysis & Fact-Checking in Colab"
date: 2026-02-12T10:00:00-05:00
draft: false
tags: ["Video Analysis", "Fact-Checking", "Colab", "Misinformation", "NLP", "AI"]
summary: "A Google Colab pipeline that turns online videos into structured summaries and verifiable claims with automated fact-checking."
---

This project is a Google Colab–based automated video analysis pipeline that transforms online videos into structured, verifiable knowledge. Give it a YouTube URL or a direct link to a social-media video and it runs an end-to-end workflow that includes ingestion, transcription, content analysis, summarization, and independent fact-checking.

The goal is to speed up verification workflows by producing concise summaries, extracted claims, and credibility signals from video content — all from a reproducible Colab notebook.

---

## How it works (short)

Feed the pipeline a video link and it performs:

- Video ingestion: downloads and extracts audio from shared links.
- Speech-to-text transcription: converts spoken content to accurate, readable text.
- Content analysis: identifies key topics, named entities, and explicit claims.
- Automated summarization: produces a concise, human-readable summary.
- Independent fact-checking: cross-verifies extracted claims against external sources and returns credibility signals and sources.

The pipeline runs in Google Colab so anyone can open, run, and reproduce the analysis without local installs.

---

## Example (brief)

Input: a viral interview uploaded to YouTube.

Output: a short report containing:

- a 3–5 sentence summary of the video's main points;
- a list of 6–12 candidate factual claims extracted from speech;
- for each claim: a credibility review, supporting or contradicting sources, and short final data based opinion;

This structured output helps researchers and fact-checkers prioritize which claims need deeper investigation.

---

## 🔧 Implementation notes (technical details)

- Architecture: A Colab notebook stitches together lightweight utilities and model calls: video download, audio extraction, ASR, NLP analysis, summarization, and web-based fact checks.
- Ingestion: the `yt_dlp` Python module downloads media; `ffmpeg` extracts audio and standardizes sample rate.
- ASR: `openai/whisper-large-v3` is used for speech-to-text transcription (high-quality ASR) with configuration options for runtime and language models.
- Analysis: `meta-llama/Llama-3.2-3B-Instruct` drives sentence segmentation, claim detection, named-entity recognition, and lightweight topic clustering and claim rewriting for downstream checks.
- Summarization: extractive + abstractive blend (model-backed summarization using Llama-3.2-3B-Instruct with conservative decoding) to keep outputs concise and faithful.
- Fact-checking: a lightweight verification loop uses `meta-llama/Llama-3.2-3B-Instruct` to rewrite candidate claims, perform automated web searches for evidence, retrieve sources, and run entailment/scoring to flag supporting or contradicting signals.
- Provenance: each claim links back to transcript timestamps and to retrieved sources (URLs, snippets, and metadata).
- Reproducibility: the Colab notebook pins versions, logs inputs, and provides canned examples to reproduce reported outputs.

Implementation choices emphasize transparency: explicit timestamps, raw transcript exports, and the ability to re-run individual pipeline stages.

---

## 🛡️ Caution

- Bias & misuse: the system surfaces video claims but does not assert definitive truth — it provides evidence and scores for human reviewers.
- Privacy: the notebook warns users before processing videos of private individuals and suggests consent best practices.

---

## 📂 Source code

Implementation details, prompt templates, and the small orchestration code are available in the repository: 

---

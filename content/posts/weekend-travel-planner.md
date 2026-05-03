---
title: "Built a weekend travel planner because ChatGPT kept recommending wine tours to my toddler 🍷🧸"
date: 2026-05-02
draft: false
tags:
  - multi-agent-ai
  - gradio
  - hugging-face-spaces
  - travel-planner
  - prompt-engineering
---

{{< siteimg src="images/TravelPlanner.png" alt="Tired Parent" style="display:block;margin:18px auto 28px auto;max-width:880px;height:auto;border:0;" >}}

Weekend trips with kids shouldn't feel like a second job. But every time I asked AI for recommendations, I got generic answers that ignored nap schedules, snack breaks, and the eternal question: "Is this stroller-friendly?"

So I built my own solution.

## The Project

A multi-agent travel planner that generates 2-night, 3-day family itineraries based on kids' age ranges (0–2, 3–5, 6–9, 10–12, 13+), origin city, and budget.

## What It Does Differently

- **Age-specific activity recommendations** – No, a 4yo and a 12yo don't want the same thing
- **Witty rejection if you don't have kids** – Politely told you're too well-rested for this service
- **Two-step wizard UI** – Doesn't overwhelm parents with forms

## Tech Stack Learnings

**🔹 Multi-agent AI workflow**  
Built with OpenAI SDK, each agent handles a specific domain (lodging, activities, dining, pacing). The coordination logic was harder than the prompts themselves — getting agents to agree on a realistic daily schedule was humbling.

**🔹 Gradio + Hugging Face Spaces**  
Deployed in minutes. The `gr.State` wizard pattern made the two-step UX possible without frontend complexity. 

**🔹 Age range design**  
My first split (0-3, 3-6, 6+) failed because "6+" is too wide. A 6yo and a 12yo have nothing in common travel-wise. Landed on: Infant (0-2), Preschool (3-5), Primary (6-9), Tween (10-12), Teen (13+). The 6-9 "Primary" bucket was the hardest to name but feels right.

**🔹 Budget realism**  
Weekend trips cost $250–$500 (budget), $500–$1,000 (comfortable), or $1,000+ (splurge). Not the $4k averages you see online — those are week-long trips with flights.

## Live Site and open source code

https://huggingface.co/spaces/ZombieDadCoding/Weekend_Family_Travel_Planner


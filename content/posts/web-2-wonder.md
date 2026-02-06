---
title: "From Web to Wonder: AI Turns Any URL into a Toddler's Tale"
date: 2025-02-01T10:00:00-05:00
draft: false
tags: ["LLM", "Function Calling", "Toddler Story", "AI Engineering", "Prompt Engineering"]
summary: "Ever wished for a simple way to distill complex web pages into engaging stories for tiny humans? In this post, I explore how to use AI function calls to transform any URL into a captivating toddler-friendly tale, perfect for a few minutes of magical distraction."
---

> I built an AI function that takes a website URL and crafts a short, engaging story suitable for a toddler. Perfect for turning adult content into child-friendly narratives!

*This project was inspired by an exercise to conclude week1 in the [AI Engineer Core Track](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/) course by Ed Donner.*

---

## 🚀 The Challenge: Internet for Infants?

As an AI engineer (and sometimes, a tired parent!), I often wonder how to bridge the gap between the vast, complex information on the internet and the curious, developing minds of toddlers. Traditional summaries are too dense, and manually rewriting content is time-consuming. What if an LLM could do the heavy lifting, not just summarizing, but *transforming*?

My goal was clear:
* **Input:** A website URL (e.g., a news article, a Wikipedia page, even a technical documentation page).
* **Output:** A simple, engaging story, 2-3 minutes long, using vocabulary and concepts a toddler can grasp.
* **Method:** Leverage AI function calling for a clean, programmatic approach.

---

## 💡 Example in Action: What Happens When AI Reads Wikipedia?
Let's see this in practice. I gave my function the Wikipedia page for "Dolphins". Input URL: https://en.wikipedia.org/wiki/Dolphin

Story created by LLM Gemini 2.5 Flash model:

> Hello, little friends! Are you ready for a happy ocean story?                                                      
> Let's meet our new friend, Dilly the Dolphin! Dilly lives in the big, big blue ocean. It's like a giant bathtub for him, full of water!                                                                                                
> Dilly is a very special animal. He has smooth, grey skin, just like a smooth, round stone. And guess what? He has a little hole on top of his head! Pssshhh! That's how Dilly breathes the fresh air, even though he lives in the water.                                                                                                             
> Dilly loves to swim! He wiggles his tail and zooms through the water. Splash, splash, zoom! He can swim super fast! Sometimes, Dilly gets so excited, he jumps high, high out of the water! Wheee! Can you jump high like Dilly?       
> Dilly isn't alone. He has lots of dolphin friends! They all swim and play together. They love to chase each other  and play hide-and-seek among the wavy seaweed. They are very smart friends!                                        
> When Dilly talks to his friends, he makes happy clicking sounds and pretty whistling songs. Click, click, wheee! Can you make a happy sound like Dilly?                                                                             
> And when Dilly gets hungry, he eats yummy little fish. Munch, munch! What a tasty snack!                           
> Dilly is a friendly, playful, and very happy dolphin. He loves his ocean home and all his friends. Maybe one day, if you look closely at the ocean, you'll see Dilly jump and wave hello with a happy Click, click!                  
> The End! 


## 🔗 The Code Behind the Magic
Want to dive deeper into the implementation? The full source code, including the web scraping logic, prompt templates, and the LLM integration, is available on GitHub.

[LLM Engineering Github source code](https://github.com/ed-donner/llm_engineering/blob/main/week1/community-contributions/toddler_story_creator_using_gemini_API.ipynb)


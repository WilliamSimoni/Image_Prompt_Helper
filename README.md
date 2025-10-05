# Image Prompt Helper

## Overview

This project was created to test **DSPy** (Declarative Self-improving Python) in a practical, real-world scenario. 

### Why This Project?

Generating detailed image prompts is often tedious. When working with image generation models (like DALL-E, Midjourney, or Stable Diffusion), the quality of results heavily depends on prompt detail and specificity. Typically, I find myself asking an LLM to interview me with questions to flesh out my vague ideas into comprehensive prompts.

This project automates that iterative refinement process using DSPy's ReAct agent pattern, creating an interactive system that:
- Asks targeted questions to gather context
- Summarises the information collected
- Generates improved, detailed image prompts
- Allows iterative refinement based on user feedback

## Features

- **Interactive questioning**: ReAct agent dynamically asks relevant questions to understand your vision
- **Iterative refinement**: Continuously improve prompts based on your feedback
- **Context accumulation**: Each iteration builds on previous information
- **Modular design**: Easy to swap LLM backends or customise questioning logic

## Installation
1. Clone the repo and open a terminal in the repo folder
2. Update the .env file to set the LLM connection. I used LM Studio with Gemma 3
3. run pip install .
4. run python main.py. A CLI interface will let you use the tool

## Architecture
```mermaid
flowchart TD
    Start([User provides initial prompt]) --> Init[Initialize PromptGenerator with LM]
    Init --> FirstGen[Generate initial prompt]
    
    FirstGen --> ReactAgent[ReAct Agent]
    ReactAgent --> AskQ{Need more info?}
    AskQ -->|Yes| Tool[ask_questions tool]
    Tool --> UserInput[User answers questions]
    UserInput --> Store[Store Q&A pairs]
    Store --> AskQ
    AskQ -->|No| Summary[Generate questions_answers_summary]
    
    Summary --> ChainOfThought[ChainOfThought: Generate improved prompt]
    ChainOfThought --> Display[Display prompt to user]
    
    Display --> UserDecision{Satisfied?}
    UserDecision -->|No - Refine| Feedback[User provides feedback]
    Feedback --> ReactAgent
    UserDecision -->|Yes| End([Complete])
    
    UserDecision -->|Max iterations reached| End
    
    style ReactAgent fill:#e1f5ff
    style ChainOfThought fill:#fff4e1
    style Tool fill:#f0e1ff
    style UserInput fill:#e1ffe1

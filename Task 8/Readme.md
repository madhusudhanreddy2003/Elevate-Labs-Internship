# 💬 Task 8 – Rule-Based Chatbot (with Calculator)  
_A Simple Console Chatbot Using Python, if-else, and Sympy_

This project is part of the **Elevate Labs Internship – Task 8**, where the goal is to build a **rule-based chatbot** using Python and basic `if-elif-else` logic.

In this upgraded version, the chatbot:

- Acts like a simple conversational bot  
- Can **evaluate math expressions** (works like a mini calculator)  
- Uses **random default responses** (Option 4) when it doesn’t understand  
- Runs in the terminal using a loop  

---

## 🌟 Features

### ✔ Rule-Based Conversation (if-elif-else)
The chatbot responds to:

- Greetings → `hello`, `hi`, `hey`  
- “How are you?”  
- “What is your name?”  
- “Who created you?”  
- “Tell me a joke”  
- “Weather” type questions  

All implemented using basic `if-elif-else` blocks.

---

### ✔ Math Calculation Support (Calculator Mode)
If the user types a **pure math expression**, the bot tries to evaluate it using **SymPy**.

Examples:

```text
You: 2+3*5
🤖 Chatbot: The result is 17

You: (10/3)^2
🤖 Chatbot: The result is 11.1111111111111

You: can you solve 77*77+99-3/5 ?
🤖 Chatbot: The result is 6027.40000000000

It uses:
```bash
from sympy import sympify, N
```
and a helper:
```bash
sym_expr = sympify(expr)
result = N(sym_expr
```
to safely compute results.

### ✔ Random Default Responses

When the chatbot doesn’t understand the input, it doesn’t reply with a boring fixed line.
Instead, it chooses a response randomly from a list.
<br>
Example list:
```bash
default_responses = [
    "🤖 Chatbot: Sorry, I didn’t understand that. You can ask me things like greetings, jokes, or calculations!",
    "🤖 Chatbot: Hmm… that went over my head 😅 Try asking me a math question like 2+3*5 or something simple.",
    "🤖 Chatbot: I’m still learning 📚 but I’m good at basic calculations and simple chat. Try a math expression!",
    "🤖 Chatbot: I didn’t get that. You can ask me who created me, tell me 'hi', or type a math expression like (10/3)^2.",
]

```
Then in the final else block:
```bash
import random

else:
    print(random.choice(default_responses))

```

---

## 📂 Project Structure
```bash
Task 8/
│── chatbot.py     # Main chatbot script
└── README.md      # Documentation (this file)

```

---

## ⚙️ Requirements
Install SymPy (for calculations):
```bash
pip install sympy

```

---

## ▶️ How to Run

From inside the folder:
```bash
python chatbot.py

```

## Sample interaction with 🤖 Chatbot:
```bash
🤖 Chatbot: Hello! I am your simple rule-based chatbot with calculator support.
Type 'exit' to stop the conversation.
You can also type math expressions like: 2+3*5, (10/3)^2, 100-45, etc.

You: hi
🤖 Chatbot: Hello there! How can I help you today?

You: 10+5*3
🤖 Chatbot: The result is 25

You: tell me a joke
🤖 Chatbot: Why don’t programmers like nature? Because it has too many bugs! 😄

You: asdfghjkl
🤖 Chatbot: Hmm… that went over my head 😅 Try something like 999*999-11-+74/3!, I will show True Power of Me in calculation 😎

You: exit
🤖 Chatbot: Goodbye! Have a great day 🙂

```

---

## 🎯 Learning Outcomes
By completing this task, I gained experience with:
- How rule-based chatbots work using if-elif-else
- Basic input/output loop logic in Python
- Detecting math expressions and evaluating them using SymPy
- Adding random behavior for more natural responses
- Writing clean, structured console applications

---

### 👨‍💻 Author
Kethari Madhu Sudhan Reddy<br>
Python Developer • Data Analyst • AIML Engineer<br>
maddoxer143@gmail.com

---

### 📜 License

This project is an Open Source — use it freely!

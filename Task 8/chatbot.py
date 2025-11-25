from sympy import sympify, N
import random
import re

print("🤖 Chatbot: Hello! I am your simple rule-based chatbot with calculator support.")
print("Type 'exit' to stop the conversation.")
print("You can also type math expressions like: 2+3*5, (10/3)^2, 100-45, etc.")
print("I can also understand sentences like: 'what is 10+5*3' or 'solve 100-45'\n")


# -----------------------------
# Extract math expression
# -----------------------------
def extract_expression(text: str) -> str:
    """
    Extract math expression from any sentence.
    Example:
    'what is 10+5*3' -> '10+5*3'
    """
    cleaned = re.sub(r"[^0-9+\-*/%^().]", "", text)
    return cleaned.strip()


def is_math_expression(text: str) -> bool:
    """
    Determine if the cleaned text is a valid math expression.
    """
    expr = extract_expression(text)
    if not expr:
        return False

    has_digit = any(ch.isdigit() for ch in expr)
    has_op = any(ch in "+-*/%^()." for ch in expr)

    return has_digit and has_op


def try_calculate(expr: str):
    """Safely evaluate math expression using SymPy."""
    try:
        result = N(sympify(expr))
        return True, result
    except Exception:
        return False, None


# -----------------------------
# Random default responses
# -----------------------------
default_responses = [
    "🤖 Chatbot: Sorry, I didn’t understand that. Try asking a math question like 999*999-11-+74/3! \n",
    "🤖 Chatbot: Hmm… that went over my head 😅 Try something like 999*999-11-+74/3!, I will show True Power of Me in calculation 😎\n",
    "🤖 Chatbot: I’m still learning 📚 but I’m great at calculations! Try one!\n",
    "🤖 Chatbot: I didn’t get that. You can say hi, ask who created me, or ask a calculation!\n",
]


# -----------------------------
# Conversation loop
# -----------------------------
while True:
    user_raw = input("You: ")
    user = user_raw.lower().strip()

    # Exit command
    if user == "exit":
        print("\n🤖 Chatbot: Goodbye! Have a great day 🙂")
        break

    # 1️⃣ Try to evaluate math inside the text
    if is_math_expression(user_raw):
        expr = extract_expression(user_raw)
        success, result = try_calculate(expr)
        if success:
            print(f"🤖 Chatbot: The result is {result}\n")
            continue

    # 2️⃣ Rule-based responses

    # Greetings
    if "hello" in user or "hi" in user or "hey" in user:
        print("🤖 Chatbot: Hello there! How can I help you today?\n")

    # Asking name
    elif "your name" in user:
        print("🤖 Chatbot: I am a simple Python chatbot created by Madhu!\n")
    # How are you
    elif "how are you" in user:
        print("🤖 Chatbot: I'm doing great! What about you?\n")

    # User feeling good
    elif "i am fine" in user or "i am good" in user:
        print("🤖 Chatbot: That's awesome to hear! 😊\n")

    # Joke
    elif "joke" in user:
        print("🤖 Chatbot: Why don’t programmers like nature? Because it has too many bugs! 😂\n")
    # Weather
    elif "weather" in user:
        print("🤖 Chatbot: I can't check real weather due to my limitations and I don't have internet access, but I hope it's sunny for you ☀️\n")

    # Creator
    elif "who created you" in user or "who made you" in user:
        print("🤖 Chatbot: I was created by Kethari Madhu Sudhan Reddy for Task 8 on part of Elevate Labs Internship 🔥\n")
    # Default (random)
    else:
        print(random.choice(default_responses))

from chatbot import Chatbot

ai = Chatbot()

print("Welcome to the Chatbot! Type 'exit' to quit.")
print("commands:")
print("/search(question here) - Search for an answer to your question.  ")
print(" remember('key', 'value') - Store a key=value")
print("memory- view stored info")
print("quit - exit the program")

while True:
    usermsg = input("You: ").strip()

    if usermsg.lower() == "exit" or usermsg.lower() == "quit":
        print("Have a great day! Goodbye!")
        break

    if not usermsg:
        print("Please enter a message.")
        continue

    response = ai.respond(usermsg)

    print("AI:", response)

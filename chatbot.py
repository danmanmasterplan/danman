import json
import os


from internet import web_search


class Chatbot:
    def __init__(self):
        self.name = "python ai"
        self.memory = self.load_memory()
        self.responses = self.load_responses()

    def load_memory(self):
        if os.path.exists("memory.json"):
            with open("memory.json", "r") as file:
                return json.load(file)
        return {
            "facts": {},
            "conversation_history": []
        }

    def save_memory(self):
        with open("memory.json", "w") as file:
            json.dump(self.memory, file, indent=4)

    def load_responses(self):
        with open("responses.json", "r") as file:
            return json.load(file)

    def respond(self, message):
        message = message.strip()

        if message.lower().startswith("/search"):
            query = message[8:].strip()
            if not query:
                return "please provide something to search for."
            search_results = web_search(query)

            if not search_results:
                return "No results found."

            output = ""
            for result in search_results:
                output += f"Title: {result['title']}\n"
                output += f"Information: {result['body']}\n"
                output += f"URL: {result['url']}\n"
            return output

        if message.lower().startswith("/remember "):
            information = message[10:]
            if "=" not in information:
                return "Please provide information in the format: key=value"
            key = key.strip()
            value = value.strip()

            if not key or not value:
                return "Both key and value must be provided."

            self.memory["facts"][key] = value
            self.save_memory()

            return f"I'll remember that {key} is {value}."

        if message.lower() == "/memory":
            facts = self.memory["facts"]

            if not facts:
                return "I don't have any stored information."

            return "\n".join(
                f"{key}: {value}"
                for key, value in facts.items()
            )

        response = "i'm not sure how to respond to that. Please try again or use a command."

        lower_message = message.lower()

        for keyword, answers in self.responses.items():
            if keyword in lower_message:
                import random
                response = random.choice(answers)
                break

        self.memory["conversation_history"].append({"user": message, "ai": response})
        self.memory["conversation_history"] = self.memory["conversation_history"][-20:]
        self.save_memory()

        return response 
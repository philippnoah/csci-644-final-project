import os
from openai import OpenAI
import numpy as np

ACTION_MAPPING = {
    0: "REQUEST_DESCRIPTION",
    1: "REQUEST_INTERACTION_PREF",
    2: "REQUEST_CLARIFICATION",
    3: "REQUEST_DOCUMENTATION_DETAIL",
    4: "REQUEST_DOCUMENTATION_TYPE",
    5: "REQUEST_UNIT_TESTS",
    6: "REQUEST_FRAMEWORKS_CONFIRMATION",
    7: "REQUEST_FILE_STRUCTURE_CONFIRMATION",
    8: "REQUEST_LANGUAGE_CONFIRMATION",
    9: "BUILD_CODEBASE",
}

ACTION_2_MSG = {
    0: [
        "Howdy! What would you like to build today?",
        "Hello, please provide the description of the project that you are looking to build."
        ],
    1: "What is your preferred interaction style?",
    2: "Ask 3 clarification questions that will help you build a good codebase that runs.",
    3: "What level of documentation detail do you require? (none, some, a lot)",
    4: "Do you prefer docstrings or comments?",
    5: "Do you require unit tests?",
    6: "Suggest framework(s) for the project. Ask the user if they accept it.",
    7: "Kinldy suggest a file structure for the project. Ask the user if they accept it. The file structure should be flat.",
    8: "Suggest a language for the project. Ask the user if they accept it.",
    9: """
    Write the codebase.
    Priority 1: Your answer MUST look like: '```<filename>\n<file_content>```'. NOTHING else should be in the returned string. All characters should be escaped so that the string can be parsed as JSON.
    Priority 2: Make the hierarchy flat, that is, just produce a list of files -- NO folders.
    Priority 3: Don't leave any file empty. Fill it with actual code, not just comments or 'pass' statements.
    """,
}

class NLG:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.messages = [
            {
                "role": "system",
                "content": "You are a codebase assistant. You ask questions and propose actions to the user to build a codebase. You are always concise and clear in your messages. You can ask for more details, clarification, documentation, unit tests, frameworks, file structure, language, and to build the codebase. After some back and forth, your goal is for you to eventually write the full code for a codebase."
            }]
        self.action_mapping = ACTION_MAPPING
        self.action2msg = ACTION_2_MSG

    def get_message(self, action):
        role = "system"
        content = ""
        if action == 0:
            role = "assistant"
            content = np.random.choice(self.action2msg[action])
        elif action in [2, 3, 4, 5, 6, 7, 8, 9]:
            content = self.action2msg[action]
        else:
            content = "Rephrase and ask this question given the context (adjust and elaborate as needed): " + self.action2msg[action]
        return {"role": role, "content": content}

    def action(self, action):
        msg = self.get_message(action)
        self.messages.append(msg)
        response = ""
        if action in [0, 3, 4, 5]:
            pass
        elif msg["role"] == "system":
            response = self.client.chat.completions.create(messages=self.messages, model="gpt-3.5-turbo").choices[0].message.content
            self.messages.append({"role": "assistant", "content": response})
        else:
            response = msg["content"]
        # print(self.messages)
        response = self.messages[-1]["content"]
        return response
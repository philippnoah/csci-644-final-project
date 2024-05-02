from nlg import NLG
import numpy as np
import json
import os

class DialogueManager: 
    def __init__(self, model, env):
        self.nlg = NLG()
        self.model = model
        self.env = env
        self.done = False
    
    def step(self, action):
        response = self.nlg.action(action)
        return response
    
    def parse_user_input(self, user_input):
        # if user pressed esc, then stop the conversation 
        if not user_input:
            self.done = True
        self.nlg.messages.append({"role": "user", "content": user_input})
        return user_input
    
    def run(self):
        obs, _ = self.env.reset()
        for i in range(20):
            # print(f"\n\nROUND {i}")
            obs = {k: np.array([v]) for k, v in obs.items()}
            # print("STATE: ", obs)
            action, _ = self.model.predict(obs, deterministic=True)
            # print("ACTION: ", action)
            response = self.step(action[0])
            print("\nASSISTANT:\nSounds good! " + response)
            user = input(f"\n\nUSER:\n")
            user = self.parse_user_input(user)
            # print("USER: ", user)
            obs, reward, self.done, trunc, info = self.env.step(action)
            if self.done:
                break
        
        if self.done:
            print("Conversation ended. Now attempting to build the codebase...")
        
        s = self.nlg.messages[-2]["content"]

        b = []
        a = s.split("```")
        for i in a:
            if len(i) > 3 and i not in ["", "\n"]:
                b.append(i)

        # breakpoint()
        basedir = "codebase"
        if os.path.exists(basedir) and os.path.isdir(basedir) and os.listdir(basedir):
            input("dir is not empty. delete and press enter")
        for t in b:
            try:
                name, content = t.split("\n", 1)
                print(name, repr(content[:20]))
                os.makedirs(basedir, exist_ok=True)
                # write the file
                with open(os.path.join(basedir, name), "w") as f:
                    f.write(content)
            except Exception as e:
                print("Oops")
                print(e)
        
        print("Codebase built successfully. I think?")
        print("Thank you for choosing our services.")
        print("Goodbye.")
            
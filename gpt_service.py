import os
import openai
import json

class GPTService:
    def __init__(self, system_role="You are a helpful assistant who responds to my questions.", temperature=0):
        self.api_key = os.environ['OPENAI_API_KEY']
        self.user_prompt = ''
        self.response = ''
        self.system_role = system_role
        self.temperature = temperature
        openai.api_key = self.api_key

    def get_response(self, user_prompt):
        model = "gpt-3.5-turbo"
        self.response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": self.system_role},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
        )

        # Get the generated text
        generated_text = self.response['choices'][0]['message']['content']
        
        try:
            data = json.loads(generated_text)
            print(data)
            return data
        except json.JSONDecodeError:
            print(generated_text)
            return generated_text

    def prompt(self, user_prompt=None):
        if user_prompt is None:
            self.user_prompt = input("Please provide a prompt: ")
        else:
            self.user_prompt = user_prompt
        return self.get_response(self.user_prompt)


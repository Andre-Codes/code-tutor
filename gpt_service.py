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
        self.md_code_instruct = 'Surround any python code with a single backtick'
        self.md_table_instruct = "Format the parameters and examples as a markdown \
            table using the following instructions: To add a table, use three or \
                more hyphens (---) to create each column header, and use pipes (|) \
                    to separate each column. For compatibility, you should also add \
                        a pipe on either end of the row."

    def get_response(self, user_prompt, table=False):
        
        if table:
            user_content = f"{user_prompt}; {self.md_code_instruct}; {self.md_table_instruct}"
        else:
            user_content = f"{user_prompt}; {self.md_code_instruct}"
        
        model = "gpt-3.5-turbo"
        self.response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": self.system_role},
                {"role": "user", "content": user_content},
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


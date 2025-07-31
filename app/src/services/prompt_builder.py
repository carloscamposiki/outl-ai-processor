class PromptBuilder:

    def __init__(self):
        # Read .txt file with prompt template
        self.prompt_template = self._read_prompt_template()

    def build(self, trend_name: str, posts: list[str]):
        posts_as_string = "\n".join(posts)
        prompt = self.prompt_template.replace("[trend_name]", trend_name)
        prompt = prompt.replace("[posts]", posts_as_string)
        return prompt

    def _read_prompt_template(self):
        try:
            with open('prompt/prompt.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise Exception("Prompt template file not found.")

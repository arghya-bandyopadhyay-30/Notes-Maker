from ollama import chat

from processors.processor import Processor


class Translator(Processor):
    def translate(self, original_script: str) -> str:
        if not self.should_process():
            return original_script

        print(f"Translating the Hindi script to English...")
        prompt = self.prompt_factory.prompt(
            prompt_file="translation_prompt.yaml",
            prompt_key="translation",
            placeholders={
                "source_language": "hindi",
                "script": original_script
            }
        )

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": item.role,
                    "content": item.prompt,
                }
                for item in prompt.content
            ]
        )

        return response.message.content.strip()

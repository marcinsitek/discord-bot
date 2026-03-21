from transformers import AutoModelForCausalLM, AutoTokenizer

class LLMChatbot:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.history = {}

    def _get_user_history(self, user) -> list:
        if user in self.history:
            return self.history[user]
        else: 
            return []
    
    def _update_user_history(self, user, role, content) -> None:
        if user in self.history:
            self.history[user].append({"role": f"{role}", "content": f"{content}"})
        else:
            self.history[user] = []
            self.history[user].append({"role": f"{role}", "content": f"{content}"})


    async def generate_response(self, user, user_input) -> str:
        messages = self._get_user_history(user) + [{"role": "user", "content": user_input}]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        inputs = self.tokenizer(text, return_tensors="pt")
        response_ids = self.model.generate(**inputs, max_new_tokens=32768)[0][len(inputs.input_ids[0]):].tolist()
        response = self.tokenizer.decode(response_ids, skip_special_tokens=True)

        self._update_user_history(user, "user", user_input)
        self._update_user_history(user, "assistant", response)

        return response

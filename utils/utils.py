from litellm import completion

import dotenv
dotenv.load_dotenv()

anthropic_models = ['claude-3-5-sonnet-20240620', 'claude-3-haiku-20240307']

llm_provider = "anthropic"  #"azure"
messages = [{"role": "user", "content": "Hey! how's it going? Please answer in json format."}]
model_name = anthropic_models[0]

response = completion(messages=messages, model=model_name, custom_llm_provider=llm_provider)

# the same format for OpenAI and Anthropic
print(response["choices"][0]["message"]["content"])

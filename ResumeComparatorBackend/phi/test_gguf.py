from llama_cpp import Llama

# Specify the path to your GGUF model
model_path = "../ai_models/Phi-4-mini-instruct-Q3_K_L.gguf"

# Initialize the Llama model with the given GGUF model
llm = Llama(model_path=model_path)

# Example prompt to test the model
prompt = "What is quantum physics?"

# Run inference
output = llm(prompt, max_tokens=50)

# Print the result
print(output["choices"][0]["text"])
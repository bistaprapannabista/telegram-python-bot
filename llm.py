import ollama
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'how are you?',
  },
])
print(response['message']['content'])
# aiAmy


## Install for devs
Requirements :
-Python 3.11.9 (or above?)
-moondream2-text-model-f16.gguf and moondream2-mmproj-f16.gguf from https://huggingface.co/moondream/moondream2-gguf/tree/main (put it in ai_amy/ai_models directory)

Commands :
```
#Create a virtual env (=copy of your python install so the libs get installed only inside this ".venv" folder and not everywhere in the system).
python -m venv .venv

#Activate the venv.
.venv/Scripts/activate

#Install llama-cpp lib in binary format.
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

#Read the pypriject.toml and install the libs.
pip install -e .[dev]

#Launch the program.
python aiAmy/main.py
```

model_path = "llama2"
inference = NexaTextInference(
    model_path=model_path,
    local_path=None,
    stop_words=[],
    temperature=0.7,
    max_new_tokens=512,
    top_k=50,
    top_p=0.9,
    profiling=True
)

# run() method
inference.run()

# run_streamlit() method
inference.run_streamlit(model_path)

# create_embedding(input) method
inference.create_embedding("Hello, world!")

# create_chat_completion(messages)
inference.create_chat_completion(
    messages=[{"role": "user", "content": "write a long 1000 word story about a detective"}]
)

# create_completion(prompt)
inference.create_completion("Q: Name the planets in the solar system? A:")
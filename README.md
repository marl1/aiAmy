# aiAmy


## Install for devs
Requirements :
-Python 3.11.9 (because of some incompatibilities in the PyAV library used by nexaai https://github.com/PyAV-Org/PyAV/issues/1140 )
-llava-phi-3-mini-int4.gguf from https://huggingface.co/xtuner/llava-phi-3-mini-gguf/tree/main (put it in ai_amy/ai_models directory)
Commands :
```
#Create a virtual env (a copy of your python install basically) so the libs get installed only inside this ".venv" folder and not everywhere in the system.
python -m venv .venv

#Activate the venv.
.venv/Scripts/activate

#Install nexaai lib in binary form
pip install nexaai --prefer-binary --index-url https://github.nexa.ai/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir

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
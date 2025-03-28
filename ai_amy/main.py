from loguru import logger
from MainWindow import MainWindow
from nexa.gguf import NexaTextInference
import time

# Create the Windows for the character
main_window=MainWindow()

# inference = NexaTextInference(
#     model_path=None,
#     local_path="./ai_amy/ai_models/llava-phi-3-mini-int4.gguf",
#     stop_words=[],
#     temperature=0.7,
#     max_new_tokens=512,
#     top_k=50,
#     top_p=0.9,
#     profiling=True
# )

# run() method
#inference.run()

# run_streamlit() method
#inference.run_streamlit(model_path)

# create_embedding(input) method
#inference.create_embedding("Hello, world!")

# create_chat_completion(messages)
#inference.create_chat_completion(
#    messages=[{"role": "user", "content": "write a long 1000 word story about a detective"}]
#)

#time.sleep(5.5)
#print("lol")

# create_completion(prompt)
#var = inference.create_completion("Q: Name the planets in the solar system? A:")
#print("var",var)

#main_window.set_after(0, lambda: print(inference.create_completion("Q: From now on, you're Amy the friendly ai assistant/pet floating on the desktop. Say hello! A:")))

main_window.start_mainloop()

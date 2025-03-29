from MainWindow import MainWindow
from TextInference import *
from concurrent import futures

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class AmyController:
    def __init__(self):
        # Launch the LLM
        self.text_inference = TextInference()
        # Create the Windows for the character
        self.main_window=MainWindow(self)
        self.main_window.start_mainloop()

    def send_text(self, text):
        print("received ", text)
        thread_pool_executor.submit(self.fetch_answer, text)

    def fetch_answer(self, text):
        answer = self.text_inference.getAnswerTo(text)
        self.main_window.text_output.set_content(answer)
from ai_amy.main import AmyController

def run_application():
    AmyController()

# This block is important for running directly during development
# and prevents code from running automatically on import
if __name__ == "__main__":
    run_application()
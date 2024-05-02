import pdfparser
from chat import chatbot

def main():
    # Initialize the Chroma database
    chroma = pdfparser.initialize('pdfs')

    # Start the chatbot
    chatbot(chroma)

if __name__ == "__main__":
    main()

import time
import log
from openai import OpenAI
from validation import verify_facts
import pdfparser

def generate_response(user_input, client, chroma, accuracy):

    similar_docs = pdfparser.query(chroma, user_input)

    for doc in similar_docs[:accuracy]:
        content = ""
        content += doc
        # print(doc)

    # Generate a response
    log.log("Query GPT-4 Turbo for response")
    chat = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a cyber security assistant focusing on web development. Limit your responses to 100 words."},
                    {"role": "user", "content": "Here is the prompt: " + user_input + "If the prompt is not related to cyber security, return: I am here to answer cyber security related questions. If the prompt is related to cyber security, form your answer using only the following information, and do not ramble about irrelevant info: " + content }],
                stream=True,
            )
    log.log("Query GPT-4 Turbo for response")

    # for when stream off cause verify chat
    # response = chat.choices[0].message.content

    # fact checker method - not great
    '''if not verify_facts(chroma, response, accuracy):
        print("Error")'''

    print("\nSecLM: ", end="",)

    # Print the response character by character if stream off
    '''for char in response:
        print(char, end="", flush=True,)
        time.sleep(0.01)  # Delay'''

    # Print the response character by character
    log.log("Printing GPT-4 Turbo response")
    for chunk in chat:
            delta_content = chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else None
            if delta_content:
                print(delta_content, end="", flush=True,)
                time.sleep(0.1)  # Delay
    log.log("Printing GPT-4 Turbo response")

    print("\n")

def chatbot(chroma):
    # Print welcome message
    print("\nWelcome to SecLM! Enter your message below or type 'exit' to quit.\n")

    # Get accuracy setting 
    while True:
        accuracy = input("Enter your perferred accuracy setting (1 [fastest speeds] - 3 [medium] - 5 [verified results]): ")
        if (accuracy.isdigit() and int(accuracy) in [1, 3, 5]) or accuracy == 'exit':
            break
        else:
            print("\nInvalid input. Please enter a number from the following: [1, 3, 5].\n")

    if accuracy == 'exit':
        print("\nGoodbye!")
    else:
        print("\nAccuracy set to: " + accuracy + "!\n")

    while True:
        # Create an instance of the OpenAI class
        client = OpenAI(
             api_key='sk-proj-J1sz5dVtpp71rwqrVCugT3BlbkFJXFe4IcybAtqy8RELqlE6',
        )

        # Get user input
        user_input = input("User: ")

        if user_input.lower() == 'exit':
            break

        # Generate a response
        generate_response(user_input, client, chroma, int(accuracy))

    print("\nGoodbye!")

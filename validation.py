import spacy
import pdfparser

# Load a Spacy model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

def verify_facts(chroma, response, accuracy):
    
    # Extract facts from the response
    doc = nlp(response)
    facts = [ent.text for ent in doc.ents]

    # Fact check
    verified = False

    # Check if the response is default
    if response == "I am here to answer cyber security related questions.":
        verified = True
        return verified
    
    else: 
        for fact in facts:
            # Query the vector database
            similar_docs = pdfparser.query(chroma, fact)

            # Check if the fact is present in the similar documents
            for doc in similar_docs[:accuracy]:
                if fact in doc:
                    print(f"The fact '{fact}' is verified in the document: {doc}")
                    verified = True
                else:
                    print(f"The fact '{fact}' could not be verified in the document: {doc}")

        return verified
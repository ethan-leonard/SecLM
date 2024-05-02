# SecLM

This project is a cybersecurity AI assistant run through the terminal that utilizes PDF documents via a vector database to form its results.

## Project Setup

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of [Python](https://www.python.org/downloads/).

- You have installed the latest version of [Java](https://www.java.com/en/)


### Setup

To alter the contents of the vector database, simply add/remove PDFs from the PDFs folder.

1. Navigate to the `root` directory.

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv .env
    ```

    ### For Windows
    ```bash
    .env/Scripts/activate
    ```

    *If you get an error saying you can't run the script, run this command:*
    ```bash
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

    ### For Mac
    ```bash
    .env/bin/activate  
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. To start the application:

    ```bash
    python manage.py
    ```


## Use

Upon starting the application, you will receive a message welcoming you to SecLM.

1. First, you must choose your desired accuracy. There are three options: 1, 3, and 5. These values alter the amount of chunks supplied to GPT-4 assistant upon each query, respectively.

2. After you have selected your accuracy, you can begin querying the SecLM assistant. Ask any questions you have related to cybersecurity. The preinstalled PDFs specialize in website development security. 

3. When you are done, simply type 'exit' to end the program!


## Stack

- Python: Main language being used for the majority of the source code.

- Java: Used purely for the Tika library.

- Apache Tika: Java library used for parsing the PDF documents. Night and day difference in speed compared to the Python libraries.

- CharacterTextSplitter: From Langchain, used to split PDF text into chunks to be loaded into the vector database.

- HuggingFaceEmbeddings: From Langchain, used to create the model for the embeddings for the vector database. Can run on just CPU.

- Chroma: From Langchain, super-fast vector database. Loaded with all the PDF text using the embedding models made by HuggingFaceEmbeddings.


## Hallucination Mitigation

- Upon receiving a query from the user, SecLM first passes the query into the Chroma vector database and gets a verified result from the PDF documents. 

- In the event that the user's query is not covered in the documents, SecLM will return the response: "I am here to answer cybersecurity-related questions."

- The preloaded PDF documents contain NIST protocols, so a response to any cybersecurity question can be found within the vector database.

- After the Chroma vector database returns the relevant information, those chunks are passed into the GPT-4 model with the condition that the model must pull its answer from the given information.

- The accuracy adjuster feature allows users to change how many chunks of text are provided to the GPT-4 model. More chunks will mean a better response, but marginally longer wait time.


## Challenges and Insights

- Initially set off to create a validation.py file that would hold a function capable of detecting hallucinations in the returned response from the GPT-4 model. This resulted in the following issues:

    1. First problem was that the nature of this function would disable the streaming feature from the GPT-4 model as you would have to pass the response as a single string to the hallucination checker function.

    2. Second problem was that there is no good efficient method for detecting hallucinations:
        - I opted to first try out the Spacy en_core_web_sm to detect entities in the returned response and check them with the verified vector database. While this sounds promising, it quickly became apparent that all this function did was pull keywords out of the response and check if those words were in the chunks stored in the vector database. This provided very little insight into if the responses were actually factual.

        - I then opted to first run the query in the GPT-4 model, then the vector database, and then finally prompt GPT-4 to check whether the initial response from GPT-4 matched the vector database information. This method not only doubled the cost of each user query as the GPT-4 model was being called twice, it also doubled the time.

- Detecting hallucinations in a response from GPT-4 is extremely difficult. If this were an easy task, they would have already done it, and GPT-4 would never hallucinate. 

- Because my first solution did little to actually verify if the response was factual, and because my second solution was too costly in time and money, I instead opted to create a method to mitigate hallucinations instead of detect them.

- My hallucination mitigation method involves first querying the Chroma vector database upon receiving a query from the user, and then pass the resulting chunks into the GPT-4 model with the initial query and instruct it to form its answer purely based on the information provided by the chunks.

- This not only allows for only one call to the GPT-4 API, it also does a great job mitigating hallucinations as the response if formed from PDF documents, and it maintains the iconic speed of the GPT-4 model via streaming.

- Other than this, this project was pretty smooth sailing.


## Testing 

This project utilizes a log function in log.py that takes in a process name via string and adds to a log.txt file the times it completes tasks.

1. Performance Overview:

    - Splitting PDFs into Chunks: Around 0.005 seconds

    - Creating Embeddings Model: Around 4.2 seconds

    - Creating Chroma Vector Database: Around 13.3 seconds

    - Querying Chroma Vector Database: Around 0.005

    - Querying GPT-4 Turbo for Response: Ranges from around 0.8 seconds to 1.4 seconds

    - Printing GPT-4 Turbo Response: Ranges from around 7 seconds to 15 seconds

    - Parsing PDFs into List: Around 0.6 seconds

    From this, we can determine that creating the Chroma vector database is by far the most time-consuming task, and thankfully it only needs to be performed once at the start of every session.

2. Test Queries

    - 'Hello!' -> 'I am here to answer cybersecurity-related questions.'

    - 'What is pizza?' -> 'I am here to answer cybersecurity-related questions.'

    - 'Who is MrBeast?' -> 'I am here to answer cybersecurity-related questions.'

    - 'What is XSS in Django?' -> 'In Django, Cross-Site Scripting (XSS) is a security vulnerability that allows an attacker to inject client-side scripts into the browsers of other users. This can happen when malicious scripts are stored in the database, included in page content from untrusted sources like cookies or web services, or delivered through links that users click. Although using Django templates offers significant protection against XSS by automatically escaping variables, it is essential to ensure that all data is adequately sanitized to defend against any XSS attacks originating from untrusted sources.'

    - 'What is XSS in Next.js' -> 'An XSS (Cross-Site Scripting) attack in Next.js occurs when attackers inject malicious scripts into web pages viewed by other users. These scripts run on the user’s browser under the trusted domain of the website, allowing the attacker to steal cookies, session tokens, or other sensitive information displayed on the page. In the context of Next.js, which is a popular React framework, developers must ensure that user inputs are sanitized and that dynamic content is handled securely to prevent XSS vulnerabilities. Properly understanding and implementing security measures against XSS is crucial for maintaining the integrity of a web application.'

    - 'What is an SQL injection, and what features does Django have to prevent it?' -> 'SQL injection is a cybersecurity threat where attackers manipulate SQL queries by injecting malicious SQL code into them. This can lead to unauthorized access to or manipulation of database data. Django prevents SQL injection primarily through its querysets, which use query parameterization. In Django, the SQL code and the query parameters are defined separately, ensuring that user-provided parameters (which could be malicious) are safely escaped by the underlying database driver, thereby preventing the execution of harmful SQL code. This feature is inherent in Django’s ORM (Object-Relational Mapping) system, safeguarding applications from SQL injection attacks.'

    - 'What is an SQL injection, and what features does Next.js have to prevent it?' -> 'An SQL injection is a type of security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. It can allow the attacker to view data that they are not normally able to retrieve, manipulate or delete data, and potentially gain administrative rights to a database. Next.js, a framework for React applications, inherently encourages practices that help prevent SQL injections. Next.js does not directly handle database queries in its core framework, meaning that the actual prevention of SQL injections is dependent on the developer correctly handling data inputs and using safe methods to interact with databases, such as prepared statements or ORM libraries that escape SQL queries by default. Additionally, inputs such as URL parameters and headers are recognized as potential vectors for attacks and should be handled cautiously, ensuring they are properly sanitized and validated before use in database queries. This aligns with the principle of minimizing trust in client-supplied data to enhance app security.'

    - 'What is clickjacking?' -> 'Clickjacking is a type of cyber attack where attackers use visual deception to trick users into clicking on unseen elements on a webpage. Essentially, the user thinks they are interacting with legitimate buttons or links, but their actions are manipulated to perform unintended functions on another site. For example, a user might believe they are clicking to claim a prize but are inadvertently making a purchase on an e-commerce site. This exploit can have various harmful consequences, including unauthorized transactions and privacy breaches.'

    - 'According to NIST, what are the CSF tiers?' -> 'The NIST Cybersecurity Framework (CSF) Tiers, as explained in Section 3, categorize an organization’s cybersecurity practices into four levels based on how well they perceive risk and the processes they implement. Tier 1 (Partial) describes organizations with inconsistent cybersecurity practices. Tier 2 (Risk-Informed) represents organizations recognizing cyber risks but lacking a holistic company-wide approach. Tier 3 (Repeatable) denotes organizations with formally approved policies integrated across the business. Lastly, Tier 4 (Adaptive) characterizes organizations with proactive and adaptable cybersecurity responses that are continuously informed by current risk assessment and organizational learning.'

3. Test Query Evaluation

    - By looking at just the last test query, you can see that by using the Chroma vector database, the GPT-4 model returns a response directly from the provided documents, greatly mitigating any hallucinations.

    - Because this project is using a prebuilt vector database: Chroma, it is extremely efficient for loading and returning results. Even at the max accuracy setting, the responses from the SecLM model are comparable to ChatGPT's official website.

    - By simply implementing the vector database, there is now a far less chance that the model will hallucinate, and the responses will also be built on more factual data.


## Video

 - https://www.loom.com/share/64ade74788654c94828be52138986ca5?sid=b2664e26-0e83-47a4-a8f0-efdc1f951d8f
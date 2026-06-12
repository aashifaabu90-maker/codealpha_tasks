import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

from flask import Flask, request, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)

chat_history = []

faq = {
    "what is ai": "AI stands for Artificial Intelligence.",
    "what is machine learning": "Machine Learning is a subset of AI.",
    "what is python": "Python is a programming language.",
    "what is data science": "Data Science is the study of data.",
    "what is deep learning": "Deep Learning is a subset of Machine Learning.",
    "what is nlp": "NLP stands for Natural Language Processing.",
    "what is computer vision": "Computer Vision enables computers to understand images.",
    "what is flask": "Flask is a lightweight Python web framework.",
    "what is html": "HTML is used to create web pages.",
    "what is css": "CSS is used to style web pages.",
    "what is javascript": "JavaScript adds interactivity to websites.",
    "what is sql": "SQL is used to manage databases.",
    "what is database": "A database stores information.",
    "what is github": "GitHub is a platform for code hosting.",
    "what is api": "API allows software applications to communicate.",
    "what is cloud computing": "Cloud Computing provides services over the internet.",
    "what is cyber security": "Cyber Security protects systems from attacks.",
    "what is internet": "The Internet is a global network.",
    "what is wifi": "Wi-Fi allows wireless internet access.",
    "what is software": "Software is a set of computer instructions.",
    "what is hardware": "Hardware refers to physical computer components.",
    "what is algorithm": "An algorithm is a step-by-step solution.",
    "what is programming": "Programming is writing instructions for computers.",
    "what is java": "Java is a popular programming language.",
    "what is c++": "C++ is an extension of C language.",
    "what is operating system": "An operating system manages hardware and software.",
    "what is linux": "Linux is an open-source operating system.",
    "what is chatbot": "A chatbot is a program that interacts with users.",
    "what is internship": "An internship provides practical work experience.",
    "who are you": "I am an FAQ chatbot.",
    "what is tensorflow":"TensorFlow is a machine learning framework.",
    "what is pandas":"Pandas is a Python data analysis library.",
    "what is numpy":"NumPy is used for numerical computing.",
    "what is django":"Django is a Python web framework.",
    "what is bootstrap":"Bootstrap is a CSS framework.",
    "what is tensorflow":"TensorFlow is a machine learning framework.",
"what is keras":"Keras is a deep learning library.",
"what is pandas":"Pandas is a data analysis library.",
"what is numpy":"NumPy is used for numerical computing.",
"what is django":"Django is a Python web framework.",
"what is bootstrap":"Bootstrap is a CSS framework.",
"what is react":"React is a JavaScript library.",
"what is mysql":"MySQL is a relational database.",
"what is mongodb":"MongoDB is a NoSQL database.",
"what is data mining":"Data Mining finds patterns in data.",
"what is big data":"Big Data refers to extremely large datasets.",
"what is data analytics":"Data Analytics examines data for insights.",
"what is neural network":"A Neural Network is inspired by the human brain.",
"what is supervised learning":"Supervised Learning uses labeled data.",
"what is unsupervised learning":"Unsupervised Learning uses unlabeled data.",
"what is tensorflow":"TensorFlow is a machine learning framework.",
"what is keras":"Keras is a deep learning library.",
"what is pandas":"Pandas is a data analysis library.",
"what is numpy":"NumPy is used for numerical computing.",
"what is django":"Django is a Python web framework.",
"what is bootstrap":"Bootstrap is a CSS framework.",
"what is react":"React is a JavaScript library.",
"what is angular":"Angular is a front-end web framework.",
"what is nodejs":"Node.js allows JavaScript to run on servers.",
"what is mysql":"MySQL is a relational database management system.",
"what is mongodb":"MongoDB is a NoSQL database.",
"what is data mining":"Data Mining discovers patterns in data.",
"what is big data":"Big Data refers to very large datasets.",
"what is data analytics":"Data Analytics extracts insights from data.",
"what is neural network":"A Neural Network is inspired by the human brain.",
"what is supervised learning":"Supervised Learning uses labeled training data.",
"what is unsupervised learning":"Unsupervised Learning uses unlabeled data.",
"what is reinforcement learning":"Reinforcement Learning learns through rewards and penalties.",
"what is artificial intelligence":"Artificial Intelligence enables machines to mimic human intelligence.",
"what is machine vision":"Machine Vision allows computers to interpret visual information.",
"what is iot":"IoT stands for Internet of Things.",
"what is blockchain":"Blockchain is a distributed digital ledger.",
"what is cloud storage":"Cloud Storage stores data on remote servers.",
"what is aws":"AWS is Amazon's cloud computing platform.",
"what is azure":"Azure is Microsoft's cloud platform.",
"what is google cloud":"Google Cloud provides cloud computing services.",
"what is frontend":"Frontend is the user-facing part of a website.",
"what is backend":"Backend handles server-side operations.",
"what is full stack development":"Full Stack Development includes frontend and backend development.",
"what is web development":"Web Development is building websites and web applications.",
"what is app development":"App Development is creating software applications.",
"what is software testing":"Software Testing checks software quality.",
"what is debugging":"Debugging is finding and fixing errors in code.",
"what is version control":"Version Control tracks changes in code.",
"what is git":"Git is a distributed version control system.",
"what is open source":"Open Source software allows public access to source code.",
"what is compiler":"A Compiler converts source code into machine code.",
"what is interpreter":"An Interpreter executes code line by line.",
"what is oop":"OOP stands for Object-Oriented Programming.",
"what is inheritance":"Inheritance allows a class to acquire properties from another class.",
"what is polymorphism":"Polymorphism allows one interface to have multiple implementations.",
"what is encapsulation":"Encapsulation hides data within a class.",
"what is abstraction":"Abstraction hides implementation details.",
"what is exception handling":"Exception Handling manages runtime errors.",
"what is recursion":"Recursion is a function calling itself.",
"what is array":"An Array stores multiple values in a single variable.",
"what is linked list":"A Linked List is a linear data structure.",
"what is stack":"A Stack follows Last In First Out principle.",
"what is queue":"A Queue follows First In First Out principle.",
"what is binary tree":"A Binary Tree is a hierarchical data structure."
}

faq_questions = list(faq.keys())

def preprocess(text):
    text = text.lower()

    tokens = word_tokenize(text)

    stop_words = {
        "what","is","are","the",
        "a","an","about","define",
        "explain","tell","me"
    }

    tokens = [
        word for word in tokens
        if word.isalnum() and word not in stop_words
    ]

    return " ".join(tokens)

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FAQ Chatbot</title>
<style>
body{
    font-family:Arial,sans-serif;
    background:#f4f6f9;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
}
.box{
    background:white;
    padding:30px;
    width:700px;
    border-radius:15px;
    box-shadow:0 0 15px rgba(0,0,0,0.2);
}
h2{
    text-align:center;
}
input{
    width:95%;
    padding:10px;
    border:1px solid #ccc;
    border-radius:8px;
}
button{
    margin-top:10px;
    padding:10px 20px;
    background:#007bff;
    color:white;
    border:none;
    border-radius:8px;
    cursor:pointer;
}
.answer{
    margin-top:20px;
    background:#eef2f7;
    padding:15px;
    border-radius:8px;
}
.history{
    margin-top:20px;
}
</style>
</head>
<body>

<div class="box">

<h2>🤖 FAQ Chatbot</h2>

<form method="POST">

<input
type="text"
name="question"
placeholder="Ask a question..."
required>

<br>

<button type="submit">
Ask
</button>

</form>

{% if answer %}

<div class="answer">

<h3>Answer</h3>

<p>{{ answer }}</p>

</div>

{% endif %}

{% if history %}

<div class="history">

<h3>Chat History</h3>

{% for q,a in history %}

<p><b>You:</b> {{ q }}</p>

<p><b>Bot:</b> {{ a }}</p>

<hr>

{% endfor %}

</div>

{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        clean_question = preprocess(question)

        user_vector = vectorizer.transform(
            [clean_question]
        )

        similarity = cosine_similarity(
            user_vector,
            faq_vectors
        )

        best_match_index = similarity.argmax()
        best_score = similarity[0][best_match_index]

        print(best_score)

        if best_score > 0.8:

             best_score = similarity[0][best_match_index]

        if best_score > 0.6:

            matched_question = faq_questions[
                best_match_index
            ]

            answer = faq[
                matched_question
            ]

        else:

            answer = (
                "Sorry, I could not find "
                "a matching FAQ."
            )

        chat_history.append(
            (question, answer)
        )

    return render_template_string(
        HTML,
        answer=answer,
        history=chat_history
    )

if __name__ == "__main__":
    app.run(debug=True)

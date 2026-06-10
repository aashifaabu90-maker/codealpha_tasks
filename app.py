from flask import Flask, request, render_template_string
from deep_translator import GoogleTranslator

app = Flask(__name__)

history = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Language Translation Tool</title>

    <style>

        body{
            font-family: Arial, sans-serif;
            background:#f4f6f9;
            display:flex;
            justify-content:center;
            align-items:center;
            min-height:100vh;
        }

        .box{
            background:white;
            padding:30px;
            width:650px;
            border-radius:15px;
            box-shadow:0 0 15px rgba(0,0,0,0.2);
            text-align:center;
        }

        h2{
            color:#333;
        }

        textarea{
            width:95%;
            height:120px;
            padding:10px;
            border:1px solid #ccc;
            border-radius:8px;
            resize:none;
        }

        select{
            width:45%;
            padding:10px;
            margin:10px;
            border:1px solid #ccc;
            border-radius:8px;
        }

        button{
            padding:10px 20px;
            margin:8px;
            border:none;
            border-radius:8px;
            background:#007bff;
            color:white;
            cursor:pointer;
        }

        button:hover{
            background:#0056b3;
        }

        .result{
            margin-top:20px;
            background:#eef2f7;
            padding:15px;
            border-radius:8px;
            text-align:left;
        }

    </style>

    <script>

        function copyText(){

            let text =
            document.getElementById("translatedText").innerText;

            navigator.clipboard.writeText(text);

            alert("Translation Copied!");
        }

        function swapLanguages(){

            let source =
            document.getElementsByName("source")[0];

            let target =
            document.getElementsByName("target")[0];

            let temp = source.value;

            source.value = target.value;

            target.value = temp;
        }

    </script>

</head>

<body>

<div class="box">

    <h2>🌍 Language Translation Tool</h2>

    <form method="POST">

        <textarea
        name="text"
        placeholder="Enter text here..."
        required></textarea>

        <br>

        
        <br><br>

<div style="display:flex; justify-content:space-between; margin-top:15px;">

    <div style="width:45%;">
        <label><b>Source Language</b></label>
        <br><br>

        <select name="source" style="width:100%;">
            <option value="en">English</option>
            <option value="ta">Tamil</option>
            <option value="hi">Hindi</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="es">Spanish</option>
        </select>
    </div>

    <div style="width:45%;">
    

<label><b>Target Language</b></label>
        

        <select name="target" style="width:100%;">
            <option value="ta">Tamil</option>
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="es">Spanish</option>
        </select>
    </div>

</div>
        
        </select>

        <br>

        <button type="button"
        onclick="swapLanguages()">

        Swap Languages

        </button>

        <br>

        <button type="submit">

        Translate

        </button>

        <button type="reset">

        Clear

        </button>

    </form>

    {% if result %}

    <div class="result">

        <h3>Translated Text</h3>

        <p id="translatedText">

            {{ result }}

        </p>

        <button
        type="button"
        onclick="copyText()">

        Copy

        </button>

    </div>

    {% endif %}

    {% if history %}

    <div class="result">

        <h3>Recent Translations</h3>

        {% for item in history %}

        <p>

        <b>Input:</b>

        {{ item.original }}

        </p>

        <p>

        <b>Output:</b>

        {{ item.translated }}

        </p>

        <hr>

        {% endfor %}

    </div>

    {% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        text = request.form["text"]
        source = request.form["source"]
        target = request.form["target"]

        try:

            result = GoogleTranslator(
                source=source,
                target=target
            ).translate(text)

            history.insert(0, {
                "original": text,
                "translated": result
            })

            if len(history) > 5:
                history.pop()

        except Exception:

            result = "Translation failed. Please try again."

    return render_template_string(
        HTML,
        result=result,
        history=history
    )

if __name__ == "__main__":
    app.run(debug=True)

from sanic import Sanic
from sanic_cors import CORS
import base64
import os
import whisper
import textwrap
from sanic.request import Request
from sanic.response import HTTPResponse, json, text
from sanic_ext import Extend

app = Sanic("api")
app.config.CORS_ORIGINS = "*"
Extend(app)


@app.route("/upload", methods=["POST"])
async def upload_audio(request: Request) -> HTTPResponse:
    base64_data = request.body.decode()
    filename = request.args.get("name")

    image_data = base64.b64decode(base64_data)

    with open(f"uploads/{filename}", "wb") as f:
        f.write(image_data)
    return text("upload successful")

@app.route("/process", methods=["POST", "GET"])
async def process_audio(request: Request) -> HTTPResponse:
    file_name = request.args.get("name")
    model = whisper.load_model("base")
    result = model.transcribe(f"uploads/{file_name}", fp16=False, language="English")
    wrapped_text = textwrap.fill(result["text"], width=80, break_long_words=False)
    os.remove(f"uploads/{file_name}")
    return text(wrapped_text)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port)

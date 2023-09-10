import io
import webbrowser
from typing import Any

from flask import Flask, flash, render_template, request, send_file
from PIL import Image

from pydis_jam23.codecs import CODECS, Codec, CodecError, CodecParam

app = Flask(__name__)
app.secret_key = "secret"  # We're only running locally.

# Yep, it's a global mutable variable. It *should* work fine though since
# there's only one user.
current_image: Image.Image | None = None


def run_server():
    webbrowser.open("http://localhost:5000", new=2)
    app.run()


@app.route("/")
def index():
    return render("index.j2")


@app.route("/codec/<codec>")
def get_codec(codec: str):
    return render("codec.j2", codec=find_codec(codec))


@app.route("/encode/<codec>", methods=["GET"])
def get_encode(codec: str):
    return render("action.j2", codec=find_codec(codec), encode=True)


@app.route("/encode/<codec>", methods=["POST"])
def post_encode(codec: str):
    global current_image  # noqa: PLW0603 - global mutable
    if current_image is None:
        msg = "No image loaded"
        raise ValueError(msg)
    codec_obj = find_codec(codec)
    message = request.form["message"].encode("utf-8")
    extra_args = get_args(codec_obj.params + codec_obj.encode_params)
    try:
        current_image = codec_obj.encode(current_image, message, **extra_args)
        print(current_image)
    except CodecError as e:
        flash(f"Encoding failed: {e}")
    return render("action.j2", codec=codec_obj, encode=True)


@app.get("/decode/<codec>")
def get_decode(codec: str):
    return render("action.j2", codec=find_codec(codec), encode=False)


@app.post("/decode/<codec>")
def post_decode(codec: str):
    if current_image is None:
        msg = "No image loaded"
        raise ValueError(msg)
    codec_obj = find_codec(codec)
    extra_args = get_args(codec_obj.params + codec_obj.decode_params)
    try:
        message = codec_obj.decode(current_image, **extra_args).decode("utf-8")
    except (CodecError, UnicodeDecodeError) as e:
        message = None
        flash(f"Decoding failed: {e}")
    return render("action.j2", codec=codec_obj, encode=False, decoded_message=message)


@app.get("/current_image")
def get_current_image():
    if not current_image:
        msg = "No image loaded"
        raise ValueError(msg)
    file = io.BytesIO()
    current_image.save(file, format="PNG")
    file.seek(0)
    return send_file(file, mimetype="image/png")


@app.post("/current_image")
def post_current_image():
    global current_image  # noqa: PLW0603 - global mutable
    file = request.files["image"]
    buffer = io.BytesIO()
    file.save(buffer)
    buffer.seek(0)
    current_image = Image.open(buffer)
    current_image.load()
    return "OK", 200


def find_codec(short_name: str) -> Codec:
    for codec in CODECS:
        if codec.short_name == short_name:
            return codec
    msg = f"Codec {short_name} not found"
    raise ValueError(msg)


def get_args(params: list[CodecParam]) -> dict[str, Any]:
    args: dict[str, Any] = {}
    for param in params:
        args[param.name] = param.type_(request.form.get(param.name, param.default))
    return args


def render(template: str, **kwargs: object):
    return render_template(
        template,
        codecs=CODECS,
        current_image=bool(current_image),
        issubclass=issubclass,
        bool=bool,
        int=int,
        **kwargs,
    )

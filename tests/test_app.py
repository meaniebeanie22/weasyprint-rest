import time
import os
import hashlib
import mimetypes
from werkzeug.datastructures import FileStorage


def test_app():
    pass


def test_get_health_status(client):
    res = client.get("/api/v1.0/health")
    assert "status" in res.json and res.json["status"] == "OK"


def test_get_health_timestamp(client):
    min_time = round(time.time() * 1000)
    max_time = min_time + 1000
    res = client.get("/api/v1.0/health")
    assert "timestamp" in res.json and min_time <= int(res.json["timestamp"]) <= max_time


def test_post_print_no_mode(client):
    data = get_print_input()
    res = client.post(
        "/api/v1.0/print",
        content_type='multipart/form-data',
        data=data,
        headers=auth_header()
    )
    assert res.status_code == 200 and res.headers['Content-Type'] == "application/pdf"


def test_post_print_access_deny(client):
    res = client.post(
        "/api/v1.0/print",
        content_type='multipart/form-data'
    )
    assert res.status_code == 401


def test_post_print_html_missing_params(client):
    res = client.post(
        "/api/v1.0/print",
        content_type='multipart/form-data',
        headers=auth_header()
    )
    assert res.status_code == 422


def get_print_input(use_template=True):
    input_dir = get_path("./resources/report")
    template_dir = get_path("./resources/templates/report")

    data = {
        "html": read_file(input_dir, "report.html"),
    }

    if use_template:
        data["template"] = "report"
    else:
        data.update({
            "style": read_file(template_dir, "report.css"),
            "asset[]": [
                # TODO: Fonts does currently not work
                read_file(template_dir, "FiraSans-Bold.otf"),
                read_file(template_dir, "FiraSans-Italic.otf"),
                read_file(template_dir, "FiraSans-LightItalic.otf"),
                read_file(template_dir, "FiraSans-Light.otf"),
                read_file(template_dir, "FiraSans-Regular.otf"),
                read_file(template_dir, "heading.svg"),
                read_file(template_dir, "internal-links.svg"),
                read_file(template_dir, "multi-columns.svg"),
                read_file(template_dir, "report-cover.jpg"),
                read_file(template_dir, "style.svg"),
                read_file(template_dir, "table-content.svg")
            ]
        })

    return data


def read_file(path, filename):
    abs_path = os.path.join(path, filename)
    return FileStorage(
        stream=open(abs_path, "rb"),
        filename=filename,
        content_type=mimetypes.guess_type(filename)[0],
    )


def write_file(path, filename, data):
    abs_path = os.path.join(path, filename)
    with open(abs_path, "wb") as file:
        file.write(data)


def verify_output(data):
    input_file = get_path("./resources/report/result.png")
    data_hash = hashlib.sha1(data).hexdigest()
    with open(input_file, "rb") as file:
        input_data = file.read()
        input_hash = hashlib.sha1(input_data).hexdigest()
        return data_hash == input_hash
    return False


def get_path(relative_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, relative_path)


def auth_header():
    return {"X_API_KEY": "SECRET_API_KEY"}

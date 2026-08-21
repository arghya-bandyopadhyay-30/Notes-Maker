import re
import subprocess
import time
from pathlib import Path

import requests

from utils.environment_system import EnvironmentSystem


environment_system = EnvironmentSystem()

opencode_path = environment_system.find_executable("opencode")

opencode_process = environment_system.start_process([opencode_path, "serve"])

try:
    for i in range(30):
        output = opencode_process.stdout.readline()
        print(f"[{i}] {output}", end="")

        match = re.search(
            r"http://127\.0\.0\.1:\d+",
            output,
        )

        if match:
            base_url = match.group()
            print(f"Found URL: {base_url}")
            break
    else:
        raise RuntimeError(
            "Failed to determine the OpenCode server URL."
        )

    print(f"\nOpenCode server: {base_url}")

    time.sleep(2)

    print("Creating session...")
    session = requests.post(
        f"{base_url}/session",
        json={},
        timeout=10,
    ).json()
    print(f"Session created: {session['id']}")

    content = Path(
        "output/_R_d3ibfttY.txt"
    ).read_text(
        encoding="utf-8"
    )

    start_time = time.perf_counter()

    response = requests.post(
        f"{base_url}/session/{session['id']}/message",
        json={
            "parts": [
                {
                    "type": "text",
                    "text": (
                        "Translate this Hindi script to natural English:\n"
                        f"{content}"
                    ),
                }
            ]
        },
        timeout=300,
    ).json()

    end_time = time.perf_counter()

    text = next(
        part["text"]
        for part in response["parts"]
        if part["type"] == "text"
    )

    print(text.encode('utf-8', errors='replace').decode('utf-8'))

    print(
        f"\nLLM processing time: "
        f"{end_time - start_time:.2f} seconds"
    )

finally:
    opencode_process.terminate()
    opencode_process.wait()
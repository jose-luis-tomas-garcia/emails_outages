from crewai_tools import BaseTool
import time
import os


class file_writer(BaseTool):
    name: str = "File writer"
    description: str = "Writes contents to a local file. "
    def _run(self, file_name: str, contents: str) -> str:
        try:
            with open(file_name, "w") as f:
                f.write(contents)
            print(f"File written to {file_name}.")
            return contents
        except Exception:
            return "Failed to save contents."

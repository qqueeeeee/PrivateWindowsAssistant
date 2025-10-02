from llama_index.core.tools import FunctionTool
import os

note_file = os.path.join("data", "notes.txt")

def save_note(note: str) -> str:
    os.makedirs(os.path.dirname(note_file), exist_ok=True)
    with open(note_file, "a", encoding="utf-8") as f:
        f.write(note + "\n")
    return f"Note saved: {note}"

note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="Use this tool when the user wants to save a note of something. Append a plain text note to notes.txt. Takes a single string (the note)."
)
# Import libraries
import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

# Function to take one raw zoom txt file and output one formatted txt file
def process_zoom_chat(input_file: str, output_file: str) -> None:
    """
    Process one .txt file in the input directory and save result to the output directory
    """
    messages: Dict[str, Tuple[str, str]] = {}
    replies: Dict[str, List[Tuple[str, str, str]]] = defaultdict(list)
    root_messages_order: List[str] = []

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        if not line.strip() or "Reacted to" in line:
            i += 1
            continue

        msg_match = re.match(r"^(\d{2}:\d{2}:\d{2})\t([^\t]+):\t(.*)", line)
        if msg_match:
            timestamp, name, content = msg_match.groups()

            if content.startswith("Replying to "):
                snippet_match = re.match(r'Replying to "([^"]+)"', content)
                snippet = snippet_match.group(1) if snippet_match else ""
                # remove trailing dots / ellipsis to aid matching
                snippet = snippet.rstrip(" .\u2026")

                i += 1
                reply_lines: List[str] = []
                while i < len(lines):
                    next_line = lines[i].rstrip("\n")
                    if re.match(r"^\d{2}:\d{2}:\d{2}\t", next_line):
                        break
                    if not next_line.strip():
                        i += 1
                        continue
                    reply_lines.append(next_line.strip())
                    i += 1

                reply_content = "\n".join(reply_lines)
                # Find the root message whose content contains the snippet
                # Iterate in reverse order so that replies attach to the most recent
                # matching message, which helps in cases where multiple messages
                # share the same truncated preview (happens more than I'd like)
                original_msg_id = None
                for msg_id in reversed(root_messages_order):
                    original_content = messages[msg_id][1]
                    if snippet and snippet in original_content:
                        original_msg_id = msg_id
                        break

                if original_msg_id and reply_content:
                    replies[original_msg_id].append((timestamp, name, reply_content))
                elif reply_content:
                    # unmatched reply becomes its own root message
                    msg_id = f"{timestamp}\t{name}:\t{reply_content}"
                    messages[msg_id] = (name, reply_content)
                    root_messages_order.append(msg_id)
                continue
            else:
                # regular message
                msg_id = f"{timestamp}\t{name}:\t{content}"
                messages[msg_id] = (name, content)
                root_messages_order.append(msg_id)
                i += 1
                continue
        else:
            i += 1
            continue

    with open(output_file, "w", encoding="utf-8") as f_out:
        for msg_id in root_messages_order:
            name, content = messages[msg_id]
            f_out.write(f"{name}\n{content}\n\n")
            if msg_id in replies:
                f_out.write(f"Replies to {name}:\n")
                for _, reply_name, reply_content in replies[msg_id]:
                    f_out.write(f"\t{reply_name}\n\t{reply_content}\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python zoom-formatter-new.py <input_file> <output_file>")
        sys.exit(1)
    in_file, out_file = sys.argv[1], sys.argv[2]
    process_zoom_chat(in_file, out_file)

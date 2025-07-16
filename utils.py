def print_header(title: str):
    line = "─" * (len(title) + 4)
    print(f"\n╭{line}╮")
    print(f"│  {title}  │")
    print(f"╰{line}╯")

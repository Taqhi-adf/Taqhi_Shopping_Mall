from graph import graph

if __name__ == "__main__":
    print("=" * 70)
    print("TAQHI SHOPPING MALL — LOCAL AI OPERATIONS ASSISTANT")
    print("Type 'exit' to stop.")
    print("=" * 70)

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        try:
            result = graph.invoke({"question": question})
            print("\nAI:\n")
            print(result.get("answer", "No answer returned."))
        except Exception as exc:
            print(f"ERROR: {exc}")

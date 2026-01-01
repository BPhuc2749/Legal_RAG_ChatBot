from app.pipeline import LegalRAGPipeline

if __name__ == "__main__":
    rag = LegalRAGPipeline()

    while True:
        q = input("Question (type 'exit' to quit): ").strip()
        if q.lower() == "exit":
            break

        result = rag.run(q)

        print("\nAnswer:\n", result["answer"])
        print("\nSources:")
        for c in result["contexts"]:
            print(f"- {c['source_type']} | {c['source']} | page {c['page']}")
        print(f"\nLatency: {result['latency']:.2f}s\n")

import os
import time
from datetime import datetime

from app.pipeline import LegalRAGPipeline

QUESTIONS_FILE = "notes/eval_questions.md"
OUTPUT_DIR = "notes/eval_results"


def load_questions(path: str) -> list[str]:
    questions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("-"):
                questions.append(line[1:].strip())
    return questions


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rag = LegalRAGPipeline()

    questions = load_questions(QUESTIONS_FILE)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(OUTPUT_DIR, f"run_{ts}.md")

    total_latency = 0.0

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Eval Run {ts}\n\n")
        f.write(f"Total questions: {len(questions)}\n\n")

        for i, q in enumerate(questions, 1):
            result = rag.run(q)

            latency = result["latency"]
            total_latency += latency
            citations = result["contexts"]

            f.write(f"## Q{i}: {q}\n\n")
            f.write(f"**Latency:** {latency:.2f}s\n\n")
            f.write(f"**Citations:** {len(citations)}\n\n")

            # rút gọn answer
            answer_preview = result["answer"][:800]
            f.write("**Answer (preview):**\n\n")
            f.write(answer_preview + "\n\n")
            f.write("---\n\n")

        avg_latency = total_latency / len(questions) if questions else 0.0

        f.write("## Summary\n\n")
        f.write(f"- Questions: {len(questions)}\n")
        f.write(f"- Avg latency: {avg_latency:.2f}s\n")

    print(f"[DONE] Eval report saved to {out_path}")


if __name__ == "__main__":
    main()

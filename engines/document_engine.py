# document_engine.py
import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from llama_index.core.tools import FunctionTool
import fitz  

class DocumentEngine:
    def __init__(self, pdf_dir="data\\College_PDFs\\", chunk_size=1000, overlap=200, store_file="data\\College_PDFs\\index_data.faiss"):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self.sources = []
        self.embeddings = None
        self.index = None
        self.store_file = Path(store_file)
        self.pdf_dir = Path(pdf_dir)
        self.meta_file = self.store_file.with_suffix(".json")

        if self.store_file.exists() and self.meta_file.exists():
            self._load_index()
            self._process_new_pdfs()
        else:
            self._load_pdfs(list(self.pdf_dir.glob("*.pdf")))
            self._save_index()

    def _chunk_text(self, text):
        chunks, start = [], 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks

    def _extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        return "\n".join(page.get_text() for page in doc)

    def _load_pdfs(self, pdf_files):
        new_chunks, new_sources, new_embeddings = [], [], []

        for pdf_file in pdf_files:
            print("Reading PDF:", pdf_file.name)
            text = self._extract_text(pdf_file)
            chunks = self._chunk_text(text)

            if not chunks:
                print(f"No text found in {pdf_file.name}. Skipping.")
                continue

            embeddings = self.embedder.encode(chunks, convert_to_numpy=True, batch_size=32, show_progress_bar=True)

            new_chunks.extend(chunks)
            new_sources.extend([pdf_file.name] * len(chunks))
            new_embeddings.extend(embeddings)

        if not new_chunks:
            return

        if self.index is None:
            dim = new_embeddings[0].shape[0]
            self.index = faiss.IndexFlatL2(dim)
            self.chunks = new_chunks
            self.sources = new_sources
            self.embeddings = np.array(new_embeddings, dtype="float32")
        else:
            self.chunks.extend(new_chunks)
            self.sources.extend(new_sources)
            self.embeddings = np.vstack([self.embeddings, np.array(new_embeddings, dtype="float32")])

        self.index.add(np.array(new_embeddings, dtype="float32"))

    def _save_index(self):
        faiss.write_index(self.index, str(self.store_file))
        meta = {
            "chunks": self.chunks,
            "sources": self.sources,
            "processed_pdfs": list(set(self.sources))  # which PDFs we’ve indexed
        }
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f)

    def _load_index(self):
        self.index = faiss.read_index(str(self.store_file))
        with open(self.meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.chunks = meta["chunks"]
        self.sources = meta["sources"]

    def _process_new_pdfs(self):
        all_pdfs = {pdf.name: pdf for pdf in self.pdf_dir.glob("*.pdf")}
        with open(self.meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        processed_pdfs = set(meta.get("processed_pdfs", []))

        new_pdfs = [path for name, path in all_pdfs.items() if name not in processed_pdfs]

        if new_pdfs:
            print("Found new PDFs:", [p.name for p in new_pdfs])
            self._load_pdfs(new_pdfs)
            self._save_index()
        else:
            print("No new PDFs to process.")

    def search(self, query, k=3, subject=None):
        q_emb = self.embedder.encode([query], convert_to_numpy=True)

        if subject:  
            mask = [i for i, src in enumerate(self.sources) if subject.lower() in src.lower()]
            if not mask:
                return [(f"No results found for subject '{subject}'", subject)]
            subject_embs = self.embeddings[mask]
            D, I = faiss.IndexFlatL2(subject_embs.shape[1]).search(np.array(q_emb, dtype="float32"), k)
            results = []
            for idx in I[0]:
                if idx < len(mask):
                    real_idx = mask[idx]
                    results.append((self.chunks[real_idx], self.sources[real_idx]))
            return results
        else:
            D, I = self.index.search(np.array(q_emb, dtype="float32"), k)
            return [(self.chunks[idx], self.sources[idx]) for idx in I[0]]


# Lazy-loaded singleton for faster startup
doc_engine = None

def get_doc_engine():
    """Lazy initialization of document engine"""
    global doc_engine
    if doc_engine is None:
        doc_engine = DocumentEngine(pdf_dir="data\\College_PDFs\\")
    return doc_engine

def query_documents(query: str) -> str:
    try:
        subject = None
        if "subject:" in query.lower():
            parts = query.split("subject:")
            query, subject = parts[0].strip(), parts[1].strip()

        # Initialize document engine only when needed
        engine = get_doc_engine()
        results = engine.search(query, subject=subject)
        
        if not results:
            return "No relevant documents found for your query."
        
        return "\n\n".join([f"[{src}] {text}" for text, src in results])
    except Exception as e:
        return f"Document search is initializing. Please try again in a moment."

document_tool = FunctionTool.from_defaults(
    fn=query_documents,
    name="document_engine",
    description="Look up information in my notes/syllabus PDFs and return useful text with the PDF name. You can also specify a subject with `subject:SUBJECT_NAME`."
)

"""
AI KNOWLEDGE AGENT WITH STRUCTURED DICTIONARY OUTPUT
Retrieves context from FAISS index and generates structured responses
used dataclass for better structure
Note: do not forget to run ingest.py file before this file-to extact data
"""

import faiss
import numpy as np
import requests
import pickle
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

INDEX_PATH = "index.faiss"
META_PATH = "metadata.pkl"

# ============================================================================
# STRUCTURED DATA CLASSES
# ============================================================================

@dataclass
class Citation:
    """Structured citation information."""
    document_name: str
    section_id: str
    page_number: int
    paragraph_number: int
    relevance_score: float
    text_excerpt: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class AgentResponse:
    """Structured agent response."""
    case_id: str
    timestamp: str
    query: str
    answer: str
    confidence: str  # "high", "medium", "low"
    citations: List[Dict]
    risk_factors: List[str]
    recommendations: List[str]
    requires_manual_review: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict:
        return asdict(self)

    def format_output(self) -> str:
        """Format response for display."""
        output = []
        output.append("\n" + "="*80)
        output.append(f"📋 CASE ID: {self.case_id}")
        output.append(f"🕐 TIMESTAMP: {self.timestamp}")
        output.append("="*80)
        
        output.append(f"\n❓ QUERY:")
        output.append(f"   {self.query}")
        
        output.append(f"\n💬 ANSWER:")
        output.append(f"   {self.answer}")
        
        output.append(f"\n🎯 CONFIDENCE: {self.confidence.upper()}")
        
        if self.citations:
            output.append(f"\n📚 CITATIONS ({len(self.citations)}):")
            for idx, citation in enumerate(self.citations, 1):
                output.append(f"   [{idx}] {citation.get('document_name', 'Unknown')}")
                output.append(f"       Section: {citation.get('section_id', 'N/A')} | "
                            f"Page: {citation.get('page_number', 'N/A')} | "
                            f"Relevance: {citation.get('relevance_score', 0):.1%}")
        
        if self.risk_factors:
            output.append(f"\n⚠️  RISK FACTORS:")
            for risk in self.risk_factors:
                output.append(f"   • {risk}")
        
        if self.recommendations:
            output.append(f"\n💡 RECOMMENDATIONS:")
            for rec in self.recommendations:
                output.append(f"   • {rec}")
        
        if self.requires_manual_review:
            output.append(f"\n🚨 STATUS: REQUIRES MANUAL REVIEW")
        
        output.append("\n" + "="*80)
        return "\n".join(output)


# ============================================================================
# LOAD INDEX & METADATA
# ============================================================================

print("🔄 Loading FAISS index and metadata...")
try:
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        store = pickle.load(f)
    
    texts = store["texts"]
    metadata = store["metadata"]
    print(f" Loaded {len(texts)} documents")
except Exception as e:
    print(f" Error loading index: {e}")
    print("   Make sure index.faiss and metadata.pkl exist")
    exit(1)


# ============================================================================
# OLLAMA FUNCTIONS
# ============================================================================

def get_embedding(text: str) -> np.ndarray:
    """Get embedding from Ollama."""
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "llama3.2", # see the README.md file for more information to better perfomance
                "prompt": text
            },
            timeout=30
        )
        response.raise_for_status()
        return np.array(response.json()["embedding"], dtype="float32")
    except Exception as e:
        print(f"  Embedding error: {e}")
        return np.zeros(4096, dtype="float32")  # Fallback


def call_ollama(prompt: str, extract_json: bool = True) -> str:
    """Call Ollama for text generation."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()["response"].strip()
        
        if extract_json:
            # Try to extract JSON from response
            try:
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    result = result.split("```")[1].split("```")[0].strip()
                return result
            except:
                return result
        
        return result
    except Exception as e:
        print(f"  Ollama error: {e}")
        return json.dumps({
            "answer": f"Error: {str(e)}",
            "confidence": "low",
            "risk_factors": ["System error occurred"],
            "recommendations": ["Retry request or contact support"]
        })


# ============================================================================
# RETRIEVAL FUNCTION
# ============================================================================

def retrieve_context(query: str, top_k: int = 3) -> List[Dict]:
    """Retrieve relevant context from FAISS index."""
    query_embedding = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i, dist in zip(indices[0], distances[0]):
        if i < len(texts):
            # Calculate similarity score (convert L2 distance to similarity)
            similarity = 1 / (1 + float(dist))
            
            results.append({
                "text": texts[i],
                "metadata": metadata[i],
                "relevance_score": similarity
            })
    
    return results


# ============================================================================
# STRUCTURED AGENT FUNCTION
# ============================================================================

def ask_agent_structured(case_id: str, case_context: str, user_question: str) -> Dict[str, Any]:
    """
    Main agent function that returns structured dictionary output.
    
    Returns:
        Dictionary with keys:
        - case_id: str
        - timestamp: str
        - query: str
        - answer: str
        - confidence: str (high/medium/low)
        - citations: List[Dict]
        - risk_factors: List[str]
        - recommendations: List[str]
        - requires_manual_review: bool
        - metadata: Dict
    """
    
    # Step 1: Retrieve relevant context
    search_query = f"{case_context}. {user_question}"
    sources = retrieve_context(search_query, top_k=5)
    
    if not sources:
        return AgentResponse(
            case_id=case_id,
            timestamp=datetime.now().isoformat(),
            query=user_question,
            answer="No applicable policy information found in knowledge base.",
            confidence="low",
            citations=[],
            risk_factors=["No relevant policy documents found"],
            recommendations=["Manual review required", "Consult policy expert"],
            requires_manual_review=True,
            metadata={"sources_found": 0}
        ).to_dict()
    
    # Step 2: Build citations
    citations = []
    combined_sources = ""
    
    for idx, s in enumerate(sources, 1):
        meta = s["metadata"]
        
        citation = Citation(
            document_name=meta.get("document_name", f"Document_{idx}"),
            section_id=meta.get("section_id", "N/A"),
            page_number=meta.get("page_number", 0),
            paragraph_number=meta.get("paragraph_number", 0),
            relevance_score=s.get("relevance_score", 0.0),
            text_excerpt=s["text"][:200] + "..."
        )
        citations.append(citation.to_dict())
        
        combined_sources += f"\n--- SOURCE {idx} ---\n"
        combined_sources += f"Document: {citation.document_name}\n"
        combined_sources += f"Section: {citation.section_id}\n"
        combined_sources += f"Content: {s['text']}\n"
    
    # Step 3: Create structured prompt for AI
    prompt = f"""You are an AI insurance policy analyst. Analyze the case and provide a structured response.

STRICT REQUIREMENTS:
1. Use ONLY the provided policy sources
2. Do NOT invent or assume information
3. Be specific and cite policy sections
4. Identify risk factors and provide recommendations
5. Your response MUST be valid JSON

POLICY SOURCES:
{combined_sources}

CASE CONTEXT:
{case_context}

QUESTION:
{user_question}

Respond with ONLY a JSON object (no other text) with this exact structure:
{{
  "answer": "Clear, specific answer based on policy sources",
  "confidence": "high|medium|low",
  "risk_factors": ["list", "of", "risks"],
  "recommendations": ["list", "of", "recommendations"],
  "requires_manual_review": true|false
}}
"""
    
    # Step 4: Get AI response
    ai_response_text = call_ollama(prompt, extract_json=True)
    
    # Step 5: Parse AI response
    try:
        ai_data = json.loads(ai_response_text)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        ai_data = {
            "answer": ai_response_text,
            "confidence": "medium",
            "risk_factors": ["Unable to parse structured response"],
            "recommendations": ["Review response manually"],
            "requires_manual_review": True
        }
    
    # Step 6: Build final structured response
    response = AgentResponse(
        case_id=case_id,
        timestamp=datetime.now().isoformat(),
        query=user_question,
        answer=ai_data.get("answer", "No answer provided"),
        confidence=ai_data.get("confidence", "medium"),
        citations=citations,
        risk_factors=ai_data.get("risk_factors", []),
        recommendations=ai_data.get("recommendations", []),
        requires_manual_review=ai_data.get("requires_manual_review", False),
        metadata={
            "sources_found": len(sources),
            "avg_relevance": np.mean([s["relevance_score"] for s in sources]),
            "case_context": case_context
        }
    )
    
    return response.to_dict()


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def print_structured_output(response_dict: Dict[str, Any]):
    """Print the structured dictionary in a readable format."""
    response = AgentResponse(**response_dict)
    print(response.format_output())


def print_raw_dict(response_dict: Dict[str, Any]):
    """Print the raw dictionary (for debugging/API use)."""
    print("\n" + "="*80)
    print("📦 RAW DICTIONARY OUTPUT:")
    print("="*80)
    print(json.dumps(response_dict, indent=2))
    print("="*80)


# ============================================================================
# INTERACTIVE CHAT LOOP
# ============================================================================

def run_interactive_agent():
    """Run the agent in interactive mode."""
    print("\n" + "="*80)
    print("🤖 AI KNOWLEDGE AGENT - STRUCTURED OUTPUT MODE")
    print("="*80)
    print("Type 'exit' to quit, 'raw' to toggle raw dictionary output\n")
    
    case_context = input("📋 Enter case context: ")
    case_id = f"CASE-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    show_raw = False
    
    while True:
        question = input("\n❓ Ask a question: ")
        
        if question.lower() == "exit":
            print("\n Goodbye!")
            break
        
        if question.lower() == "raw":
            show_raw = not show_raw
            print(f"\n🔧 Raw dictionary output: {'ON' if show_raw else 'OFF'}")
            continue
        
        if not question.strip():
            continue
        
        print("\n🔄 Processing...")
        
        # Get structured response
        response_dict = ask_agent_structured(case_id, case_context, question)
        
        # Display based on mode
        if show_raw:
            print_raw_dict(response_dict)
        else:
            print_structured_output(response_dict)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def run_example():
    """Run example queries to demonstrate structured output."""
    print("\n" + "="*80)
    print("📘 RUNNING EXAMPLE QUERIES")
    print("="*80)
    
    case_id = "EXAMPLE-001"
    case_context = "Florida homeowner flood claim, $180,000 damage, basement flooding"
    
    questions = [
        "Is basement damage covered under flood insurance?",
        "What documentation is required for this claim?",
        "What are the processing time requirements in Florida?"
    ]
    
    for q in questions:
        print(f"\n\n{'='*80}")
        print(f"QUERY: {q}")
        print(f"{'='*80}")
        
        response_dict = ask_agent_structured(case_id, case_context, q)
        print_structured_output(response_dict)
        
        print("\n--- RAW DICTIONARY ---")
        print(json.dumps(response_dict, indent=2))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        run_example()
    else:

        run_interactive_agent()

"""
Simple Information Extraction Demo with LangChain and SCOPE

This demonstrates SCOPE learning with a simpler, more predictable task than research.
Information extraction shows clearer learning patterns and faster optimization.
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio

from config import SCOPE_DATA_PATH, ENABLE_SCOPE, OPENAI_API_KEY


# ============================================================================
# BASE PROMPT - Will evolve through SCOPE learning
# ============================================================================

BASE_EXTRACTION_PROMPT = """You are an information extraction specialist.
Your task is to extract requested information from text accurately.

## Core Instructions:
- Extract only the requested information
- Be accurate and precise
- If information is missing, state "Not found"
- Provide clean, structured output
"""


# ============================================================================
# EXTRACTION TASKS - Designed to trigger different learning patterns
# ============================================================================

EXTRACTION_TASKS = [
    # Task 1: Simple email extraction
    {
        "instruction": "Extract the email address",
        "text": "Contact John Doe at john.doe@example.com for support",
        "expected_pattern": "email"
    },
    
    # Task 2: Multiple fields (structured format)
    {
        "instruction": "Parse and extract: name, age, and city",
        "text": "Name: Jane Smith, Age: 28, City: Boston",
        "expected_pattern": "structured"
    },
    
    # Task 3: Missing data (error handling)
    {
        "instruction": "Extract the phone number",
        "text": "You can email us at support@company.com",
        "expected_pattern": "not_found"
    },
    
    # Task 4: Malformed data
    {
        "instruction": "Extract name, age, city, and phone",
        "text": "name:John|age:|city:NYC|phone:555-0123",
        "expected_pattern": "partial"
    },
    
    # Task 5: Multiple items
    {
        "instruction": "Extract all email addresses",
        "text": "Team members: alice@test.com, Bob <bob@example.org>, and charlie@mail.net",
        "expected_pattern": "multiple"
    },
    
    # Task 6: Complex nested
    {
        "instruction": "Parse and extract all contact information",
        "text": "Name: Michael Chen, Email: m.chen@corp.com, Phone: +1-555-0199, Department: Engineering",
        "expected_pattern": "complex"
    },
    
    # Task 7: Ambiguous format
    {
        "instruction": "Extract the full name",
        "text": "Dr. Sarah Williams-Johnson, PhD",
        "expected_pattern": "ambiguous"
    },
    
    # Task 8: Empty input (edge case)
    {
        "instruction": "Extract email address",
        "text": "",
        "expected_pattern": "empty"
    },
]


# ============================================================================
# SCOPE INTEGRATION
# ============================================================================

_scope_optimizer = None


def get_scope_optimizer():
    """Get or create SCOPE optimizer instance."""
    global _scope_optimizer
    if _scope_optimizer is None and ENABLE_SCOPE:
        try:
            from scope import SCOPEOptimizer
            from scope.models import create_openai_model
            
            scope_model = create_openai_model(
                model="gpt-4o",
                api_key=OPENAI_API_KEY
            )
            
            _scope_optimizer = SCOPEOptimizer(
                synthesizer_model=scope_model,
                exp_path=SCOPE_DATA_PATH,
                enable_quality_analysis=True,
                quality_analysis_frequency=1,
                synthesis_mode="efficiency",
                store_history=True
            )
            return _scope_optimizer
        except Exception as e:
            print(f"⚠️  SCOPE initialization failed: {e}")
            return None
    return _scope_optimizer


def _observe_with_scope(optimizer, agent_name, task, model_output, observations, current_prompt, task_id):
    """Helper to observe with SCOPE."""
    if optimizer is None:
        return None
    
    try:
        result = asyncio.run(
            optimizer.on_step_complete(
                agent_name=agent_name,
                agent_role="Information Extraction Specialist",
                task=task,
                model_output=model_output,
                observations=observations,
                error=None,
                current_system_prompt=current_prompt,
                task_id=task_id
            )
        )
        return result
    except Exception as e:
        print(f"⚠️  SCOPE observation failed: {e}")
        return None


# ============================================================================
# INFORMATION EXTRACTOR
# ============================================================================

class InfoExtractor:
    """Simple information extractor with SCOPE learning."""
    
    def __init__(self, scope_optimizer=None):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.scope_optimizer = scope_optimizer
        self.base_prompt = BASE_EXTRACTION_PROMPT
        self.tasks_completed = 0
        self.learning_events = 0
    
    def get_current_prompt(self):
        """Get current prompt with strategic rules if available."""
        prompt = self.base_prompt
        
        if self.scope_optimizer:
            try:
                strategic_rules = self.scope_optimizer.get_strategic_rules_for_agent(
                    "info_extractor"
                )
                if strategic_rules:
                    prompt += f"\n\n## Strategic Guidelines (Learned):\n{strategic_rules}"
            except:
                pass
        
        return prompt
    
    def extract(self, instruction: str, text: str, task_id: str):
        """Extract information from text."""
        current_prompt = self.get_current_prompt()
        
        # Build user message
        user_message = f"{instruction}\n\nText: {text}"
        
        # Call LangChain LLM
        messages = [
            SystemMessage(content=current_prompt),
            HumanMessage(content=user_message)
        ]
        
        response = self.llm.invoke(messages)
        output = response.content
        
        # Observe with SCOPE
        if self.scope_optimizer:
            observations = f"Extracted from text: '{text[:50]}...'"
            result = _observe_with_scope(
                self.scope_optimizer,
                agent_name="info_extractor",
                task=f"{instruction} | Text: {text}",
                model_output=output,
                observations=observations,
                current_prompt=current_prompt,
                task_id=task_id
            )
            
            if result:
                guideline, guideline_type = result
                self.learning_events += 1
                return {
                    "output": output,
                    "learned": True,
                    "guideline": guideline,
                    "guideline_type": guideline_type
                }
        
        self.tasks_completed += 1
        return {
            "output": output,
            "learned": False
        }


# ============================================================================
# DEMO EXECUTION
# ============================================================================

def run_simple_demo():
    """Run the simple extraction demo."""
    print("\n" + "="*70)
    print("SIMPLE DEMO: Information Extraction with SCOPE")
    print("="*70)
    print("This demo shows SCOPE learning with a simpler, more predictable task.")
    print("Information extraction provides clearer learning patterns.\n")
    
    # Initialize
    optimizer = get_scope_optimizer()
    if optimizer:
        print("✓ SCOPE optimizer initialized")
    else:
        print("⚠️  Running without SCOPE")
    
    extractor = InfoExtractor(scope_optimizer=optimizer)
    
    # Show initial prompt
    print("\n" + "="*70)
    print("INITIAL PROMPT")
    print("="*70)
    print(extractor.get_current_prompt())
    print("="*70 + "\n")
    
    # Run extraction tasks
    results = []
    for i, task in enumerate(EXTRACTION_TASKS, 1):
        print(f"\n{'='*70}")
        print(f"Task {i}/{len(EXTRACTION_TASKS)}")
        print(f"{'='*70}")
        print(f"Instruction: {task['instruction']}")
        print(f"Text: {task['text']}")
        print()
        
        result = extractor.extract(
            instruction=task['instruction'],
            text=task['text'],
            task_id=f"extraction_{i}"
        )
        
        print(f"Output: {result['output']}\n")
        
        if result['learned']:
            print(f"📚 SCOPE learned ({result['guideline_type']}): {result['guideline'][:100]}...")
        
        results.append({
            "task": i,
            "output": result['output'],
            "learned": result['learned']
        })
    
    # Show evolved prompt
    print("\n" + "="*70)
    print("EVOLVED PROMPT")
    print("="*70)
    print(extractor.get_current_prompt())
    print("="*70 + "\n")
    
    # Statistics
    print("="*70)
    print("STATISTICS")
    print("="*70)
    print(f"Tasks completed: {len(EXTRACTION_TASKS)}")
    print(f"Learning events: {extractor.learning_events}")
    print(f"Learning rate: {extractor.learning_events}/{len(EXTRACTION_TASKS)}")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    run_simple_demo()

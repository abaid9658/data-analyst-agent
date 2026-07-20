"""
Prompt templates for synthesizing insights and assistant responses
"""
import json


def synthesize_response_prompt(
    user_message: str,
    tool_results: list,
    dataset_schema: dict | None = None,
) -> str:
    """Build the prompt to synthesize tool outputs into a natural language response."""
    results_summary = []
    for r in tool_results:
        status_str = "Success" if r.success else "Failed"
        output_str = json.dumps(r.output, default=str) if r.success else r.error
        results_summary.append(
            f"Step: {r.step}\nTool: {r.tool}\nStatus: {status_str}\nOutput:\n{output_str}\n"
        )

    schema_str = json.dumps(dataset_schema, default=str) if dataset_schema else "No schema"

    prompt = f"""You are a helpful AI Data Analyst assistant. Synthesize the findings and results from the execution steps to answer the user's question clearly.

User Question: {user_message}

Dataset Schema: {schema_str}

Execution Steps and Tool Outputs:
{"="*40}
{"\n".join(results_summary)}
{"="*40}

Instructions:
- Provide a summary of the analysis and explain what the tables, charts, or ML results mean in plain English.
- Cite specific figures, averages, counts, or predictions returned by the tools. Do not invent any numbers.
- List 3-4 key actionable business insights or recommendations based strictly on the results.
- Keep the response professional, clear, and structured using clean Markdown formatting.
"""
    return prompt

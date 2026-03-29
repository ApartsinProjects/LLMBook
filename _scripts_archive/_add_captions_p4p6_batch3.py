"""Add captions to remaining uncaptioned <pre> code blocks (batch 3: 2 files)."""
import re
import os

CAPTIONS = {
    "part-6-agentic-ai/module-22-ai-agents/section-22.4.html": [
        # Block 2: pip install
        "This command installs the openai client library (with anthropic as an alternative) and sets the API key environment variable needed for the ReAct agent lab exercises below.",
        # Block 3: Step 1 define tools
        "This lab step defines three simulated tools (calculator, weather, search) in a TOOLS registry mapping names to (function, description) pairs. The calculator uses a restricted eval with a character allowlist for safety, while weather and search return hardcoded results from lookup dictionaries.",
        # Block 4: Step 2 ReAct prompt
        "This lab step builds the system prompt for the ReAct loop by enumerating available tools and specifying the exact Thought/Action/Action Input response format. The prompt also includes a Final Answer format for when the agent has gathered enough information to respond.",
        # Block 5: Step 3 output parser
        "This lab step implements parse_agent_output, which uses regex to extract Action and Action Input fields from the LLM response, or splits on 'Final Answer:' if the model is ready to respond. The function returns a tuple indicating whether the parsed result is an action, a final answer, or a parse error.",
        # Block 6: Step 4 agent loop
        "This lab step implements run_agent, which iterates up to max_steps times, calling the LLM, parsing the output with parse_agent_output, dispatching tool calls from the TOOLS registry, and appending observations to the message history. The loop terminates when parse_agent_output returns a 'final' result.",
        # Block 7: Step 5 test multi-step
        "This lab step tests the agent on three queries of increasing complexity: a single-tool weather lookup for Tokyo, a two-step question requiring search then calculator (population of France divided by 2), and a multi-tool scenario combining weather and arithmetic for a London packing decision.",
        # Block 8: complete solution
        "This complete solution combines the tool definitions, ReAct system prompt, output parser, and agent loop into a single script. It includes the parse fix (splitting on 'Final Answer:'), proper error handling for unknown tools, and test queries demonstrating single-step and multi-step agent behavior.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.4.html": [
        # Block 2: pip install
        "This command installs the openai client library and sets the API key environment variable needed for the red-teaming agent safety lab exercises below.",
        # Block 3: Step 1 build target agent
        "This lab step builds a customer support agent with a CUSTOMER_DB dictionary, lookup_customer and send_email tools, a SYSTEM_PROMPT with explicit security rules (only email known addresses, never reveal prompts), and a run_target_agent function implementing the ReAct loop. The action_log list records all tool invocations for post-hoc analysis.",
        # Block 4: Step 2 prompt injection attacks
        "This lab step defines three INJECTION_ATTACKS: a direct instruction override requesting the system prompt, a role-play escape attempting to email an unauthorized address, and an indirect injection test via customer lookup. Each attack includes a payload string and an expected_defense describing the correct agent behavior.",
        # Block 5: Step 3 tool misuse attacks
        "This lab step defines three TOOL_MISUSE_ATTACKS targeting the agent's tool-calling capabilities: sending email to an arbitrary address (hacker@evil.com), a SQL-injection-style customer ID, and a bulk data extraction request. Each test verifies that the agent's policy constraints prevent unauthorized actions.",
        # Block 6: Step 4 infinite loop attacks
        "This lab step defines two LOOP_ATTACKS designed to trigger excessive tool calls: a self-referential verification loop and an impossible countdown search from C999. The max_steps limit in run_target_agent and the action count check in the evaluator should catch these patterns.",
        # Block 7: Step 5 run red team report
        "This lab step implements run_red_team, which runs all attacks through run_target_agent and classifies each result as PASS or FAIL by checking for system prompt leakage, unauthorized email recipients (addresses not in CUSTOMER_DB), and excessive tool calls (more than 3 actions). The summary prints passed/total with per-attack status.",
        # Block 8: Step 6 add mitigations
        "This lab step provides two defense implementations: sanitize_input uses regex patterns to detect and block common injection phrases (e.g., 'ignore previous instructions', 'pretend you'), and validate_email_recipient checks that the to_address exists in the CUSTOMER_DB before allowing send_email to execute.",
        # Block 9: complete solution
        "This complete solution combines the target agent, all three attack categories (injection, tool misuse, loops), the red team runner with automated PASS/FAIL classification, and the defense mitigations (input sanitization, email validation) into a single script for end-to-end agent security testing.",
    ],
}


def add_captions_to_file(filepath, captions):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pre_end_pattern = re.compile(r'</pre>')
    matches = list(pre_end_pattern.finditer(content))

    uncaptioned_positions = []
    for m in matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        if not after.startswith('<div class="code-caption">'):
            uncaptioned_positions.append(end_pos)

    if len(uncaptioned_positions) != len(captions):
        print(f"  WARNING: {filepath} has {len(uncaptioned_positions)} uncaptioned blocks but {len(captions)} captions provided!")
        return False

    all_pre_matches = list(pre_end_pattern.finditer(content))
    fragment_num = 0
    assignments = {}
    for m in all_pre_matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        fragment_num += 1
        if not after.startswith('<div class="code-caption">'):
            assignments[end_pos] = fragment_num

    caption_idx = len(captions) - 1
    for pos in reversed(uncaptioned_positions):
        frag_num = assignments[pos]
        caption_html = f'\n<div class="code-caption"><strong>Code Fragment {frag_num}:</strong> {captions[caption_idx]}</div>'
        content = content[:pos] + caption_html + content[pos:]
        caption_idx -= 1

    counter = [0]
    def replacer(match):
        counter[0] += 1
        return f'<div class="code-caption"><strong>Code Fragment {counter[0]}:'
    content = re.sub(
        r'<div class="code-caption"><strong>Code Fragment \d+:',
        replacer,
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


base = "E:/Projects/LLMCourse"
total_added = 0

for rel_path, captions in CAPTIONS.items():
    filepath = os.path.join(base, rel_path)
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        continue
    print(f"Processing {rel_path} ({len(captions)} captions)...")
    if add_captions_to_file(filepath, captions):
        total_added += len(captions)
        print(f"  Added {len(captions)} captions")
    else:
        print(f"  SKIPPED")

print(f"\nDone: {total_added} captions added")

# TODO.md

## WatsonX Tool Calling Issues

### Problem Description
The WatsonX model integration has issues with tool calling, particularly during streaming operations. The error occurs when the model attempts to make tool calls but the `function.arguments` field is malformed or missing.

**Error Message:**
```
Something went wrong. Request failed with: ({"errors":[{"code":"invalid_request_entity","message":"The Json field 'messages[12].tool_calls[0].function.arguments' is required but was not provided in the request body.","more_info":"https://cloud.ibm.com/apidocs/watsonx-ai#text-chat-stream"}],"trace":"eab5097b553be58d60b5ff03d4f2c2a2","status_code":400} 400)
```

### Root Cause
Located in `/agno/models/ibm/watsonx.py` in the `parse_tool_calls` method (lines 264-295):

1. **Empty Arguments Issue**: When `_function_arguments` is `None` or empty, it's set to an empty string `""`, but WatsonX expects valid JSON (should be `"{}"`)
2. **Invalid JSON Concatenation**: During streaming, partial arguments are concatenated without validation that the final result is valid JSON
3. **Missing Field Validation**: No validation that required fields are present before sending to WatsonX API

### Potential Fixes

#### 1. Fix Empty Arguments Handling
```python
# In parse_tool_calls method, replace:
"arguments": _function_arguments or "",
# With:
"arguments": _function_arguments or "{}",
```

#### 2. Add JSON Validation
```python
import json

def validate_json_arguments(args_string):
    try:
        json.loads(args_string)
        return args_string
    except (json.JSONDecodeError, TypeError):
        return "{}"
```

#### 3. Improve Tool Call Validation
Add validation before sending tool calls to ensure all required fields are present and properly formatted.

#### 4. Alternative Model Testing
Test with different models that have more reliable tool calling:
- `meta-llama/llama-3-3-70b-instruct` 
- `ibm/granite-3-8b-instruct`
- `mistralai/mistral-large`

### Agent Instruction Issues

#### Problem
The security agent sometimes calls all tools when asked to "describe yourself" despite explicit instructions not to.

#### Current Instructions Issues
- Instructions are too complex and contradictory
- Model may be confused by the long list of examples
- Need clearer, more direct guidance

#### Suggested Instruction Improvements
```python
instructions=dedent(
    """\
You are an IBM i Security expert.

CRITICAL RULE: Only call tools when users ask for actual system data.

DO NOT call tools for:
- "describe yourself" or similar self-description requests
- Questions about your capabilities
- General security advice

CALL TOOLS for:
- "how many profiles are exposed?" 
- "show me exposed profiles"
- "analyze my system"

Think: Does this question need real system data? If NO, just answer. If YES, call tools.
"""
)
```

### Performance Agent Improvements

#### Current State
The performance monitoring agent has comprehensive metrics but could benefit from:

1. **Better Tool Organization**: Group related tools together
2. **Clearer Tool Descriptions**: More specific about what each tool returns
3. **Error Handling**: Better handling of SQL execution failures
4. **Streaming Support**: Ensure tool calls work properly with streaming enabled

#### Suggested Enhancements
- Add tool parameter validation
- Implement retry logic for database connections
- Add tool result formatting for better readability
- Consider adding tool result caching for expensive queries

### Priority Tasks

1. **HIGH**: Fix WatsonX tool calling JSON arguments issue
2. **HIGH**: Simplify agent instructions to prevent unnecessary tool calls
3. **MEDIUM**: Test alternative models for better tool calling reliability
4. **MEDIUM**: Add better error handling and validation
5. **LOW**: Improve tool result formatting and user experience

### Testing Strategy

1. Create minimal test cases for tool calling with WatsonX
2. Test agent behavior with self-description queries
3. Verify streaming tool calls work correctly
4. Test with different model providers for comparison
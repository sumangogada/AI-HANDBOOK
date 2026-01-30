
Prompt Engineering:
Not very useful because everything relies on the prompt given by the user and there is no control over the response so it can lead to errors or exceptions returned to the user.

Json Mode:
JSON mode is a more flexible capability that forces the LLM to always output a valid JSON string, but the JSON structure is arbitrary. It's useful when you need JSON output but don't want to specify the exact structure.
Json mode is more flexible and always returns the contents in json format but the instructions given may or may not be returned back .
For Example : You always need categories and content as keys to be returned , it will not be guaranteed.

Function calling mode:
if your use case can be framed to use function calling, it is recommended to use it. OpenAI will automatically optimize your prompt according to the specified functions, and the language models were trained with this prompt format. This increases the likelihood of better responses and reduces the frequency of hallucinations. Additionally, the response comes parsed in ChatCompletionMessageToolCall objects, which is convenient.
import tiktoken


encoding = tiktoken.encoding_for_model("gpt-5")

text = "Hello,Tell me a joke"

token_length = encoding.encode(text)

token_count = len(token_length)

print(f"No. of tokens : {token_count}")
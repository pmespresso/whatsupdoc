import hashlib
import itertools
import tiktoken
import re

tokenizer = tiktoken.get_encoding("cl100k_base")
# create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

new_separators = ["\n" * i for i in range(0, 43 + 1)]


def clean_text(text: str) -> str:
    cleaned_text = re.sub(r"\[\n\n\n\n\]", "", text)
    cleaned_text = re.sub(r"\[\s*__\s*\]", "", text)
    cleaned_text = re.sub(r"\[Music\]", "", cleaned_text)

    return cleaned_text


def get_ids(metadatas):
    return [
        hashlib.md5(
            f"{metadata['loc']}{metadata['text']}{metadata['chunk']}".encode()
        ).hexdigest()
        for metadata in metadatas
    ]

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))
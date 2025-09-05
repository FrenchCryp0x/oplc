# app/storage.py
import os, json, tempfile
from huggingface_hub import hf_hub_download
import zstandard as zstd

HF_DATASET_REPO = os.getenv("HF_DATASET_REPO")  # e.g., yourname/oplc-pp-mirror
# Use a writable temp dir by default; still honor env if set
CACHE_DIR = os.getenv("CACHE_DIR") or os.path.join(tempfile.gettempdir(), "oplc-cache")
os.makedirs(CACHE_DIR, exist_ok=True)

HEX = "0123456789ABCDEF"


def validate_prefix(prefix: str) -> None:
    if len(prefix) != 5 or any(c not in HEX for c in prefix):
        raise ValueError("prefix must be 5 hex chars (SHA-1 uppercased)")

def shard_name(prefix: str) -> str:
    return f"pp-{prefix[:2].lower()}.jsonl.zst"

async def get_suffixes_from_hf(prefix: str) -> list[str]:
    if not HF_DATASET_REPO:
        raise ValueError("HF_DATASET_REPO unset for hf mode")
    local_path = hf_hub_download(repo_id=HF_DATASET_REPO, filename=f"data/{shard_name(prefix)}", repo_type="dataset", cache_dir=CACHE_DIR)
    res: list[str] = []
    dctx = zstd.ZstdDecompressor()
    with open(local_path, "rb") as fh:
        with dctx.stream_reader(fh) as reader:
            buf = b""
            while True:
                chunk = reader.read(1 << 16)
                if not chunk: break
                buf += chunk
                *lines, buf = buf.split(b"\n")
                for line in lines:
                    if not line: continue
                    try:
                        obj = json.loads(line)
                        if obj.get("prefix") == prefix:
                            res.append(f"{obj['suffix']}:{obj['count']}")
                    except Exception:
                        continue
    return res

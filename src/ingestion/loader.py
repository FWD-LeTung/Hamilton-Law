import os
from pathlib import Path
from huggingface_hub import snapshot_download

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
PROJEECT_ROOT = Path(__file__).resolve().parent.parent.parent

snapshot_download(
    repo_id="th1nhng0/vietnamese-legal-documents",
    repo_type="dataset",
    local_dir=PROJEECT_ROOT / "data"
)
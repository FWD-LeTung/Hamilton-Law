import os
import polars as pl
from pathlib import Path

from langchain_core.documents import Document
from huggingface_hub import snapshot_download

import psutil
process = psutil.Process(os.getpid())
def mem():
    return process.memory_info().rss/1024/1024

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data"
CONTENT_PATH = DATA_PATH / "data" / "content.parquet"
METADATA_PATH = DATA_PATH / "data" / "metadata.parquet"
def download_dataset():
    snapshot_download(
        repo_id="th1nhng0/vietnamese-legal-documents",
        repo_type="dataset",
        local_dir=DATA_PATH
    )

def load_documents():
    
    df_merged = (
        pl.scan_parquet(CONTENT_PATH)
        .join(
            pl.scan_parquet(METADATA_PATH), 
            on="id", 
            how="left"
        )
    ).select(["id", "title", 
              pl.col("loai_van_ban").alias("doc_type"), 
              pl.col("co_quan_ban_hanh").alias("authority"), 
              pl.col("ngay_ban_hanh").alias("issue_date"), 
              pl.col("ngay_co_hieu_luc").alias("effective_date"), 
              pl.col("tinh_trang_hieu_luc").alias("status")
    ])


    df = (pl.scan_parquet())
    print("After Merged:", mem(), "MB")
    print("Start load docs")
    for i, row in enumerate(df_merged.iter_rows(named=True)):
        docs.append(
            Document(
                page_content=row["content_html"], 
                metadata = {
                    key: value
                    for key, value in row.items()
                    if key != "content"
                }
            )
        )
        if i % 50000 == 0:
            print(i, mem(), "MB")
    return docs

load_documents()
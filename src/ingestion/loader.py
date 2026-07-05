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

def download_dataset():
    snapshot_download(
        repo_id="th1nhng0/vietnamese-legal-documents",
        repo_type="dataset",
        local_dir=DATA_PATH
    )

def load_documents():
    docs =[]
    print("Before read parquet:", mem(), "MB")
    content_df = pl.read_parquet(DATA_PATH / "data" / "content.parquet")
    metadata_df = pl.read_parquet(DATA_PATH / "data" / "metadata.parquet")
    print("After read parquet:", mem(), "MB")
    #relationships_df = pl.read_parquet(DATA_PATH / "data" / "relationships.parquet")
    meta_small = metadata_df.select(["id", "title",  
                                     pl.col("loai_van_ban").alias("doc_type"), 
                                     pl.col("co_quan_ban_hanh").alias("authority"), 
                                     pl.col("ngay_ban_hanh").alias("issue_date"),
                                     pl.col("ngay_co_hieu_luc").alias("effective_date"), 
                                     pl.col("tinh_trang_hieu_luc").alias("status")
                                     ])
    meta_small = meta_small.with_columns(pl.col("id").cast(pl.Utf8))
    df_merged = content_df.join(meta_small, on="id", how="left")
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
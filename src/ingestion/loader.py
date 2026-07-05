import os
import polars as pl
from pathlib import Path

from langchain_core.documents import Document
from huggingface_hub import snapshot_download

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
    content_df = pl.read_parquet(DATA_PATH / "data" / "content.parquet")
    metadata_df = pl.read_parquet(DATA_PATH / "data" / "metadata.parquet")
    relationships_df = pl.read_parquet(DATA_PATH / "data" / "relationships.parquet")
    meta_small = metadata_df.select(["id", "title",  
                                     pl.col("loai_van_ban").alias("doc_type"), 
                                     pl.col("co_quan_ban_hanh").alias("authority"), 
                                     pl.col("ngay_ban_hanh").alias("issue_date"),
                                     pl.col("ngay_co_hieu_luc").alias("effective_date"), 
                                     pl.col("tinh_trang_hieu_luc").alias("status")
                                     ])
    df_merged = content_df.join(meta_small, on="id", how="left")
    
    for row in df_merged.iter_rows(named=True):
        docs.append(
            Document(
                page_content=row["content"], 
                metadata = {
                    key: value
                    for key, value in row.items()
                    if key != "content"
                }
            )
        )
    
    return docs
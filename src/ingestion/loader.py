import os
import polars as pl
import pyarrow.parquet as pq

from pathlib import Path
from langchain_core.documents import Document
from huggingface_hub import snapshot_download

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

def load_documents(batch_size: int = 10_000):
    metadata_df = (
        pl.read_parquet(METADATA_PATH)
        .with_columns(pl.col("id").cast(pl.Utf8))
    )

    content_pf = pq.ParquetFile(CONTENT_PATH)

    for batch in content_pf.iter_batches(
        batch_size=batch_size,
        columns=["id", "content_html"],
    ):
        content_chunk = (
            pl.from_arrow(batch)
            .with_columns(pl.col("id").cast(pl.Utf8))
        )

        df_merged = (
            content_chunk
            .join(metadata_df, on="id", how="left")
            .select([
                "id",
                "title",
                "content_html",
                pl.col("loai_van_ban").alias("doc_type"),
                pl.col("co_quan_ban_hanh").alias("authority"),
                pl.col("ngay_ban_hanh").alias("issue_date"),
                pl.col("ngay_co_hieu_luc").alias("effective_date"),
                pl.col("tinh_trang_hieu_luc").alias("status"),
            ])
        )

        for row in df_merged.iter_rows(named=True):
            yield Document(
                page_content=row["content_html"],
                metadata={
                    k: v
                    for k, v in row.items()
                    if k != "content_html"
                },
            )
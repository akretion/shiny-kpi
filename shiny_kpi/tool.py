import gettext
import polars as pl 

_ = gettext.gettext


def drop_null_columns_in_df(df: pl.DataFrame) -> pl.DataFrame:
    return df[[s.name for s in df if not (s.null_count() == df.height)]]

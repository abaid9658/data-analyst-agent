"""
Statistics Tool — Descriptive statistics, hypothesis testing, correlation, and outlier detection
"""
import logging
from typing import Any
import numpy as np
import pandas as pd
from scipy import stats
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


class StatisticsTool(BaseTool):
    """
    Tool for statistical calculations: descriptive statistics, hypothesis tests, correlations, outliers.
    """

    name = "statistics"
    description = "Perform statistical summaries, hypothesis tests, correlation analysis, and outlier detection"

    async def execute(self, params: dict[str, Any]) -> dict:
        data = params.get("data")
        stat_type = params.get("stat_type", "summary")
        col_x = params.get("column_x")
        col_y = params.get("column_y")

        df = self._to_dataframe(data)
        if df is None or df.empty:
            return {"success": False, "error": "No data available for statistical analysis"}

        try:
            if stat_type == "summary":
                return self._descriptive_summary(df)
            elif stat_type == "correlation":
                return self._correlation_matrix(df)
            elif stat_type == "hypothesis_test":
                return self._hypothesis_test(df, col_x, col_y)
            elif stat_type == "outliers":
                return self._outlier_detection(df, col_x)
            else:
                return {"success": False, "error": f"Unknown statistics type: {stat_type}"}
        except Exception as e:
            logger.error("Statistics tool execution failed: %s", e)
            return {"success": False, "error": str(e)}

    def _descriptive_summary(self, df: pd.DataFrame) -> dict:
        """Calculate basic descriptive stats for numeric columns."""
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            return {"success": False, "error": "No numeric columns in dataset"}

        summary = {}
        for col in numeric_df.columns:
            summary[col] = {
                "count": int(numeric_df[col].count()),
                "mean": float(numeric_df[col].mean()),
                "std": float(numeric_df[col].std()) if len(numeric_df[col]) > 1 else 0.0,
                "min": float(numeric_df[col].min()),
                "max": float(numeric_df[col].max()),
                "median": float(numeric_df[col].median()),
            }

        return {
            "success": True,
            "stat_type": "summary",
            "results": summary,
            "insights": [f"Processed descriptive statistics for {len(summary)} numeric columns"],
        }

    def _correlation_matrix(self, df: pd.DataFrame) -> dict:
        """Calculate correlation matrix for numeric columns."""
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.shape[1] < 2:
            return {"success": False, "error": "Need at least 2 numeric columns for correlation"}

        corr = numeric_df.corr().to_dict()
        return {
            "success": True,
            "stat_type": "correlation",
            "results": corr,
            "insights": ["Calculated Pearson correlation matrix across numeric columns"],
        }

    def _hypothesis_test(self, df: pd.DataFrame, col_x: str | None, col_y: str | None) -> dict:
        """Perform standard hypothesis testing (t-test / ANOVA)."""
        if not col_x or col_x not in df.columns or not col_y or col_y not in df.columns:
            return {"success": False, "error": "Requires valid columns X and Y"}

        # If X is categorical and Y is numeric -> t-test (2 categories) or ANOVA (multiple categories)
        if pd.api.types.is_numeric_dtype(df[col_y]):
            groups = df[col_x].unique()
            grouped_data = [df[df[col_x] == g][col_y].dropna().values for g in groups]

            if len(groups) == 2:
                stat, p_val = stats.ttest_ind(grouped_data[0], grouped_data[1], equal_var=False)
                test_name = "Independent Two-Sample T-Test"
            else:
                stat, p_val = stats.f_oneway(*grouped_data)
                test_name = "One-Way ANOVA"

            significant = p_val < 0.05
            return {
                "success": True,
                "stat_type": "hypothesis_test",
                "test_name": test_name,
                "statistic": float(stat),
                "p_value": float(p_val),
                "significant": bool(significant),
                "insights": [
                    f"Performed {test_name}. P-value = {p_val:.4f}.",
                    f"The difference is {'statistically significant' if significant else 'not statistically significant'} (alpha = 0.05)."
                ],
            }

        return {"success": False, "error": "Hypothesis testing supports numeric target column Y"}

    def _outlier_detection(self, df: pd.DataFrame, col: str | None) -> dict:
        """Identify outliers using the IQR method."""
        if not col or col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            return {"success": False, "error": "Select a valid numeric column for outlier detection"}

        series = df[col].dropna()
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        return {
            "success": True,
            "stat_type": "outliers",
            "outliers_count": len(outliers),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "insights": [
                f"Identified {len(outliers)} outliers using the IQR rule.",
                f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]."
            ],
        }

    def _to_dataframe(self, data: Any) -> pd.DataFrame | None:
        if data is None:
            return None
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, dict) and "columns" in data and "rows" in data:
            return pd.DataFrame(data["rows"], columns=data["columns"])
        return None

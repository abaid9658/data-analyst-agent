"""
ML Tool — Automated machine learning pipeline
Supports: regression, classification, clustering, time-series forecasting
"""
import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    silhouette_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans

from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


class MLTool(BaseTool):
    """
    Automated ML pipeline — auto-detects problem type, trains, evaluates, explains.
    """

    name = "ml"
    description = "Automated machine learning: regression, classification, clustering, forecasting"

    async def execute(self, params: dict[str, Any]) -> dict:
        data = params.get("data")
        target_col = params.get("target_column")
        problem_type = params.get("problem_type", "auto")
        question = params.get("question", "")

        df = self._to_dataframe(data)
        if df is None or df.empty:
            return {"success": False, "error": "No data available for ML"}

        # Auto-detect problem type
        if problem_type == "auto":
            problem_type = self._detect_problem_type(df, target_col, question)

        logger.info("Running ML pipeline: %s on %d rows", problem_type, len(df))

        try:
            if problem_type == "regression":
                return await self._run_regression(df, target_col)
            elif problem_type == "classification":
                return await self._run_classification(df, target_col)
            elif problem_type == "clustering":
                return await self._run_clustering(df)
            elif problem_type == "forecasting":
                return await self._run_forecasting(df, target_col)
            else:
                return {"success": False, "error": f"Unknown problem type: {problem_type}"}
        except Exception as e:
            logger.error("ML pipeline failed: %s", e)
            return {"success": False, "error": str(e)}

    def _detect_problem_type(
        self, df: pd.DataFrame, target_col: str | None, question: str
    ) -> str:
        """Auto-detect the ML problem type."""
        question_lower = question.lower()

        # Check for explicit forecasting/time-series keywords
        if any(kw in question_lower for kw in ["forecast", "predict next", "future", "trend"]):
            # Check for date column
            date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
            if date_cols:
                return "forecasting"

        # No target → clustering
        if not target_col or target_col not in df.columns:
            return "clustering"

        # Target dtype decides regression vs classification
        target = df[target_col].dropna()
        unique_ratio = target.nunique() / len(target)

        if pd.api.types.is_numeric_dtype(target) and unique_ratio > 0.05:
            return "regression"
        else:
            return "classification"

    async def _run_regression(self, df: pd.DataFrame, target_col: str) -> dict:
        """Run regression pipeline."""
        df_clean = self._clean_dataframe(df)
        X, y, feature_names = self._prepare_features(df_clean, target_col)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Try multiple models, pick best
        models = {
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
            "Linear Regression": LinearRegression(),
        }

        best_model = None
        best_r2 = -float("inf")
        best_name = ""
        results = {}

        for name, model in models.items():
            X_tr = X_train_scaled if name == "Linear Regression" else X_train
            X_te = X_test_scaled if name == "Linear Regression" else X_test
            model.fit(X_tr, y_train)
            preds = model.predict(X_te)
            r2 = r2_score(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)
            results[name] = {"r2": round(r2, 4), "rmse": round(float(rmse), 4), "mae": round(float(mae), 4)}
            if r2 > best_r2:
                best_r2 = r2
                best_model = model
                best_name = name

        # Feature importance
        importance = self._get_feature_importance(best_model, feature_names)

        # Cross-validation
        cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring="r2")

        return {
            "success": True,
            "problem_type": "regression",
            "best_model": best_name,
            "metrics": results[best_name],
            "all_model_results": results,
            "feature_importance": importance,
            "cross_validation": {
                "mean_r2": round(float(cv_scores.mean()), 4),
                "std_r2": round(float(cv_scores.std()), 4),
            },
            "insights": [
                f"Best model: {best_name} with R² = {best_r2:.3f}",
                f"Top feature: {importance[0]['feature'] if importance else 'N/A'}",
            ],
        }

    async def _run_classification(self, df: pd.DataFrame, target_col: str) -> dict:
        """Run classification pipeline."""
        df_clean = self._clean_dataframe(df)
        X, y, feature_names = self._prepare_features(df_clean, target_col, encode_target=True)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        models = {
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        }

        best_model = None
        best_acc = 0
        best_name = ""
        results = {}

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            results[name] = {"accuracy": round(float(acc), 4)}
            if acc > best_acc:
                best_acc = acc
                best_model = model
                best_name = name

        importance = self._get_feature_importance(best_model, feature_names)

        return {
            "success": True,
            "problem_type": "classification",
            "best_model": best_name,
            "metrics": results[best_name],
            "feature_importance": importance,
            "insights": [
                f"Best model: {best_name} with accuracy = {best_acc:.1%}",
                f"Most important feature: {importance[0]['feature'] if importance else 'N/A'}",
            ],
        }

    async def _run_clustering(self, df: pd.DataFrame) -> dict:
        """Run K-Means clustering."""
        df_clean = self._clean_dataframe(df)
        numeric_df = df_clean.select_dtypes(include="number").dropna(axis=1)

        if numeric_df.shape[1] < 2:
            return {"success": False, "error": "Need at least 2 numeric columns for clustering"}

        scaler = StandardScaler()
        X = scaler.fit_transform(numeric_df)

        # Find optimal k using elbow / silhouette
        best_k = 3
        best_silhouette = -1
        for k in range(2, min(8, len(df) // 5 + 1)):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X)
            sil = silhouette_score(X, labels)
            if sil > best_silhouette:
                best_silhouette = sil
                best_k = k

        km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        labels = km.fit_predict(X)

        cluster_sizes = pd.Series(labels).value_counts().sort_index().to_dict()

        return {
            "success": True,
            "problem_type": "clustering",
            "n_clusters": best_k,
            "silhouette_score": round(float(best_silhouette), 4),
            "cluster_sizes": {str(k): int(v) for k, v in cluster_sizes.items()},
            "insights": [
                f"Optimal clusters: {best_k} (silhouette score: {best_silhouette:.3f})",
                f"Largest cluster: {max(cluster_sizes.values())} samples",
                f"Smallest cluster: {min(cluster_sizes.values())} samples",
            ],
        }

    async def _run_forecasting(self, df: pd.DataFrame, target_col: str) -> dict:
        """Run time-series forecasting using Prophet."""
        try:
            from prophet import Prophet

            # Find date column
            date_col = next(
                (c for c in df.columns if "date" in c.lower() or "time" in c.lower()), None
            )
            if not date_col or not target_col:
                return {"success": False, "error": "Need date and target columns for forecasting"}

            prophet_df = df[[date_col, target_col]].rename(
                columns={date_col: "ds", target_col: "y"}
            )
            prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])
            prophet_df = prophet_df.dropna()

            model = Prophet(seasonality_mode="multiplicative")
            model.fit(prophet_df)

            # Forecast 90 days ahead
            future = model.make_future_dataframe(periods=90)
            forecast = model.predict(future)

            future_rows = forecast[forecast["ds"] > prophet_df["ds"].max()].head(12)

            return {
                "success": True,
                "problem_type": "forecasting",
                "forecast": future_rows[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records"),
                "model": "Prophet",
                "insights": [
                    "Forecast generated for next 90 days",
                    f"Predicted next period: {future_rows['yhat'].iloc[0]:.2f}" if len(future_rows) > 0 else "",
                ],
            }
        except ImportError:
            # Fallback to simple linear trend
            return {"success": False, "error": "Prophet not installed — please install prophet"}

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning."""
        df = df.copy()
        # Fill numeric nulls with median
        for col in df.select_dtypes(include="number").columns:
            df[col] = df[col].fillna(df[col].median())
        # Fill categorical nulls with mode
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "unknown")
        # Drop duplicate rows
        df = df.drop_duplicates()
        return df

    def _prepare_features(
        self, df: pd.DataFrame, target_col: str, encode_target: bool = False
    ) -> tuple:
        """Prepare features and target for ML."""
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found")

        feature_cols = [c for c in df.columns if c != target_col]
        X = df[feature_cols].copy()
        y = df[target_col].copy()

        # Encode categoricals
        le = LabelEncoder()
        for col in X.select_dtypes(include="object").columns:
            X[col] = le.fit_transform(X[col].astype(str))

        if encode_target and pd.api.types.is_object_dtype(y):
            y = le.fit_transform(y.astype(str))

        return X.values, np.array(y), list(X.columns)

    def _get_feature_importance(self, model: Any, feature_names: list[str]) -> list[dict]:
        """Extract feature importance from tree models."""
        if not hasattr(model, "feature_importances_"):
            return []
        importances = model.feature_importances_
        pairs = sorted(
            zip(feature_names, importances), key=lambda x: x[1], reverse=True
        )
        return [{"feature": f, "importance": round(float(i), 4)} for f, i in pairs[:10]]

    def _to_dataframe(self, data: Any) -> pd.DataFrame | None:
        if data is None:
            return None
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, dict) and "columns" in data and "rows" in data:
            return pd.DataFrame(data["rows"], columns=data["columns"])
        return None

from __future__ import annotations

import re
from pathlib import Path

import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

FIG_DIR = Path("exported_figures")
FIG_DIR.mkdir(exist_ok=True)

ECON = {
    "red": "#E3120B",
    "navy": "#006BA2",
    "cyan": "#3EBCD2",
    "teal": "#379A8B",
    "gold": "#EBB434",
    "plum": "#B4405B",
    "grey": "#758D99",
    "ink": "#121212",
    "paper": "#FEFAF1",
    "rule": "#B3B3B3",
}

ECON_CYCLE = [ECON[c] for c in ["navy", "red", "cyan", "teal", "gold", "plum", "grey"]]


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "figure.facecolor": ECON["paper"],
            "axes.facecolor": ECON["paper"],
            "savefig.facecolor": ECON["paper"],
            "font.family": "sans-serif",
            "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
            "font.size": 11,
            "axes.edgecolor": ECON["ink"],
            "axes.labelcolor": ECON["ink"],
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": True,
            "axes.grid": True,
            "grid.color": ECON["rule"],
            "grid.linewidth": 0.6,
            "grid.linestyle": "-",
            "xtick.color": ECON["ink"],
            "ytick.color": ECON["ink"],
            "xtick.direction": "out",
            "ytick.direction": "out",
            "axes.prop_cycle": mpl.cycler(color=ECON_CYCLE),
            "legend.frameon": False,
        }
    )


def economist_frame(
    fig,
    title,
    subtitle="",
    source="Source: Scoping review of spatio-temporal infectious-disease models",
    tag="",
    top=0.88,
    left=0.08,
):
    fig.patches.append(
        Rectangle(
            (left, top + 0.08),
            0.022,
            0.022,
            transform=fig.transFigure,
            facecolor=ECON["red"],
            edgecolor="none",
            zorder=5,
        )
    )
    if tag:
        fig.text(
            left + 0.028,
            top + 0.09,
            tag,
            ha="left",
            va="center",
            fontsize=10,
            color=ECON["ink"],
            fontweight="bold",
        )
    fig.text(
        left,
        top + 0.045,
        title,
        ha="left",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=ECON["ink"],
    )
    if subtitle:
        fig.text(
            left,
            top + 0.012,
            subtitle,
            ha="left",
            va="center",
            fontsize=11,
            color=ECON["grey"],
        )
    fig.add_artist(
        Line2D(
            [left, 0.95],
            [top - 0.008, top - 0.008],
            transform=fig.transFigure,
            color=ECON["ink"],
            linewidth=0.8,
        )
    )
    fig.text(left, 0.02, source, ha="left", va="bottom", fontsize=9, color=ECON["grey"], style="italic")


def econ_axes(ax, grid_axis="y"):
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=4, width=0.8, color=ECON["ink"])
    ax.spines["bottom"].set_color(ECON["ink"])
    ax.spines["bottom"].set_linewidth(0.8)
    ax.grid(False)
    if grid_axis in ("x", "y"):
        ax.grid(axis=grid_axis, visible=True, color=ECON["rule"], linewidth=0.6, zorder=1)
    return ax


COUNTRY_PATTERNS = {
    "USA": ["usa", "united states", "u.s.", "us states", "america"],
    "UK": ["united kingdom", "england", "wales", "scotland", "britain", "u.k"],
    "China": ["china", "shenzhen", "shenzen", "guangdong", "guangdon", "shandong", "shandon", "hong kong", "beijing", "shanghai", "wuhan", "hubei"],
    "Italy": ["italy", "milan", "rome", "reggio emilia", "regio emilia"],
    "Spain": ["spain", "madrid", "barcelona", "castilla", "catalonia"],
    "Japan": ["japan", "tokyo"],
    "India": ["india", "mumbai", "delhi", "bangalore", "chennai"],
    "Brazil": ["brazil", "sao paulo", "rio de janeiro"],
    "Germany": ["germany", "berlin", "munich"],
    "France": ["france", "paris"],
    "Iran": ["iran", "tehran"],
    "Turkey": ["turkey", "istanbul"],
    "Portugal": ["portugal", "lisbon"],
    "Sri Lanka": ["sri lanka"],
    "Taiwan": ["taiwan"],
    "Peru": ["peru"],
    "Sierra Leone": ["sierra leone"],
    "Mexico": ["mexico"],
    "Chile": ["chile"],
    "Argentina": ["argentina"],
    "South Korea": ["south korea", "korea"],
    "Australia": ["australia", "sydney", "melbourne"],
    "Canada": ["canada", "toronto", "ontario"],
    "Russia": ["russia", "moscow"],
    "South Africa": ["south africa"],
    "Nigeria": ["nigeria"],
    "Kenya": ["kenya"],
    "Ethiopia": ["ethiopia"],
    "Saudi Arabia": ["saudi arabia"],
    "Pakistan": ["pakistan"],
    "Indonesia": ["indonesia", "jakarta"],
    "Thailand": ["thailand", "bangkok"],
    "Vietnam": ["vietnam"],
    "Philippines": ["philippines"],
    "Singapore": ["singapore"],
    "Malaysia": ["malaysia"],
    "Bangladesh": ["bangladesh", "dhaka"],
    "Netherlands": ["netherlands", "holland"],
    "Belgium": ["belgium"],
    "Switzerland": ["switzerland", "swiss"],
    "Sweden": ["sweden"],
    "Norway": ["norway"],
    "Denmark": ["denmark"],
    "Greece": ["greece"],
    "Egypt": ["egypt"],
    "Colombia": ["colombia"],
    "Ecuador": ["ecuador"],
}


def extract_countries(raw):
    if pd.isna(raw):
        return []
    padded = f" {str(raw).lower()} "
    hits = []
    for country, patterns in COUNTRY_PATTERNS.items():
        if any(p in padded for p in patterns):
            hits.append(country)
    if not hits and ("global" in padded or "multi" in padded or "worldwide" in padded or "west africa" in padded):
        hits.append("Global / multi-region")
    return hits


TIME_RESOLUTION_ORDER = [
    "Daily",
    "Weekly",
    "Biweekly",
    "Monthly",
    "Annual",
    "Mixed / multiple",
    "Other",
    "Not reported",
]

HORIZON_BAND_ORDER = ["1 week or less", "1-4 weeks", "4 weeks+", "Not reported"]

METHOD_FAMILY_ORDER = [
    "GNN",
    "LSTM / GRU / RNN",
    "CNN-based",
    "Transformer / attention",
    "Hybrid / mechanistic",
    "Probabilistic / Bayesian",
    "Classical ML / statistical",
    "Other",
]


def normalize_temporal_resolution(raw):
    if pd.isna(raw):
        return "Not reported"
    text = str(raw).strip().lower()
    if not text or text == "<na>" or "doesn" in text or "didn" in text or "not say" in text:
        return "Not reported"
    hits = set()
    if "day" in text or "daily" in text:
        hits.add("Daily")
    if "biweekly" in text:
        hits.add("Biweekly")
    if "week" in text or "weekly" in text:
        hits.add("Weekly")
    if "month" in text or "monthly" in text:
        hits.add("Monthly")
    if "annual" in text or text == "year":
        hits.add("Annual")
    if len(hits) > 1:
        return "Mixed / multiple"
    if hits:
        return next(iter(hits))
    return "Other"


def _unit_to_days(value, unit):
    factor = {
        "day": 1,
        "days": 1,
        "week": 7,
        "weeks": 7,
        "month": 30,
        "months": 30,
        "year": 365,
        "years": 365,
        "biweekly": 14,
        "biweek": 14,
    }[unit]
    return float(value) * factor


LIST_UNIT_RE = re.compile(r"((?:\d+(?:\.\d+)?\s*,\s*)+\d+(?:\.\d+)?)\s*(day|days|week|weeks|month|months|year|years)")
RANGE_UNIT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(day|days|week|weeks|month|months|year|years|biweekly|biweek)")
SINGLE_UNIT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(day|days|week|weeks|month|months|year|years|biweekly|biweek)")


def parse_horizon_days(raw):
    if pd.isna(raw):
        return np.nan
    text = str(raw).strip().lower().replace("–", "-").replace("—", "-")
    if not text:
        return np.nan
    if any(k in text for k in ["didn't say", "didnt say", "not explicitly reported", "near future"]):
        return np.nan
    if re.search(r"\d+/\d+/\d+", text):
        return np.nan
    if text in {"daily", "1 day", "day"}:
        return 1.0
    if text in {"weekly", "one week", "1 week", "week"}:
        return 7.0
    if text in {"monthly", "1 month", "month"}:
        return 30.0
    if text in {"annual", "year", "1 year"}:
        return 365.0
    if "short term" in text:
        return np.nan
    values = []
    for nums, unit in LIST_UNIT_RE.findall(text):
        for n in re.findall(r"\d+(?:\.\d+)?", nums):
            values.append(_unit_to_days(float(n), unit))
    for _lo, hi, unit in RANGE_UNIT_RE.findall(text):
        values.append(_unit_to_days(float(hi), unit))
    for n, unit in SINGLE_UNIT_RE.findall(text):
        values.append(_unit_to_days(float(n), unit))
    if not values:
        return np.nan
    return max(values)


def horizon_band(days):
    if pd.isna(days):
        return "Not reported"
    if days <= 14:
        return "<=2 weeks"
    if days <= 28:
        return "2-4 weeks"
    return ">4 weeks"


def method_family(raw):
    if pd.isna(raw):
        return "Other"
    text = str(raw).strip().lower()
    if any(k in text for k in ["hybrid", "sir", "seir", "compartment", "mechanistic", "physics informed", "pinn"]):
        return "Hybrid / mechanistic"
    if any(k in text for k in ["graph", "gnn", "gcn", "gat", "mpnn"]):
        return "GNN"
    if any(k in text for k in ["transformer", "attention", "mamba", "state space", "peformer"]):
        return "Transformer / attention"
    if any(k in text for k in ["lstm", "gru", "rnn", "recurrent", "seq2seq", "sequence to sequence"]):
        return "LSTM / GRU / RNN"
    if any(k in text for k in ["cnn", "convolution", "u-net", "encoder-decoder", "resnet"]):
        return "CNN-based"
    if any(k in text for k in ["bayesian", "gaussian process", "probabilistic", "inla"]):
        return "Probabilistic / Bayesian"
    if any(k in text for k in ["random forest", "xgboost", "gradient", "svm", "lasso", "glm", "regression", "arima", "sarima", "naive bayes", "symbolic"]):
        return "Classical ML / statistical"
    return "Other"


def explainability_group(raw):
    if pd.isna(raw):
        return "No explicit explainability"
    text = str(raw).strip().lower()
    if not text or text in {"no", "n"}:
        return "No explicit explainability"
    if text.startswith("yes") or "mechanistic" in text or "shap" in text or "gaussian process" in text:
        return "Claims explainability"
    return "No explicit explainability"


def prepare_time_features(df):
    out = df.copy()
    out["temporal_resolution_group"] = out["Temporal resolution"].apply(normalize_temporal_resolution)
    out["forecast_horizon_days"] = out["Forecast horizon"].apply(parse_horizon_days)
    out["forecast_horizon_band"] = out["forecast_horizon_days"].apply(horizon_band)
    out["method_family"] = out["Method category"].apply(method_family)
    out["explainability_group"] = out["Explainable? (Y/N)"].apply(explainability_group)
    return out


def normalize_disease(raw):
    if pd.isna(raw):
        return "Unspecified"
    text = str(raw).strip()
    low = text.lower()
    if "covid" in low:
        return "COVID-19"
    if low in {"ili", "influenza like illness"}:
        return "ILI"
    if low.startswith("influenza") and "covid" not in low and "," not in low and " and " not in low:
        return "Influenza"
    return text


def code_bucket(series):
    s = series.fillna("").astype(str).str.strip()
    out = []
    url_markers = ("http", "github.com", "doi.org", "drive.google")
    for raw in s:
        v = raw.lower().replace(" ", "")
        if not v:
            out.append("Not reported")
        elif any(m in v for m in url_markers):
            out.append("Y")
        elif "request" in v or "partial" in v:
            out.append("Partial / on request")
        elif v.startswith("notavail") or v.startswith("notavai") or v.startswith("no") or v in ("n", "na"):
            out.append("N")
        elif v.startswith("yes") or v == "y":
            out.append("Y")
        else:
            out.append("Not reported")
    return pd.Series(out)

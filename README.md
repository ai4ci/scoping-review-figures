# Artificial Intelligence (AI) and Machine Learning (ML) for Spatio-temporal Infectious Disease Forecasting: A Scoping Review – Figures

This repository contains the code and figure-generation scripts accompanying the manuscript:

> **Artificial Intelligence (AI) and Machine Learning (ML) for Spatio-temporal Infectious Disease Forecasting: A Scoping Review**
> **Authors:** Amber Palmer, Zixuan Liu, Mengyan Zhang, Rob Challen, Leon Danon

## Overview

This repository provides the scripts used to generate the figures included in our scoping review of artificial intelligence (AI) and machine learning (ML) methods for spatio-temporal infectious disease forecasting.

The review synthesises recent developments in AI/ML forecasting methods, the data used to train them, evaluation practices, uncertainty quantification, interpretability, reproducibility, and fairness considerations across infectious diseases.

## Abstract

### Background

Infectious diseases spread across space and time, yet most artificial intelligence (AI) and machine learning (ML) models treat prediction as a purely temporal problem. Spatio-temporal forecasting is vital for public health decision-making, enabling interventions to be implemented at the optimum time and place. However, to the best of our knowledge, no review has synthesised the AI/ML methods used for this purpose across multiple diseases while examining the data used, model evaluation, uncertainty quantification, interpretability, and fairness.

### Methods

Five databases were searched on **20 November 2025** (Scopus, Web of Science, Compendex, IEEE Xplore, and PubMed). Studies were eligible if they used AI/ML to forecast infectious disease transmission spatio-temporally in humans.

### Findings

A total of **93 studies** published between **2018 and 2026** were included, spanning **14 infectious diseases**. Recurrent neural networks (43 studies; 46%) and graph neural networks (36 studies; 39%) dominated, with hybrid mechanistic–ML models growing steadily after 2022.

Despite methodological convergence, more than **30 distinct error metrics** were used, and no shared benchmark datasets or evaluation methods were adopted, making cross-study comparison of model performance infeasible. Uncertainty was quantified in **18 studies (19%)**, and external validation was performed in **12 studies (13%)**. **Sixty-six studies (71%)** did not share their code openly. There was an under-representation of forecasts in low-income countries. Only one study conducted a fairness analysis, examining whether model performance varied across population groups.

### Interpretation

Increasingly sophisticated models are being developed that remain difficult to compare, trust, or reproduce and have been produced predominantly in middle- and higher-income countries, with near-absent fairness analysis. Three priorities for future research emerge:

1. Adoption of shared benchmarks and evaluation standards.
2. Reporting of uncertainty, validation, and interpretability methods.
3. Extension of methods to under-represented regions, with fairness analysis conducted.

Addressing these gaps is essential for enabling spatio-temporal AI/ML forecasting of infectious diseases to better inform equitable public health policies.


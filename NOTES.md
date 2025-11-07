# Stage 1: Relative Threshold

## Key Concepts

This stage uses a relative amplitude threshold to find the first break. This is a two-pass method:

1.  Find the peak amplitude for the trace.
2.  Find the first sample that exceeds a small percentage of that peak.

## Relevant Sources

> "The challenge is that amplitudes decay over distnace, A trace-by-trace normalization is required before a consistent threshold can be applied."

> "A simple and robust method is to... normalize each trace by its maximum peak-to-trough... A simple threshold can then be applied to this normalized data."
> — (Source: CREWES Research Report)

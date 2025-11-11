# Stage 1: Absolute Threshold

## Key Concepts

The strategy is to go over each tracks and pin the first reading that is over a certin threshold, to be the first pick


# Stage 2: Model-Driven STA/LTA Strategy

## key conecepts

The stategy is to run a "dumb" STA/LTA on all the tracks, which gets the first breaks close to the source currectly,
but fumbels on the distnent ones. and then pick only the good points and fit a model onto them, and then run a small scale STA/LTA (only look at a small window next to the model) and pick the option with the greatest ratio.

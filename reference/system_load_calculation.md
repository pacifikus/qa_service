### Calculate the load on the system.

We will proceed from the following assumptions:
- 36000 queries per month (DAU - 300, average 4 queries per user per day)

Server load: `36000 / (30 * 86400) = 0.013 RPS`

If each server response fits in 2.5MB, then we generate traffic at 0.26 Mbps

Initially, there are **30.000 vectors** in the index of dimension 512 float64 => `30.000 * 512 * 8B = 117.2 MB` are needed for storage

To store **metadata** (question text, link): we need `30.000 * 1KB = 29.3MB`

Expected **embeddings growth**: 1.000 vectors per month = `1.000 * 512 * 8B = 3.9MB`

Expected **metadata growth**: `1.000 * 1KB = 0.97MB`

On the horizon of 1 year, we will need 200MB of space

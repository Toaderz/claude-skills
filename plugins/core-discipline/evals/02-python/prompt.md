This data pipeline drops rows when the upstream API times out. Add retry handling with backoff, and make sure a permanent failure surfaces rather than being swallowed.

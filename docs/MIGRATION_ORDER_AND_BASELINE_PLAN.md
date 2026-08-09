# Migration Order and Baseline Plan

Proposed inspection order is filename order 01 through 08 only; this is not an execution order. Before any application: manual backup, live-schema comparison, approved order, rollback feasibility, and connection verification are mandatory.

Baseline choices for the four existing tables: record them as already-applied baseline in a future tracking table; create explicit no-op baseline records after schema fingerprint approval; or replace with approved versioned migrations. All choices are UNKNOWN until an owner approves them.

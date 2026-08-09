# PostgreSQL Migration Implementation Guide

Use ordered `YYYYMMDDHHMM_description.sql` files. `dry-run` lists files without DB access. `apply` requires explicit approval and a backup reference, then remains blocked pending baseline tracking/schema comparison. App startup never calls the runner.

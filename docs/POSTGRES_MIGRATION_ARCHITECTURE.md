# PostgreSQL Migration Architecture

Future migrations use ordered filenames `YYYYMMDDHHMM_description.sql`, immutable versions, explicit PostgreSQL syntax (identity columns rather than SQLite AUTOINCREMENT), and a tracking table recording version, checksum, applied timestamp, and approved actor. App startup never runs migrations. Baseline registration for four ORM tables requires read-only schema fingerprint approval; drift is recorded, not fixed. Missing prerequisites, FK mismatches, duplicate CREATE, and destructive statements block apply.

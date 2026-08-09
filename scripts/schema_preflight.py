"""Read-only PostgreSQL schema fingerprint; never prints DATABASE_URL."""
import argparse, json, os, sys
parser=argparse.ArgumentParser(); parser.add_argument("--output", required=True); args=parser.parse_args()
if not os.getenv("DATABASE_URL"):
    print("DATABASE_URL is required.", file=sys.stderr); raise SystemExit(1)
import psycopg2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.database import Base

def baseline():
    result={}
    for table in Base.metadata.sorted_tables:
        result[table.name]={"columns": {c.name:{"type":str(c.type).lower(),"nullable":c.nullable} for c in table.columns}, "pk": [c.name for c in table.primary_key.columns], "indexes": sorted(i.name for i in table.indexes)}
    return result

def compare(expected, actual):
    differences=[]
    for name, spec in expected.items():
        found=actual.get(name)
        if not found: differences.append({"table":name,"kind":"missing_table"}); continue
        for col, detail in spec["columns"].items():
            if col not in found["columns"]: differences.append({"table":name,"column":col,"kind":"missing_column"})
            elif found["columns"][col]["nullable"] != detail["nullable"]: differences.append({"table":name,"column":col,"kind":"nullable"})
        if found["pk"] != spec["pk"]: differences.append({"table":name,"kind":"primary_key"})
    return "DRIFT" if differences else "MATCH", differences
try:
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            actual={name:{"columns":{},"pk":[],"indexes":[]} for (name,) in cur.fetchall()}
            cur.execute("SELECT table_name,column_name,is_nullable FROM information_schema.columns WHERE table_schema='public'")
            for table,col,nullable in cur.fetchall():
                if table in actual: actual[table]["columns"][col]={"nullable": nullable == "YES"}
            cur.execute("SELECT tc.table_name,kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu USING (constraint_name,table_schema) WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema='public'")
            for table,col in cur.fetchall():
                if table in actual: actual[table]["pk"].append(col)
    status,differences=compare(baseline(),actual)
    report={"status":status,"differences":differences}
    open(args.output,"w",encoding="utf-8").write(json.dumps(report,default=str))
except Exception:
    print("schema preflight failed", file=sys.stderr); raise SystemExit(1)

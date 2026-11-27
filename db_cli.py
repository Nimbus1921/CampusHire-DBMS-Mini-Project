"""
Interactive SQLite Database Console for CampusHire DBMS Mini-Project.
Allows executing SQL statements directly in the command prompt with formatted output.
"""

import sqlite3
import os
import sys

# Ensure UTF-8 output in Windows PowerShell / CMD
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'college_placement.db')

def print_table(cursor, rows):
    if not rows:
        print("  (0 rows returned)")
        return
    headers = [col[0] for col in cursor.description]
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val) if val is not None else "NULL"))

    # Print Header
    separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    print(separator)
    header_line = "| " + " | ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers)) + " |"
    print(header_line)
    print(separator)

    # Print Rows
    for row in rows:
        row_line = "| " + " | ".join(f"{(str(val) if val is not None else 'NULL'):<{widths[i]}}" for i, val in enumerate(row)) + " |"
        print(row_line)
    print(separator)
    print(f"  ({len(rows)} row(s) returned)\n")

def main():
    print("=" * 70)
    print("  CAMPUSHIRE - DIRECT DATABASE CONSOLE (SQLite 3)")
    print(f"  Database File: {DB_PATH}")
    print("=" * 70)
    print("  Type any SQL query (SELECT, INSERT, UPDATE, DELETE).")
    print("  Type 'tables' to list all tables. Type 'exit' or 'quit' to close.")
    print("=" * 70 + "\n")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    buffer = []
    while True:
        try:
            prompt = "SQL> " if not buffer else " ...> "
            line = input(prompt)
            stripped = line.strip()

            if not buffer:
                if not stripped:
                    continue
                if stripped.lower() in ('exit', 'quit', 'q'):
                    print("Exiting database console. Goodbye!")
                    break
                if stripped.lower() == 'tables':
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
                    tables = [r[0] for r in cur.fetchall()]
                    print("\nTables in Database:")
                    for t in tables:
                        print(f"  • {t}")
                    print()
                    continue
                if stripped.lower() == 'clear':
                    buffer = []
                    continue

            buffer.append(line)

            # Check if query ends with a semicolon
            full_query = " ".join(buffer).strip()
            if not full_query.endswith(";"):
                continue

            # Complete query encountered
            buffer = []
            cur.execute(full_query)
            if full_query.strip().upper().startswith(("SELECT", "PRAGMA", "EXPLAIN", "WITH")):
                rows = cur.fetchall()
                print_table(cur, rows)
            else:
                conn.commit()
                print(f"  Query executed successfully. ({cur.rowcount} row(s) affected)\n")

        except KeyboardInterrupt:
            if buffer:
                print("\n  (Query buffer cleared)")
                buffer = []
            else:
                print("\nExiting database console.")
                break
        except Exception as e:
            buffer = []
            print(f"  SQL Error: {str(e)}\n")

    conn.close()

if __name__ == '__main__':
    main()

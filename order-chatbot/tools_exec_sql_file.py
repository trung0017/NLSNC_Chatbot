import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


def exec_sql_file(cursor, file_path: Path) -> None:
	# Read and execute semicolon-separated statements, with naive string handling
	sql = file_path.read_text(encoding="utf-8")
	statements = []
	buff = []
	in_string = False
	quote = ""
	for ch in sql:
		if ch in ('"', "'"):
			if not in_string:
				in_string = True
				quote = ch
			elif quote == ch:
				in_string = False
		if ch == ";" and not in_string:
			stmt = "".join(buff).strip()
			if stmt and not stmt.startswith("--") and not stmt.startswith("/*"):
				statements.append(stmt)
			buff = []
		else:
			buff.append(ch)
	tail = "".join(buff).strip()
	if tail and not tail.startswith("--") and not tail.startswith("/*"):
		statements.append(tail)

	for stmt in statements:
		cursor.execute(stmt)


def main() -> None:
	if len(sys.argv) != 2:
		print("Usage: tools_exec_sql_file.py PATH_TO_SQL", file=sys.stderr)
		sys.exit(1)
	sql_path = Path(sys.argv[1]).resolve()
	if not sql_path.exists():
		print(f"ERROR: SQL file not found: {sql_path}", file=sys.stderr)
		sys.exit(1)

	root = Path(__file__).resolve().parent
	load_dotenv(root / ".env")

	cfg = dict(
		host=os.getenv("DB_HOST", "localhost"),
		port=int(os.getenv("DB_PORT", "3306") or "3306"),
		user=os.getenv("DB_USER", "root"),
		password=os.getenv("DB_PASSWORD", ""),
		database=os.getenv("DB_NAME", "chatbot_db"),
	)

	conn = mysql.connector.connect(**cfg)
	cur = conn.cursor()

	exec_sql_file(cur, sql_path)
	conn.commit()
	cur.close()
	conn.close()

	print(f"OK: Executed {sql_path}")


if __name__ == "__main__":
	main()


import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


def get_env(key: str, default: str = "") -> str:
	# Prefer DB_* variables; fall back to MYSQL_*; then default
	value = os.getenv(key)
	if value is not None and value != "":
		return value
	legacy_key = key.replace("DB_", "MYSQL_", 1) if key.startswith("DB_") else key
	value = os.getenv(legacy_key)
	if value is not None and value != "":
		return value
	return default


def exec_sql_file(cursor, file_path: Path) -> None:
	# Execute SQL statements separated by semicolons, while being robust with strings/comments
	sql = file_path.read_text(encoding="utf-8")
	statements = []
	buffer = []
	in_string = False
	string_quote = ""
	i = 0
	while i < len(sql):
		ch = sql[i]
		if ch in ('"', "'"):
			if not in_string:
				in_string = True
				string_quote = ch
			elif string_quote == ch:
				in_string = False
		if ch == ";" and not in_string:
			stmt = "".join(buffer).strip()
			if stmt and not stmt.startswith("--") and not stmt.startswith("/*"):
				statements.append(stmt)
			buffer = []
		else:
			buffer.append(ch)
		i += 1
	tail = "".join(buffer).strip()
	if tail and not tail.startswith("--") and not tail.startswith("/*"):
		statements.append(tail)

	for stmt in statements:
		try:
			cursor.execute(stmt)
		except Exception as exc:
			# Continue on idempotent DDL errors (e.g., database/table exists)
			errmsg = str(exc).lower()
			if any(x in errmsg for x in ["exists", "duplicate", "already", "warning"]):
				continue
			raise


def main() -> None:
	root = Path(__file__).resolve().parent
	# Load environment variables from .env in project root
	load_dotenv(dotenv_path=root / ".env")
	db_host = get_env("DB_HOST", "localhost")
	db_port = int(get_env("DB_PORT", "3306") or "3306")
	db_user = get_env("DB_USER", "root")
	db_password = get_env("DB_PASSWORD", "12345678")
	db_name = get_env("DB_NAME", "chatbot_db")

	# Connect without database to create it if missing
	conn = mysql.connector.connect(host=db_host, port=db_port, user=db_user, password=db_password)
	conn.autocommit = True
	cur = conn.cursor()
	cur.execute(
		f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
		"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
	)
	cur.close()
	conn.close()

	# Import schema and sample data
	conn = mysql.connector.connect(
		host=db_host, port=db_port, user=db_user, password=db_password, database=db_name
	)
	cur = conn.cursor()

	schema_path = root / "database" / "schema.sql"
	sample_path = root / "database" / "sample_data.sql"

	if not schema_path.exists():
		print(f"ERROR: schema file not found at {schema_path}", file=sys.stderr)
		sys.exit(1)

	exec_sql_file(cur, schema_path)

	if sample_path.exists():
		exec_sql_file(cur, sample_path)

	conn.commit()
	cur.close()
	conn.close()

	print(f"OK: Imported schema and sample data into database '{db_name}'")


if __name__ == "__main__":
	main()


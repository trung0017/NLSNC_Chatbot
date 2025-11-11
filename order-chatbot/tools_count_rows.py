import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


def main() -> None:
	# Load .env next to this script
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

	tables = ["products", "categories", "promotions", "faqs", "training_data", "chat_history"]

	results = {}
	for t in tables:
		try:
			cur.execute(f"SELECT COUNT(*) FROM {t}")
			(count,) = cur.fetchone()
			results[t] = count
		except Exception as ex:
			results[t] = f"ERR: {ex}"

	cur.close()
	conn.close()

	for k, v in results.items():
		print(f"{k}: {v}")


if __name__ == "__main__":
	main()


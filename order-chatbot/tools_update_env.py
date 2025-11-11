import sys
from pathlib import Path


def upsert_env_line(env_path: Path, key: str, value: str) -> None:
	lines = []
	if env_path.exists():
		# Preserve existing file and line endings
		text = env_path.read_text(encoding="utf-8")
		# Keep original newline style
		nl = "\r\n" if "\r\n" in text else "\n"
		lines = text.splitlines()
	else:
		nl = "\n"

	found_idx = None
	for i, line in enumerate(lines):
		strip = line.strip()
		if not strip or strip.startswith("#"):
			continue
		if strip.split("=", 1)[0] == key:
			found_idx = i
			break

	entry = f"{key}={value}"
	if found_idx is not None:
		lines[found_idx] = entry
	else:
		lines.append(entry)

	env_path.write_text(nl.join(lines) + ("" if lines and lines[-1] == "" else nl), encoding="utf-8")


def main() -> None:
	if len(sys.argv) != 3:
		print("Usage: tools_update_env.py KEY VALUE", file=sys.stderr)
		sys.exit(1)
	key, value = sys.argv[1], sys.argv[2]
	env_path = Path(__file__).resolve().parent / ".env"
	upsert_env_line(env_path, key, value)
	print(f"Updated {key} in {env_path}")


if __name__ == "__main__":
	main()


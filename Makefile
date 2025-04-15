format:
	uv run -- ruff check --select I --fix
	uv run -- ruff format
	uv run -- taplo fmt

lint:
	uv run -- pyright .
	uv run -- mypy .
	uv run -- ruff check
	uv run -- ruff format --check

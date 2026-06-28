# Code Review Checklist

Follow this checklist after generating or modifying code. Run automated checks, then perform manual reviews.

Automated checks (run locally / in CI):

```bash
# format
black .
# lint
ruff check .
# type-check
mypy --strict
# tests
pytest -q
```

Manual review items:
- Verify no missing imports or unused imports.
- Check for circular imports and long import chains.
- Ensure functions and methods have type hints and docstrings.
- Confirm exception handling is explicit and mapped at API boundaries.
- Confirm no secrets or credentials are hardcoded.
- Validate new endpoints against API contract in `docs/`.
- Check performance-sensitive code (retrieval, embeddings) for batching and caching.
- Verify explainability outputs include provenance and are deterministic where possible.

If any item fails, fix and re-run automated checks before merging.

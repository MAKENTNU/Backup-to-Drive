lint: ## Runs pre-commit hooks against all files. Provide the `hook` arg to only run that specific hook.
	pre-commit run $(hook) --all-files

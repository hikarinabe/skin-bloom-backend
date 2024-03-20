ENV_NAME=venv

run:
	firebase emulators:start

FUN = cosmetic_info
prod-run:
	functions-framework --target ${FUN} --debug

setup:
	@echo NOTE: run this commend in your tarminal
	@echo python3.12 -m venv $(ENV_NAME) && source $(ENV_NAME)/bin/activate

deactivate:
	deactivate

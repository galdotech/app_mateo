.PHONY: ui doctor

ui:
	bash tools/compile_ui.sh

doctor:
	python tools/doctor.py

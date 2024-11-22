
PYUIC=pyuic5
PFLAGS=

all: ui/Article_design.py ui/DialogExportText_design.py ui/DialogTopCoauthors_design.py ui/EditReferenceFormat_design.py ui/MainWindow_design.py ui/Settings_design.py

ui/%_design.py: ui/%.ui
	$(PYUIC) $(PFLAGS) $< -o $@

clean:
	rm ui/*.py

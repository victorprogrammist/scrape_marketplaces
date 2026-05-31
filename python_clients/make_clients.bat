
rem python -m pip install pyinstaller
 
pyinstaller --clean --onefile --noconsole --distpath . scrape_ozon_gui.py

pyinstaller --clean --onefile --distpath . scrape_ozon_cli.py


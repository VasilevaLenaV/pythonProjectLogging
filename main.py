# Создать телефонный справочник с возможностью импорта и экспорта данных в нескольких форматах.
import view as ui
import logger as log

global logger
logger = log.init(__name__)

logger.info("start program")
ui.ls_menu()

logger.info("end program")
print("End")

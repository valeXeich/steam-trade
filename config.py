from pathlib import Path

if 'dist' in __file__:
    PATH_TO_DB = f"{Path(__file__).parent}/db/sta.db"
    PATH_TO_STYLES = f"{Path(__file__).parent}/ui/styles/"
    PATH_TO_ASSETS = f"{Path(__file__).parent}/ui/assets/"
    
    PATH_TO_GET_JSON_BUTTON_STYLES = f"{PATH_TO_STYLES}GetJSONButton.qss"
    PATH_TO_GUARD_BUTTON_STYLES = f"{PATH_TO_STYLES}GuardButton.qss"
    PATH_TO_SETTINGS_BUTTON_STYLES = f"{PATH_TO_STYLES}SettingsButton.qss"
else:
    PATH_TO_DB = f"{Path(__file__).parent}/core/db/sta.db"
    PATH_TO_STYLES = f"{Path(__file__).parent}/ui/styles/"
    PATH_TO_ASSETS = f"{Path(__file__).parent}/ui/assets/"
    
    PATH_TO_COMPONENTS_BUTTONS = f"{Path(__file__).parent}/ui/components/buttons/"
    PATH_TO_GET_JSON_BUTTON_STYLES = f"{PATH_TO_COMPONENTS_BUTTONS}GetJSONButton/GetJSONButton.qss"
    PATH_TO_GUARD_BUTTON_STYLES = f"{PATH_TO_COMPONENTS_BUTTONS}GuardButton/GuardButton.qss"
    PATH_TO_SETTINGS_BUTTON_STYLES = f"{PATH_TO_COMPONENTS_BUTTONS}SettingsButton/SettingsButton.qss"


PATH_TO_MAIN_STYLES = f"{PATH_TO_STYLES}main.qss"
PATH_TO_MODALS_STYLES = f"{PATH_TO_STYLES}modals.qss"
PATH_TO_SIDEBAR_STYLES = f"{PATH_TO_STYLES}sidebar.qss"
PATH_TO_TABLE_PAGE_STYLES = f"{PATH_TO_STYLES}table-page.qss"
PATH_TO_LOG_PAGE_STYLES = f"{PATH_TO_STYLES}log-page.qss"

PATH_TO_GET_JSON_BUTTON_IMAGE = f"{PATH_TO_ASSETS}get_json.png"
PATH_TO_GUARD_ADD_BUTTON_IMAGE = f"{PATH_TO_ASSETS}guard_add.png"
PATH_TO_GUARD_REMOVE_BUTTON_IMAGE = f"{PATH_TO_ASSETS}guard_remove.png"
PATH_TO_SETTINGS_BUTTON_IMAGE = f"{PATH_TO_ASSETS}settings.png"

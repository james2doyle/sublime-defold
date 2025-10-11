import logging
import subprocess
import threading
import urllib.request
from typing import Any, Dict, Union

import sublime
import sublime_plugin

# --- Configuration ---
# Command to execute to find the Defold Editor's listening port.
# @see https://forum.defold.com/t/defold-android-development-app-required-ports/72433/2
PORT_DISCOVERY_COMMAND = (
    # known working version on OSX
    "ps -A | awk '/[c]om.defold.editor/ { print $1 }' | xargs lsof -p | grep LISTEN | grep -Eo ':\\d+' | cut -f2 -d:"
    # Linux? `lsof -p $(pgrep -f "com.defold.editor") -i -P -n | grep LISTEN | grep -Eo ':\\d+' | cut -f2 -d:`
    # windows?
    # $processId = (Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*com.defold.editor*'} | Select-Object -ExpandProperty ProcessId)
    # if ($processId) {
    #     Get-NetTCPConnection | Where-Object {$_.State -eq 'Listen' -and $_.OwningProcess -eq $processId} | Select-Object -ExpandProperty LocalPort
    # } else {
    #     Write-Host "Process 'com.defold.editor' not found."
    # }
)

# @see https://github.com/defold/defold/blob/dev/editor/doc/http-api.md#the-command-endpoint
HOT_RELOAD_PATH = "/command/hot-reload"
PROJECT_SETTING_KEY = "defold_hot_reload"

logger = logging.getLogger("DefoldPlugin")


# --- Helper Function for Asynchronous Hot-Reload ---
def run_hot_reload():
    """
    Discovers the Defold Editor port using a shell command and sends the
    hot-reload command via an HTTP POST request.
    (Implementation remains the same as previous version)
    """

    # 1. Discover the Editor Port using the shell command
    try:
        # Run the discovery command and capture its output
        port_process = subprocess.run(
            PORT_DISCOVERY_COMMAND,
            shell=True,
            check=True,  # Raise an exception for non-zero exit codes
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
        )
        editor_port = port_process.stdout.strip()

        if not editor_port or not editor_port.isdigit():
            raise ValueError("Could not find a valid port. Output: '{}'".format(editor_port))

        # 2. Construct the full URL
        url = "http://localhost:{}".format(editor_port) + HOT_RELOAD_PATH

        # 3. Execute the equivalent of: curl -X POST "localhost:${EDITOR_PORT}/command/hot-reload"
        # The data is set to an empty byte string for a simple POST request.
        data_bytes = b""
        request = urllib.request.Request(url, data=data_bytes, method="POST")

        # Open the URL with a timeout
        response: Dict[str, Any] = urllib.request.urlopen(request, timeout=5)

        # Log success message to the Sublime Text console
        msg: str = "Defold Hot Reload: Reloaded!"
        sublime.status_message(msg)
        logger.debug("Defold Hot Reload: Success! URL: {} (Status: {})".format(url, response.status))

    except subprocess.CalledProcessError as e:
        # Handle cases where the shell command fails (e.g., process not running)
        msg: str = "Defold Hot Reload: ERROR running discovery command (Code {}): {}".format(
            e.returncode, e.stderr.strip()
        )
        sublime.status_message(msg)
        raise ValueError(msg)

    except Exception as e:
        # Handle network or port-finding errors
        msg: str = "Defold Hot Reload: ERROR during reload. Is the Defold Editor running? Details: {}".format(str(e))
        sublime.status_message(msg)
        raise ValueError(msg)


# --- Sublime Text Event Listener with Project Setting Check ---
class DefoldHotReloadOnSaveListener(sublime_plugin.EventListener):
    """
    Listens for the post-save event and checks project settings before running hot-reload.
    """

    def on_post_save_async(self, view: sublime.View):
        """
        Called after a view has been saved. Checks project settings before initiating the command.
        """

        window: Union[sublime.Window, None] = view.window()
        if not window:
            msg: str = "Defold Hot Reload: No window found."
            sublime.status_message(msg)
            raise ValueError(msg)

        # 1. Get the Project Data (which contains the 'settings' block)
        # We need a window to access project data.
        project_data = window.project_data()

        # 2. Check the setting in the 'settings' block of the project file.
        # We use .get(key, {}) to safely access the settings block, and then
        # .get(key, False) to default the setting value to False if not present.
        should_run: bool = project_data.get("settings", {}).get(PROJECT_SETTING_KEY, False)

        # 3. Proceed only if the setting is explicitly True AND a file name exists
        if view.file_name() and should_run is True:
            # Start a new, non-blocking thread for the work
            thread = threading.Thread(target=run_hot_reload)
            thread.start()

        elif view.file_name():
            # Optional: Log if the feature is disabled, which is useful for debugging.
            # print('Defold Hot Reload: Project setting "{}" is not set or is False. Skipping.'.format(PROJECT_SETTING_KEY))
            pass


class DefoldReloadCommand(sublime_plugin.TextCommand):
    """
    A Sublime Text command to manually trigger a Defold hot-reload.
    It runs the same logic as the on-save listener, checking project settings
    before initiating the hot-reload.
    """

    def run(self, edit: sublime.Edit):
        view = self.view

        # Proceed only if the setting is explicitly True AND a file name exists in the current view.
        # This replicates the exact conditions from the on-save listener.
        if view.file_name():
            # Start a new, non-blocking thread for the hot-reload work,
            # just like the on-save listener does.
            thread = threading.Thread(target=run_hot_reload)
            thread.start()
        # If the conditions are not met (e.g., setting is False or no file is open),
        # the command will silently do nothing, mirroring the behavior of the on-save listener.

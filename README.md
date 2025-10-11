Sublime Defold
==============

Sublime Defold is a powerful Sublime Text plugin that helps you develop Defold games with Sublime Text.

### Install

You must have [astrochili/defold-annotations](https://github.com/astrochili/defold-annotations) setup in your Defold project if you want the types in the snippets to work correctly.

```sh
# change to the directory found with "Preference: Browse Packages", then clone
git clone https://github.com/james2doyle/sublime-defold.git Defold
```

### Features

**Hot Reload**: Reload on save or you can run the "Defold: Reload" command
**Snippets and Completions**: Helpful code completion for common commands and patterns

### Installation

#### Via Package Control (Recommended)

1. Open Sublime Text.
1. Go to Tools > Command Palette... (or press Ctrl+Shift+P / Cmd+Shift+P).
1. Type Package Control: Install Package and press Enter.
1. Search for Sublime Gemini and press Enter to install.

#### Manual Installation

1. Navigate to your Sublime Text Packages directory. You can find this by going to Preferences > Browse Packages... in Sublime Text.
1. Run `git clone https://github.com/james2doyle/sublime-defold Defold` in that folder

#### Project Configuration

You can configure the `defold_hot_reload` on the project level.

In your `.sublime-project` file:

```jsonc
{
    // ... folders array with paths, etc.
    "settings": {
        "defold_hot_reload": true
        // ... the rest of your settings
    }
}
```

The plugin will check your `.sublime-project` so the project settings before trying to send a hot reload to the editor.

### Usage

TODO

#### Command Palette

1. Open Tools > Command Palette... (Ctrl+Shift+P / Cmd+Shift+P).
1. Type Gemini to see available commands:
  - Defold: Reload: Reload the running build.

#### Key Bindings

You can set up custom key bindings for frequently used commands. Go to Preferences > Key Bindings and add entries like this:

```jsonc
[
    { "keys": ["ctrl+alt+g", "ctrl+alt+c"], "command": "defold_reload" }
]
```

### Development

#### Project Structure

- `defold-reload-on-save.py`: Main plugin entry point and core logic for sending hot reload commands.
- `AGENTS.md`: Helper for AI coding tools.
- `pyproject.toml`: Project configuration for dependency management and build tools.
- `snippets/`: Folder with all the Sublime snippets.

local wezterm = require("wezterm")

local config = wezterm.config_builder()

config.enable_scroll_bar = false
config.font = wezterm.font("CaskaydiaCove Nerd Font Mono", { weight = "Light", assume_emoji_presentation = true })
config.line_height = 1.2
config.font_size = 14.0
config.enable_tab_bar = false
config.window_decorations = "RESIZE"
config.window_padding = {
	left = 0,
	right = 0,
	top = 0,
	bottom = 0,
}

wezterm.on("toggle-opacity", function(window)
	local overrides = window:get_config_overrides() or {}
	if not overrides.window_background_opacity then
		overrides.window_background_opacity = 0.8
	else
		overrides.window_background_opacity = nil
	end
	window:set_config_overrides(overrides)
end)

config.keys = {
	{
		key = "Enter",
		mods = "CMD",
		action = wezterm.action.ToggleFullScreen,
	},
	{
		key = "u",
		mods = "CMD",
		action = wezterm.action.EmitEvent("toggle-opacity"),
	},
}

return config

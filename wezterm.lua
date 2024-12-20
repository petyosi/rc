local wezterm = require("wezterm")

local config = wezterm.config_builder()

config.enable_scroll_bar = false
config.font = wezterm.font_with_fallback({
	"JetBrainsMono Nerd Font Propo",
	"Apple Color Emoji",
})

config.line_height = 1.2
config.font_size = 14.0
config.freetype_load_target = "Light"
-- config.freetype_load_target = "Mono"
config.enable_tab_bar = false
config.color_scheme = "Monokai Remastered"
-- config.color_scheme = "3024 Day (Gogh)"
config.window_decorations = "RESIZE"
config.window_padding = {
	left = 0,
	right = 0,
	top = 0,
	bottom = 0,
}
config.max_fps = 240
config.animation_fps = 60

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
	{
		key = "6",
		mods = "SHIFT",
		action = wezterm.action.DisableDefaultAssignment,
	},
	{
		key = "s",
		mods = "CMD",
		action = wezterm.action.SendKey({ key = "s", mods = "CTRL" }),
	},
	{
		key = "w",
		mods = "CMD",
		action = wezterm.action.SendKey({ key = "d", mods = "ALT" }),
	},
}

return config

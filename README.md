# spotify-status

## Dependencies

- [tekore](https://pypi.org/project/tekore)

## Module

```ini
[module/spotify]
type = custom/script
exec = ~/.config/polybar/spotify-status/main.py track

[module/spotify-back]
type = custom/script
exec = ~/.config/polybar/spotify-status/main.py previous_dry
click-left = ~/.config/polybar/spotify-status/main.py previous

[module/spotify-playpause]
type = custom/script
exec = ~/.config/polybar/spotify-status/main.py playpause_dry
click-left = ~/.config/polybar/spotify-status/main.py playpause

[module/spotify-next]
type = custom/script
exec = ~/.config/polybar/spotify-status/main.py next_dry
click-left = ~/.config/polybar/spotify-status/main.py next
```


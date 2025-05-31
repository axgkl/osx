# OSX Automnation

yabai feeds the fifo via:

```
PY=/Users/gk/uv/osx/.venv/bin/python3
# for mode in win spc; do
for mode in spc; do
    fifo="/tmp/yabai-$mode.fifo"
    rm -f "$fifo" && mkfifo "$fifo"
    if [ $mode = win ]; then
        yabai -m signal --add event=window_focused action='echo "window_focused $YABAI_WINDOW_ID" > '$fifo''
        #         yabai -m signal --add event=window_destroyed action='echo "window_destroyed $YABAI_WINDOW_ID" > '$fifo''
        #         #yabai -m signal --add app='^Ghostty$' event=window_created action='echo "ghostty_created $YABAI_WINDOW_ID" > '$fifo''
    else
        yabai -m signal --add event=space_changed action='echo "space_changed $YABAI_SPACE_ID $YABAI_SPACE_INDEX" > '$fifo''
    fi
    $PY /Users/gk/uv/osx/yabairc "$fifo" &
done
```


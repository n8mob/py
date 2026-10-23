import beep
import oled_ui


display = oled_ui.OledUI()

m = beep.Morser(dit=0.1, callback=lambda morser: display.update(morser))

m.blink_and_beep()

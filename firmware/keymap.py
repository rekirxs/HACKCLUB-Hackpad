import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

# Optional OLED support — KMK has several different OLED extensions
# If your KMK build provides `kmk.extensions.oled` use that; otherwise
# adapt the display initialization below to use your display driver.
try:
    from kmk.extensions.oled import OLED
    oled_available = True
except Exception:
    OLED = None
    oled_available = False

# Initialize the Keyboard
keyboard = KMKKeyboard()

# --- HARDWARE CONFIGURATION ---

# 1. SWITCH MATRIX
# Update these pins to match your KiCad Routing!
keyboard.col_pins = (board.D2, board.D3, board.D4, board.D5)  # Columns
keyboard.row_pins = (board.D0, board.D1)                      # Rows
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# 2. ROTARY ENCODER
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
# Pin A = D9, Pin B = D10 (Check your schematic!)
encoder_handler.pins = ((board.D9, board.D10, None, False),)

# 3. RGB LEDS (Underglow)
# If your KMK build includes an RGB extension, configure it here.
# Example omitted for brevity — keep your existing RGB configuration if needed.

# 4. MODULES
keyboard.modules.append(Layers())
media = MediaKeys()
keyboard.extensions.append(media)

# Simple state used for OLED display
_display_state = {
    "layer": 0,
    "last_action": "",
    "volume": 50,  # a tracked volume value (0-100)
}

# --- OLED SETUP (optional) ---
if oled_available:
    # Default init — adapt params for your specific OLED (width/height, i2c pins)
    oled = OLED()
    keyboard.extensions.append(oled)

    def _update_oled():
        # The OLED extension API varies between KMK versions. Some provide
        # `oled.display_text(...)`, `oled.paint_text(...)` or `oled.display`.
        # We attempt a few common methods and fall back to no-op if none work.
        if not oled_available:
            return
        lines = [
            f"Layer: {_display_state['layer']}",
            f"Vol: {_display_state['volume']}%",
            f"{_display_state['last_action'][:16]}",
        ]
        try:
            # KMK OLED common helper
            oled.display_text('\n'.join(lines))
            return
        except Exception:
            pass
        try:
            # Alternative API
            oled.paint_text('\n'.join(lines))
            return
        except Exception:
            pass
        try:
            # Very low-level: expose framebuffer or buffer write
            oled.show('\n'.join(lines))
            return
        except Exception:
            pass

else:
    def _update_oled():
        # No OLED available — become a no-op.
        return

# --- KEYMAPS ---

# Define special keys
L1_KEY = KC.MO(1)

# Layer 0: Normal Shortcuts
# Layer 1: Media Control
keyboard.keymap = [
    # LAYER 0 (Default)
    [
        KC.A,    KC.B,     KC.C,     KC.D,
        KC.E,    KC.F,     KC.G,     L1_KEY,
    ],
    # LAYER 1 (Media / navigation)
    [
        KC.N1,   KC.N2,    KC.N3,    KC.N4,
        KC.MUTE, KC.VOLU,  KC.VOLD,  KC.TRNS,
    ],
]

# --- ENCODER MAP ---
# We will map the encoder to call a small helper so we can both send media
# key events and update the OLED `volume` tracking variable.

def _encoder_volume_up():
    # Send the media key for volume up and update display state.
    try:
        media.volume_up()
    except Exception:
        # If MediaKeys doesn't expose a helper, attempt a generic consumer send
        try:
            keyboard.consumer_control.send(media.codes.VOLUME_INCREMENT)
        except Exception:
            pass
    _display_state['volume'] = min(100, _display_state['volume'] + 2)
    _display_state['last_action'] = 'Vol +'
    _update_oled()


def _encoder_volume_down():
    try:
        media.volume_down()
    except Exception:
        try:
            keyboard.consumer_control.send(media.codes.VOLUME_DECREMENT)
        except Exception:
            pass
    _display_state['volume'] = max(0, _display_state['volume'] - 2)
    _display_state['last_action'] = 'Vol -'
    _update_oled()


def _encoder_press():
    # Toggle mute
    try:
        media.mute()
    except Exception:
        try:
            keyboard.consumer_control.send(media.codes.MUTE)
        except Exception:
            pass
    _display_state['last_action'] = 'Mute'
    _update_oled()

# Wire the encoder handler to call our helpers. Many KMK builds will accept
# tuples with callables in `encoder_handler.map`. If your KMK version does not,
# adapt these lines to your encoder API.
encoder_handler.map = [
    # Layer 0 behavior: (rotate cw, rotate ccw, press)
    ((_encoder_volume_up, _encoder_volume_down, _encoder_press),),
    # Layer 1 behavior
    ((KC.UP, KC.DOWN, KC.ENT),),
]

# Update display initially
_update_oled()

if __name__ == '__main__':
    keyboard.go()

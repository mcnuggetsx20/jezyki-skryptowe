# cheesecake.tcl

namespace eval ::ttk::theme::cheesecake {
    ttk::style theme create cheesecake -parent default -settings {
        # Kolory bazowe
        set bgColor "#fdf1d6"
        set fgColor "#e72ca9"
        set correctColor "#94e089"
        set errorColor "#ff7f7f"

        # Ogólne tło
        ttk::style configure . -background $bgColor -foreground $fgColor -font "Courier 12"

        # Przycisk
        ttk::style configure TButton -background $bgColor -foreground $fgColor -padding 5 -relief flat

        # Label
        ttk::style configure TLabel -background $bgColor -foreground $fgColor

        # Entry
        ttk::style configure TEntry -fieldbackground $bgColor -foreground $fgColor -insertcolor $fgColor -borderwidth 1

        # Frame
        ttk::style configure TFrame -background $bgColor
    }
}

# Funkcja do ustawienia motywu
proc set_theme {theme_name} {
    if {$theme_name eq "cheesecake"} {
        ttk::style theme use cheesecake
    }
}

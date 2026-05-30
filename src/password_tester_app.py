import threading
import customtkinter as ctk
from password_checker import check_password, check_hibp, get_strength
from password_generator import generate_password
from password_strength import PasswordStrength

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

STRENGTH_CONFIG = {
    PasswordStrength.WEAK:        {"label": "Weak",        "color": "#E03E3E", "progress": 0.25},
    PasswordStrength.FAIR:        {"label": "Fair",        "color": "#E08C00", "progress": 0.50},
    PasswordStrength.STRONG:      {"label": "Strong",      "color": "#7ABF00", "progress": 0.75},
    PasswordStrength.VERY_STRONG: {"label": "Very Strong", "color": "#00C864", "progress": 1.00},
}

TIPS_TEXT = (
    "• At least 8 characters long\n"
    "• Not a repeated or generic password\n"
    "• At least one uppercase letter (A–Z)\n"
    "• At least one lowercase letter (a–z)\n"
    "• At least one digit (0–9)\n"
    "• At least one special character: !@#$%^&*()"
)


class PasswordTesterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Tester")
        self.geometry("480x580")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # --- Tab view ---
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabs.add("Test")
        self.tabs.add("Generate")

        self._build_test_tab(self.tabs.tab("Test"))
        self._build_generate_tab(self.tabs.tab("Generate"))

    # ------------------------------------------------------------------ #
    #  TEST TAB                                                            #
    # ------------------------------------------------------------------ #
    def _build_test_tab(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Title row
        title_row = ctk.CTkFrame(frame, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            title_row,
            text="Test a Password",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        ).pack(side="left")

        # Theme toggle
        self.theme_button = ctk.CTkButton(
            title_row,
            text="☀ Light Mode",
            width=110,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            command=self._toggle_theme
        )
        self.theme_button.pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            title_row,
            text="Show Tips",
            width=100,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self._show_tips
        ).pack(side="right")

        # Password entry
        ctk.CTkLabel(
            frame,
            text="Enter your password",
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(fill="x", pady=(0, 6))

        self.entry_password = ctk.CTkEntry(
            frame,
            placeholder_text="Type your password here...",
            show="•",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_password.pack(fill="x")
        self.entry_password.bind("<KeyRelease>", self._on_type)

        self.show_password_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            frame,
            text="Show password",
            variable=self.show_password_var,
            command=self._toggle_visibility,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(8, 0))

        # Strength bar
        ctk.CTkLabel(
            frame,
            text="Password Strength",
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(fill="x", pady=(20, 6))

        self.strength_bar = ctk.CTkProgressBar(frame, height=16)
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x")

        self.label_strength = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=12), anchor="w"
        )
        self.label_strength.pack(fill="x", pady=(4, 0))

        # Feedback labels
        self.label_feedback = ctk.CTkLabel(
            frame,
            text=" ",
            font=ctk.CTkFont(size=12, slant="italic"),
            anchor="w",
            wraplength=400
        )
        self.label_feedback.pack(fill="x", pady=(6, 0))

        self.label_hibp = ctk.CTkLabel(
            frame,
            text=" ",
            font=ctk.CTkFont(size=12, slant="italic"),
            anchor="w",
            wraplength=400
        )
        self.label_hibp.pack(fill="x", pady=(2, 0))

        # Test button
        self.button_test = ctk.CTkButton(
            frame,
            text="Test Password",
            height=44,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._test_password
        )
        self.button_test.pack(fill="x", pady=(20, 0))

    # ------------------------------------------------------------------ #
    #  GENERATE TAB                                                        #
    # ------------------------------------------------------------------ #
    def _build_generate_tab(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(
            frame,
            text="Generate a Password",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 20))

        # Length slider
        self.length_var = ctk.IntVar(value=16)

        length_row = ctk.CTkFrame(frame, fg_color="transparent")
        length_row.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(
            length_row,
            text="Length",
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(side="left")

        self.label_length_value = ctk.CTkLabel(
            length_row,
            text="16",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="e"
        )
        self.label_length_value.pack(side="right")

        self.slider_length = ctk.CTkSlider(
            frame,
            from_=8,
            to=32,
            number_of_steps=24,
            variable=self.length_var,
            command=self._on_slider
        )
        self.slider_length.pack(fill="x", pady=(0, 20))

        # Character type checkboxes
        ctk.CTkLabel(
            frame,
            text="Include",
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(fill="x", pady=(0, 8))

        self.var_upper   = ctk.BooleanVar(value=True)
        self.var_lower   = ctk.BooleanVar(value=True)
        self.var_digits  = ctk.BooleanVar(value=True)
        self.var_special = ctk.BooleanVar(value=True)

        checkbox_frame = ctk.CTkFrame(frame, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=(0, 20))

        for text, var in [
            ("Uppercase (A–Z)",       self.var_upper),
            ("Lowercase (a–z)",       self.var_lower),
            ("Digits (0–9)",          self.var_digits),
            ("Special (!@#$%^&*())", self.var_special),
        ]:
            ctk.CTkCheckBox(
                checkbox_frame,
                text=text,
                variable=var,
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=3)

        # Generated password output
        ctk.CTkLabel(
            frame,
            text="Generated Password",
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(fill="x", pady=(0, 6))

        output_row = ctk.CTkFrame(frame, fg_color="transparent")
        output_row.pack(fill="x", pady=(0, 8))

        self.entry_generated = ctk.CTkEntry(
            output_row,
            height=40,
            font=ctk.CTkFont(size=14),
            state="readonly",
            placeholder_text="Click Generate..."
        )
        self.entry_generated.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            output_row,
            text="Copy",
            width=70,
            height=40,
            command=self._copy_password
        ).pack(side="right")

        # Error label
        self.label_gen_error = ctk.CTkLabel(
            frame,
            text=" ",
            font=ctk.CTkFont(size=12, slant="italic"),
            anchor="w",
            text_color="#E03E3E"
        )
        self.label_gen_error.pack(fill="x")

        # Generate button
        ctk.CTkButton(
            frame,
            text="Generate",
            height=44,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._generate_password
        ).pack(fill="x", pady=(12, 0))

    # ------------------------------------------------------------------ #
    #  TEST TAB LOGIC                                                      #
    # ------------------------------------------------------------------ #
    def _on_type(self, event=None):
        password = self.entry_password.get()

        if not password:
            self.strength_bar.set(0)
            self.strength_bar.configure(progress_color="#4A4A4A")
            self.label_strength.configure(text="", text_color="gray")
            self.label_feedback.configure(text=" ")
            self.label_hibp.configure(text=" ")
            return

        strength = get_strength(password)
        config = STRENGTH_CONFIG[strength]
        self.strength_bar.set(config["progress"])
        self.strength_bar.configure(progress_color=config["color"])
        self.label_strength.configure(text=config["label"], text_color=config["color"])

    def _toggle_visibility(self):
        self.entry_password.configure(
            show="" if self.show_password_var.get() else "•"
        )

    def _test_password(self):
        password = self.entry_password.get()

        result = check_password(password)
        if result:
            self.label_feedback.configure(text=f"✗ {result}", text_color="#E03E3E")
            self.label_hibp.configure(text=" ")
            return

        self.label_feedback.configure(text="✓ Password is secure!", text_color="#00C864")
        self.label_hibp.configure(text="⏳ Checking breach database...", text_color="gray")
        self.button_test.configure(state="disabled")

        thread = threading.Thread(target=self._run_hibp_check, args=(password,), daemon=True)
        thread.start()

    def _run_hibp_check(self, password: str):
        try:
            pwned, count = check_hibp(password)
            if pwned:
                msg = f"⚠ Found in {count:,} data breach(es). Avoid using this password."
                color = "#E08C00"
            else:
                msg = "✓ Not found in any known data breaches."
                color = "#00C864"
        except Exception:
            msg = "⚠ Could not reach breach database. Check your connection."
            color = "gray"

        self.after(0, self._update_hibp_label, msg, color)

    def _update_hibp_label(self, msg: str, color: str):
        self.label_hibp.configure(text=msg, text_color=color)
        self.button_test.configure(state="normal")

    def _show_tips(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Password Tips")
        dialog.geometry("360x240")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Tips for a strong password",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            dialog,
            text=TIPS_TEXT,
            font=ctk.CTkFont(size=12),
            justify="left",
            wraplength=300
        ).pack(padx=24, pady=(0, 16))

        ctk.CTkButton(
            dialog, text="Got it", width=100, command=dialog.destroy
        ).pack(pady=(0, 16))

    def _toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙 Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀ Light Mode")
    
    # ------------------------------------------------------------------ #
    #  GENERATE TAB LOGIC                                                  #
    # ------------------------------------------------------------------ #
    def _on_slider(self, value):
        self.label_length_value.configure(text=str(int(value)))

    def _generate_password(self):
        if not any([
            self.var_upper.get(),
            self.var_lower.get(),
            self.var_digits.get(),
            self.var_special.get()
        ]):
            self.label_gen_error.configure(text="✗ Select at least one character type.")
            return

        self.label_gen_error.configure(text=" ")

        password = generate_password(
            length=self.length_var.get(),
            use_upper=self.var_upper.get(),
            use_lower=self.var_lower.get(),
            use_digits=self.var_digits.get(),
            use_special=self.var_special.get()
        )

        self.entry_generated.configure(state="normal")
        self.entry_generated.delete(0, "end")
        self.entry_generated.insert(0, password)
        self.entry_generated.configure(state="readonly")

    def _copy_password(self):
        password = self.entry_generated.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
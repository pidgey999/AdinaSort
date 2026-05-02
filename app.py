import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Callable


@dataclass
class Item:
    name: str
    price: int


class InventoryApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Battle Royale Assistant")
        self.root.geometry("680x430")

        self.gold = 1000
        self.max_slots = 10
        self.inventory: list[Item] = []
        self.shop_items = [
            Item("Camera", 150),
            Item("Drone", 200),
            Item("EMP", 250),
            Item("Medkit", 100),
        ]

        self.hotkeys: dict[str, str] = {
            "Chest Slot 1": "F1",
            "Chest Slot 2": "F2",
            "Chest Slot 3": "F3",
        }

        # TODO: connect this to your existing automation sorter implementation.
        self.sort_callback: Callable[[], None] = self._default_sort_callback

        self._build_ui()
        self._refresh_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")
        ttk.Label(
            header,
            text="Battle Royale Inventory Helper",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        self.gold_label = ttk.Label(header, text="")
        self.gold_label.pack(side="right")

        icon_row = ttk.LabelFrame(self.root, text="Quick Actions", padding=12)
        icon_row.pack(fill="x", padx=12)

        self._icon_button(icon_row, "↕", "Sort", self.sort_inventory).pack(side="left", padx=6)
        self._icon_button(icon_row, "🛒", "Buy", self.open_buy_dialog).pack(side="left", padx=6)
        self._icon_button(icon_row, "⌨", "Hotkeys", self.open_hotkey_dialog).pack(side="left", padx=6)

        body = ttk.Frame(self.root, padding=12)
        body.pack(fill="both", expand=True)

        left = ttk.LabelFrame(body, text="Shop", padding=10)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.shop_list = tk.Listbox(left, height=10)
        self.shop_list.pack(fill="both", expand=True)
        ttk.Button(left, text="Buy Selected", command=self.buy_selected_item).pack(fill="x", pady=(8, 0))

        right = ttk.LabelFrame(body, text="Inventory", padding=10)
        right.pack(side="right", fill="both", expand=True, padx=(6, 0))

        self.inventory_list = tk.Listbox(right, height=10)
        self.inventory_list.pack(fill="both", expand=True)

        row = ttk.Frame(right)
        row.pack(fill="x", pady=(8, 0))
        ttk.Button(row, text="Drop Selected", command=self.drop_item).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Sort Now", command=self.sort_inventory).pack(side="left", fill="x", expand=True, padx=(6, 0))

    def _icon_button(self, parent: tk.Widget, icon: str, text: str, command: Callable[[], None]) -> ttk.Button:
        return ttk.Button(parent, text=f"{icon}\n{text}", command=command)

    def _refresh_ui(self) -> None:
        self.gold_label.config(text=f"Gold: {self.gold} | Slots: {len(self.inventory)}/{self.max_slots}")

        self.shop_list.delete(0, tk.END)
        for item in self.shop_items:
            self.shop_list.insert(tk.END, f"{item.name} ({item.price}g)")

        self.inventory_list.delete(0, tk.END)
        for idx, item in enumerate(self.inventory, start=1):
            self.inventory_list.insert(tk.END, f"{idx}. {item.name}")

    def _default_sort_callback(self) -> None:
        # Replace this with existing sorter.sort_once call when integrated.
        return

    def sort_inventory(self) -> None:
        order = {"Camera": 0, "Drone": 1, "EMP": 2}

        def key(item: Item) -> tuple[int, str]:
            return (order.get(item.name, 99), item.name)

        self.inventory.sort(key=key)
        self.sort_callback()
        self._refresh_ui()
        messagebox.showinfo("Sort", "Inventory sorted. (Hook up with in-game sorter next)")

    def open_buy_dialog(self) -> None:
        if not self.shop_items:
            messagebox.showwarning("Shop", "No items in shop.")
            return
        self.shop_list.selection_clear(0, tk.END)
        self.shop_list.selection_set(0)
        self.buy_selected_item()

    def buy_selected_item(self) -> None:
        selected = self.shop_list.curselection()
        if not selected:
            messagebox.showinfo("Info", "Select an item to buy.")
            return
        if len(self.inventory) >= self.max_slots:
            messagebox.showwarning("Inventory Full", "No empty inventory slot.")
            return

        item = self.shop_items[selected[0]]
        if self.gold < item.price:
            messagebox.showwarning("Not enough gold", "You do not have enough gold.")
            return

        self.gold -= item.price
        self.inventory.append(item)
        self._refresh_ui()

    def drop_item(self) -> None:
        selected = self.inventory_list.curselection()
        if not selected:
            messagebox.showinfo("Info", "Select an item to drop.")
            return
        del self.inventory[selected[0]]
        self._refresh_ui()

    def open_hotkey_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Chest Hotkeys")
        dialog.geometry("340x220")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Set hotkeys for grabbing chest items", font=("Segoe UI", 10, "bold")).pack(pady=10)

        entries: dict[str, ttk.Entry] = {}

        form = ttk.Frame(dialog, padding=10)
        form.pack(fill="both", expand=True)

        for idx, action in enumerate(self.hotkeys.keys()):
            ttk.Label(form, text=action).grid(row=idx, column=0, sticky="w", pady=4)
            entry = ttk.Entry(form)
            entry.insert(0, self.hotkeys[action])
            entry.grid(row=idx, column=1, sticky="ew", pady=4, padx=(8, 0))
            entries[action] = entry

        form.columnconfigure(1, weight=1)

        def save_hotkeys() -> None:
            for action, entry in entries.items():
                value = entry.get().strip().upper()
                if not value:
                    messagebox.showwarning("Invalid", f"Hotkey for '{action}' cannot be empty.")
                    return
                self.hotkeys[action] = value
            messagebox.showinfo("Saved", "Hotkeys saved for chest-grab actions.")
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save_hotkeys).pack(pady=(0, 12))


def main() -> None:
    root = tk.Tk()
    InventoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

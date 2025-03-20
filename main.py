from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea, Button, Label, Static
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from datetime import datetime
import json
import os

JOURNAL_FILE = "roses_thorns_journal.json"

def load_entries():
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_entry(date, roses, thorn):
    entries = load_entries()
    entries[date] = {"roses": roses, "thorn": thorn}
    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=4)

class HistoryScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]
    
    def compose(self) -> ComposeResult:
        yield Header("History of Entries")
        yield Static(id="history_results", classes="results")
        yield Footer()
    
    def on_mount(self) -> None:
        results = self.load_history()
        self.display_results(results)
    
    def load_history(self):
        entries = load_entries()
        return sorted(entries.items(), reverse=True)
    
    def display_results(self, results):
        output = self.query_one("#history_results")
        
        if not results:
            output.update("No entries found.")
            return
            
        text = []
        for date, content in results:
            text.append(f"[bold]📅 {date}[/bold]")
            text.append(f"[green]🌹 Roses:[/green] • {' • '.join(content['roses'])}")
            text.append(f"[red]🌵 Thorn:[/red] {content['thorn']}")
            text.append("―" * 40)
            
        output.update("\n".join(text))

class RosesAndThornsApp(App):
    BINDINGS = [("q", "quit", "Quit")]
    
    def compose(self) -> ComposeResult:
        self.date = datetime.today().strftime("%Y-%m-%d")
        
        yield Header("Roses and Thorns Journal")
        yield Vertical(
            Label(f"📅 {self.date}"),
            Label("[green]🌹 Rose #1:[/green] Something positive about your day", classes="prompt"),
            TextArea(id="rose1"),
            Label("[green]🌹 Rose #2:[/green] Another positive about your day", classes="prompt"),
            TextArea(id="rose2"),
            Label("[red]🌵 Thorn:[/red] Something challenging about your day", classes="prompt"),
            TextArea(id="thorn"),
            Horizontal(
                Button("💾 Save", id="save"),
                Button("📜 History", id="history"),
            ),
            Static(id="output")
        )
        yield Footer()

    def on_mount(self) -> None:
        self.rose1_box = self.query_one("#rose1")
        self.rose2_box = self.query_one("#rose2")
        self.thorn_box = self.query_one("#thorn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        output = self.query_one("#output")
        
        if button_id == "save":
            rose1 = self.rose1_box.text.strip()
            rose2 = self.rose2_box.text.strip()
            thorn = self.thorn_box.text.strip()
            
            if not rose1 or not rose2 or not thorn:
                output.update("⚠️ Please fill in both roses and a thorn!")
                return
                
            save_entry(self.date, [rose1, rose2], thorn)
            output.update("✅ Entry saved!")
            
        elif button_id == "history":
            self.push_screen(HistoryScreen())

if __name__ == "__main__":
    app = RosesAndThornsApp()
    app.run()

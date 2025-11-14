# todo.py
"""
Enhanced CLI To-Do List with timestamped exports and export folder maintenance.

Features added per request:
- Export filenames include date & time (timestamp)
- PDF includes header (App title + your name) and export timestamp inside the PDF
- Exports saved into "exports/" folder
- Auto-delete old exports older than AUTO_DELETE_DAYS
- CSV export (timestamped) saved to exports/ as well
"""

import csv
import os
import json
import glob
from datetime import datetime, date, timedelta

# ---------- CONFIG ----------
CSV_FILE = "tasks.csv"
EXPORTS_DIR = "exports"
AUTO_DELETE_DAYS = 7  # files older than this (days) will be auto-deleted from exports/
USER_FULL_NAME = "Kethari Madhu Sudhan Reddy"  # your name to print in PDF header
APP_TITLE = "Madhu's To-Do CLI"
DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"

# ---------- Utilities ----------
def timestamp_now():
    return datetime.now().strftime(TIMESTAMP_FORMAT)

def timestamp_human():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_exports_dir():
    if not os.path.exists(EXPORTS_DIR):
        os.makedirs(EXPORTS_DIR, exist_ok=True)

def clean_old_exports(days=AUTO_DELETE_DAYS):
    """Delete files in exports folder older than `days` days."""
    ensure_exports_dir()
    cutoff = datetime.now() - timedelta(days=days)
    patterns = [os.path.join(EXPORTS_DIR, "*")]
    deleted = 0
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < cutoff:
                    os.remove(path)
                    deleted += 1
            except Exception:
                continue
    if deleted:
        print(f"Auto-clean: removed {deleted} old export file(s) older than {days} day(s).")

# ---------- Date handling ----------
def parse_date(s):
    s = (s or "").strip()
    if s.lower() in ("", "no due", "none", "na"):
        return None
    try:
        return datetime.strptime(s, DATE_FORMAT).date()
    except ValueError:
        return None

def format_date(d):
    return d.strftime(DATE_FORMAT) if d else "no due"

# ---------- CSV persistence ----------
def load_tasks():
    tasks = []
    if not os.path.exists(CSV_FILE):
        return tasks
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                task = {
                    "id": int(row.get("id", "") or 0),
                    "title": row.get("title", "") or "",
                    "done": row.get("done", "0") == "1",
                    "due": parse_date(row.get("due", "")),
                    "priority": int(row.get("priority", "0") or 0),
                    "category": row.get("category", "") or "General",
                    "starred": row.get("starred", "0") == "1",
                    "subtasks": json.loads(row.get("subtasks_json", "[]") or "[]"),
                    "notes": row.get("notes", "") or ""
                }
                tasks.append(task)
            except Exception:
                continue
    return tasks

def save_tasks(tasks):
    # assign incremental ids
    for idx, t in enumerate(tasks, start=1):
        t["id"] = idx
    fieldnames = ["id", "title", "done", "due", "priority", "category", "starred", "subtasks_json", "notes"]
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in tasks:
            writer.writerow({
                "id": t.get("id", ""),
                "title": t.get("title", ""),
                "done": "1" if t.get("done") else "0",
                "due": format_date(t.get("due")),
                "priority": str(t.get("priority", 0) or 0),
                "category": t.get("category", ""),
                "starred": "1" if t.get("starred") else "0",
                "subtasks_json": json.dumps(t.get("subtasks", []), ensure_ascii=False),
                "notes": t.get("notes", "")
            })

# ---------- Display helpers ----------
def print_starred(tasks):
    starred = [t for t in tasks if t.get("starred") and not t.get("done")]
    if not starred:
        return
    print("\n★ Starred / Important tasks:")
    for t in starred:
        due = format_date(t.get("due"))
        pri = t.get("priority") or "-"
        print(f"  [*] {t['title']} (Due: {due}, Pri: {pri}, Cat: {t['category']})")
    print()

def show_menu_header(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t["done"])
    print("\n" + "="*60)
    print(f"{APP_TITLE} — CLI To-Do List")
    print(f"Owner: {USER_FULL_NAME}")
    print(f"Tasks completed: {completed}/{total}")
    print_starred(tasks)
    print("="*60)

def show_tasks(tasks, filter_mode="all", sort_mode=None):
    filtered = tasks
    if filter_mode == "incomplete":
        filtered = [t for t in tasks if not t["done"]]
    elif filter_mode == "completed":
        filtered = [t for t in tasks if t["done"]]
    elif filter_mode and filter_mode.startswith("category:"):
        cat = filter_mode.split(":",1)[1]
        filtered = [t for t in tasks if t["category"].lower() == cat.lower()]

    if sort_mode == "priority":
        filtered = sorted(filtered, key=lambda x: (x.get("priority") or 999))
    elif sort_mode == "due":
        filtered = sorted(filtered, key=lambda x: (x.get("due") is None, x.get("due") or date.max))
    elif sort_mode == "alpha":
        filtered = sorted(filtered, key=lambda x: x.get("title","").lower())

    if not filtered:
        print("\nNo tasks for this view.\n")
        return

    print("\nIndex | Done | Star | Pri | Due        | Category   | Title")
    print("-"*90)
    for i, t in enumerate(filtered, start=1):
        done = "[✔]" if t["done"] else "[ ]"
        star = "[*]" if t["starred"] else "   "
        pri = str(t["priority"]) if t["priority"] else "-"
        due = format_date(t.get("due"))
        cat = t.get("category")
        title = t.get("title")
        print(f"{i:5} | {done:4} | {star:3} | {pri:3} | {due:10} | {cat:10} | {title}")
        if t.get("subtasks"):
            for si, st in enumerate(t["subtasks"], start=1):
                st_done = "[✔]" if st.get("done") else "[ ]"
                print(f"      - {st_done} {st.get('title')}")
    print("-"*90)
    print(f"Showing {len(filtered)} task(s).")

# ---------- Input helpers ----------
def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a non-empty value.")

def input_priority():
    while True:
        s = input("Priority (1 highest .. 5 lowest) or blank for none: ").strip()
        if s == "":
            return 0
        if s.isdigit() and 1 <= int(s) <= 5:
            return int(s)
        print("Invalid priority. Enter 1-5 or blank.")

def input_due():
    while True:
        s = input(f"Due date (YYYY-MM-DD) or blank for no due: ").strip()
        if s == "":
            return None
        d = parse_date(s)
        if d:
            return d
        print("Invalid date format. Use YYYY-MM-DD.")

def choose_task(tasks, filter_mode="all"):
    if filter_mode == "incomplete":
        candidates = [t for t in tasks if not t["done"]]
    elif filter_mode == "completed":
        candidates = [t for t in tasks if t["done"]]
    else:
        candidates = tasks

    if not candidates:
        print("No tasks to choose from.")
        return None

    for idx, t in enumerate(candidates, start=1):
        print(f"{idx}. {'[✔]' if t['done'] else '[ ]'} {t['title']} (Due: {format_date(t.get('due'))})")
    try:
        sel = int(input("Enter selection number: ").strip())
        if 1 <= sel <= len(candidates):
            chosen = candidates[sel-1]
            for i, tt in enumerate(tasks):
                if tt is chosen:
                    return i
        print("Invalid selection.")
        return None
    except ValueError:
        print("Please enter a number.")
        return None

# ---------- Operations ----------
def add_task(tasks):
    title = input_nonempty("Task title: ")
    due = input_due()
    priority = input_priority()
    print("Choose category (or type custom):")
    print("1. Work\n2. Personal\n3. Study\n4. Others\n5. Custom")
    cat_choice = input("Choice (1-5): ").strip()
    if cat_choice == "1":
        category = "Work"
    elif cat_choice == "2":
        category = "Personal"
    elif cat_choice == "3":
        category = "Study"
    elif cat_choice == "4":
        category = "Others"
    else:
        category = input_nonempty("Enter custom category: ")
    starred = input("Mark as important / starred? (yes/no): ").strip().lower() == "yes"
    notes = input("Notes (optional): ").strip()

    subtasks = []
    while True:
        s = input("Add a subtask (leave blank to stop): ").strip()
        if not s:
            break
        subtasks.append({"title": s, "done": False})

    task = {
        "id": 0,
        "title": title,
        "done": False,
        "due": due,
        "priority": priority,
        "category": category,
        "starred": starred,
        "subtasks": subtasks,
        "notes": notes
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added and saved.")

def remove_task(tasks):
    idx = choose_task(tasks, "all")
    if idx is None:
        return
    t = tasks[idx]
    confirm = input(f"Are you sure you want to DELETE '{t['title']}'? Type 'yes' to confirm: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return
    tasks.pop(idx)
    save_tasks(tasks)
    print("Task removed.")

def toggle_done(tasks):
    idx = choose_task(tasks, "all")
    if idx is None:
        return
    tasks[idx]["done"] = not tasks[idx]["done"]
    save_tasks(tasks)
    status = "completed" if tasks[idx]["done"] else "not completed"
    print(f"Task '{tasks[idx]['title']}' marked {status}.")

def edit_task(tasks):
    idx = choose_task(tasks, "all")
    if idx is None:
        return
    t = tasks[idx]
    print(f"Editing task: {t['title']}")
    confirm = input("Proceed to edit? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Edit cancelled.")
        return
    print("Leave blank to keep current value.")
    new_title = input(f"New title [{t['title']}]: ").strip()
    if new_title:
        t['title'] = new_title
    print(f"Current due: {format_date(t['due'])}")
    new_due_raw = input("New due (YYYY-MM-DD) or blank: ").strip()
    if new_due_raw:
        new_due = parse_date(new_due_raw)
        if new_due:
            t['due'] = new_due
        else:
            print("Invalid date; keeping old.")
    new_pri = input(f"New priority (1-5) or blank [{t['priority'] or '-'}]: ").strip()
    if new_pri:
        if new_pri.isdigit() and 1 <= int(new_pri) <= 5:
            t['priority'] = int(new_pri)
        else:
            print("Invalid priority; keeping old.")
    new_cat = input(f"New category or blank [{t['category']}]: ").strip()
    if new_cat:
        t['category'] = new_cat
    star = input(f"Starred? yes/no or blank [{ 'yes' if t['starred'] else 'no' }]: ").strip().lower()
    if star == "yes":
        t['starred'] = True
    elif star == "no":
        t['starred'] = False

    if t.get("subtasks"):
        print("Subtasks:")
        for i, st in enumerate(t["subtasks"], start=1):
            print(f"{i}. {'[x]' if st['done'] else '[ ]'} {st['title']}")
        sub_action = input("Edit subtasks? (add/toggle/remove/skip): ").strip().lower()
    else:
        sub_action = input("Add subtasks? (add/skip): ").strip().lower()

    if sub_action == "add":
        while True:
            s = input("Subtask title (blank to stop): ").strip()
            if not s:
                break
            t['subtasks'].append({"title": s, "done": False})
    elif sub_action == "toggle":
        try:
            which = int(input("Enter subtask number to toggle: ").strip())
            if 1 <= which <= len(t['subtasks']):
                t['subtasks'][which-1]['done'] = not t['subtasks'][which-1]['done']
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")
    elif sub_action == "remove":
        try:
            which = int(input("Enter subtask number to remove: ").strip())
            if 1 <= which <= len(t['subtasks']):
                removed = t['subtasks'].pop(which-1)
                print(f"Removed subtask: {removed['title']}")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")
    new_notes = input(f"Notes (blank to keep) [{t.get('notes','')[:40]}]: ").strip()
    if new_notes:
        t['notes'] = new_notes
    save_tasks(tasks)
    print("Task updated and saved.")

def search_tasks(tasks):
    q = input("Enter search text (searches title, category, due, priority, notes): ").strip().lower()
    if not q:
        print("Empty search.")
        return
    results = []
    for t in tasks:
        if q in t.get('title','').lower() or q in t.get('category','').lower() or q in (t.get('notes','').lower()):
            results.append(t)
        else:
            if t.get('due') and q in format_date(t.get('due')):
                results.append(t)
            elif q.isdigit() and int(q) == t.get('priority'):
                results.append(t)
    if not results:
        print("No matches.")
        return
    show_tasks(results)

def add_subtask(tasks):
    idx = choose_task(tasks, "all")
    if idx is None:
        return
    t = tasks[idx]
    s = input_nonempty("Subtask title: ")
    t.setdefault("subtasks", []).append({"title": s, "done": False})
    save_tasks(tasks)
    print("Subtask added.")

# ---------- Sorting helpers ----------
def sort_menu(tasks):
    print("Sort by:")
    print("1. Priority (high → low)")
    print("2. Due date (closest first)")
    print("3. Alphabetical (A→Z)")
    print("4. Cancel")
    c = input("Choice (1-4): ").strip()
    if c == "1":
        show_tasks(tasks, "all", sort_mode="priority")
    elif c == "2":
        show_tasks(tasks, "all", sort_mode="due")
    elif c == "3":
        show_tasks(tasks, "all", sort_mode="alpha")
    else:
        print("Cancelled sort view.")

# ---------- Reminders ----------
def startup_reminders(tasks):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    due_today = [t for t in tasks if t.get("due") == today and not t.get("done")]
    due_tom = [t for t in tasks if t.get("due") == tomorrow and not t.get("done")]
    if due_today or due_tom:
        print("\n⚠️  Reminders:")
        if due_today:
            for t in due_today:
                print(f"  - DUE TODAY: {t['title']} (Pri: {t.get('priority') or '-'}, Cat: {t.get('category')})")
        if due_tom:
            for t in due_tom:
                print(f"  - DUE TOMORROW: {t['title']} (Pri: {t.get('priority') or '-'}, Cat: {t.get('category')})")
        print()

# ---------- Export helpers ----------
def export_to_csv(tasks, filename=None):
    ensure_exports_dir()
    clean_old_exports()
    ts = timestamp_now()
    if not filename:
        filename = os.path.join(EXPORTS_DIR, f"tasks_export_{ts}.csv")
    fieldnames = ["id", "title", "done", "due", "priority", "category", "starred", "subtasks_json", "notes"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in tasks:
            writer.writerow({
                "id": t.get("id", ""),
                "title": t.get("title", ""),
                "done": "1" if t.get("done") else "0",
                "due": format_date(t.get("due")),
                "priority": str(t.get("priority", 0) or 0),
                "category": t.get("category", ""),
                "starred": "1" if t.get("starred") else "0",
                "subtasks_json": json.dumps(t.get("subtasks", []), ensure_ascii=False),
                "notes": t.get("notes", "")
            })
    print(f"Exported tasks to {filename}")

def export_to_pdf(tasks):
    ensure_exports_dir()
    clean_old_exports()
    try:
        from fpdf import FPDF
    except Exception:
        print("PDF export requires 'fpdf' package.")
        print("Install with: pip install fpdf")
        choice = input("Export to CSV instead? (yes/no): ").strip().lower()
        if choice == "yes":
            export_to_csv(tasks)
        else:
            print("PDF export cancelled.")
        return

    ts = timestamp_now()
    human_ts = timestamp_human()
    filename = os.path.join(EXPORTS_DIR, f"tasks_export_{ts}.pdf")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    # Header: App title and user name
    pdf.cell(0, 8, APP_TITLE, ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 7, f"Owner: {USER_FULL_NAME}", ln=True)
    pdf.cell(0, 7, f"Exported: {human_ts}", ln=True)
    pdf.ln(4)

    # Content per task
    pdf.set_font("Arial", size=11)
    for t in tasks:
        status = "Done" if t.get("done") else "Pending"
        star = "*" if t.get("starred") else ""
        due = format_date(t.get("due"))
        pri = str(t.get("priority")) if t.get("priority") else "-"
        header = f"{star} {t.get('title')} [{status}] (Due: {due}, Pri: {pri}, Cat: {t.get('category')})"
        pdf.multi_cell(0, 6, header)
        if t.get("notes"):
            pdf.multi_cell(0, 5, f"Notes: {t.get('notes')}")
        if t.get("subtasks"):
            for st in t["subtasks"]:
                st_status = "x" if st.get("done") else " "
                pdf.multi_cell(0, 5, f"  - [{st_status}] {st.get('title')}")
        pdf.ln(2)

    # Footer with generation timestamp
    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 6, f"Generated by {APP_TITLE} for {USER_FULL_NAME} on {human_ts}", ln=True, align="C")

    pdf.output(filename)
    print(f"Exported tasks to {filename}")

# ----------------- Main loop -----------------
def main():
    tasks = load_tasks()
    startup_reminders(tasks)

    while True:
        show_menu_header(tasks)
        print("Menu:")
        print("1. View all tasks")
        print("2. View only incomplete tasks")
        print("3. View only completed tasks")
        print("4. Add task (with due date, priority, category, subtasks)")
        print("5. Remove task (with confirmation)")
        print("6. Mark complete / toggle")
        print("7. Edit task (with confirmation)")
        print("8. Add a subtask to a task")
        print("9. Search tasks")
        print("10. Sort / Sorting views")
        print("11. Export to PDF (saved to exports/ with timestamped filename)")
        print("12. Export to CSV (saved to exports/ with timestamped filename)")
        print("13. Exit")

        choice = input("Choose (1-13): ").strip()
        if choice == "1":
            show_tasks(tasks, "all")
        elif choice == "2":
            show_tasks(tasks, "incomplete")
        elif choice == "3":
            show_tasks(tasks, "completed")
        elif choice == "4":
            add_task(tasks)
        elif choice == "5":
            remove_task(tasks)
        elif choice == "6":
            toggle_done(tasks)
        elif choice == "7":
            edit_task(tasks)
        elif choice == "8":
            add_subtask(tasks)
        elif choice == "9":
            search_tasks(tasks)
        elif choice == "10":
            sort_menu(tasks)
        elif choice == "11":
            export_to_pdf(tasks)
        elif choice == "12":
            export_to_csv(tasks)
        elif choice == "13":
            print("Goodbye — tasks saved in", CSV_FILE)
            break
        else:
            print("Invalid choice. Pick a number from 1 to 13.")

if __name__ == "__main__":
    main()

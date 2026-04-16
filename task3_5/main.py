from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

import streamlit as st

TASKS_FILE = Path(__file__).parent / "tasks.json"
STATUSES = ["pending", "in-progress", "done"]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str
    created_at: str

    @classmethod
    def new(cls, title: str, description: str, status: str = "pending") -> "Task":
        return cls(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            status=status,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def load_tasks() -> list[Task]:
    """Load tasks from JSON file. Returns empty list on missing/corrupt file."""
    if not TASKS_FILE.exists():
        return []
    try:
        raw = TASKS_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array")
        return [Task(**item) for item in data]
    except (json.JSONDecodeError, TypeError, ValueError, KeyError):
        st.warning(
            f"⚠️ `tasks.json` is corrupted or has an unexpected format. "
            "Starting with an empty task list."
        )
        return []


def save_tasks(tasks: list[Task]) -> None:
    """Persist tasks list to JSON file."""
    TASKS_FILE.write_text(
        json.dumps([asdict(t) for t in tasks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Session state bootstrap
# ---------------------------------------------------------------------------

def init_state() -> None:
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()
    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None
    if "confirm_delete_id" not in st.session_state:
        st.session_state.confirm_delete_id = None


# ---------------------------------------------------------------------------
# Sidebar — Create Task form
# ---------------------------------------------------------------------------

def render_sidebar() -> None:
    st.sidebar.title("➕ Add New Task")
    with st.sidebar.form("create_task_form", clear_on_submit=True):
        title = st.text_input("Title *", max_chars=120)
        description = st.text_area("Description", max_chars=500)
        status = st.selectbox("Initial Status", STATUSES)
        submitted = st.form_submit_button("Create Task")

    if submitted:
        if not title.strip():
            st.sidebar.error("Title is required.")
        else:
            task = Task.new(title.strip(), description.strip(), status)
            st.session_state.tasks.append(task)
            save_tasks(st.session_state.tasks)
            st.sidebar.success(f"Task **{task.title}** created.")
            st.rerun()


# ---------------------------------------------------------------------------
# Main area — task table + inline edit/delete
# ---------------------------------------------------------------------------

def render_task_table() -> None:
    tasks = st.session_state.tasks

    st.title("📋 Task Manager")
    st.caption(f"{len(tasks)} task(s) total  •  data saved in `tasks.json`")

    if not tasks:
        st.info("No tasks yet. Use the sidebar to create one.")
        return

    # Summary dataframe (read-only overview)
    st.subheader("All Tasks")
    st.dataframe(
        [
            {
                "ID": t.id,
                "Title": t.title,
                "Status": t.status,
                "Created": t.created_at,
            }
            for t in tasks
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # Per-task action rows
    st.subheader("Actions")
    for task in tasks:
        cols = st.columns([5, 1, 1])
        with cols[0]:
            badge = {"pending": "🔵", "in-progress": "🟡", "done": "🟢"}.get(
                task.status, "⚪"
            )
            st.markdown(f"{badge} **{task.title}** — *{task.status}*")
            if task.description:
                st.caption(task.description[:120])

        with cols[1]:
            if st.button("✏️ Edit", key=f"edit_{task.id}", use_container_width=True):
                st.session_state.edit_id = task.id
                st.session_state.confirm_delete_id = None
                st.rerun()

        with cols[2]:
            if st.button("🗑️ Delete", key=f"del_{task.id}", use_container_width=True):
                st.session_state.confirm_delete_id = task.id
                st.session_state.edit_id = None
                st.rerun()

    # Delete confirmation banner
    if st.session_state.confirm_delete_id:
        target = next(
            (t for t in tasks if t.id == st.session_state.confirm_delete_id), None
        )
        if target:
            st.warning(f"Delete **{target.title}**? This cannot be undone.")
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("Yes, delete", type="primary"):
                st.session_state.tasks = [
                    t for t in tasks if t.id != target.id
                ]
                save_tasks(st.session_state.tasks)
                st.session_state.confirm_delete_id = None
                st.rerun()
            if c2.button("Cancel"):
                st.session_state.confirm_delete_id = None
                st.rerun()


def render_edit_form() -> None:
    """Render inline edit form when edit_id is set."""
    edit_id = st.session_state.edit_id
    if edit_id is None:
        return

    task = next(
        (t for t in st.session_state.tasks if t.id == edit_id), None
    )
    if task is None:
        st.session_state.edit_id = None
        return

    st.divider()
    st.subheader(f"✏️ Editing: {task.title}")
    with st.form("edit_task_form"):
        new_title = st.text_input("Title *", value=task.title, max_chars=120)
        new_desc = st.text_area("Description", value=task.description, max_chars=500)
        current_idx = STATUSES.index(task.status) if task.status in STATUSES else 0
        new_status = st.selectbox("Status", STATUSES, index=current_idx)
        c1, c2 = st.columns(2)
        save = c1.form_submit_button("💾 Save", type="primary")
        cancel = c2.form_submit_button("Cancel")

    if save:
        if not new_title.strip():
            st.error("Title cannot be empty.")
        else:
            task.title = new_title.strip()
            task.description = new_desc.strip()
            task.status = new_status
            save_tasks(st.session_state.tasks)
            st.session_state.edit_id = None
            st.rerun()

    if cancel:
        st.session_state.edit_id = None
        st.rerun()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Task Manager", page_icon="📋", layout="wide")
    init_state()
    render_sidebar()
    render_task_table()
    render_edit_form()


if __name__ == "__main__":
    main()

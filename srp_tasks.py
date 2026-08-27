from abc import ABC, abstractmethod


# --- Abstract Storage ---
class TaskStorage(ABC):
    @abstractmethod
    def load_tasks(self):
        pass

    @abstractmethod
    def save_tasks(self, tasks):
        pass


# --- Model Class (อัปเดต 2.1 & 2.2) ---
class Task:
    def __init__(
        self,
        task_id,
        description,
        due_date=None,
        completed=False,
        priority="medium",  # 2.1 เพิ่ม priority attribute (กำหนดค่าเริ่มต้นเป็น medium)
    ):
        self.id = task_id
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.priority = priority.lower()

    def mark_completed(self):
        self.completed = True
        print(f"Task {self.id} '{self.description}' marked as completed.")

    # 2.2 อัปเดต __str__ เพื่อแสดงผลค่า priority
    def __str__(self):
        status = "✓" if self.completed else " "
        due = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.id}. {self.description}{due} [Priority: {self.priority.upper()}]"


# --- File Storage (อัปเดตให้รองรับ priority) ---
class FileTaskStorage(TaskStorage):
    def __init__(self, filename="tasks.txt"):
        self.filename = filename

    def load_tasks(self):
        loaded_tasks = []
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 5:  # ปรับเพิ่มเป็น 5 ฟิลด์รองรับ priority
                        task_id = int(parts[0])
                        description = parts[1]
                        due_date = parts[2] if parts[2] != "None" else None
                        completed = parts[3] == "True"
                        priority = parts[4]
                        loaded_tasks.append(
                            Task(
                                task_id,
                                description,
                                due_date,
                                completed,
                                priority,
                            )
                        )
        except FileNotFoundError:
            print(
                f"No existing task file '{self.filename}' found. Starting fresh."
            )
        return loaded_tasks

    def save_tasks(self, tasks):
        with open(self.filename, "w") as f:
            for task in tasks:
                f.write(
                    f"{task.id},{task.description},{task.due_date},{task.completed},{task.priority}\n"
                )
        print(f"Tasks saved to {self.filename}")


# --- Task Manager Class (อัปเดต 2.3) ---
class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()
        self.next_id = (
            max([t.id for t in self.tasks] + [0]) + 1 if self.tasks else 1
        )
        print(f"Loaded {len(self.tasks)} tasks. Next ID: {self.next_id}")

    # 2.3 อัปเดต add_task ให้รับพารามิเตอร์ priority เพิ่มเติม
    def add_task(self, description, due_date=None, priority="medium"):
        task = Task(self.next_id, description, due_date, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)
        print(f"Task '{description}' added with {priority.upper()} priority.")
        return task

    def list_tasks(self):
        print("\n--- Current Tasks ---")
        if not self.tasks:
            print("No tasks available.")
            return
        for task in self.tasks:
            print(task)
        print("---------------------")

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_task_completed(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.storage.save_tasks(self.tasks)
            return True
        print(f"Task {task_id} not found.")
        return False


# --- Main Program Logic ---
if __name__ == "__main__":
    file_storage = FileTaskStorage("my_tasks.txt")
    manager = TaskManager(file_storage)

    # ทดสอบการเพิ่มงานโดยกำหนดระดับความสำคัญต่างกัน
    manager.add_task(
        "Review SOLID Principles", due_date="2024-08-10", priority="high"
    )
    manager.add_task(
        "Prepare for Final Exam", due_date="2024-08-15", priority="medium"
    )
    manager.add_task("Buy Coffee", priority="low")

    manager.list_tasks()
    manager.mark_task_completed(1)
    manager.list_tasks()
print("Finished")
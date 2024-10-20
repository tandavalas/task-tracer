from sqlite3 import Connection

from task.domain.entity import Task
from task.domain.value_objects.status import Status
from task.infrastructure.task_repository import TaskSqliteRepository


class TestTaskAlchemyRepository:
    def test_if_we_have_connection(self, connection):
        assert isinstance(connection, Connection)

    def test_create_new_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        result = repository.save(task)

        assert isinstance(result, int) is True
        assert result is not None

    def test_find_task_by_id(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        found = repository.get_by_id(1)

        assert isinstance(found.id, int) is True
        assert found.description == task.description
        assert found.status == task.status
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

    def test_return_none_when_passing_invalid_uuid(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        repository.save(task)

        found = repository.get_by_id("fake id")
        assert found is None

    def test_update_task(self, connection, migrations):
        description_updated = "update description"
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        task.id = repository.save(task)

        task.description = description_updated
        repository.update(task)
        updated = repository.get_by_id(task.id)

        assert isinstance(updated.id, int) is True
        assert updated.id == task.id
        assert updated.description == description_updated
        assert updated.created_at == task.created_at
        assert updated.updated_at != task.updated_at

    def test_delete_task(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)
        task.id = repository.save(task)

        found = repository.get_by_id(task.id)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == task.status
        assert found.created_at == task.created_at
        assert found.updated_at == task.updated_at

        repository.delete(task.id)

        found = repository.get_by_id(task.id)

        assert found is None

    def test_listing_tasks(self, connection, migrations):
        task1 = Task(description="task 1")
        task2 = Task(description="test 2")
        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)
        tasks = repository.list(page=1, per_page=2)

        assert len(tasks.items) == 2
        assert tasks.page == 1
        assert tasks.per_page == 2
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task1.id
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == task1.status
        assert tasks.items[0].created_at == task1.created_at
        assert tasks.items[0].updated_at == task1.updated_at

    def test_marking_task_as_in_progress(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)

        task.id = repository.save(task)
        found = repository.get_by_id(task.id)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == Status.TODO

        task.status = Status.IN_PROGRESS
        repository.update(task)

        found = repository.get_by_id(task.id)
        assert found.id == task.id
        assert found.status == Status.IN_PROGRESS

    def test_marking_task_as_done(self, connection, migrations):
        task = Task(description="test")
        repository = TaskSqliteRepository(connection)

        task.id = repository.save(task)
        found = repository.get_by_id(task.id)

        assert isinstance(found.id, int) is True
        assert found.id == task.id
        assert found.description == task.description
        assert found.status == Status.TODO

        task.status = Status.DONE
        repository.update(task)

        found = repository.get_by_id(task.id)
        assert found.id == task.id
        assert found.status == Status.DONE

    def test_list_task_with_todo_status(self, connection, migrations):
        task1 = Task(description="task 1", status=Status.TODO)
        task2 = Task(description="task 2", status=Status.DONE)

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        tasks = repository.list(filter=Status.TODO.value)

        assert len(tasks.items) == 1
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task1.id
        assert tasks.items[0].description == task1.description
        assert tasks.items[0].status == Status.TODO
        assert tasks.items[0].created_at == task1.created_at
        assert tasks.items[0].updated_at == task1.updated_at

    def test_list_task_with_done_status(self, connection, migrations):
        task1 = Task(description="task 1")
        task2 = Task(description="task 2", status=Status.DONE)

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        tasks = repository.list(filter=Status.DONE.value)

        assert len(tasks.items) == 1
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task2.id
        assert tasks.items[0].description == task2.description
        assert tasks.items[0].status == Status.DONE
        assert tasks.items[0].created_at == task2.created_at
        assert tasks.items[0].updated_at == task2.updated_at

    def test_list_task_with_in_progress_status(self, connection, migrations):
        task1 = Task(description="task 1")
        task2 = Task(description="task 2", status=Status.IN_PROGRESS)

        repository = TaskSqliteRepository(connection)
        task1.id = repository.save(task1)
        task2.id = repository.save(task2)

        tasks = repository.list(filter=Status.IN_PROGRESS.value)

        assert len(tasks.items) == 1
        assert isinstance(tasks.items[0].id, int) is True
        assert tasks.items[0].id == task2.id
        assert tasks.items[0].description == task2.description
        assert tasks.items[0].status == Status.IN_PROGRESS
        assert tasks.items[0].created_at == task2.created_at
        assert tasks.items[0].updated_at == task2.updated_at

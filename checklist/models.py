from django.db import models
from django.utils import dateformat


class Task(models.Model):
    name = models.CharField("Task title", max_length=50)
    description = models.TextField("Task description", blank=True)

    def __str__(self):
        return f"Task: {self.name}"


class Day(models.Model):
    day = models.IntegerField("Day number", primary_key=True)
    tasks = models.ManyToManyField(Task, verbose_name="Tasks for the day")

    class Meta:
        ordering = ["day"]

    def __str__(self):
        return f"Day {self.day}"


class Quarantine(models.Model):
    username = models.CharField("Username", max_length=150)
    start_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Start timestamp"
    )

    def __str__(self):
        return f"Quarantine for {self.username} on {self.pretty_start_timestamp()}"

    def pretty_start_timestamp(self):
        return dateformat.format(self.start_timestamp, 'Y-m-d H:i:s')


class QuarantineDay(models.Model):
    quarantine = models.ForeignKey(
        Quarantine,
        on_delete=models.CASCADE,
        verbose_name="Quarantine instance"
    )
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        verbose_name="Day data"
    )

    def __str__(self):
        day = self.day.day
        username = self.quarantine.username
        start_timestamp = self.quarantine.pretty_start_timestamp()

        return f"Quarantine day {day} for {username} on {start_timestamp}"


class QuarantineTask(models.Model):
    day = models.ForeignKey(
        QuarantineDay,
        on_delete=models.CASCADE,
        verbose_name="Quarantine task day instance"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Task data"
    )

    is_done = models.BooleanField("Task done", default=False)

    def __str__(self):
        task = self.task.name
        day = self.day.day.day
        username = self.day.quarantine.username
        start_timestamp = self.day.quarantine.pretty_start_timestamp()

        return f"Quarantine task {task} on day {day} for {username} on {start_timestamp}"

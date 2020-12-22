from django.db import models
from account.models import User, Profile


class Task(models.Model):

    created_by = models.ForeignKey(
        User, verbose_name="Created By", on_delete=models.CASCADE, null=False, blank=False)
    task_name = models.CharField(
        verbose_name="Task Name", max_length=20, null=False, blank=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        verbose_name="Created At", auto_now_add=True)
    last_reviewed = models.DateTimeField(
        verbose_name="Last Reviewed", auto_now=True)

    def __str__(self):
        return self.task_name


class TaskDetail(models.Model):
    PRIORITY_CHOICES = (
        ('1', 'High'),
        ('2', 'Moderate'),
        ('3', 'Low'),
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, null=False, blank=False)
    assigned_to = models.ForeignKey(
        User, verbose_name="Assigned To", on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(
        verbose_name="Description", null=False, blank=False)
    priority = models.CharField(
        choices=PRIORITY_CHOICES, max_length=9, null=False, blank=False)


class TaskUpdate(models.Model):
    STATUS_CHOICES = (
        ('1', 'Not Started'),
        ('2', 'In Progress'),
        ('3', 'Deferred'),
        ('4', 'Waiting on someone else'),
        ('5', 'Completed'),
    )
    taskdetail = models.ForeignKey(
        TaskDetail, on_delete=models.CASCADE, null=False, blank=False)
    update_info = models.CharField(
        verbose_name="Update Information", max_length=200, null=False, blank=False)
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, null=False, blank=False, default=1)
    updated_at = models.DateTimeField(auto_now=True)
